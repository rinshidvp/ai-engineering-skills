# Domain Modeling (Glossary & ADRs)

Actively sharpen the project's shared language and record hard-to-reverse decisions as they crystallize during discovery. Create files **lazily** — only when you actually have a first term or decision to write.

## File layout

Single-context repo (most projects):
```
/
├── GLOSSARY.md
└── docs/
    └── adr/
        └── 0001-short-slug.md
```

If `GLOSSARY-MAP.md` exists at the repo root, the repo has multiple bounded contexts; follow the map to the relevant context's `GLOSSARY.md` and `docs/adr/`.

## During discovery

1. **Challenge conflicts:** If the user uses a term that conflicts with `GLOSSARY.md`, call it out immediately ("Your glossary defines 'Session' as X, but you mean Y here — which is right?").
2. **Sharpen fuzzy words:** When a term is overloaded ("account", "item", "record"), propose one canonical name and record synonyms to avoid.
3. **Cross-check with code:** If the user describes behavior that contradicts the codebase, surface the mismatch right away.
4. **Update `GLOSSARY.md` inline:** Capture each settled term immediately instead of batching at the end.

## `GLOSSARY.md` format

```markdown
# {Project or Context Name}

{1–2 sentences describing what this project/context is.}

## Language

**Subject**:
A course or topic a student tracks in the app.
_Avoid_: course, category, tag

**Study Session**:
One timed focus block logged by a student.
_Avoid_: timer, study_log, block
```

Rules for `GLOSSARY.md`:
- **Be opinionated:** Pick one canonical word and list rejected synonyms under `_Avoid_`.
- **Keep it tight:** 1–2 sentences defining what the thing *is*, not how it is coded.
- **No implementation details:** Never put database schemas, API routes, or general programming concepts (timeouts, errors, utils) in `GLOSSARY.md`.

## ADRs (`docs/adr/NNNN-slug.md`)

Only offer to write an ADR when **all three** are true:
1. **Hard to reverse:** Changing your mind later carries meaningful cost (One-Way Door).
2. **Surprising without context:** A future reader or agent would wonder "why did they do it this way?"
3. **Real trade-off:** There were genuine alternatives and you picked one for specific reasons.

If any of the three is missing, skip the ADR. Scan `docs/adr/` for the highest existing number and increment by one (`0001`, `0002`, ...).

```markdown
# {Short title of the decision}

{1–3 sentences: the context, what we decided, and why.}
```

Add optional sections (**Status**, **Considered Options**, **Consequences**, **Reversal Condition**) only when they add real value; a single sharp paragraph is usually enough.
