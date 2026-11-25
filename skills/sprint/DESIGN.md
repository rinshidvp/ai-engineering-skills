# Sprint Skill — Design

You're about to edit the sprint skill. Read this first. It explains why things are the way they are, so you don't undo hard-won decisions or repeat mistakes we already made.

---

## The Problem This Skill Solves

Agents duplicate existing code. Consistently. Across every sprint we've run.

The root cause is not ignorance — agents can be told "don't duplicate" and they'll read the instruction and duplicate anyway. The training reward is task completion. Building fresh code and reporting "done" gets the reward faster than stopping to investigate whether something already exists, reporting back, and waiting for a redirect.

Document-level enforcement doesn't work. We tried:
- Project instruction rules (`AGENTS.md` / `CLAUDE.md`, "check what exists before building")
- DESIGN.md contracts ("this component owns X")
- Brick validation gates ("no brick creates something that already exists")

All of these are semantic, judgment-dependent, and applied at the wrong time. An agent reads "check what exists" and optimizes past it toward completing the brick.

**What does work:** Structural placement at point of action. Checks that fire where the work happens, not in a self-review checklist at the bottom. Concrete artifacts (reuse analysis, design decisions) that become inputs to the next step — not advice to consider.

---

## Key Design Decisions

### Reuse Discovery is mandatory, not complexity-gated

The Input Assessment table originally had "Clear → straight to brick decomposition." This meant clear requests skipped all exploration. But "clear intent" says nothing about what the codebase already has. A developer who says "add a retry mechanism" has clear intent — but doesn't know a retry utility already exists three modules over.

**Decision:** Reuse Discovery appears in every row of the complexity table. It runs before any other upstream phase. Even for single-file changes. The cost is a few clerk Explore agents. The alternative is rebuilding something that exists.

**Without this:** Clear requests skip exploration entirely. The orchestrator decomposes bricks blind to what the codebase already has.

### Reuse analysis goes in design.md, design decisions go in decisions.md

The reuse analysis is a design artifact — what exists, what to extend, what patterns to follow. It belongs in design.md alongside architectural decisions.

The decisions that flow from the analysis — which components you're using and why, constraints you're accepting, expectations about extension points — go in decisions.md. These are commitments that agents must respect (decisions.md is READ-ONLY for agents).

**Why the split:** An agent needs to know "use X" (design.md analysis) AND "extend X's interface, don't wrap it" (decisions.md commitment). The analysis tells you what exists. The decision tells you what to do about it.

### Brick descriptions must say "extend" not "create"

When design.md lists existing code that covers what a brick would build, the brick description must use "extend" or "use" language. Not "create" or "build."

**Why this matters:** Agents follow brick instructions literally. A brick that says "Create a retry mechanism with configurable backoff" will produce a new file even if the agent knows an existing retry utility exists. A brick that says "Extend the existing retry utility to support configurable backoff modes" points the agent at the existing code. The verb in the brick description is the strongest signal the agent receives about whether to build new or extend existing.

**Enforced at:** Decomposition step 4 (inline check with bad/good contrast), validation gate (explicit checkbox).

### Read/write distinction resolves "stay in your lane" tension

The original rule was "Stay within the files listed in your brick — do not modify files outside your scope." This created a structural incentive for duplication: an agent that can't look outside its brick can't discover that existing code covers its task. The escape hatch ("report back if existing code covers it") required agents to violate the rule it sat alongside.

**Decision:** Split into two distinct permissions:
- **Write** only the files listed in your brick
- **Read** any file you need for context

Reading outside your brick is explicitly expected. Writing outside it breaks parallel execution. These are different operations with different consequences, and the skill text now distinguishes them.

**Without this:** Agents interpret lane discipline as "don't read outside your files" and build duplicates because they never discover the existing code.

### Escape hatch takes priority over task completion

The agent guidelines say: "This takes priority over completing the brick." This is a direct counter to the training reward. Without explicit priority ranking, agents resolve the tension between "complete the brick" and "report back if existing code covers it" in favor of completion — because that's what the training scores.

**Without this:** Agent finds existing code, decides building new is faster, completes the brick with a duplicate.

### Wave re-check catches mid-sprint staleness

Bricks are planned against the pre-sprint codebase. By wave 3, the codebase has changed. A brick planned before the sprint that says "create utility X" may now duplicate something wave 2 built.

Step 10 (Reuse Re-Check) runs after every wave gate, before planning the next wave. It asks: do any remaining bricks duplicate something this wave created?

**Without this:** Later waves are planned against stale state. Bricks that were valid when designed are now duplicates of what earlier waves built.

### Milestone reviewer asks about duplication, not just breakage

