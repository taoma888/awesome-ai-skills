# 🤖 Awesome AI Skills

> Hermes Agent 的 AI 赚钱与内容自动化技能集合 — 让 AI 像 CEO 一样思考：发现机会 → 验证需求 → 设计 MVP → 自动化执行 → 持续变现

---

## ✨ 功能

| 技能 | 描述 | 脚本 |
|------|------|------|
| 💰 **autonomous-earning-system** | 自主赚钱系统：需求挖掘 → 竞品分析 → MVP设计 → 变现方案 | `demand_miner.py`, `competitor_radar.py`, `mvp_generator.py` |
| 🚗 **content-autopilot** | 内容自动驾驶：热点发现 → AI改写 → 去AI化 → 多平台发布 | `fetch_trending.py`, `article_rewriter.py`, `auto_publisher.py` |
| 🔥 **trend-hunter** | 热点猎手：全网AI热点监控，实时推送 | `hot_topics.py` |
| 💸 **affiliate-monetization** | 联盟变现：联盟链接生成、推广文案、SEO优化 | `affiliate_link_generator.py` |

---

## 🚀 快速开始

### 需求挖掘
```bash
python3 skills/autonomous-earning-system/scripts/demand_miner.py "AI工具导航"
```

### 生成MVP方案
```bash
python3 skills/autonomous-earning-system/scripts/mvp_generator.py --idea "AI写作助手" --type affiliate
```

### 竞品分析
```bash
python3 skills/autonomous-earning-system/scripts/competitor_radar.py --urls https://tools.cn https://ai-bot.cn
```

### 热点发现
```bash
python3 skills/trend-hunter/scripts/hot_topics.py --platforms weibo,zhihu
```

### 联盟变现
```bash
python3 skills/affiliate-monetization/scripts/affiliate_link_generator.py Cursor --platforms weibo,zhihu
```

### 内容改写
```bash
python3 skills/content-autopilot/scripts/article_rewriter.py --topic "Claude 4发布" --length 1200
```

---

## 📦 安装

```bash
git clone https://github.com/YOUR_USERNAME/awesome-ai-skills.git
cd awesome-ai-skills
pip install requests
```

### 可选环境变量

```bash
# AI API (用于文章改写)
export DASHSCOPE_API_KEY="your-api-key"    # 阿里云百炼
export OPENAI_API_KEY="your-api-key"       # OpenAI

# 微信通知 (用于热点推送)
export WX_WORK_WEBHOOK="https://qyapi.weixin.qq.com/..."

# Cloudflare (用于自动发布到D1)
export CF_ACCOUNT_ID="your-account-id"
export CF_API_TOKEN="your-api-token"
export D1_DATABASE_ID="your-db-id"
```

---

## 📊 代码统计

| 指标 | 数值 |
|------|------|
| 技能数 | 4 |
| 脚本数 | 8 |
| 代码行数 | ~2300 |

---

## 🤝 贡献

欢迎提交 PR！每个技能都是一个独立目录：
- `SKILL.md` — 技能说明（触发条件、使用方法）
- `scripts/` — 可执行脚本
- `references/` — 参考资料（可选）
- `templates/` — 模板文件（可选）

---

## 📄 License

MIT — 详见 [LICENSE](LICENSE)
