#!/usr/bin/env python3
"""Validate SVG output against the obsidian-svg design system."""

from __future__ import annotations

import math
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


APPROVED_COLORS = {
    "#E6F1FB",
    "#185FA5",
    "#0C447C",
    "#EEEDFE",
    "#534AB7",
    "#3C3489",
    "#E1F5EE",
    "#0F6E56",
    "#085041",
    "#FAEEDA",
    "#854F0B",
    "#633806",
    "#F1EFE8",
    "#5F5E5A",
    "#444441",
}

SPECIAL_COLOR_VALUES = {
    "none",
    "context-stroke",
    "currentcolor",
    "transparent",
    "inherit",
}

BACKGROUND_FILL = "rgb(245, 244, 237)"
TEXT_APPROX_WIDTH = 8.0
TEXT_HORIZONTAL_PADDING = 48.0
REQUIRED_RECT_RX = 8.0
REQUIRED_RECT_STROKE_WIDTH = 0.5
REQUIRED_ARROW_STROKE_WIDTH = 1.5
MIN_BOX_GAP = 60.0
MIN_BOTTOM_PADDING = 40.0
FLOAT_TOLERANCE = 1e-6


@dataclass
class Rect:
    x: float
    y: float
    width: float
    height: float
    element: ET.Element

    @property
    def right(self) -> float:
        return self.x + self.width

    @property
    def bottom(self) -> float:
        return self.y + self.height


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def parse_float(value: str | None, default: float | None = None) -> float | None:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def parse_viewbox(value: str) -> tuple[float, float, float, float] | None:
    parts = value.replace(",", " ").split()
    if len(parts) != 4:
        return None
    try:
        return tuple(float(part) for part in parts)
    except ValueError:
        return None


