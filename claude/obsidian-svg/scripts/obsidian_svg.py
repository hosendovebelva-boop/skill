from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path, PurePosixPath


DEFAULT_FILL = "rgb(245, 244, 237)"
SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_VAULT_ROOT = SCRIPT_PATH.parents[4]
DEFAULT_EMBED_DIR = "图片/SVG"

SVG_BLOCK_RE = re.compile(r"<svg\b[\s\S]*?</svg>", re.IGNORECASE)
SVG_OPEN_RE = re.compile(r"<svg\b[^>]*>", re.IGNORECASE | re.DOTALL)
RECT_TAG_RE = re.compile(r"<rect\b[^>]*>", re.IGNORECASE | re.DOTALL)
ATTR_RE = re.compile(r"\b([A-Za-z_:][-A-Za-z0-9_:.]*)=(['\"])(.*?)\2", re.DOTALL)
FILL_ATTR_RE = re.compile(r"\bfill=(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)
STYLE_ATTR_RE = re.compile(r"\bstyle=(['\"])(.*?)\1", re.IGNORECASE | re.DOTALL)
INVALID_AMP_RE = re.compile(
    r"&(?!#\d+;|#x[0-9A-Fa-f]+;|[A-Za-z][A-Za-z0-9._:-]*;)"
)
NUMERIC_PREFIX_RE = re.compile(r"^\s*(\d+(?:\.\d+)*)")
NUMERIC_SVG_NAME_RE = re.compile(r"^\d+(?:_\d+)*\.svg$", re.IGNORECASE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def attrs_from_tag(tag_text: str) -> dict[str, str]:
    return {match.group(1).lower(): match.group(3) for match in ATTR_RE.finditer(tag_text)}


def add_or_replace_fill_attr(tag_text: str, fill: str) -> str:
    style_match = STYLE_ATTR_RE.search(tag_text)
    if style_match:
        style_text = style_match.group(2)
        if re.search(r"(^|;)\s*fill\s*:", style_text, flags=re.IGNORECASE):
            updated_style = re.sub(
                r"((?:^|;)\s*fill\s*:\s*)[^;]+",
                rf"\1{fill}",
                style_text,
                count=1,
                flags=re.IGNORECASE,
            )
        else:
            updated_style = style_text.rstrip()
            if updated_style and not updated_style.endswith(";"):
                updated_style += ";"
            if updated_style:
                updated_style += " "
            updated_style += f"fill: {fill}"
        tag_text = (
            tag_text[: style_match.start(2)]
            + updated_style
            + tag_text[style_match.end(2) :]
        )

    if FILL_ATTR_RE.search(tag_text):
        return FILL_ATTR_RE.sub(f'fill="{fill}"', tag_text, count=1)

    if tag_text.endswith("/>"):
        return tag_text[:-2].rstrip() + f' fill="{fill}"/>'

    if tag_text.endswith(">"):
        return tag_text[:-1].rstrip() + f' fill="{fill}">'

    return tag_text


def ensure_xml_entities(svg_text: str) -> str:
    return INVALID_AMP_RE.sub("&amp;", svg_text)


def is_zero(value: str | None) -> bool:
    return value is None or value in {"0", "0px", "0.0", "0.0px"}


def rect_looks_like_background(tag_text: str) -> bool:
    attrs = attrs_from_tag(tag_text)
    return bool(attrs.get("width") and attrs.get("height") and is_zero(attrs.get("x")) and is_zero(attrs.get("y")))


def normalize_fill(fill: str | None) -> str:
    return re.sub(r"\s+", " ", fill or "").strip().lower()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def parse_svg(svg_text: str) -> ET.Element:
    return ET.fromstring(ensure_xml_entities(svg_text))


def has_background(svg_text: str, fill: str = DEFAULT_FILL) -> bool:
    try:
        root = parse_svg(svg_text)
    except ET.ParseError:
        return False

    required = normalize_fill(fill)
    for child in list(root):
        if local_name(child.tag) != "rect":
            continue
        width = child.attrib.get("width")
        height = child.attrib.get("height")
        if width and height and normalize_fill(child.attrib.get("fill")) == required:
            return True
    return False


def ensure_background(svg_text: str, fill: str) -> str:
    svg_text = ensure_xml_entities(svg_text)
    open_match = SVG_OPEN_RE.search(svg_text)
    if not open_match:
        raise ValueError("No <svg> opening tag found.")

    for rect_match in RECT_TAG_RE.finditer(svg_text, open_match.end()):
        rect_tag = rect_match.group(0)
        if rect_looks_like_background(rect_tag):
            updated = add_or_replace_fill_attr(rect_tag, fill)
            return svg_text[: rect_match.start()] + updated + svg_text[rect_match.end() :]

    insertion = f'\n  <rect width="100%" height="100%" fill="{fill}"/>\n'
    return svg_text[: open_match.end()] + insertion + svg_text[open_match.end() :]


def build_embed_path(embed_dir: str, file_name: str) -> str:
    parts = [part for part in Path(embed_dir).parts if part not in ("", ".")]
    return str(PurePosixPath(*parts, file_name))


def number_prefix(text: str) -> list[int]:
    match = NUMERIC_PREFIX_RE.match(text)
    if not match:
        return []
    return [int(part) for part in match.group(1).split(".")]


def append_with_overlap(parts: list[int], nums: list[int]) -> None:
    max_overlap = min(len(parts), len(nums))
    overlap = 0
    for size in range(max_overlap, 0, -1):
        if parts[-size:] == nums[:size]:
            overlap = size
            break
    parts.extend(nums[overlap:])


def note_relative_parts(note_path: Path, vault_root: Path) -> tuple[str, ...]:
    try:
        return note_path.resolve().relative_to(vault_root.resolve()).parts
    except ValueError as exc:
        raise ValueError(f"Note is not inside vault root: {note_path}") from exc


def name_parts_for_note(note_path: Path, vault_root: Path, index: int) -> list[int]:
    if index < 1:
        raise ValueError("--index must be >= 1")

    relative_parts = note_relative_parts(note_path, vault_root)
    if not relative_parts:
        raise ValueError(f"Cannot derive a name from path: {note_path}")

    parts: list[int] = []
    for directory in relative_parts[:-1]:
        nums = number_prefix(directory)
        if nums:
            append_with_overlap(parts, nums)

    stem_nums = number_prefix(Path(relative_parts[-1]).stem)
    if stem_nums:
        if parts and stem_nums[0] in parts:
            stem_nums = stem_nums[1:]
        parts.extend(stem_nums)

    if not parts:
        raise ValueError(f"No numeric path prefix found for: {note_path}")

    parts.append(index)
    return parts


def file_name_for_note(note_path: Path, vault_root: Path, index: int) -> str:
    parts = name_parts_for_note(note_path, vault_root, index)
    return "_".join(str(part) for part in parts) + ".svg"


def extract_note(note_path: Path, vault_root: Path, embed_dir: str, fill: str) -> int:
    note_text = read_text(note_path)
    matches = list(SVG_BLOCK_RE.finditer(note_text))
    if not matches:
        print(f"No inline SVG blocks found in {note_path}")
        return 0

    export_dir = vault_root / embed_dir
    written_files: list[Path] = []
    counter = 0

    def replacer(match: re.Match[str]) -> str:
        nonlocal counter
        counter += 1
        file_name = file_name_for_note(note_path, vault_root, counter)
        export_path = export_dir / file_name
        svg_text = ensure_background(match.group(0), fill)
        write_text(export_path, svg_text)
        written_files.append(export_path)
        return f"![[{build_embed_path(embed_dir, file_name)}]]"

    updated_note = SVG_BLOCK_RE.sub(replacer, note_text)
    if updated_note != note_text:
        write_text(note_path, updated_note)

    print(f"Updated note: {note_path}")
    for written in written_files:
        print(f"Wrote SVG: {written}")
    return 0


def normalize_svg(svg_paths: list[Path], fill: str) -> int:
    for svg_path in svg_paths:
        original = read_text(svg_path)
        updated = ensure_background(original, fill)
        parse_svg(updated)
        if updated != original:
            write_text(svg_path, updated)
            print(f"Updated SVG: {svg_path}")
        else:
            print(f"Unchanged SVG: {svg_path}")
    return 0


def validate_svg(svg_paths: list[Path], fill: str, strict_name: bool) -> int:
    had_error = False
    for svg_path in svg_paths:
        errors: list[str] = []
        warnings: list[str] = []
        try:
            text = read_text(svg_path)
            root = parse_svg(text)
            if local_name(root.tag) != "svg":
                errors.append("root element is not <svg>")
            if not has_background(text, fill):
                errors.append(f"missing top-level background fill {fill}")
        except Exception as exc:
            errors.append(str(exc))

        if not NUMERIC_SVG_NAME_RE.match(svg_path.name):
            message = "filename is not numeric underscore form"
            if strict_name:
                errors.append(message)
            else:
                warnings.append(message)

        if errors:
            had_error = True
            print(f"INVALID: {svg_path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {svg_path}")
            for warning in warnings:
                print(f"  - warning: {warning}")

    return 1 if had_error else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Manage SVG assets for the D:\\obsidian\\C++ Obsidian vault.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    name_parser = subparsers.add_parser(
        "name-for-note",
        help="Print the numeric underscore SVG filename for a note and SVG index.",
    )
    name_parser.add_argument("note", type=Path, help="Absolute or relative path to the markdown note.")
    name_parser.add_argument("--index", type=int, required=True, help="1-based SVG index inside the note.")
    name_parser.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT_ROOT)

    extract_parser = subparsers.add_parser(
        "extract-note",
        help="Export inline SVG blocks from a markdown note into 图片/SVG and replace them with embeds.",
    )
    extract_parser.add_argument("note", type=Path, help="Absolute or relative path to the markdown note.")
    extract_parser.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT_ROOT)
    extract_parser.add_argument("--embed-dir", default=DEFAULT_EMBED_DIR)
    extract_parser.add_argument("--fill", default=DEFAULT_FILL)

    normalize_parser = subparsers.add_parser(
        "normalize-svg",
        help="Ensure one or more SVG files contain the required background rectangle.",
    )
    normalize_parser.add_argument("svg_paths", nargs="+", type=Path)
    normalize_parser.add_argument("--fill", default=DEFAULT_FILL)

    validate_parser = subparsers.add_parser(
        "validate-svg",
        help="Validate SVG XML, required background, and optionally numeric underscore naming.",
    )
    validate_parser.add_argument("svg_paths", nargs="+", type=Path)
    validate_parser.add_argument("--fill", default=DEFAULT_FILL)
    validate_parser.add_argument("--strict-name", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "name-for-note":
            print(file_name_for_note(args.note.resolve(), args.vault_root.resolve(), args.index))
            return 0

        if args.command == "extract-note":
            return extract_note(
                note_path=args.note.resolve(),
                vault_root=args.vault_root.resolve(),
                embed_dir=args.embed_dir,
                fill=args.fill,
            )

        if args.command == "normalize-svg":
            return normalize_svg([path.resolve() for path in args.svg_paths], args.fill)

        if args.command == "validate-svg":
            return validate_svg(
                [path.resolve() for path in args.svg_paths],
                args.fill,
                args.strict_name,
            )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
