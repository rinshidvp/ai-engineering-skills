---
name: implementation-plan
description: Creates a backbone implementation plan (data models, contracts, orchestration, boundaries, pre-decisions, verification checkpoints, task breakdown) saved to tasks/, which serves as both the human review document and the execution guide. Use before building a feature that adds 2+ files or changes 3+ existing ones, adds models, pipelines or endpoints, or will be split across subagents.
---

# Writing Implementation Plans

A plan written before a multi-file change catches the expensive mistakes
(wrong boundaries, undecided error handling, no way to prove the feature works)
while they're still cheap to fix. Use this skill before creating task files,
handing implementation to subagents, or starting a multi-file change.

The plan serves two purposes at once:
1. **Human review:** what you're building and why you made these decisions.
2. **Your execution guide:** your map during implementation.

See `references/example-plan.md` for full example with all sections populated.

## When to Use This Skill

**Use it for:**
- Features requiring 2+ new files
- Changes modifying 3+ existing files
- New models, pipelines, or API endpoints
- Architectural changes or refactoring
- Work you're about to split into task files or hand to subagents

**NOT needed for:**
- Single-file changes
- Debugging tasks
- Investigation/exploration work
- Research tasks where you're gathering information
- Small, contained changes where a quick plan in your host's plan mode (or a few lines in chat) is enough

## Document Hierarchy

This is the **EXECUTION** document - it defines HOW to build.

**Workflow position:**
- `*.requirements.md` (requirements) → `*.design.md` (architecture) → `*.plan.md` (execution)

**Scale to complexity:**
- **Simple features:** Just `*.plan.md` (most common)
- **Medium features:** `*.design.md` → `*.plan.md`
- **Complex features:** `*.requirements.md` → `*.design.md` → `*.plan.md`

Not all projects need all three. Start with plan, add upstream docs only when complexity warrants.

## Core Principle: Backbone vs Leaves

The plan defines **what** and **why**. You decide **how** during implementation.

### BACKBONE (Specify in Plan)
- Domain language & settled decisions — use `GLOSSARY.md` terms throughout and respect `docs/adr/`
- Data model schemas - Fields, types, validation rules, relationships
- Public API contracts - Method signatures, return types, exceptions raised
- Orchestration flow - Which module calls which (A → B → C)
- Integration points - Where this connects to existing code
- Error handling strategy - Fail fast vs graceful degradation
- Testing seams & strategy - Prefer existing seams and the **highest, fewest seams possible** (ideally 1); confirm seams with the user before locking the plan; specify what external boundaries to mock
- Key decisions - WHY you chose approach X over Y

### LEAVES (Omit from Plan)
- Variable names, local variables, loop implementations
- Specific error messages, log statements
- Helper method internals
- Code formatting and style choices

See `references/boundaries.md` for IN SCOPE / OUT OF SCOPE / MUST NOT CHANGE / MUST FOLLOW templates and sanity check.

## Pre-Decisions

Resolve ambiguities NOW, not during implementation. See `references/pre-decisions.md` for template and common decisions bank.

**Template:**
```
Decision: [What needs deciding]
Options: [A, B, C]
Choice: [X]
Rationale: [Why X over others]
```

## Feature Verification

Every feature needs at least one test that proves the happy path works. Without it, "all tests pass" says nothing about the new code. The test:
- Did not exist before your feature
- Exercises new code path
- Would FAIL if you removed your implementation

Stats padding: "24/24 existing tests pass" proves nothing. "New feature test passes" proves it works. Need both, but only second declares done.

See `../writing-unit-tests/SKILL.md` for full test discipline.

## Verification Checkpoints

Build verification into the plan:

| After Step | Verify By | Fail Action |
|------------|-----------|-------------|
| Data models created | Unit test instantiation, validation | Fix before proceeding |
| Repository implemented | Integration test with real DB | Don't build dependent code |
| Endpoint wired | curl/httpie returns expected shape | Debug routing before logic |
| Full flow complete | End-to-end test passes | Root cause before shipping |

Don't build floor 3 until floor 2 is solid.

## Migration Notes (When Changing Existing Systems)

