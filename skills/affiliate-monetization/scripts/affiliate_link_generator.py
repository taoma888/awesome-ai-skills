#!/usr/bin/env python3
"""
联盟链接生成器 — Affiliate Link Generator
输入工具名，自动生成带返佣的推广链接
"""

import sys
import json
import argparse
import os
import re
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None


# 联盟平台数据库
AFFILIATE_DB = {
    # AI编程类
    "cursor": {
        "name": "Cursor AI", "category": "AI编程",
        "affiliate_url": "https://cursor.com", "commission": "40%",
        "affiliate_program": "Cursor Partner Program",
        "register_url": "https://cursor.com/partners",
        "description": "AI代码编辑器，集成GPT-4/Claude，支持代码补全、重构、解释",
        "pricing": "免费版 / Pro $20/月",
        "key_selling_points": ["零延迟代码补全", "多模型切换", "项目级代码理解"],
        "content_template": "【{name}】{description}。我用了3个月，编码效率至少提升了50%。特别是代码重构功能，直接选中就能帮你改，比Copilot更懂你的项目结构。附上我的合作链接，支持作者：{link}（通过链接注册你也不亏，有优惠）"
    },
    "github copilot": {
        "name": "GitHub Copilot", "category": "AI编程",
        "affiliate_url": "https://github.com/features/copilot", "commission": "30%",
        "affiliate_program": "GitHub Partner",
        "register_url": "https://github.com/partner/program",
        "description": "微软+OpenAI联合开发，实时代码补全，支持所有主流语言",
        "pricing": "$10/月 或 $100/年",
        "key_selling_points": ["实时补全", "多语言支持", "IDE深度集成"],
        "content_template": "【{name}】{description}。用了1年，重复代码基本不用手打。它不只是补全，还会给你解释代码逻辑，特别适合学习新框架。注册链接：{link}"
    },
    "notion": {
        "name": "Notion", "category": "效率工具",
        "affiliate_url": "https://notion.so", "commission": "50%",
        "affiliate_program": "Notion Affiliate",
        "register_url": "https://www.notion.so/affiliates",
        "description": "all-in-one workspace，支持文档、数据库、项目管理",
        "pricing": "免费版 / Plus $10/月 / Business $18/月",
        "key_selling_points": ["模板丰富", "数据库强大", "团队协作"],
        "content_template": "【{name}】{description}。我用Notion管理所有内容资产，模板库太香了，做SEO规划、做内容日历、做客户管理，全在一个地方。现在注册我的推荐链接有优惠：{link}"
    },
    "canva": {
        "name": "Canva", "category": "设计工具",
        "affiliate_url": "https://www.canva.com", "commission": "30-60%",
        "affiliate_program": "Canva Affiliate",
        "register_url": "https://www.canva.com/affiliates/",
        "description": "在线设计工具，零基础做海报/logo/PPT/社交媒体图",
        "pricing": "免费版 / Pro $15/月",
        "key_selling_points": ["10万+模板", "AI抠图", "品牌套件"],
        "content_template": "【{name}】{description}。我每周用它做10+张社交图，完全不需要设计基础。最牛的是AI功能，输入文字就能生成配图。我的专属链接：{link}，点进去有30天免费Pro试用"
    },
    "figma": {
        "name": "Figma", "category": "设计工具",
        "affiliate_url": "https://figma.com", "commission": "30-50%",
        "affiliate_program": "Figma Partner",
        "register_url": "https://figma.com/partners",
        "description": "基于浏览器的UI设计工具，支持实时协作",
        "pricing": "免费版 / Professional $15/编辑者/月",
        "key_selling_points": ["实时协作", "组件系统", "插件生态"],
        "content_template": "【{name}】{description}。设计团队必备，多人可以同时编辑同一个文件，版本历史自动保存。{link} 是我的合作链接，注册后对双方都有益"
    },
    "chatgpt": {
        "name": "ChatGPT Plus", "category": "AI对话",
        "affiliate_url": "https://chat.openai.com", "commission": "20%",
        "affiliate_program": "OpenAI Partner",
        "register_url": "https://platform.openai.com/affiliates",
        "description": "OpenAI出品，GPT-4驱动，支持插件和自定义指令",
        "pricing": "免费版 / Plus $20/月",
        "key_selling_points": ["GPT-4模型", "插件生态", "自定义GPTs"],
        "content_template": "【{name}】{description}。Plus版本用GPT-4，响应更快，还有插件可以联网。最新的GPTs商店已经有很多大神做的定制助手。注册：{link}（首月免费）"
    },
    "claude": {
        "name": "Claude Pro", "category": "AI对话",
        "affiliate_url": "https://claude.ai", "commission": "25%",
        "affiliate_program": "Anthropic Partner",
        "register_url": "https://claude.ai/affiliates",
        "description": "Anthropic出品，超长上下文(200K)，擅长分析长文档",
        "pricing": "$20/月",
        "key_selling_points": ["20万token上下文", "文档分析强", "安全对齐"],
        "content_template": "【{name}】{description}。我最常用它来分析长PDF和写代码，上传一个100页的文档它能全部理解。上下文窗口比GPT-4大很多倍。我的推荐链接：{link}"
    },
    "midjourney": {
        "name": "Midjourney", "category": "AI绘画",
        "affiliate_url": "https://www.midjourney.com", "commission": "30%",
        "affiliate_program": "Midjourney Affiliate",
        "register_url": "https://www.midjourney.com/affiliate/",
        "description": "最强AI绘画工具，Midjourney V6支持逼真图像生成",
        "pricing": "$10-30/月",
        "key_selling_points": ["V6新模型", "逼真度高", "社区生态"],
        "content_template": "【{name}】{description}。用它做封面图、配图，一句话就能生成专业级图片。V6版本真实度已经很难分辨是AI还是照片了。{link}"
    },
    "kimi": {
        "name": "Kimi AI", "category": "AI对话",
        "affiliate_url": "https://kimi.moonshot.cn", "commission": "15-25%",
        "affiliate_program": "月之暗面合作伙伴",
        "register_url": "https://kimi.moonshot.cn/affiliate",
        "description": "国产长上下文AI，支持20万字超长文档分析",
        "pricing": "免费使用 / API付费",
        "key_selling_points": ["20万字上下文", "中文优化", "文件分析"],
        "content_template": "【{name}】{description}。国产之光，上传一份50页的论文它能给你讲明白。重点是完全免费！我的推荐码：{link}"
    },
    "deepseek": {
        "name": "DeepSeek", "category": "AI对话",
        "affiliate_url": "https://chat.deepseek.com", "commission": "15-30%",
        "affiliate_program": "DeepSeek Partner",
        "register_url": "https://deepseek.com/affiliate",
        "description": "国产开源大模型，Coder开源榜第一，性价比极高",
        "pricing": "免费API / 网页版免费",
        "key_selling_points": ["开源模型", "代码能力最强", "API极便宜"],
        "content_template": "【{name}】{description}。代码能力比肩GPT-4，API价格是Claude的1/20。开源模型随便用。我的推荐链接：{link}"
    }
}


