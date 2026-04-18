---
name: autonomous-revenue-machine
description: "Autonomous revenue generation system — discovers monetization opportunities, validates demand, designs MVPs, and deploys revenue-generating assets in under 2 hours. Target: ¥10,000+/month passive income."
risk: medium
source: custom
date_added: "2026-04-18"
tags: [revenue, monetization, mvp, affiliate, automation]
requires_env: [DASHSCOPE_API_KEY]
---

# 💰 Autonomous Revenue Machine

> **Mission**: Transform AI skills into cash — automatically.  
> No fluff. No theory. Real money in real systems.

---

## 🎯 When to Use

Trigger when the user says:
- "怎么赚钱" / "变现" / "搞钱"
- "有个想法" / "我想做XX"
- "能不能自动"
- "被动收入"
- Any affiliate, monetization, or revenue-related request

---

## ⚡ Hard Gate (Must Confirm Before Proceeding)

You **MUST** present a Revenue Brief before touching any code:

```
╔══════════════════════════════════════════════════════╗
║            REVENUE BRIEF — FIRST STEP               ║
╠══════════════════════════════════════════════════════╣
║  Opportunity: <one-line summary>                     ║
║  Target Income: <¥X/month>                          ║
║  Time to First Dollar: <X days>                     ║
║  Effort Level: ⭐ to ⭐⭐⭐⭐⭐                         ║
║  Risk Level: LOW / MEDIUM / HIGH                   ║
║  Top 3 Monetization Paths:                          ║
║    1. <path A> (est. ¥X/month)                     ║
║    2. <path B> (est. ¥X/month)                     ║
║    3. <path C> (est. ¥X/month)                     ║
║  MVP Cost: ¥0 / ¥99 / ¥299 / ¥999+                 ║
║  Recommended: <path A>                              ║
╚══════════════════════════════════════════════════════╝
```

**Do NOT skip this gate. Do NOT start coding before showing this brief.**

---

## 🔁 The 4-Phase Revenue Loop

```
PHASE 1: DISCOVER          PHASE 2: VALIDATE
  Find opportunity           Verify demand exists
  ↓                          ↓
PHASE 3: BUILD MVP          PHASE 4: MONETIZE
  Ship fast, ship cheap      Deploy revenue engine
```

---

## Phase 1: DISCOVER — Opportunity Radar

### Sources to Mine

| Source | What to Find | Frequency |
|--------|-------------|-----------|
| 微博热搜 | Emerging trends with monetization potential | Real-time |
| 知乎热榜 | Unresolved problems people pay to solve | Daily |
| 百度指数 | Rising search terms with commercial intent | Daily |
| Reddit r/SideProject | Micro-SaaS ideas with proven paying users | Weekly |
| Product Hunt | New tools with affiliate programs | Daily |
| 联盟平台 | New AI tool affiliate programs (15-50% commission) | Weekly |

### Opportunity Scoring Formula

```
SCORE = (Demand × 3) + (Competition × 1) + (Monetization × 4) + (Effort × 2)

Where:
  Demand      = 搜索量/1000 (0-10)
  Competition = 1(低) 5(中) 10(高)
  Monetization= 1(广告) 3(订阅) 5(联盟) 7(卖货)
  Effort      = 1(简单) 3(中等) 5(复杂)
```

**Only pursue opportunities with SCORE ≥ 20.**

### Minimum Viable Validation

Before any build, confirm at least ONE of:
- [ ] 有人在搜索这个词（月搜索量 > 500）
- [ ] 有人在论坛/社媒问过这个问题
- [ ] 有竞品在收钱（月收入 > ¥5000）
- [ ] 有现成的付费解决方案

---

## Phase 2: VALIDATE — Demand Verification

### The 48-Hour Validation Protocol

```
Day 1 — Content Test:
  1. Write a landing page (1-page HTML)
  2. Run ads (¥100 budget) to the page
  3. Measure email sign-up rate
  
  PASS: >10% sign-up rate → proceed
  FAIL: <10% → pivot or abandon

Day 2 — Payment Test:
  1. Set up a payment link (微信/支付宝/LinkBio)
  2. Drive another ¥100 of traffic
  3. Measure conversion to first paying customer

  PASS: >3% paid → strong opportunity
  FAIL: <3% → validate problem more before building
```

### Refusal Conditions (Hard Stop)

Do NOT proceed to Phase 3 if:
- No validation data exists
- Total addressable market < ¥10,000/month
- User cannot explain who pays and why
- Regulatory or legal risk is present
- Competitor has 10x more resources in this space

---

