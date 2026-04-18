#!/usr/bin/env python3
"""
📊 Revenue Dashboard — 收入追踪仪表盘
聚合所有收入来源，每日自动汇报
"""

import sys
import json
import argparse
import os
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# 默认数据文件
DATA_DIR = Path.home() / ".hermes" / "revenue"
STATE_FILE = DATA_DIR / "state.json"


# 内置收入类型
INCOME_TYPES = {
    "affiliate": "联盟佣金",
    "ads": "广告收入",
    "subscription": "订阅收入",
    "digital": "数字产品",
    "service": "服务收入"
}


def ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "income_streams": {},
        "daily_records": {},
        "last_updated": None
    }


def save_state(state: dict):
    ensure_data_dir()
    state["last_updated"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def add_income(stream: str, amount: float, status: str = "pending", note: str = ""):
    """添加一笔收入记录"""
    state = load_state()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if stream not in state["income_streams"]:
        state["income_streams"][stream] = {
            "name": INCOME_TYPES.get(stream, stream),
            "records": [],
            "total_earned": 0,
            "total_paid": 0,
            "pending": 0
        }
    
    record = {
        "date": today,
        "amount": amount,
        "status": status,
        "note": note,
        "created_at": datetime.now().isoformat()
    }
    
    state["income_streams"][stream]["records"].append(record)
    state["income_streams"][stream]["total_earned"] += amount
    if status == "paid":
        state["income_streams"][stream]["total_paid"] += amount
    elif status == "pending":
        state["income_streams"][stream]["pending"] += amount
    
    save_state(state)
    return record


def get_daily_summary(days: int = 7) -> dict:
    """获取每日收入摘要"""
    state = load_state()
    today = datetime.now()
    
    result = {
        "period": f"{days} days",
        "days": {},
        "totals": {k: 0 for k in INCOME_TYPES},
        "total_earned": 0,
        "total_paid": 0,
        "total_pending": 0
    }
    
    for i in range(days):
        day = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        result["days"][day] = {k: 0 for k in INCOME_TYPES}
    
    for stream, data in state["income_streams"].items():
        for record in data["records"]:
            day = record["date"]
            if day in result["days"]:
                result["days"][day][stream] += record["amount"]
                result["totals"][stream] += record["amount"]
        
        result["total_earned"] += data["total_earned"]
        result["total_paid"] += data["total_paid"]
        result["total_pending"] += data["pending"]
    
    return result


def calculate_metrics(summary: dict) -> dict:
    """计算关键指标"""
    total = summary["total_earned"]
    paid = summary["total_paid"]
    pending = summary["total_pending"]
    days = len(summary["days"])
    
    # 每日平均
    daily_avg = total / days if days > 0 else 0
    
    # 年度预估
    yearly_projection = daily_avg * 365
    
    # MRR (月度经常性收入, 以pending为主估算)
    mrr = pending * 4  # 假设pending每月稳定
    
    # 今日收入
    today = datetime.now().strftime("%Y-%m-%d")
    today_income = summary["days"].get(today, {}).copy()
    
    return {
        "total_earned": total,
        "total_paid": paid,
        "total_pending": pending,
        "daily_average": round(daily_avg, 2),
        "monthly_projection": round(daily_avg * 30, 2),
        "yearly_projection": round(yearly_projection, 2),
        "mrr": round(mrr, 2),
        "paid_ratio": round(paid / total * 100, 1) if total > 0 else 0,
        "pending_ratio": round(pending / total * 100, 1) if total > 0 else 0
    }


def get_top_performer(summary: dict) -> dict:
    """找出最赚钱的渠道"""
    if not summary["totals"]:
        return None
    
    top_stream = max(summary["totals"].items(), key=lambda x: x[1])
    if top_stream[1] > 0:
        return {
            "stream": top_stream[0],
            "name": INCOME_TYPES.get(top_stream[0], top_stream[0]),
            "amount": top_stream[1]
        }
    return None


def format_daily_report(summary: dict, metrics: dict) -> str:
    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    today_income = summary["days"].get(today_str, {})
    today_total = sum(today_income.values())
    
    # 昨天
    yesterday = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday_income = sum(summary["days"].get(yesterday, {}).values())
    
    # 变化
    if yesterday_income > 0:
        change = ((today_total - yesterday_income) / yesterday_income) * 100
        change_str = f"{'+' if change >= 0 else ''}{change:.1f}%"
    else:
        change_str = "N/A"
    
    lines = [
        f"┌─────────────────────────────────────────────┐",
        f"│  📊 收入日报 — {today.strftime('%Y-%m-%d %H:%M')}          │",
        f"├─────────────────────────────────────────────┤",
        f"│  💰 今日收入: ¥{today_total:.2f}                      │",
        f"│     vs 昨日: {change_str}                          │",
        f"│                                              │",
    ]
    
    # 各渠道今日
    if today_income:
        for stream, amount in today_income.items():
            if amount > 0:
                name = INCOME_TYPES.get(stream, stream)
                lines.append(f"│    • {name}: ¥{amount:.2f}                    │")
    
    lines.extend([
        f"│                                              │",
        f"│  📈 近7天总收入: ¥{metrics['total_earned']:.2f}              │",
        f"│     日均: ¥{metrics['daily_average']:.2f}                    │",
        f"│     月预估: ¥{metrics['monthly_projection']:.2f}               │",
        f"│     年预估: ¥{metrics['yearly_projection']:.2f}              │",
        f"│                                              │",
        f"│  💵 已到账: ¥{metrics['total_paid']:.2f} ({metrics['paid_ratio']}%)          │",
        f"│  ⏳ 待确认: ¥{metrics['total_pending']:.2f} ({metrics['pending_ratio']}%)          │",
    ])
    
    # Top performer
    top = get_top_performer(summary)
    if top:
        lines.append(f"│                                              │")
        lines.append(f"│  🏆 本期最赚: {top['name']} ¥{top['amount']:.2f}        │")
    
    lines.extend([
        f"└─────────────────────────────────────────────┘",
    ])
    
    return '\n'.join(lines)


def send_wechat_report(message: str, webhook_url: str = None) -> bool:
    """发送微信通知"""
    wx_hook = webhook_url or os.getenv("WECHAT_WEBHOOK_URL") or os.getenv("WX_WORK_WEBHOOK")
    if not wx_hook or not REQUESTS_AVAILABLE:
        return False
    
    try:
        payload = {
            "msgtype": "text",
            "text": {
                "content": message.replace("│", "|").replace("┌", "").replace("┐", "").replace("├", "").replace("┤", "").replace("└", "").replace("─", "-").replace("┬", "").replace("┴", "").replace("─", "")
            }
        }
        resp = requests.post(wx_hook, json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"⚠️ 微信通知失败: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="📊 收入追踪仪表盘")
    parser.add_argument("--add", "-a", nargs=3, metavar=("STREAM", "AMOUNT", "STATUS"),
                       help="添加收入: stream amount status(pending/paid)")
    parser.add_argument("--summary", "-s", action="store_true", help="显示收入摘要")
    parser.add_argument("--days", "-d", type=int, default=7, help="统计天数")
    parser.add_argument("--report", "-r", action="store_true", help="生成完整报告")
    parser.add_argument("--notify", "-n", action="store_true", help="发送微信通知")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    args = parser.parse_args()
    
    if args.add:
        stream, amount, status = args.add
        record = add_income(stream, float(amount), status)
        print(f"✅ 已添加: {stream} +¥{amount} ({status})")
    
    if args.summary or args.report:
        summary = get_daily_summary(args.days)
        metrics = calculate_metrics(summary)
        
        if args.json:
            print(json.dumps({"summary": summary, "metrics": metrics}, ensure_ascii=False, indent=2))
        else:
            print(format_daily_report(summary, metrics))
            
            if args.notify:
                if send_wechat_report(format_daily_report(summary, metrics)):
                    print("\n✅ 微信通知已发送")
                else:
                    print("\n⚠️ 微信通知发送失败（未配置webhook）")
    
    if not any([args.add, args.summary, args.report]):
        # 默认显示日报
        summary = get_daily_summary(7)
        metrics = calculate_metrics(summary)
        print(format_daily_report(summary, metrics))
        print("\n使用 --help 查看更多选项")


if __name__ == "__main__":
    main()
