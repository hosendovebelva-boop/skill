# cpp-tutor 权威来源路由

本文件用于回答“这个结论依据什么”。先判断论断层级，再选来源；学生笔记用于了解学习上下文，不替代规范或官方文档。

Vault 根目录：`<OBSIDIAN_VAULT>`

## 一、来源层级

### 1. 规范保证

用于回答“标准是否保证”“是不是未定义行为”“协议必须怎样处理”。

- C++：ISO C++ 正式标准或与目标版本对应的 working draft。
- C/POSIX：ISO C 标准、The Open Group POSIX 规范。
- Linux：Linux man-pages、Linux kernel documentation；注意它们描述 Linux，不自动代表所有 Unix。
- 网络协议：RFC Editor 发布的当前 RFC；先确认旧 RFC 是否已被更新或废止。

### 2. 实现行为

用于回答“GCC/Clang/MSVC/Linux/glibc 在这台平台上怎么做”。

- 编译器与标准库：GCC、Clang/LLVM、MSVC、libstdc++、libc++ 官方文档。
- ABI 与对象布局：目标平台 ABI 文档、编译器文档、必要时配合反汇编或小实验。
- Linux 内核行为：man-pages、内核文档、目标内核源码与可复现实验。

实现观察必须写明平台、编译器/库或版本，不能上升为跨平台标准结论。

### 3. 教材解释与工程建议

教材适合建立模型、解释机制和提供实践建议，但不能替代规范条文。Effective 系列的 Item 是建议；CSAPP、TLPI、Stevens 等书中的实现说明也要注意版本与平台边界。

## 二、按主题选择来源

| 问题类型 | 第一来源 | 解释性来源 |
|---|---|---|
| 值类别、对象生命周期、重载决议、模板规则、UB | 对应版本 C++ 标准/working draft | 《C++ Primer》《Effective Modern C++》 |
| 智能指针、RAII、接口设计、Modern C++ 实践 | 标准库规范与实现文档 | 《Effective Modern C++》《Effective C++》 |
| STL 容器、算法、迭代器失效规则 | 标准库条款、实现文档 | 《C++ Primer》《Effective STL》 |
| 原子、内存序、happens-before、数据竞争 | C++ 并发与内存模型条款 | 《C++ Primer》《Effective Modern C++》；底层联系可参考 CSAPP |
| POSIX 线程、进程、信号、文件与 IPC | POSIX + 对应 man page | *The Linux Programming Interface*、*Modern Operating Systems* |
| Linux 专属 API：`epoll`、`io_uring`、`eventfd` 等 | Linux man-pages、内核文档 | TLPI、*Linux 多线程服务端编程*、*Systems Performance* |
| socket API 与阻塞/非阻塞 I/O | POSIX / Linux man-pages | *UNIX Network Programming, Vol. 1*、TLPI |
| TCP/IP、HTTP、DNS、TLS 等线上协议 | 当前 RFC / 协议官方规范 | *TCP/IP Illustrated, Vol. 1*、网络教材 |
| vtable、对象布局、name mangling、调用约定 | 目标 ABI 与编译器文档 | CSAPP、体系结构教材；明确“常见实现” |
| Cache、NUMA、内存层次、性能分析 | 硬件/内核/工具官方文档 | *Computer Architecture: A Quantitative Approach*、*Systems Performance* |

## 三、本地资料

本地书籍位于：

```text
<OBSIDIAN_VAULT>/图片/书籍/
```

使用前先按文件名搜索，不要依赖过期清单：

```bash
find '<OBSIDIAN_VAULT>/图片/书籍' -maxdepth 1 -type f -iname '*关键词*'
```

当前已核对存在的主要资料：

| 领域 | 本地文件名模式 |
|---|---|
| C++ 基础与语言 | `C++ Primer*.pdf`、`C++ Primer Plus*.pdf` |
| C++ 工程实践 | `Effective C++.pdf`、`Effective Modern C++.pdf`、`Effective STL*.pdf` |
| 系统与操作系统 | `Computer Systems A Programmers Perspective*.pdf`、`Modern Operating Systems.pdf` |
| Linux/POSIX | `The Linux programming interface*.pdf`、`Linux多线程服务端编程*.pdf` |
| 网络 | `UNIX Network Programming*.pdf`、`TCPIP Illustrated*.pdf`、`Computer Networking*.pdf`、`Computer Networks*.pdf` |
| 体系结构与性能 | `Computer Architecture A Quantitative Approach*.pdf`、`Systems Performance*.pdf` |

本地 PDF 的存在只说明可以核对原文，不代表内容比更新后的规范优先。

## 四、何时必须核验

遇到以下情况，输出前必须核验规范、官方文档或本地原文：

- 使用“必须”“保证”“永远”“未定义行为”“未指定”“实现定义”等强语气。
- 给出精确的标准条款、书籍 Item、章节、页码或直接引语。
- 讨论原子与内存序、对象生命周期、严格别名、ODR、异常保证等易误判规则。
- 讨论系统调用返回值、`errno`、信号安全、阻塞条件、继承/共享语义。
- 讨论协议字段、状态机、超时、重传、版本兼容或已更新的 RFC。
- 把反汇编、某个编译器结果或 Linux 行为推广到其他平台。

## 五、引用写法

优先概括，不堆砌书目：

```markdown
### 权威依据
- **规范保证**：C++ working draft `[已核验条款]` —— [概括结论]
- **实现行为**：Linux `epoll(7)` —— [Linux 上的具体语义]
- **教材解释**：《Effective Modern C++》Item 23 —— [该 Item 帮助理解的实践含义]
- **适用边界**：[标准保证 / Linux 专属 / 某编译器实现 / 工程建议]
```

规则：

1. 没核对精确位置，就不要写条款号、Item、页码。
2. 不凭记忆生成直接引语；无法读取原文时用自己的话概括。
3. 简单问题保留 1 个最相关来源即可；只有来源之间存在分工时才并列。
4. 教材与规范冲突时，以适用版本的规范和官方文档为准，并说明教材的版本背景。
5. 学生笔记有误时，指出“笔记原文—修正—依据—适用边界”，不要只说结论。
