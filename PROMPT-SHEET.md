# `dev-skills` Daily Prompt Sheet

Copy-paste templates for running your full strategic AI engineering workflow without memorizing commands. Replace **`[bracketed text]`** with your specifics.

---

## 0. Three-Second Pre-Flight Check (Before Every Session)

1. **Effort level:** Keep your model on **Medium** for exploration, grilling, planning, and normal coding. Switch to **High** *only* for final verification, stubborn debugging, or deep web research.
2. **Smart Zone (< ~150k tokens):** Start a **fresh chat** when moving from planning → building → reviewing. Never stay in one mega-chat all day.
3. **Pick the right path size:**
   - **Tiny fix (1 file, obvious):** Prompt directly → run tests → commit.
   - **Normal feature (fits 1 session):** `discovery` → `implementation-plan` *(if 3+ files)* → `writing-unit-tests` (TDD build) → `code-reviewer` → `pr` → `retro`.
   - **Large multi-slice feature:** `discovery` → `software-design` → `implementation-plan` → `sprint` → `code-reviewer` → `pr` → `retro`.
   - **Messy / vibe-coded repo:** `architecture-audit` → pick 1 candidate → `discovery` → refactor.

---

## 1. Align Before Coding (`discovery` & `prototype`)

### Grill a new feature idea (Frontier Rounds + Glossary + ADRs)
```text
Use the discovery skill to grill me before we build [describe your rough idea in 1–3 sentences]. Check GLOSSARY.md and docs/adr/ first, scout the codebase in a subagent, and ask me Frontier Rounds. Do not write code yet.
```
*Fast reply tip during rounds:* **`Q1: yes. Q2: actually make it admin-only. Q3: yes.`**

### Brainstorm between two technical choices
```text
Use the discovery skill in Brainstorm mode to help me choose between [Option A] and [Option B] for [goal]. Compare trade-offs, test your first instinct, and tell me if this is a One-Way or Two-Way Door.
```

### Build or clean up `GLOSSARY.md` on an existing project
```text
Use the discovery skill (domain-modeling) to scan this repo for inconsistent names used for the same concepts, then grill me in one round so we can write a clean GLOSSARY.md with _Avoid_ synonyms.
```

### Visually compare UI layouts or interaction options (`prototype`)
```text
Use the prototype skill to build 3 genuinely different options for [screen / interaction / layout] as a single HTML prototype I can click through and compare. End with a tradeoff table and your recommendation.
```

---

## 2. Design & Plan (`software-design` & `implementation-plan`)

### Design a complex multi-module feature (`software-design`)
```text
Use the software-design skill to turn tasks/[YYYY-MM-DD-slug].requirements.md into a clean design. Favor deep modules, apply the deletion test, and define explicit CONTRACT blocks (GUARANTEES / EXPECTS / DOES NOT).
```

### Create a vertical tracer-bullet execution plan (`implementation-plan`)
```text
Use the implementation-plan skill to create a vertical tracer-bullet plan from tasks/[YYYY-MM-DD-slug].requirements.md. Confirm our public test seams and task granularity with me before saving to tasks/.
```

### Plan a wide rename or schema change safely (Expand–Contract)
```text
Use the implementation-plan skill to plan migrating [old name / schema / API] to [new name / schema / API] using an expand–contract sequence so tests stay green after every batch.
```

---

## 3. Build & Test (`writing-unit-tests`, Small Build, `sprint`)

### Build a small/medium feature in 1 session (TDD loop — skip `sprint`)
```text
Implement [feature / Task N] from tasks/[YYYY-MM-DD-slug].plan.md using the writing-unit-tests skill. First confirm the public seams we're testing, then work one vertical Red -> Green slice at a time. Run typecheck and single-file tests as you go, and run the full test suite once at the end.
```

### Audit existing tests for fake / brittle tests
```text
Use the writing-unit-tests skill to audit tests in [path]. Flag tautological tests, implementation-coupled tests, or internal mocks that violate the Mock Ladder, and tell me which to delete or rewrite.
```

### Execute a large multi-slice plan in parallel worktrees (`sprint`)
```text
Use the sprint skill to decompose tasks/[YYYY-MM-DD-slug].plan.md into verifiable bricks and waves, then run them in isolated git worktrees with wave gates.
```