The original reviewer prompt was: "It's the next morning and something in this layer is broken. What did we miss?" Duplication isn't breakage — it compiles, tests pass, the feature works. A failure-oriented reviewer has no reason to surface it.

The updated prompt adds: "Also: did any brick build something that already existed in the codebase?"

**Without this:** The milestone review is the one independent-eyes check in the entire sprint, and it's blind to the most common quality problem.

### Commit messages describe code changes, not sprint mechanics

The observed failure: git history filled with `sprint(session): brick 011 — source message events`. These messages are meaningless to any developer reading git log after the sprint. "Brick 011" is sprint scaffolding — not a description of what changed.

The collect mechanism makes this consequential: agent commits come into main verbatim via rebase + fast-forward. There is no squash step. Whatever the agent writes is what lands in history.

**Decision:** Agents commit with conventional messages (`feat/fix/refactor(scope): description`). Sprint context (session, wave, brick IDs) belongs in progress.md. The dispatch prompt template specifies this. The agent guidelines checklist enforces it at completion. Step 8 catches stragglers before the next wave.

**Without this:** Sprint-internal messages accumulate in history. After the sprint, `git log` reads like a task tracker, not a codebase changelog.

---

## Known Limitations

These are real failure modes we chose not to fix. Each has a reason. Revisit these trade-offs if the underlying constraints change (model capabilities, token costs, script capabilities).

### Exploration agent's semantic limits

Reuse discovery uses clerk for exploration. Clerk is fast and cheap but literal — it pattern-matches on names, not semantics. It may miss existing code that does the same thing under a different name or in an unexpected location.

**Why not fixed (as of this writing):** Using a more capable model for exploration costs significantly more tokens per sprint. The orchestrator (which is more capable) reads the exploration output and makes the semantic connections. If the exploration agent misses something, the orchestrator's own read of DESIGN.md files is the second line of defense.

**Mitigation:** The exploration instruction says "search broadly: the duplicate often lives in a different module than expected." This nudges toward wider search scope without requiring semantic reasoning.

**Revisit when:** Cheaper models gain better semantic understanding, or exploration token costs drop enough to justify a more capable model.

### Self-check blindspots

The reuse re-check (Step 10) is the orchestrator checking its own prior work. The validation gate is the orchestrator self-evaluating. The same blind spot that missed the duplicate at planning time will miss it at re-check time.

**Why not fixed:** Adding an independent reviewer at every re-check point would double the token cost of every wave transition. The milestone review (Step 9) is the independent-eyes check, and it now includes the duplication question.

**Mitigation:** The milestone review uses a separate agent with fresh context, specifically prompted to look for duplication. This catches what self-checks miss — just not at every wave boundary.

**Revisit when:** Token costs drop enough that an independent re-check agent at every wave gate is affordable.

### Reminders as text, not structural gates

The `<reminder>` tags at the bottom of creating-a-sprint.md and running-a-sprint.md are text that the orchestrator reads once and may internalize imperfectly. They don't block execution.

**Why not fixed:** Structural enforcement would require script-level checks (e.g., "sprint-run script refuses to dispatch until design.md contains a Reuse Analysis section"). The sprint scripts don't currently have this capability, and adding it creates a new maintenance burden. The reminders serve as a last-chance catch for orchestrators who skimmed the procedure.

**Mitigation:** The critical rules are placed at point-of-action in the procedure steps themselves (not just in the reminder). The reminder is redundancy, not the primary mechanism.

**Revisit when:** The sprint script gains a pre-dispatch validation hook.

### Sunk cost after partial implementation

An agent may build significant code before discovering that existing code covers its task. By then, the path of least resistance is to ship what was built rather than discard it and report back.

**Why not fixed:** Structural prevention would require agents to complete a discovery phase before writing any code — but this doubles agent execution time for every brick, including the majority where no duplicate exists. The escape hatch instruction says "STOP and report back," but we can't enforce that an agent stops mid-implementation.

**Mitigation:** The reuse analysis in the dispatch prompt tells agents upfront what exists. If the analysis is complete, agents shouldn't need to discover duplicates during implementation.

**Revisit when:** Agent tooling supports a mandatory "read before write" phase that doesn't double execution time.

---

## Principles for Editing This Skill

These come from the prompt-engineering skill and from observed failures. Follow them when adding or changing skill text.

### Every addition must trace to an observed failure

Don't add speculative rules. If you can't point to "the agent did X wrong, so I added Y," the addition is probably bloat. More text = more tokens = less attention per instruction. The sprint skill is already large.

### Checks at point of action, not in a self-review appendix

If a rule matters, place it where the work happens. A "verify you didn't duplicate" item in a checklist at the bottom of a file will be skipped. The same check inline at the dispatch step will fire.

