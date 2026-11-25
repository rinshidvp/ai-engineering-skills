# Running a Sprint

Self-contained workflow for orchestrating agents through a brick DAG. Read `../SKILL.md` first for schema, script reference, and failure modes. Read `orchestration-pattern.md` (same folder) — wave execution is multi-agent; the main agent orchestrates, never implements.

You're a build pipeline controller. Each wave is a build stage. Agents are workers in isolated worktrees. Evidence is the build log. A stage doesn't pass until you've verified its outputs — not heard about them, verified them.

> Role map: `clerk` = runner (fast tier), `coder` = builder (strong tier). The Agent Selection table in `orchestration-pattern.md` is the source of truth; tier → model per host is in `../../_shared/hosts.md`. Legacy names in this file map accordingly.

If you catch yourself writing implementation code — stop. Spawn an agent.

---

## Initialization Check (before Step 1)

Verify the sprint setup from `creating-a-sprint.md` is in place:

- Current branch is `sprint/<YYYY-MM-DD>-<task-slug>` (run `git branch --show-current`).
- progress.md has a Metadata header with the branch name, creation timestamp, and pending-changes disposition.
- Working tree is clean (no uncommitted changes from outside the sprint).

If any of the above is missing, run Sprint Initialization from `creating-a-sprint.md` first. Don't dispatch agents into an unbranched or dirty working tree — worktrees branch from HEAD and inherit whatever's there.

After each phase, append a structured entry to progress.md per `progress-schema.md` (same folder). T1 compliance checks parse these entries (see `orchestration-pattern.md` for agent mapping: fast tier for T1, strong tier for T3).

**The lesson from a previous sprint:** 14 bricks shipped, all type-checked clean, all agents reported "PASS." The app made infinite API calls on load, two pages crashed on missing imports, and layouts were broken by undefined CSS variables. Every bug was a runtime failure invisible to static analysis. The orchestrator ran `tsc --noEmit` as the gate and called it done. The same pattern hits every domain: a Rust binary that compiles clean but panics on real input, a CLI tool that passes `cargo test` but silently drops flags, an API server where every handler type-checks but the middleware chain swallows errors. Type-checking is the floor, not the gate. **You must run the software.**

---

## Wave Audit Protocol (applies to every wave)

The Loop below runs through Steps 1–13 per wave. At the close of each wave — after the Wave Gate passes and before dispatching the next wave:

1. **Append a Wave entry to progress.md** per `progress-schema.md` — wave number, brick ids, evidence per brick (named test + assertion, runtime observation), checkpoint sha.
2. **Spawn T1 compliance check** — verifies the wave's checklist from `progress-schema.md`: worktrees were created for multi-brick waves, gate Levels 1+2+3 are all recorded with evidence, the wave commit landed on the sprint branch, reuse re-check is recorded. T1 checks presence + structure + reference resolution — never correctness.
3. **If T1 fails**: a brick is incompletely reported, or a gate level was skipped. Fix the audit before next dispatch — don't just override.
4. **Spawn T3 deep review** — code-reviewer subagent on the wave's diff (and a completeness review at milestone boundaries / final sign-off, per Steps 9 and 12 below). T3's job is correctness, not compliance. Record findings in the wave's progress entry under the `T3:` field. If T3 surfaces issues, resolve them before dispatching the next wave.
5. **Failures bubble to the orchestrator.** Retry / escalate / skip-with-rationale decisions belong to the orchestrator per `orchestration-pattern.md`. Never silently retry a brick or wave.

Parallelize T1 checks across bricks within a wave when they're independent.

For T1 prompt skeleton, see `orchestration-pattern.md`.

---

## The Loop

| Step | Name | What happens | Skip when |
|------|------|-------------|-----------|
| 1 | Load State | Read ready bricks, decisions, context, DESIGN.md | Never |
| 2 | Pre-Flight | Scan shared infra, set up test runners, define verification commands, anti-pattern registry | After wave 1 (already done) |
| 3 | Plan Wave | File conflict matrix, worktree/batch decision, announce dispatch | Never |
| 4 | Dispatch | Mark in_progress, create worktrees, spawn agents with curated prompts | Never |
| 5 | Collect | Rebase worktree branches, compile check | Single-brick wave (no worktree) |
| 6 | Verify | Named test + assertion evidence per brick | Never |
| 7 | Wave Gate | L1 (static) + L2 (behavioral) + L3 (runtime via independent T1R audit agent) | Never — L3 is not deferrable, not self-assessed |
| 8 | Commit | Conventional commits, specific files | Multi-brick (already committed via collect) |
| 9 | Milestone Review | completeness review + independent T3R integration audit | Every 2-3 waves or at layer boundaries |
| 10 | Reuse Re-Check | Do remaining bricks duplicate what this wave built? | Never |
| 11 | Repeat | Next ready bricks | No more bricks |
| 12 | Sign-Off Review | Cross-brick seam review | Never |
| 13 | Sprint Complete | Resolve findings, progress.md entry, report to human | Never |

