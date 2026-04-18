#!/usr/bin/env python3
"""
自动发布器 — Auto Publisher
将文章一键发布到多个平台：D1数据库 / 微信公众号 / 知乎 / 微博
"""

import sys
import json
import argparse
import os
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None


def publish_to_d1(article_md: str, title: str, category: str = "AI资讯") -> dict:
    """发布到 Cloudflare D1 数据库"""
    db_id = os.getenv("D1_DATABASE_ID")
    account_id = os.getenv("CF_ACCOUNT_ID")
    api_token = os.getenv("CF_API_TOKEN")

    if not all([db_id, account_id, api_token]):
        return {"success": False, "error": "缺少环境变量: D1_DATABASE_ID, CF_ACCOUNT_ID, CF_API_TOKEN"}

    # 从Markdown提取内容（简化处理）
    import re
    content_clean = re.sub(r'#+\s+', '', article_md)
    content_clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content_clean)
    content_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', content_clean)

    # 提取第一段作为摘要
    paragraphs = [p.strip() for p in content_clean.split('\n') if p.strip()]
    excerpt = paragraphs[0][:200] if paragraphs else ""

    sql = f"""
    INSERT INTO articles (title, content, excerpt, category, author, status, created_at)
    VALUES (
      '{title.replace("'", "''")}',
      '{content_clean.replace("'", "''")[:10000]}',
      '{excerpt.replace("'", "''")}',
      '{category}',
      'HermesAI',
      'published',
      '{datetime.now().isoformat()}'
    )
    """

    try:
        resp = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{account_id}/d1/database/{db_id}/query",
            headers={
                "Authorization": f"Bearer {api_token}",
                "Content-Type": "application/json"
            },
            json={"sql": sql},
            timeout=15
        )
        resp.raise_for_status()
        result = resp.json()
        if result.get("success"):
            return {"success": True, "platform": "D1", "article_id": result.get("result", [{}])[0].get("id")}
        return {"success": False, "error": str(result)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def publish_to_weixin(article_md: str, title: str) -> dict:
    """发布到微信公众号"""
    # 微信公众号需要access_token（需配置）
    appid = os.getenv("WX_APPID")
    appsecret = os.getenv("WX_APPSECRET")

    if not all([appid, appsecret]):
        return {"success": False, "error": "缺少微信参数: WX_APPID, WX_APPSECRET"}

    try:
        # 获取access_token
        token_resp = requests.get(
            "https://api.weixin.qq.com/cgi-bin/token",
            params={"grant_type": "client_credential", "appid": appid, "secret": appsecret},
            timeout=10
        )
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            return {"success": False, "error": f"获取token失败: {token_data}"}

        # 上传图文消息
        import re
        content_html = md_to_wx(article_md)

        payload = {
            "articles": [{
                "thumb_media_id": "",
                "author": "HermesAI",
                "title": title,
                "digest": title[:54],
                "content": content_html,
                "content_source_url": "",
                "need_open_comment": 1,
                "only_fans_can_comment": 0
            }]
        }

        resp = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={access_token}",
            json=payload,
            timeout=10
        )
        result = resp.json()
        if result.get("media_id"):
            return {"success": True, "platform": "微信公众号", "media_id": result["media_id"]}
        return {"success": False, "error": str(result)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def md_to_wx(md: str) -> str:
    """Markdown转微信HTML（简化版）"""
    import re
    html = md
    html = re.sub(r'<[^>]+>', '', html)
    html = re.sub(r'#+\s+([^\n]+)', r'<h2>\1</h2>', html)
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\n\n+', '\n', html)
    html = html.replace('\n', '<br/>')
    return html


def save_local(article_md: str, title: str, output_dir: str = "output") -> dict:
    """保存到本地文件"""
    os.makedirs(output_dir, exist_ok=True)
    # 生成安全文件名
    safe_title = re.sub(r'[^\w\s\u4e00-\u9fff-]', '', title)[:30]
    safe_title = safe_title.replace(' ', '-')
    filename = f"{output_dir}/{safe_title}_{datetime.now().strftime('%Y%m%d')}.md"

    import re
    full_content = f"---\ntitle: {title}\ndate: {datetime.now().isoformat()}\n---\n\n{article_md}"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return {"success": True, "platform": "本地文件", "file": filename}


def main():
    parser = argparse.ArgumentParser(description="自动发布器")
    parser.add_argument("--file", "-f", required=True, help="文章文件路径(.md)")
    parser.add_argument("--title", "-t", help="文章标题（默认从文件读取）")
    parser.add_argument("--platforms", "-p", default="local",
                       help="发布平台: d1,weixin,local (逗号分隔)")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()

    # 读取文章
    if not os.path.exists(args.file):
        print(f"❌ 文件不存在: {args.file}")
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取标题
    import re
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = args.title or title_match.group(1) if title_match else "无标题文章"

    print(f"📤 发布文章：{title}")
    print(f"   平台：{args.platforms}")

    results = []
    platforms = [p.strip() for p in args.platforms.split(',')]

    for platform in platforms:
        if platform == "d1":
            r = publish_to_d1(content, title)
            results.append(r)
            status = "✅" if r["success"] else "❌"
            print(f"   {status} D1: {r.get('error', r.get('article_id', 'OK'))}")
        elif platform == "weixin":
            r = publish_to_weixin(content, title)
            results.append(r)
            status = "✅" if r["success"] else "❌"
            print(f"   {status} 微信: {r.get('error', r.get('media_id', 'OK'))}")
        elif platform == "local":
            r = save_local(content, title)
            results.append(r)
            print(f"   ✅ 本地: {r['file']}")

    success = sum(1 for r in results if r["success"])
    print(f"\n🎉 完成：{success}/{len(results)} 平台发布成功")

    if args.json:
        print(json.dumps({"title": title, "results": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
