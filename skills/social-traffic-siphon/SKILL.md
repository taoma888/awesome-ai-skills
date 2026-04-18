---
name: social-traffic-siphon
description: "Social media traffic generation engine — discovers trending topics, generates platform-specific viral content, and automatically distributes to Weibo/知乎/小红书/微博 to drive targeted traffic to any target URL. Target: 500+ UV/day."
risk: low
source: custom
date_added: "2026-04-18"
tags: [traffic, social-media, viral, content, seo, weibo, zhihu, xiaohongshu]
requires_env: []
---

# 🔥 Social Traffic Siphon

> **Mission**: Turn hot topics into targeted traffic — automatically.  
> Find what's trending → Generate viral content → Distribute everywhere → Drive traffic back.

---

## 🎯 When to Use

Trigger when:
- "引流" / "流量" / "推广" / "获客"
- "微博/知乎/小红书怎么发"
- "帮我写推广文案"
- "蹭热点"
- "怎么让人看到我的网站"

---

## ⚡ Hard Gate

Before generating content, always confirm:

```
╔══════════════════════════════════════════════════════╗
║              TRAFFIC BRIEF                          ║
╠══════════════════════════════════════════════════════╣
║  Target URL: <where traffic lands>                   ║
║  Platform(s): 微博 / 知乎 / 小红书 / 全部            ║
║  Topic Keywords: <hot trend to piggyback>            ║
║  Target Audience: <who you want>                     ║
║  CTA: <what visitor does on arrival>                 ║
║  Posting Time: <optimal posting window>             ║
╚══════════════════════════════════════════════════════╝
```

---

## 🔁 The Traffic Loop

```
STEP 1: HOT TOPIC DISCOVERY
  → Mine 微博/知乎/百度/抖音 热搜
  → Filter by: relevance + timeliness + competition
  ↓
STEP 2: CONTENT GENERATION
  → Generate platform-specific content (not generic!)
  → Include: hook, value, CTA, hashtag
  ↓
STEP 3: SCHEDULE & DISTRIBUTE
  → Queue content for optimal posting times
  → Auto-post if credentials configured
  ↓
STEP 4: TRACK & FEEDBACK
  → Monitor clicks, engagement, conversions
  → Double down on what's working
```

---

## Step 1: HOT TOPIC DISCOVERY

### Platform Priority Matrix

| Platform | Best For | Post Frequency | Traffic Quality |
|----------|----------|---------------|----------------|
| 微博 | Breaking news, hot takes | 3-5x/day | Medium |
| 知乎 | In-depth answers, thought leadership | 1-2x/day | High |
| 小红书 | Visuals, tutorials, "X天搞定Y" | 1-3x/day | High |
| 百度 | SEO content, long-tail | 1x/day | Medium |
| 抖音/视频号 | Video content, demos | 1x/day | Very High |

### Topic Selection Criteria

**ONLY pursue topics where ALL of:**
- [ ] Trending NOW (within 24 hours)
- [ ] Related to your niche (AI tools / productivity / side income)
- [ ] You have something valuable to add (not just noise)
- [ ] Competition is not dominated by 10M+ follower accounts
- [ ] Hashtags exist and are active

### Topic Template

```json
{
  "topic": "Claude 4 发布",
  "platform": "知乎",
  "headline_angle": "Claude 4 vs GPT-5: 真实对比，普通用户选哪个？",
  "hook": "刚发布就被吹上天，但我用了3个月说点真话",
  "hashtags": ["#Claude4", "#AI工具", "#效率提升"],
  "target_url": "https://aisstt.fun/tools/claude",
  "cta": "点击查看国内平替"
}
```

---

## Step 2: CONTENT GENERATION

### Per-Platform Format Rules

#### 微博 (Weibo)
```
Format: Hook (20字) + Insight (100字) + CTA + Hashtags (3-5个)
Length: 150-300字
Optimal Length: 210字（刚好不被折叠）
Image: 必须配图，建议16:9
Timing: 12:00-13:00 / 18:00-19:00 / 22:00-23:00
```