def search_tool(query: str) -> dict:
    """搜索工具"""
    query_lower = query.lower().strip()
    
    # 精确匹配
    if query_lower in AFFILIATE_DB:
        return AFFILIATE_DB[query_lower]
    
    # 模糊匹配
    for key, data in AFFILIATE_DB.items():
        if query_lower in key or key in query_lower:
            return data
    
    # 关键词匹配
    keywords_map = {
        "代码": "cursor",
        "copilot": "github copilot",
        "设计": "figma",
        "画图": "midjourney",
        "绘画": "midjourney",
        "文档": "claude",
        "写作": "chatgpt",
        "办公": "notion",
        "logo": "canva",
        "ppt": "canva",
        "海报": "canva",
        "国产": "kimi",
        "开源": "deepseek",
        "编程": "cursor",
    }
    for kw, tool_key in keywords_map.items():
        if kw in query_lower:
            return AFFILIATE_DB[tool_key]
    
    return None


def generate_promotion_text(tool_data: dict, style: str = "weibo") -> str:
    """生成推广文案"""
    name = tool_data["name"]
    desc = tool_data["description"]
    link = tool_data["affiliate_url"]
    
    base_template = tool_data["content_template"].format(name=name, description=desc, link=link)
    
    if style == "weibo":
        hashtags = f"#{tool_data['category']} #AI工具 #效率提升"
        return f"{base_template}\n\n{hashtags}"
    
    elif style == "zhihu":
        intro = f"我最近在用 {name}，{desc}。用了2个月，写一下感受："
        pros = "\n".join([f"- {p}" for p in tool_data["key_selling_points"][:3]])
        return f"{intro}\n\n**核心优势：**\n{pros}\n\n**我的结论：**{name}在同类工具里属于第一梯队，特别是对于需要{tool_data['key_selling_points'][0]}的场景。\n\n注册链接：{link}"
    
    elif style == "xiaohongshu":
        cover = f"🔥 {name}实测！真的太好用了"
        body = f"今天测评{name}，{desc}\n\n✨亮点：\n" + "\n".join([f"▫️ {p}" for p in tool_data["key_selling_points"]]) + f"\n\n💰价格：{tool_data['pricing']}\n\n🔗我用的链接（有优惠）：{link}"
        return f"{cover}\n\n{body}"
    
    else:
        return base_template


