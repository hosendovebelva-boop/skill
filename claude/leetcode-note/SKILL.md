---
name: leetcode-note
description: >-
  Create, categorize, and cross-link LeetCode problem notes in the Obsidian vault
  under `5.算法/力扣/`. Use when the user asks to record a LeetCode problem, create
  algorithm notes, migrate existing LeetCode notes into categories, or when the user
  mentions "力扣", "LeetCode", a specific problem number with algorithm context, or
  "算法笔记". This skill also handles organizing notes by algorithm type (动态规划,
  滑动窗口, etc.) and generating SVG solution flowcharts.
---

# LeetCode Note Skill

Record LeetCode problems and solutions as structured Obsidian notes with SVG flowcharts, STL cross-references, and algorithm-type categorization.

**Paired skills:**
- `obsidian-markdown` — for Obsidian-flavored formatting (callouts, wikilinks, embeds, frontmatter)
- `svg-precision-skill` — for generating SVG solution flowcharts
- `obsidian-cli` — for vault search and note operations

---

## Fixed Paths

| Item | Path (relative to vault root) |
|------|------|
| Notes root | `5.算法/力扣/` |
| Category directory | `5.算法/力扣/{分类名}/` |
| SVG storage | `图片/SVG/` |
| STL references | `5.算法/14. STL/` |
| Note template | `references/note-template.md` (in this skill) |
| Category & STL map | `references/category-map.md` (in this skill) |

---

## Core Rules

1. **File name**: `{题号}. {中文题名}.md` — use LeetCode official Chinese title.
2. **Location**: `5.算法/力扣/{分类名}/{题号}. {中文题名}.md` — one problem, one primary category.
3. **SVG naming**: `5_1_{题号}_{序号}.svg` — stored in `图片/SVG/`. The `5_1` prefix represents "5.算法/力扣", `{序号}` starts at 1.
4. **SVG background**: every SVG must include a solid background rectangle as its first child element: `<rect width="100%" height="100%" fill="rgb(245, 244, 237)"/>`.
5. **SVG embed syntax**: `![[5_1_{题号}_{序号}.svg|{width}]]` — typical width is 760.
6. **STL cross-references**: when solution code uses STL containers, algorithms, or utilities, add wikilinks to corresponding `14. STL/` files. See `references/category-map.md` for the keyword-to-file mapping.
7. **SVG required**: each note must include at least one SVG diagram showing the solving process, data structure state changes, or algorithm flow.
8. **Frontmatter**: must include `阅读次数: 0` and tags `[力扣, {分类名}]`. Add `aliases` for the English problem title.
9. **Language**: all note content in Chinese. Code identifiers, API names, and C++ keywords remain in English.
10. **Cross-references**: when referencing another problem already in the vault, use wikilink `[[{题号}. {中文题名}]]`. Do NOT link to notes that do not exist.
11. **Clean sections**: delete template sections that are not applicable. Never leave empty headings.
12. **Check before create**: always search the vault before creating a new note to avoid duplicates.

---

## Category System

Problems are categorized by their **primary algorithm technique** (the core method used in the optimal solution).

### Decision Framework

1. If the optimal solution primarily uses one technique, that is the category.
2. If multiple techniques apply equally, choose the one most instructive for learning.
3. If unsure, ask the user.
4. Create the category directory on first use — do not pre-create empty directories.

### Available Categories

See `references/category-map.md` for the full list of 20 categories with descriptions and example problem numbers:

滑动窗口 · 双指针 · 动态规划 · 链表 · 二叉树 · 回溯 · 贪心 · 堆与优先队列 · 图论 · 排序 · 栈与队列 · 哈希表 · 二分查找 · 设计题 · 前缀和 · 深度优先搜索 · 广度优先搜索 · 并查集 · 单调栈 · 字符串

---

## SVG Workflow

### When to Create SVGs

- Data structure state changes during the algorithm (pointer movements, heap operations, array modifications)
- Step-by-step solving process (sliding window expansion/contraction, DP table filling)
- Before/after comparisons
- Key state transition diagrams

### Generation Process

1. Determine what the SVG should illustrate (algorithm steps, data structure states, etc.)
2. Check existing SVGs: search for `5_1_{题号}_*.svg` in `图片/SVG/` to find the next available sequence number.
3. Delegate SVG construction to `svg-precision-skill`:
   - Specify viewBox dimensions (typical: 760×400 to 980×600)
   - Include background rectangle: `fill="rgb(245, 244, 237)"`
   - Use Chinese labels for all visible text
   - Use clear, readable fonts (16px+ for labels)
