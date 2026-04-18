#!/usr/bin/env python3
"""
🔥 Social Traffic Siphon — 社媒流量虹吸器
生成适配微博/知乎/小红书的病毒传播内容
"""

import sys
import json
import re
import argparse
import os
from datetime import datetime

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# 各平台最优发帖时间
OPTIMAL_TIMES = {
    "weibo": ["07:30", "12:30", "18:30", "22:30"],
    "zhihu": ["20:00", "21:00", "21:30"],
    "xiaohongshu": ["07:30", "12:00", "19:30", "20:00"],
    "wechat": ["08:00", "12:30", "21:00"]
}

# 平台字数限制
CHAR_LIMITS = {
    "weibo": {"min": 50, "max": 300, "optimal": 210},
    "zhihu": {"min": 500, "max": 3000, "optimal": 1200},
    "xiaohongshu": {"min": 200, "max": 1000, "optimal": 600},
    "wechat": {"min": 1000, "max": 5000, "optimal": 2000}
}


# 标题模板库
HEADLINE_TEMPLATES = {
    "震惊体": ["竟然", "99%的人都不知道", "央视曝光", "删前速看", "颠覆认知"],
    "数字体": ["3个技巧", "7天搞定", "1分钟学会", "5个方法", "30天改变"],
    "问题体": ["为什么", "如何", "怎么", "要不要", "是不是"],
    "对比体": ["vs", "VS", "对比", " PK ", "哪个好"],
    "利益体": ["省钱", "赚钱", "提效", "涨粉", "暴富"]
}

# hashtag 库
HASHTAG_TEMPLATES = {
    "ai": ["#AI工具", "#人工智能", "#效率提升", "#AI助手", "#科技", "#数字游民", "#副业"],
    "tools": ["#AI工具推荐", "#打工人必备", "#效率神器", "#职场干货", "#摸鱼必备"],
    "income": ["#副业变现", "#被动收入", "#赚钱思维", "#财务自由", "#理财"]
}


def generate_weibo_hook(topic: str, style: str = "数字体") -> str:
    """生成微博钩子"""
    templates = {
        "震惊体": f"震惊！{topic}竟然还有这种操作",
        "数字体": f"用了{topic}，3个月省下10000块",
        "问题体": f"为什么都在说{topic}？看完就懂了",
        "对比体": f"{topic} vs 传统方法，我选前者",
        "利益体": f"{topic}让我每月多赚5000+，亲测有效"
    }
    return templates.get(style, templates["数字体"])


def generate_weibo_content(topic: str, target_url: str, keywords: list = None, style: str = "数字体") -> dict:
    """生成微博内容"""
    hook = generate_weibo_hook(topic, style)
    hashtags = keywords[:5] if keywords else ["#AI工具", "#效率提升", "#打工人必备"]
    
    # 优化长度
    content_parts = [
        hook,
        "",
        f"最近研究{topic}，发现一套超好用的方法论，用了2个月效率翻倍。",
        "",
        f"具体看这里 ↓",
        target_url,
        "",
        " ".join(hashtags)
    ]
    
    full_content = "\n".join(content_parts)
    
    # 截断到最优长度
    if len(full_content) > CHAR_LIMITS["weibo"]["max"]:
        full_content = full_content[:CHAR_LIMITS["weibo"]["optimal"]]
    
    return {
        "platform": "weibo",
        "content": full_content,
        "char_count": len(full_content),
        "optimal_length": CHAR_LIMITS["weibo"]["optimal"],
        "is_optimal": CHAR_LIMITS["weibo"]["optimal"] - 30 <= len(full_content) <= CHAR_LIMITS["weibo"]["optimal"] + 30,
        "has_image": True,
        "recommended_times": OPTIMAL_TIMES["weibo"],
        "hashtags": hashtags
    }


def generate_zhihu_content(topic: str, target_url: str, keywords: list = None) -> dict:
    """生成知乎内容"""
    hashtags = keywords[:3] if keywords else ["#AI工具", "#效率提升", "#职业发展"]
    
    sections = [
        ("直接回答", f"关于{topic}，我的结论是：值得尝试，尤其是这3类人。"),
        ("个人经历", f"我是去年开始接触{topic}的，一开始也只是抱着试试看的心态。用了3个月后，发现确实有效——我的日常工作效率提升了大概40%左右。"),
        ("核心优势", f"**{topic}最值得用的3个场景：**\n\n1. **场景A** — 具体说明这个场景为什么适合，以及我的使用体验\n2. **场景B** — 同上\n3. **场景C** — 同上"),
        ("产品推荐", f"如果你是做{keywords[0] if keywords else '内容创作'}的，墙裂建议试试。现在注册还有优惠：[链接]({target_url})"),
        ("总结", f"总结一下：{topic}不是万能的，但在特定场景下确实能帮你省大量时间。关键是找到适合自己的使用方式。"),
        ("互动钩子", f"你们有用过类似的工具吗？评论区来聊聊 — 选中的评论我都会回复。")
    ]
    
    full_content = "\n\n".join([f"## {k}\n\n{v}" if k != "直接回答" else f"**{v}**" for k, v in sections])
    
    return {
        "platform": "zhihu",
        "content": full_content,
        "char_count": len(full_content),
        "optimal_length": CHAR_LIMITS["zhihu"]["optimal"],
        "sections": len(sections),
        "has_image": True,
        "recommended_times": OPTIMAL_TIMES["zhihu"],
        "hashtags": hashtags
    }


