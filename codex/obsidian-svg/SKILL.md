---
name: obsidian-svg
description: |
  创建、优化、验证 SVG 图表并管理 Obsidian vault 的 SVG 资产。当用户需要以下操作时使用此 Skill：
  - 创建 SVG 图表（如"画一个架构图"、"生成内存布局图"、"画一个流程图"）
  - 优化现有 SVG（如"优化这个 SVG"、"改进图表样式"）
  - 验证 SVG 质量（如"检查 SVG"、"验证图表"）
  - 提取内联 SVG（如"把笔记里的 SVG 提取出来"）
  - 规范化 SVG 背景和命名（如"规范化 SVG 文件"）
  触发词：SVG、画图、架构图、流程图、内存布局、图表、diagram、优化SVG、验证SVG
---

# Obsidian SVG — 创建 + 优化 + 资产管理

本 Skill 整合了四项能力：精确 SVG 构建、教学级视觉设计、设计系统验证、Obsidian vault 资产管理。

---

## 路径配置

| 项目 | 路径 |
|------|------|
| Vault 根目录 | 当前 vault（macOS 常见：`~/Documents/C++/obsidian_notes-main`） |
| SVG 资产目录 | `<vault>/图片/SVG` |
| 参考图目录 | `~/.claude/skills/obsidian-svg/references/`（本 skill 内置） |
| 资产管理脚本 | `~/.claude/skills/obsidian-svg/scripts/obsidian_svg.py` |
| 设计系统验证 | `~/.claude/skills/obsidian-svg/scripts/validate_svg.py` |
| 精确构建 CLI | `~/.claude/skills/obsidian-svg/scripts/svg_cli.py` |

---

## 先读：参考图与选型（必做）

**禁止**对所有笔记套同一套「等宽卡片网格」。先判断内容形态，再选布局；可在一张图内组合多种手法。

### 内置参考图（动手前至少读 1–2 张同类）

| 参考文件 | 内容形态 | 学什么 |
|----------|----------|--------|
| `references/readahead-预读流水线.svg` | **机制动画帧 / 窗口增长** | 多行「状态快照」并排；标记页红点；消费与预取重叠时间条；少卡片、多几何示意 |
| `references/全路径-read未命中泳道.svg` | **跨层时序泳道** | 四层横向泳道 + 编号步骤；中段睡眠虚线框；层间垂直箭头；底部延迟预算条 |
| `references/p99毛刺-周期归因与分层二分.svg` | **诊断方法全景** | 对齐双折线时间线；指纹表；分层二分梯；尾延迟放大器；底部流程条——多手法拼一页 |
| `references/SLO-错误预算与噪声回归门禁.svg` | **控制环 + 门禁双面板** | 左对齐大标题+副标题；A/B 分区；管线卡片；燃尽曲线；告警表；分布重叠示意；噪声对策表 |

Vault 同源路径（便于对照嵌入）：

- `图片/SVG/readahead-预读流水线.svg`
- `图片/SVG/全路径-read未命中泳道.svg`
- `图片/SVG/p99毛刺-周期归因与分层二分.svg`
- `图片/SVG/SLO-错误预算与噪声回归门禁.svg`

### 按内容选型（具体情况具体分析）

| 笔记在讲什么 | 优先布局 | 参考 |
|--------------|----------|------|
| 内核/设备机制、窗口、队列、流水线重叠 | 时间/窗口帧序列 + 少量标注 | readahead |
| 一次调用跨用户态/内核/块层/设备 | 泳道（lane）+ 编号步骤 + 睡眠/等待区 | 全路径 read |
| 排障、归因、方法、决策 | 时间线对齐 + 表 + 分层梯 + 底部流程 | p99 毛刺 |
| 契约/告警/回归门禁、概念对照 | 双面板 A/B + 曲线/分布 + 表格 | SLO |
| 指标家族、变量矩阵、签名对照 | 等宽卡片网格 + 公式条（可作子区，勿整页唯一手法） | 9.x iostat 类 |
| 内存布局、MESI、false sharing | 结构示意 + 好坏对照 + 协议条 | 0.1 Cache 类 |

**搭配原则：**

1. **一张图可混用**多种手法（例如上半泳道 + 下半签名表；左曲线 + 右告警表）。
2. **先叙事后装饰**——标题讲清「这张图解决什么问题」，副标题给一句判断准则。
3. **密度服务于教学**——关键数字、公式、边界条件写进图；不要为了「干净」删掉判断句。
4. **不要机械复刻**某一张参考的分区数量；参考的是视觉系统与信息架构，不是像素模板。

---

## 介质路由

在动手之前先决定用 SVG 还是 Mermaid。

