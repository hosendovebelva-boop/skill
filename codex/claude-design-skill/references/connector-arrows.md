# Connector arrows — the canonical spec

> **Scope: this spec applies ONLY to step-driven HTML explainer animations for
> notes (e.g. the Obsidian vault's algorithm / systems-programming animations).**
> It is a genre convention for that artifact type — do NOT impose it on landing
> pages, slide decks, posters, dashboards, or brand work. Those choose their own
> connector language (or none at all).

Within that genre: whenever a diagram connects boxes/nodes with SVG lines and arrowheads (mapping diagrams, flowcharts, architecture views inside an explainer), follow this spec exactly. It exists because the naive approach — big hollow chevrons drawn as strokes, thick lines with drop-shadows, endpoints that pile onto the same point — reads as hand-drawn scribble the moment two connectors converge on one target.

Reference implementation: the Section → Segment wires in
`虚拟地址空间-Section与Segment.html` (Obsidian vault, `1.C++基础/1. 计算机基础/`).

## The rules

### 1. Arrowhead: small filled triangle, never a stroked chevron

- Filled triangle, **~9px long × 10px wide** (`aw = 9`, `ah = 5`), `fill` = the connector's color, `stroke: none`.
- Never draw arrowheads as open chevrons with `stroke` — at 2.5px+ stroke weight they balloon to 20px+ and visually collide with anything nearby.
- The triangle is part of the connector: same semantic color, fades with the line.

```js
// tip flush against the target box (see rule 3)
const dArr = `M ${tipX} ${tipY} L ${tipX - 9} ${tipY - 5} L ${tipX - 9} ${tipY + 5} Z`;
```

### 2. Line: cubic Bézier with horizontal tangents, quiet weights

- Path: `M x1 y1 C W*0.45 y1, W*0.55 y2, x2 y2` — both ends leave/arrive horizontally, so the arrowhead can always point straight at the target edge.
- Idle/hint state: `stroke-width: 2`, `opacity: ~0.1` (visible as a whisper, not a distraction).
- Active state: `stroke-width: 3`, full semantic color. **No drop-shadow, no glow, never 4px+.**
- Source end gets a small port circle (`r ≈ 4`), panel-background fill, colored stroke.

### 3. The tip must touch the target

A connector that stops 10px short of its target box reads as floating decoration. Set the SVG container to `overflow: visible` and extend the tip through any grid gap so the triangle's point lands on (or 1–2px from) the target's border.

```js
const x2 = W - 1;          // line ends at container edge
const tipX = x2 + 9;       // triangle reaches into the grid gap to the card border
```

### 4. Fan-in: stagger endpoints ≥ 18–20px

When N connectors converge on one target, never let them share an endpoint — the arrowheads overlap and cross. Spread the arrival points vertically around the target's center:

```js
const ySpread = (slot - (total - 1) / 2) * 20;   // 20px per slot, centered
const y2 = targetCenterY + ySpread;
```

Count slots per target *before* laying out, then assign in order. With one connector the offset is 0 (dead center) automatically.

### 5. Motion: draw-in on persistent DOM

Connectors follow the build-once + mutate rule (see [step-animations.md](step-animations.md)):

- Create every `<path>`/`<circle>` once with stable ids; steps only toggle classes and update attributes.
- On activation, animate the line drawing from source to target via `stroke-dasharray`/`stroke-dashoffset` (duration ≈ 520ms). **Clear the dasharray after the animation** — a stale dasharray leaves gaps after resize changes the path length.
- The arrowhead fades in with a **~200ms transition-delay** so it appears as the line arrives, not before.
- Turning off is a plain opacity fade — no reverse draw.

```js
function drawIn(path) {
  const L = path.getTotalLength();
  path.style.transition = 'none';
  path.style.strokeDasharray = L;
  path.style.strokeDashoffset = L;
  void path.getBoundingClientRect();          // force reflow
  path.style.transition = '';
  path.style.strokeDashoffset = '0';
  clearTimeout(path._t);
  path._t = setTimeout(() => {
    path.style.strokeDasharray = '';
    path.style.strokeDashoffset = '';
  }, 560);
}
```

Track what is currently lit (a `Set`) and only run `drawIn` on off→on transitions — re-running it on every step repaint makes already-lit lines flicker.

### 6. Focus: hide inactive connectors completely

When any connector is active, inactive ones go to `opacity: 0` — not a faint gray. Half-visible idle lines behind active ones read as noise. When *nothing* is active (overview state), all connectors may sit at the ~0.1 hint opacity.

### 7. CSS hygiene: arrowheads are `<path>` too

A selector like `.wire-svg path.on { stroke-width: 3 }` also matches the arrowhead path and gives the filled triangle an unwanted outline. Isolate line rules from arrow rules:

```css
.wire-svg path.on:not(.arrow) { opacity: 1; stroke-width: 3; }
.wire-svg .arrow { fill: var(--line); stroke: none; }
.wire-svg .arrow.on { opacity: 1; transition-delay: 200ms; }
```

### 8. Layout is computed, not hardcoded

Compute endpoints from `getBoundingClientRect()` of the actual source/target elements relative to the SVG container, re-run on `resize`, and set the `viewBox` to the container's live pixel size. Hardcoded coordinates drift the first time content wraps differently.

## Checklist before shipping a diagram with connectors

- [ ] Arrowheads are small filled triangles (≤ 10px), colored like their line
- [ ] Tips touch the target boxes (no floating gap)
- [ ] Converging connectors staggered ≥ 18px — no overlapping/crossing heads
- [ ] Active weight 3px, no drop-shadow; idle is a ~0.1-opacity hint
- [ ] Draw-in animates `stroke-dashoffset` on persistent DOM; dasharray cleared afterward
- [ ] Arrowhead appears with a short delay, as the line arrives
- [ ] Line CSS rules exclude `.arrow` paths
- [ ] Geometry recomputed on resize from real element rects
