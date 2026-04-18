#!/usr/bin/env python3
"""
MVP 生成器 — MVP Generator
基于需求分析和竞品研究，自动生成可执行的最小可行产品方案
"""

import sys
import json
import argparse
from datetime import datetime

# 变现模板库
MONETIZATION_TEMPLATES = {
    "affiliate": {
        "name": "联盟营销型导航站",
        "free_features": ["无限浏览工具", "基础搜索", "分类导航"],
        "paid_features": ["高级评测", "对比报告", "专属工具推荐", "去广告"],
        "price": "¥9.9-29.9/月",
        "affiliate_commission": "10-50%",
        "timeline": "7天上线",
        "mvp_step": [
            "1. 注册联盟计划 (Amazon Associates / 工具官网返佣)",
            "2. 选品20-50个高频使用的AI工具",
            "3. 建站（静态页 + D1数据库）",
            "4. 每个工具写100字真实评测（差异化！）",
            "5. 嵌入联盟链接（自然植入，非硬推）",
            "6. 提交sitemap到Google",
            "7. 知乎/公众号发布引流文章"
        ]
    },
    "subscription": {
        "name": "付费工具/SaaS",
        "free_features": ["每天3次使用", "基础功能"],
        "paid_features": ["无限使用", "导出功能", "优先更新", "客服支持"],
        "price": "¥19-99/月",
        "affiliate_commission": "N/A",
        "timeline": "14-30天上线",
        "mvp_step": [
            "1. 明确核心问题（不是'做个工具'而是'帮用户节省X时间'）",
            "2. 用 No-Code 搭原型 (n8n / Zapier / Cursor)",
            "3. 找5个真实用户内测（免费换反馈）",
            "4. 迭代2-3轮",
            "5. 上线付费版",
            "6. 收集10个付费用户作为社会证明"
        ]
    },
    "content": {
        "name": "内容变现站",
        "free_features": ["免费阅读5篇/月", "基础搜索"],
        "paid_features": ["全站解锁", "专属内容", "社群会员", "1v1咨询"],
        "price": "¥29-199/月",
        "affiliate_commission": "N/A",
        "timeline": "3-7天上线",
        "mvp_step": [
            "1. 确定细分领域（如：AI编程副业/AI写作技巧）",
            "2. 用 AI 改写工具生成10篇伪原创文章",
            "3. 用 Hugo/Hexo 建站",
            "4. 接入联盟链接（书/课程/工具）",
            "5. SEO优化（标题/描述/内链）",
            "6. 提交到微信搜一搜/知乎专栏"
        ]
    }
}


def generate_mvp(product_idea: str, demand_grade: str, competitors: list = None,
                 target_monetization: str = "affiliate") -> dict:
    """生成MVP方案"""

    template = MONETIZATION_TEMPLATES.get(target_monetization, MONETIZATION_TEMPLATES["affiliate"])

    # 核心问题提取
    product_name = product_idea if product_idea else "AI工具导航站"
    
    # 目标用户画像
    personas = {
        "affiliate": "想用AI工具提效但不知道选哪个的职场人",
        "subscription": "愿意为效率付费的独立开发者/创业者",
        "content": "想学习AI应用技巧但没时间的上班族"
    }
    
    # 差异化
    differentiators = {
        "affiliate": [
            "不是罗列工具，而是真实评测 + 使用场景",
            "不是硬推链接，而是自然融入内容",
            "不是做SEO农场，而是做信任积累"
        ],
        "subscription": [
            "解决一个具体问题，不是功能堆砌",
            "有明确效果指标（如：节省50%时间）",
            "提供使用支持，不只是给工具"
        ],
        "content": [
            "比公众号更系统，比知乎更深入",
            "每周深度1篇 > 每天水文5篇",
            "带可操作的下一步，不是空谈"
        ]
    }
    
    # KPI
    kpis = {
        "affiliate": {
            "week1": "网站上线，提交sitemap",
            "month1": "日UV 100，月佣金 ¥500",
            "month3": "日UV 500，月佣金 ¥3000",
            "month6": "日UV 2000，月佣金 ¥15000"
        },
        "subscription": {
            "week1": "内测版上线，5个真实用户",
            "month1": "10个付费用户",
            "month3": "50个付费用户，月收入 ¥5000",
            "month6": "200个付费用户，月收入 ¥20000"
        },
        "content": {
            "week1": "发布10篇文章到知乎/公众号",
            "month1": "日IP 50，联盟收入 ¥200",
            "month3": "日IP 300，月收入 ¥2000",
            "month6": "日IP 1000，月收入 ¥8000"
        }
    }

    mvp = {
        "product_name": product_name,
        "type": target_monetization,
        "type_name": template["name"],
        "target_persona": personas.get(target_monetization),
        "timeline": template["timeline"],
        "free_features": template["free_features"],
        "paid_features": template["paid_features"],
        "price": template["price"],
        "differentiators": differentiators.get(target_monetization, []),
        "steps": template["mvp_step"],
        "kpis": kpis.get(target_monetization, {}),
        "risks": generate_risks(target_monetization, demand_grade),
        "quick_win": generate_quick_win(target_monetization)
    }
    
    return mvp


