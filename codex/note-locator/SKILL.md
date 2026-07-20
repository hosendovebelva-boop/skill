---
name: note-locator
description: |
  在Obsidian知识库中定位笔记并解析关联。当用户需要以下操作时使用此Skill：
  - 搜索笔记（如"找一下虚函数的笔记"、"搜索关于指针的内容"）
  - 查找相关知识点（如"智能指针相关的笔记有哪些"）
  - 定位特定主题（如"TCP编程在哪"、"多态相关笔记"）
  - 了解笔记关联（如"这个笔记链接了哪些其他笔记"）
  触发词：搜索、查找、定位、找、哪里、相关笔记、关联笔记、wiki-link
---

# Note Locator - Obsidian笔记定位器

## 功能概述

此Skill用于在C++ Obsidian知识库中快速定位笔记，并解析其wiki-link关联关系。

## 使用方法

### 基本搜索
```bash
python .claude/skills/note-locator/scripts/locate.py "关键词"
```

### 指定搜索目录
```bash
python .claude/skills/note-locator/scripts/locate.py "关键词" --path "C++基础"
```

### 只返回路径（不解析链接）
```bash
python .claude/skills/note-locator/scripts/locate.py "关键词" --no-links
```

### 显示更多候选结果
```bash
python .claude/skills/note-locator/scripts/locate.py "关键词" --top 5
```

## 输出格式

```
=== 笔记定位结果 ===

目标笔记: C++基础/12. OOP/12.3 多态/12.3.2 虚函数.md
匹配度: 95%

直接关联笔记 (3个):
  → C++基础/12. OOP/12.3 多态/12.3.1 静态多态与动态多态.md
  → C++基础/6. 指针/6.9 指针总结.md
  → C++基础/1. 计算机基础/1.2 函数栈帧建立与销毁.md

其他候选 (如未精确匹配):
  1. [85%] C++高级/6. OOP/6.3 虚函数深入.md
  2. [72%] C++基础/12. OOP/12.3 多态/12.3.7 从内存角度理解.md
```

## 使用场景示例

| 用户请求 | 执行命令 |
|---------|---------|
| "找一下虚函数的笔记" | `python .claude/skills/note-locator/scripts/locate.py "虚函数"` |
| "智能指针相关的笔记有哪些" | `python .claude/skills/note-locator/scripts/locate.py "智能指针"` |
| "TCP编程在哪个目录" | `python .claude/skills/note-locator/scripts/locate.py "TCP编程"` |
| "搜索关于epoll的内容" | `python .claude/skills/note-locator/scripts/locate.py "epoll"` |

## 注意事项

1. 搜索基于文件名模糊匹配，支持中文关键词
2. 自动解析目标笔记中的 `[[wiki-links]]` 并定位关联文件
3. 如果链接目标不存在，会标记为 `[未找到]`
4. 默认返回匹配度最高的结果，可用 `--top N` 返回多个候选