def normalize_color(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    if value.startswith("#"):
        return value.upper()
    rgb_match = re.fullmatch(
        r"rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)",
        value,
        re.IGNORECASE,
    )
    if rgb_match:
        red, green, blue = (int(part) for part in rgb_match.groups())
        return f"rgb({red}, {green}, {blue})"
    return value.lower()


def parse_style(style_value: str | None) -> dict[str, str]:
    result: dict[str, str] = {}
    if not style_value:
        return result
    for chunk in style_value.split(";"):
        if ":" not in chunk:
            continue
        key, value = chunk.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def get_attr(elem: ET.Element, key: str) -> str | None:
    if key in elem.attrib:
        return elem.attrib[key]
    return parse_style(elem.attrib.get("style")).get(key)


def is_close(value: float | None, expected: float) -> bool:
    return value is not None and abs(value - expected) <= FLOAT_TOLERANCE


def is_background_rect(
    elem: ET.Element, svg_root: ET.Element, viewbox: tuple[float, float, float, float]
) -> bool:
    if local_name(elem.tag) != "rect":
        return False
    if elem not in list(svg_root):
        return False
    vb_x, vb_y, vb_width, vb_height = viewbox
    return (
        is_close(parse_float(get_attr(elem, "x"), 0.0), vb_x)
        and is_close(parse_float(get_attr(elem, "y"), 0.0), vb_y)
        and is_close(parse_float(get_attr(elem, "width")), vb_width)
        and is_close(parse_float(get_attr(elem, "height")), vb_height)
        and normalize_color(get_attr(elem, "fill")) == BACKGROUND_FILL
    )


def read_svg(source: str) -> str:
    if source == "-":
        data = sys.stdin.read()
        if not data.strip():
            raise ValueError("stdin is empty")
        return data
    path = Path(source)
    return path.read_text(encoding="utf-8")


def rect_distance(first: Rect, second: Rect) -> float:
    dx = max(0.0, max(first.x, second.x) - min(first.right, second.right))
    dy = max(0.0, max(first.y, second.y) - min(first.bottom, second.bottom))
    if dx > 0.0 and dy > 0.0:
        return math.hypot(dx, dy)
    return max(dx, dy)


def text_content(elem: ET.Element) -> str:
    parts = [text.strip() for text in elem.itertext() if text and text.strip()]
    return "".join(parts)


def validate_svg_text(svg_text: str) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        return [f"invalid XML: {exc}"]

    if local_name(root.tag) != "svg":
        errors.append("root element must be <svg>")
        return errors

    viewbox_raw = root.attrib.get("viewBox")
    if not viewbox_raw:
        errors.append("missing viewBox")
        return errors

    viewbox = parse_viewbox(viewbox_raw)
    if viewbox is None:
        errors.append("viewBox must contain four numeric values")
        return errors

    vb_x, vb_y, vb_width, vb_height = viewbox
    vb_bottom = vb_y + vb_height

    all_elements = list(root.iter())
    rects: list[Rect] = []
    marker_refs: list[ET.Element] = []
    background_rects = [
        elem for elem in all_elements if is_background_rect(elem, root, viewbox)
    ]

    if not background_rects:
        errors.append(
            f'missing top-level background rect with fill="{BACKGROUND_FILL}" sized to the viewBox'
        )
    else:
        root_children = list(root)
        first_graphic = next(
            (
                child
                for child in root_children
                if local_name(child.tag) not in {"defs", "title", "desc", "metadata"}
            ),
            None,
        )
        if first_graphic is not background_rects[0]:
            errors.append("background rect must appear before foreground content")

    for elem in all_elements:
        tag = local_name(elem.tag)

        for attr_name in ("fill", "stroke"):
            color = normalize_color(get_attr(elem, attr_name))
            if (
                color
                and color not in APPROVED_COLORS
                and color not in SPECIAL_COLOR_VALUES
                and color != BACKGROUND_FILL
            ):
                errors.append(
                    f"{tag} uses unapproved {attr_name} color {get_attr(elem, attr_name)!r}"
                )

        if tag == "rect":
            if is_background_rect(elem, root, viewbox):
                continue
            x = parse_float(get_attr(elem, "x"), 0.0)
            y = parse_float(get_attr(elem, "y"), 0.0)
            width = parse_float(get_attr(elem, "width"))
            height = parse_float(get_attr(elem, "height"))
            rx = parse_float(get_attr(elem, "rx"))
            stroke_width = parse_float(get_attr(elem, "stroke-width"))
            if width is None or height is None:
                errors.append("rect is missing numeric width/height")
            else:
                rects.append(Rect(x or 0.0, y or 0.0, width, height, elem))
            if not is_close(rx, REQUIRED_RECT_RX):
                errors.append("rect is missing rx=\"8\"")
            if not is_close(stroke_width, REQUIRED_RECT_STROKE_WIDTH):
                errors.append("rect must use stroke-width=\"0.5\"")

        if tag == "text":
            if get_attr(elem, "dominant-baseline") != "central":
                errors.append("text is missing dominant-baseline=\"central\"")

        if get_attr(elem, "marker-end"):
            marker_refs.append(elem)
            if get_attr(elem, "marker-end") != "url(#arrow)":
                errors.append("arrow marker-end must be url(#arrow)")
            stroke_width = parse_float(get_attr(elem, "stroke-width"))
            if not is_close(stroke_width, REQUIRED_ARROW_STROKE_WIDTH):
                errors.append("arrows must use stroke-width=\"1.5\"")

    if marker_refs:
        marker_ids = {
            elem.attrib.get("id")
            for elem in all_elements
            if local_name(elem.tag) == "marker" and elem.attrib.get("id")
        }
        if "arrow" not in marker_ids:
            errors.append("missing <marker id=\"arrow\"> definition")

    for group in all_elements:
        if local_name(group.tag) != "g":
            continue
        group_rects = [elem for elem in group if local_name(elem.tag) == "rect"]
        if len(group_rects) != 1:
            continue
        rect_elem = group_rects[0]
        width = parse_float(get_attr(rect_elem, "width"))
        if width is None:
            continue
        text_elems = [elem for elem in group.iter() if local_name(elem.tag) == "text"]
        if not text_elems:
            continue
        longest = max((len(text_content(elem)) for elem in text_elems), default=0)
        required_width = longest * TEXT_APPROX_WIDTH + TEXT_HORIZONTAL_PADDING
        if width + FLOAT_TOLERANCE < required_width:
            errors.append(
                f"rect at ({get_attr(rect_elem, 'x')}, {get_attr(rect_elem, 'y')}) is too narrow "
                f"for its text ({width:g} < {required_width:g})"
            )

    for index, first in enumerate(rects):
        for second in rects[index + 1 :]:
            if rect_distance(first, second) + FLOAT_TOLERANCE < MIN_BOX_GAP:
                errors.append(
                    "rect gaps must be at least 60px "
                    f"(found {rect_distance(first, second):.2f}px)"
                )

    max_bottom = 0.0
    for rect in rects:
        max_bottom = max(max_bottom, rect.bottom)
    for elem in all_elements:
        if local_name(elem.tag) == "text":
            y = parse_float(get_attr(elem, "y"))
            if y is not None:
                max_bottom = max(max_bottom, y)

    if vb_bottom + FLOAT_TOLERANCE < max_bottom + MIN_BOTTOM_PADDING:
        errors.append(
            "viewBox bottom padding is too small "
            f"({vb_bottom:g} < {max_bottom + MIN_BOTTOM_PADDING:g})"
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python validate_svg.py <svg-path-or->")
        return 1

    source = sys.argv[1]
    try:
        svg_text = read_svg(source)
    except OSError as exc:
        print(f"Failed to read SVG: {exc}")
        return 1
    except ValueError as exc:
        print(f"Failed to read SVG: {exc}")
        return 1

    errors = validate_svg_text(svg_text)
    if errors:
        print("SVG validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("SVG validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
