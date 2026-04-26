---
name: svg-precision-skill
description: Generate deterministic SVGs from structured specs with validation and rendering. Use for icons, diagrams, charts, UI mockups, and technical drawings.
---

# SVG Precision Skill

Build SVGs from explicit scene specifications, then validate before handing them off.

## Workflow

1. Translate the request into a concrete spec with fixed dimensions and coordinates.
2. Use `references/spec.md` for templates and `references/recipes.md` for stable layout patterns.
3. Build the SVG with `scripts/svg_cli.py build`.
4. Validate with `scripts/svg_cli.py validate`.
5. If the SVG is being produced for an Obsidian note repo or another content repo with local asset rules, read and obey those local instructions before deciding where the SVG lives and how it is embedded.
6. For dense or text-heavy diagrams, inspect the SVG in the target renderer (or from a screenshot) after validation because structural checks do not catch overflow, cramped labels, or marker collisions.
7. Render a PNG preview when the user needs a quick visual check or the target app is not easily inspectable.

## Rules

- Set `viewBox`, width, and height explicitly.
- Prefer absolute coordinates and simple shapes.
- Treat text as risky when exact rendering matters.
- Set an explicit `fontFamily` on text-heavy diagrams to avoid renderer drift and validation warnings.
- For dense diagrams, prefer explicit `lines` over hoping a renderer will wrap long labels well.
- Size node and callout boxes from the text first; widen or heighten the box before shrinking fonts too far.
- Reserve filled arrowheads for the primary flow; use smaller hollow arrowheads for secondary, dashed, or crowded connectors.
- Pull tight connector endpoints back a few pixels so arrow markers do not visually stab into the target border.
- Avoid exotic filters unless they are necessary and testable.

## Obsidian Note Repo Rules

When the output target is an Obsidian vault or markdown note repo, apply these extra rules:

- Check repo-local instructions first. If an `AGENTS.md`, local skill, or note-policy file defines SVG storage or embedding rules, follow that before using a generic default.
- If the local rule says raw `<svg>...</svg>` blocks should be externalized, write each SVG to the repo's designated asset folder and replace the inline block with an Obsidian embed such as `![[name.svg]]`.
- If the repo keeps SVG assets in a dedicated directory such as `图片/SVG/`, use that exact directory instead of leaving SVG files next to the markdown note.
- Match nearby naming patterns instead of inventing a new one. If a note already uses figure names like `9_1_1.svg`, `9_1_2.svg`, continue that numbered sequence.
- If the local rule requires a solid background rectangle, include it explicitly. For repos that specify `fill="rgb(245, 244, 237)"`, place that background rectangle at the start of the SVG content.
- If a local helper skill or script exists for SVG export or background injection, prefer using it. If it is missing, follow the same repo rule manually and say so.