**用 SVG：** 静态架构图、机制原理图、内存布局、组件分组、并列对比、概念图、算法概览、技术图表、研究级精绘、诊断全景、泳道、控制环。

**用 Mermaid：** 纯序列图、线程调用链、回调顺序、请求-响应时序、启动/关闭流程、生命周期时间线——且用户未要求 SVG 时。

用户明确要求 SVG、或需要与 vault 教学图同一视觉系统时，**优先 SVG**。

---

## 工作流

1. **读笔记上下文** — 确定教学点、嵌入位置、是否已有同章参考图。
2. **选型** — 按上表选 1 种主布局，必要时组合副布局；打开 1–2 张 `references/` 对照。
3. **规划几何** — viewBox（教学全景常用 `1240 × 740–940`）、分区 A/B/C、坐标网格、标题区高度。
4. **构建 SVG** — 绝对坐标；标签不溢出；中文解释 + 英文标识符。
5. **应用教学视觉系统**（见下）— 与参考图一致，而非只套 strict palette。
6. **保存** — `<vault>/图片/SVG/`，优先数字下划线命名；既有语义文件名可保留。
7. **嵌入** — `![[图片/SVG/<file>.svg|900]]`（宽度可按笔记调整）。
8. **检查** — 合法 XML、背景、可读性；`validate_svg.py` 对教学色板可能失败，见「验证策略」。
9. **diff** — 只动目标 SVG 与必要的笔记嵌入行。

---

## 教学视觉系统（高性能存储 / 系统笔记首选）

与 `references/SLO-错误预算与噪声回归门禁.svg` 等同族。用于深度教学图；**可与下方「strict 节点色板」并存**：简单卡片图用 strict，教学全景用本系统。

### 画布与字体

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1240 H"
     font-family="'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',sans-serif">
```

- 背景：`fill="rgb(245, 244, 237)"` 或 `#F5F4ED`，铺满 viewBox
- 面板底：`#FBFBF6`，描边 `#D8D5C8`
- 主标题：`font-size="22" font-weight="700" fill="#2B2A26"`，**左对齐**（`x≈48`）
- 副标题：`font-size="13" fill="#6B675C"`
- 区标题：`font-size="13" font-weight="700" fill="#4A473F"`，可用 `A · …` / `B · …`
- 主文案：`11–12.5`；注释：`9.5–10.5`
- 中性字色：`#2B2A26` / `#4A473F` / `#6B675C`

### 语义色（节点 / 强调）

| 角色 | fill | stroke | text |
|------|------|--------|------|
| 信息 / 流程蓝 | `#E3EAF4` | `#3D5A80` | `#2C4460` |
| 安全 / 通过绿 | `#DCE9E3` | `#2F6B5E` | `#24473F` |
| 注意 / 窗口琥珀 | `#EFE7DA` 或 `#F3E8D3` | `#8A6A3A` / `#B07D2B` | `#6B4E28` |
| 告警 / 饱和红 | `#F0E0DB` | `#A64B3C` | `#733428` |
| 中性灰 | `#F1EFE8` / `#EDEBE3` | `#4A473F` / `#9B968A` | `#4A473F` |
| 泳道淡紫（可选） | `#EDEAF3` | `#D8D5C8` | `#6B5B95` |

描边宽度：内容框常用 `1.2–1.5`（教学图可读优先）；圆角 `rx="7"` 或 `8`。

### 箭头

教学图优先**实心三角**（与参考一致）：

```xml
<defs>
  <marker id="arr" viewBox="0 0 10 10" refX="8.5" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M0,0 L10,5 L0,10 z" fill="#5A564B"/>
  </marker>
  <!-- 告警流可用 fill="#A64B3C" 的第二 marker -->
</defs>
```

连线：`stroke="#5A564B"`，`stroke-width="1.5–1.8"`，`marker-end="url(#arr)"`。

### 信息架构习惯

- 顶部：一句「问题/命题」标题 + 一句「判断准则」副标题
- 中部分区：A/B（或 ①②③④）按叙事推进，不是装饰分栏
- 曲线/表/签名卡：只承载决策信息
- 底部：边界条件、口径提醒、或「刻画→对号→二分→验证」类流程条
- 需要公式时用独立条带（如 Little's law / Q_fio），勿塞进过小卡片

---

## Strict 节点色板（简单图 / 校验友好）

用于少节点、等宽卡片、需要 `validate_svg.py` 全绿的场景：

| 色系 | fill | stroke | text |
|------|------|--------|------|
| Blue | `#E6F1FB` | `#185FA5` | `#0C447C` |
| Purple | `#EEEDFE` | `#534AB7` | `#3C3489` |
| Teal | `#E1F5EE` | `#0F6E56` | `#085041` |
| Amber | `#FAEEDA` | `#854F0B` | `#633806` |
| Gray | `#F1EFE8` | `#5F5E5A` | `#444441` |

