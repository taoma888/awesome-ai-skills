#!/usr/bin/env python3
"""
热点发现器 — Trending Hunter
抓取多平台热搜，筛选AI相关热点，自动生成选题建议
"""

import sys
import json
import argparse
import os
from datetime import datetime
from urllib.parse import quote

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# 热搜数据源（免费，无需API Key）
ENDPOINTS = {
    "weibo": {
        "name": "微博热搜",
        "url": "https://weibo.com/ajax/side/hotSearch",
        "parse": lambda r: [
            {"rank": i+1, "word": item.get("word",""), "num": item.get("num","")}
            for i, item in enumerate(r.get("data", {}).get("realtime", [])[:20])
        ]
    },
    "zhihu": {
        "name": "知乎热榜",
        "url": "https://api.zhihu.com/topstory/hot-lists/total",
        "parse": lambda r: [
            {"rank": i+1, "title": item.get("target",{}).get("title",""),
             "answer_count": item.get("target",{}).get("answer_count","")}
            for i, item in enumerate(r.get("data", [])[:20])
        ]
    },
    "baidu": {
        "name": "百度热搜",
        "url": "https://top.baidu.com/api?sa=pcindex_hot",
        "parse": lambda r: [
            {"rank": i+1, "word": item.get("query",""), "desc": item.get("desc","")}
            for i, item in enumerate(r.get("result", [])[:20])
        ]
    },
}


def fetch_json(url: str, headers: dict = None, timeout: int = 10) -> dict:
    """通用JSON请求"""
    if not REQUESTS_AVAILABLE:
        return {}
    default_headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)',
        'Accept': 'application/json',
    }
    if headers:
        default_headers.update(headers)
    try:
        resp = requests.get(url, headers=default_headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"⚠️  请求失败 {url}: {e}", file=sys.stderr)
        return {}


def fetch_weibo() -> list:
    """微博热搜"""
    data = fetch_json(ENDPOINTS["weibo"]["url"])
    items = ENDPOINTS["weibo"]["parse"](data)
    return items