def generate_risks(mon_type: str, grade: str) -> list:
    risks = []
    if mon_type == "affiliate":
        risks.append(("SEO周期长", "同时做知乎/公众号/小红书引流"))
        risks.append(("佣金政策变化", "不要依赖单一联盟，多平台分散"))
        risks.append(("流量获取难", "聚焦长尾词，先做精准流量"))
    elif mon_type == "subscription":
        risks.append(("用户留存低", "每周发版本更新，保持用户参与感"))
        risks.append(("竞争激烈", "找细分场景，避免正面竞争"))
        risks.append(("冷启动难", "先免费积累用户，再转化付费"))
    elif mon_type == "content":
        risks.append(("内容同质化", "做深度+个人风格，不做搬运"))
        risks.append(("平台依赖", "建立自己的邮件列表/粉丝群"))
    if grade == "B":
        risks.append(("需求待验证", "先小范围测试，再决定是否投入"))
    return risks


def generate_quick_win(mon_type: str) -> dict:
    wins = {
        "affiliate": {
            "action": "今天就注册3个联盟计划（Amazon + Canva + Notion）",
            "why": "0成本，5分钟，立即开始赚取第一笔佣金"
        },
        "subscription": {
            "action": "用Cursor Agent 48小时做出内测版",
            "why": "AI编程让开发速度提升10倍"
        },
        "content": {
            "action": "今天写1篇深度文章发知乎，明天上榜",
            "why": "知乎流量长期有效，一篇文章可持续引流数月"
        }
    }
    return wins.get(mon_type, wins["affiliate"])


def format_markdown(mvp: dict) -> str:
    lines = [
        f"# 🚀 MVP 方案：{mvp['product_name']}\n",
        f"> **类型**: {mvp['type_name']} | **启动周期**: {mvp['timeline']} | "
        f"**目标用户**: {mvp['target_persona']}\n",
        f"\n---\n",
        "\n## 💡 差异化定位\n"
    ]
    for d in mvp['differentiators']:
        lines.append(f"- ✦ {d}")
    
    lines.extend([f"\n## 💰 变现设计\n",
        f"| 套餐 | 内容 | 价格 |",
        f"|------|------|------|",
        f"| 免费版 | {', '.join(mvp['free_features'][:3])} | ¥0 |",
        f"| 付费版 | {', '.join(mvp['paid_features'][:3])} | {mvp['price']} |"
    ])
    
    if mvp.get('affiliate_commission') and mvp['affiliate_commission'] != "N/A":
        lines.append(f"\n> 💸 **额外佣金**: {mvp['affiliate_commission']}（工具推荐返佣）")
    
    lines.extend([f"\n## 📋 7天启动清单\n"])
    for i, step in enumerate(mvp['steps'], 1):
        lines.append(f"{i}. {step}")
    
    lines.extend([f"\n## 📊 KPI 里程碑\n",
        f"| 时间 | 目标指标 |",
        f"|------|---------|"]
    )
    for period, target in mvp['kpis'].items():
        lines.append(f"| {period} | {target} |")
    
    if mvp['risks']:
        lines.extend([f"\n## ⚠️ 风险与对策\n"])
        for risk, mitigation in mvp['risks']:
            lines.append(f"- **{risk}** → {mitigation}")
    
    lines.extend([f"\n## ⚡ 今天就能做的事\n",
        f"> 🎯 **{mvp['quick_win']['action']}**",
        f"> {mvp['quick_win']['why']}\n",
        f"\n---\n*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*"
    ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="MVP 生成器 — 自动生成可执行方案")
    parser.add_argument("--idea", "-i", default="AI工具导航站", help="产品名称/方向")
    parser.add_argument("--grade", "-g", default="A", choices=["A","B","C","D"], help="需求等级")
    parser.add_argument("--type", "-t", default="affiliate",
                       choices=["affiliate", "subscription", "content"],
                       help="变现模式")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()
    
    print(f"🎯 生成 MVP 方案：{args.idea}（需求等级:{args.grade}）...")
    
    mvp = generate_mvp(args.idea, args.grade, target_monetization=args.type)
    
    if args.json:
        print(json.dumps(mvp, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(mvp))


if __name__ == "__main__":
    main()
