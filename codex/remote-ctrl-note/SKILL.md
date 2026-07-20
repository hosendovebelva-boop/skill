---
name: remote-ctrl-note
description: |
  远控系统项目专用笔记管理 Skill。当用户需要以下操作时使用此 Skill：
  - 为远控项目写笔记、更新笔记
  - 同步项目代码变化到笔记
  - 分析远控系统代码并生成文档
  触发词：远控笔记、远控系统笔记、更新远控笔记、同步远控、远控项目、远控系统
---

# Remote-Ctrl-Note - 远控系统项目笔记管理

## 模版选择（重要！首先判断）

写笔记前**必须先判断**应该使用哪个模版：

| 判断条件 | 使用模版 | 模版路径 |
|---------|---------|---------|
| 记录某次 commit 的功能实现、架构重构、模块设计 | **远控系统模版笔记** | `模版/远控系统模版笔记.md` |
| 记录运行时发现的 Bug 及其调试修复过程 | **远控系统Debug日志模版** | `模版/远控系统Debug日志模版.md` |

### 详细判断逻辑

**使用「远控系统模版笔记」的场景**：
- 用户说"写笔记"、"记录这次提交"、"分析这段代码"
- 内容是：新功能实现、架构演进、模块重构、代码讲解
- 笔记存放于：`6.项目/远控系统/X. 章节目录/` 下
- 命名格式：`X.X 功能名称.md`
- 例：`6.4 网络模型线程完善(3).md`、`2.8 屏幕截屏与发送.md`

**使用「远控系统Debug日志模版」的场景**：
- 用户说"记录这个 Bug"、"写 Debug 日志"、"这个问题怎么解决的"
- 内容是：Bug 现象 → 调试过程 → 根因分析 → 修复方案
- 笔记存放于：`6.项目/远控系统/0. Debug日志/` 下
- 命名格式：`Debug-XXX 问题简述.md`（编号从 Debug 经验汇总索引中查下一个可用编号）
- 例：`Debug-013 显示命令与鼠标命令冲突导致程序卡死.md`
- **写完后必须同步更新** `Debug 经验汇总与方法论.md` 的索引表和分类统计

**一次 commit 可能同时产生两种笔记**：
- 版本笔记记录"做了什么改动、为什么这样设计"
- Debug 日志记录"遇到了什么 Bug、怎么排查的、怎么修的"
- 两者通过 `[[wiki-link]]` 互相引用

---

## 核心原则

1. **Git 驱动**：通过 git diff/log 精准定位新增代码，避免重复分析
2. **代码必须详解**：关键代码必须有详细注释 + 设计思路讲解
3. **技术栈讲清楚**：每个功能涉及的 Win32 API、MFC 机制都要解释
4. **不重复已讲内容**：已讲解过的代码用 `[[wiki-link]]` 引用
5. **新增代码功能**：分享新的类、新的函数有什么新的功能、函数间的调用关系

---

## 与 note-creator 的协作

本 Skill **复用 `note-creator` 的核心规范**：

| 复用内容 | 说明 |
|---------|------|
| 代码讲解规范 | 每段代码必须有配套讲解，禁止只堆砌代码 |
| 笔记结构模板 | 设计背景 → 架构设计 → 核心实现 → 易错点 |
| Modern C++ 风格 | 代码示例遵循现代 C++ 写作规范 |
| 关联链接规范 | 合理使用 wiki-link，不过度链接 |

**差异点**：
- `note-creator`：创建通用 C++ 技术笔记
- `remote-ctrl-note`：专注于远控项目，整合 git 变更、项目代码路径

---

## 项目信息

| 项目 | 说明 |
|------|------|
| **项目路径** | `D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl` |
| **笔记路径** | `D:\obsidian\C++\6.项目\远控系统\` |
| **架构** | C/S 架构，被控端 (RemoteCtrl) + 控制端 (RemoteClient) |
| **技术栈** | MFC, Winsock, Win32 API |

### 项目结构

```
RemoteCtrl/
├── RemoteCtrl/           # 被控端 (Server)
│   ├── ServerSocket.h    # 网络核心：CServerSocket, CPacket
│   ├── ServerSocket.cpp  # 网络实现
│   ├── RemoteCtrl.cpp    # 主程序入口
│   └── ...
├── RemoteClient/         # 控制端 (Client)
│   ├── RemoteClientDlg.h # MFC 对话框
│   └── ...
└── RemoteCtrl.sln        # VS 解决方案
```

---

## 执行流程（重要）

### 第一步：读取 Git 提交信息

**必须先执行** Git 命令，了解用户最近做了什么修改：

```bash
# 1. 查看最近提交记录
cd "D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl"
git log --oneline -10

# 2. 查看最近一次提交的详细信息（文件变更统计）
git log -1 --stat