---

### 1. Load State

```bash
uv run scripts/sprint_tasks.py ready <tasks-file> --json
# No uv? Use: python scripts/sprint_tasks.py ready <tasks-file> --json
```

Read decisions.md. Read context.md if it exists. Read progress.md if resuming.
Read `brick-design.md` (same folder) — internalize what a brick is before dispatching agents to build them.

Read every `DESIGN.md` in directories the sprint touches. These capture
architectural decisions and component contracts. Bricks that violate them
will be caught at review and reverted.

A well-designed codebase accumulates composable building blocks. Before
scoping any brick, check what already exists — components, hooks, utilities
that do what the brick needs or can be extended to. If two bricks would
build similar things, extract the shared piece first. Duplication is a
design failure, not a speed optimization.

### 2. Pre-Flight — Shared Infrastructure Scan

Before dispatching wave 1, walk the `files` arrays of ALL bricks. Identify:
- Shared config files (package.json, lock files, build configs, tsconfig)
- Common dependencies multiple bricks will import
- Test infrastructure (test runners, setup files, mock utilities)
- Gitignore rules that block new directories

If shared infra setup is needed: do it on the main branch first, commit it, then dispatch agents from that base.

If shared infra is already set up, tell every agent explicitly: "Do NOT modify: [list files]. All dependencies are installed."

This prevents the failure mode where 8 agents independently add the same dependency, creating 8-way merge conflicts on collection.

**Test infrastructure is non-negotiable.** If any brick has `guarantees_tested` and no test runner is configured, set it up now. Run a trivial test to prove the pipeline works. Commit it before Wave 1. A sprint with guarantee specifications and no way to run tests is structurally broken — agents will "verify" guarantees by reading their own code, which proves nothing.

**Verification commands.** Define two commands in context.md before dispatching:

1. **Test command** — how to run unit tests (e.g., `cargo test`, `npm test`, `pytest`)
2. **Runtime command** — how to start the software and verify it actually runs (e.g., `cargo run` + curl, dev server + load page, CLI invocation)

If you can't define both, you can't verify the sprint's output. This is a pre-flight blocker. Write them under a `## Verification` heading in context.md so every agent and every wave gate uses the same commands.

**Anti-pattern registry.** Every technology stack has footguns that compile clean but fail at runtime. Before Wave 1, add a `## Known Anti-Patterns` section to context.md. These go into every agent prompt and the wave gate grep list. The orchestrator identifies these by asking: "What are the common mistakes in this stack that static analysis won't catch?" Document them as grep-able patterns with the failure they cause.

### 3. Plan Wave — File Conflict Gate

Extract the `files` array from each ready brick. Build the overlap matrix.

- No overlap → parallel agents, each in its own worktree
- Shared files → single agent, all overlapping bricks batched

**Blast radius check:** If any brick in this wave changes a type or function signature, grep for consumers across the codebase. If consumers live in files outside this wave's scope and no later brick fixes them, the wave gate will fail on compile. Either batch the consumer fix into this brick or plan a compile-fix step before the gate.

**Worktree decision:**
- Single brick → run in main tree. No worktree overhead.
- Multiple bricks, no file overlap → create a worktree per brick.
- Multiple bricks, shared files → batch to one agent.

Announce before dispatching:
```
Wave N (single brick — no worktree):
  🤖 A @ coder — Brick 007: <name> (files: x.ts, y.ts)

Wave M (parallel — worktrees):
  🤖 A @ coder (worktree) — Brick 003: <name> (files: x.rs, y.rs)
  🤖 B @ coder (worktree) — Brick 004 + 005: <names> (batched: share z.rs)
  🤖 C @ clerk (worktree) — Brick 006: <name> (mechanical: copy fixtures)
```

### 4. Dispatch

Mark bricks `in_progress`:
```bash
uv run scripts/sprint_tasks.py update <tasks-file> <id> --status in_progress
# No uv? Use: python scripts/sprint_tasks.py update ...
```

**Path 1: Single brick (no worktree)**

Agent works directly in the main tree. No worktree create step. Skip section 5.