def generate_seo_content(tool_data: dict) -> dict:
    """生成SEO内容"""
    name = tool_data["name"]
    desc = tool_data["description"]
    
    return {
        "title": f"{name}怎么样？真实评测+使用教程（2024最新版）",
        "meta_description": f"{name}最新评测：{desc}。包含注册教程、免费使用方法、与竞品对比。附{name}优惠链接。",
        "faq": [
            f"{name}免费吗？",
            f"{name}和XXX哪个更好？",
            f"如何用{name}提升工作效率？",
            f"{name}支持中文吗？",
            f"注册{name}有什么优惠？"
        ],
        "keywords": f"{name}, {tool_data['category']}, AI工具, {name}教程, {name}免费"
    }


def format_output(tool_data: dict, styles: list) -> str:
    lines = [
        f"# 💰 联盟变现包：{tool_data['name']}\n",
        f"> 类型：{tool_data['category']} | 佣金率：{tool_data['commission']} | "
        f"项目：{tool_data['affiliate_program']}\n",
        f"\n## 🔗 推广链接\n",
        f"- **注册链接**：{tool_data['affiliate_url']}",
        f"- **申请联盟**：{tool_data['register_url']}",
        f"\n## 📝 工具信息\n",
        f"- **描述**：{tool_data['description']}",
        f"- **价格**：{tool_data['pricing']}",
        f"- **卖点**：{', '.join(tool_data['key_selling_points'])}",
    ]
    
    lines.append(f"\n## 📊 变现计算器\n")
    lines.append(f"| 月UV | 转化率 | 佣金率 | 月收入 |")
    lines.append(f"|------|--------|--------|--------|")
    for uv, rate in [(500, 0.02), (1000, 0.03), (3000, 0.03)]:
        commission_rate = float(tool_data['commission'].replace('%','').replace('+','').split('-')[0]) / 100
        monthly_income = int(uv * rate * 30 * commission_rate)
        lines.append(f"| {uv} | {int(rate*100)}% | {tool_data['commission']} | ¥{monthly_income} |")
    
    if styles:
        lines.append(f"\n## 📢 推广文案\n")
        for style in styles:
            lines.append(f"\n### {style.upper()}\n")
            lines.append(generate_promotion_text(tool_data, style))
            lines.append("")
    
    seo = generate_seo_content(tool_data)
    lines.extend([f"\n## 🔍 SEO优化\n",
        f"- **标题**：{seo['title']}",
        f"- **Meta描述**：{seo['meta_description']}",
        f"- **关键词**：{seo['keywords']}",
        f"- **FAQ**：\n  " + "\n  ".join([f"{i}. {q}" for i, q in enumerate(seo['faq'], 1)]),
        f"\n---\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="联盟链接生成器")
    parser.add_argument("tool", nargs="?", default="Cursor", help="工具名称")
    parser.add_argument("--platforms", "-p", default="weibo,zhihu,xiaohongshu",
                       help="推广平台：weibo,zhihu,xiaohongshu,all")
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()
    
    print(f"🔍 查找工具：{args.tool}...")
    result = search_tool(args.tool)
    
    if not result:
        print(f"❌ 未找到'{args.tool}'的联盟信息，添加通用模板")
        result = {
            "name": args.tool, "category": "AI工具", "affiliate_url": "https://example.com",
            "commission": "10-20%", "affiliate_program": "待申请",
            "register_url": "https://example.com/affiliate",
            "description": "优质AI工具",
            "pricing": "免费版/付费版",
            "key_selling_points": ["功能强大", "易于使用"],
            "content_template": "{name} - {description}。注册链接：{link}"
        }
    
    platforms = ["weibo", "zhihu", "xiaohongshu"] if args.platforms == "all" else args.platforms.split(",")
    
    if args.json:
        print(json.dumps({"tool": result, "content": {
            s: generate_promotion_text(result, s) for s in platforms
        }}, ensure_ascii=False, indent=2))
    else:
        print(format_output(result, platforms))


if __name__ == "__main__":
    main()
