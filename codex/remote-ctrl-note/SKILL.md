---
name: remote-ctrl-note
description: Create, update, and cross-link Obsidian notes for the remote-control project at `D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl`. Use when Codex needs to sync Git/code changes into `D:\obsidian\C++\6.项目\远控系统`, analyze the MFC/Winsock/Win32 codebase into project notes, create or update numbered feature notes, or record bug-fix work as `Debug-XXX` notes. This skill also decides when to use `远控系统模版笔记.md` versus `远控系统Debug日志模版.md`, and how to produce an English-first draft followed by a polished technical-Chinese version.
---

# Remote Ctrl Note

Use this skill for the Windows remote-control project and its Obsidian notes. Read Git and changed code first, then map the result into the existing note structure without repeating material that already has a good note.

Default note-output workflow:

1. Read Git and changed code first.
2. Build the note structure and mechanism explanation in English first.
3. Then translate and rewrite that draft into natural, polished technical Chinese unless the user explicitly asks for an English final note.
4. Treat the Chinese version as the default final delivery.

This is a project workflow skill, not a full Obsidian-operation skill by itself. In note tasks, pair it conceptually with:

- `obsidian-markdown` when writing or restructuring Obsidian-flavored markdown, frontmatter, wikilinks, callouts, and note-friendly section layout
- `obsidian-cli` when the task benefits from fast vault search, path confirmation, note creation, bulk lookup, or checking whether an existing note/title/path already exists

In practice:

- Use `remote-ctrl-note` to decide what to write, where to write it, and how it should relate to project code/history
- Use `obsidian-markdown` thinking when shaping the final note format
- Use `obsidian-cli` style workflows when locating notes or validating names/links quickly

## Fixed Paths

- Project root: `D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl`
- Server code: `D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl\RemoteCtrl`
- Client code: `D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl\RemoteClient`
- Notes root: `D:\obsidian\C++\6.项目\远控系统`
- Debug notes: `D:\obsidian\C++\6.项目\远控系统\0. Debug日志`
- Main note template: `D:\obsidian\C++\模版\远控系统模版笔记.md`
- Debug note template: `D:\obsidian\C++\模版\远控系统Debug日志模版.md`

## Core Rules

1. Read Git history before reading large code files.
2. Read only changed files and relevant functions, not the whole project by default.
3. Reuse existing notes with `[[wiki-link]]` instead of repeating prior explanations.
4. Explain Win32 API, MFC behavior, Winsock flow, threading, and data flow, not just code.
5. Keep the numbered Chinese naming scheme used by the notes directory.
6. When the change is mainly a bug fix, create or update a `Debug-XXX` note and link it from the main feature note.
7. Use Codex shell commands and normal file reads; do not rely on Claude-only `Read` or `Glob` phrasing.
8. When the note involves architecture sequencing or cross-thread call flow, use diagrams instead of prose only.
9. Delete irrelevant template sections after inserting a template; never leave empty headings behind.
10. Prefer SVG or Mermaid over ASCII for mechanism diagrams. For static comparison, architecture, and block-layout diagrams, prefer SVG; for time-ordered interaction, request-response choreography, and thread timing, prefer Mermaid.
11. When a note introduces Win32 thread/message mechanics, include beginner-friendly API guidance: signatures only when useful, parameter/return meaning in project context, and comparisons such as `PostThreadMessage` vs `PostMessage` vs `SendMessage`, or `GetMessage` vs `PeekMessage`, when those differences matter to the design.
12. When a numbered note contains a concrete debug story, also create or update a matching note under `D:\obsidian\C++\6.项目\远控系统\0. Debug日志`, record the bug there in debug-log form, and add backlinks both ways between the main note and the debug note.
13. Prefer a teaching-oriented voice: direct, plain, and easy to follow. Do not write in a stiff or overly academic tone, and do not use strange metaphors or decorative analogies.
14. For chapter notes, explain the end-to-end chain first: what the request path is, where the response comes back, which thread or window finishes the job, and only then dive into traps or fixes.
15. When a commit contains both mechanism evolution and bug fixes, keep the main numbered note focused on the mechanism/storyline; move the detailed bug autopsy into bug notes or debug notes and link to them instead of dumping every bug detail into the main note.
16. Unless the user explicitly asks to keep the final note in English, always use an English-first drafting step followed by a polished technical-Chinese final version.
17. In the final Chinese note, translate visible labels inside Mermaid and visible text inside SVG as well; do not leave mixed-language diagrams unless the user explicitly wants that.

## Template Selection

Use the templates with this split:

- Use `D:\obsidian\C++\模版\远控系统模版笔记.md` for numbered feature notes, subsystem design notes, refactor notes, architecture notes, call-flow notes, and chapter-style notes such as `6.1`, `6.2`, `6.3`, or `6.4`.
- Use `D:\obsidian\C++\模版\远控系统Debug日志模版.md` for standalone debugging records where the core value is `现象 -> 调试过程 -> 根因 -> 修复 -> 验证`, especially `Debug-XXX` notes under `0. Debug日志`.
- If one change contains both feature evolution and a concrete bug fix, write both:
  - the main numbered note with `远控系统模版笔记.md`
  - the paired `Debug-XXX` note with `远控系统Debug日志模版.md`
  - backlinks between them

