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
| Vault 根目录 | `D:\obsidian\C++` |
| SVG 资产目录 | `D:\obsidian\C++\图片\SVG` |
| 资产管理脚本 | `.claude/skills/obsidian-svg/scripts/obsidian_svg.py` |
| 设计系统验证 | `.claude/skills/obsidian-svg/scripts/validate_svg.py` |
| 精确构建 CLI | `.claude/skills/obsidian-svg/scripts/svg_cli.py` |

---

## 介质路由

在动手之前先决定用 SVG 还是 Mermaid。

**用 SVG：** 静态架构图、机制原理图、内存布局、组件分组、并列对比、概念图、算法概览、技术图表、研究级精绘。

**用 Mermaid：** 序列图、线程调用链、回调顺序、请求-响应时序、启动/关闭流程、生命周期时间线。除非用户明确要求 SVG。

---

## 工作流

1. **确定介质** — 按路由规则选择 SVG 或 Mermaid。
2. **规划布局** — 在心中构建场景规格：画布尺寸、viewBox、分组、节点坐标、标签、连线、图例。有歧义时先问用户。
3. **构建 SVG** — 使用显式几何：设定 `width`、`height`、`viewBox`，使用绝对坐标，保持标签完全在框内。
4. **应用设计系统** — 遵循下方的颜色、排版、箭头、布局规则。
5. **保存文件** — 存入 `D:\obsidian\C++\图片\SVG`，使用数字下划线命名。
6. **替换嵌入** — 将笔记中的内联 `<svg>` 替换为 `![[图片/SVG/<file>.svg]]`。
7. **验证** — 运行 `validate_svg.py`，确保通过所有检查。
8. **检查 diff** — 确认编辑范围仅限于目标图表。

---

## 设计系统

### 背景

每个 SVG 必须包含一个顶层背景矩形，`fill="rgb(245, 244, 237)"`，尺寸匹配 viewBox，置于前景元素之前。除非用户明确要求透明。

### 色彩体系

仅使用以下节点颜色，跨图表使用多种色系：

| 色系 | fill | stroke | text |
|------|------|--------|------|
| Blue | `#E6F1FB` | `#185FA5` | `#0C447C` |
| Purple | `#EEEDFE` | `#534AB7` | `#3C3489` |
| Teal | `#E1F5EE` | `#0F6E56` | `#085041` |
| Amber | `#FAEEDA` | `#854F0B` | `#633806` |
| Gray | `#F1EFE8` | `#5F5E5A` | `#444441` |

特殊值 `none`、`context-stroke`、`currentColor`、`transparent`、`inherit` 允许使用。

### 排版

- 主标签：`font-family="system-ui,sans-serif" font-size="14" font-weight="500"`
- 副标签：`font-family="system-ui,sans-serif" font-size="12" font-weight="400"`
- 每个 `<text>` 必须包含 `dominant-baseline="central"`
- 默认 `text-anchor="middle"`，仅在确需左对齐时使用 `start`

### 语言

- 可见解释性标签默认中文
- 代码标识符、API 名、类名、函数名、文件名、协议名保持原始语言

### 布局规则

| 规则 | 值 |
|------|-----|
| 最小框宽 | `最长标签字符数 x 8 + 48` |
| 单行框高 | `44` |
| 双行框高 | `56` |
| 框间最小间距 | `60` |
| 框圆角 | `rx="8"` |
| 框描边宽 | `0.5` |
| 箭头描边宽 | `1.5` |
| viewBox 底部留白 | `max_element_bottom + 40` |
| 四周留白 | `>= 20px` |

### 箭头标记

所有使用箭头的 SVG 必须包含此 marker 定义：

