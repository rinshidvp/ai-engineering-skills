---
name: prototype
description: Explore options by building them. Generate multiple concrete artifacts — HTML wireframes, code spikes, architecture diagrams — so the human can compare by looking, not by reading descriptions. Use when the human says "show me options", "what could this look like", "mock up a few approaches", "wireframe this", "spike it", "try a few layouts", "what are our options for X", or any request to explore before committing. Also trigger when a decision is stuck and seeing the alternatives would unstick it. Do NOT use for single implementations, polishing existing UI, when the direction is already decided, or when a verbal comparison would answer the question.
---

# Prototype

You explore decisions by making them concrete. Instead of describing three approaches, you build all three so the human can look at them side by side and point. The artifacts are throwaway — speed and genuine variety matter more than polish.

The failure mode you're fighting: hearing "3 options" and reverse-engineering 3 variations of the same idea. The number doesn't matter. What matters is that each option represents a genuinely different approach with its own merit. If you can't explain why someone would pick each one independently, you don't have different options — you have costumes on one idea.

## Finding genuine options

Before building anything, map the real approaches. This is 30 seconds of thinking, not a ceremony:

1. What's the actual decision? Translate the surface request into the underlying question. The request names a thing to build; the question names what's being decided.
2. Where would reasonable people disagree? Those disagreements are your options. "Show everything at once" vs. "focus on one thing at a time" vs. "only surface exceptions" — each has a thesis.
3. Each option earns its place. It needs:
   - A **name** (descriptive, not A/B/C)
   - A **thesis** — one line on when this is the right choice
   - A **worst-when** — when this approach actively hurts

If two options share a thesis, merge them. If you find 5 genuine approaches, build 5. If only 2 exist, build 2. Don't pad. Default to 3 if you're unsure — most decisions have 2-4 real branches.

**Good** (each option has a different thesis — a reason someone would pick it):
```
Option 1: "Right when users need to compare across items."
Option 2: "Right when users focus on one item at a time."
Option 3: "Right when most items are ignorable and only exceptions matter."
```

**Bad** (three costumes on one idea — same structure, different surface):
```
Option A: Blue cards with rounded corners
Option B: White cards with shadows
Option C: Dark mode cards with borders
```

## Match fidelity to the question

One rule: vary only the thing being decided. Hold everything else constant. The fidelity follows from what kind of question is being asked.

| Question | What varies | What's constant | Fidelity |
|----------|-------------|-----------------|----------|
| "How should this be organized?" | Structure, layout, flow | Styling — deliberately minimal | Low. Polish makes people pick the prettiest, not the best. |
| "What should this look like?" | Colors, type, spacing, mood | Structure — identical across options | High. A mood you can't feel isn't comparable. |
| "How should this piece work?" | Interaction model, states | Page context around it | Must be interactive — clicks, hovers, state changes. |

For structural/backend decisions (data models, API shapes, architecture): produce code files + a tradeoff table. No HTML viewer needed — the comparison is textual.

## Building the artifacts

**Visual prototypes** — a single self-contained HTML file in `tmp/{YYYYMMDD}-prototype-{name}/`. All options live in one page with JS-based tab switching — no separate files, no broken links, one file to open. Each option is a `<section>` that shows/hides when the user clicks the switcher pills.

Load `references/wireframe-aesthetic.md` for the default wireframe look — a sketch-note style with handwriting fonts (Patrick Hand, Caveat), dashed borders, and inline annotations. The sketch aesthetic and no-branding rule apply to *wireframes* (structural questions). Styling/mood prototypes are the opposite — real candidate fonts and colors ARE the option.

Conventions:
- Single standalone HTML. Inline CSS and JS. Google Fonts as needed.
- Real content, never lorem ipsum. Placeholder charts as simple shapes.
- Wireframe at the viewport the question targets (mobile-first projects → 375px). State which you chose.
- For styling/mood questions where comparison is simultaneous, show options side-by-side instead of tabbed.
- Include the review overlay: copy `scripts/review-overlay.js` (in this skill's folder) into the prototype directory and add `<script src="review-overlay.js"></script>` before `</body>`. This adds a review toolbar (bottom-left icon, starts expanded then collapses) for pinning comments and drawing annotations directly on the wireframe. To help the reviewer, add `data-screen-label="Screen Name"` to each major section (each option section, key UI areas) — the overlay groups annotations by this label. Use descriptive labels like "Option A — Unified List" or "Dashboard header".

The page includes a **floating option switcher** — small circular pills (A, B, C) fixed at bottom-right. Click to switch between options. Hover to see full names and the current option's thesis. Current option pill is filled dark. Keep it minimal — just pills by default, detail panel appears on hover.

**Structural prototypes** — code files in `tmp/{YYYYMMDD}-prototype-{name}/`. Each option gets a subdirectory.

**Architecture prototypes** — HTML files with inline SVG diagrams + prose analysis. Same floating switcher.

## End with a recommendation

After presenting the artifacts, always recommend: "I'd go with X because [reason]. But Y wins if [condition]." Neutrality forces work onto the human. Being wrong surfaces reasoning they can push back on.

Include a tradeoff table in chat — dimensions as rows, options as columns. End with the file path to open (or open it via browser tooling).

## Refining

"I pick B" → iterate on B, drop the others.
"B but with A's sidebar" → mashup is first-class, not an edge case. Combine and produce a new artifact.
"None of these" → ask what's missing from the space. New discovery round.
"This is it, build it" → name the decisions the prototype embodies. Hand off to implementation. Keep prototype files as the reference anchor.

## When NOT to prototype

- If there's genuinely one viable approach, say so and build it. Prototyping is for decisions.
- If the problem needs conversation before artifacts, use the `discovery` skill (Brainstorm mode) first.

## Delegation

The thinking — finding the real options, writing the briefs — is your job. Never delegate that. Production CAN be delegated: one subagent per option when options are independent (how to spawn one in each host: `../_shared/hosts.md`). Write specific enough briefs that the structural differences come from the spec, not from the agent's improvisation.
