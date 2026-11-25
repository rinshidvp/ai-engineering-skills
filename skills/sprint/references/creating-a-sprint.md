# Creating a Sprint

Self-contained workflow for decomposing work into a brick DAG. Read `../SKILL.md` first for schema, script reference, and failure modes. Read `orchestration-pattern.md` (same folder) before dispatching any phase — the main agent orchestrates fresh sub-agents per phase, never doing the phase work itself.

---

## Sprint Initialization (before any phase)

Before triage, brainstorming, or anything else.

**1. Pending changes.** Survey the working tree.

- Run `git status` and look at what's modified.
- Low-risk pending (docs, formatting, small isolated tweaks, tests): commit as a pre-sprint snapshot, e.g. `chore: pre-sprint snapshot` or a more specific conventional message if the content is coherent. Don't be annoying — just commit.
- Looks risky (mid-flight large refactor, broken build, anything that could mislead later debugging): list the files to the user with a one-line summary and ask whether to commit, stash, or abort. Default to committing if in doubt.
- Either way, record the SHA (or "stashed", or "none") in progress.md metadata.

**2. Branch.** Create and switch the working tree to `sprint/<YYYY-MM-DD>-<task-slug>`:

```bash
git checkout -b sprint/$(date +%Y-%m-%d)-<task-slug>
```

All sprint work — including worktrees spawned during running-a-sprint — branches from here. Sprint completion leaves the branch for the user to PR. No auto-merge.

**3. Initialize progress.md.** Write the header per `progress-schema.md` (same folder):

```markdown
# Sprint: <task-name>

## Metadata
- branch: sprint/<YYYY-MM-DD>-<task-slug>
- created: <epoch_ms>
- pending-changes-at-start: <committed | stashed | none>
- pending-changes-commit: <sha if committed>
```

Every phase below appends a structured entry to progress.md per the schema. T1 Clerk compliance checks parse this file.

---

## Per-Phase Protocol

Every phase below runs as a fresh sub-agent (the only exception is brick decomposition — that's the orchestrator's own deliverable). After each phase:

1. **File the artifact** at the path named in the phase.
2. **Append a progress.md entry** per `progress-schema.md` — name the artifact, the evidence references, the agent used, the timestamp.
3. **Spawn T1 compliance check** (cheap/fast auditor subagent) — reads progress.md + the artifact, runs the phase's checklist from `progress-schema.md`. T1 checks presence + structure + that evidence references resolve. It does NOT judge correctness.
4. **If T1 fails**: fix the gap and re-check. If you can't resolve it, bubble to the user per `orchestration-pattern.md`.
5. **If the phase has a user gate**: present the artifact, ask for explicit approval, record response text + timestamp in the progress entry. Don't proceed without it.

The orchestrator never does the phase work itself — it dispatches, files, validates, gates. See `orchestration-pattern.md` for full rationale, cost discipline, and prompt skeletons.

---

## Input Assessment

Read the request. Before decomposing bricks, decide how much upstream planning is needed.

**Is the idea fuzzy or clear?**

- **Fuzzy** ("add caching", "improve performance", "can we do X") → upstream planning required, start with brainstorming
- **Clear with unknowns** (specific scope, but integration/API questions remain) → discovery phase, then decompose
- **Clear** (specific scope, no unknowns) → reuse discovery, then decompose

**Assess complexity to determine which phases to run:**

| Size | Signs | Upstream Phases |
|------|-------|-----------------|
| Small (1-2 files, no unknowns) | Single function, obvious change | Reuse Discovery → decompose |
| Small (1-2 files, with unknowns) | External API, unfamiliar library | Reuse Discovery → Discovery → decompose |
| Medium (3-5 files) | Multiple components, some integration | Reuse Discovery → Design → Implementation Plan → decompose |
| Large (5+ files, multi-component) | Architectural decisions, stakeholder requirements | Reuse Discovery → Spec → QA Plan → Design → Implementation Plan → decompose |
| Fuzzy idea (any size) | Vague request, multiple interpretations | Brainstorm → Reuse Discovery → then scale by size above |

Reuse Discovery appears in every row. Clear intent ≠ clear codebase. Implementation Planning appears for multi-file features — see `references/planning-funnel.md` ("never skip for multi-file features"). Start minimal on everything else.

