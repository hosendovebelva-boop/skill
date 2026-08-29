# Vault 参考数据

Vault 根：`~/Documents/C++/obsidian_notes-main`

> 下面的目录表是 2026-07-26 从磁盘实测的快照。目录会变，**用之前先 `ls` 核对**。

---

## 一、目录映射

### C++ / 系统编程

| 主题 | 目录 |
|---|---|
| C++ 基础语法、类型、指针、结构体 | `1.C++基础/` 下对应章节 |
| 智能指针、RAII | `1.C++基础/6. 指针/` |
| OOP、继承、多态 | `1.C++基础/12. OOP/` |
| 左值右值、移动语义 | `1.C++基础/13. 左值与右值/` |
| 模板、STL、C++11/14/17/20 | `2.C++高级/` |
| Linux 系统编程、网络编程 | `3.Linux/` |
| Windows 编程 | `4.windows/` |

### 算法

| 内容 | 目录 |
|---|---|
| STL 笔记 | `5.算法/5.1 STL/` |
| 算法知识点 | `5.算法/5.2 算法/5.2.N 章节名/` |
| 力扣题解 | `5.算法/5.3 力扣/5.3.N 分类名/` |

`5.3` 的子目录编号与名称对齐 `5.2`（`5.2.19 动态规划` → `5.3.19 动态规划`）。

**注意 `5.3 力扣/` 是混合状态**：既有 `5.3.N 名称` 标准目录，也有历史遗留的纯中文目录（`排序/`、`字符串/`、`动态规划/`、`深度优先搜索/`、`广度优先搜索/`、`并查集/`、`拓扑排序/`、`最短路径/`），还有若干散落在根目录的 `.md`。新建时用标准目录；整理旧笔记时注意这三种形态并存。

### 其他方向

| 领域 | 目录 | 备注 |
|---|---|---|
| 项目笔记 | `6.项目/` | 含 `03.远控系统/`、`06.远控服务端/` |
| LLM 应用 | `7.LLM应用/N. 主题/` | 先读 `7.LLM应用/培养方案.md` |
| 数值分析 | `7.LLM应用/5.数值分析/`、`7.LLM应用/6.数值分析笔记/` | 归 `numerical-analysis` skill 管 |
| 高性能存储 | `8.高性能存储/` | |
| 投资 | `12.投资/N. 日期区间/` | 先读 `12.投资/培养方案.md` |
| 模板文件 | `模版/` | `算法笔记模版.md` 等 |
| 图片 / SVG | `图片/`、`图片/SVG/` | |

---

## 二、权威来源

写之前在脑内检索对应来源，引用时写清书名和条款号。

### C++ / 系统编程

| 书 | 覆盖 | 本地资源（以磁盘实际文件为准） |
|---|---|---|
| 《C++ Primer》 | 系统学习现代 C++ 语言、标准库与惯用写法 | `图片/书籍/C++ Primer (Stanley*.pdf` |
| 《C++ Primer Plus》 | 入门补充、语法和基础编程练习 | `图片/书籍/C++ Primer Plus*.pdf` |
| 《Effective C++》 | 经典 C++、OOP、资源管理 | `图片/书籍/Effective C++.pdf` |
| 《Effective Modern C++》 | C++11/14、智能指针、移动语义、并发 | `图片/书籍/Effective Modern C++.pdf` |
| 《Effective STL》 | 容器、算法、迭代器 | 本地暂未发现 |
| 《Linux 多线程服务端编程》 | 网络编程、并发、Reactor | 本地暂未发现 |
| 《CSAPP》 | 底层原理、内存、链接 | 本地暂未发现 |
| 《Modern Operating Systems》 | 进程、线程、内存、文件系统、I/O 与操作系统设计 | `图片/书籍/Modern Operating Systems.pdf` |

### 高性能系统 / AI Infra

> AI Infra 的资料分两层：教材负责解释相对稳定的原理；项目、厂商和标准组织的官方文档负责确认当前接口、版本边界和硬件限制。写笔记时两者要分开引用，不能用教材的旧描述替代最新规范。

#### 核心教材（以本地可用版本为准）

