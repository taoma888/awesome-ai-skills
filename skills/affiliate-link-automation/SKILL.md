---
name: affiliate-link-automation
description: "Automated affiliate marketing engine — discovers new AI tool affiliate programs, generates conversion-optimized promotion content for all platforms, tracks commission status, and identifies new revenue opportunities. Target: ¥5,000+/month from affiliate commissions."
risk: medium
source: custom
date_added: "2026-04-18"
tags: [affiliate, commission, monetization, cpa, cps, revenue, automation]
requires_env: [DASHSCOPE_API_KEY]
---

# 💸 Affiliate Link Automation

> **Mission**: Make affiliate marketing autonomous — from discovery to commission tracking.  
> Find tools → Get affiliate links → Generate content → Track commissions → Reinvest profits.

---

## 🎯 When to Use

Trigger when:
- "联盟" / "佣金" / "返佣" / "推广链接"
- "怎么推广XX工具"
- "帮我写推广文案"
- "这个工具有没有佣金"
- "AFF" / "Affiliate" / "CPA" / "CPS"
- "佣金多少" / "返现"

---

## ⚡ Hard Gate

Before generating affiliate content, confirm:

```
╔══════════════════════════════════════════════════════╗
║           AFFILIATE BRIEF                          ║
╠══════════════════════════════════════════════════════╣
║  Tool Name: <AI tool name>                         ║
║  Commission Rate: <X% or ¥X per sale>             ║
║  Cookie Duration: <X days>                        ║
║  Payment Threshold: <¥X minimum>                   ║
║  Average Sale Value: <¥X>                         ║
║  EPC (Earnings Per Click): <¥X>                   ║
║  Network/Program: <Affiliate network or direct>    ║
║  Registration URL: <Affiliate signup link>         ║
║  Promotion Allowed: SEO / Paid Ads / Social?      ║
║  Prohibited: <Any restrictions>                   ║
╚══════════════════════════════════════════════════════╝
```

**If commission rate < 10% and EPC < ¥0.50, recommend alternative monetization.**

---

## 🔁 The Affiliate Loop

```
STEP 1: DISCOVER PROGRAMS
  → Monitor new AI tool launches for affiliate offers
  → Scan affiliate networks (阿里云百炼, Amazon, CJ, etc.)
  → Track competitor affiliate activities
  ↓
STEP 2: EVALUATE OPPORTUNITY
  → Calculate potential revenue (commission × conversion × traffic)
  → Verify program legitimacy (payment history, cookie duration)
  → Check promotion restrictions
  ↓
STEP 3: SECURE LINKS
  → Register for program (or retrieve existing links)
  → Generate tracking links with UTM parameters
  → Create link shortcuts/bundles for easy access
  ↓
STEP 4: GENERATE CONTENT
  → Platform-specific promotional copy (Weibo/知乎/小红书)
  → SEO-optimized tool reviews
  → Comparison pages (vs alternatives)
  → Email sequences for subscribers
  ↓
STEP 5: TRACK & OPTIMIZE
  → Monitor clicks, conversions, commissions
  → A/B test content for better conversion
  → Identify high-performing traffic sources
  → Reinvest profits into top channels
```

---

## Step 1: DISCOVER PROGRAMS

### Major AI Affiliate Networks & Programs

| Platform | Commission | Cookie | Sign-up |
|----------|-----------|--------|---------|
| 阿里云百炼 (Alibaba Cloud) | 15-30% | 30 days | Direct |
| Amazon AI Services | 3-10% | 24 hours | Amazon Associates |
| OpenAI API | 10-20% | 30 days | Partner Program |
| Anthropic Claude | 25% | 30 days | Affiliate Program |
| Cursor | 40% | 30 days | Partner Portal |
| Canva | 30-60% | 45 days | Canva Affiliate |
| Notion | 50% (first year) | 30 days | Notion Partners |
| Figma | 30-50% | 30 days | Figma Affiliate |
| GitHub Copilot | 30% | 30 days | GitHub Partner |
| DeepSeek | 15-30% | 30 days | Direct |
| 月之暗面 (Kimi) | 15-25% | 30 days | Direct |
| 讯飞星火 | 10-20% | 30 days | Direct |

### Discovery Sources

```
1. Tool launches — Product Hunt, Twitter/X, 知乎
2. Affiliate networks — 阿里云云市场, Amazon PartnerCentral
3. Competitor monitoring — What tools are top bloggers promoting?
4. Reddit r/juststart — Affiliate discussions
5. 站长工具 — Competitive affiliate analysis
```

### New Program Alert Template

```markdown
## 🆕 New Affiliate Program Detected

**Tool**: <name>
**URL**: <tool website>
**Commission**: <rate>
**Cookie**: <days>
**EPC Estimate**: <¥X>
**Monthly Search Volume**: <X>
**Competition**: LOW / MEDIUM / HIGH
**Recommendation**: ✅ PURSUE / ⚠️ EVALUATE / ❌ SKIP
**Revenue Potential**: ¥<X>-<X>/month (at 100/500/1000 UV)
```

---

## Step 2: EVALUATE OPPORTUNITY

### Revenue Calculator

```python
Monthly Revenue = Traffic × CTR × Conversion × Commission × AOV

Where:
  Traffic    = Monthly unique visitors to your affiliate link
  CTR        = Click-through rate (typical: 2-5%)
  Conversion = Free → Paid conversion (typical: 1-3%)
  Commission = Commission rate (e.g., 0.30 for 30%)
  AOV        = Average Order Value (¥)

Example:
  1,000 UV × 3% CTR × 2% conversion × 30% commission × ¥200 AOV
  = ¥3.60/month per 1,000 UV
```

### Minimum Thresholds