# 3. 查看具体代码变更（关键！）
git diff HEAD~1 HEAD -- "*.cpp" "*.h"
# 或指定两个 commit：
git diff <旧commit> <新commit> -- "*.cpp" "*.h"
```

**Git 信息用途**：
- 精准定位**新增代码**，只分析变化部分
- 了解用户的**开发意图**（从 commit message）
- **节省 token**，不用完整读取所有文件

### 第二步：读取新增/修改的代码文件

根据 git diff 结果，**只读取有变化的文件**：

```bash
# 示例：git diff 显示 RemoteCtrl.cpp 有变化
Read RemoteCtrl/RemoteCtrl/RemoteCtrl.cpp
```

### 第三步：检查已有笔记

使用 Glob 搜索已有笔记，确定哪些代码已经讲解过：

```bash
# 搜索远控系统笔记
Glob "D:\obsidian\C++\6.项目\远控系统\**\*.md"
```

**决策逻辑**：
| 情况 | 处理方式 |
|------|---------|
| 新代码/新功能 | 完整展示 + 详细注释讲解 |
| 已讲解过的代码 | 用 `[[wiki-link]]` 引用之前笔记 |
| 修改已有代码 | 说明修改点，对比新旧实现 |

### 第四步：按模板生成笔记

根据「模版选择」章节的判断结果，读取对应的 Obsidian 模版文件：
- 版本笔记：`Read "D:\obsidian\C++\模版\远控系统模版笔记.md"`
- Debug 日志：`Read "D:\obsidian\C++\模版\远控系统Debug日志模版.md"`

按模版结构填充内容，删除不相关的章节（模版中有 HTML 注释说明）。

---

## 代码讲解规范（核心！）

### 必须讲清楚的内容

对于每个功能/函数，必须包含：

| 内容 | 说明 | 示例 |
|------|------|------|
| **技术栈** | 用到了什么 API/技术 | Win32 API: SetWindowPos, ClipCursor |
| **设计思路** | 为什么这样设计 | 使用线程是为了不阻塞主线程 |
| **关键点** | 代码中的关键行 | `wndTopMost` 使窗口永远置顶 |
| **参数说明** | API 参数含义 | `SWP_NOSIZE | SWP_NOMOVE` 只改变 Z 序 |
| **易错点** | 容易出错的地方 | ShowCursor 使用引用计数 |

### 代码展示格式

**完整展示 + 详细注释**：

```markdown
### threadLockDlg 线程函数

这是锁机功能的**核心实现**。设计思路：在独立线程中创建全屏窗口，避免阻塞主线程的网络通信。

**技术栈**：
- `_beginthreadex`：C 运行时库线程创建
- `SetWindowPos`：设置窗口 Z 序（置顶）
- `ClipCursor`：限制鼠标活动范围
- `FindWindow`：根据类名查找窗口
- `PostThreadMessage`：跨线程消息传递

```cpp
unsigned __stdcall threadLockDlg(void* arg)
{
    // ===== 1. 创建并显示对话框 =====
    // Create: 创建非模态对话框，不阻塞当前线程
    dlg.Create(IDD_DIALOG_INFO, NULL);
    dlg.ShowWindow(SW_SHOW);

    // ===== 2. 设置全屏尺寸 =====
    CRect rect;
    rect.left = 0;
    rect.top = 0;
    // GetSystemMetrics: 获取系统度量值
    // SM_CXFULLSCREEN: 全屏窗口客户区宽度（不含任务栏）
    rect.right = GetSystemMetrics(SM_CXFULLSCREEN);
    rect.bottom = GetSystemMetrics(SM_CYFULLSCREEN);
    rect.bottom *= 1.05;  // 乘以 1.05 确保覆盖任务栏区域
    dlg.MoveWindow(rect);

    // ===== 3. 窗口置顶 =====
    // wndTopMost: 窗口置于所有非置顶窗口之上
    // SWP_NOSIZE | SWP_NOMOVE: 不改变大小和位置，只改变 Z 序
    dlg.SetWindowPos(&dlg.wndTopMost, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE);

    // ... 后续代码
}
```

**关键点解析**：

1. **线程函数签名**
   - `unsigned __stdcall` 是 `_beginthreadex` 要求的调用约定
   - 返回值 `unsigned`，参数 `void*`

2. **全屏计算**
   - `SM_CYFULLSCREEN` 不含任务栏高度，乘以 1.05 确保覆盖
```

### 禁止的做法

```markdown
❌ 错误：只贴代码，不讲解

```cpp
unsigned __stdcall threadLockDlg(void* arg)
{
    dlg.Create(IDD_DIALOG_INFO, NULL);
    dlg.ShowWindow(SW_SHOW);
    // ... 100 行代码
}
```

❌ 错误：讲解太简略

