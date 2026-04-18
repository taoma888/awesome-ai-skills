---
name: revenue-dashboard
description: "Unified revenue intelligence dashboard — aggregates all income streams (affiliate commissions, ad revenue, subscriptions, digital products), calculates key metrics (MRR, ARPU, LTV, ROAS), and delivers daily/weekly automated reports via WeChat notification. Target: Know your exact revenue status every morning."
risk: low
source: custom
date_added: "2026-04-18"
tags: [revenue, analytics, dashboard, metrics, tracking, affiliate, automation, notifications]
requires_env: [WECHAT_WEBHOOK_URL]
---

# 📊 Revenue Dashboard

> **Mission**: Know your number — every morning, automatically.  
> Aggregate all revenue streams → Calculate key metrics → Report to WeChat daily.

---

## 🎯 When to Use

Trigger when:
- "收入" / "赚了多少" / "收益" / "账单"
- "今天赚了多少"
- "收入报表" / "财务报告"
- "佣金到账了吗"
- "帮我看下收入情况"
- Any financial status or monetization health check

---

## ⚡ Hard Gate

Before pulling data, confirm scope:

```
╔══════════════════════════════════════════════════════╗
║           REVENUE BRIEF                          ║
╠══════════════════════════════════════════════════════╣
║  Income Streams Active:                           ║
║    ☑ Affiliate Commissions                        ║
║    ☑ Ad Revenue (display/sponsored)              ║
□   ☐ Subscription/Membership                      ║
□   ☐ Digital Product Sales                        ║
□   ☐ Services/Consulting                         ║
□   ☐ Other: <specify>                             ║
║                                                    ║
║  Reporting Cadence: DAILY / WEEKLY / MONTHLY      ║
║  Alert Threshold: ¥X (notify if daily < X)       ║
╚══════════════════════════════════════════════════════╝
```

---

## 🔁 The Revenue Intelligence Loop

```
STEP 1: COLLECT
  → Pull data from all income sources (APIs, manual entry)
  → Normalize currencies and time zones
  ↓
STEP 2: CALCULATE
  → Compute MRR, ARPU, LTV, ROAS, conversion rates
  → Compare vs. previous period
  ↓
STEP 3: ANALYZE
  → Identify top performers and underperformers
  → Detect anomalies (sudden drops or spikes)
  → Calculate channel attribution
  ↓
STEP 4: REPORT
  → Format daily WeChat digest
  → Flag issues requiring attention
  → Recommend specific actions
  ↓
STEP 5: ALERT
  → If revenue < alert threshold → immediate notification
  → If anomaly detected → investigate + notify
```

---

## Step 1: COLLECT — Data Sources

### Affiliate Networks (API)

| Network | Data Available | Update Frequency |
|---------|---------------|-----------------|
| 阿里云百炼 | Clicks, Conversions, Commission | Daily |
| Amazon Associates | Earnings, Orders | Daily |
| Awin | Impressions, Clicks, Commission | Daily |
| ShareASale | Sales, Commission | Daily |
| CJ Affiliate | Performance | Daily |

### Ad Revenue

| Platform | Data | Via |
|---------|------|-----|
| Google AdSense | RPM, CPC, Revenue | API |
| 百度联盟 | Revenue, Impressions | Dashboard |
| 腾讯广告 | Revenue, CTR | Dashboard |

### Subscription / Product Sales

| Platform | Data | Via |
|---------|------|-----|
| 微信支付 | Transaction history | WeChat Pay API |
| Gumroad | Sales, Refunds, MRR | Gumroad API |
| Stripe | Subscriptions, MRR, Churn | Stripe API |

---

## Step 2: CALCULATE — Key Metrics

### Core Revenue Metrics

```python
# Monthly Recurring Revenue (MRR)
MRR = Sum(plan_price × active_subscribers)

# Average Revenue Per User (ARPU)
ARPU = MRR / total_active_users

# Lifetime Value (LTV)
LTV = ARPU × average_customer_lifetime_months

# Year-over-Year Growth
YoY_Growth = (Current_MRR - MRR_1year_ago) / MRR_1year_ago × 100

# Month-over-Month Growth
MoM_Growth = (Current_MRR - MRR_last_month) / MRR_last_month × 100

# Conversion Rate
CVR = paid_customers / total_visitors × 100

# Revenue Per Visitor (RPV)
RPV = total_revenue / total_visitors
```

### Affiliate-Specific Metrics

```python
# Earnings Per Click (EPC)
EPC = total_commission / total_clicks

# Conversion Rate by Platform
CVR_platform = conversions / clicks × 100

# Pending vs. Confirmed Commission
Pending_Rate = pending_commission / total_commission × 100

# Top Earning Tool
Top_Tool = tool with highest commission in period
```

