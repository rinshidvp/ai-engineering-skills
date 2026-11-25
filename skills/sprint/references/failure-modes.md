# Learned Failure Modes

These aren't hypothetical — each traces to a real sprint failure.

---

## Data Loss

**Parallel agents silently overwrite each other.** Bricks E004 and E012 both wrote execution.rs. Last writer won. Earlier agent's work vanished with no error. **Fix:** Worktree isolation — `sprint_tasks.py worktree create` per brick when dispatching in parallel. Merge back with `worktree collect`. File conflict matrix still matters: shared files must be batched into one agent.

**Wave 2 agent reverts Wave 1 edits.** Agent reads source file for context, Edit tool replaces content, extraction from Wave 1 disappears. **Fix:** Commit after every wave gate (checkpoint), so the next wave's worktrees branch from committed state.

**Next wave agents nuke tracked file changes.** Bricks 024-029 modified 15 tracked files. None were committed. Next wave agents restored them to HEAD state. All modifications lost. **Fix:** Self-managed worktree isolation (agents work in isolated copies) + MANDATORY commit after every wave gate. Together these eliminate both within-wave and between-wave data loss.

---

## False Confidence

**Agent reports success on partial work.** Brick 001 hit prompt limits after 42 tool calls. Created test files but never cleaned up source files. Reported nothing — the Task tool returned "Prompt is too long." Next wave built on incomplete foundations. **Fix:** Wave gate verification (grep/ls deliverables before dispatching dependents).

**"Tests pass" is not "feature works."** 25/25 tests passed. Zero tested the actual feature. **Fix:** Require specific evidence — test output showing the new behavior, not just a green count.

**Validation theater.** The sprint reports all bricks passed. Every brick cites test counts. No brick shows the specific assertion that proves its guarantee. The feature ships broken — it was always broken. The tests were testing infrastructure that predated the feature. This is the worst failure mode because it looks like success. **Fix:** `guarantees_tested` on every implementation brick. Name the test, name the assertion. If you can't name it, the test doesn't exist yet.

---

## Merge & Infrastructure

**N-way merge conflicts in shared infra.** 8 parallel agents each independently added the same test dependencies to package.json and build config. Collection produced 8-way merge conflicts. **Fix:** Pre-flight infrastructure scan before wave 1. Set up shared infra once on the main branch, commit it, then dispatch agents from that base. Tell every agent explicitly which files are frozen.

---

## Specification Drift

**Agent modifies reference files instead of target files.** Agent told to "reference V1 source at path/A, create new file at path/B" modifies path/A instead. Paths are similar, agent picks the one that already exists. **Fix:** context.md must explicitly mark reference directories as READ-ONLY with a concrete table mapping "read this -> write here". Agent prompts must include frozen file lists.

**Agent simplifies a load-bearing type definition.** Agent told "create struct per the context doc" built a simplified version. Six downstream bricks consumed it. Required a follow-up sprint. **Fix:** When a brick defines a type that downstream bricks depend on, embed the exact definition in the agent prompt — never reference it indirectly.

---

## Self-Reported Compliance

**Orchestrator acknowledges instruction then does exactly what it warns against.** The sprint guide said "you must run the software" on page 1. The orchestrator read it, quoted it, then wrote "Level 3: deferred" at every wave gate across 4 waves. Every bug found later — nested router crash, race conditions, empty timeline, off-by-one navigation — was a runtime failure invisible to the static and unit-test checks the orchestrator actually ran. The instruction was clear. The agent optimized for completion over compliance. This isn't intentional deception — agents pattern-match to complete tasks and skip the hard parts when nothing structurally prevents it. **Fix:** Level 3 runtime verification is executed by an independent T1R agent (clerk), not self-assessed by the orchestrator. The orchestrator dispatches the audit agent, reads its observations, and makes the pass/fail call — but the observation itself is independent. See `orchestration-pattern.md` for T1R and T3R prompt skeletons.

**T1 rubber-stamps self-reported evidence.** T1 checks that progress.md has a non-empty Level 3 field. The orchestrator writes "Level 3: passed — app loads correctly" without running anything. T1 sees text and says PASS. **Fix:** T1 now verifies that audit artifact files exist at claimed paths and contain actual command output — not just that a text claim exists in progress.md.

---

## Cross-Brick Breakage

**Type change breaks consumers between waves.** A brick changed a field type. Consumers in other modules still used the old type. Nothing compiled between waves. **Fix:** At decomposition, trace consumers of any type/interface change. Either include consumer fixes in the same brick, or note which files break and plan a compile-fix step before the gate.

**Existing guard silently drops new data.** A struct grew new fields, but a serializer's emptiness check was still written for the old shape — silently dropping records. No brick tested the full persistence path. **Fix:** When a brick changes a data shape, tell the agent which existing code serializes or guards that data.