---

## 4. Debug Without Guessing (`debugging`)

### Root-cause a bug or flaky failure
```text
Use the debugging skill to investigate [describe bug / paste error]. Start with Phase 0: build and minimise a fast red-capable repro command before forming competing hypotheses. Tag temporary logs with [DEBUG-xxxx] and lock in a regression test before closing.
```

---

## 5. Review, Polish & Ship (`code-reviewer`, `code-quality`, `refine-loop`, `pr`)

### Run an independent Two-Axis Code Review + Merge Danger
*(Switch effort to **High** if this is a risky change!)*
```text
Spawn the code-reviewer agent to review our changes against main and tasks/[YYYY-MM-DD-slug].requirements.md. Report Spec findings, Standards/Security findings, Merge Danger, and your SHIP / SHIP-WITH-FIXES / REWORK verdict.
```

### Simplify messy working code without changing behavior (`code-quality`)
```text
Use the code-quality skill in Simplification mode on [file/folder]. Make the code easier to read while strictly preserving all behavior, and run tests to prove nothing changed.
```

### Run a capped 2-pass review-and-fix polish cycle (`refine-loop`)
```text
Use the refine-loop skill to review and polish [files / plan / design] through the [code-quality / software-design] lens, capped at two passes.
```

### Generate a visual PR description with Merge Danger (`pr`)
```text
Use the pr skill to write a Pull Request body for this branch against main, including a compact visual summary, before/after execution evidence, and Merge Danger (Door + Blast Radius).
```

---

## 6. Protect Your Context Window (`session-continuity`)

### Save state at the end of a session
```text
Use the session-continuity skill to write a Session Handoff to tasks/[task-name].handoff.md so a fresh chat can pick up cleanly without guessing.
```

### Resume in a brand-new chat
```text
Bootstrap from tasks/[task-name].handoff.md using the session-continuity skill.
```

### Emergency Context Flush (when chat gets long mid-task)
```text
Use the session-continuity skill in Context Flush mode: distill everything from this conversation into tasks/[task-name].plan.md so I can restart in a clean chat.
```

---

## 7. Compound Quality, Fight Slop & Learn (`retro`, `architecture-audit`, `teach`)

### Post-feature / post-PR retrospective (`retro`)
```text
Use the retro skill on this session. Propose improvements ranked by impact: deterministic checks (linter / strict types / pre-commit / CI) first, CODING_STANDARDS.md judgment rules second, and AGENTS.md navigation pointers or pruning third.
```

### Proactive anti-slop scan on an existing repo (`architecture-audit`)
```text
Use the architecture-audit skill on this repo. Focus on recent git hotspots, explore in a fresh subagent, and open the visual HTML before/after report in my browser. Do not edit code yet.
```

### Harden a vibe-coded repo with deterministic guardrails ("The Straightjacket")
```text
Audit this repo's automated guardrails (strict TypeScript / types, linter rules banning escape hatches like `any`, fast test runner, and pre-commit or CI checks). Propose the smallest deterministic setup that catches agent mistakes early, confirm with me, and wire it up.
```

### Learn any unfamiliar concept, book chapter, or report (`teach`)
```text
Use the teach skill to teach me [concept / paste architecture card / repo folder] in plain English using examples from my own code. Set up MISSION.md if missing, then open Lesson 1 as an interactive HTML page with a short quiz.
```

---

## 8. Three Handy Micro-Prompts (No Extra Skill Needed!)

### "Wait, What?" (when AI replies in confusing jargon)
```text
Stop — that didn't click. Re-explain where we are in plain, simple English using concrete examples from this project and our exact GLOSSARY.md terms.
```

### Background Primary-Source Research
```text
Spawn a fresh-context research subagent to investigate [topic / library / API] using official docs and primary source code only (no random blog posts). Have it save a concise markdown summary with source citations to docs/research/[slug].md while we keep working.
```

### Client / Teammate Questionnaire (when someone else holds the answers)
```text
I need answers from [role, e.g. client / professor / teammate] before we can decide [topic]. Ask me who they are and what decisions I'm blocked on, then write a clean, non-jargon markdown questionnaire I can send them.
```

---

## 9. Rescue & Upgrade an Existing Vibe-Coded Repo (5-Step Playbook)

