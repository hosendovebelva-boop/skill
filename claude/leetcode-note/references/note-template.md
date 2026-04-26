# LeetCode Note Template

Use this template when creating a new LeetCode problem note.
Replace all `{placeholders}` with actual content. Delete sections that are not applicable.

---

````markdown
---
阅读次数: 0
tags:
  - 力扣
  - {算法分类}
aliases:
  - {英文题名, e.g. Two Sum}
---

# {题号}. {中文题名}

## {算法技巧名}简介

> [!note]
> 如果该算法技巧已在其他题目笔记中介绍过，使用 wikilink 引用即可（如 `参见 [[3. 无重复字符的最长子串]]`），并删除此节。

{用2-3段话介绍该算法技巧的核心思想、适用场景。}

### 核心思想

{一句话概括该技巧的本质。}

> [!tip]
> {适用场景提示：什么样的题目特征适合使用这种技巧。}

### 基本模版

```cpp
// {算法技巧} 通用代码框架
{通用代码模版}
```

---

## 题目描述

{用自己的语言简述题目要求和关键约束条件。不要复制原题。}

### 示例

```text
输入：{示例输入}
输出：{示例输出}
解释：{示例解释}
```

> [!important]
> {关键约束或边界条件提示。}

---

## 解题思路

{分步骤解释思路。配合 SVG 图解展示算法执行过程。}

### 步骤分解

1. {步骤1}
2. {步骤2}
3. {步骤3}

### 图解

![[5_1_{题号}_1.svg|760]]

{对图解的文字说明：每一步发生了什么，关键状态如何变化。}

---

## 代码实现

```cpp
class Solution {
public:
    {返回类型} {方法名}({参数列表}) {
        // {实现代码}
    }
};
```

### 代码分析

{对代码中关键行的逐行说明。重点解释不容易理解的部分。}

---

## 易错点

1. {易错点1：描述 + 正确做法}
2. {易错点2：描述 + 正确做法}
3. {易错点3：描述 + 正确做法}

> [!warning]
> {最常见的陷阱，特别提醒。}

---

## 复杂度

- **时间复杂度**：`O(?)` — {简要分析}
- **空间复杂度**：`O(?)` — {简要分析}

---

## 相关链接

- [[14.x {STL文件名}]] — {用途说明}
- [[{相关题号}. {相关题名}]] — {关联说明，如"同类题型"、"前置知识"、"进阶变体"}
````

---

## Template Usage Notes

1. **算法技巧简介** section: Only include when this problem introduces a technique for the first time. If already covered in an earlier note, replace with a one-line wikilink reference and delete the subsections.

2. **示例推演** (optional section): For complex problems, add a step-by-step trace after `解题思路`:
   ```text
   ## 示例推演
   
   以输入 `{example}` 为例：
   
   | 步骤 | 状态 | 操作 | 结果 |
   |------|------|------|------|
   | 1 | ... | ... | ... |
   ```

3. **多解法** (optional): If documenting multiple approaches, repeat the `解题思路` + `代码实现` sections with clear headings:
   ```
   ## 解法一：{方法名}
   ### 解题思路
   ### 代码实现
   
   ## 解法二：{方法名}
   ### 解题思路
   ### 代码实现
   ```

4. **Callout types**:
   - `[!tip]` — 适用场景、技巧提示
   - `[!important]` — 关键区分、核心概念
   - `[!warning]` — 易错陷阱、常见错误
   - `[!note]` — 补充说明、学习建议
