---
name: concept-explainer
description: Explain difficult or unfamiliar concepts with adjustable depth, ELI5-style simplification, analogies, examples, misconceptions, and related concepts. Use when the user asks to explain, simplify, define, compare, clarify, "what is", "how does", "why does", "ELI5", "analogy for", or equivalent Chinese learning requests.
---

# Concept Explainer

Use this skill to make a concept feel understandable without flattening it into a misleading simplification.

## Quick Workflow

1. Infer the learner level from the request. If the level is unclear, start at a practical beginner or high-school level and offer to go deeper.
2. Give a one-sentence definition before details.
3. Build one strong analogy or visual model.
4. Explain how it actually works with accurate terminology.
5. Add 2-3 examples at increasing difficulty.
6. Name common misconceptions and correct them.
7. Connect the concept to nearby ideas when useful.

For a small question, use only the needed subset. For a study request, use the full structure.

## Depth Levels

| Level | Use For | Style |
| --- | --- | --- |
| ELI5 | Complete beginner | Everyday words, one core analogy, no jargon |
| High school | Some background | Basic terms, concrete examples, clear cause and effect |
| Undergraduate | Foundational knowledge | Technical vocabulary, mechanisms, formulas when useful |
| Graduate | Advanced learner | Assumptions, edge cases, limitations, research context |

## Explanation Template

```markdown
## In One Sentence
[Concept] is [simple definition] that [what it does or why it matters].

## Intuition
Think of it like [familiar thing]. Just as [familiar thing does X], [concept] does Y.

## How It Works
[Accurate explanation with the right terms, introduced gently.]

## Examples
1. Simple: [everyday or toy example]
2. Applied: [real use case]
3. Deeper: [edge case or more technical case]

## Common Misconceptions
- Myth: [wrong belief]
  Reality: [correct model]

## Related Concepts
- [Concept A]: [relationship]
```

## Analogy Patterns

- Structure analogy: Map components of the concept to parts of a familiar object.
- Process analogy: Map the steps of the concept to a familiar process.
- Scale analogy: Use size, time, or quantity comparisons when raw numbers are hard to feel.
- Contrast analogy: Explain what the concept is not, especially when two ideas are often confused.

Never let an analogy quietly become the explanation. State where the analogy breaks.

## Quality Checks

- Start simple, then add precision.
- Define each new technical term the first time it appears.
- Use examples that test the core idea, not decorative examples.
- Address at least one likely misconception for non-trivial concepts.
- Prefer clarity over breadth; do not introduce adjacent topics unless they reduce confusion.
