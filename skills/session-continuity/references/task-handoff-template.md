# Task Handoff Output Template

Print this directly — do not write to a file. The user copies it into a new chat.

---

```markdown
## Context

<What was being built, what state it's in now. Brief but complete — the new agent has zero prior context.>

## Decisions Already Made

<Each decision with rationale. Frame as SETTLED — the new agent must not re-litigate these.>
- **<decision>**: <rationale> (rejected: <alternatives>)

## Constraints

<Explicit instructions, user preferences, "must" and "must not">
- <constraint with WHY if not obvious>

## Learnings & Gotchas

<What was discovered. Dead ends. Things that break. Non-obvious behavior.>
- <learning>

## Dead Ends (Don't Repeat These)

<What was tried, failed, and WHY. High value — prevents wasted cycles.>
- <approach>: <why it failed>

## Quick Wins

<Low-effort improvements noticed but not yet done. Skip section if none.>
- <quick win>

## Approved State

<What's been built and accepted. Exact specs of accepted outputs.>
<If approved-with-tweaks, describe the tweaked version.>

## Key Files

| File | What's In It |
|------|-------------|
| `relative/path` | <brief> |

## Suggested Skills

- `<skill-name>` — <why the next session should load it>

## Task

<REASON from user — what the new agent should do and why we're starting fresh>

## Next Steps

1. <step with acceptance criteria>
2. <step with acceptance criteria>
```
