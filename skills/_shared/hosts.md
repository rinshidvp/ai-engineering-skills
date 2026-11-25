# Host mapping

The skills in this repo are written host-neutrally: they say "search the code",
"spawn a subagent", "fast tier", "strong tier". This file is the only place that
says what those words mean in each tool. Read it when a skill tells you to spawn
an agent or pick a model and you aren't sure how your host does it.

## Actions

| Action | Claude Code | opencode | Antigravity |
|---|---|---|---|
| Read a file | `Read` | `read` | `read_file` |
| Search code | `Grep` / `Glob` | `grep` / `glob` | `run_command` (ripgrep/PowerShell) |
| Run a command (tests, git, curl) | `Bash` (or `PowerShell` on Windows) | `bash` | `run_command` |
| Spawn a subagent | `Agent` tool (`subagent_type`, optional `model`) | `Task` tool | `invoke_subagent` |
| Broad read-only exploration | `Agent` with `subagent_type: Explore` | `Task` subagent | `invoke_subagent` (`research`) |
| Independent code review | `code-reviewer` agent (installed by `install.ps1`) | `@code-reviewer` | `invoke_subagent` (`code-reviewer`) |
| Plan before building | plan mode (`EnterPlanMode`) | write the plan file directly | write the plan file directly |
| Start a clean context | `/clear`, or a new session | new session | new chat |

## Model tiers

Skills name a **tier**, not a model, so the same instructions work everywhere.

| Tier | Used for | Claude Code | opencode | Antigravity |
|---|---|---|---|---|
| **fast** (runner, auditor, explorer) | Fully specified mechanical work: run tests, apply a known change, find files, compliance checks | `haiku` | your cheap/fast model | Flash |
| **strong** (builder, orchestrator) | Implementation needing judgment: integration, error handling, unclear specs | `sonnet`, or inherit the session model | your strong default | Pro |
| **reviewer** | Independent review, triage of contested findings, design trade-offs | `opus` | your strongest model | Pro |

Why tiers matter: fast models are literal. On an ambiguous brief they
pattern-match and confidently produce something plausible that drifts from the
intent. Give the fast tier only work whose brief leaves nothing to decide, and
keep judgment work (reviews, design calls, triage) on the strong or reviewer
tier. The fast tier costs roughly 5x less, which matters on sprints with many
parallel bricks.

## Effort levels (Smart Zone discipline)

- **Default to Medium effort** for everyday exploration, grilling, planning,
  and normal implementation. High/Extra-High effort on routine exploration
  burns tokens without improving file lookup and pushes sessions into the
  Dumb Zone (> ~150k tokens) faster.
- **Reserve High effort** for final verification (running the app, traces,
  proving behavior), stubborn root-cause debugging, and open-ended web research.

## Claude Code notes

Claude Code ships some workflows that overlap with skills here. Use the
built-in when it fits, and the skill when you need what it adds:

| Need | Use |
|---|---|
| Find bugs in the current diff | built-in `/code-review` |
| Small behavior-preserving cleanup of changed code | built-in `/simplify` |
| Design-level review: SRP, layering, "does this click", is the feature complete | `code-quality` skill or `code-reviewer` agent |
| Review → fix → verify loop with a pass cap | `refine-loop` skill |
| Quick plan for a contained change | plan mode |
| Multi-file feature plan saved to `tasks/` with task breakdown | `implementation-plan` skill |
| Context getting long within one task | auto-compaction handles it; use `session-continuity` when handing work to a new session or another person |
