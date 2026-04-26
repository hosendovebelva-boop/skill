# Recipes (predictable rendering)

## Universal

- Always include `xmlns="http://www.w3.org/2000/svg"` (the builder does this).
- Use `shape-rendering: geometricPrecision` for technical drawings.
- For crisp 1px lines on pixel grids: use integer coords and odd/even stroke widths intentionally.
- Prefer `fill="none"` on stroked shapes to avoid accidental fills.

## Icons

- Default canvas: 24x24 viewBox.
- Stroke-based: `strokeLinecap: round`, `strokeLinejoin: round`, `strokeWidth: 2`.
- Avoid filters; keep paths simple; expand strokes only if a consumer requires it.

## Diagrams / Flowcharts

- Use a marker arrow in defs; connect shapes using `line` or `path`.
- Group each node: background shape + label text in a `group`.
- Keep consistent padding: 16-24px inside nodes.
- Route edges orthogonally when readability matters (use `path` with `M L L` segments).
- Split long labels with explicit `lines`; CJK text and note-sized diagrams overflow sooner than slide-sized graphics.
- Size nodes and callouts from content first; add width or height before reducing font size.
- Use filled arrowheads for the main sequence only; smaller hollow arrowheads read better for side notes, dashed connectors, and tight callouts.
- Stop crowded connectors a few pixels before the target edge so the arrowhead remains visible without touching the box stroke.
- After `validate`, inspect the SVG at the real consumption size in the target renderer because validator success does not guarantee comfortable spacing.

## Dense Note Diagrams

- Treat note diagrams like constrained UI layouts rather than presentation slides: space is tight and labels are often longer.
- Keep the main flow on one stable axis and push diagnostics, caveats, or fix notes into lighter side columns.
- Use visual semantics consistently: strong fill + solid arrow for primary flow, lighter box + dashed line + hollow arrow for secondary commentary.
- Prefer a little more height and whitespace over squeezing many competing annotations into the same row.

## Charts

- Build chart area first (axes box), then plot area, then labels.
- Reserve margins (e.g., left 80, bottom 60, right 40, top 40) so labels never clip.
- Snap bars/points to integers; round tick labels; keep gridlines light.

## UI mockups

- Start with a background rect (page) and a 8pt grid.
- Use large corner radii (16-24) for modern cards.
- Keep text styles consistent: titles 24-32, body 14-16.
- Shadows vary across renderers; prefer subtle strokes unless the shadow is essential.

## Technical drawings

- Specify units in `canvas.units` and include scale in metadata.
- Use thin strokes (0.5-1.5) and set `vector-effect: non-scaling-stroke` when scaling output.
- Dimensions: extension lines + dimension line + arrow markers + centered label.
- Add centerlines / dashed lines with `strokeDasharray`.
