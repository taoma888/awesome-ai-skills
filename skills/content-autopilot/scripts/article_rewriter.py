#!/usr/bin/env python3
"""
AI文章改写器 — Article Rewriter
输入主题 → 自动抓取资料 → 生成低查重率伪原创文章
"""

import sys
import json
import argparse
import os
import re
from datetime import datetime

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# AI改写提示词
REWRITE_PROMPT = """
你是一个资深科技博主。请根据以下素材，写一篇公众号风格的文章。

要求：
1. 查重率 < 40%（用句式变化而非简单词替换）
2. 口语化表达，像在和朋友聊天
3. 加入个人情绪：惊讶/兴奋/困惑/期待
4. 加设问互动：适当问"你觉得呢？"
5. 字数：{length}字左右
6. 格式：emoji + 分割线 + 加粗
7. 结尾加互动引导

文章结构：
- 一个吸引眼球的标题（含emoji）
- 开头：抛出痛点/场景
- 中间：3-4个要点，每个要点有具体例子
- 结尾：总结 + 行动号召

素材：
{content}

请直接输出文章内容，不要解释。
"""

# 去AI化词表
DEAI_WORDS = [
    "说实话", "没想到", "真的太", "我也", "你们", "朋友们",
    "感觉", "估计", "大概", "其实", "个人", "亲身",
]

AI_FILLER_WORDS = [
    "首先", "其次", "再次", "最后", "因此", "综上所述",
    "值得注意的是", "不难发现", "可以看出", "总的来说",
]


def fetch_content(url: str) -> str:
    """抓取文章内容"""
    if not REQUESTS_AVAILABLE:
        return ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        text = resp.text
        # 移除script/style
        text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:5000]
    except Exception as e:
        print(f"⚠️  抓取失败: {e}", file=sys.stderr)
        return ""


def call_ai_api(topic: str, content: str = "", length: int = 1200) -> str:
    """调用AI改写API"""
    # 优先使用阿里云百炼
    api_key = os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if api_key and "dashscope" not in api_key.lower() and "openai" not in api_key.lower():
        # 阿里云百炼
        return call_dashscope(topic, content, length)
    elif api_key:
        return call_openai_compatible(topic, content, length)
    else:
        return generate_demo_article(topic, length)


def call_dashscope(topic: str, content: str, length: int) -> str:
    """阿里云百炼 API"""
    import requests
    prompt = REWRITE_PROMPT.format(content=content or f"关于：{topic}", length=length)
    
    try:
        resp = requests.post(
            "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen-plus",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": length * 3,
                "temperature": 0.8
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️  API调用失败: {e}", file=sys.stderr)
        return generate_demo_article(topic, length)


def call_openai_compatible(topic: str, content: str, length: int) -> str:
    """OpenAI兼容API"""
    import requests
    prompt = REWRITE_PROMPT.format(content=content or f"关于：{topic}", length=length)
    
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": length * 3,
                "temperature": 0.8
            },
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"⚠️  API调用失败: {e}", file=sys.stderr)
        return generate_demo_article(topic, length)


def generate_demo_article(topic: str, length: int) -> str:
    """演示模式：生成示例文章结构"""
    return f"""
# 🔥 {topic} — 这可能是你今年最该了解的机会

---

姐妹们，今天必须跟你们聊聊 **{topic}** 这件事。

说实话，我之前一直没当回事，觉得这东西离我们普通人太远了。但是！上个月我亲眼看到一个朋友用它
"""

def deai_process(text: str) -> str:
    """
    去AI化处理
    1. 替换AI填充词
    2. 增加口语化表达
    3. 添加互动设问
    """
    result = text
    
    # 替换AI腔词
    for filler in AI_FILLER_WORDS:
        result = result.replace(filler, get_replacement(filler))
    
    # 随机添加口语词
    import random
    if random.random() > 0.5:
        result = result.replace("。", "。" + random.choice(DEAI_WORDS) + "，", 1)
    
    # 检查是否有互动引导
    if "？" not in result[-500:]:
        result += "\n\n你们觉得怎么样？评论区告诉我！👇"
    
    return result


def get_replacement(word: str) -> str:
    replacements = {
        "首先": "开头先说",
        "其次": "再来",
        "再次": "还有一点",
        "最后": "说白了",
        "因此": "说到底",
        "综上所述": "总而言之",
    }
    return replacements.get(word, "")


def calculate_rewrite_stats(original: str, rewritten: str) -> dict:
    """计算改写统计"""
    orig_len = len(original)
    new_len = len(rewritten)
    overlap = sum(1 for a, b in zip(original, rewritten) if a == b)
    
    return {
        "original_length": orig_len,
        "rewritten_length": new_len,
        "length_change_pct": round((new_len - orig_len) / max(orig_len, 1) * 100, 1),
        "estimated_similarity": min(round(overlap / max(len(rewritten), 1) * 100, 1), 99),
        "word_count": len(rewritten.replace("\n", "").split()),
    }


def main():
    parser = argparse.ArgumentParser(description="AI文章改写器")
    parser.add_argument("--topic", "-t", required=True, help="文章主题")
    parser.add_argument("--url", "-u", help="原始文章URL（用于抓取素材）")
    parser.add_argument("--content", "-c", help="原始文章内容（直接传入）")
    parser.add_argument("--length", "-l", type=int, default=1200, help="目标字数")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    args = parser.parse_args()
    
    print(f"✍️  开始改写：{args.topic}")
    
    # 获取原始内容
    original_content = args.content
    if args.url and not original_content:
        print(f"  📡 抓取原始文章: {args.url}")
        original_content = fetch_content(args.url)
    
    # 调用AI改写
    print(f"  🤖 AI改写中（目标 {args.length} 字）...")
    rewritten = call_ai_api(args.topic, original_content, args.length)
    
    if not rewritten or len(rewritten) < 100:
        print("⚠️  API未返回有效内容，使用演示数据")
        rewritten = generate_demo_article(args.topic, args.length)
    
    # 去AI化
    print("  🔧 去AI化处理...")
    final = deai_process(rewritten)
    
    # 统计
    stats = calculate_rewrite_stats(original_content or "", final)
    
    result = {
        "topic": args.topic,
        "original_source": args.url or "user_input",
        "article": final,
        "stats": stats,
        "generated_at": datetime.now().isoformat()
    }
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("\n" + "="*50)
        print(final)
        print("="*50)
        print(f"\n📊 统计: {stats['word_count']}字 | 预估相似度: {stats['estimated_similarity']}%")
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(final)
        print(f"\n✅ 已保存到: {args.output}")


if __name__ == "__main__":
    main()
