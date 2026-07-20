# Step-driven explainer animations (transition quality)

For **step-through / state-machine explainers** — algorithm walkthroughs, data-structure diagrams, "how X works" pieces driven by prev / next / play over a list of discrete states. This is a *different genre* from timeline/video motion (Stage + Sprite); the rules below are what make it feel smooth instead of janky.

## The one rule that matters: animate by mutation, not rebuild

**Build the DOM once. On each step, mutate the existing elements in place** (set `className` / `style` / `textContent` on nodes with stable ids). **Never** rebuild the view with `container.innerHTML = render(state)` on every step.

Why this is the whole ballgame: CSS `transition` animates a property *changing on an element that stays alive*. If you replace innerHTML each step, every element is destroyed and recreated — so the browser has nothing to transition *from*. Your `transition: all .5s` is dead code; the UI snaps between states. This is the #1 defect in hand-written explainer animations, and it's invisible in the source (the CSS looks correct).

```js
// ❌ transitions never run — elements are new every step, so they snap
function render(state){ container.innerHTML = state.cells.map(c => `<div class="cell ${c.cls}">${c.v}</div>`).join(''); }

// ✅ build once, then only mutate — CSS transitions actually fire
function build(){ container.innerHTML = values.map((v,i)=>`<div class="cell" id="c${i}">${v}</div>`).join(''); }
function render(state){ state.cells.forEach((c,i)=>{ document.getElementById('c'+i).className = 'cell '+c.cls; }); }
```

Engine shape: each scene exposes `build()` (create persistent nodes with stable ids, run once when the scene mounts) and `render(state)` (mutate those nodes). The step engine calls `build` on scene switch and `render` on every step change. Keyframe `@keyframes` animations *do* run on freshly-inserted nodes, so one-shot "pop/flash" effects can still use a rebuilt sub-region — but anything that should *tween* between two states (colour, position, size, opacity) must be a persistent element whose property you change.

## Transition techniques that read well

- **Sliding pointers/labels** (`i`, `l`/`r`, `slow`/`fast`, `prev`/`curr`): one absolutely-positioned badge per pointer; each step set its `left` (px, from the target cell's `offsetLeft + offsetWidth/2`) with `transition: left …`. It glides to the new cell instead of teleporting — this is what makes a pointer walk legible.
- **Redirected links / "this pointer just changed"** (linked lists, trees): keep one SVG `<path>` per edge; on the step where an edge changes, update its `d` and replay a draw-in via `stroke-dashoffset` (measure `getTotalLength()`, set dasharray+offset to length, force reflow, transition offset to 0). Draws the eye to the *one* thing that changed.
- **Bars / magnitudes** (sorting, prefix sums, histograms): persistent bar divs; change `height` with a `height` transition. A swap becomes two bars trading heights — the motion *is* the explanation.
- **Re-triggering a keyframe on a persistent node**: `el.classList.remove('pop'); void el.offsetWidth; el.classList.add('pop');` (the reflow restarts the animation).
- **Region fills** (2D grids, inclusion-exclusion, windows): tint cells by set membership and let `transition: background/border` fade regions in and out as the set changes step to step.

## Also part of "polished", not just correct

- **Separate the action from the explanation.** Give each step a one-line `▸ 本步动作 / ▸ what this step does` line (monospace chip) above the prose paragraph. The learner reads the action; the paragraph is there if they want depth.
- **Commit to one visual system across a series.** Shared tokens (palette, `--ease`, `--dur`), one card/tab/control chrome, soft shadows, consistent radii. If you're making several animations, they should look like one product.
- **Honour reduced motion:** `@media (prefers-reduced-motion: reduce){ *{transition-duration:1ms!important;animation-duration:1ms!important;} }`.
- **Keep controls reachable:** prev / play-pause / next, step dots, `←`/`→`/space keyboard nav, a step readout.
- **Connector lines/arrows between boxes** (mappings, flow edges) follow the arrow spec — small filled-triangle heads, staggered fan-in, draw-in via `stroke-dashoffset`. See [connector-arrows.md](connector-arrows.md).
- **Embedded code panels** (line-by-line "where does this live" samples) follow the code-panel spec — all code visible with zero scrolling, ≥0.5-alpha active-line highlight on dark backgrounds, sentinel-based syntax highlighting. See [code-panels.md](code-panels.md).

## Benchmark

Reference implementation (local vault): `<OBSIDIAN_VAULT>/5.算法/5.2 算法/5.2.2.1 位运算动画.html` — 6 bit-manipulation scenes, persistent-DOM engine, per-step `▸` action line, warm-paper token system. The sibling family `5.2.4.1`–`5.2.9.1` (prefix sum, sorting, binary search, two-pointer, hashing, linked list) applies the same engine; `5.2.4.1 前缀和动画.html` is the transition showcase (2D inclusion-exclusion region fades, diff bars rising via `height`).

Match that bar: real tweened transitions, sliding pointers, one coherent token system, an action line per step.

## Checklist before calling a step animation done

- [ ] DOM is built once; steps only mutate (no per-step `innerHTML =` on the animated region)
- [ ] At least one property genuinely *tweens* between steps (colour / position / size), verified by eye — not a snap
- [ ] Pointers/labels slide to their new position rather than teleporting
- [ ] Each step has a one-line action summary distinct from the explanation
- [ ] prev / play / next + dots + keyboard nav all work; last step stops the player
- [ ] `prefers-reduced-motion` respected