4. Save SVG to `图片/SVG/5_1_{题号}_{序号}.svg`
5. Embed in note: `![[5_1_{题号}_{序号}.svg|760]]`

---

## STL Wikilink Logic

1. After writing the solution code, scan it for STL keywords (types, function calls, `#include` headers).
2. Look up matches in `references/category-map.md` → STL Keyword-to-Wikilink Mapping table.
3. For each match, add one wikilink entry in the `相关链接` section:
   ```
   - [[14.x {文件名}]] — {简要说明该STL特性在本题中的用途}
   ```
4. At most one wikilink per STL reference file per note.
5. Only link when the STL feature is **used in code**, not just mentioned in prose.

---

## Workflow: Creating a New Note

### Step 1: Gather Information

Collect from the user:
- LeetCode problem number and Chinese title
- The solution code (C++)
- The primary algorithm category (or determine it from the solution)

### Step 2: Check for Duplicates

```
Use obsidian MCP simple_search to search for the problem number in the vault.
Also check: does 5.算法/力扣/{分类名}/{题号}. {中文题名}.md already exist?
```

### Step 3: Prepare Category Directory

- Check if `5.算法/力扣/{分类名}/` exists
- If not, create it (Obsidian will create the directory when the first note is added)

### Step 4: Build Note from Template

- Load `references/note-template.md`
- Fill in all `{placeholder}` values
- Write the algorithm introduction (or link to existing one)
- Write problem description in your own words
- Write solution approach with step-by-step explanation
- Include the full solution code with analysis
- List common mistakes
- Analyze time/space complexity

### Step 5: Generate SVGs

- Determine what diagrams best illustrate the solution
- Check existing SVG sequence: `find 图片/SVG/ -name "5_1_{题号}_*.svg"`
- Use `svg-precision-skill` to generate each SVG
- Embed SVGs at appropriate positions in the note

### Step 6: Add Cross-References

- **STL links**: scan code → map to `14. STL/` wikilinks (see STL Wikilink Logic)
- **Problem links**: check vault for related problems, add wikilinks
- **Category peers**: link to problems in the same category directory if relevant

### Step 7: Validate

Run through the validation checklist before finalizing.

---

## Workflow: Migrating Existing Notes

One-time migration of existing flat notes in `5.算法/力扣/` into category subdirectories.

### Migration Table

| Current File | Target Category | Reason |
|---|---|---|
| `3. 无重复字符的最长子串.md` | `滑动窗口/` | 核心方法是滑动窗口 |
| `15. 三数之和.md` | `双指针/` | 排序后使用双指针 |
| `25. K 个一组翻转链表.md` | `链表/` | 链表操作（分组翻转） |
| `146. LRU 缓存.md` | `设计题/` | 经典数据结构设计 |
| `206. 反转链表.md` | `链表/` | 基本链表翻转 |
| `215. 数组中的第K个最大元素.md` | `堆与优先队列/` | 堆/快速选择 |

### Migration Steps

1. Read each note's content from its current location.
2. Create the target category directory if it does not exist.
3. Write the note content to the new path: `5.算法/力扣/{分类名}/{题号}. {中文题名}.md`
4. Delete the original file from `5.算法/力扣/`.
5. Optionally add missing `tags` frontmatter to notes that lack them.

> [!note]
> Obsidian wikilinks resolve by **filename**, not by full path. Moving files into subdirectories does NOT break existing wikilinks. No link editing is required.

---

## Validation Checklist

Before delivering a note, verify:

- [ ] File name matches `{题号}. {中文题名}.md`
- [ ] File is located in `5.算法/力扣/{分类名}/`
- [ ] Frontmatter has `阅读次数: 0` and appropriate `tags` (includes `力扣` + category)
- [ ] No empty headings or unfilled template placeholders remain
- [ ] Code block uses `cpp` language tag
- [ ] At least one SVG diagram is embedded
- [ ] SVG files exist in `图片/SVG/` with correct naming `5_1_{题号}_{序号}.svg`
- [ ] SVGs include background rectangle with `fill="rgb(245, 244, 237)"`
- [ ] STL wikilinks in `相关链接` match actual code usage
- [ ] Cross-references to other vault problems are valid (target notes exist)
- [ ] All content is in Chinese; code identifiers are in English