---

## Reuse Discovery — Always Run

> Role map: `clerk` = runner (fast tier), `coder` = builder (strong tier). The Agent Selection table in `orchestration-pattern.md` is the source of truth; tier → model per host is in `../../_shared/hosts.md`. Legacy names in this file map accordingly.

Before decomposing bricks, survey the codebase for what already exists. This runs regardless of complexity — a "clear" request means the *intent* is clear, not that you know what the codebase already has.

**Spawn Explore agents (clerk) in parallel:**

1. **Components & utilities** — find reusable code in the areas this feature touches. Search broadly: the duplicate often lives in a different module than expected.
2. **Patterns** — how does existing code solve similar problems? What conventions must the new feature follow?
3. **Constraints** — read `DESIGN.md` files for every module in scope. Extract contracts, ownership boundaries, frozen interfaces.

**Output goes to two places:**

**`<task-name>.design.md` — Reuse Analysis section.** This is where the inventory of existing code lives. If a design doc already exists from the Design phase, append this section. If no Design phase ran, create the file with just this section.

```markdown
## Reuse Analysis

### Existing code to use or extend
- `web/src/hooks/useRetryableRequest.ts` — retry logic with configurable backoff. Extend for this feature instead of building new.
- `server/src/utils/parse.rs` — already handles the format we need.

### Patterns to follow
- All data hooks use the `silent` refetch pattern (see useSessionDetail.ts).
- Error boundaries wrap at page level, not component level.

### Constraints from DESIGN.md
- BoardView owns column state — no external code may change activeColId.
- SSE events must never trigger loading skeletons.

### Nothing found for
- Notification system — no existing toast queue, will need to build.
```

**`<task-name>.decisions.md` — Design Decisions section.** Record the *decisions* that flow from the analysis: which components you're using and why, constraints you're accepting, expectations about how existing code will be extended.

```markdown
## Design Decisions

### Components we're using
- DECISION: Use `useRetryableRequest` for retry logic — it already handles backoff and abort. Extend its config interface, don't wrap it.
- DECISION: Reuse `RetroToast` for notifications — it's wired into App.tsx. Don't create a second toast system.

### Constraints we're accepting
- BoardView owns column state — bricks MUST NOT programmatically change `activeColId`
- SSE refetches use `silent=true` — any new data hook MUST follow this pattern

### Component expectations
- `useRetryableRequest` will be extended (not replaced) to support the new retry modes
- `RetroToast` API is frozen — new notification types must fit its existing interface
```

Bricks reference the design.md reuse analysis. A brick that says "create retry hook" when `useRetryableRequest` is in the analysis is a design failure caught before dispatch, not after.

If exploration finds that the feature (or a significant piece of it) already exists — stop and surface this before decomposing any bricks.

**User gate:** Present the Reuse Analysis and Design Decisions to the user. "Does this look right? Any existing code I missed? Any constraints I should know about?" Record approval with timestamp in the progress entry. Do not proceed to Specification Grounding without it — the reuse analysis shapes every brick downstream.

---

## Specification Grounding — Always Run

After Reuse Discovery, before decomposing bricks. The architect must know what they're building at granular detail — not "a quotas page" but what sections it has, what data each section shows, what interactions exist. Not "a retry endpoint" but what it accepts, what it returns, what the edge cases are.

The problem this solves: an architect who has API types, component libraries, and a plan file *feels* like they know enough. They pattern-match "quotas page" into a plausible layout. "Retry endpoint" into a plausible contract. Every detail feels like knowledge, not invention. Eight agents ship. Everything compiles. Tests pass. The output matches nothing the user intended because the details were inferred, not sourced.

Inference feels like knowledge. This step forces the difference to surface.

### 1. Find design inputs

Grep plan files, handoff docs, specs, context files, and project instructions (`AGENTS.md` / `CLAUDE.md` if present) for references to design sources. Search broadly — UI and backend projects use different terminology:

```bash
grep -ri 'prototype\|mockup\|design.*ref\|visual.*ref\|handoff\|brief\|spec\|rfc\|schema\|contract\|abi\|protocol\|interface.*def' tasks/ tmp/ *.md
```