**Path 2: Multiple bricks (worktrees)**

```bash
uv run scripts/sprint_tasks.py worktree create <tasks-file> <brick-id>
# prints the absolute worktree path — capture it for the agent prompt
```

Each agent prompt must start with: `FIRST: cd <worktree-absolute-path> && pwd` and include: "ALL file reads, writes, and commands must use this worktree directory. Do NOT operate on the main working tree."

Spawn agents in a single message.

**Agent selection:** use the strong tier for implementation bricks, spawned
with your host's subagent tool (`../../_shared/hosts.md`). The agent must follow `references/agent-guidelines.md`
(code quality, testing discipline, pushback on unclear requirements, reporting
discrepancies with design sources). It must refuse to guess when the
specification is incomplete — which is what you want.

Use the fast tier only for fully mechanical bricks (file moves, fixture copying, running commands).

Agent prompt template — compact, no extras:

```
**Read first** (these are your sources of truth — read ALL before writing code):
- @<decisions.md> (READ-ONLY)
- @<context.md>
- @<design.md> — Reuse Analysis + component contracts
- @<spec.md> (if exists) — requirements and acceptance criteria
- @<qa-plan.md> (if exists) — test cases this brick must satisfy
- @<design sources — prototype files, API schema, whatever applies to this brick>
- @<grounding skeleton for this unit if one was produced during specification grounding>

**Brick NNN: <name>**
<description from tasks.json — must include granular detail: not "build a quotas page"
but "build a page with sections A, B, C where section A contains fields X, Y, Z
per the prototype at <file>:<lines>">

**Acceptance criteria:**
<criteria from tasks.json>

**Existing code to use/extend:** <items from design.md Reuse Analysis relevant to this brick>
**Write ONLY:** <file list from brick>
**Do NOT modify:** <frozen shared infra files>
**Downstream:** <serializers, guards, or consumers this brick's data flows through — if any>

**Evidence (tests):** run `<test command>` — show the assertion output, not the count.
**Evidence (runtime):** run `<runtime gate command from context.md>` — verify the feature loads and works.
**Guarantees:** <guarantees_tested items>
**Anti-patterns (will fail review):** <from context.md Known Anti-Patterns section>
```

**What goes in the brick description matters more than anything else in this prompt.** The brick description IS the specification the agent builds against. If it says "build a quotas page" — the agent will invent a quotas page. If it says "build a quotas page matching prototype at `tmp/v2/src/pages/QuotasPage.tsx`: hero section (lines 45-80), tab toggles (lines 82-95), day-grouped windows ledger (lines 100-180), 7-day rolling strip (lines 185-220)" — the agent builds that.

Every brick description for a non-trivial unit must include the granular skeleton from specification grounding. The agent should never need to decide what the output looks like — only how to implement it. If the agent has to make a design decision, the specification was incomplete.

If your prompt is over 20 lines of prose, you are re-stating content that belongs in context.md or decisions.md. Point to them with `@` references — don't dump their contents inline. But DO include design source file paths — the agent needs to read the actual files.

### 5. Collect — Rebase Worktrees for Linear History

Skip if the wave was a single brick — the agent already committed to the main tree.

After each agent completes, integrate its worktree branch in sequence:

```bash
# Rebase worktree branch onto HEAD and fast-forward
uv run scripts/sprint_tasks.py worktree collect <tasks-file> <brick-id>

# Remove the worktree and branch
uv run scripts/sprint_tasks.py worktree cleanup <tasks-file> <brick-id>
```

Clean linear history — no merge commits. Agent commits land in main verbatim via rebase, so their messages must be conventional from the start.

Bad: `sprint(session): brick 011 — source message events`
Good: `feat(events): emit source message events from transport sources`

Sprint context (session, wave, brick IDs) belongs in progress.md — not git log.

If rebase conflicts: the file overlap matrix was wrong. Do NOT force-resolve. Abort the rebase (`git rebase --abort`), surface to the human, fix the matrix.

After all branches integrated:
```bash
cargo check    # or tsc --noEmit — does the combined code compile?
cargo test --lib  # do existing tests still pass?
```

### 6. Verify — Evidence, Not Assertions

Bad: "Done." / "Tests pass." / "540/540 passed."
Good: `cargo test timeout::tests::test_returns_timeout_after_max_wait` → test name, passing, specific assertion output.

A wave where every brick reports counts has proven nothing. When an agent returns without evidence: "Run the specific test. Show me the assertion, not the score."

Update tasks.json. Append to progress.md with timestamp and evidence.

### 7. Wave Gate — Verify Before Proceeding

