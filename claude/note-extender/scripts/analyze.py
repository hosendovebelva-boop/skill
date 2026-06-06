#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note Analyzer - 笔记元信息提取器
为 note-extender Skill 提供笔记结构分析
"""

import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any
from collections import Counter


def extract_metadata(content: str, filepath: str) -> Dict[str, Any]:
    """
    提取笔记的元信息
    """
    lines = content.split('\n')

    metadata = {
        'file': filepath,
        'title': '',
        'stats': {},
        'structure': [],
        'links': [],
        'code_blocks': [],
        'warnings': [],
        'quality_indicators': {}
    }

    # 提取标题 (第一个 # 开头的行)
    for line in lines:
        if line.startswith('# ') and not line.startswith('## '):
            metadata['title'] = line[2:].strip()
            break

    if not metadata['title']:
        metadata['title'] = Path(filepath).stem

    # 统计信息
    metadata['stats'] = {
        'total_chars': len(content),
        'total_lines': len(lines),
        'word_count': len(content),  # 中文按字符计
        'code_lines': 0,
        'heading_count': 0,
        'link_count': 0,
        'image_count': 0
    }

    # 提取章节结构 (排除代码块内的内容)
    headings = []
    in_code_block = False
    for i, line in enumerate(lines):
        # 检测代码块边界
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        # 跳过代码块内的内容
        if in_code_block:
            continue
        # 检测 Markdown 标题 (# 后面必须有空格)
        if line.startswith('#') and len(line) > 1 and line.lstrip('#').startswith(' '):
            level = len(line) - len(line.lstrip('#'))
            title = line.lstrip('#').strip()
            if title and level <= 6:  # 有效的 Markdown 标题层级
                headings.append({
                    'level': level,
                    'title': title,
                    'line': i + 1
                })
    metadata['structure'] = headings
    metadata['stats']['heading_count'] = len(headings)

    # 提取 wiki-links
    link_pattern = r'(?<!!)\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    links = re.findall(link_pattern, content)
    metadata['links'] = list(set(links))
    metadata['stats']['link_count'] = len(links)

    # 提取图片
    image_pattern = r'!\[\[([^\]]+)\]\]'
    images = re.findall(image_pattern, content)
    metadata['stats']['image_count'] = len(images)

    # 提取代码块
    code_block_pattern = r'```(\w*)\n(.*?)```'
    code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
    code_info = []
    total_code_lines = 0
    for lang, code in code_blocks:
        lines_count = len(code.strip().split('\n'))
        total_code_lines += lines_count
        code_info.append({
            'language': lang or 'unknown',
            'lines': lines_count
        })
    metadata['code_blocks'] = code_info
    metadata['stats']['code_lines'] = total_code_lines

    # 质量指标检测
    quality = {
        'has_definition': False,      # 有概念定义
        'has_example': False,         # 有代码示例
        'has_warning': False,         # 有警告/注意
        'has_best_practice': False,   # 有最佳实践
        'has_reference': False,       # 有参考来源
        'has_links': len(links) > 0,  # 有关联链接
    }

    content_lower = content.lower()

    # 检测概念定义
    if any(kw in content for kw in ['定义', '概念', '是什么', '指的是', '表示']):
        quality['has_definition'] = True

    # 检测代码示例
    if len(code_blocks) > 0:
        quality['has_example'] = True

    # 检测警告/注意
    if any(kw in content for kw in ['注意', '警告', 'warning', '陷阱', '误区', '错误', '避免']):
        quality['has_warning'] = True

    # 检测最佳实践
    if any(kw in content for kw in ['最佳实践', '推荐', '建议', '应该', '不应该', 'best practice']):
        quality['has_best_practice'] = True

    # 检测参考来源
    if any(kw in content for kw in ['参考', 'Effective', 'Item', '书籍', '来源']):
        quality['has_reference'] = True

    metadata['quality_indicators'] = quality

    # 计算质量得分
    score = sum([
        quality['has_definition'] * 20,
        quality['has_example'] * 25,
        quality['has_warning'] * 15,
        quality['has_best_practice'] * 15,
        quality['has_reference'] * 10,
        quality['has_links'] * 15,
    ])
    metadata['quality_score'] = score

    # 生成警告
    warnings = []
    if not quality['has_definition']:
        warnings.append("缺少明确的概念定义")
    if not quality['has_example']:
        warnings.append("缺少代码示例")
    if not quality['has_warning']:
        warnings.append("缺少陷阱/注意事项说明")
    if not quality['has_links']:
        warnings.append("缺少关联笔记链接")
    if metadata['stats']['total_chars'] < 500:
        warnings.append("内容较少，可能需要扩展")

    metadata['warnings'] = warnings

    return metadata


def format_report(metadata: Dict[str, Any]) -> str:
    """格式化输出元信息报告"""
    lines = []
    lines.append("=" * 50)
    lines.append(f"笔记分析报告: {metadata['title']}")
    lines.append("=" * 50)
    lines.append("")

    # 基本统计
    stats = metadata['stats']
    lines.append("## 基本统计")
    lines.append(f"  文件: {metadata['file']}")
    lines.append(f"  字数: {stats['total_chars']} 字符 / {stats['total_lines']} 行")
    lines.append(f"  章节: {stats['heading_count']} 个")
    lines.append(f"  代码: {stats['code_lines']} 行")
    lines.append(f"  链接: {stats['link_count']} 个")
    lines.append(f"  图片: {stats['image_count']} 个")
    lines.append("")

    # 章节结构
    if metadata['structure']:
        lines.append("## 章节结构")
        for h in metadata['structure']:
            indent = "  " * (h['level'] - 1)
            lines.append(f"  {indent}{'#' * h['level']} {h['title']}")
        lines.append("")

    # 代码块
    if metadata['code_blocks']:
        lines.append("## 代码块")
        lang_counter = Counter(cb['language'] for cb in metadata['code_blocks'])
        for lang, count in lang_counter.items():
            lines.append(f"  {lang}: {count} 块")
        lines.append("")

    # 现有链接
    if metadata['links']:
        lines.append("## 现有链接")
        for link in metadata['links'][:10]:  # 最多显示10个
            lines.append(f"  → [[{link}]]")
        if len(metadata['links']) > 10:
            lines.append(f"  ... 还有 {len(metadata['links']) - 10} 个链接")
        lines.append("")

    # 质量评估
    lines.append("## 质量评估")
    quality = metadata['quality_indicators']
    indicators = [
        ('概念定义', quality['has_definition']),
        ('代码示例', quality['has_example']),
        ('陷阱警示', quality['has_warning']),
        ('最佳实践', quality['has_best_practice']),
        ('参考来源', quality['has_reference']),
        ('关联链接', quality['has_links']),
    ]
    for name, has in indicators:
        status = "✓" if has else "✗"
        lines.append(f"  [{status}] {name}")
    lines.append(f"  总分: {metadata['quality_score']}/100")
    lines.append("")

    # 改进建议
    if metadata['warnings']:
        lines.append("## 需要改进")
        for w in metadata['warnings']:
            lines.append(f"  ⚠ {w}")
        lines.append("")

    return '\n'.join(lines)


def main():
    # Windows UTF-8 支持
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='笔记元信息分析器'
    )
    parser.add_argument(
        'file',
        help='笔记文件路径'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='输出JSON格式'
    )

    args = parser.parse_args()

    # 读取文件
    filepath = Path(args.file)
    if not filepath.exists():
        print(f"错误: 文件不存在 - {filepath}")
        sys.exit(1)

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 - {e}")
        sys.exit(1)

    # 分析
    metadata = extract_metadata(content, str(filepath))

    # 输出
    if args.json:
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
    else:
        print(format_report(metadata))


if __name__ == '__main__':
    main()