这个函数创建了一个对话框。
```

---

## 引用格式

| 引用类型 | 格式 | 使用场景 |
|---------|------|---------|
| **笔记引用** | `[[笔记名#章节]]` | 引用已讲解过的概念/代码 |
| **项目文件引用** | `> 📁 \`文件路径\` : 函数名 (行 XX-XX)` | 指向项目代码位置 |
| **简短提示** | `> 📎 详见 [[笔记名]]` | 简短的交叉引用 |

---

## 笔记模板

笔记模板已外置为 Obsidian 模版文件，写笔记时直接读取对应模版：

| 模版 | 路径 | 适用场景 |
|------|------|---------|
| **版本笔记模版** | `模版/远控系统模版笔记.md` | 功能实现、架构重构、模块设计 |
| **Debug 日志模版** | `模版/远控系统Debug日志模版.md` | Bug 调试与修复记录 |

使用方法：`Read "D:\obsidian\C++\模版\远控系统模版笔记.md"` 或 `Read "D:\obsidian\C++\模版\远控系统Debug日志模版.md"`，按模版结构填充内容，删除不相关的章节。

---

## 已有笔记索引

写新笔记前，先检查这些已有笔记，避免重复讲解：

| 笔记 | 已讲解的内容 |
|------|-------------|
| [[2.1 网络编程基本设计]] | Winsock 初始化、socket/bind/listen/accept |
| [[2.2 网络编程架构设计]] | CServerSocket 单例模式、CHelper 自动释放 |
| [[2.3 设计网络传输包协议]] | CPacket 完整实现、协议格式、粘包处理、校验和 |
| [[2.4 获取磁盘分区信息]] | GetLogicalDriveStrings、命令处理框架 |
| [[3.1 锁机处理]] | threadLockDlg、LockMachine、UnlockMachine、Win32 锁机 API |

**使用方式**：如果新笔记需要用到 CPacket，不要重复贴代码，而是：
```markdown
数据包解析使用 [[2.3 设计网络传输包协议]] 中定义的 CPacket 类。
```

---

## Git 命令速查

```bash
# 进入项目目录
cd "D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl"

# 查看最近提交
git log --oneline -10

# 查看最近提交的文件变更
git log -1 --stat

# 查看具体代码差异（最近一次提交）
git diff HEAD~1 HEAD -- "*.cpp" "*.h"

# 查看两个提交之间的差异
git diff <commit1> <commit2> -- "*.cpp" "*.h"

# 查看某次提交的完整内容
git show <commit> -- "*.cpp" "*.h"
```

---

## 质量检查清单

创建笔记前，确保：

- [ ] **读取了 git diff**，了解本次代码变更
- [ ] **精准定位新增代码**，不重复分析旧代码
- [ ] **技术栈讲清楚**：涉及的 API、MFC 机制都有解释
- [ ] **设计思路讲清楚**：为什么这样实现
- [ ] **关键点都有注释**：代码中重要的行都有说明
- [ ] **参数含义讲清楚**：API 参数不能一笔带过
- [ ] **易错点有警示**：常见错误和正确做法
- [ ] **合理使用引用**：已讲解内容用 wiki-link 引用
- [ ] **代码索引准确**：文件路径和行号对应实际代码
- [ ] **添加远控系统tags**：添加 项目/远控系统 的tags

---

## 注意事项

1. **先读 Git，再读代码**：精准定位变化，节省 token
2. **新代码必须详细讲解**：技术栈、设计思路、关键点缺一不可
3. **不重复已讲解的代码**：用 `[[wiki-link]]` 引用
4. **保持引用准确**：引用时确保笔记名和章节标题正确
5. **代码要可运行**：展示的代码应该是项目中实际的代码
6. **同步更新已有笔记索引**：新增笔记后更新本 Skill 的索引表
7. **清晰的函数调用流程图**：在解释功能的时候体现函数的调用链和数据的传输链
8. **图表使用规范**：
   - **时序图（多方交互）**：使用 Mermaid `sequenceDiagram`，适合展示 C/S 通信、消息传递顺序
   - **流程图/结构图（单一流程）**：使用 ASCII 图，适合展示函数调用链、目录结构、简单分支
   - **复杂流程图/架构图**：使用 SVG 矢量图，放在 `D:\obsidian\C++\图片\` 目录下，笔记中使用相对路径引用：`![图名](../../图片/文件名.svg)`
   - **SVG 箭头样式**：默认使用小号空心箭头，`markerWidth/markerHeight` 约 6-7，`path` 使用 `fill="none"` + `stroke`，不要使用大号实心三角箭头


---

## 快速参考

### 项目路径
- 被控端：`D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl\RemoteCtrl\`
- 控制端：`D:\c++\project\remote_ctl\remote_ctl\RemoteCtrl\RemoteClient\`

### 笔记路径
- 笔记目录：`D:\obsidian\C++\6.项目\远控系统\`

### 核心文件
| 文件 | 内容 |
|------|------|
| ServerSocket.h | CServerSocket, CPacket 定义 |
| ServerSocket.cpp | 网络实现 |
| RemoteCtrl.cpp | 被控端主程序 |
| RemoteClientDlg.cpp | 控制端 UI 逻辑 |
