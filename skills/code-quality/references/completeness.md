# Implementation Completeness

A fresh-agent review for blind spots after finishing a feature. When you're close to the work, you have blind spots. You know what you *intended* to do, so you might not notice what you *forgot*. This workflow is that question.

## How to Use This

**Your context is the session. The agent's context is money.** Don't waste either.

**Pass (cheap):**
- File paths you modified
- Function/class names you changed
- The feature or API this is part of
- Related components worth checking
- What you were trying to accomplish (one sentence)
- Areas you're uncertain about

**Never include (expensive):**
- Code snippets or diffs
- File contents
- Detailed explanations of what the code does

Point, don't paste. Tell the agent where to look. Let it do the reading and verification.

## Invoke the Agent

Spawn an independent reviewer subagent (strong model) with a prompt like:

```
Review [feature name] — completeness check.

Implemented [brief description].

Modified:
- path/to/file.py (function_name)
- path/to/config.py (new setting)

Affects: [the API/feature this is part of]

Also check: [related component], [other API that uses this]
```

Use the `code-reviewer` agent, or any independent subagent on the reviewer tier (`../../_shared/hosts.md`). Include only file paths and names. Don't paste code; let the reviewer read the files.

## Decision Chain (Critical for Accurate Reviews)

Without the decision chain, the reviewer can only check code quality — not whether the code matches what was agreed. It will flag intentional decisions as bugs.

**If a sprint session exists**, include sprint context in the reviewer prompt:

```bash
# sprint task state (use python instead of uv run if uv isn't installed):
uv run <sprint-skill-dir>/scripts/sprint_tasks.py list tasks/<name>.tasks.json
# plus: decisions file (why things were built this way),
# progress file (what was attempted, what passed),
# tasks/<name>.objective.md (objective and current state)
```

Include the output in the reviewer prompt. It gives the reviewer decisions (why things were built this way, not just what), brick list (what was attempted, what passed, what was pivoted), and objective (current state).

**If there's no sprint**, find the task files manually:

```bash
ls tasks/*.md
```

Include file paths in the reviewer prompt alongside source file paths. The reviewer needs the design doc and handoff to understand WHY decisions were made.