```xml
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

引用：`marker-end="url(#arrow)"`。风格要求：小空心箭头、`fill="none"`、细描边。

### SVG 构建规则

- 包含完整 `<svg>` 根：`xmlns`、`width`、`height`、`viewBox`
- 背景矩形紧跟在 `<defs>`/`<title>`/`<desc>` 之后
- 非简单图形添加 `<title>` 和 `<desc>` 用于可访问性
- 标签保持在框内，增大框尺寸而非缩小文字
- 长解释移至底部注释栏，不要塞进框里
- 优先使用正交 `polyline` 连接器而非长直线
- 使用绝对坐标和稳定尺寸，不依赖查看器默认值
- 避免装饰效果：重阴影、复杂渐变、噪点纹理

---

## 科学精度

适用于研究级图表、内存布局、字节单元、时间线、层级结构：

- 使用可复现几何，不手动估位
- 相关对象对齐到共享 x/y 坐标
- 重复组件使用稳定网格间距
- 图表标注轴、单位、刻度、图例和数据编码
- 文字渲染不可靠：给标签充足 padding，不依赖浏览器字体度量

---

## 数字下划线命名

从笔记路径的数字前缀派生文件名，附加 1-based SVG 索引。

规则：
- 剥离前导零：`04.Linux播放器服务器` → `4`
- 数字间用 `_` 分隔
- SVG 索引始终为最后一个数字
- 无法找到数字前缀时停止，不编造名字

示例：
- `6.项目\04.Linux播放器服务器\4.1 线程\4.1.6 Logger.md`，第 3 个 SVG → `6_4_1_1_6_3.svg`
- `6.项目\03.远控系统\1. 基础设置\1.2 visual studio 配置 git.md`，第 2 个 SVG → `6_3_1_2_2.svg`

---

## 命令参考

### 计算文件名

```powershell
python ".claude/skills/obsidian-svg/scripts/obsidian_svg.py" name-for-note "D:\obsidian\C++\path\to\note.md" --index 1
```

### 提取内联 SVG

```powershell
python ".claude/skills/obsidian-svg/scripts/obsidian_svg.py" extract-note "D:\obsidian\C++\path\to\note.md"
```

### 规范化 SVG 背景

```powershell
python ".claude/skills/obsidian-svg/scripts/obsidian_svg.py" normalize-svg "D:\obsidian\C++\图片\SVG\diagram.svg"
```

### 验证 SVG（基础）

```powershell
python ".claude/skills/obsidian-svg/scripts/obsidian_svg.py" validate-svg "D:\obsidian\C++\图片\SVG\diagram.svg"
```

新生成的数字资产加 `--strict-name`；旧手命名文件不加。

### 验证 SVG（设计系统）

```powershell
python ".claude/skills/obsidian-svg/scripts/validate_svg.py" "D:\obsidian\C++\图片\SVG\diagram.svg"
```

从 stdin 验证：

```powershell
Get-Content "path\to\diagram.svg" | python ".claude/skills/obsidian-svg/scripts/validate_svg.py" -
```

### 从 JSON spec 构建 SVG

```powershell
python ".claude/skills/obsidian-svg/scripts/svg_cli.py" build spec.json output.svg
```

### 渲染 PNG 预览

```powershell
python ".claude/skills/obsidian-svg/scripts/svg_cli.py" render diagram.svg preview.png --scale 2
```

需要 CairoSVG：`pip install cairosvg`

---

## 验证清单

交付前确认：

- [ ] 顶层背景矩形存在，使用 `rgb(245, 244, 237)`
- [ ] 背景矩形在前景内容之前
- [ ] 箭头使用 `marker-end="url(#arrow)"` 且 `<marker id="arrow">` 已定义
- [ ] 所有 fill/stroke/text 颜色来自批准色系
- [ ] 标签未溢出框宽度
- [ ] 矩形使用 `rx="8"` 和 `stroke-width="0.5"`
- [ ] 箭头使用 `stroke-width="1.5"`
- [ ] `<text>` 包含 `dominant-baseline="central"`
- [ ] 框间距 >= 60px
- [ ] viewBox 底部留白 >= 40px
- [ ] SVG 是合法 XML
- [ ] 笔记使用 Obsidian 嵌入 `![[图片/SVG/<file>.svg]]`
- [ ] 新资产使用数字下划线命名
- [ ] 运行 `validate_svg.py` 通过
