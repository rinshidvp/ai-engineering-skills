# Session Handoff Template

Living document: Section 1 is updated each session to reflect current truth. Section 2 is append-only history.

---

```markdown
# <Task Name> — Handoff Document

> **LIVING DOCUMENT**: Section 1 is updated each session. Section 2 is append-only.
>
> ## Instructions for Future Agents
>
> **On session start:**
> 1. Read this file and any linked spec/design files
> 2. Check "Current Phase" and "Open Items" to know where to continue
>
> **During session:**
> - Update "Current Phase" if you advance to a new phase
> - Update "Open Items" as items are resolved or new ones surface
>
> **On session end:**
> 1. Update Section 1 with current state
> 2. Append a new entry to Section 2 (Session Log)

---

## Section 1: Current State

### Objective
<What we're building and why. 2-3 sentences.>

### Current Phase
<Phase name> — <IN PROGRESS | COMPLETE | BLOCKED>

### Decisions & Rationale
1. **<decision>**: <rationale> (rejected: <alternatives>)

### Explicit Constraints
- <"must" and "must not" — output format, naming, tech stack, do's and don'ts>
- <user opinions captured as constraints>

### Approved Outputs & Assets
- <anything the user accepted as final, with exact wording/specs>
- <if approved-with-tweaks, capture the TWEAKED version>

### Scope & Boundaries
- **Included**: <what's in scope>
- **Excluded**: <what's explicitly out>
- **Deferred**: <"do later" items — DO NOT implement now>

### Learnings & Gotchas
- <insight about codebase, architecture, or domain>
- <non-obvious constraint or surprising behavior>

### Dead Ends
- <what was tried, didn't work, and WHY — prevents next agent from repeating>

### Quick Wins
- <low-effort improvements noticed but not yet addressed>

### Open Items
1. <item needing resolution>
2. <UNSPECIFIED: items where the answer is unknown — ask, don't guess>

### Key Files
| File | Purpose |
|------|---------|
| `relative/path/to/file` | <what's in it and why it matters> |

### Suggested Skills
- `<skill-name>` — <why the next session should load it>

### Environment Setup
```bash
# Verified commands to get into working state
cd <project path>
<only commands that were actually run and confirmed working>
```

### How to Resume
1. Read <list of files>
2. Run Environment Setup commands above
3. Continue with <next action>

---

## Section 2: Session Log

### Session 1 — YYYY-MM-DD

**Phase**: <phase name> → <status>

**Work done**:
- <bullet>

**Learnings**:
- <what we discovered>

**Dead ends**:
- <what was tried and didn't work>

**Blockers surfaced**:
- <blocker> (if any)

---

<!-- NEXT SESSION: Append below this line -->
```
