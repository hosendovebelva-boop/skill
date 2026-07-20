#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Note Locator - Obsidian笔记定位器
用于在Obsidian知识库中模糊搜索笔记并解析wiki-link关联
"""

import os
import re
import sys
import argparse
from pathlib import Path
from difflib import SequenceMatcher
from typing import List, Tuple, Optional, Set


def normalize_path(path: str) -> str:
    """统一路径格式，兼容Windows/Linux"""
    return str(Path(path)).replace('\\', '/')


def get_all_md_files(root_path: str) -> List[str]:
    """递归获取目录下所有.md文件"""
    md_files = []
    root = Path(root_path)

    if not root.exists():
        return md_files

    for path in root.rglob('*.md'):
        # 跳过隐藏目录和特殊目录
        parts = path.parts
        if any(part.startswith('.') or part.startswith('_') for part in parts):
            continue
        md_files.append(normalize_path(str(path)))

    return md_files


def calculate_similarity(keyword: str, filename: str) -> float:
    """
    计算关键词与文件名的相似度
    使用多种策略综合评分
    """
    # 提取纯文件名（不含路径和扩展名）
    name_only = Path(filename).stem

    # 策略1: 完全包含（最高优先级）
    if keyword.lower() in name_only.lower():
        # 关键词越长，包含匹配的权重越高
        contain_score = len(keyword) / max(len(name_only), 1) * 100
        return min(95 + contain_score * 0.05, 100)

    # 策略2: 序列匹配
    seq_ratio = SequenceMatcher(None, keyword.lower(), name_only.lower()).ratio()

    # 策略3: 词汇重叠（处理中文分词）
    keyword_chars = set(keyword)
    name_chars = set(name_only)
    overlap = len(keyword_chars & name_chars)
    char_ratio = overlap / max(len(keyword_chars), 1)

    # 策略4: 路径匹配加分（如果关键词出现在路径中）
    path_bonus = 0
    if keyword.lower() in filename.lower():
        path_bonus = 10

    # 综合评分
    final_score = (seq_ratio * 50 + char_ratio * 40 + path_bonus)
    return min(final_score, 100)


def fuzzy_search(keyword: str, md_files: List[str], top_n: int = 3) -> List[Tuple[str, float]]:
    """
    模糊搜索，返回匹配度最高的文件列表
    返回: [(文件路径, 匹配度), ...]
    """
    results = []

    for filepath in md_files:
        score = calculate_similarity(keyword, filepath)
        if score > 20:  # 最低阈值
            results.append((filepath, score))

    # 按匹配度降序排序
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]


def extract_wiki_links(content: str) -> Set[str]:
    """
    从笔记内容中提取所有wiki-links
    支持格式: [[链接]] 或 [[链接|显示文本]]
    """
    # 匹配 [[...]] 格式，排除图片 ![[...]]
    pattern = r'(?<!!)\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
    matches = re.findall(pattern, content)

    # 清理链接名称
    links = set()
    for match in matches:
        # 移除可能的锚点 #
        link_name = match.split('#')[0].strip()
        if link_name:
            links.add(link_name)

    return links


def find_link_target(link_name: str, md_files: List[str]) -> Optional[str]:
    """
    根据链接名称查找实际文件路径
    Obsidian链接可以是完整路径或仅文件名
    """
    link_lower = link_name.lower()

    # 优先精确匹配文件名
    for filepath in md_files:
        filename = Path(filepath).stem.lower()
        if filename == link_lower:
            return filepath

    # 尝试匹配包含路径的链接
    for filepath in md_files:
        # 移除扩展名后比较
        path_without_ext = filepath[:-3] if filepath.endswith('.md') else filepath
        if path_without_ext.lower().endswith(link_lower):
            return filepath

    # 模糊匹配作为后备
    for filepath in md_files:
        filename = Path(filepath).stem.lower()
        if link_lower in filename or filename in link_lower:
            return filepath

    return None


def locate_note(keyword: str, root_path: str, top_n: int = 3,
                resolve_links: bool = True) -> dict:
    """
    主函数：定位笔记并解析关联

    返回:
    {
        'target': {'path': str, 'score': float} | None,
        'links': [{'name': str, 'path': str | None}, ...],
        'candidates': [{'path': str, 'score': float}, ...]
    }
    """
    result = {
        'target': None,
        'links': [],
        'candidates': []
    }

    # 获取所有md文件
    md_files = get_all_md_files(root_path)

    if not md_files:
        return result

    # 模糊搜索
    matches = fuzzy_search(keyword, md_files, top_n)

    if not matches:
        return result

    # 最佳匹配作为目标
    best_path, best_score = matches[0]
    result['target'] = {'path': best_path, 'score': round(best_score, 1)}

    # 其他候选
    if len(matches) > 1:
        result['candidates'] = [
            {'path': p, 'score': round(s, 1)}
            for p, s in matches[1:]
        ]

    # 解析wiki-links
    if resolve_links and result['target']:
        try:
            with open(best_path, 'r', encoding='utf-8') as f:
                content = f.read()

            links = extract_wiki_links(content)

            for link_name in sorted(links):
                target_path = find_link_target(link_name, md_files)
                result['links'].append({
                    'name': link_name,
                    'path': target_path
                })
        except Exception as e:
            result['error'] = f"读取文件失败: {e}"

    return result


def format_output(result: dict) -> str:
    """格式化输出结果"""
    lines = []
    lines.append("=" * 40)
    lines.append("笔记定位结果")
    lines.append("=" * 40)
    lines.append("")

    if not result['target']:
        lines.append("未找到匹配的笔记")
        return '\n'.join(lines)

    # 目标笔记
    target = result['target']
    lines.append(f"目标笔记: {target['path']}")
    lines.append(f"匹配度: {target['score']}%")
    lines.append("")

    # 关联笔记
    if result['links']:
        lines.append(f"直接关联笔记 ({len(result['links'])}个):")
        for link in result['links']:
            if link['path']:
                lines.append(f"  → {link['path']}")
            else:
                lines.append(f"  → {link['name']} [未找到]")
        lines.append("")

    # 其他候选
    if result['candidates']:
        lines.append("其他候选:")
        for i, cand in enumerate(result['candidates'], 1):
            lines.append(f"  {i}. [{cand['score']}%] {cand['path']}")
        lines.append("")

    # 错误信息
    if 'error' in result:
        lines.append(f"警告: {result['error']}")

    return '\n'.join(lines)


def main():
    # 修复Windows控制台UTF-8编码问题
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Obsidian笔记定位器 - 模糊搜索并解析wiki-link关联'
    )
    parser.add_argument(
        'keyword',
        help='搜索关键词'
    )
    parser.add_argument(
        '--path', '-p',
        default='.',
        help='搜索根目录 (默认: 当前目录)'
    )
    parser.add_argument(
        '--top', '-t',
        type=int,
        default=3,
        help='返回候选数量 (默认: 3)'
    )
    parser.add_argument(
        '--no-links',
        action='store_true',
        help='不解析wiki-links'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='输出JSON格式'
    )

    args = parser.parse_args()

    # 执行定位
    result = locate_note(
        keyword=args.keyword,
        root_path=args.path,
        top_n=args.top,
        resolve_links=not args.no_links
    )

    # 输出结果
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == '__main__':
    main()
