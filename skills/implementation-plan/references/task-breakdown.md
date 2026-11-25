# Task Breakdown Reference

## Core Rule: Vertical "Tracer-Bullet" Slices

Prefer **vertical slices** over horizontal layer-by-layer tasks:
- **Avoid horizontal slicing:** "Task 1: all DB models → Task 2: all APIs → Task 3: all UI → Task 4: tests last." Nothing works until the final task, so early design mistakes stay hidden.
- **Use vertical slices:** Each task cuts a narrow, **complete end-to-end path** (data + logic + interface + its own verification test) that is demoable or testable on its own and fits inside **one Smart Zone session** (< ~150k tokens).
- **Prefactor first:** If cleaning up messy existing code makes the feature slices easy, make Task 1 a small, behavior-preserving prefactor (*"make the change easy, then make the easy change"*).

### Exception: Wide Refactors (Expand–Contract)

When one mechanical change (renaming a column, retyping a widely used symbol) touches dozens of call sites so no single vertical slice can land green, sequence it as **expand–contract**:
1. **Expand:** Add the new form beside the old so nothing breaks.
2. **Migrate:** Update call sites in small blast-radius batches (per folder/module), each blocked by Expand, keeping tests green after every batch.
3. **Contract:** Delete the old form once zero callers remain (blocked by all Migrate batches).

## Template

```markdown
## Tasks

### Task 1: [Short descriptive name — end-to-end behavior]
- **Delivers:** [1–2 sentences on the verifiable end-to-end behavior]
- **Files:** [Expected paths to create/modify]
- **Blocked by:** [Task numbers, or "none" if ready immediately]
- **Agent:** [runner / builder / orchestrator — based on complexity]
- **Verify:** [Exact test command or observable proof inside this slice]
```

## How to Break Down

1. **Check for prefactoring** — Does one small cleanup make everything else simpler? Put it first.
2. **Slice vertically by user behavior** — Start with the thinnest working end-to-end path (tracer bullet), then layer additional behaviors on top.
3. **Include the test inside each slice** — Never defer all testing to a final "write tests" task.
4. **Mark blocking edges explicitly** — Only list tasks that genuinely gate this one so unblocked tasks can run in parallel.
5. **Group by file** — Avoid having two parallel tasks edit the same file.

## Agent Assignment Guidelines

| Agent | Model Tier | Use For |
|-------|------------|---------|
| **runner** | fast | Bounded, mechanical work: apply a known pattern, migrate a batch, run verification |
| **builder** | strong | Requires judgment: vertical feature slices, complex logic, integration, error handling |
| **orchestrator** | (you) | Architectural decisions, orchestration, things requiring full context |

## Dependency Graph Example (Vertical Slices)

```
Task 1 (prefactor seam) ──> Task 2 (tracer bullet: create & read basic note + test)
                                    │
                        ┌───────────┴───────────┐
                        ▼                       ▼
              Task 3 (edit/delete       Task 4 (tag filter
               note + tests)             + tests)
```

## Example Task List (Vertical)

### Task 1: Prefactor note storage behind a clean seam
- **Delivers:** Extracts note persistence behind `NoteStore` so feature slices can test against an in-memory adapter without touching disk.
- **Files:** `src/notes/store.ts`, `src/notes/store.test.ts`
- **Blocked by:** none
- **Agent:** builder
- **Verify:** Existing tests stay green + `npm test src/notes/store.test.ts` passes.

### Task 2: Tracer bullet — create and view a study note end-to-end
- **Delivers:** A student can create a plain-text note for a Subject and see it rendered back (schema + API + UI + happy-path feature test).
- **Files:** `src/notes/create.ts`, `src/routes/notes.ts`, `src/ui/NotesPanel.tsx`, `src/notes/create.test.ts`
- **Blocked by:** Task 1
- **Agent:** builder
- **Verify:** `npm test src/notes/create.test.ts` passes and note persists across reload.

### Task 3: Edit and delete existing notes
- **Delivers:** A student can update or remove a note with validation and empty-state handling.
- **Files:** `src/notes/update.ts`, `src/ui/NoteItem.tsx`, `src/notes/update.test.ts`
- **Blocked by:** Task 2
- **Agent:** builder
- **Verify:** `npm test src/notes/update.test.ts` passes.

### Task 4: Filter notes by Subject
- **Delivers:** A student can filter their notes list by Subject (reuses `GLOSSARY.md` term).
- **Files:** `src/notes/filter.ts`, `src/ui/SubjectFilter.tsx`, `src/notes/filter.test.ts`
- **Blocked by:** Task 2
- **Agent:** runner
- **Verify:** `npm test src/notes/filter.test.ts` passes.
