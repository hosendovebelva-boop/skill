# Algorithm Category & STL Mapping Reference

## Algorithm Categories

Each category name is used as a subdirectory under `5.算法/力扣/`.

| 分类名 | 说明 | 典型题号 |
|--------|------|----------|
| 滑动窗口 | 维护一个窗口在数组/字符串上滑动，用于子串/子数组问题 | 3, 76, 239, 438 |
| 双指针 | 左右指针或快慢指针遍历有序/链表结构 | 15, 11, 167, 283 |
| 动态规划 | 状态转移方程求最优解，含背包、区间DP、树形DP等 | 70, 198, 300, 1143 |
| 链表 | 链表增删改查、反转、合并、环检测 | 206, 25, 21, 141, 160 |
| 二叉树 | 二叉树遍历、构造、性质判断、路径问题 | 94, 104, 226, 236 |
| 回溯 | 递归搜索所有可能解，剪枝优化 | 46, 78, 39, 51 |
| 贪心 | 局部最优推导全局最优 | 55, 45, 134, 763 |
| 堆与优先队列 | 利用堆结构维护最值，Top-K 问题 | 215, 347, 295, 23 |
| 图论 | 图的遍历、最短路、拓扑排序、最小生成树 | 200, 207, 743, 785 |
| 排序 | 各类排序算法及其应用 | 912, 56, 148, 179 |
| 栈与队列 | 单调栈、括号匹配、队列模拟 | 20, 155, 232, 394 |
| 哈希表 | 利用哈希实现O(1)查找、去重、计数 | 1, 49, 128, 560 |
| 二分查找 | 有序结构上的对数级搜索 | 33, 34, 74, 153 |
| 设计题 | 数据结构设计与实现 | 146, 155, 208, 380 |
| 前缀和 | 前缀和/差分数组快速求区间和 | 303, 304, 560, 238 |
| 深度优先搜索 | DFS 遍历树/图/矩阵 | 200, 130, 417, 695 |
| 广度优先搜索 | BFS 层序遍历、最短路径 | 102, 127, 994, 752 |
| 并查集 | Union-Find 处理连通性问题 | 547, 684, 721, 990 |
| 单调栈 | 单调递增/递减栈求下一个更大/更小元素 | 42, 84, 496, 739 |
| 字符串 | KMP、Trie、字符串匹配与处理 | 28, 5, 14, 72 |

---

## STL Keyword-to-Wikilink Mapping

When solution code contains these C++ STL keywords, add the corresponding wikilink to the note's `相关链接` section.

| C++ 关键词 / 类型 | Wikilink | 匹配规则 |
|-------------------|----------|----------|
| `vector`, `push_back`, `emplace_back`, `std::vector` | `[[14.1 vector]]` | 代码中使用 vector 容器 |
| `queue`, `priority_queue`, `front`, `std::queue` | `[[14.2 queue]]` | 代码中使用队列 |
| `list`, `splice`, `push_front`, `std::list` | `[[14.3 list及其与其他结构的区别]]` | 代码中使用双向链表 |
| `set`, `multiset`, `unordered_set`, `std::set` | `[[14.4 set]]` | 代码中使用集合容器 |
| `map`, `unordered_map`, `multimap`, `std::map` | `[[14.5 map]]` | 代码中使用映射容器 |
| `string`, `substr`, `find`, `npos`, `std::string`, `to_string` | `[[14.6 string]]` | 代码中使用字符串操作 |
| `iterator`, `begin()`, `end()`, `::iterator`, `auto it` | `[[14.7 迭代器]]` | 代码中显式使用迭代器 |
| `stack`, `adapter`, `std::stack` | `[[14.8 容器适配器]]` | 代码中使用栈适配器 |
| `greater<>`, `less<>`, `operator()`, functor | `[[14.9 函数对象]]` | 代码中使用函数对象/比较器 |
| `bind`, `placeholders`, `std::bind` | `[[14.10 泛型算法与绑定器]]` | 代码中使用绑定器 |
| `sort`, `nth_element`, `lower_bound`, `upper_bound`, `binary_search`, `accumulate`, `transform`, `for_each`, `reverse`, `unique`, `partition`, `max_element`, `min_element` | `[[14.11 算法]]` | 代码中使用 STL 算法函数 |
| 大整数运算、高精度加减乘除 | `[[14.12 高精度]]` | 涉及大数运算 |
| 前缀和、`partial_sum`、差分数组 | `[[14.13 前缀和]]` | 使用前缀和技巧 |
| 红黑树底层、`std::map`/`std::set` 内部实现 | `[[14.14 红黑树]]` | 讨论底层树结构 |
| 动态规划、状态转移方程、`dp[]` | `[[14.15 动态规划]]` | 使用动态规划方法 |

### Mapping Rules

1. Only add a wikilink when the STL feature is **actually used in the solution code**, not merely mentioned in prose.
2. Add at most **one wikilink per STL reference file** per note.
3. Each wikilink in `相关链接` must include a brief Chinese description of why it is relevant.
4. Format: `- [[14.x xxx]] — {简要说明用途}`
