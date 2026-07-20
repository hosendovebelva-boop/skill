# Code panels in step-driven explainers — the canonical spec

> **Scope: this spec applies ONLY to step-driven HTML explainer animations for
> notes (e.g. the Obsidian vault's algorithm / systems-programming animations).**
> It is a genre convention for that artifact type — do NOT impose it on landing
> pages, slide decks, dashboards, posters, or brand work. Those follow their own
> systems (a hero code snippet on a landing page has completely different rules).

Many note explainers embed a small "where does this line live" code sample whose
lines light up as the steps advance. This spec exists because the naive version
fails three ways: the panel balloons to fill its column and scrolls, the
active-line highlight is too faint to see on a dark background, and chained
regex syntax highlighting corrupts its own HTML.

Reference implementation: the demo.cpp panel in
`虚拟地址空间-Section与Segment.html` (Obsidian vault, `1.C++基础/1. 计算机基础/`).

## The rules

### 1. All code visible, zero scrolling

The entire sample must fit without scrolling **on either axis**. This is a hard
requirement — a learner stepping through an animation must never drag a
scrollbar to see the highlighted line.

- Keep the sample short: **≤ ~15 lines**. If the point needs more, trim the
  demo, don't grow the box.
- Compact type: mono **13px**, line-height **~1.55**, line padding `2px 14px`,
  box padding `12px 0`.
- The card **hugs its content**: no `min-height`, no `flex: 1` stretching the
  panel to fill its column. Empty space below the card is fine; a stretched
  half-empty code box is not.
- Verify programmatically: `scrollWidth === clientWidth && scrollHeight === clientHeight`.

### 2. Active-line highlight must be unmissable on the dark background

Light-theme semantic tokens at low alpha (e.g. `rgba(24,95,165,.22)`) disappear
on a dark code background. For each semantic category:

- Background: a **brightened variant of the category hue at ≥ 0.5 alpha**
  (e.g. `.text` blue → `rgba(52,122,198,.52)`).
- Left indicator: **4px inset bar in a bright tint** of the hue (e.g. `#82B4E8`),
  not the dark light-theme token.
- Lighten the highlighted line's text (`#F7F4EA`-ish) and its comment span, so
  the row reads as "lit", not just tinted.

```css
.cl[class*="hl-"]{color:#F7F4EA;}
.cl[class*="hl-"] .cmt{color:#CCC8BA;}
.cl.hl-text{background:rgba(52,122,198,.52);box-shadow:inset 4px 0 0 #82B4E8;}
```

The hue must stay in the same semantic family as the rest of the page (the
`.data` row lights amber because `.data` is amber everywhere else).

### 3. Syntax highlighting: never chain naive regex replaces

The classic bug: after a keyword pass inserts `<span class="kw">`, a later
string-literal pass matches the `"kw"` **inside the tag attribute** and wraps
it, shattering the markup — the panel then renders literal `"kw">` text. This
is invisible until you look at the output.

Safe order — isolate, then highlight, then restore:

```js
// 1. split the trailing comment off first
const m = line.match(/^(.*?)(\/\/.*)?$/);
let code = m[1]; const cmt = m[2] || '';
// 2. park string literals behind digit-free sentinels
const strs = [];
code = code.replace(/"[^"]*"/g, s => {
  strs.push(s);
  return '\u0001' + String.fromCharCode(65 + strs.length - 1) + '\u0001';
});
// 3. now keyword/number passes can't touch strings or span attributes
code = code
  .replace(/\b(int|const|static|return|new|char)\b/g, '<span class="kw">$1</span>')
  .replace(/\b(\d+)\b/g, '<span class="num">$1</span>')
// 4. restore strings, wrapped
  .replace(/\u0001([A-Z])\u0001/g, (_, c) =>
    '<span class="str">' + strs[c.charCodeAt(0) - 65] + '</span>');
const html = code + (cmt ? '<span class="cmt">' + cmt + '</span>' : '');
```

Sentinels must contain **no digits and no word characters the later passes
match** (`\u0001A\u0001` works; `%%0%%` does not — `\b\d\b` eats it). Write the
sentinel as an explicit `\u0001` escape in source, never as a raw control
character (invisible in editors, breaks future edits).

### 4. Line rows are persistent DOM

Same rule as everything else in an explainer (see
[step-animations.md](step-animations.md)): build the line `<div>`s once with
stable ids; each step only swaps highlight classes. Background/color transitions
then tween the highlight from line to line instead of snapping.

### 5. Comments carry the teaching

In a "where does this live" panel, each line's trailing comment names its
destination (`// .data`, `// .bss`, `// .stack`). Align the comment column with
spaces under `white-space: pre` so the destinations read as a table.

## Checklist before shipping an explainer with a code panel

- [ ] Sample ≤ ~15 lines; box hugs content (no min-height / flex stretch)
- [ ] No scrollbar on either axis (`scrollWidth === clientWidth`, `scrollHeight === clientHeight`)
- [ ] Active-line background ≥ 0.5 alpha of a brightened category hue; 4px bright left bar
- [ ] Highlighted line's text and comment are lightened
- [ ] Syntax highlighting uses comment-split + string sentinels — rendered text contains no `"kw">` / `"cmt">` fragments
- [ ] Line rows persist across steps; highlights transition, not snap