The gate has three levels. All three must pass. Skipping level 2 or 3 is how broken sprints ship.

**Level 1 — Static (does it compile?)**
- Created files → `ls` them
- Removed patterns → `grep` to confirm gone
- Modified structure → `cargo check` / `tsc --noEmit`
- Anti-pattern grep → scan for known footguns from context.md's anti-pattern registry

**Level 2 — Behavioral (does it do what it claims?)**
- For unit-testable bricks: run the test suite, see named assertions pass
- For runtime-verified bricks: exercise the feature, observe correct behavior
- Every guarantee in `guarantees_tested` must have corresponding evidence — a test output or an observed runtime behavior. If a guarantee has no evidence, the brick hasn't proved it holds weight

Bad: compile succeeds → proceed.
Good: run the named test → see the named assertion pass.

**Level 3 — Runtime (does the software actually work?) — INDEPENDENT AUDIT**

Level 3 is NOT self-assessed. Dispatch a fresh audit subagent (T1R — cheap/fast model) to run verification independently. See `orchestration-pattern.md` for the T1R prompt skeleton.

The T1R agent receives: (1) the verification commands from context.md, (2) the list of features/paths this wave touched. It runs the commands, exercises each affected path, and writes raw observations to `tasks/<task-name>.wave<N>-audit.txt`. The orchestrator reads the observations and makes the pass/fail call — but the observations themselves are independent.

**Why this can't be self-assessed:** A previous sprint orchestrator read the instruction "you must run the software," acknowledged it, then wrote "Level 3: deferred" at every wave gate across 4 waves. Every bug found later was a runtime failure. The instruction was clear. The agent optimized for completion. No amount of prompting fixes this — structural separation of execution from reporting does.

Level 3 is not deferrable. If the software can't be exercised after this wave, that's a gate failure — record it as FAILED and decide the recovery move per the Failure Protocol.

**Bricks with no runtime surface** (pure library modules, data models, serialization utilities): T1R verifies that the module compiles, links into the larger build, and its unit tests run. The T1R agent runs the test command and the build command — not the server. This is still independently verified (the agent runs the commands, not the orchestrator), but the exercise is compilation + tests, not "start the app and click around." Record the scope in the audit artifact: "No runtime surface — verified via build + unit tests."

**Multi-service software** (e.g., Rust backend + React frontend): Define test and runtime commands per technology layer in context.md under `## Verification`. The T1R agent runs all of them.

If Level 2 is weak (few tests), Level 3 becomes your primary verification. The T1R audit is the only thing standing between you and shipping on faith.

### 8. Commit Checkpoint — MANDATORY

**Single-brick waves (no worktree):** The agent worked in the main tree. After the gate passes, stage and commit:

```
git add <specific files from this wave>
git commit -m "feat(scope): what this wave changed"
```

Use conventional commits (`feat`, `fix`, `refactor`) — these survive into the PR and main branch history long after the sprint is forgotten. Describe the code change, not sprint mechanics. Commit specific files (not `git add -A` — it catches secrets and build artifacts). Ask user unless pre-authorized.

**Multi-brick waves (worktrees):** Agent commits are already in main from `worktree collect`. No new commit needed. Confirm messages are conventional:

```
git log --oneline -<N>   # N = number of bricks in this wave
```

If any message uses sprint-internal format (`brick 011 — ...`), amend it before dispatching the next wave.

### 9. Milestone Review

After completing a logical layer, three checks:

**Static review** — spawn a code-reviewer subagent (strong model):

"It's the next morning and something in this layer is broken. What did we miss? Also: did any brick build something that already existed in the codebase — a hook, utility, component, or pattern that was already there and could have been reused?"

**Independent integration audit (T3R)** — spawn a strong-model subagent with the T3R prompt from `orchestration-pattern.md`. This agent reads acceptance criteria for the completed layer's bricks, then independently starts the software and exercises it against those criteria. It reports VERIFIED/FAILED/UNTESTABLE per criterion and writes findings to `tasks/<task-name>.milestone<N>-audit.txt`.

T3R catches the class of bugs where every brick passes its unit test but the integrated feature doesn't work. A code reviewer reading files cannot catch import mismatches, integration failures, or state management bugs that only manifest at runtime. T3R can — because it runs the software.

Surface findings from both before proceeding. T3R failures are gate failures — resolve before dispatching the next wave.

### 10. Reuse Re-Check

The remaining bricks were planned against the pre-sprint codebase. This wave just changed it.

