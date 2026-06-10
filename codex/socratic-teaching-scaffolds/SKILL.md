---
name: socratic-teaching-scaffolds
description: Guide learners to discover knowledge through Socratic questioning, progressive scaffolding, misconception detection, Feynman explanations, and worked-example fading. Use when teaching complex concepts, correcting misconceptions, mentoring problem solving, designing learning paths, or when the user asks "teach me", "help me understand", "guided discovery", "Socratic method", or equivalent Chinese learning requests.
---

# Socratic Teaching Scaffolds

Use this skill when the goal is durable understanding, not just a polished explanation.

## Core Workflow

1. Diagnose the learner's current model.
2. Design a question ladder from current understanding to target understanding.
3. Guide discovery with purposeful questions and calibrated scaffolding.
4. Fade support as competence grows.
5. Validate transfer with a novel problem or learner explanation.

In ordinary chat, ask one focused question or a small set of diagnostic questions, then wait. When designing a lesson plan or self-study module, provide the full ladder and scaffolding plan.

## When To Read References

- Read [references/template.md](references/template.md) for a structured teaching session, lesson plan, or repeatable coaching format.
- Read [references/methodology.md](references/methodology.md) for complex topics, persistent misconceptions, branching question trees, or multi-session learning paths.
- Read [references/evaluators/rubric_socratic_teaching_scaffolds.json](references/evaluators/rubric_socratic_teaching_scaffolds.json) to self-check a finished teaching plan or session.

## Question Types

- Clarify: "What do you already mean by this term?"
- Probe assumptions: "What would have to be true for that to work?"
- Probe evidence: "How could we test that idea?"
- Explore implications: "What would happen if we changed this part?"
- Reveal contradictions: "If that model is right, what should happen in this case?"
- Build metacognition: "How would you know you understood this?"

Each question must have a job: reveal current thinking, guide a pattern, test an edge case, or validate transfer.

## Scaffolding Levels

| Level | Mode | Use When |
| --- | --- | --- |
| 5 | Full modeling | Learner lacks an entry point; show a complete worked example with thinking aloud |
| 4 | Guided practice | Learner can help complete steps with hints |
| 3 | Coached practice | Learner attempts; intervene with questions when stuck |
| 2 | Independent with feedback | Learner solves first; review after |
| 1 | Transfer | Learner explains, creates examples, or teaches someone else |

Start at the level implied by diagnosis, not Level 5 by default. Move down after success. Move up when struggle becomes frustration.

## Common Teaching Patterns

- Concrete to abstract: familiar example, then pattern, then technical definition.
- Prediction to surprise to explanation: ask for a prediction, reveal a contradiction, guide the corrected model.
- Model to practice to reflect: demonstrate once, coach practice, then ask when the strategy applies or fails.
- Feynman ladder: ELI5, peer-level explanation, technical explanation, then edge cases.
- Worked-example fading: full solution, partial solution, independent attempt, transfer task.

## Guardrails

- Do not turn Socratic teaching into a guessing game. If the learner is stuck, provide a hint, example, or direct explanation.
- Honor sound reasoning even when it takes a different path than expected.
- Make implicit expert steps explicit.
- Use productive struggle, but watch for frustration.
- Correct misconceptions through prediction, contradiction, and reconstruction rather than blunt assertion.
- End with a transfer check or a concrete next practice task when the session is substantial.