def generate_xiaohongshu_content(topic: str, target_url: str, keywords: list = None) -> dict:
    """生成小红书内容"""
    hashtags = keywords[:6] if keywords else ["#AI工具", "#效率神器", "#打工人必备", "#职场干货", "#好物推荐", "#种草"]
    
    sections = [
        ("封面标题", f"救命！{topic}也太香了吧😭"),
        ("Hook", f"姐妹们！今天必须安利一下{topic}，用了1个月彻底离不开！"),
        ("介绍", f"✨ **这是什么**\n{topic}，简单说就是帮你自动化处理重复工作的AI工具。"),
        ("亮点", f"✨ **最香的3个功能**\n\n▫️ **功能1**：具体说明\n▫️ **功能2**：具体说明\n▫️ **功能3**：具体说明"),
        ("使用场景", f"📌 **适合谁**\n- 每天做重复性工作的人\n- 想提升效率的职场人\n- 需要处理大量内容的创作者"),
        ("价格", f"💰 **价格**：有免费版，付费版¥XX/月起。"),
        ("我的评价", f"🙋 **我的评价**：用了1个月，省下大概20小时。墙裂推荐！"),
        ("链接", f"🔗 [我的专属优惠链接]({target_url})"),
        ("互动", f"\n\n👇你们有用过什么提升效率的神器吗？评论区告诉我！")
    ]
    
    lines = []
    for title, body in sections:
        if title == "封面标题":
            lines.append(f"**{body}**")
        elif title == "Hook":
            lines.append(body)
        else:
            lines.append(body)
        lines.append("")
    
    full_content = "\n".join(lines)
    
    return {
        "platform": "xiaohongshu",
        "content": full_content,
        "char_count": len(full_content),
        "optimal_length": CHAR_LIMITS["xiaohongshu"]["optimal"],
        "emoji_count": full_content.count("✨") + full_content.count("💰") + full_content.count("📌"),
        "has_image": True,
        "recommended_times": OPTIMAL_TIMES["xiaohongshu"],
        "hashtags": hashtags,
        "cover_style": "前后对比"
    }


def generate_all_content(topic: str, target_url: str, keywords: list = None, style: str = "数字体") -> dict:
    """一次生成所有平台内容"""
    return {
        "topic": topic,
        "target_url": target_url,
        "keywords": keywords or ["#AI工具", "#效率提升"],
        "generated_at": datetime.now().isoformat(),
        "utm_params": f"utm_source=social&utm_medium=content&utm_campaign={topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}",
        "platforms": {
            "weibo": generate_weibo_content(topic, target_url, keywords, style),
            "zhihu": generate_zhihu_content(topic, target_url, keywords),
            "xiaohongshu": generate_xiaohongshu_content(topic, target_url, keywords)
        }
    }


def format_report(result: dict) -> str:
    lines = [
        f"# 🔥 社媒内容生成报告",
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"📌 话题: {result['topic']}",
        f"🔗 目标链接: {result['target_url']}",
        f"🏷️ UTM: ?{result['utm_params']}\n",
    ]
    
    for platform, data in result["platforms"].items():
        lines.append(f"## 📱 {platform.upper()}")
        lines.append(f"**推荐发帖时间**: {', '.join(data['recommended_times'])}")
        lines.append(f"**字数**: {data['char_count']} (最优: {data['optimal_length']})")
        
        optimal_marker = " ✅" if data.get("is_optimal", False) else " ⚠️" if data.get("emoji_count") else ""
        lines.append(f"**内容**{optimal_marker}:\n")
        lines.append(data["content"])
        lines.append("")
        lines.append(f"**Hashtags**: {' '.join(data.get('hashtags', []))}")
        lines.append("\n" + "="*50 + "\n")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="🔥 社媒流量内容生成器")
    parser.add_argument("--topic", "-t", required=True, help="话题/主题")
    parser.add_argument("--url", "-u", required=True, help="目标URL")
    parser.add_argument("--keywords", "-k", help="关键词 (逗号分隔)")
    parser.add_argument("--platforms", "-p", default="weibo,zhihu,xiaohongshu", help="平台")
    parser.add_argument("--style", "-s", default="数字体", choices=["震惊体", "数字体", "问题体", "对比体", "利益体"])
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()
    
    keywords = [kw.strip() for kw in args.keywords.split(",")] if args.keywords else None
    
    result = generate_all_content(args.topic, args.url, keywords, args.style)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
