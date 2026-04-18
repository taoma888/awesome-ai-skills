# 🚗 内容自动驾驶 — Content Autopilot

> 全自动：热点发现 → AI改写 → 去AI化 → 多平台适配 → 自动发布 → 数据追踪

---

## 触发条件

```
用户说：写文章、创作、内容、更新文章、自动发布、
热点蹭热度、伪原创、改写、AI写作
```

---

## 核心流水线（7步）

```
Step 1: 热点发现        → 抓取微博/知乎/微信/B站热搜
Step 2: 内容规划        → 生成5W1H大纲
Step 3: 素材搜集        → 抓取权威来源（TechCrunch/机器之心等）
Step 4: AI改写          → 低查重率伪原创（<40%）
Step 5: 去AI化处理      → 口语化+情绪词+设问互动
Step 6: 多平台适配      → 公众号/微博/知乎格式
Step 7: 自动发布        → 写入D1 / 发布到平台
```

---

## 改写标准（必须遵守）

| 指标 | 要求 |
|------|------|
| 查重率 | < 40%（用句式变化而非词替换） |
| AI感 | 去除"首先、其次、因此、综上所述" |
| 情绪词 | 加"说实话、我个人、没想到、真的太" |
| 互动 | 加"你们觉得呢？评论区告诉我！" |
| 字数 | 800-2000字 |
| 配图 | Unsplash CC0 图片一张 |
| 格式 | 公众号格式：emoji + 分割线 + 加粗 |
| 原创标识 | 每篇文章末尾加"原创 by AI" |

---

## 使用示例

```bash
# 获取今日热点
python scripts/fetch_trending.py --platforms weibo,zhihu --limit 10

# 改写文章
python scripts/article_rewriter.py --topic "Claude 4发布" --length 1200

# 一键发布到D1
python scripts/auto_publisher.py --article "output/claude4_rewrite.md" --platforms d1,weixin
```

---

## 脚本说明

### `fetch_trending.py`
抓取多平台热搜，支持：
- 微博热搜 TOP50
- 知乎热榜 TOP20
- 微信热文（搜一搜）
- 百度指数飙升
- Google Trends

### `article_rewriter.py`
AI改写核心引擎：
- 输入：原始文章URL或关键词
- 输出：改写后文章（Markdown格式）
- 去AI化处理（口语化/情绪化）

### `auto_publisher.py`
多平台自动发布：
- D1数据库（直接写入）
- 微信公众号（API发布）
- 知乎专栏
- 微博长文

---

## 配置

```bash
export D1_DATABASE_ID="xxx"
export CF_ACCOUNT_ID="xxx" 
export CF_API_TOKEN="xxx"
export AI_MODEL="qwen3.5-plus"  # 阿里云百炼
```
