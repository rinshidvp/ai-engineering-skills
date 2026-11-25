# Orchestration Pattern

How the sprint skill executes: main agent as orchestrator, fresh sub-agents per phase, tiered review, audit trail in progress.md.

---

## Roles

**Main agent (orchestrator) — Coder.**
- Owns: triage, phase dispatch, validation of artifacts against checklists, brick decomposition (NEVER delegated), worktree management, wave merge, proof package.
- Does NOT: re-explore the codebase, do the phase work itself, accept sub-agent self-reports without verifying the artifact.
- Retains in context: objective, accumulated decisions, current phase, artifact paths. NOT the sub-agents' exploration trail.

**Phase sub-agents — Coder/Clerk per task.**
- Each phase = a fresh sub-agent with a curated input package.
- Input package = **file paths to read**, not embedded content (see Cost Discipline below).
- Output = a single artifact filed by the main agent.
- On failure: bubble back to orchestrator. Orchestrator decides retry / escalate / skip-with-rationale.

---

## Agent Selection

Works on Claude Code, opencode and Antigravity. Pick the role, then spawn it
the way your host does (see `../../_shared/hosts.md` for the spawn tool and
which model each tier maps to).

| Role | Model tier | Use When |
|------|------------|----------|
| builder | strong | **Default for implementation bricks.** Follows `references/agent-guidelines.md` (code quality, testing discipline, pushback on incomplete specs). Will refuse to guess when specifications are incomplete and report discrepancies with design sources. |
| general-purpose | strong | Non-brick tasks: investigation, analysis, ad-hoc fixes |
| runner | fast | Fully predetermined work: run tests, apply known changes, file moves |
| auditor | cheap/fast | Specification grounding audits, file searches, mechanical lookups, T1 compliance checks, T1R runtime audits |
| explorer | cheap/fast | Find files, search code, understand structure |
| code-reviewer | reviewer | Review completed work at milestones (see `agents/code-reviewer/body.md` in this repo) |
| completeness-reviewer | reviewer | Check completeness after a layer of bricks (same reviewer prompt with a seam/completeness lens — see running-a-sprint.md Steps 9/12) |

Legacy names from the mentor repo map as: `sprint-dev` → builder,
`general-purpose` → general-purpose, `minion`/`clerk` → runner/auditor,
`Explore` → explorer, `implementation-reviewer`/`qa-dev` → completeness-reviewer.
If you see those names in older handoffs, translate them.

Cheap/fast models are literal — they will confidently do the wrong thing on ambiguous tasks because they pattern-match rather than reason. The result looks plausible but silently diverges from intent. Always use a strong model for judgment work.

---

## The fresh-context principle

Each phase agent starts with no prior turns. It reads what the orchestrator points at, does its phase, returns its artifact. The orchestrator absorbs the artifact, not the agent's reasoning trail.

Why: an agent alive through design + reuse + grounding + planning has context bloat. Important details deprioritize as context grows. A human engineer doesn't keep all phases active in their head — they finish a session, write down what matters, take a break, come back to the next thing with only relevant context loaded. Fresh sub-agents simulate that.

---

## Cost discipline

Output tokens cost ~5× input tokens. Apply this everywhere:

- Don't embed context inline in agent prompts. Write it once to a file and have the agent read it.
- Reuse context files across phases: `context.md`, `decisions.md`, `design.md` are read by many agents.
- Short prompts that point to files beat long prompts that embed content.

**Good:**

```
Read @tasks/<name>.context.md, @tasks/<name>.decisions.md, @tasks/<name>.design.md.
Then do <phase task>. Output to @tasks/<name>.<artifact>.md.
```

**Bad:**

```
Here is the full context: [500 lines of design decisions inlined]
Here is the full design: [800 lines inlined]
Now do <phase task>.
```

The bad version pays the output cost every spawn. The good version pays it once.

If the same instruction goes to many agents, write it to a shared instruction file and reference it. Worth a one-time write if it's reused ≥2 times.

---

## Review tiers

| Tier | Model tier | When | What it catches |
|---|---|---|---|
| **T1 — Compliance audit** | Cheap/fast | After every phase artifact is filed | Presence + structure: artifact exists, required sections present, evidence artifacts exist at claimed paths and contain real content |
| **T1R — Independent runtime audit** | Cheap/fast | Every wave gate (Level 3) | Runtime failures invisible to static analysis — the agent runs verification commands independently and reports raw observations |
| **T2 — Adversarial review** | Reviewer | Once, on brick outline before tasks.json | Blind spots, verification gaps, dependency risks, footguns, pre-mortem |
| **T3 — Deep review** | Reviewer (`code-reviewer` / completeness review) | Wave gates, milestone reviews, final sign-off | Correctness, completeness, seam bugs |
| **T3R — Independent integration audit** | Reviewer | Milestones + final sign-off | Exercises the software against acceptance criteria — not reading code, running the software |

