#!/usr/bin/env python3
"""
竞品雷达 — Competitor Radar
分析竞争对手的变现模式、流量、SEO、差异化，给出可操作建议
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


# 变现模式特征库
MONETIZATION_PATTERNS = {
    "affiliate": {
        "keywords": ["affiliate", "commission", "partner", "推荐", "佣金", "返现"],
        "indicators": ["?ref=", "/partner/", "affiliate", "联盟"],
        "commission_range": "10-50%",
        "speed": "快（1-2周)"
    },
    "subscription": {
        "keywords": ["pricing", "plan", "subscription", "monthly", "yearly", "套餐", "订阅", "月付", "年费"],
        "indicators": ["/pricing", "/plans", "免费试用", "免费注册"],
        "commission_range": "N/A",
        "speed": "中（1-3月)"
    },
    "ads": {
        "keywords": ["advertise", "ads", "advertisement", "赞助商", "广告"],
        "indicators": ["google adsense", "adsense", "/ads/", "广告位"],
        "commission_range": "$2-10 CPM",
        "speed": "快（1月)"
    },
    "freemium": {
        "keywords": ["free", "premium", "pro", "upgrade", "免费", "高级", "专业版"],
        "indicators": ["免费版", "付费版", "免费试用", "Get Started"],
        "commission_range": "N/A",
        "speed": "中（1-2月)"
    },
    "affiliate+content": {
        "keywords": ["review", "best", "top", "compare", "评测", "推荐", "对比", "排行榜"],
        "indicators": ["最佳", "TOP", "榜单", "review", "comparison"],
        "commission_range": "5-30%",
        "speed": "中（2-4月)"
    }
}


def fetch_page_text(url: str, timeout: int = 8) -> str:
    """抓取页面文本（简化版，不用Playwright）"""
    if not requests:
        return ""
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        # 简单去HTML标签
        text = resp.text
        import re
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:3000]  # 限制长度
    except Exception:
        return ""


def detect_monetization(page_text: str, url: str) -> dict:
    """检测页面变现模式"""
    text_lower = page_text.lower()
    scores = {}
    
    for pattern_name, pattern_data in MONETIZATION_PATTERNS.items():
        score = 0
        for kw in pattern_data["keywords"]:
            if kw.lower() in text_lower:
                score += 2
        for ind in pattern_data["indicators"]:
            if ind.lower() in url.lower():
                score += 1
        if score > 0:
            scores[pattern_name] = {
                "score": score,
                "range": pattern_data["commission_range"],
                "speed": pattern_data["speed"]
            }
    
    if not scores:
        return {"type": "unknown", "score": 0, "range": "N/A", "speed": "未知"}
    
    best = max(scores.items(), key=lambda x: x[1]["score"])
    
    # 组合模式检测
    if "affiliate" in scores and "affiliate+content" in scores:
        return {"type": "affiliate+content", "score": scores["affiliate+content"]["score"],
                "range": "10-30%", "speed": "中(2-4月)"}
    
    return {"type": best[0], "score": best[1]["score"],
            "range": best[1]["range"], "speed": best[1]["speed"]}


def analyze_competitor(url: str, name: str = "") -> dict:
    """分析单个竞品"""
    page_text = fetch_page_text(url)
    monetization = detect_monetization(page_text, url)
    
    # 简易流量估算（基于页面规模）
    page_size_estimate = len(page_text)
    traffic_estimate = "未知"
    if page_size_estimate > 10000:
        traffic_estimate = "月均1万+"
    if page_size_estimate > 50000:
        traffic_estimate = "月均10万+"
    if page_size_estimate > 100000:
        traffic_estimate = "月均50万+"
    
    # 检测SEO友好度
    seo_signals = {
        "title": "title" in page_text[:500],
        "meta_desc": "description" in page_text[:1000],
        "headings": "h1" in page_text or "h2" in page_text,
    }
    seo_score = sum(seo_signals.values()) * 25
    
    # 检测内容质量
    content_words = len(page_text.split())
    content_quality = "低" if content_words < 200 else "中" if content_words < 1000 else "高"
    
    return {
        "name": name or url,
        "url": url,
        "monetization": monetization,
        "traffic_estimate": traffic_estimate,
        "seo_score": seo_score,
        "content_quality": content_quality,
        "page_words": content_words,
        "strengths": get_strengths(seo_score, content_words, monetization),
        "weaknesses": get_weaknesses(seo_score, content_words, monetization),
    }


def get_strengths(seo: int, words: int, mon: dict) -> list:
    s = []
    if seo >= 75: s.append("SEO优化良好")
    if words >= 1000: s.append("内容丰富")
    if mon["type"] == "affiliate+content": s.append("内容+变现结合好")
    if mon["type"] == "subscription": s.append("高利润率订阅模式")
    return s


def get_weaknesses(seo: int, words: int, mon: dict) -> list:
    w = []
    if seo < 50: w.append("SEO薄弱，可超越机会")
    if words < 500: w.append("内容单薄，用户体验差")
    if mon["type"] == "unknown": w.append("变现模式不清晰")
    if mon["type"] == "ads": w.append("仅靠广告，依赖流量")
    return w


def format_report(competitors: list) -> str:
    """生成 Markdown 报告"""
    lines = [
        "# 🔬 竞品分析报告",
        f"\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n",
        "\n## 📊 概览\n",
        f"| # | 竞品 | 变现模式 | 佣金范围 | 预估流量 | SEO评分 | 内容质量 |",
        f"|---|------|---------|---------|---------|--------|---------|"
    ]
    
    for i, c in enumerate(competitors, 1):
        mon_icon = {"affiliate": "💰", "subscription": "📋", "ads": "📢", 
                    "freemium": "🆓", "affiliate+content": "📝"}.get(c["monetization"]["type"], "❓")
        lines.append(
            f"| {i} | [{c['name']}]({c['url']}) | {mon_icon} {c['monetization']['type']} | "
            f"{c['monetization']['range']} | {c['traffic_estimate']} | "
            f"{c['seo_score']}分 | {c['content_quality']} |"
        )
    
    # 差异化建议
    lines.extend(["\n## 💡 差异化切入点\n"])
    
    all_weak = []
    for c in competitors:
        all_weak.extend(c["weaknesses"][:1])  # 每个竞品取一个弱点
    
    if all_weak:
        counter = 1
        for w in list(set(all_weak))[:3]:
            lines.append(f"{counter}. 针对：{w} → 做差异化")
            counter += 1
    
    # 变现建议
    lines.extend(["\n## 💰 变现建议\n"])
    mon_types = [c["monetization"]["type"] for c in competitors]
    if "affiliate" in mon_types or "affiliate+content" in mon_types:
        lines.append("- 联盟营销是最快验证的变现路径 ✅")
    if "subscription" in mon_types:
        lines.append("- 高级功能/去广告可做付费订阅")
    if "ads" in mon_types:
        lines.append("- ⚠️ 纯广告依赖流量，建议增加联盟收入")
    
    # 行动清单
    lines.extend(["\n## 🎯 立即可执行\n"])
    lines.append("1. 注册竞品的联盟计划（Amazon Associates / 工具官方返佣）")
    lines.append("2. 借鉴竞品的工具评测框架，写更详细的评测")
    lines.append("3. 在知乎回答相关问题，带上你的网站链接")
    lines.append("4. 每周更新3-5个工具，保持内容新鲜度")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="竞品雷达 — 分析竞争对手")
    parser.add_argument("--urls", "-u", nargs="+", default=[], help="竞品URL列表")
    parser.add_argument("--file", "-f", type=str, help="从文件读取URL列表（一行一个）")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()
    
    urls = args.urls
    if args.file and os.path.exists(args.file):
        urls = [line.strip() for line in open(args.file) if line.strip() and not line.startswith('#')]
    
    if not urls:
        # 默认竞品
        urls = [
            "https://tools.cn",
            "https://ai-bot.cn",
        ]
        print(f"ℹ️  未提供URL，使用默认演示竞品：{urls}")
    
    print(f"🔍 开始分析 {len(urls)} 个竞品...")
    
    results = []
    for url in urls:
        print(f"  📡 分析: {url}")
        result = analyze_competitor(url)
        results.append(result)
        print(f"    → 变现: {result['monetization']['type']} | SEO: {result['seo_score']}分")
    
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(format_report(results))


if __name__ == "__main__":
    main()