Whatever the project type, the design source varies:
- **UI:** prototype, mockup, design brief, styleguide, wireframe
- **API:** OpenAPI spec, contract doc, existing endpoint being replicated
- **Backend/systems:** design doc, CONTRACT blocks, behavioral spec, test cases, protocol spec, ABI definition, wire format specification
- **CLI:** requirements doc, existing usage patterns, CLI spec, man page, help text
- **Any:** a conversation where the user explicitly defined the behavior

Read every design source you find. Not the reference to it — the file itself. If the plan says "prototype at `tmp/v2/`" — read the files in `tmp/v2/`. If the spec references an OpenAPI schema — read the schema.

If no design source exists for a significant part of what you're building, that's a gap. Three resolution paths:

1. **User provides a source** — they sketch it, write a brief, or point to an existing reference. Best outcome: the grounding audit has real material.
2. **Co-create interactively** — the architect proposes a skeleton ("here's what I'd build — sections A, B, C with these interactions"), presents it to the user, and the user corrects it. The validated skeleton becomes the design source. This is the most common path for features described in a sentence.
3. **Feature is too underspecified** — if the user can't validate a skeleton and doesn't want to write a spec, the feature isn't ready for a full sprint. Scope a discovery/spike sprint first to produce the design source, then run the implementation sprint against it.

Do not fill the gap with inference. Do not proceed with an unvalidated architect-invented skeleton — that's inference with extra steps.

### 2. Grounding audit

For each major output of the sprint (each page, endpoint, module, service — whatever the unit of work is), spawn a clerk agent. The agent tries to produce a skeleton of what that unit looks like — not real code, but the concrete structure. The goal is to surface every detail the architect would need to write a brick, and flag anything that can't be sourced.

**Prompt pattern:**