### Why independent audits exist

Agents don't intentionally fake compliance — they pattern-match to complete the task and skip the hard parts. A previous sprint orchestrator read the instruction "you must run the software," acknowledged it, then wrote "Level 3: deferred" at every single wave gate across 4 waves. Every bug found later — nested router crash, race conditions, empty timeline, off-by-one navigation — was a runtime failure invisible to the static and unit-test checks the orchestrator actually ran. The instruction was clear. The agent optimized for completion over compliance.

No amount of prompting fixes this. The orchestrator is both executor and reporter — it can claim Level 3 passed without running anything, and T1 (checking the self-report) will see a non-empty field and say PASS. The structural fix is separation of execution from reporting: **an independent agent runs the verification commands and reports what it observes, with no knowledge of what "should" work.**

### Tier responsibilities

**T1** checks that evidence artifacts exist at claimed paths and contain real content. It does NOT check correctness, and it does NOT trust text claims in progress.md — it verifies the artifacts themselves. If progress.md claims "Level 3 evidence at tasks/wave2-l3.txt," T1 reads that file and confirms it contains actual command output (not just "passed").

**T1R** is a fresh cheap/fast-model agent with zero sprint context. It receives: (1) the verification commands from context.md, (2) the list of paths/features this wave touched. It runs the commands, reports raw observations, and flags anything that errors, crashes, or produces unexpected output. It does not judge whether the feature is correct — it reports what it sees. The orchestrator reads the observation and makes the pass/fail call, but the observation itself is independent.

**T2** attacks the plan once, before execution.

**T3** evaluates the code for correctness and completeness by reading diffs and files.

**T3R** is a fresh strong-model agent at milestones. It reads acceptance criteria for the completed layer, then independently starts the software and exercises it against those criteria. It reports: what worked, what failed, what it couldn't test. This catches the class of bugs where every brick passes its unit test but the integrated feature doesn't work.

**These tiers are independent.** Passing T1 says nothing about T1R, T3, or T3R. Each catches a different class of failure. Skipping any tier means that class of failure ships undetected.

T1 runs synchronously between phases by default. Within a wave, T1 checks across parallel bricks can run in parallel. T1R runs as part of the wave gate (Step 7, Level 3). T3R runs at milestones (Step 9) and sign-off (Step 12).

---

## Audit trail

Every phase output writes a structured entry to progress.md. Schema in `progress-schema.md`.

The entry is the witness statement: it names the artifact, the evidence, who validated, when. Stating it forces the orchestrator to actually do it; gives T1, T3, and the user something to verify against.

If the artifact exists but the progress.md entry doesn't — the phase isn't done.

---

## Failure → bubble up

When a phase agent fails or produces a bad artifact:

1. Phase agent reports failure, or T1 catches a compliance failure.
2. Orchestrator records the failure in progress.md (what happened, what was produced, the failure mode).
3. Orchestrator decides the recovery move: retry same agent, retry with a different model, surface to user, or skip with explicit rationale (and record the rationale).
4. Never silently retry. Never silently skip. The orchestrator's decision is itself audit-logged.

---

## Anti-patterns

Each entry: the move → the failure mode it produces → the right thing instead.

- **Main agent re-exploring the codebase.** "Let me read these 30 files myself." → main agent's context fills with exploration trails; later judgment gets buried under early reading. Spawn a sub-agent.
- **Stuffing context into prompts.** → pays the output-token cost on every spawn; bloats every subsequent turn; long prompts deprioritize the actual task. Use `@file` references.
- **Treating T1 as sufficient.** → Clerk passes presence, not correctness; seam bugs and wrong-shape contracts survive every wave. T3 still has to run.
- **Skipping the progress.md entry** because "the artifact speaks for itself." → no audit spine; T1 can't run, resume can't reconstruct, user can't verify. The entry IS the phase's witness statement.
- **Delegating brick decomposition.** → intent gets lost in transcription; acceptance criteria flatten, guarantees drift, file lists miss entries. tasks.json is the architect's deliverable; write it yourself.
- **Silent retry-and-hope on phase failure.** → the same failure recurs unobserved; the audit shows progress that didn't happen. Record the failure, decide the recovery move explicitly.
- **Trusting the orchestrator's self-reported Level 3.** → the orchestrator writes "Level 3: passed" without running the software; T1 sees a non-empty field and says PASS; runtime bugs ship. Level 3 must be executed by an independent T1R agent — the orchestrator does not self-certify runtime verification.
- **"Deferred" as a Level 3 status.** → Level 3 is not deferrable. If the software can't be exercised after this wave, that's a gate failure, not a deferral. Record it as FAILED and decide the recovery move.