If modifying existing code/data, plan the transition:
- Data migration: backfill script, rollback strategy
- Code migration: deprecated endpoint, new endpoint, removal ticket
- Rollback plan: feature flag, forward-compatible data

## Acceptance Criteria

Testable statements. How do we know it works? Include both feature verification and regression checks.

## Task Breakdown (For Agent Execution)

After the backbone plan, break work into **vertical "tracer-bullet" slices** (not horizontal layer-by-layer tasks). See `references/task-breakdown.md` for template, prefactoring, expand–contract, and dependency graph rules.

- Each task delivers a narrow, **complete, verifiable end-to-end slice** (with its own test inside the slice, not deferred to the end) sized to fit in **one Smart Zone session** (< ~150k tokens).
- **Prefactor first** if cleaning up an existing area makes downstream slices easier (*"make the change easy, then make the easy change"*).
- **runner (fast tier):** bounded mechanical work
- **builder (strong tier):** complex logic, integration, judgment
- **orchestrator (you):** architectural decisions, full context

Which model each tier means on your host: `../_shared/hosts.md`.

**Dependency graph:** mark blocking edges explicitly. Group by file to avoid conflicts.

## Output Location

**Save the plan to:** `./tasks/YYYY-MM-DD-<title>.plan.md`, so it sits next to the requirements and design docs and survives the session
**Example:** `./tasks/2025-01-15-learning-api.plan.md`
**NOT in:** temp/, tmp/, or project root

## Using This Plan During Implementation

1. Read "Data Models" → implement classes first, copy signatures, add validation
2. Read "Orchestration" → implement method signatures, follow pseudocode flow
3. Read "Boundaries" → stay IN SCOPE, don't touch MUST NOT CHANGE, follow MUST FOLLOW
4. Read "Pre-Decisions" → follow pre-decided choices at decision points
5. Read "Testing Strategy" → write tests as you implement, mock as specified
6. Verify "Verification Checkpoints" → after each step, run specified verification
7. Verify "Acceptance Criteria" → all must pass before marking complete

For leaf decisions not in plan: descriptive names, actionable error messages, useful logging, extract helpers >30 lines.

The plan tells you WHAT to build and WHY. You decide HOW.

## Assumption & Granularity Check (Before Presenting the Plan)

Plans fail most often on an assumption nobody said out loud or on poorly sized tasks. Before saving or locking the plan, explicitly check with the user:
1. **Assumptions:** What am I assuming (requirements, existing code, system structure)?
2. **Unilateral decisions:** What did I decide on my own, and should the user confirm?
3. **Test seams:** Do the proposed test seams match expectations (highest, fewest seams)?
4. **Task granularity & blockers:** Does each vertical slice feel the right size (not too coarse/fine), and are the blocking edges right?

If questions → ASK NOW. User has context you don't.

## Self-Check Before Saving Plan

- [ ] Data models & API contracts fully specified?
- [ ] Orchestration flow shown (A→B→C)?
- [ ] Boundaries set (in/out/must-not/must-follow)?
- [ ] Boundary sanity check run (symptom vs root, cleaner vs messier)?
- [ ] Pre-decisions made with rationale?
- [ ] Testing strategy included (unit/integration, mocking)?
- [ ] Verification checkpoints defined?
- [ ] Migration/rollback if changing existing system?
- [ ] Testable acceptance criteria?
- [ ] Task breakdown included (vertical Smart Zone slices, blocking edges marked, agents assigned)?
- [ ] Free of leaf implementations (no loops, vars, try/except)?
- [ ] Would I know what to build from this plan?

If ANY is NO → Fix before saving.

## Common Mistakes

❌ Complete method implementations (loops, vars, try/except)
❌ "Handle errors appropriately" - ambiguous, make pre-decision explicit
❌ Forgetting boundaries - might break existing code
❌ Missing feature verification test - cannot declare done without it

See `references/example-plan.md` for full populated example.
See `references/task-breakdown.md` for task template and dependency graph.
See `../writing-unit-tests/SKILL.md` for test discipline (mock boundaries only, feature test mandatory).
See `../discovery/SKILL.md` for upstream requirements (R-numbered).
See `../software-design/SKILL.md` for upstream contracts (GUARANTEES/EXPECTS).