#### 知乎 (Zhihu)
```
Format: 问题直接回答 → 论证3点 → 总结推荐
Length: 800-2000字
Structure: 
  1. 一句话直接回答问题
  2. 个人经历/数据支撑
  3. 3个核心论点（每个配具体例子）
  4. 产品推荐（自然植入，不硬广）
  5. 总结 + 评论区互动钩子
Image: 建议3-5张图（开头+内容+结尾）
Timing: 20:00-22:00
```

#### 小红书 (Xiaohongshu)
```
Format: 封面标题 + 开头钩子 + 正文干货 + 结尾互动
Length: 300-800字
Emoji: 大量使用，但别过度
Cover Style: 前后对比 / 数字冲击 / 对话式
Caption Structure:
  ① Hook (震惊数字或问题)
  ② Who/What/Why 介绍
  ③ 3-5个实用干货点
  ④ 我的推荐（软植入）
  ⑤ 评论区互动问题
Timing: 19:00-21:00
```

#### 微信公众号 (WeChat Official)
```
Format: 标题 + 引入 + 正文(3-5个小标题) + 总结 + 二维码/原文链接
Length: 1500-3000字
Opening: 蹭热点或提出痛点（50字内）
Body: 段落短，每段<100字，多用emoji
Closing: 总结要点 + 引导留言 + 转发激励
Image: 封面750x422 + 文中插图
```

---

## Step 3: SCHEDULE & DISTRIBUTE

### Optimal Posting Windows

| Platform | Breakfast | Lunch | Dinner | Late Night |
|----------|-----------|-------|--------|------------|
| 微博 | 7-9 | 12-13 | 18-19 | 22-23 |
| 知乎 | - | - | 20-22 | - |
| 小红书 | 7-9 | 12-14 | 19-21 | - |
| 抖音 | 7-9 | 12-14 | 18-20 | 21-23 |

### Content Queue Structure

```yaml
queue:
  - platform: weibo
    topic: "Claude 4发布"
    content_ref: "content/claude4_weibo_v1.md"
    scheduled_time: "2026-04-18 12:30:00"
    status: pending
  
  - platform: zhihu
    topic: "Claude 4对比GPT-5"
    content_ref: "content/claude4_zhihu_v1.md"
    scheduled_time: "2026-04-18 20:00:00"
    status: pending
```

---

## Step 4: TRACK & FEEDBACK

### Metrics to Monitor

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| 阅读量 (Views) | >500 | Improve headline |
| 互动率 (Engagement) | >3% | Add more hooks |
| 点击率 (CTR) | >2% | Improve CTA |
| 转化率 (Conversion) | >1% | Optimize landing page |

### Traffic Attribution

Always use UTM parameters:
```
https://target-url.com?utm_source=weibo&utm_medium=social&utm_campaign=claude4_2026
```

---

## 🚫 Refusal Conditions

Do NOT generate content if:
1. **Topic is politically sensitive** — don't touch
2. **Topic involves personal attacks** — defamation risk
3. **User provides no target URL** — traffic without destination is useless
4. **Spam intent detected** — pure promotional content with no value
5. **Misinformation risk** — don't amplify unverified claims
6. **Competitor bashing** — don't do this, legally and ethically risky

---

## 📝 Output Format

```markdown
## Traffic Campaign: <Topic>

### Platform Content Plan

#### 微博
**Posting Time**: 2026-04-18 12:30
**Hook**: <20字震惊体>
**Content**:
<150-300字>

**Hashtags**: #xxx #xxx #xxx

**Image**: [Generated cover image]

---

#### 知乎
**Posting Time**: 2026-04-18 20:00
**Question**: <目标问题>
**Answer Structure**: 
1. 直接回答
2. 个人经历
3. 3个论点
4. 产品推荐
5. 总结

**Image Suggestions**: [3张图建议]

---

### Analytics
**UTM Source**: weibo_zhihu_<topic>_<date>
**Target URL**: https://...
**Expected CTR**: X%
**Expected Daily Traffic**: X-XX UV
```

---

## Limitations

- Content generation quality depends on source material
- Posting requires platform credentials (not auto-posted without auth)
- Actual traffic depends on platform algorithms and competition
- This skill generates content and strategy — platform account management is separate
