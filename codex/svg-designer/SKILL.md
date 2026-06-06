---
name: svg-designer
description: Create polished SVG diagrams for architecture diagrams, flowcharts, concept maps, comparison diagrams, and other visual explanations. Use when the user asks for an SVG diagram, block diagram, component layout, labeled comparison figure, or a visually refined illustration. For sequence-heavy, thread-call, request-response, callback-order, and timing-order explanations, prefer Mermaid instead of forcing SVG.
---

# SVG Designer

Use this skill to produce polished diagrams with a consistent visual system. Default visible labels to Chinese, but keep API names, class names, function names, filenames, protocol names, and other literal identifiers in their source language.

For Obsidian use, make SVG backgrounds explicit instead of transparent. By default every SVG must include a solid top-level background rectangle filled with `rgb(245, 244, 237)` so the diagram remains readable in both light and dark mode. Only skip the background if the user explicitly asks for transparency.

## Medium Routing

Choose the diagram medium before drafting content.

- Use SVG for static architecture, layered structure, component grouping, side-by-side comparison, fixed-layout mechanism summaries, concept maps, and visually rich block layouts.
- Use Mermaid for sequence diagrams, thread call chains, callback order, request-response choreography, startup or shutdown order, and timing-heavy logic.
- Only force a sequence-style diagram into SVG if the user explicitly asks for SVG.

## Workflow

1. Normalize visible labels to Chinese by default. Translate semantic labels, legends, subtitles, and connector text, but do not awkwardly translate code tokens or protocol terms.
2. Plan the layout silently. Do not print the layout plan or self-critique unless the user explicitly asks for them.
3. Generate SVG or Mermaid.
4. If the output is SVG, add a full-canvas background rectangle near the top of the SVG. Match the `viewBox` bounds and fill it with `rgb(245, 244, 237)`.
5. Validate the result before returning it. If the output is SVG, run `python "C:\Users\Administrator\.codex\skills\svg-designer\scripts\validate_svg.py" <svg-path>` or pipe the SVG into `python "C:\Users\Administrator\.codex\skills\svg-designer\scripts\validate_svg.py" -`.
6. Revise until the diagram passes the rules below.

## Output Contract

- If the user requests inline output, return only the final diagram block.
- If the user provides an output path, write the diagram to that path instead of only describing it.
- If Mermaid is the better fit, return Mermaid instead of forcing SVG.
- Do not append process commentary after the final diagram block unless the user asks for explanation.

## SVG Design System

### Color Ramps

Use only these node colors:

- Blue: fill `#E6F1FB`, stroke `#185FA5`, text `#0C447C`
- Purple: fill `#EEEDFE`, stroke `#534AB7`, text `#3C3489`
- Teal: fill `#E1F5EE`, stroke `#0F6E56`, text `#085041`
- Amber: fill `#FAEEDA`, stroke `#854F0B`, text `#633806`
- Gray: fill `#F1EFE8`, stroke `#5F5E5A`, text `#444441`

Use multiple ramps across a diagram unless the user explicitly wants a monochrome result.

### Typography

- Primary label: `font-family="system-ui,sans-serif" font-size="14" font-weight="500"`
- Secondary label: `font-family="system-ui,sans-serif" font-size="12" font-weight="400"`
- Add `dominant-baseline="central"` to every `<text>` element.
- Use `text-anchor="middle"` unless left alignment is genuinely needed.

### Layout Rules

- Minimum box width: `longest_label_chars x 8 + 48`
- Single-line box height: `44`
- Two-line box height: `56`
- Minimum gap between boxes: `60`
- Box corner radius: `rx="8"`
- Box stroke width: `0.5`
- Arrow stroke width: `1.5`
- ViewBox height: `max_element_bottom + 40`
- Keep at least `20` px padding on each side

### Background Rule

- Every SVG must include a top-level background rectangle sized to the `viewBox`.
- Use `fill="rgb(245, 244, 237)"`.
- Place the background before foreground nodes so it does not cover the diagram.
- Do not leave SVG output transparent unless the user explicitly asks for transparency.

### Required Arrow Marker

Include this marker in SVG output whenever the diagram uses arrows:

```xml
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5"
          markerWidth="6" markerHeight="6" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke"
          stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
</defs>
```

Reference arrows with `marker-end="url(#arrow)"`.

## SVG Validation Checklist

Before returning SVG, confirm all of the following:

- A top-level background rectangle exists and uses `rgb(245, 244, 237)`.
- Arrow definitions are present when arrows use `marker-end`.
- All fills, strokes, and text colors come from the approved ramps, except `none` and `context-stroke`.
- No label obviously overflows its box width rule.
- All node rectangles use `rx="8"` and `stroke-width="0.5"`.
- All arrows use `stroke-width="1.5"`.
- Every `<text>` includes `dominant-baseline="central"`.
- Box spacing is at least `60`.
- The `viewBox` bottom padding is at least `40`.
- The SVG is complete and valid XML.

## Quick Commands

Validate an SVG file:

```powershell
python "C:\Users\Administrator\.codex\skills\svg-designer\scripts\validate_svg.py" "D:\path\to\diagram.svg"
```

Validate SVG from stdin:

```powershell
Get-Content "D:\path\to\diagram.svg" | python "C:\Users\Administrator\.codex\skills\svg-designer\scripts\validate_svg.py" -
```
