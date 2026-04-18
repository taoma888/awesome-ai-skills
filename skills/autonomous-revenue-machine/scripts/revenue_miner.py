#!/usr/bin/env python3
"""
💰 Revenue Miner — 变现机会挖掘器
自动扫描全网变现机会，返回可执行方案
"""

import sys
import json
import re
import argparse
import os
from datetime import datetime, timedelta
from urllib.parse import quote

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# AI关键词（商业化相关）
AI_KEYWORDS = [
    "ai", "gpt", "claude", "llm", "大模型", "文心", "通义", "kimi",
    "deepseek", "copilot", "midjourney", "sora", "gemini", "aigc",
    "机器学习", "chatgpt", "人工智能", "AI工具", "AI助手", "AI写作",
    "AI绘画", "AI视频", "AI配音", "AI代码"
]

# 变现关键词
MONETIZE_KEYWORDS = [
    "付费", "订阅", "会员", "收费", "价格", "套餐",
    "优惠", "折扣", "年费", "月费", "免费试用",
    " affiliate", "佣金", "推广", "赚钱", "变现"
]

# 平台配置
PLATFORMS = {
    "weibo": {
        "name": "微博热搜",
        "url": "https://weibo.com/ajax/side/hotSearch",
        "type": "social"
    },
    "zhihu": {
        "name": "知乎热榜",
        "url": "https://api.zhihu.com/topstory/hot-lists/total",
        "type": "qna"
    },
    "hackernews": {
        "name": "HackerNews",
        "url": "https://hn.algolia.com/api/v1/search?query=AI+monetize&tags=story&hitsPerPage=20",
        "type": "tech"
    },
    "reddit": {
        "name": "Reddit SideProject",
        "url": "https://www.reddit.com/r/SideProject/hot.json?limit=20",
        "type": "community"
    }
}


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
    items = data.get("data", {}).get("realtime", [])[:30]
    return [{"rank": i+1, "word": item.get("word",""), "num": item.get("num",""), "label_name": item.get("label_name","")}
            for i, item in enumerate(items)]


def fetch_zhihu() -> list:
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.zhihu.com/"}
    data = fetch_json(PLATFORMS["zhihu"]["url"], headers=headers)
    items = data.get("data", [])[:20]
    result = []
    for i, item in enumerate(items):
        target = item.get("target", {})
        title = target.get("title","")
        result.append({
            "rank": i+1,
            "title": title,
            "url": target.get("url","").replace("https://www.zhihu.com",""),
            "answer_count": target.get("answer_count", 0),
            "follower_count": target.get("follower_count", 0)
        })
    return result


def fetch_hackernews() -> list:
    data = fetch_json(PLATFORMS["hackernews"]["url"])
    items = data.get("hits", [])[:20]
    return [{"rank": i+1, "title": item.get("title",""), "url": item.get("url",""),
             "points": item.get("points",0), "comments": item.get("num_comments",0)}
            for i, item in enumerate(items)]


def fetch_reddit() -> list:
    headers = {"User-Agent": "Mozilla/5.0"}
    data = fetch_json(PLATFORMS["reddit"]["url"], headers=headers)
    posts = data.get("data", {}).get("children", [])[:20]
    return [{"rank": i+1, "title": p.get("data",{}).get("title",""),
             "score": p.get("data",{}).get("score",0),
             "num_comments": p.get("data",{}).get("num_comments",0),
             "url": p.get("data",{}).get("url","")}
            for i, p in enumerate(posts)]


def is_monetizable(text: str) -> bool:
    """检测文本是否与变现/商业化相关"""
    t = text.lower()
    has_monetize = any(kw.lower() in t for kw in MONETIZE_KEYWORDS)
    has_ai = any(kw.lower() in t for kw in AI_KEYWORDS)
    return has_monetize or has_ai