---

## Step 3: ANALYZE — Intelligence

### Daily Digest Format

```markdown
┌─────────────────────────────────────────────┐
│  📊 REVENUE DAILY DIGEST — 2026-04-18      │
├─────────────────────────────────────────────┤
│  💰 Today: ¥XXX                            │
│     vs Yesterday: +X.X%                    │
│                                              │
│  📈 This Week: ¥X,XXX (MTD: X.X%)         │
│                                              │
│  🏆 Top Performer: Tool Name (¥XXX)        │
│  ⚠️ Needs Attention: Tool Name (X clicks, 0 converts) │
│                                              │
│  📋 PENDING COMMISSIONS: ¥XXX              │
│     ↳ Awaiting approval (7-30 days)         │
│                                              │
│  🎯 Daily Target: ¥XXX | On Track: ✅/❌   │
│                                              │
│  💡 RECOMMENDATION: <action>               │
└─────────────────────────────────────────────┘
```

### Anomaly Detection Rules

| Condition | Alert Level | Action |
|-----------|-------------|--------|
| Revenue drops >20% vs same day last week | 🔴 HIGH | Immediate investigate |
| Revenue drops >10% for 3 consecutive days | 🟡 MEDIUM | Schedule review |
| Pending commission >60% of total | 🟡 MEDIUM | Verify with network |
| Zero conversions for 7+ days | 🟡 MEDIUM | Review content |
| New all-time high | 🟢 POSITIVE | Celebrate + document |

---

## Step 4: REPORT — WeChat Notification

### WeChat Message Format

```json
{
  "msgtype": "news",
  "news": {
    "articles": [
      {
        "title": "💰 Revenue Report 2026-04-18",
        "description": "Today: ¥1,247 | Week: ¥8,934 | MRR: ¥32,450\n🏆 Top: Cursor ¥890\n⚠️ Alert: DeepSeek 0 converts (7 days)\n💡 Action: Increase DeepSeek content",
        "url": "https://your-dashboard-url.com"
      }
    ]
  }
}
```

### Automated Schedule

| Report | Frequency | Time | Content |
|--------|-----------|------|---------|
| Daily Digest | Every morning | 08:00 | Yesterday's revenue + highlights |
| Weekly Summary | Every Monday | 09:00 | Week recap + trend analysis |
| Monthly Report | 1st of month | 10:00 | Full month P&L + recommendations |
| Alert | Real-time | When triggered | Immediate revenue issue |

---

## Step 5: ALERT — Action Triggers

### Alert Conditions

```yaml
alerts:
  revenue_drop:
    condition: "today_revenue < yesterday_revenue × 0.7"
    threshold: "¥500 minimum"
    priority: HIGH
  
  zero_conversions:
    condition: "affiliate_clicks > 10 AND conversions = 0"
    duration: "7 consecutive days"
    priority: MEDIUM
  
  commission_stalled:
    condition: "pending_commission > total_commission × 0.6"
    duration: "30+ days"
    priority: MEDIUM
  
  new_record:
    condition: "today_revenue > all_time_high"
    priority: LOW (positive)
```

---

## 🚫 Refusal Conditions

1. **Asking for financial advice** — not a licensed financial advisor
2. **Tax calculation requests** — recommend professional accountant
3. **Requests to falsify data** — never manipulate metrics
4. **Requests to share competitor revenue** — confidential information

---

## 📊 Dashboard Data Schema

```json
{
  "report_date": "2026-04-18",
  "generated_at": "2026-04-18T08:00:00+08:00",
  "income_streams": {
    "affiliate": {
      "total_earned": 8500.00,
      "total_paid": 6200.00,
      "pending": 2300.00,
      "by_tool": {
        "cursor": {"clicks": 234, "conversions": 12, "commission": 960.00},
        "notion": {"clicks": 156, "conversions": 8, "commission": 792.00}
      }
    },
    "ads": {
      "revenue": 2340.00,
      "impressions": 45600,
      "rpm": 51.32
    },
    "subscriptions": {
      "mrr": 4990.00,
      "arpu": 49.90,
      "churn_rate": 2.3
    }
  },
  "totals": {
    "today": 1247.00,
    "this_week": 8934.00,
    "this_month": 34200.00,
    "mrr": 34200.00
  },
  "alerts": [],
  "recommendations": ["Increase DeepSeek content", "Test new Canva headline"]
}
```

---

## Limitations

- Manual data entry required for sources without API access
- Currency conversion rates are approximate
- Projections are estimates, not guarantees
- Report delivery depends on WeChat webhook availability
- Historical data must be maintained by user (no automatic backfill)
