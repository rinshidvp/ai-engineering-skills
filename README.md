# AI Engineering Skills & Prompt Sheet

A clean, host-neutral library of **AI Agent Skills**, an independent **`code-reviewer`** agent, and a ready-to-use **`PROMPT-SHEET.md`** built for strategic software engineering with AI (not vibe coding).

Works across **Claude Code**, **opencode**, **Google Antigravity**, **Cursor**, **Codex**, and any agent supporting the open Agent Skills (`SKILL.md`) format.

---

## What's Inside

| Skill / Asset | Purpose |
| :--- | :--- |
| [`PROMPT-SHEET.md`](PROMPT-SHEET.md) | Copy-paste prompt templates for every stage of building, debugging, reviewing, and rescuing existing repos. |
| `discovery` | Frontier-Rounds grilling + Brainstorm mode + inline `GLOSSARY.md` & 3-part ADR (`docs/adr/`) maintenance + numbered `R1` requirements. |
| `prototype` | Build 2–4 genuinely different clickable HTML wireframes or code spikes to compare options visually before committing. |
| `software-design` | Deep-module design with the deletion test, testable seams, `CONTRACT` blocks (`GUARANTEES / EXPECTS / DOES NOT`), and `DESIGN.md`. |
| `architecture-audit` | Scan an existing repo's `git log` hotspots in a fresh subagent, open a visual HTML before/after report, and grill through deepening refactors. |
| `implementation-plan` | Vertical tracer-bullet execution plan (sized for 1 Smart Zone session), test seams, boundaries, pre-decisions, and expand–contract refactors. |
| `writing-unit-tests` | 6 laws of valuable tests, 6-level Mock Ladder, pre-agreed seams, vertical Red → Green TDD loop, and mandatory feature-verification test. |
| `sprint` | Heavy-duty parallel execution in isolated git worktrees with wave gates and `sprint_tasks.py` helper. |
| `debugging` | Phase 0 tight red-capable repro loop → competing hypotheses → runtime observation (`[DEBUG-xxxx]` tags) → root-cause fix + regression test. |
| `touch-gestures` | Build and verify browser swipes/drags across mobile Chrome and iOS Safari without breaking scroll/zoom. |
| `ui-ux-polish` | Inspect live desktop/mobile UI, audit common design/typography/spacing bugs, or apply a `DESIGN.md` consistently across an app — strictly without touching functions or business logic. |
| `code-quality` | Pragmatic architecture review, behavior-preserving simplification, SRP redesign, and completeness checks. |
| `pr` | Concise PR body with visual summary, before/after execution evidence, and **Merge Danger** (`One-Way` vs. `Two-Way` Door + Blast Radius). |
| `refine-loop` | Independent review → fix → verify polish loop capped at 2 passes. |
| `retro` | Post-session/PR retrospective that upgrades deterministic checks first (lint/types/CI), `CODING_STANDARDS.md` second, and prunes `AGENTS.md` bloat. |
| `session-continuity` | Protect your Smart Zone (< ~150k tokens) with 4-stage session handoffs, fresh-chat bootstraps, and Context Flush. |
| `teach` | Stateful personal tutor: short interactive HTML lessons with retrieval quizzes and `learning-records/`. |
| `agents/code-reviewer` | Independent read-only reviewer running **Two-Axis Review** (Spec vs. Standards/Design/Security) + Merge Danger + `SHIP / SHIP-WITH-FIXES / REWORK`. |

---

## Quick Setup (1 Minute)

### 1. Clone the repo
```bash
git clone https://github.com/rinshidvp/ai-engineering-skills.git
cd ai-engineering-skills
```

### 2. Install into your AI agent

**Windows (PowerShell):**
```powershell
.\install.ps1                 # installs to Claude Code, opencode, and Antigravity
.\install.ps1 -Only claude    # or: opencode, antigravity
```
*(Skills are linked via directory junctions; agents are generated copies — re-run `install.ps1` after editing `agents/`.)*

**macOS / Linux (or Cursor / Windsurf / any other agent):**
Copy the folders inside `skills/` (including `_shared/`) into your agent's global skills folder (`~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.gemini/config/skills/`, or project-local `.agents/skills/`).

### 3. Start Using the Loop
Open [`PROMPT-SHEET.md`](PROMPT-SHEET.md) for copy-paste prompts:
1. **New feature:** `discovery` → `software-design` *(if big)* → `implementation-plan` → `writing-unit-tests` (TDD) or `sprint` → `code-reviewer` → `pr` → `retro`
2. **Existing messy repo:** Follow **Section 9** of [`PROMPT-SHEET.md`](PROMPT-SHEET.md) (5-step safe rescue playbook)
3. **Keep effort on Medium** for everyday building; switch to **High** for verification and stubborn debugging.