| Metric | Minimum to Pursue |
|--------|------------------|
| Commission Rate | ≥10% |
| Cookie Duration | ≥7 days |
| EPC | ≥¥0.30 |
| AOV | ≥¥50 |
| Program Age | ≥6 months (verified paying) |

---

## Step 3: SECURE LINKS

### Link Generation Rules

```
Format:
  https://{affiliate_url}?utm_source={platform}&utm_medium=affiliate&utm_campaign={tool}_{date}

Example:
  https://cursor.com?ref=yourname&utm_source=aisstt&utm_medium=social&utm_campaign=claude4_2026
```

### Link Shortcut System

```json
{
  "cursor": "https://cursor.com?ref=aisstt",
  "claude": "https://claude.ai?ref=aisstt",
  "notion": "https://notion.so?ref=aisstt",
  "canva": "https://canva.com?ref=aisstt",
  "figma": "https://figma.com?ref=aisstt"
}
```

---

## Step 4: GENERATE CONTENT

### Content Type Priority

| Content Type | Traffic Potential | Conversion | Effort |
|--------------|------------------|------------|--------|
| Tool comparison page | HIGH (SEO) | MEDIUM | 2hr |
| "Best X tools" roundup | HIGH (SEO) | HIGH | 1hr |
| Individual tool review | MEDIUM (SEO) | MEDIUM | 1hr |
| Weibo promotion | LOW (social) | LOW | 15min |
| 知乎 answer | MEDIUM (search) | HIGH | 30min |
| 小红书 post | MEDIUM (social) | MEDIUM | 20min |
| Email to list | HIGH (direct) | HIGH | 30min |

### Promotion Copy Templates

#### 微博 (Short-form)
```
🔥 {tool_name}让我每周多出10小时

{one sentence value prop}

注册用我的链接：
{affiliate_link}

#hashtag1 #hashtag2 #hashtag3
```

#### 知乎 (Long-form answer)
```
【直接回答问题】

我用了{tool_name} {X}个月，{核心结论}

【为什么有效】

1. {具体优势1} — {例子}
2. {具体优势2} — {例子}
3. {具体优势3} — {例子}

【我的真实体验】
{100字个人经历}

【推荐】
如果你也是做{目标用户}，墙裂建议试试。
注册链接（用我的，有优惠）：{affiliate_link}
```

#### 小红书 (Visual + Story)
```
标题：{数字}天用下来，{tool_name}真的绝了

正文：
姐妹们！今天必须安利{tool_name}
之前我一直用XXX，但是{tool_name}的X功能太香了
✨ {亮点1}
✨ {亮点2}
✨ {亮点3}
价格：{pricing}
[我的专属优惠链接]({affiliate_link})
```

---

## Step 5: TRACK & OPTIMIZE

### Tracking Setup

```yaml
tracking:
  utm_source: [weibo, zhihu, xiaohongshu, email, seo, direct]
  utm_medium: [social, content, email, paid]
  utm_campaign: "{tool}_{content_type}_{date}"
  events:
    - click
    - signup
    - trial_start
    - conversion
    - commission_confirmed
```

### Commission Status States

| Status | Meaning | Action |
|--------|---------|--------|
| PENDING | Click recorded, no sale yet | Wait |
| APPROVED | Sale confirmed, awaiting payment | Track |
| PAID | Money in account | Celebrate + Reinvest |
| REJECTED | Sale reversed/fraudulent | Analyze why |
| LOCKED | Cookie expired / no conversion | Drive more traffic |

### Weekly Affiliate Report

```markdown
## 📊 Weekly Affiliate Report

**Period**: 2026-W15 (Apr 7-13)

| Tool | Clicks | Conversions | Commission | Status |
|------|--------|-------------|------------|--------|
| Cursor | 45 | 2 | ¥160 | PENDING |
| Notion | 23 | 1 | ¥99 | APPROVED |
| Canva | 67 | 3 | ¥270 | PAID |

**Total Earned**: ¥529
**Total Paid Out**: ¥270
**Pending**: ¥259

**Top Performer**: Canva (highest EPC this week)
**Needs Attention**: {tool with 0 conversions despite clicks}

**Action Items**:
1. Create comparison content for {top_tool}
2. Test new headline for {underperforming_tool}
3. Apply for {new_tool} affiliate program
```

---

## 🚫 Refusal Conditions (Non-Negotiable)

Do NOT promote affiliate programs:
1. **Illegal or scam products** — pyramid schemes, fake courses, etc.
2. **Misleading claims** — don't promise results you can't verify
3. **Competition with user's own product** — conflicts of interest
4. **Tools you haven't personally used** — must have real experience
5. **Programs with < 30-day payment track record** — payment risk
6. **Adult/gambling/crypto schemes** — legal and ethical risk
7. **"Guaranteed income" claims** — unrealistic promises

---

## 🛠️ Available Tools

| Tool | Purpose |
|------|---------|
| `affiliate_link_generator.py` | Generate affiliate links + content for 10+ AI tools |
| `competitor_radar.py` | Monitor what competitors are promoting |
| `social_traffic_siphon.py` | Distribute affiliate content across platforms |

---

## 💰 Revenue Targets

| Month | Target Revenue | Required Clicks/Day |
|-------|---------------|---------------------|
| Month 1 | ¥1,000 | 50 |
| Month 3 | ¥5,000 | 150 |
| Month 6 | ¥15,000 | 400 |
| Month 12 | ¥50,000 | 1,000 |

---

## Limitations

- Affiliate programs change commission rates without notice
- Cookie duration means delayed conversions (factor into tracking)
- Actual earnings depend on traffic quality, not just quantity
- Compliance with platform ToS is user's responsibility
- Tax implications of affiliate income vary by jurisdiction
