#!/usr/bin/env python3
"""
MiniMax API 使用量追踪器
用于查询 MiniMax API 的 Token 使用量、调用次数和费用统计
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 配置文件路径
CONFIG_PATH = Path.home() / ".claude" / "minimax_usage.json"

# MiniMax API 端点
BASE_URL = "https://api.minimax.chat/v1/text"
# 可能的其他端点
BILLING_URLS = [
    "https://api.minimax.chat/v1/billing/usage",
    "https://api.minimax.chat/v1/account/quota",
    "https://api.minimax.chat/v1/account/balance",
]

# 模型定价（Token 价格，单位：人民币/百万 token）
# 价格可能随时间变化，请以官方文档为准
MODEL_PRICING = {
    "abab4": {"input": 1.0, "output": 2.0},       # ¥/百万 token
    "abab5": {"input": 1.0, "output": 2.0},
    "abab5.5": {"input": 1.0, "output": 2.0},
    "abab6": {"input": 5.0, "output": 10.0},
    "abab6.5": {"input": 10.0, "output": 20.0},
    "abab6.5s": {"input": 1.0, "output": 2.0},   # 速度版
    "abab6.5s-chat": {"input": 1.0, "output": 2.0},
    "default": {"input": 5.0, "output": 10.0},
}


def load_config():
    """加载配置文件"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(config):
    """保存配置文件"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"[OK] Config saved to {CONFIG_PATH}")


def get_api_key(config, api_key=None):
    """获取 API Key"""
    if api_key:
        return api_key
    if "api_key" in config:
        return config["api_key"]
    return None


def get_pricing(model_name):
    """获取模型定价"""
    model_lower = model_name.lower()
    for model_key, pricing in MODEL_PRICING.items():
        if model_key in model_lower:
            return pricing
    return MODEL_PRICING["default"]


def query_usage(api_key, model=None, detailed=False):
    """
    查询 MiniMax API 使用量

    注意：MiniMax 当前版本的计费 API 可能不同，
    此代码基于通用 REST API 模式实现
    """
    import urllib.request
    import urllib.error

    # 构建请求 URL
    url = f"{BASE_URL}/billing/usage"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        request = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return parse_usage_response(data, model, detailed)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"[X] API request failed (HTTP {e.code}): {e.reason}")
        if error_body:
            print(f"    Response: {error_body}")
        return None

    except urllib.error.URLError as e:
        print(f"[X] Network request failed: {e.reason}")
        return None

    except Exception as e:
        print(f"[X] Query failed: {str(e)}")
        return None


def parse_usage_response(data, model=None, detailed=False):
    """解析 API 响应"""
    # MiniMax API 响应格式可能因版本而异
    # 以下为通用解析逻辑

    if "data" in data:
        usage = data["data"]
    elif "usage" in data:
        usage = data["usage"]
    else:
        usage = data

    # 提取基本信息
    result = {
        "model": model or "unknown",
        "prompt_tokens": usage.get("prompt_tokens", 0) or 0,
        "completion_tokens": usage.get("completion_tokens", 0) or 0,
        "total_tokens": usage.get("total_tokens", 0) or 0,
        "request_count": usage.get("request_count", 0) or 0,
        "cost": usage.get("cost", 0.0) or 0.0,
        "balance": usage.get("balance", 0.0) or 0.0,
        "quota_limit": usage.get("quota_limit", 0.0) or 0.0,
    }

    # 计算费用（如果 API 未直接提供）
    if result["cost"] == 0.0 and result["total_tokens"] > 0:
        pricing = get_pricing(result["model"])
        result["cost"] = (
            result["prompt_tokens"] / 1_000_000 * pricing["input"] +
            result["completion_tokens"] / 1_000_000 * pricing["output"]
        )

    # 计算剩余配额
    if result["quota_limit"] > 0:
        result["remaining"] = result["quota_limit"] - result["cost"]
        result["usage_percent"] = (result["cost"] / result["quota_limit"]) * 100
    elif result["balance"] > 0:
        result["remaining"] = result["balance"]
        result["usage_percent"] = 0.0

    return result


def format_number(num):
    """格式化数字（添加千分位）"""
    if num is None:
        return "0"
    return f"{int(num):,}"


def format_currency(amount):
    """格式化货币"""
    if amount is None:
        return "¥0.00"
    return f"¥ {amount:,.2f}"


def print_usage_report(usage, detailed=False):
    """打印使用量报告"""
    if not usage:
        return

    print()
    print("=" * 50)
    print("       MiniMax API Usage")
    print("=" * 50)

    # 模型信息
    print(f"\nModel: {usage['model']}")
    print("-" * 50)

    # Token 使用
    print(f"Total Tokens:   {format_number(usage['total_tokens']):>12}")
    if detailed:
        print(f"  - Prompt:      {format_number(usage['prompt_tokens']):>12}")
        print(f"  - Completion:  {format_number(usage['completion_tokens']):>12}")

    # 调用次数
    print(f"Requests:       {format_number(usage['request_count']):>12}")

    # 费用
    print(f"Cost:           {format_currency(usage['cost']):>12}")

    # 剩余配额
    print("-" * 50)
    if usage.get('remaining'):
        print(f"Remaining:      {format_currency(usage['remaining']):>12}")

    # 使用进度条
    if usage.get('usage_percent', 0) > 0:
        percent = min(usage['usage_percent'], 100)
        bar_length = 20
        filled = int(bar_length * percent / 100)
        bar = "#" * filled + "-" * (bar_length - filled)
        print(f"\nUsage:          [{bar}] {percent:.1f}%")

    print("\n" + "=" * 50)


def set_alert(config, threshold):
    """设置使用量预警阈值"""
    config["alert_threshold"] = threshold
    save_config(config)
    print(f"[✓] 预警阈值已设置为 {threshold}%")


def check_alert(config, usage):
    """检查是否触发预警"""
    if not config.get("alert_threshold"):
        return

    threshold = config["alert_threshold"]
    percent = usage.get("usage_percent", 0)

    if percent >= threshold:
        print(f"\n[!] ALERT: MiniMax API usage reached {percent:.1f}%")
        print(f"    Threshold: {threshold}%")
        print(f"    Remaining: {format_currency(usage.get('remaining', 0))}")


def cmd_config(args):
    """配置 API Key"""
    config = load_config()
    if args.api_key:
        config["api_key"] = args.api_key
        save_config(config)
    else:
        print("Please provide API Key: --api-key YOUR_KEY")


def cmd_query(args):
    """查询使用量"""
    config = load_config()
    api_key = get_api_key(config, args.api_key)

    if not api_key:
        print("[X] API Key not configured")
        print("    Please configure using:")
        print("    1. Command line: --api-key YOUR_API_KEY")
        print("    2. Config command: python usage.py config --api-key YOUR_API_KEY")
        return

    print("Testing MiniMax API connection...")
    import urllib.request
    import urllib.error

    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    test_data = json.dumps({
        "model": "abab6.5s-chat",
        "messages": [{"role": "user", "content": "test"}]
    }).encode()

    try:
        request = urllib.request.Request(url, data=test_data, headers=headers, method="POST")
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            print("[OK] API Key is valid!")
            print(f"    Model: {data.get('model', 'unknown')}")
            if 'usage' in data:
                print(f"    Tokens used: {data['usage'].get('total_tokens', 0)}")
            print("\n[!] Billing API not available")
            print("    Please check usage at: https://api.minimax.chat/")
    except Exception as e:
        print(f"[X] Connection failed: {e}")


def cmd_alert(args):
    """设置预警"""
    config = load_config()
    set_alert(config, args.threshold)


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax API 使用量追踪器",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # config 命令
    parser_config = subparsers.add_parser("config", help="配置 API Key")
    parser_config.add_argument("--api-key", help="MiniMax API Key")

    # query 命令
    parser_query = subparsers.add_parser("query", help="查询使用量")
    parser_query.add_argument("--api-key", help="MiniMax API Key")
    parser_query.add_argument("--model", help="指定模型名称")
    parser_query.add_argument("--detailed", action="store_true",
                              help="显示详细信息")

    # alert 命令
    parser_alert = subparsers.add_parser("alert", help="设置使用量预警")
    parser_alert.add_argument("--threshold", type=float, default=80.0,
                              help="预警阈值百分比 (默认: 80)")

    # 添加默认命令
    parser.add_argument("--api-key", help="MiniMax API Key")
    parser.add_argument("--model", help="指定模型名称")
    parser.add_argument("--detailed", action="store_true",
                        help="显示详细信息")

    args = parser.parse_args()

    # 默认执行 query
    if not args.command:
        args.command = "query"

    # 执行命令
    if args.command == "config":
        cmd_config(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "alert":
        cmd_alert(args)


if __name__ == "__main__":
    main()