def fetch_zhihu() -> list:
    """知乎热榜"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://www.zhihu.com/'
    }
    data = fetch_json(ENDPOINTS["zhihu"]["url"], headers=headers)
    items = ENDPOINTS["zhihu"]["parse"](data)
    return items


def fetch_baidu() -> list:
    """百度热搜"""
    data = fetch_json(ENDPOINTS["baidu"]["url"])
    items = ENDPOINTS["baidu"]["parse"](data)
    return items


def fetch_all(platforms: list = None) -> dict:
    """获取所有平台热搜"""
    all_platforms = list(ENDPOINTS.keys())
    platforms = platforms or all_platforms
    
    results = {}
    for p in platforms:
        if p == "weibo":
            results["weibo"] = fetch_weibo()
        elif p == "zhihu":
            results["zhihu"] = fetch_zhihu()
        elif p == "baidu":
            results["baidu"] = fetch_baidu()
        else:
            print(f"⚠️  未知平台: {p}")
    
    return results


# AI相关关键词过滤
AI_KEYWORDS = [
    "ai", "人工智能", "chatgpt", "gpt", "claude", "openai", "大模型",
    "LLM", "文心", "通义", "kimi", "deepseek", "豆包", "智谱", "Copilot",
    "AI", "绘画", "GPT", "Claude", "Midjourney", "Sora", "Gemini",
    "机器学习", "神经网络", "AI工具", "AI助手", "AI写作", "AI绘画",
    "AI视频", "AI编程", "AI搜索", "AIGC", "AGI"
]


def is_ai_related(text: str) -> bool:
    """判断是否与AI相关"""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in AI_KEYWORDS)


def filter_ai_trending(results: dict) -> list:
    """过滤出AI相关的热点"""
    ai_items = []
    
    for platform, items in results.items():
        for item in items:
            # 微博
            if platform == "weibo" and is_ai_related(item.get("word", "")):
                ai_items.append({
                    "platform": "微博",
                    "rank": item["rank"],
                    "keyword": item["word"],
                    "hot_score": item.get("num", "未知"),
                    "source": "weibo"
                })
            # 知乎
            elif platform == "zhihu" and is_ai_related(item.get("title", "")):
                ai_items.append({
                    "platform": "知乎",
                    "rank": item["rank"],
                    "keyword": item["title"],
                    "answer_count": item.get("answer_count", "未知"),
                    "source": "zhihu"
                })
            # 百度
            elif platform == "baidu" and is_ai_related(item.get("word", "")):
                ai_items.append({
                    "platform": "百度",
                    "rank": item["rank"],
                    "keyword": "word",
                    "desc": item.get("desc", ""),
                    "source": "baidu"
                })
    
    return ai_items


def generate_content_ideas(ai_items: list, limit: int = 5) -> list:
    """为AI热点生成内容选题"""
    ideas = []
    for item in ai_items[:limit]:
        keyword = item.get("keyword", item.get("title", ""))
        
        # 生成3种不同角度的标题
        angles = [
            f"🔥 {keyword}来了！实测体验+赚钱机会分析",
            f"💡 深度：{keyword}将如何改变你的工作？",
            f"📊 {keyword}最新动态！附入门教程+变现思路"
        ]
        
        ideas.append({
            "platform": item["platform"],
            "rank": item["rank"],
            "keyword": keyword,
            "angles": angles,
            "urgency": "🔥 今日热点" if item["rank"] <= 5 else "📈 上升热点",
            "best_format": "测评+教程" if item["rank"] <= 3 else "资讯+解读"
        })
    
    return ideas


def format_report(results: dict, ai_items: list, ideas: list) -> str:
    lines = [
        f"# 🔥 AI 热点日报",
        f"\n📅 **{datetime.now().strftime('%Y-%m-%d %H:%M')}**\n",
        "\n## 🤖 AI 相关热点\n"
    ]
    
    if not ai_items:
        lines.append("*今日暂无AI相关热点，自动扩展到科技领域*\n")
    
    for item in ai_items[:10]:
        lines.append(f"- **{item['platform']}** #{item['rank']} {item.get('keyword','')}")
    
    lines.extend(["\n## ✍️ 内容选题建议\n"])
    
    for idea in ideas:
        lines.append(f"\n### 📌 {idea['urgency']} | {idea['platform']} #{idea['rank']}")
        lines.append(f"**核心词**: {idea['keyword']}")
        lines.append(f"**推荐格式**: {idea['best_format']}\n")
        lines.append("**可选标题:**")
        for angle in idea['angles']:
            lines.append(f"- {angle}")
    
    # 今日操作建议
    if ideas:
        best = ideas[0]
        lines.extend([
            "\n---\n",
            "\n## ⚡ 今日最佳行动\n",
            f"> 🎯 选择 **'{best['keyword']}'** 作为今日选题",
            f"> 📝 格式：{best['best_format']}",
            f"> 🔗 发布平台：知乎 + 微信公众号 + aisstt.fun\n"
        ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="热点发现器 — 挖掘AI相关热点")
    parser.add_argument("--platforms", "-p", default="weibo,zhihu",
                       help="平台列表，逗号分隔: weibo,zhihu,baidu")
    parser.add_argument("--limit", "-n", type=int, default=5, help="选题数量")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    parser.add_argument("--no-filter", "-f", action="store_true", help="不过滤AI关键词")
    args = parser.parse_args()
    
    platforms = [x.strip() for x in args.platforms.split(",")]
    
    print(f"🔍 抓取 {platforms} 热搜中...")
    results = fetch_all(platforms)
    
    total = sum(len(v) for v in results.values())
    print(f"✅ 获取到 {total} 条热搜")
    
    if args.no_filter:
        ai_items = []
        for platform, items in results.items():
            for i, item in enumerate(items, 1):
                item["source"] = platform
                item["platform"] = platform.capitalize()
                item["rank"] = i
                ai_items.append(item)
    else:
        ai_items = filter_ai_trending(results)
        print(f"🤖 其中 AI 相关：{len(ai_items)} 条")
    
    ideas = generate_content_ideas(ai_items, args.limit)
    
    if args.json:
        print(json.dumps({
            "raw": results,
            "ai_filtered": ai_items,
            "ideas": ideas
        }, ensure_ascii=False, indent=2))
    else:
        print(format_report(results, ai_items, ideas))


if __name__ == "__main__":
    main()