def score_opportunity(text: str, platform: str, metrics: dict = None) -> int:
    """计算变现机会评分"""
    score = 0
    text_lower = text.lower()
    
    # AI相关度
    ai_count = sum(1 for kw in AI_KEYWORDS if kw.lower() in text_lower)
    score += min(ai_count * 3, 15)
    
    # 变现相关度
    mon_count = sum(1 for kw in MONETIZE_KEYWORDS if kw.lower() in text_lower)
    score += min(mon_count * 4, 20)
    
    # 平台加成
    if platform == "reddit":
        score += 5  # 社区讨论质量高
    elif platform == "zhihu":
        score += 3  # 问答平台，需求明确
    elif platform == "hackernews":
        score += 4  # Tech圈，创新项目多
    
    # 互动指标
    if metrics:
        if "num" in metrics:  # 热搜热度
            score += min(int(metrics["num"]) // 1000, 10)
        if "points" in metrics:  # HN票数
            score += min(metrics["points"] // 10, 15)
        if "score" in metrics:  # Reddit评分
            score += min(metrics["score"] // 50, 10)
        if "answer_count" in metrics:
            score += min(metrics["answer_count"] // 10, 8)
        if "follower_count" in metrics:
            score += min(metrics["follower_count"] // 1000, 10)
        if "num_comments" in metrics:
            score += min(metrics["num_comments"] // 20, 8)
    
    return score


def suggest_monetization(text: str, score: int) -> dict:
    """基于文本内容推断变现路径"""
    text_lower = text.lower()
    suggestions = []
    
    # 工具类 → 联盟营销
    tool_indicators = ["工具", "软件", "app", "网站", "platform", "tool", "app"]
    if any(ind in text_lower for ind in tool_indicators):
        suggestions.append({
            "path": "联盟营销 (Affiliate)",
            "est_monthly": "¥500-5000",
            "action": "申请该工具的联盟计划，生成推广内容"
        })
    
    # 教程/课程类 → 知识付费
    learn_indicators = ["教程", "学习", "课程", "how to", "tutorial", "guide", "入门"]
    if any(ind in text_lower for ind in learn_indicators):
        suggestions.append({
            "path": "知识付费 (Digital Products)",
            "est_monthly": "¥300-3000",
            "action": "制作教程视频/文档，在抖音/小红书/知乎发布"
        })
    
    # 资源类 → 付费订阅
    resource_indicators = ["资源", "下载", "模板", "素材", "prompt", "资源包"]
    if any(ind in text_lower for ind in resource_indicators):
        suggestions.append({
            "path": "资源订阅 (Subscription)",
            "est_monthly": "¥200-2000",
            "action": "整理资源包，设置付费订阅或单次购买"
        })
    
    # 服务类 → 咨询/代运营
    service_indicators = ["运营", "推广", "营销", "增长", "seo", "增长黑客"]
    if any(ind in text_lower for ind in service_indicators):
        suggestions.append({
            "path": "服务变现 (Services)",
            "est_monthly": "¥1000-10000",
            "action": "提供AI工具使用培训、代运营服务"
        })
    
    # 默认建议
    if not suggestions:
        suggestions.append({
            "path": "内容流量变现 (Ads/联盟)",
            "est_monthly": "¥100-1000",
            "action": "围绕该话题创作内容，通过广告+联盟变现"
        })
    
    return {
        "score": score,
        "level": "🔥 HOT" if score >= 30 else "⚡ WARM" if score >= 20 else "💤 COOL",
        "suggestions": suggestions[:2],  # 最多2个变现路径
        "priority": "HIGH" if score >= 25 else "MEDIUM" if score >= 15 else "LOW"
    }


def format_report(all_results: dict) -> str:
    lines = [
        f"# 💰 变现机会雷达报告",
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
        f"扫描平台: {', '.join(all_results.keys())}\n",
    ]
    
    # 汇总所有内容
    all_items = []
    for platform, items in all_results.items():
        for item in items:
            text = item.get("word", "") or item.get("title", "")
            if not is_monetizable(text):
                continue
            
            metrics = {k: v for k, v in item.items() if k not in ["rank", "word", "title"]}
            score = score_opportunity(text, platform, metrics)
            analysis = suggest_monetization(text, score)
            
            if score >= 15:  # 只展示15分以上的机会
                all_items.append({
                    "platform": platform,
                    "text": text,
                    "score": score,
                    "level": analysis["level"],
                    "priority": analysis["priority"],
                    "suggestions": analysis["suggestions"],
                    "metrics": metrics
                })
    
    # 按分数排序
    all_items.sort(key=lambda x: x["score"], reverse=True)
    
    if not all_items:
        lines.append("\n😴 暂无高价值变现机会，稍后再来...")
        return '\n'.join(lines)
    
    lines.append(f"## 🔥 TOP {min(10, len(all_items))} 变现机会\n")
    
    for i, item in enumerate(all_items[:10], 1):
        platform_name = PLATFORMS.get(item["platform"], {}).get("name", item["platform"])
        text = item["text"]
        score = item["score"]
        level = item["level"]
        priority = item["priority"]
        suggestions = item["suggestions"]
        
        lines.append(f"### {i}. {level} [{platform_name}] {text}")
        lines.append(f"**评分**: {score} | **优先级**: {priority}")
        
        if item["metrics"]:
            metric_str = " | ".join([f"{k}: {v}" for k, v in list(item["metrics"].items())[:3]])
            lines.append(f"**数据**: {metric_str}")
        
        lines.append(f"\n**💡 变现路径:**")
        for s in suggestions:
            lines.append(f"- [{s['path']}] 预估: {s['est_monthly']}")
            lines.append(f"  → {s['action']}")
        lines.append("")
    
    # 行动建议
    lines.append("## 🎯 立即行动\n")
    if all_items:
        top = all_items[0]
        lines.append(f"**最高优先**: {top['text']}")
        for s in top["suggestions"][:1]:
            lines.append(f"  → {s['action']}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="💰 变现机会挖掘器")
    parser.add_argument("--platforms", "-p", default="weibo,zhihu,hackernews,reddit")
    parser.add_argument("--min-score", "-s", type=int, default=15, help="最低评分阈值")
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")]
    
    print(f"🔍 扫描变现机会中 ({datetime.now().strftime('%H:%M:%S')})...")
    
    results = {}
    for p in platforms:
        try:
            if p == "weibo":
                results[p] = fetch_weibo()
            elif p == "zhihu":
                results[p] = fetch_zhihu()
            elif p == "hackernews":
                results[p] = fetch_hackernews()
            elif p == "reddit":
                results[p] = fetch_reddit()
        except Exception as e:
            print(f"⚠️  {p}: {e}")
            results[p] = []
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_report(results))


if __name__ == "__main__":
    main()
