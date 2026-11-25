---
name: ui-ux-polish
description: Inspect a live website or frontend codebase to find common UI/UX problems, fix typography/font sizes and spacing, or apply a given design consistently across the entire app — strictly without touching functions or business logic. Use when polishing UI, auditing layout/mobile/contrast issues, fixing font sizes and hierarchy, or applying a reference mockup/DESIGN.md across screens.
---

# UI/UX Polish

Elevate an existing website or app to production design craft while keeping
every function, API call, and state flow untouched. Combines live visual
inspection, a consistent `DESIGN.md` token system, anti-AI-slop typography and
layout craft, and a hard **Zero Logic Changes** gate.

## Pick Your Mode

1. **Audit (`audit`):** Inspect the running site (desktop `1280×800` + mobile
   `375×812`) and code to report concrete UI/UX bugs (`Must Fix` / `Should Fix`
   / `Polish`) with exact `file:line` pointers — no edits yet.
2. **Typeset (`typeset`):** Fix font sizes, type scale, weights, line-height,
   line length (`<= 75ch`), and heading hierarchy (`H1 → H2 → H3`).
3. **Layout & Responsive (`layout`):** Fix alignment, 4px/8px spacing rhythm,
   mobile overflow (`scrollWidth <= clientWidth`), cramped tap targets, and
   missing hover/focus/empty/loading states.
4. **Apply Design (`apply-design`):** Given a screenshot, mockup, or design
   spec, extract a single token sheet into `DESIGN.md` (colors, type scale,
   spacing, radii, shadows, surface rules) and apply it consistently screen by
   screen across the entire app.
5. **Polish (`polish`):** Full visual-only pass across a screen or feature
   combining typography, spacing, states, and anti-AI-slop cleanup.

## Step 1: Understand the Surface Before Touching CSS

Before editing any file:
- Read `GLOSSARY.md` (if present) and `DESIGN.md` (if present; create it lazily
  in `apply-design` mode).
- Identify the surface's **Mode** so ambition matches purpose:
  - **Persuade** *(landing pages, marketing, hero)*: bold visual identity,
    clear focal point, memorable typography.
  - **Operate** *(apps, dashboards, forms, tools)*: precision, restraint,
    scannability, predictable interactive patterns.
  - **Read** *(docs, blogs, study guides)*: comfortable measure (`45–75ch`),
    generous line-height, calm contrast.
- **Inspect rendered truth first:** Start or open the running app and capture
  screenshots + computed styles (font families, sizes, spacing, overflow) on
  both **desktop (`1280×800`)** and **mobile (`375×812`)**. If the app cannot
  run locally, inspect existing CSS/Tailwind tokens and component markup and
  state clearly that visual verification was static-only.

## Step 2: Apply Craft Rules (Read Before Editing)

Load `references/craft-checklist.md` immediately before making UI edits. Core
non-negotiables:
- **Typography:** Max 1–2 deliberate font families; consistent type scale (no
  random `13px / 15px / 17px / 19px` soup); body line-height `1.5–1.6`, heading
  line-height `1.1–1.25`; paragraph width `<= 75ch`; never use sub-12px body or
  label text.
- **Spacing & Rhythm:** Strict 4px/8px spacing scale (`gap-*` over scattered
  margins); generous section separation; zero horizontal scroll on `375px`
  mobile; touch targets `>= 40px`.
- **Kill AI-Slop Tells:** No identical rounded SaaS cards with soft grey
  shadows everywhere, no tracked-out ALL-CAPS eyebrow labels above every
  heading, no random single-word colored accents in titles, no gratuitous
  fade-and-slide-up on every section.
- **Brief wins:** If the user gave a specific design/mockup, follow it
  faithfully across every screen instead of substituting your own taste.

## Step 3: Strict "Zero Logic Changes" Guardrail

Refinement preserves behavior 100%. While running this skill:
- **Allowed:** CSS, Tailwind classes, theme tokens, CSS variables, typography,
  spacing, layout wrappers, responsive breakpoints, visual icons/states
  (`hover:`, `focus-visible:`, `disabled:`), semantic HTML upgrades that keep
  DOM behavior identical.
- **Forbidden:** Changing business logic, API requests, state transitions,
  hooks, prop signatures, form validation rules, data transformations, or
  event-handler behavior.
- **If a UI fix truly requires a logic change** (for example, adding a missing
  loading state variable): **stop and ask the user first** instead of silently
  editing application logic.

## Step 4: Verify Before Finishing

1. **Diff check:** Inspect `git diff` and confirm zero unintended changes to
   functions, state, or API calls.
2. **Tests & typecheck:** Run existing typecheck and test suite to prove no
   behavior regressed.
3. **Visual check:** Re-capture desktop (`1280×800`) and mobile (`375×812`)
   screenshots and confirm zero horizontal overflow, clean font hierarchy,
   readable contrast, and faithful match to `DESIGN.md`.
4. **Report:** Summarize what changed visually (before → after), confirm
   **Zero logic modified**, and list any follow-up items that would require a
   logic change.

Host tool mapping (browser inspection, commands, subagents): `../_shared/hosts.md`.
