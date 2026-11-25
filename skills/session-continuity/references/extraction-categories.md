# Extraction Categories

Use this as a checklist during Stage 1 (Exhaustive Extraction). For each item, include a short quote or paraphrase from the conversation, and tag confidence (high/medium/low) that it's still relevant and not overruled later.

---

## 1. Goals & Requirements
What the user is trying to achieve overall. Not just the immediate task — the broader objective.

## 2. Explicit Instructions
All "do this", "use that", "output as X", "store in Y" directives. Format, naming, tooling, environment choices.

## 3. Decisions Made
Choices between alternatives. For each:
- What was chosen?
- What was rejected?
- Who decided (user or agent)?
- Why?
- If the user changed their mind: capture the **final** stance, note superseded options.

## 4. Feedback on Outputs
Code, design, text the user reviewed:
- What was approved as-is?
- What was approved with modifications? (Capture the **modified** version, not just the original.)
- What was rejected?

## 5. Constraints & Assumptions
- Anything the agent stated ("I'll use X") — did user confirm or silently agree?
- Implicit technical constraints (must work offline, no external APIs, etc.)
- User opinions expressed as preferences ("I hate X") — these are constraints.

## 6. Output Specifications
Exact format, schema, file names, directory structures, API contracts, key behaviors. Tiny details matter:
- Date formats
- Error message wording
- Field names and casing
- File paths and naming conventions

## 7. Scope & Boundaries
- Explicitly included
- Explicitly excluded
- Marked as "later" or "deferred" (the next agent must NOT implement these)

## 8. Context & Background
Business logic, regulations, user personas, dependencies, prior art.

## 9. External References
Links, docs, threads. Extract the **relevant content**, not just the pointer — the next agent may not have access.

## 10. Priorities & Tone
What matters most, what's flexible, what "nice-to-have" means.

---

## Also Extract (Often Missed)

These don't fit neatly into the categories above but are high-value for the next agent:

- **Learnings** — insights about codebase, architecture, domain discovered during work
- **Quick wins** — low-effort improvements noticed but not yet addressed
- **Dead ends** — what was tried and didn't work, and WHY. This is knowledge, not failure.
- **Gotchas** — non-obvious constraints, surprising behavior, things that broke unexpectedly
- **Working commands** — exact commands that were run and verified (not theoretical)
- **User voice** — the user's actual words on preferences and directives, not paraphrased into generic advice
