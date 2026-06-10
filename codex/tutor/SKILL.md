---
name: tutor
description: Run interactive StudyVault quiz tutoring for Obsidian-style learning: discover a StudyVault, diagnose knowledge, quiz specific sections, drill weak concepts, grade answers, and update concept tracking files. Use when the user wants a diagnostic assessment, study session, review, weak-area drill, progress check, "quiz me", "test me", "let's study", "/tutor", or equivalent Chinese study requests.
---

# Tutor

Use this skill as a quiz tutor that tracks knowledge at the concept level. The goal is to expose blind spots, explain mistakes, and keep a compact dashboard current.

## Required Behavior

- Detect the user's language and use it for all user-facing output and newly created file content.
- Preserve existing StudyVault paths, filenames, language, and dashboard conventions when found.
- Ask before choosing a session type. In Codex, present concise numbered choices in normal chat and wait for the user; do not use tools that force recommended choices for quiz options.
- Read [references/quiz-rules.md](references/quiz-rules.md) before writing any quiz question.
- Ask exactly 4 multiple-choice questions per round, with 4 plausible options each.
- Never include hints in option labels or descriptions.
- After grading, update both the relevant concept file(s) and the dashboard.

## Workflow

### Phase 0: Detect Language

Infer the language from the user's latest message. If mixed, prefer the language the user used for the request.

### Phase 1: Discover StudyVault

1. Search the current project or vault for `StudyVault/`.
2. List available section directories or markdown sections.
3. Search for a compact dashboard file such as `*dashboard*`.
4. If a dashboard exists, read it and preserve its path.
5. If StudyVault exists but no dashboard exists, create one from the template below.
6. If no StudyVault exists, report that and stop. Ask for the vault path only if discovery cannot find it.

### Phase 2: Ask Session Type

Analyze the dashboard and offer context-aware choices:

- Diagnostic: for unmeasured areas.
- Drill weak areas: for areas with low accuracy or unresolved concepts.
- Choose a section: always include this.
- Hard-mode review: include when all measured areas are strong.

Wait for the user's choice before reading source notes and building questions.

### Phase 3: Build Questions

1. Read the markdown notes in the selected section(s).
2. For weak-area drills, also read `concepts/{area}.md` and target unresolved or low-confidence concepts.
3. Read [references/quiz-rules.md](references/quiz-rules.md).
4. Create exactly 4 questions using the zero-hint rules.

### Phase 4: Present Quiz

Present all 4 questions in one message unless the user asks for one-at-a-time mode. Use neutral numbered options. Ask the user to reply with answers such as `1A 2C 3B 4D`.

### Phase 5: Grade And Explain

Show a compact results table with question, correct answer, user answer, and result. For wrong answers, explain the misconception and the correct model briefly. Map every question to its area and concept.

### Phase 6: Update Tracking Files

Update `concepts/{area}.md`:

- New concept: add a row; if wrong, add an error note.
- Existing unresolved concept answered correctly: increment attempts and correct count; mark resolved.
- Existing resolved concept answered wrong: increment attempts; mark unresolved again; update the error note.

Update the dashboard by recalculating from concept files:

- Per-area correct, wrong, rate, and level.
- Total questions and cumulative rate.
- Unresolved and resolved concept counts.
- Weakest and strongest areas.

Keep the dashboard compact. Store per-concept details only in concept files.

## Dashboard Template

```markdown
# Learning Dashboard

> Concept-based metacognition tracking. See linked files for details.

## Proficiency by Area

| Area | Correct | Wrong | Rate | Level | Details |
| --- | ---: | ---: | ---: | --- | --- |
| **Total** | **0** | **0** | **-** | Unmeasured | |

## Stats

- **Total Questions**: 0
- **Cumulative Rate**: -
- **Unresolved Concepts**: 0
- **Resolved Concepts**: 0
- **Weakest Area**: -
- **Strongest Area**: -
```

## Concept File Template

```markdown
# {Area Name} - Concept Tracker

| Concept | Attempts | Correct | Last Tested | Status |
| --- | ---: | ---: | --- | --- |

## Error Notes

(Add notes only for missed concepts.)
```