> You are auditing a specification before implementation begins. Do NOT write real code. Produce a SKELETON — the structure of what will be built.
>
> **Your inputs** (read all of these first):
> - [list design source files: prototype pages, API specs, design docs, etc.]
> - [list relevant existing code: types, components, patterns]
> - [plan/spec/handoff file if exists]
>
> **Your task:** For [unit of work], describe the concrete structure:
> - For a page: every section in order, every field/column in each section, every interaction (click, expand, navigate), every state (loading, empty, error).
> - For an API endpoint: every parameter, every response field, every error case, every edge case.
> - For a module: every public function signature, every type, every edge case, every failure mode.
> - For a script: every subcommand/flag, every input/output format, every error case.
>
> **Rules:**
> - Every detail must come from a source file you read. Cite the file path.
> - If you cannot find a detail in any source, mark it as **ASSUMPTION: [what you guessed and why you couldn't find it]**.
> - There is nothing to guess. Every assumption is a gap that must be resolved before building.
> - Do not fill gaps with plausible defaults. Flag them.
>
> **Output:** The skeleton, then a section listing ALL assumptions found.

**Cost note:** If you're running this audit for more than one unit of work, write the prompt body to a file once (e.g., `tasks/<name>.grounding-prompt.md`) and `@`-reference it in each sub-agent's prompt instead of pasting the body N times. Output tokens cost ~5× input — repeated inline prompts add up fast.

Run one agent per unit of work, in parallel. They're cheap (clerk) and fast.

**Reading the results:**

- **Zero assumptions** → the specification is grounded. Proceed to decomposition. The skeleton becomes input to brick descriptions — it's the concrete detail each brick implements.
- **Assumptions found** → these are unknowns. For each one:
  - Can it be resolved by reading another file? → read it, re-run.
  - Does it require a decision? → make it explicitly, record in `decisions.md`.
  - Does it require user input? → ask. "The prototype doesn't specify what happens when X. What should happen?"
  - Is the design source incomplete? → surface it. "The spec covers endpoints A and B but not C. Do we need C?"

Do not proceed to brick decomposition with unresolved assumptions. A brick built on an assumption is a brick that might be wrong — and every brick downstream of it inherits the risk.

---

## Upstream Planning (when needed)

Run these phases before brick decomposition. Each has a review checkpoint — stop and get explicit approval before proceeding. Detail on each phase: `planning-funnel.md` (same folder).

**Brainstorming** (optional skill — follow `planning-funnel.md` inline process)
- When: idea is vague or fuzzy
- Output: refined direction ready for next phase
- Checkpoint: "Does this capture what you want to build?"

**Requirements** (optional skill — follow `planning-funnel.md` inline process)
- When: large feature, external stakeholders, multiple interpretations possible
- Output: `./tasks/YYYY-MM-DD-<title>.spec.md`
- Checkpoint: "Requirements clear? Scope agreed?"

**QA Planning** (optional skill — follow `planning-funnel.md` inline process)
- When: large feature with multiple behaviors to verify
- Output: `./tasks/YYYY-MM-DD-<title>.qa-plan.md`
- Checkpoint: "Test cases cover requirements?"

**Design** (`software-design` skill, in this repo)
- When: any multi-component or multi-layer feature; whenever brick boundaries would otherwise be invented from intuition rather than derived from contracts
- Output: `./tasks/YYYY-MM-DD-<title>.design.md` — components, layers, GUARANTEES / EXPECTS / FAILURE BEHAVIOR per component
- Checkpoint: "Layers right? Component contracts clear? Validated by user before brick decomposition."

**Implementation Planning** (`implementation-plan` skill, in this repo)
- When: always for multi-file features
- Output: `./tasks/YYYY-MM-DD-<title>.plan.md`
- Checkpoint: "Plan executable? Tests identified?"

At every checkpoint: stop, present the deliverable, ask the checkpoint question, wait for explicit approval before proceeding.

---

## Brick Decomposition

Read `brick-design.md` (same folder) before decomposing. A brick is a building block — a verified unit that downstream bricks depend on. If you design bricks as tasks ("produce these files"), agents will treat them as tasks. If you design bricks as building blocks ("deliver this guarantee so the next brick can trust it"), agents will build accordingly. The mindset starts here, at planning time.

**Calibration:**

Bad brick: "Set up the data layer" — unclear scope, no named files, unclear when done.
Good brick: "Create User and Session models in models.rs with serde derives" — one agent, named files, testable output.

Bad criteria: "Tests pass." / "Works correctly."
Good criteria: "`cargo test models::tests::test_user_default` → asserts `user.name == \"\"`."

For every brick, ask: **"How will the wave gate verify this brick holds weight?"** If you can't answer that at design time, the brick's acceptance criteria are incomplete and agents will fill the gap with "it compiles."

If a design doc has GUARANTEES or CONTRACT blocks, extract the component graph from those blocks. Dependencies come from contracts, not intuition.

For full sizing and criteria guidance: `brick-design.md` (same folder).
For wave ordering: `wave-planning.md` (same folder).

**Process:**

1. **Understand** — read `DESIGN.md` for every module in scope, then spec/context/design references. If the plan, handoff, or spec references a prototype, mockup, design brief, API schema, or any other design source — read it. Not the reference. The file. Use the grounding audit skeletons as the concrete detail for what each brick produces.
2. **Discuss** — surface assumptions, propose approach
3. **Decide** — capture in `<task-name>.decisions.md`
4. **Outline** — draft the brick decomposition as a summary: brick names, one-line descriptions, wave plan, key dependencies, and judgment calls. Don't write tasks.json yet.
5. **Adversarial review** — spawn a strong-model review subagent to attack the outline. The reviewer has not seen your reasoning — they see only the outline, the design doc, and the codebase. Their job is to find what you missed.

   Prompt the reviewer with the outline and:

   > You're reviewing a sprint plan before execution. Your job is to find failure modes, not confirm the plan is good. Attack it:
   >
   > 1. **Blind spots** — what will break that isn't covered by any brick? Cross-brick seams, missing error handling, integration gaps.
   > 2. **Verification gaps** — which bricks have no meaningful way to prove they work? "make check passes" is not proof. What would a real test look like for each brick?
   > 3. **Dependency risks** — which bricks will block the most work if they ship wrong? Are those bricks well-specified enough that an agent can't misinterpret them?
   > 4. **Technology footguns** — what are the common mistakes in this stack that agents will make? These become the anti-pattern registry in context.md.
   > 5. **Scope creep** — any brick that's trying to do too much for one agent session?
   > 6. **The pre-mortem** — it's 2 weeks from now and this sprint shipped broken. What went wrong? What wasn't tested? What assumption was wrong?

   Surface findings to the human alongside the outline. Fix the plan before writing tasks.json. This is the "measure twice" step — fixing a brick in an outline costs nothing, fixing it after 3 waves of agents built on it costs everything.

6. **Decompose** — after outline approval, write bricks to tasks.json. For every brick as you write it:

   **Reuse check (per brick):** Cross-reference against the Reuse Analysis. If design.md lists existing code that covers what this brick would build, the description must say **"extend"** or **"use"**, not "create" or "build." Bad: "Create a retry hook with backoff." Good: "Extend `useRetryableRequest` to support configurable backoff modes."

   **Evidence check (per implementation brick):** Fill in `guarantees_tested` with a named test + named assertion. If you can't name the evidence, the brick's acceptance criteria are incomplete — fix them now, not at the gate.

   **File conflict check (per brick):** If this brick's `files` overlap with another brick, either batch them into one agent or add a dependency so they run sequentially. Parallel agents writing the same file = silent data loss (see `references/failure-modes.md`).

   **Type consumer check (per brick that changes a type/interface):** Trace consumers. Fix same-module consumers in this brick. List cross-module consumers as known breakage or schedule a dependent brick.

   **Load-bearing type check:** If a brick defines a type consumed by 3+ other bricks, write out the exact definition so it can go inline in the agent prompt — indirect references get simplified by agents.

   **CONTRACT check (per brick that creates a new source file):** Include in acceptance criteria: "CONTRACT block at top of file."

   **QA plan cross-reference (when qa-plan.md exists):** Every test case in qa-plan.md must map to at least one brick's acceptance criteria or `guarantees_tested`. If a test case has no brick — either the decomposition is missing a brick, or the test case should be dropped from the plan. Unmapped test cases are gaps that won't be verified until sign-off, when they're expensive to fix.

   Incorporate findings from the adversarial review — add anti-patterns to context.md, tighten acceptance criteria, add missing bricks.

7. **Final validation sweep** — confirm nothing slipped through:

   - [ ] Wave 1 bricks are independently testable now
   - [ ] No two bricks build similar logic — if they need shared code, there's an extraction brick first
   - [ ] Specification grounding ran — every brick's details trace to a source the architect actually read. No brick contains details inferred from the name alone.
   - [ ] Closing bricks are present (see below)

---

## Closing Bricks

Implementation bricks build the feature. Closing bricks verify the work is
durable — that the next session (which has zero context) can understand,
maintain, and extend what was built.

### What goes IN implementation bricks

**CONTRACT blocks** — written by the implementation agent, not a closing brick.
The agent writing the code has full context on what the component guarantees,
expects, and refuses.

Add to acceptance criteria of any implementation brick that creates a new
source file:

> "CONTRACT block at top of `<file>` documenting GUARANTEES, EXPECTS, FAILURE BEHAVIOR, DOES NOT."

The `software-design` skill defines the CONTRACT format.

**DESIGN.md** — the design document should exist alongside code BEFORE
implementation starts (see `software-design` skill). In a sprint,
the design is drafted in `tasks/<name>.design.md` during design discussion,
then promoted to `<module>/DESIGN.md` before bricks are dispatched.
Implementing agents read DESIGN.md to understand what to build. If
implementation reveals the design needs updating, the implementing agent
updates DESIGN.md in the same brick.

Add to acceptance criteria of implementation bricks that change component
boundaries or contracts:

> "Update `<module>/DESIGN.md` if component relationships or boundaries changed."

### What gets its own closing brick

**Design documentation review** — verify that DESIGN.md and CONTRACT blocks
are complete, consistent, and tested. This is verification, not creation —
the design docs should already exist from the design phase and implementation
bricks.

Add this brick when: the sprint creates or modifies 2+ components in the same
module, or creates a new module.

```
{
  "name": "Design documentation review",
  "description": "Verify design documentation for <modules>. Check: (1) DESIGN.md exists and describes every component. (2) Every source file has a CONTRACT block. (3) CONTRACT blocks are consistent with DESIGN.md. (4) Every GUARANTEE has a test. Fix any gaps found.",
  "type": "test",
  "depends_on": [all implementation brick IDs],
  "files": ["<module>/DESIGN.md", ...]
}
```

Type is `"test"` — it's verification, not new functionality. `guarantees_tested`
is not required for type `"test"`.

**Assumption validation** — validate assumptions about external system behavior that the sprint's design depends on.

Add this brick when: `decisions.md` lists assumptions about how an external system, API, or protocol behaves. If the sprint only touches internal code with no external dependencies, skip this.

Trigger examples:
- "JMAP server-side `from` filter uses substring matching" → validate with a real JMAP query
- "WhatsApp `NormalizeMessage` sets `msg_type` before media download" → validate by reading the code path or writing a spike
- "SQLite UPSERT handles concurrent writes" → validate with a concurrency test

```
{
  "name": "Validate: <assumption>",
  "description": "Verify assumption from decisions.md: '<assumption>'. Write a test or spike that proves it. If the assumption is wrong, document the actual behavior and flag what needs to change.",
  "type": "discovery",
  "depends_on": [],
  "files": ["<test or spike file>"]
}
```

Type is `"discovery"` — the outcome might change the design. These bricks can often run in wave 1 (no code dependencies) since they test existing behavior, not new code.

### When to skip closing bricks

- **Skip design synthesis** for single-file changes, bug fixes, or sprints where no new components are created.
- **Skip assumption validation** when the sprint has no external dependencies and `decisions.md` lists no assumptions about system behavior outside this codebase.
- **Never skip CONTRACT blocks** in implementation bricks — a new source file without a CONTRACT block is incomplete work.

---

## Output

```bash
# From the sprint skill folder (or globally if installed):
uv run scripts/sprint_tasks.py init tasks/<task-name>.tasks.json \
  --session "<task-name>" \
  --objective "Brief objective text"
# No uv? Use: python scripts/sprint_tasks.py init ...
```

**After running `init`, read each created file before writing to it.** The Write tool rejects writes to files that haven't been read in the current session — even files you just created.

Your job is decomposition and judgment. The tasks.json is your deliverable — you write it.

**Why you don't delegate this:** A previous sprint delegated tasks.json writing to a coder agent. The planner described bricks in natural language, coder serialized them. The result: acceptance criteria got flattened, guarantee names drifted from the design doc, and file lists had omissions. The planner approved it without reading carefully because they'd already "done the thinking." Delegating your own deliverables is how intent gets lost. The agent writing the JSON didn't do the decomposition — they're transcribing without understanding.

Write the bricks directly into tasks.json. If the format is mechanical friction, use the sprint_tasks.py script to scaffold, then edit. But the decomposition, the acceptance criteria, the guarantee names — these flow from your judgment. Don't route them through a translator.

Also create `<task-name>.context.md` when the sprint touches multiple packages — the 20% agents always need (architecture, key constraints, type definitions). Reference the 80% (full design docs) by path inside context.md.

---

## Failure Protocol (planning phases)

When a phase sub-agent fails or T1 surfaces an unresolvable gap:

1. Record the failure in progress.md (what happened, what was produced, the failure mode).
2. Decide the recovery move explicitly:
   - **Retry** if the failure was transient or the agent had insufficient context — re-spawn with a better-curated package.
   - **Escalate to user** if the failure exposes a genuine unknown (grounding audit produced an unresolvable ASSUMPTION, design produced contradictory contracts, adversarial review surfaced a blocker that needs human judgment).
   - **Skip with rationale** only if the phase is genuinely not needed for this scope; record the rationale in the progress entry.
3. Never silently retry. Never silently skip. The orchestrator's recovery decision is itself an audit-logged step.

For execution-phase failures (brick fails, wave gate fails), see `running-a-sprint.md` § Failure Protocol.

---

<reminder>
BEFORE decomposing: Reuse Discovery and Specification Grounding MUST both run — no exceptions. All assumptions resolved. design.md has Reuse Analysis. decisions.md has Design Decisions. If feature already exists — STOP.

BEFORE brick decomposition (multi-component): design.md with GUARANTEES/EXPECTS/FAILURE BEHAVIOR validated by user. No approval = no decomposition.

BEFORE writing tasks.json: outline → adversarial review → human approval → THEN write. Per-brick checks are inline in step 6 above.

AFTER implementation bricks: add closing bricks (design synthesis for multi-component, assumption validation when decisions.md lists external assumptions).

Do NOT create summary documents. Do NOT delegate tasks.json writing.
</reminder>