### Contrast at the decision point

Where agents make judgment calls, show bad vs. good side by side. Concrete pairs calibrate the bar better than abstract instructions.

### Prime, don't prescribe

Set the mindset early. "You're a build pipeline controller" (running-a-sprint.md opening) primes the orchestrator to think in terms of verification and evidence. A list of 20 rules without the framing would be less effective.

### Nudge, don't tutor

Short reminders for things agents tend to skip — not tutorials explaining what they already know. "Reporting back is not failure — it's the right move" is a nudge. A paragraph explaining why duplication is bad is a tutorial the agent doesn't need.

### The skill is generic

No project-specific paths, component names, or examples that only make sense in one codebase. When editing, keep examples generic or clearly marked as illustration.

---

## File Map

| File | Purpose | Edit frequency |
|------|---------|---------------|
| `SKILL.md` | Entry point: schema, script reference, failure modes, agent selection | Rare — stable |
| `references/creating-a-sprint.md` | Sprint-create workflow: assessment, reuse discovery, upstream planning, decomposition, validation | When planning process changes |
| `references/running-a-sprint.md` | Sprint-run workflow: the loop, dispatch, collect, verify, gates, commits | When execution process changes |
| `references/agent-guidelines.md` | Rules for implementation agents: tests, evidence, checklist, anti-patterns | When agent behavior needs correction |
| `references/planning-funnel.md` | Upstream phase details: brainstorming, spec, QA, design, implementation planning | When adding/changing phases |
| `references/brick-design.md` | Brick schema, sizing, acceptance criteria, files field | When brick format changes |
| `references/wave-planning.md` | Wave ordering: testability tree, compilation tree, layers | When parallel execution strategy changes |
| `scripts/sprint_tasks.py` | CRUD script for tasks.json, worktree management | When adding commands or fixing bugs |
| `DESIGN.md` | This file — design decisions about the skill itself | When design decisions change |

---

## Change Log

### 2026-03-04 — Reuse Discovery Phase

**Problem:** Comprehensive analysis identified 22 failure modes where agents duplicate existing code. Root cause: no exploration phase discovers what exists before bricks are designed. The single anti-duplication rule ("no brick creates something that already exists") was semantic, judgment-dependent, and applied too late.

**Changes:**
- Added mandatory Reuse Discovery phase to creating-a-sprint.md (runs for all complexity levels)
- Input Assessment table updated: every row includes Reuse Discovery
- Reuse Analysis output goes to design.md; Design Decisions go to decisions.md
- Brick descriptions must say "extend"/"use" when reuse analysis lists existing code (enforced at decomposition step 4 and validation gate)
- Read/write distinction in agent-guidelines.md resolves "stay in your lane" tension
- Agent escape hatch: "report back if existing code covers it" — explicitly takes priority over task completion
- Wave re-check (Step 10) catches mid-sprint staleness
- Milestone reviewer now asks about duplication, not just breakage
- `<reminder>` tags at end of both workflow files for critical rules
- Mid-sprint brick addition requires checking reuse analysis first

**Analysis method:** Decision tree mapping of all failure paths, followed by stress-test of the fixes against the same failure modes. Three secondary fixes applied after stress-test: (1) input assessment table no longer contradicts reuse discovery, (2) brick description language enforcement, (3) read/write permission distinction for agents.

### 2026-03-14 — Commit message clarity + prompt compactness

**Problems (observed in agent-hardening sprint):**
1. Git history contained sprint-internal messages (`sprint(session): brick 011 — X`). Agents had no commit format guidance, and the collect mechanism brings agent commits into main verbatim.
2. Step 8's commit template used the same sprint-internal format, contradicting Step 5.
3. Agent prompts grew to 50-60 lines by expanding the 12-item dispatch checklist into paragraphs, re-stating content already in context files.

**Changes:**
- Step 4 (Dispatch): Replaced 12-item checklist with compact prompt template. `@`-references for context/decisions files instead of inline dumping.
- Step 5 (Collect): Added commit format guidance with bad/good contrast pair.
- Step 8 (Commit Checkpoint): Split into worktree/no-worktree paths. Fixed commit message format.
- agent-guidelines.md: Added commit checklist item and sprint-internal commit anti-pattern.
- agent-guidelines.md: Compressed 235→136 lines. Applied nudge-don't-tutor to Tests, Writing Tests, Show Don't Tell, Document Shortcuts, QA Tracker sections. Tutorials replaced with one-line rules + tight bad/good contrasts.
- creating-a-sprint.md: Added delegation guidance in Output section — orchestrator makes decomposition decisions, delegates artifact writing (JSON, companion files) to coder.
- DESIGN.md: Added "Commit messages describe code changes" design decision.
