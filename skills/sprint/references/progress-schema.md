# progress.md Schema

The audit spine of a sprint. Every phase appends a structured entry. T1 checks (cheap/fast-model subagent) parse this file to verify compliance. Resume from interruption reads this file.

---

## Header (written once at sprint init)

```markdown
# Sprint: <task-name>

## Metadata
- branch: sprint/<YYYY-MM-DD>-<task-slug>
- created: <epoch_ms>
- pending-changes-at-start: <committed | stashed | none>
- pending-changes-commit: <sha if committed>
```

---

## Phase entry template (appended after every phase)

Use the phase name as the heading. Phases below are listed by name, not number — sprints skip phases (small features skip Spec/QA Plan, etc.) so numeric continuity is meaningless.

```markdown
## <phase name>
- status: passed | failed | skipped
- agent: <subagent_type> <model> [×N if parallel]
- artifact: <path>
- evidence: <file:lines | brick id | test name | spike output — must resolve>
- compliance:
  - [x] <checklist item>
  - [x] <next item>
- T1: passed at <epoch_ms> | failed at <epoch_ms> — <one-line reason>
- T3: passed at <epoch_ms> | failed at <epoch_ms> — <one-line reason> | not-required
- gate: <user response text + epoch_ms> | not-required
- notes: <only if needed>
```

`T3` applies to phases where deep Coder review runs (wave gates, milestone reviews, final sign-off). For planning phases, `T3: not-required`.

Every checkbox must reference evidence that resolves (path, line, brick id, timestamp). `[x] Done` without a reference is theater — T1 fails it.

---

## Per-phase compliance checklists

### Reuse Discovery
- [ ] `tasks/<name>.design.md` exists with `## Reuse Analysis` section
- [ ] Section lists ≥1 of: existing code to use/extend, patterns to follow, constraints from DESIGN.md
- [ ] `tasks/<name>.decisions.md` has `## Design Decisions — Components we're using` section
- [ ] User-validation entry exists with timestamp + approval text

### Specification Grounding
- [ ] Skeleton produced for each unit-of-work
- [ ] Every ASSUMPTION resolved (link to: spike result, decision in decisions.md, or user input)
- [ ] No remaining ASSUMPTION entries in any grounding output

### Design
- [ ] `design.md` has `## Components` section with ≥1 component
- [ ] Each component documents GUARANTEES, EXPECTS, FAILURE BEHAVIOR
- [ ] `## Layers` section identifies altitude of each layer
- [ ] User-validation entry: explicit approval of layers and contracts (not just "looks fine" on the file as a whole)

### Spike (per spike)
- [ ] Spike script/run captured at path
- [ ] Observed behavior recorded (not inferred)
- [ ] Either: original assumption validated with reference to evidence, OR design.md updated to reflect actual behavior

### Adversarial Review
- [ ] Review output filed
- [ ] Each finding has a disposition: addressed-in-plan | accepted-risk | won't-fix
- [ ] User saw the findings

### Brick Decomposition
- [ ] Design validated by user before decomposition (design.md user gate passed with timestamp)
- [ ] Specification grounding ran — no unresolved ASSUMPTION entries
- [ ] tasks.json validation gate from creating-a-sprint.md passes
- [ ] Every implementation brick has `guarantees_tested`
- [ ] No two bricks share files unless batched into one agent

### Wave Execution (per wave)
- [ ] Worktree created per brick (multi-brick waves)
- [ ] All bricks' acceptance criteria met with named evidence (test name + assertion, runtime observation)
- [ ] Wave gate Level 1 (static) + Level 2 (behavioral) passed with evidence
- [ ] Wave gate Level 3: T1R independent runtime audit dispatched (cheap/fast model), audit artifact at `tasks/<name>.wave<N>-audit.txt`, observations reviewed by orchestrator
- [ ] T1R audit artifact contains per-item observations (not just "passed") — T1 verifies this
- [ ] T3 deep review at the gate (code-reviewer / completeness review) filed
- [ ] Commit checkpoint on main (sha recorded)
- [ ] Reuse re-check before next wave (any newly-built code that supersedes a remaining brick?)

### Milestone Review (per milestone)
- [ ] completeness static review filed
- [ ] T3R independent integration audit dispatched (strong model), audit artifact at `tasks/<name>.milestone<N>-audit.txt`
- [ ] T3R audit contains VERIFIED/FAILED/UNTESTABLE per acceptance criterion — not test counts
- [ ] T3R findings resolved before next wave dispatch

### Sprint Sign-off
- [ ] All closing bricks passed
- [ ] T3 sign-off seam review filed
- [ ] T3R final integration audit filed (covers full feature, not just last layer)
- [ ] Proof package presented to user
- [ ] User sign-off captured

---

## Resume protocol

On session resume, the orchestrator:
1. Reads progress.md top-to-bottom.
2. Identifies the last entry whose `status: passed` was confirmed.
3. Re-reads any artifacts listed in passed entries (not the agent transcripts).
4. Resumes from the next pending phase.

If the last entry is `status: failed` or partially written, the orchestrator must decide the recovery move before continuing.
