# 💸 AI工具联盟变现系统

> 自动生成联盟链接、SEO优化、社交推广文案，让流量自动变现

---

## 触发条件

```
用户说：佣金、联盟、返佣、变现、Affiliate、赚钱链接、
推广工具、带货、分销、返现
```

---

## 核心功能

### 1. 联盟链接生成器
输入工具名 → 自动生成带返佣的推广链接

**支持的联盟平台：**
| 平台 | 佣金率 | 注册地址 |
|------|--------|---------|
| 阿里云百炼 | 15-30% | 阿里云官网 |
| Amazon AI服务 | 3-10% | Amazon Associates |
| Canva | 30-60% | Canva Affiliate |
| Notion | 50% | Notion Partners |
| Figma | 30-50% | Figma Affiliate |
| OpenAI API | 10-20% | OpenAI Partner |
| Cursor | 40% | Cursor Affiliate |
| GitHub Copilot | 30% | GitHub Partner |

### 2. SEO优化器
自动生成：
- 工具描述（150字，含关键词）
- Meta标题/描述
- FAQ问答（5条）
- 内链建议

### 3. 社交推广文案
一键生成：
- 微博推广帖（含话题）
- 知乎回答片段
- 小红书笔记
- 公众号推荐文

---

## 使用方式

```bash
# 生成联盟链接
python scripts/affiliate_link_generator.py --tool "Cursor"

# 生成推广文案
python scripts/social_poster.py --tool "Claude" --platform weibo

# 批量生成工具变现包
python scripts/batch_monetization.py --category "AI编程"
```

---

## 变现计算器

| 工具 | 月UV | 转化率 | 佣金率 | 月预估收入 |
|------|------|--------|--------|-----------|
| Cursor | 500 | 3% | 40% | ¥600 |
| Notion | 800 | 2% | 50% | ¥800 |
| Canva | 1000 | 5% | 30% | ¥1500 |
| Figma | 300 | 3% | 40% | ¥360 |
