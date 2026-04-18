#!/usr/bin/env python3
"""
需求挖掘器 — Demand Miner
用 Brave Search 挖掘真实赚钱需求，返回可变现的机会列表
"""

import sys
import json
import argparse
from datetime import datetime

try:
    import requests
    BRAVE_AVAILABLE = True
except ImportError:
    BRAVE_AVAILABLE = False


def search_brave(query: str, count: int = 10) -> list:
    """用 Brave Search 搜索"""
    if not BRAVE_AVAILABLE:
        print("⚠️  requests 未安装，将使用演示数据")
        return get_demo_results(query)
    
    api_key = __import__('os').getenv('BRAVE_API_KEY')
    if not api_key:
        print("⚠️  BRAVE_API_KEY 未设置，将使用演示数据")
        return get_demo_results(query)
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json"
    }
    params = {"q": query, "count": count}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get('web', {}).get('results', [])[:count]:
            results.append({
                "title": item.get('title', ''),
                "url": item.get('url', ''),
                "description": item.get('description', ''),
                "page_age": item.get('page_age', '')
            })
        return results
    except Exception as e:
        print(f"⚠️  搜索失败: {e}，使用演示数据")
        return get_demo_results(query)


def get_demo_results(query: str) -> list:
    """演示数据"""
    demos = {
        "AI工具导航": [
            {"title": "AI工具导航网站大全 - 2024最全AI工具收录", "url": "https://example.com/ai-tools", "description": "收录全球1000+ AI工具，包含AI写作、绘画、代码生成等分类", "page_age": "2024-12"},
            {"title": "最好的AI工具导航站推荐 - Tools目录", "url": "https://example.com/tools", "description": "每日更新AI工具数据库，提供工具对比和用户评测", "page_age": "2024-11"},
            {"title": "AI工具导航源码 - GitHub开源项目", "url": "https://github.com/example/ai-tools", "description": "开源AI工具导航网站模板，支持一键部署", "page_age": "2024-10"},
        ],
        "副业": [
            {"title": "2024年最佳副业推荐 - 在家也能月入过万", "url": "https://example.com/side-hustle", "description": "分享10种真实有效的副业赚钱方法，包含具体步骤", "page_age": "2024-12"},
            {"title": "AI时代的副业机会 - 普通人如何利用AI赚钱", "url": "https://example.com/ai-income", "description": "普通人可做的AI副业，从0到1实战分享", "page_age": "2024-11"},
        ],
    }
    return demos.get(query, [
        {"title": f"关于'{query}'的赚钱机会分析", "url": "https://example.com/demo", "description": "这是一个演示结果，配置BRAVE_API_KEY获取真实数据", "page_age": "2024-12"}
    ])


def analyze_demand(query: str, search_results: list) -> dict:
    """
    分析需求的可变现性
    返回：需求评分、变现模式建议、竞争强度
    """
    # 需求强度信号词
    pain_keywords = ["多少钱", "收费", "付费", "会员", "订阅", "破解", "免费版",
                      "怎么用", "教程", "推荐", "最好", "对比", "评测"]
    
    # 变现信号词
    monetization_signals = ["价格", "套餐", "订阅", "免费试用", "年费", "月付",
                           "买断", " license", "pricing", "plan"]
    
    pain_score = 0
    mon_score = 0
    
    for r in search_results:
        text = (r.get('title', '') + ' ' + r.get('description', '')).lower()
        for kw in pain_keywords:
            if kw in text:
                pain_score += 1
        for kw in monetization_signals:
            if kw in text:
                mon_score += 1
    
    # 评分
    total = len(search_results) * 2
    pain_norm = min(pain_score / max(total, 1), 1.0)
    mon_norm = min(mon_score / max(total, 1), 1.0)
    
    # 竞品数量（搜索结果数）
    competition = len(search_results)
    
    # 需求等级
    if pain_norm > 0.5 and mon_norm > 0.3:
        grade = "A"
        verdict = "✅ 强需求 + 可见变现路径"
    elif pain_norm > 0.3:
        grade = "B"
        verdict = "⚠️ 中等需求，需找差异化切入点"
    elif pain_norm > 0.1:
        grade = "C"
        verdict = "❌ 弱需求，谨慎投入"
    else:
        grade = "D"
        verdict = "❌ 无明确需求信号"
    
    return {
        "query": query,
        "grade": grade,
        "verdict": verdict,
        "pain_signal_score": round(pain_norm * 100),
        "monetization_signal_score": round(mon_norm * 100),
        "competition_count": competition,
        "recommendations": generate_recommendations(grade, pain_norm, mon_norm, competition)
    }


def generate_recommendations(grade: str, pain: float, mon: float, competition: int) -> list:
    """根据分析结果生成建议"""
    recs = []
    
    if grade == "A":
        recs.append("🎯 优先投入，这是验证过的需求")
        if competition > 5:
            recs.append("💡 差异化建议：评测+对比+联盟佣金组合")
        recs.append("🚀 变现路径：联盟营销 + 付费会员")
    elif grade == "B":
        recs.append("🔍 深入调研，找到细分切入点")
        recs.append("💡 可以做，但需要找到差异化角度")
        recs.append("📊 建议先做MVP验证，再决定是否放大")
    elif grade == "C":
        recs.append("⚠️ 需求较弱，建议放弃或转为内容引流")
        recs.append("💡 如果要做，考虑作为辅助产品而非主项目")
    else:
        recs.append("❌ 不建议投入，换个方向")
    
    return recs


def format_output(analysis: dict, search_results: list) -> str:
    """格式化输出为 Markdown"""
    lines = [
        f"# 🔍 需求分析报告：{analysis['query']}",
        f"\n📊 **需求等级：{analysis['grade']}级** — {analysis['verdict']}",
        f"\n| 指标 | 数值 |",
        f"|------|------|",
        f"| 需求信号强度 | {analysis['pain_signal_score']}% |",
        f"| 变现信号强度 | {analysis['monetization_signal_score']}% |",
        f"| 竞品数量 | {analysis['competition_count']}个 |",
        "\n## 💡 建议\n"
    ]
    for rec in analysis['recommendations']:
        lines.append(f"- {rec}")
    
    lines.append("\n## 🔗 搜索结果（信息来源）\n")
    for i, r in enumerate(search_results[:5], 1):
        lines.append(f"{i}. **{r['title']}**")
        lines.append(f"   {r.get('description', '无描述')[:100]}...")
        lines.append(f"   🔗 {r['url']}\n")
    
    lines.append(f"\n---\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="需求挖掘器 — 挖掘真实赚钱机会")
    parser.add_argument("keyword", nargs="?", default="AI工具导航", help="要分析的核心关键词")
    parser.add_argument("--count", "-n", type=int, default=10, help="搜索结果数量")
    parser.add_argument("--json", "-j", action="store_true", help="输出JSON格式")
    args = parser.parse_args()
    
    print(f"🔍 正在搜索: {args.keyword} ...")
    results = search_brave(args.keyword, args.count)
    print(f"✅ 获取到 {len(results)} 条搜索结果")
    
    analysis = analyze_demand(args.keyword, results)
    
    if args.json:
        print(json.dumps({"analysis": analysis, "results": results}, ensure_ascii=False, indent=2))
    else:
        print(format_output(analysis, results))


if __name__ == "__main__":
    main()