Choose the debug template when most of the note answers these questions:

- How was the bug triggered?
- How was it narrowed down?
- What exact root cause made it fail?
- What code changed to fix it?
- How was the fix verified?

Choose the main template when most of the note answers these questions:

- What feature or subsystem changed?
- Why was the design changed?
- How does the call chain or thread model work now?
- Which classes, messages, APIs, or packets are involved?
- What is the current project-stage conclusion?

## Workflow

### 1. Inspect Git first

Run these commands first:

```powershell
Set-Location "D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl"
git log --oneline -10
git log -1 --stat
git diff --name-only HEAD~1 HEAD -- "*.cpp" "*.h"
git diff HEAD~1 HEAD -- "*.cpp" "*.h"
```

Use the commit message and diff to answer:

- What new feature or behavior changed?
- Which files actually matter?
- Is this a bug fix, refactor, or new capability?

### 2. Read only the changed code

After the diff, open only the changed `.cpp` and `.h` files, then narrow to the relevant functions, classes, and call chain.

Prefer commands like:

```powershell
rg --line-number "关键函数名|类名|命令码" "D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl"
```

### 3. Check existing notes before writing

Search the current note set before creating anything new:

```powershell
rg --files "D:\obsidian\C++\6.项目\远控系统"
rg --line-number "关键字|函数名|类名|命令码" "D:\obsidian\C++\6.项目\远控系统"
```

Treat this step as the point where `obsidian-cli`-style help is especially useful:

- quickly confirm whether a note already exists
- verify the exact title/path before writing wikilinks
- locate nearby chapter notes, bug notes, templates, and summaries
- avoid creating duplicate note names that differ only slightly

Start with these anchor notes when the topic matches:

- `[[2.1 网络编程基本设计]]`
- `[[2.2 网络编程架构设计]]`
- `[[2.3 设计网络传输包协议]]`
- `[[2.4 获取磁盘分区信息]]`
- `[[3.1 锁机处理]]`
- `[[4.1 文件下载功能的实现]]`
- `[[4.4 远程桌面显示功能设计与数据接收发送]]`
- `[[4.8 鼠标远程控制（被控端）与 Bug 修复]]`

### 4. Decide the note target

Use this decision rule:

- New feature or new subsystem: create a new numbered note in the matching topic folder with the main note template.
- Existing feature extended or cleaned up: update the existing note and keep the main note template structure.
- Pure bug fix or debugging-heavy change: create or extend a `Debug-XXX` note with the debug note template, then add a short summary link in the main feature note if needed.
- Mixed feature and bug fix: keep feature design in the main note, move the debugging narrative into `Debug-XXX`.

### 5. Write the note

For the main note template, keep the sections that match the topic and delete the rest. The usual high-value sections are:

- Summary paragraph under the title
- `功能概述` or `本次提交推进了什么`
- `设计背景` or `与前一版的关系`
- `架构设计` or `重构思想`
- `核心实现`
- `线程交互与流程`
- `当前版本的准确结论`
- `Win32 / Winsock / MFC 关键机制`
- `易错点与调试`
- `关联知识`
- `代码索引`
- `更新记录`

For the debug template, keep the investigation narrative tight:

- `Bug 基本信息`
- `现象描述`
- `调试过程`
- `根因分析`
- `修复前 / 修复后`
- `验证结果`
- `调试经验`

For each important function or behavior, include:

- What the function does in the overall workflow
- Why it is designed that way
- Which APIs or framework mechanisms it depends on
- What the key parameters or flags mean
- What can go wrong and how to spot it

When a note is meant for teaching, favor this structure:

- First tell the reader what changed in one or two short paragraphs.
- Then explain the whole path from request to response in simple terms.
- Then zoom into the key functions and APIs.
- Then point the reader to dedicated bug notes for the detailed traps and debugging process.

If the repository already has a chapter-local `Bug目录`, use it for local deep dives, while still keeping the global `0. Debug日志` entry when the bug deserves project-level indexing.

For readability, prefer this teaching order when the topic is complex:

1. Give a one-paragraph conclusion first.
2. Show the old vs new mechanism contrast visually, preferring SVG for static side-by-side layouts.
3. Explain the end-to-end chain in plain language before deep code analysis.
4. Explain the real call chain in code.
5. End with API semantics, pitfalls, and current-version conclusions.

When comparing two mechanisms, do not jump straight into code. First add a dedicated comparison block that makes these answers obvious at a glance:

- Who initiates the request
- Which thread blocks or does not block
- How the response is routed back
- Where ownership or lifetime changes
- What the new model fixes and what it still leaves unfinished

When showing code, prefer actual project code with line-accurate explanation. Do not paste a long code block without commentary.