**Golden Rule (from *Working Effectively with Legacy Code*):** Never restructure messy code *before* you have safety-net tests and guardrails — refactoring without tests is just breaking things in the dark! Run these **5 steps in separate fresh chats** so every step stays in the Smart Zone:

### Step 1 (Chat 1): Read-Only Repo Health, Bug & Missing-Docs Scan
```text
Do a read-only onboarding audit of this existing repo (spawn fast explorer subagents so our main context stays clean; do NOT edit any files yet). Report back in 4 short sections:
1. Missing Foundation Docs: check for GLOSSARY.md, docs/adr/, CODING_STANDARDS.md, and AGENTS.md/CLAUDE.md (and flag if AGENTS.md is bloated).
2. Missing Deterministic Guardrails: check strict typing (e.g. tsconfig strict / `any` leaks), linter config, test runner, pre-commit hooks, and CI workflows.
3. Real Bugs & Security Risks: scan critical paths (auth, DB writes, API routes, env/secrets, silent catch blocks) and list concrete suspect bugs with file:line.
4. Hotspot Summary: check `git log` for the top 3 most-churned messy files.
End with a recommended order of attack.
```

### Step 2 (Chat 2): Add `GLOSSARY.md`, Key ADRs & Lean `AGENTS.md`
```text
Use the discovery skill (domain-modeling) on this existing repo:
1. Scan the codebase for core domain concepts and inconsistent naming, then grill me in one Frontier Round to create a clean GLOSSARY.md with _Avoid_ synonyms.
2. Identify the 1–3 biggest hard-to-reverse architectural choices already in this repo (DB, auth, hosting, state) and draft concise ADRs in docs/adr/ for my approval.
3. Create (or trim) AGENTS.md / CLAUDE.md to under 25 lines containing only build/test commands and navigation pointers to GLOSSARY.md, CODING_STANDARDS.md, and docs/adr/.
```

### Step 3 (Chat 3): Add Deterministic Guardrails + Safety-Net Tests FIRST
```text
Before we refactor anything, help me build a safety net:
1. Wire up deterministic checks (typecheck, linter, test script) and create a starter CODING_STANDARDS.md for judgment rules.
2. Use the writing-unit-tests skill: propose the highest public seams covering this app's core happy paths, wait for my confirmation, and write behavioral safety-net tests (no internal mocks) that prove current features work.
```

### Step 4 (Chat 4): Fix Real Bugs & Security Holes One by One
```text
Use the debugging skill to investigate and fix [Bug #1 from Step 1]. Build a fast red-capable repro test first, confirm the root cause, fix it, verify all safety-net tests stay green, and commit.
```

### Step 5 (Chat 5): Restructure Messy Hotspots Safely (`architecture-audit`)
```text
Use the architecture-audit skill on this repo. Focus on recent git hotspots, open the visual HTML before/after report in my browser, and wait for me to pick ONE module to deepen. Keep all Step 3 safety-net tests green during the refactor.
```

---

## 10. UI/UX Audit, Typography & Visual-Only Polish (`ui-ux-polish`)

### Find all common UI/UX problems on a live site (Read-Only Audit)
```text
Use the ui-ux-polish skill in Audit mode on this app. Inspect the rendered pages on desktop (1280x800) and mobile (375x812), check typography/font sizes, spacing rhythm, alignment, contrast, interactive states, and AI-slop tells, and list Must Fix / Should Fix / Polish items with exact file:line pointers. Do NOT edit any files yet.
```

### Fix font sizes, typography hierarchy & spacing (Zero Logic Changes)
```text
Use the ui-ux-polish skill in Typeset + Layout mode on [page / folder]. Fix inconsistent font sizes, heading hierarchy, line-height, spacing rhythm, and mobile overflow. Strictly edit CSS/Tailwind/visual markup ONLY — do NOT modify any functions, state, API calls, or logic. Verify with `git diff`, existing tests, and desktop/mobile screenshots.
```

### Apply a given design / mockup consistently across the entire app
```text
Use the ui-ux-polish skill in Apply Design mode using [paste screenshot / design reference / DESIGN.md]. First extract and confirm the DESIGN.md token sheet with me, then apply it consistently screen-by-screen across the app without touching any business logic or functions. Verify with tests and desktop/mobile screenshots.
```