特殊值 `none`、`context-stroke`、`currentColor`、`transparent`、`inherit` 允许。

### Strict 排版与间距

- 主标签：`font-family="system-ui,sans-serif" font-size="14" font-weight="500"`
- 副标签：`font-size="12" font-weight="400"`
- 每个 `<text>` 建议含 `dominant-baseline="central"`（教学图若用 `y` 基线排版可省略，但勿混用到难以阅读）
- 框：`rx="8"`，`stroke-width="0.5"`；箭头描边 `1.5`
- 框间距 ≥ 60px；viewBox 底边距 ≥ 40；四周 ≥ 20

### Strict 空心箭头（可选）

```xml
<marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
        markerWidth="6" markerHeight="6" orient="auto-start-reverse">
  <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
        stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
</marker>
```

---

## 语言

- 可见解释性标签默认**中文**
- 代码标识符、API、类名、函数名、文件名、协议名、指标名保持原始语言（`iostat`、`await`、`MESI`、`O_DIRECT` 等）

---

## SVG 构建规则

- 完整 `<svg>`：`xmlns`、建议设 `width`/`height` 或仅 `viewBox`
- 背景矩形紧跟在 `<defs>` / `<title>` / `<desc>` 之后
- 复杂图加 `<title>` 与 `<desc>`
- 标签在框内；框不够就加大，不缩小到难读
- 长解释放注释栏/底栏，不堆进节点
- 优先正交连线；绝对坐标
- 避免重阴影、复杂渐变、噪点、emoji 装饰

---

## 科学精度

适用于研究级图表、内存布局、字节单元、时间线、层级结构：

- 可复现几何，共享对齐线
- 重复组件用稳定网格
- 轴、单位、图例、数据编码写清楚
- 文字度量不可靠：给 padding，不赌字体宽度

---

## 数字下划线命名

从笔记路径数字前缀派生，附加 1-based SVG 索引。

规则：
- 剥离前导零：`04.Linux…` → `4`
- 数字间 `_`；SVG 序号在最后
- 推不出数字前缀时不编造（可保留语义名，如参考图）

示例：
- `8.高性能存储/9.…/9.2 iostat….md` 第 1 图 → `8_9_9_2_1.svg`
- `6.项目/03.远控…/1.2 ….md` 第 2 图 → `6_3_1_2_2.svg`

---

## 验证策略

1. **结构**：合法 XML；背景存在；嵌入路径正确。
2. **教学图**（本系统色板 + 密排）：以参考图观感为准；`validate_svg.py` 可能因 palette/间距报红——**可接受**，与 `SLO-错误预算与噪声回归门禁.svg` 同策略。
3. **Strict 简单图**：跑 `validate_svg.py` 并修到通过。
4. 交付前人工扫：标题是否左对齐、分区是否讲清故事、有无多余装饰线。

### 命令

```bash
# 文件名建议
python ~/.claude/skills/obsidian-svg/scripts/obsidian_svg.py name-for-note "/path/to/note.md" --index 1

# 提取内联 SVG
python ~/.claude/skills/obsidian-svg/scripts/obsidian_svg.py extract-note "/path/to/note.md"

# 规范化背景
python ~/.claude/skills/obsidian-svg/scripts/obsidian_svg.py normalize-svg "/path/to/diagram.svg"

# 基础 / 设计校验
python ~/.claude/skills/obsidian-svg/scripts/obsidian_svg.py validate-svg "/path/to/diagram.svg"
python ~/.claude/skills/obsidian-svg/scripts/validate_svg.py "/path/to/diagram.svg"

# JSON 构建 / 预览
python ~/.claude/skills/obsidian-svg/scripts/svg_cli.py build spec.json out.svg
python ~/.claude/skills/obsidian-svg/scripts/svg_cli.py render diagram.svg preview.png --scale 2
```

（Windows 上把路径换成 vault 与 skill 实际位置即可。）

---

## 验证清单

交付前确认：

- [ ] 已按内容选型，而非默认一整页等宽卡片
- [ ] 至少对照过 1 张 `references/` 同类参考图
- [ ] 顶层背景 `rgb(245, 244, 237)` / `#F5F4ED`，在前景之前
- [ ] 教学图：实心三角 marker + 语义色；strict 图：批准色板 + 间距规则
- [ ] 标题/分区叙事清楚；标签可读、不溢出
- [ ] 合法 XML；笔记嵌入 `![[图片/SVG/<file>.svg|…]]`
- [ ] 新资产优先数字下划线命名
- [ ] 教学图不因 validate 色板失败而强行改回「空洞卡片风」