When the topic includes architecture design timing, request/response choreography, or multi-thread call relationships, add diagrams with this priority:

- Use Mermaid `sequenceDiagram` for request/response flow, timing order, startup/shutdown order, and cross-thread callback order.
- Use Mermaid `flowchart` only when the main value is dynamic branching or handoff timing that would be awkward in SVG.
- Use SVG for static comparison diagrams, architecture layering, component grouping, fixed-layout mechanism summaries, and side-by-side old/new designs.
- When contrasting old and new mechanisms, prefer side-by-side SVG unless timing order is the real teaching focus; make blocking points, wake-up points, and response-delivery points explicit.
- Keep node names aligned with real class, thread, socket, and function names from the project.

### 6. Maintain links and indices

When you create or update a note:

- Add `[[wiki-link]]` references to prior notes that already explain shared concepts.
- Keep links accurate to existing note names.
- Update the surrounding summary note when the new note changes the local chapter structure.
- Keep debug notes under `0. Debug日志`.
- If a bug or debugging narrative appears in a main numbered note, add or update the dedicated `Debug-XXX` note in `0. Debug日志` and maintain double links:
  - main note -> `[[Debug-XXX ...]]`
  - debug note -> `[[对应主笔记]]`

### 7. Validate before finishing

Check all of the following:

- File name matches the numbered Chinese style already used nearby.
- The note lives in the correct chapter folder.
- Code references match real files and functions.
- The note explains design intent, not only surface syntax.
- Repeated concepts are linked, not copied.
- Empty template sections were removed.
- If the change fixed a bug, the corresponding `Debug-XXX` note and backlinks are present.

## Bug-Fix Handling

Treat a change as a bug fix when either the commit message or the diff strongly suggests it:

- Keywords such as `fix`, `bug`, `debug`, `修复`, `崩溃`
- Boundary changes such as `>` to `>=`
- Type corrections such as `int` to `intptr_t`
- Resource release additions such as `delete[]`, `CloseHandle`, `closesocket`
- Null checks, lifetime fixes, thread-exit fixes, or UI state fixes

When that happens:

1. Find the current max `Debug-XXX` note under `0. Debug日志`.
2. Create the next numbered debug note from `D:\obsidian\C++\模版\远控系统Debug日志模版.md` if the issue is new.
3. Record the symptom, root cause, wrong code, fixed code, and verification result.
4. Update `Debug 经验汇总与方法论.md` when the issue adds a reusable failure pattern.
5. Add double links between the main feature note and the debug note.

## Writing Standard

Always explain these dimensions when they matter:

- Win32 API semantics such as window z-order, cursor clipping, handles, or message dispatch
- MFC dialog or control lifecycle
- Winsock socket lifecycle and packet flow
- Thread ownership, blocking points, and cross-thread UI/message behavior
- Data packet structure and command handling

For notes aimed at learners, strengthen readability with:

- Short lead paragraphs that state the conclusion before the deep dive
- Comparison tables for old/new behavior, not just prose
- SVG for static mechanism and comparison diagrams, Mermaid for timing and interaction order, and never ASCII when a real diagram would teach better
- API mini-guides that explain not just what an API is, but why this project chose it over nearby alternatives
- Parameter and return-value tables only for APIs that are central to understanding the change
- Main notes that read like a walkthrough of one chain or one design decision, not like a changelog dump
- Bug details split into separate bug notes when that makes the main note easier to read
- Plain wording; avoid dense jargon unless it is immediately explained
- Avoid fancy metaphors, storytelling flourishes, or language that makes the explanation feel theatrical

## Language and Diagram Delivery

Unless the user explicitly overrides it, follow this output rule:

- First build the note in English.
- Then translate and rewrite it into natural technical Chinese.
- Treat the Chinese version as the final note by default.
- Keep code, API names, class names, function names, packet names, and exact file paths in their source language where precision matters.

Diagram rule of thumb:

- Static block comparison, architecture layering, component grouping, old-vs-new snapshots: use SVG.
- Request-response order, startup/shutdown timing, cross-thread callback order, and other sequence-heavy explanations: use Mermaid.
- Translate chart labels too:
  - Mermaid node text, edge labels, and note text should be Chinese in the final Chinese note.
  - Visible SVG text should also be Chinese in the final Chinese note.

Reject these failure modes:

- Dumping code without explanation
- Re-explaining `CPacket` or networking basics when a solid existing note already covers them
- Creating loosely related `相关笔记` sections with no real dependency
- Creating empty notes only to make links

## Quick Reference

Use these project facts directly:

- Architecture: C/S, `RemoteCtrl` server plus `RemoteClient` client
- Main technologies: MFC, Winsock, Win32 API
- Core files:
  - `ServerSocket.h`
  - `ServerSocket.cpp`
  - `RemoteCtrl.cpp`
  - `RemoteClientDlg.cpp`

Use this skill as a project-specific note-maintenance workflow, not as a generic markdown editor.