## Phase 3: BUILD MVP — Speed-to-Market

### MVP Stack (Pick One)

| Stack | Cost | Speed | Best For |
|-------|------|-------|----------|
| Cloudflare Pages + D1 | ¥0 | 2h | 内容站/导航站 |
| LinkBio (Carrd + Gumroad) | ¥99/yr | 1h | 数字产品 |
| WordPress + WooCommerce | ¥300/yr | 4h | 电商/联盟 |
| React + Vercel + Stripe | ¥0 | 6h | 工具类产品 |
| Ghost + Members | ¥600/yr | 3h | 订阅内容 |

### MVP Quality Gates

Before calling it done, verify:
- [ ] 页面在 3 秒内加载
- [ ] 移动端体验完整
- [ ] 有明确的 CTA（行动召唤）
- [ ] 至少一个变现路径已接通
- [ ] 数据已持久化（不是 localStorage）

---

## Phase 4: MONETIZE — Revenue Engine

### Monetization Path Priority

```
#1 联盟营销 (Affiliate) — Fastest to revenue
   → Partner with tools you already recommend
   → Commission: 10-50% of first year revenue
   
#2 数字产品 (Digital Products) — Highest margin
   → Templates, courses, guides, presets
   → Marginal cost: ¥0
   → Price: ¥9.9 to ¥999
   
#3 订阅服务 (Subscription) — Most stable
   → Monthly retainer or membership
   → Target: ¥9.9-99/month
   → Requires ongoing value delivery

#4 广告收入 (Advertising) — Most passive
   → Display ads, sponsored content
   → RPM: ¥5-50 per 1000 views
   → Requires traffic volume
```

### Revenue Deployment Checklist

For each monetization path activated:
- [ ] Payment system connected (微信支付/支付宝/Stripe)
- [ ] Conversion tracking installed
- [ ] Revenue dashboard updated
- [ ] Auto-reconciliation configured (weekly check)
- [ ] First revenue milestone set

---

## 📊 Revenue Dashboard Output

After each session, report:

```
┌─────────────────────────────────────────────────┐
│  💰 REVENUE SYSTEM STATUS                       │
├─────────────────────────────────────────────────┤
│  Active Income Streams: X                        │
│  Monthly Revenue: ¥X                             │
│  Monthly Burn: ¥X                               │
│  Net Margin: X%                                 │
│                                                  │
│  Top Performer: <stream name>                   │
│  Next Milestone: ¥X                             │
│  Days to Break Even: X                          │
└─────────────────────────────────────────────────┘
```

---

## 🚫 Refusal Conditions (Non-Negotiable)

Stop and refuse if:
1. **Legal risk** — the requested business model violates laws or platform ToS
2. **Impossible timeline** — user expects revenue in <7 days with no budget
3. **Scam intent** — user wants to deceive customers or inflate metrics
4. **No monetization path** — project has no viable way to generate revenue
5. **Market dead** — evidence shows the niche is declining or saturated
6. **User cannot pay server costs** — if the MVP costs more than user can afford

When refusing: State the reason clearly, explain why, and offer an alternative.

---

## 🛠️ Available Tools

| Tool | Purpose |
|------|---------|
| `demand_miner.py` | Mine Reddit, HN, 知乎 for monetization opportunities |
| `competitor_radar.py` | Analyze competitor traffic, revenue, stack |
| `mvp_generator.py` | Generate full MVP spec from one-sentence idea |
| `affiliate_link_generator.py` | Generate affiliate links + promotion copy |
| `hot_topics.py` | Monitor trending topics for quick content opportunities |

---

## ⚡ Speed Guidelines

| Phase | Minimum | Target | Overtime |
|-------|---------|--------|----------|
| Phase 1 Discover | 5 min | 15 min | 30 min |
| Phase 2 Validate | 24 hr | 48 hr | 72 hr |
| Phase 3 Build MVP | 1 hr | 4 hr | 24 hr |
| Phase 4 Monetize | 30 min | 2 hr | Same day |

---

## 📝 Session Output Format

Every session must produce:

```markdown
## Opportunity Brief
[One-line summary]

## Validation Status
✅/❌ [Criteria] — [Evidence]

## MVP Spec
[What to build, in 3 sentences max]

## Revenue Path
[How it makes money, with numbers]

## Next Action
[Specific, numbered, with deadline]
```

---

## Limitations

- This skill generates ideas and specs — actual code execution is a separate step
- Revenue projections are estimates, not guarantees
- No legal or financial advice — recommend professional consultation for complex structures
- System performance depends on API availability and network conditions