---

## Prompt skeletons

### T1 compliance check (cheap/fast model)

Spawn an auditor subagent after each phase artifact is filed:

```
Read @tasks/<task-name>.progress.md (focus: the most recent phase entry) and @<artifact path>.

Verify this checklist for Phase <N> — <name> (from progress-schema.md):
- [ ] <checklist item 1>
- [ ] <checklist item 2>
- [ ] ...

For each item, output one line:
  PASS: <item>
  or
  FAIL: <item> — <one-line reason, name the missing evidence>

End with one line: OVERALL: PASS | FAIL.

Do NOT judge content quality. Check only: presence, structure, that evidence references resolve to real files / lines / timestamps.
```

### T1R — Independent runtime audit (cheap/fast model)

Spawn an auditor subagent at every wave gate, Level 3. This agent has NO sprint context — it runs commands and reports observations.

```
You are an independent runtime auditor. You have no knowledge of what this sprint
is building or what "should" work. Your job is to run commands and report exactly
what you observe. Do not interpret, do not fix, do not judge correctness.

**Verification commands** (from context.md):
- Test: `<test command>`
- Runtime: `<runtime command>`

**What this wave touched:**
<list of features/paths/pages affected by this wave's bricks>

**Instructions:**
1. Run the test command. Report: exit code, number of tests, any failures (paste the failure output).
2. Run the runtime command. Report: did the software start? Any errors in stdout/stderr?
3. Exercise each affected feature/path listed above. The form of exercise depends on the project type:
   - **Web/UI:** Load the page/route. Did it render? Blank pages, missing elements, console errors?
   - **CLI:** Run the binary with expected arguments. Did it exit 0? Expected stdout? Run with invalid input — does it error gracefully or panic?
   - **API server:** Hit the affected endpoints with curl. Expected status codes? Expected response shape? Error cases return proper errors?
   - **Library:** Import and call the public API from a test or script. Expected return values? Does it link into the larger build?
   Report for each item: what you observed, any errors/crashes/unexpected output.
4. Write your raw observations to `tasks/<task-name>.wave<N>-audit.txt`.

Do NOT say "everything looks good." List what you observed for each item.
Do NOT skip items because earlier ones passed. Check every item independently.
If a command fails or hangs, report that — do not retry or attempt to fix.
```

### T3R — Independent integration audit (strong model)

Spawn a builder/reviewer subagent at milestones and final sign-off. This agent reads acceptance criteria and exercises the software against them.

```
You are an independent integration auditor. The orchestrator claims all bricks in
this layer passed. Your job is to verify that claim by exercising the software
yourself. You are skeptical — agents frequently report success on partial work,
and unit tests can pass while the integrated feature is broken.

**Acceptance criteria for this layer's bricks:**
<paste acceptance criteria from each brick in the completed layer>

**QA plan test cases (if qa-plan.md exists):**
<paste test cases from qa-plan.md that map to this layer's bricks — these are the
user-facing behaviors the feature must satisfy, not just brick-level criteria>

**Verification commands:**
- Runtime: `<runtime command from context.md>`

**Instructions:**
1. Start the software using the runtime command.
2. For each acceptance criterion AND each QA plan test case: exercise the feature it describes. Report:
   - VERIFIED: <criterion> — <what you observed that confirms it>
   - FAILED: <criterion> — <what you observed instead>
   - UNTESTABLE: <criterion> — <why you couldn't verify it>
3. Check cross-brick interactions: does data flow correctly between the components
   built in different bricks? Does navigation work? Do state changes propagate?
4. Write findings to `tasks/<task-name>.milestone<N>-audit.txt`.

Every criterion gets a verdict. "Tests pass" is not a verdict — describe what you
saw when you exercised the feature. If you can't exercise it, say why.
```

### Phase sub-agent prompt skeleton

Compact, file-reference-driven (output-token-cheap):

```
Read these (your sources of truth):
- @tasks/<name>.context.md
- @tasks/<name>.decisions.md
- @tasks/<name>.design.md
- @<phase-specific design sources, prototypes, specs>

Your task: <one-line phase description>.

Constraints:
- <bounded list, only what's NOT in the files above>

Output: <single artifact at this path>.
```

If a prompt grows beyond ~25 lines, the content belongs in a context file — not the prompt. Output tokens cost ~5× input.
