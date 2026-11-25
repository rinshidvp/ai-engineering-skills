# UI/UX Craft & Audit Checklist

Consult this checklist immediately before auditing or editing UI code.

## 1. Typography & Font Sizing (`typeset`)
- **Families:** Maximum 1–2 font families across the app. Pair intentionally
  (or use 1 strong family with clear weight/size contrast).
- **Consistent scale:** Pick one clear scale (e.g., `12 / 14 / 16 / 20 / 24 / 32 / 48px`)
  and remove one-off arbitrary sizes (`text-[13px]`, `text-[17px]`, `19px`).
- **Minimum readable size:** Body text `>= 15–16px` (`14px` minimum for dense
  tables/dashboards); captions/badges `>= 12px`.
- **Line-height:** Body `1.5–1.6` (slightly higher for serif); headings
  `1.1–1.25` so multi-line titles stay tight.
- **Measure (line length):** Cap prose paragraphs at `45–75ch` (`max-w-prose`).
- **Weight & hierarchy:** Clear contrast between primary heading (`600–700`),
  subheadings/buttons (`500–600`), body (`400`), and muted metadata (color
  contrast `>= 4.5:1` for normal text, `>= 3:1` for large text).
- **Avoid generated-page tells:** No random single-word colored/italic accent
  inside headlines; no ALL-CAPS eyebrow labels stacked above every heading; no
  decorative `01 / 02 / 03` numbers unless the content is truly sequential.

## 2. Spacing, Alignment & Responsive Layout (`layout`)
- **4px / 8px grid:** Stick to standard scale steps (`4, 8, 12, 16, 24, 32, 48, 64px`);
  eliminate off-grid magic pixels (`mt-[13px]`, `px-[17px]`).
- **Prefer `gap`:** Use Flex/Grid `gap` instead of inconsistent per-child margins.
- **Mobile (`375×812`) hygiene:**
  - Zero horizontal overflow (`document.documentElement.scrollWidth <= window.innerWidth`).
  - Stack multi-column grids cleanly; prevent long strings/URLs from breaking cards.
  - Interactive buttons/links/inputs `>= 40px` touch target height.
  - Comfortable container padding (`px-4` mobile → `px-8+` desktop).
- **Visual alignment:** Align text baselines, icon centers, and card edges
  consistently; give primary CTA clear visual dominance over secondary actions.

## 3. Common UI/UX Bugs to Catch (`audit`)
- **Missing interactive states:** Buttons/links missing clear `hover:`,
  `focus-visible:` keyboard ring, `active:`, or `disabled:` styling.
- **Broken states:** Blank white voids when data is empty, jarring layout shift
  during loading, or unstyled raw error strings.
- **Status-chip & card soup:** Too many bordered boxes inside bordered boxes,
  competing colored pills, or identical card shadows flattening hierarchy.
- **Contrast failures:** Light grey text on white, low-contrast placeholder
  text, or text over un-scrimmed images/gradients.
- **Gratuitous motion:** Remove scattered fade-in-up animations on every scroll
  section; keep motion subtle and tied to user actions (open/expand/confirm).

## 4. `DESIGN.md` Token Template (for `apply-design`)
When applying a given design consistently across an app, record tokens once:
```markdown
# Design System
- **Surface Mode:** Persuade | Operate | Read
- **Palette:** Background / Surface / Border / Text Primary / Text Muted / Primary Accent / Danger
- **Typography:** Display font, Body font, Scale (`h1`, `h2`, `h3`, `body`, `small`)
- **Spacing & Radii:** Base grid (`4px/8px`), Container max-width, Card/Button/Input radius
- **Elevation & Borders:** Hairline border vs. shadow rules (when each applies)
- **Component Rules:** Primary button, Secondary button, Input, Card, Nav bar
```
Apply these tokens screen-by-screen, verifying desktop + mobile after each pass.