| 书 | 适合解决的问题 | 官方资料 | 本地资源（以磁盘实际文件为准） |
|---|---|---|---|
| *Systems Performance: Enterprise and the Cloud*, 2nd ed. — Brendan Gregg | CPU、内存、文件系统、磁盘、网络、性能方法论、`perf`/BPF/Benchmark | [作者官网](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) | `图片/书籍/Systems Performance*.pdf` |
| *Computer Architecture: A Quantitative Approach*, 6th ed. — Hennessy & Patterson | Cache、内存层次、NUMA、PCIe、加速器、仓库级计算 | [Elsevier](https://www.educate.elsevier.com/book/details/9780128119051) | `图片/书籍/Computer Architecture A Quantitative Approach*.pdf` |
| *The Linux Programming Interface* — Michael Kerrisk | Linux I/O、`mmap`、进程、线程、`epoll`、系统调用语义 | [作者官网](https://michaelkerrisk.com/tlpi/index.html) | `图片/书籍/The Linux programming interface*.pdf` |
| *Computer Networking: A Top-Down Approach*, 9th ed. — Kurose & Ross | 网络基础、传输层、HTTP/3、QUIC、5G | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/computer-networking-a-top-down-approach/P200000013385) | `图片/书籍/Computer Networking A Top-Down Approach.pdf`（本地文件为旧版） |
| *Computer Networks*, 6th ed. — Tanenbaum, Feamster & Wetherall | 从硬件、链路层到应用层的完整网络体系 | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/computer-networks/P200000003188/9780137523214) | `图片/书籍/Computer Networks, Global Edition*.pdf` |
| *TCP/IP Illustrated, Volume 1: The Protocols*, 2nd ed. — Stevens & Fall | TCP/IP 协议行为、抓包分析、重传、拥塞控制 | [Pearson](https://www.pearson.com/en-us/subject-catalog/p/tcp-ip-illustrated-volume-1-the-protocols/P200000000242) | `图片/书籍/TCPIP Illustrated Vol. 1*.pdf` |
| *TCP/IP Illustrated, Volume 2: The Implementation* — Stevens & Wright | 4.4BSD-Lite TCP/IP 协议栈实现、socket 层、内核数据结构与源码 | [InformIT](https://www.informit.com/store/tcp-ip-illustrated-volume-2-paperback-the-implementation-9780134760131) | `图片/书籍/TCPIP illustrated. Volume 2*.pdf` |
| *TCP/IP Illustrated, Volume 3* — Stevens | T/TCP、HTTP、NNTP、UNIX 域协议；适合作为协议演进与实现史参考 | [InformIT](https://www.informit.com/store/tcp-ip-illustrated-volume-3-tcp-for-transactions-http-9780134457109) | `图片/书籍/TCPIP Illustrated, Volume 3*.pdf` |
| *UNIX Network Programming, Volume 1*, 3rd ed. — Stevens et al. | POSIX socket、阻塞/非阻塞 I/O、并发服务器 | [InformIT](https://www.informit.com/store/unix-network-programming-volume-1-the-sockets-networking-9780131411555) | `图片/书籍/UNIX Network Programming, Volume 1*.pdf` |
| *High Performance Computing: Modern Systems and Practices*, 2nd ed. | 集群、并行计算、GPU 加速、性能监控、存储与文件系统 | [Elsevier](https://shop.elsevier.com/books/high-performance-computing/sterling/978-0-12-823035-0) | 本地暂未发现 |
| 《数据存储架构与技术（第2版）》— 舒继武 | 存储设备、RAID、文件系统、网络存储、分布式存储、一致性、可靠性与数据保护 | — | `图片/书籍/数据存储架构与技术 (第2版)*.epub` |
| 《深入浅出SSD：固态存储核心技术、原理与实战》 | NAND、FTL、垃圾回收、写放大、ECC、PCIe/NVMe、SSD 测试与电源管理 | — | `图片/书籍/深入浅出SSD*.epub` |

> 本地没有发现 *Designing Data-Intensive Applications* 的中文直译版；《数据存储架构与技术（第2版）》覆盖分布式存储、一致性、可靠性等相近主题，作为中文对应教材使用，但不要把它描述成 DDIA 的翻译本。

#### 高性能网络与存储的活文档

| 资料 | 用途 |
|---|---|
| [DPDK Programmer's Guide](https://doc.dpdk.org/guides/) | 用户态网络、轮询、mbuf、队列和内存池 |
| [RDMA-Aware Networks Programming Guide](https://networking-docs.nvidia.com/doca/archive/3-4-0/rdma-aware-networks-programming-guide) | Verbs、QP、CQ、MR、RoCE/InfiniBand |
| [NVIDIA NCCL Documentation](https://docs.nvidia.com/deeplearning/nccl/) | 多 GPU / 多节点 collective communication、拓扑感知 |
| [GPUDirect RDMA](https://docs.nvidia.com/cuda/gpudirect-rdma/) | NIC 直接访问 GPU 内存，理解 GPU 网络数据路径 |
| [GPUDirect Storage](https://docs.nvidia.com/gpudirect-storage/) | 存储到 GPU 的直接 DMA、cuFile/cuObject、兼容模式与限制 |
| [SPDK Documentation](https://spdk.io/doc/index.html) | 用户态、轮询、异步、无锁 NVMe 存储栈 |
| [NVM Express Specifications](https://nvmexpress.org/specification/) | NVMe Base、NVMe over PCIe/RDMA/TCP、ZNS、NVMe-oF |

#### AI Infra 推荐主线

```text
硬件与性能基础 → Linux I/O → NVMe/SSD → io_uring
→ RDMA/RoCE → SPDK/NVMe-oF → 分布式存储
→ GPU 数据路径 → NCCL/GDS → 性能观测与故障排查
```

本地 vault 的详细章节地图见 `8.高性能存储/00. 总纲.md`；新增高性能存储或 AI Infra 笔记时，优先沿这条主线定位目录，并在正文中注明使用的是教材、标准规范还是项目官方文档。

### LLM

| 来源 | 覆盖 |
|---|---|
| 《Attention Is All You Need》 | Transformer 架构 |
| HuggingFace 官方文档 | Transformers 库、微调 |
| OpenAI / Anthropic 官方指南 | Prompt Engineering、Function Calling |
| LlamaIndex / LangChain 文档 | RAG |
| FastAPI、Docker 官方文档 | 服务与部署 |

### 投资

| 来源 | 覆盖 |
|---|---|
| 巴菲特致股东信 | 定价权、护城河、企业估值 |
| 芒格《穷查理宝典》 | 多元思维模型、心理偏误 |
| 波特《竞争战略》 | 五力模型、竞争优势 |
| Hull《期权、期货及其他衍生品》 | 衍生品定价、风险管理 |
| 彼得·林奇 | 选股、行业分析 |

---

## 三、笔记骨架（参考，不是模具）

按内容需要增删章节，别为了凑齐标题写空段。

**C++ 概念类**：概念定义 → 为什么需要 → 基本语法 → 常见用法 → 关键规则 → 陷阱与误区 → 底层原理（可选）→ 最佳实践 → 关联知识 → 参考

**C++ 设计/案例类**（代码量大时用）：问题背景 → 架构设计（组件职责表）→ 关键技术详解 → 完整实现（分段讲）→ 使用示例 → 性能分析 → 常见问题 → 要点总结

**LLM 类**：学习目标 + 本节产物 → 环境准备（依赖、环境变量、验证）→ 核心概念 → 实现 → 踩坑记录。frontmatter 加 `tags: LLM`。

**投资类**：核心概念（配大师引言）→ 生活化例子（至少两个不同角度）→ 数学表达（如适用）→ 经典案例（背景/经过/结果/启示）→ 练习。frontmatter 加金融学 tag。

**力扣题解**（vault 中现存笔记的实际结构）：
1. 题目概览（描述 / 输入输出与约束 / 示例 / 进阶）
2. 可用算法与数据结构（解法总览对比表 / 本题采用及原因 / 用到的数据结构 / 相关 STL 笔记引用）
3. 解题步骤（核心思路 / 详细步骤 / 示例推演）
4. SVG 图解
5. 源码实现（可多种写法）
6. 源码详解（变量说明 / 主流程拆解 / 写法对比 / 易错点）
7. 复杂度分析
8. 相关链接

简单题可省 4、6；复杂题可加「优化过程」「多解法对比」。

**章节题目汇总**：基础题 → 场景题 → 面试题，答案折叠。专项题型按章节性质注入（并发/网络/STL/OOP/模板各有各的考法）。
