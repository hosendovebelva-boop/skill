#!/usr/bin/env python3
"""密度自查：图里装的是标签还是句子。

核心判据不是「字多不多」，是「节点里的那些字是不是一句话」。
references/ 四张（含 64 个 text 的 SLO）全部通过本检查。

长句不是一律禁止：副标题、区标题、底栏口径条本来就是整行的句子，
它们横跨整个画面，不挤在任何一个方框里，读起来是一行字而不是一坨。
真正的问题是节点标签写成了句子。所以本检查只统计**正文区**的 text
（排除页面顶部的标题副标题、底部的总结条）。

红线（见 SKILL.md 顶部「硬约束」）：
  正文区每条 <text> 字数中位 <= 20
  正文区每条 <text> 字数 p90 <= 42
  正文区单条 <text> <= 48 字（区标题 A · / B · 除外，它们横跨整幅）
  font-size >= 9.5（短标注 <= 6 字的可以更小，如曲线上的数据点）
  viewBox 高度 <= 900

用法：
  python3 check_density.py 图片/SVG/*.svg
  python3 check_density.py ~/.claude/skills/obsidian-svg/references/*.svg   # 校准手感
"""
import re
import sys
import statistics
import xml.etree.ElementTree as ET

MED_MAX = 20
P90_MAX = 42
LINE_MAX = 48
MIN_FONT = 9.5
MAX_HEIGHT = 900

# 顶部这么高以内算标题区，底部这么高以内算总结条，两处允许整行长句
HEADER_H = 100
FOOTER_H = 90

# 区标题：横跨整幅的一行，不挤在方框里，长度不受 LINE_MAX 限制
SECTION_RE = re.compile(r"^[A-Z] ·")

# 字号可以低于 MIN_FONT 的例外：极短的点状标注（数据点、刻度、单位）
TINY_LABEL_MAX = 6

NS = "{http://www.w3.org/2000/svg}"


def percentile(sorted_vals, q):
    if not sorted_vals:
        return 0
    idx = min(int(len(sorted_vals) * q), len(sorted_vals) - 1)
    return sorted_vals[idx]


def measure(path):
    root = ET.parse(path).getroot()

    height = None
    vb = root.get("viewBox")
    if vb:
        parts = vb.split()
        if len(parts) == 4:
            height = float(parts[3])

    body = []       # 正文区的 text
    tiny_bad = []   # 字号过小、且不是极短标注的
    for t in root.iter(f"{NS}text"):
        s = "".join(t.itertext()).strip()
        if not s:
            continue
        try:
            y = float(t.get("y", "0"))
        except ValueError:
            y = 0.0

        size = t.get("font-size")
        if size:
            try:
                sz = float(size)
            except ValueError:
                sz = MIN_FONT
            if sz < MIN_FONT and len(s) > TINY_LABEL_MAX:
                tiny_bad.append((sz, s))

        in_header = y <= HEADER_H
        in_footer = height is not None and y >= height - FOOTER_H
        if in_header or in_footer:
            continue
        if SECTION_RE.match(s):     # 区标题横跨整幅，不算节点标签
            continue
        body.append(s)

    lengths = sorted(len(s) for s in body)
    median = statistics.median(lengths) if lengths else 0
    p90 = percentile(lengths, 0.9)
    overlong = [s for s in body if len(s) > LINE_MAX]

    return {
        "n": len(body),
        "median": median,
        "p90": p90,
        "overlong": overlong,
        "height": height,
        "tiny": tiny_bad,
    }


def main(paths):
    failed = False
    for path in paths:
        m = measure(path)
        problems = []

        if m["median"] > MED_MAX:
            problems.append(
                f"正文区每条 text 字数中位 {m['median']:g} > {MED_MAX}："
                "节点里在写句子，不是标签"
            )
        if m["p90"] > P90_MAX:
            problems.append(f"正文区字数 p90 {m['p90']} > {P90_MAX}")
        if m["overlong"]:
            n = len(m["overlong"])
            problems.append(f"正文区 {n} 条超过 {LINE_MAX} 字，应拆短或搬进笔记正文：")
            for s in m["overlong"][:3]:
                problems.append(f"      「{s[:38]}…」")
        if m["tiny"]:
            n = len(m["tiny"])
            problems.append(f"{n} 条字号低于 {MIN_FONT} 且不是极短标注：")
            for sz, s in m["tiny"][:3]:
                problems.append(f"      {sz:g}px 「{s[:32]}…」")
        if m["height"] is not None and m["height"] > MAX_HEIGHT:
            problems.append(f"viewBox 高 {m['height']:g} > {MAX_HEIGHT}")

        name = path.split("/")[-1]
        if problems:
            failed = True
            print(f"✗ {name}")
            for p in problems:
                print(f"    {p}")
        else:
            h = f"{m['height']:g}" if m["height"] is not None else "?"
            print(
                f"✓ {name}  text={m['n']} 中位={m['median']:g} p90={m['p90']} 高={h}"
            )

    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
