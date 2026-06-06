---
name: minimax-usage
description: |
  追踪和查询 MiniMax API 的使用情况。当用户需要以下操作时使用此 Skill：
  - 查看 API Key 的 Token 使用量
  - 查询剩余配额和调用次数
  - 获取费用明细统计
  - 设置使用量预警
  触发词：MiniMax、使用量、token、余额、费用、配额
---

# MiniMax API 使用量追踪器

## 功能概述

此 Skill 用于查询 MiniMax API 的使用情况，包括 Token 消耗、调用次数、费用统计等。

## 使用方法

### 1. 查看当前使用量

```bash
python .claude/skills/minimax-usage/scripts/usage.py query --api-key YOUR_API_KEY
```

### 2. 指定模型查询

```bash
python .claude/skills/minimax-usage/scripts/usage.py query --api-key YOUR_API_KEY --model abab6.5s-chat
```

### 3. 查看详细费用统计

```bash
python .claude/skills/minimax-usage/scripts/usage.py query --api-key YOUR_API_KEY --detailed
```

### 4. 配置文件方式（推荐）

```bash
# 首次配置 API Key
python .claude/skills/minimax-usage/scripts/usage.py config --api-key YOUR_API_KEY

# 之后直接查询
python .claude/skills/minimax-usage/scripts/usage.py query
```

### 5. 设置使用量预警

```bash
# 设置使用量达到 80% 时预警
python .claude/skills/minimax-usage/scripts/usage.py alert --threshold 80
```

## 输出格式

```
=== MiniMax API 使用情况 ===

模型: abab6.5s-chat
─────────────────────────────────
已用 Token:     1,234,567
  - 提示 Token:    987,654
  - 完成 Token:    246,913
─────────────────────────────────
调用次数:       5,678 次
费用总额:       ¥ 123.45

剩余配额:       ¥ 876.55
─────────────────────────────────
使用进度:       ████████░░ 12.3%
```

## 常见使用场景

| 用户请求 | 执行命令 |
|---------|---------|
| "MiniMax 还剩多少额度" | `python .claude/skills/minimax-usage/scripts/usage.py query` |
| "查看我的 API 使用量" | `python .claude/skills/minimax-usage/scripts/usage.py query --detailed` |
| "Token 消耗情况" | `python .claude/skills/minimax-usage/scripts/usage.py query` |
| "设置使用量预警" | `python .claude/skills/minimax-usage/scripts/usage.py alert --threshold 80` |

## 注意事项

1. **API Key 安全**：建议使用配置文件方式，避免在命令行中暴露 Key
2. **免费额度**：免费额度可能有有效期限制
3. **计费差异**：不同模型（abab4 / abab5 / abab6）计费标准不同
4. **查询频率**：避免过于频繁查询，建议间隔至少 1 分钟

## API Key 配置

首次使用需要配置 API Key，有两种方式：

**方式一：配置文件**
```bash
python .claude/skills/minimax-usage/scripts/usage.py config --api-key YOUR_KEY
```

**方式二：环境变量**
```bash
export MINIMAX_API_KEY="YOUR_API_KEY"
```

配置文件存储在 `~/.claude/minimax_usage.json`