Before planning the next wave, scan what was just built. Ask: do any remaining bricks duplicate something this wave created? A wave that builds a shared utility may make a later brick's "create utility X" redundant.

If a remaining brick now duplicates something that exists: modify the brick to extend/use it, or delete it. Update tasks.json before dispatching.

### 11. Repeat

Next ready bricks → reuse re-check → plan wave → dispatch → collect → verify → gate → commit → repeat.

### 12. Sprint Sign-Off Review

Before declaring complete, spawn a completeness-review subagent (strong model) with a sprint-seam lens — the gaps between bricks that per-brick tests don't catch:

"All bricks passed independently. Now check the seams: places where one brick changed something and another brick's code still assumes the old shape. Focus on type/interface consumers that weren't in any brick's scope, serializers or guards written for the old data shape, cross-brick data handoffs where the producing brick and consuming brick were in different waves, and dead patterns from before the sprint that survive in untested code paths."

Surface findings. Fix before declaring complete.

### 13. Sprint Complete

1. Sign-off review findings resolved
2. Completion entry in progress.md
3. Report to human

---

## Worktree Management

**Why worktrees:** Parallel agents in a shared working tree = silent data loss. Last writer wins. No error. No warning. This destroyed 15 files of work in a real sprint — bricks 024-029 modified tracked files, none were committed, next wave's agents overwrote everything.

Worktrees eliminate this class of failure. Each agent works on an isolated copy. Changes merge back explicitly. If something goes wrong, you see a rebase conflict — not silent overwriting.

**Why self-managed, not `isolation: "worktree"`:** The platform's built-in worktree isolation branches from the default branch, not HEAD. Agents would get a stale codebase missing the current branch's commits. `worktree create` always branches from HEAD, guaranteeing agents see the latest work.

**Why rebase, not merge:** `git merge` creates merge commits. With N parallel agents per wave and M waves, the history becomes an unreadable octopus graph. Rebase + fast-forward places each agent's commit linearly on HEAD — clean git log, easy bisect, original commit messages preserved. Safe here because worktree branches are private (not pushed, not shared).

---

## Failure Protocol

**Brick fails:**
1. Mark `failed` in tasks.json
2. Record in progress.md: what happened, agent output, your assessment
3. Surface to the human. Do NOT attempt autonomous fixes. Do NOT skip.
4. Wait for human decision

**Decision conflicts** (agent reports conflict with decisions.md):
1. Stop dispatching in that area
2. Surface both sides to the human
3. Wait for resolution
4. Update decisions.md if decision changes (orchestrator only)

**Resuming:**
- tasks.json statuses show what's done
- progress.md evidence shows what happened
- decisions.md still applies
- `ready` → continue the loop

---

## Adding Bricks Mid-Sprint

Discovered a gap? Need a brick that wasn't planned?

Read `brick-design.md` (same folder) — schema, sizing, criteria, files field.
Read `wave-planning.md` (same folder) — where the new brick fits in the dependency tree.

Then:
1. Check the reuse analysis (design.md) and recently completed bricks — does this gap already have a solution?
2. Edit `tasks.json` directly — append to `bricks` array with proper `depends_on`
3. Check for file conflicts with in-progress bricks
4. Don't dispatch until the current wave gate passes and changes are committed

---

<reminder>
LOAD STATE: Read design.md Reuse Analysis + decisions.md Design Decisions. Not optional. No design.md = stop.

DISPATCH: Use a strong-model subagent for implementation bricks (see orchestration-pattern.md agent mapping). Every prompt MUST include: reuse analysis items, design source file paths, granular brick description from grounding (not "build a quotas page"). Tell agents what to use/extend. If a type is consumed by 3+ bricks, embed exact definition inline. If data flows through serializers/guards, list them under **Downstream**. See `failure-modes.md` (same folder) for why each of these matters.

PLAN WAVE: Type/interface change → trace consumers, plan for compile breakage.

WAVE GATE Level 3: Dispatch T1R (independent audit subagent, cheap/fast model) — do NOT self-assess runtime. The audit agent runs verification commands and writes observations to an artifact file. You read the observations and make the call. "Deferred" is not a valid Level 3 status.

WAVE GATE: Reuse re-check before next wave — do remaining bricks duplicate what this wave built?

MILESTONE: Reviewer checks duplication, not just breakage. Duplication is invisible to failure-oriented review.

SIGN-OFF: Seam review before declaring complete. Per-brick tests pass but cross-brick seams may not.

COMMIT after every wave gate. Conventional messages. Sprint-internal messages are not acceptable — they survive into the PR.
Do NOT create summary documents.
</reminder>
