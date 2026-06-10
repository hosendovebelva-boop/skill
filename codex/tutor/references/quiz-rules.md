# Quiz Design Rules

Read this before creating any quiz question.

## Zero-Hint Policy

Every question must be answerable only by someone who knows the material.

1. Do not reveal correctness in option labels or descriptions.
2. Do not mark any option as recommended.
3. Randomize correct answer positions.
4. Ask about behavior, purpose, output, cause, or distinction without smuggling in the answer.
5. Use plausible distractors from the same domain. Wrong answers should represent common misconceptions.

Bad:

```text
A. stderr - Error output stream used by this API for classification
```

Good:

```text
A. stderr - Standard error stream
```

## Codex Interaction Rule

Some Codex input tools force a recommended option or allow fewer than 4 choices. Do not use those tools for quiz questions. Present neutral numbered choices in normal chat and wait for the user's answer.

## Question Types

- Factual recall: definitions, names, return values.
- Conceptual understanding: why a pattern or rule exists.
- Behavioral prediction: what happens when code or a system runs.
- Comparison: distinguish similar concepts.
- Debugging scenario: infer likely cause from symptoms.

## Difficulty Balance

- Diagnostic: 40% easy, 40% medium, 20% hard.
- Weak-area drill: 30% medium, 70% hard.
- Review: balanced across easy, medium, and hard.

## Drilling Unresolved Concepts

When targeting unresolved concepts from concept files:

- Do not repeat the exact old question.
- Test the same knowledge from a new angle.
- Prefer scenario questions that reveal whether the misconception is gone.

## Round Format

- 4 questions per round.
- 4 options per question.
- Single-select answers.
- Neutral labels such as A, B, C, D.
- Ask the user to reply in a compact format such as `1A 2C 3B 4D`.

## File Update Protocol

After grading:

1. Update `concepts/{area}.md` rows and error notes.
2. Recalculate the dashboard from concept files.
3. Use existing dashboard status labels if present. For new dashboards, use `Weak`, `Fair`, `Good`, `Mastered`, and `Unmeasured`.

Suggested thresholds:

- Weak: 0-39%
- Fair: 40-69%
- Good: 70-89%
- Mastered: 90-100%
- Unmeasured: no data

## Language Rule

All output and newly created tracking content must use the user's detected language. Preserve existing file language and status labels when updating old files.
