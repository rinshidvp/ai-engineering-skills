# Agent Guidelines

You're building a brick — a building block that other agents will depend on.

When your brick ships, another agent — one who has never seen your code — will import your types, call your functions, and build their entire brick on the assumption that yours works. They're trusting you. Not because they checked. Because the system told them your brick passed.

If you do a shoddy job — it compiles, the imports resolve, you say it works — you're not saving time. You're spending theirs. They'll debug a problem that isn't in their code. The orchestrator will waste a wave. And when it all unravels, the whole sprint's output gets questioned.

Build something the next agent would be right to trust.

---

## Tests

Tests define truth. If a test fails, fix the code — never the expectation.

Bad: change `assert total == 100` to `assert total == 95` because your code returns 95.
Good: fix `calculate_total()` to return 100.

Never delete, comment out, or modify existing test expectations. If a test seems wrong, surface it — you may be missing context.

---

## Writing Tests

Mock at boundaries only (external APIs, databases). Never mock your own code — if you mock `SandboxRunner`, you're not testing `SandboxRunner`.

Follow the testing discipline in this file (Tests section above). If your
project has a dedicated unit-test skill, follow that too — otherwise the
rules here are the full methodology.

---

## Show, Don't Tell

"Tests pass" is not proof. Evidence is proof.

Bad: `Feature implemented. Tests pass.`
Good: paste the actual test run output showing the specific assertion that proves the guarantee holds.

Run the feature end-to-end. Capture real output. Include it in your report.

---

## Document Shortcuts

Mark shortcuts in code — never hide them. Say so in your report.

| Marker | Meaning |
|--------|---------|
| `SCAFFOLD` | Temporary, MUST remove before production |
| `SHORTCUT` | Works but not robust, needs proper implementation |
| `TODO(production)` | Intentionally deferred feature |

---

## QA Tracker

If `./tasks/*.qa-tracker.json` exists, update it. Never mark `passed` without evidence. Append-only — never remove or modify test definitions.

---

## Implementation Checklist

### Before starting:
- [ ] Read the brick description and acceptance criteria fully
- [ ] Read context.md if referenced in the prompt (architecture, constraints)
- [ ] Read decisions.md — it's READ-ONLY, do not modify
- [ ] Understand existing code patterns before writing new ones

### During implementation:
- [ ] Follow existing patterns in the codebase
- [ ] No defensive error handling without business justification
- [ ] Mark any shortcuts with code markers (SCAFFOLD, SHORTCUT, TODO)
- [ ] **Write** only the files listed in your brick — do not modify files outside your scope. **Read** any file you need to understand existing patterns — reading outside your brick is expected, writing outside it is not.
- [ ] If you find existing code that already does what the brick asks — STOP and report back to the orchestrator. Don't build a duplicate. Say what you found, where it lives, and why it covers the brick's requirements. The orchestrator will decide whether to extend it or proceed. This takes priority over completing the brick.

### Before reporting complete:
- [ ] Code compiles/imports cleanly
- [ ] Existing tests still pass (you didn't break anything)
- [ ] New tests pass and test real behavior
- [ ] Self-verified: feature actually works end-to-end
- [ ] Evidence captured: actual output demonstrating it works
- [ ] Specific assertions from `guarantees_tested` shown — not a count
- [ ] Committed in your worktree with a conventional message describing the code change — `feat(scope): what changed`, not `brick 011 — source events`

---

## Completion Report Format

```markdown
## Brick Complete: <brick name>

### Files Created
- `path/to/file.go` — one-line description

### Files Modified
- `path/to/other.go` — what changed

### Evidence
**GUARANTEE_NAME:** <paste actual test output showing the assertion>

### Shortcuts Taken
- SHORTCUT: <what and where>

### Notes
Observations, decisions, or things the orchestrator should know.
```

---

## Anti-Patterns

**Modifying tests to pass** — Tests define correct behavior. Fix the code.

**"Tests pass" without evidence** — Run the feature. Capture output. Show the assertion.

**Hidden shortcuts** — Mark with SCAFFOLD/SHORTCUT. Say so in your report.

**Writing files outside your brick** — Your brick lists specific files. Write only those. Reading any file for context is fine and expected — but writing outside your scope breaks parallel execution.

**Building when existing code covers it** — Your brick says "create X." You find X already exists. Don't build a second one. STOP and report back: what you found, where it lives, why it covers the requirement. The orchestrator decides next steps. Reporting back is not failure — it's the right move. Building a duplicate is the failure.

**Modifying decisions.md** — READ-ONLY. If you find a conflict, report it. Don't resolve it yourself.

**Creating summary documents** — Do NOT create status files, summary docs, or progress reports. Orchestrator handles progress.md.

**Mocking your own code** — If you mock SandboxRunner, you're not testing SandboxRunner. Mock external boundaries only.

**"76 tests pass" with mocked everything** — Tests that mock your code test mock wiring, not behavior.

**Defensive error handling without justification** — Fail fast unless the business explicitly accepts partial failure.

**Sprint-internal commit messages** — `sprint(session): brick 011 — source events` tells a future developer nothing. Commit messages live in git history forever. Describe the code change: `feat(events): emit source message events from transport sources`. Sprint context belongs in progress.md.

---

## Finding Markers Before Release

```bash
grep -rn "SCAFFOLD:" src/
grep -rn "SHORTCUT:" src/
grep -rn "TODO(production)" src/
```
