#!/usr/bin/env python3
"""
热点监控器 — Hot Topics Monitor
实时监控全网AI热点，5分钟刷新，支持微信/Push通知
"""

import sys
import json
import time
import argparse
import os
from datetime import datetime, timedelta
from urllib.parse import quote

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# 监控平台配置
PLATFORMS = {
    "weibo": {
        "name": "微博热搜",
        "url": "https://weibo.com/ajax/side/hotSearch",
        "interval": 300,  # 5分钟
    },
    "zhihu": {
        "name": "知乎热榜",
        "url": "https://api.zhihu.com/topstory/hot-lists/total",
        "interval": 600,  # 10分钟
    },
    "baidu": {
        "name": "百度指数",
        "url": "https://top.baidu.com/api",
        "interval": 600,
    },
    "hackernews": {
        "name": "HackerNews",
        "url": "https://hn.algolia.com/api/v1/search?query=AI&tags=story&hitsPerPage=10",
        "interval": 900,
    },
}

# AI关键词
AI_KEYWORDS = [
    "ai", "gpt", "claude", "openai", "llm", "大模型", "文心", "通义", "kimi",
    "deepseek", "copilot", "midjourney", "sora", "gemini", "aigc", "agi",
    "机器学习", "神经网络", "chatgpt", "人工智能", "AI工具", "AI助手"
]

# 状态文件
STATE_FILE = os.path.expanduser("~/.hermes/scripts/hot_topics_state.json")


def fetch_json(url: str, headers: dict = None, timeout: int = 10) -> dict:
    if not REQUESTS_AVAILABLE:
        return {}
    try:
        resp = requests.get(url, headers=headers or {}, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"⚠️  {url}: {e}", file=sys.stderr)
        return {}


def fetch_weibo() -> list:
    data = fetch_json(PLATFORMS["weibo"]["url"])
    items = data.get("data", {}).get("realtime", [])[:20]
    return [{"rank": i+1, "word": item.get("word",""), "num": item.get("num","")}
            for i, item in enumerate(items)]


def fetch_zhihu() -> list:
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.zhihu.com/"}
    data = fetch_json(PLATFORMS["zhihu"]["url"], headers=headers)
    items = data.get("data", [])[:20]
    return [{"rank": i+1, "title": item.get("target",{}).get("title",""),
             "url": item.get("target",{}).get("url","").replace("https://www.zhihu.com","")}
            for i, item in enumerate(items)]


def fetch_hackernews() -> list:
    data = fetch_json(PLATFORMS["hackernews"]["url"])
    items = data.get("hits", [])[:10]
    return [{"rank": i+1, "title": item.get("title",""), "url": item.get("url",""),
             "points": item.get("points",0)} for i, item in enumerate(items)]


def is_ai_related(text: str) -> bool:
    t = text.lower()
    return any(kw.lower() in t for kw in AI_KEYWORDS)


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {"last_alerts": {}, "history": []}


def save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False)


def check_new(platform: str, items: list) -> list:
    """检测新增热点"""
    state = load_state()
    last = state.get("last_alerts", {}).get(platform, [])
    last_words = set(last)
    new_items = [item for item in items if item.get("word", item.get("title","")) not in last_words]
    state["last_alerts"][platform] = [item.get("word", item.get("title","")) for item in items[:10]]
    save_state(state)
    return new_items


def format_alert(platform: str, new_items: list) -> str:
    if not new_items:
        return ""
    lines = [f"🔥 **{PLATFORMS[platform]['name']}** 新上榜:"]
    for item in new_items[:5]:
        word = item.get("word", item.get("title",""))
        if "rank" in item:
            lines.append(f"  #{item['rank']} {word}")
        else:
            lines.append(f"  • {word}")
    return "\n".join(lines)


def send_wechat_alert(message: str) -> bool:
    """发送微信通知"""
    wx_hook = os.getenv("WX_WORK_WEBHOOK") or os.getenv("WECOM_WEBHOOK")
    if not wx_hook:
        return False
    try:
        resp = requests.post(wx_hook, json={"msgtype": "text", "text": {"content": message}}, timeout=10)
        return resp.status_code == 200
    except Exception:
        return False


def format_report(all_results: dict) -> str:
    lines = [
        f"# 🔥 AI热点监控日报",
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
    ]
    for platform, items in all_results.items():
        ai_items = [it for it in items if is_ai_related(it.get("word","") or it.get("title",""))]
        if ai_items:
            lines.append(f"\n## {PLATFORMS[platform]['name']} 🤖")
            for it in ai_items[:5]:
                rank = it.get("rank","")
                word = it.get("word", it.get("title",""))
                lines.append(f"{rank}. {word}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="热点监控器")
    parser.add_argument("--platforms", "-p", default="weibo,zhihu,hackernews")
    parser.add_argument("--json", "-j", action="store_true")
    parser.add_argument("--watch", "-w", action="store_true", help="持续监控模式")
    parser.add_argument("--interval", "-i", type=int, default=300, help="检查间隔(秒)")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]

    def run_once():
        results = {}
        for p in platforms:
            try:
                if p == "weibo": results[p] = fetch_weibo()
                elif p == "zhihu": results[p] = fetch_zhihu()
                elif p == "hackernews": results[p] = fetch_hackernews()
            except Exception as e:
                print(f"⚠️  {p}: {e}")
                results[p] = []

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(format_report(results))

        # 检测新热点并通知
        new_count = 0
        alerts = []
        for p, items in results.items():
            new_items = check_new(p, items)
            if new_items:
                new_count += len(new_items)
                alert = format_alert(p, new_items)
                if alert:
                    alerts.append(alert)

        if alerts and not args.json:
            alert_msg = "🔥 AI热点提醒\n" + "\n".join(alerts)
            print("\n" + alert_msg)
            if send_wechat_alert(alert_msg):
                print("✅ 微信通知已发送")

        return new_count

    if args.watch:
        print(f"👀 启动监控模式，每{args.interval}秒检查一次...")
        while True:
            n = run_once()
            print(f"⏰ {datetime.now().strftime('%H:%M:%S')} 完成，检测到{new_count}个新热点")
            time.sleep(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
