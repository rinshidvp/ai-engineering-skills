# Wireframe Aesthetic

The default wireframe style is a sketch-note — it looks like a designer thinking on paper, not a UI framework. Everything is in handwriting fonts. Cards have dashed borders. Annotations in blue or terracotta explain the reasoning inline. It should feel like opening someone's notebook, not a product screenshot.

This aesthetic applies to wireframes (structural/layout questions). Do NOT use the project's branding, design system, or production fonts for wireframes — the sketch look signals "thinking, not building." For styling/mood prototypes, use real candidate fonts and colors instead — that's what's being decided.

## The look

- **Background**: warm light gray (`#f0eee9`), not white
- **All text**: Patrick Hand (handwriting, but legible). This IS the wireframe font — headings, body, labels, everything
- **Annotations**: Caveat at 600 weight, italic, blue (`#2a78d6`) or terracotta (`#C0533A`). The designer's voice — constraints, behavior notes, scope notes, what's deferred
- **Cards**: white background, dashed borders (`border: 1.5px dashed #C8C4BE`), rounded corners (`8px`), subtle shadow. Dashed = "this is a container, not a finished component"
- **Two border systems**: containers (cards, sections) are faint and dashed (`#C8C4BE`). Drawn UI elements (buttons, inputs, chips, pills) are ink — dark `#222` strokes ~1.5px with the sketch radius below. Use the provided primitives for all interactive elements; don't invent new widget styles
- **Hand-drawn borders**: the rough border-radius trick on interactive elements: `border-radius: 255px 12px 225px 12px/12px 225px 12px 255px` — makes edges look hand-drawn. Applied via `.sk` class or built into each primitive
- **Section labels**: dark pill badges (`background: #2a2a2a; color: white; border-radius: 12px; padding: 2px 10px`). Used as reference anchors: `1`, `2a`, `1b`, etc.
- **Headings**: underlined (text-decoration: underline) in Patrick Hand at larger size. Not bold-serif — handwritten and underlined, like you'd do on a whiteboard
- **Arrows**: `→` and `↓` in text for flow and navigation. Plain text, not SVG
- **Highlight cards**: soft green (`#E8F5E9`) for positive/success states, soft pink (`#FCE4EC`) for warnings/errors/rejections
- **Data**: realistic, never lorem ipsum. Use plausible names, numbers, dates
- **Color discipline**: the only colors on the page are annotation blue/terracotta and the green/pink highlights. Everything else is cream, white, gray, and the muted tan chart fill. No brand colors, no accent fills
- **Interactive elements**: buttons, tabs, inputs, and chips are sketch-styled too — hand-drawn borders, Patrick Hand text, no fills, no gradients, no transitions

## Annotations (`.note`)

Annotations explain WHY, not WHAT. Use the `.note` class (blue) or `.note-red` (terracotta). Write them as the designer's notes — constraints, scope decisions, what's deferred, how things connect:

```html
<span class="note">no signup / no approval — students imported from ET Lab</span>

<span class="note">same pages as advisor, read-only outside own class</span>

<div class="note" style="margin-top:10px">11 pages total. Not in v1: 
student login-approval (dropped — ET Lab data is source of truth), 
hard-copy tracking (later: one extra field)</div>
```

Place annotations:
- Inline with the element they explain, in blue or terracotta
- At the bottom of sections for scope/deferral notes
- Next to flow arrows explaining transitions

## CSS starter

```css
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&family=Caveat:wght@600&display=swap');

:root {
  --bg: #f0eee9;
  --sketch-radius: 255px 12px 225px 12px/12px 225px 12px 255px;
  --card-bg: #FFFFFF;
  --card-border: #C8C4BE;
  --card-radius: 8px;
  --text: #1a1a1a;
  --text-muted: #6b6b6b;
  --annotation-blue: #2a78d6;
  --annotation-red: #C0533A;
  --sketch-font: 'Patrick Hand', cursive;
  --annotation-font: 'Caveat', cursive;
  --highlight-green: #E8F5E9;
  --highlight-pink: #FCE4EC;
}

* { box-sizing: border-box; }

body {
  background: var(--bg);
  font-family: var(--sketch-font);
  color: var(--text);
  font-size: 1.05rem;
  line-height: 1.5;
  max-width: 1200px; /* for desktop wireframes; use ~375px for mobile-targeted questions */
  margin: 0 auto;
  padding: 2rem;
}

h1, h2, h3 {
  font-family: var(--sketch-font);
  text-decoration: underline;
  text-underline-offset: 4px;
  font-weight: 400;
}

.card {
  background: var(--card-bg);
  border: 1.5px dashed var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  padding: 1.25rem;
}

.card-solid {
  background: var(--card-bg);
  border: 1.5px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  padding: 1rem;
}

/* Annotations — designer's notes */
.note { font-family: var(--annotation-font); font-weight: 600; font-size: 16px; color: var(--annotation-blue); line-height: 1.2; }
.note-red { font-family: var(--annotation-font); font-weight: 600; font-size: 16px; color: var(--annotation-red); line-height: 1.2; }

/* Layout utilities */
.wf { padding: 18px 20px; font-size: 16px; line-height: 1.35; }
.row { display: flex; gap: 10px; align-items: center; }

.section-label {
  display: inline-block;
  background: var(--text);
  color: var(--bg);
  font-family: var(--sketch-font);
  font-size: 0.85rem;
  padding: 2px 10px;
  border-radius: 12px;
  margin-right: 0.5rem;
}

.highlight-green { background: var(--highlight-green); }
.highlight-pink { background: var(--highlight-pink); }

.placeholder-chart {
  display: flex;
  gap: 0.5rem;
  align-items: flex-end;
  height: 80px;
}
.placeholder-chart div {
  background: #D4C5B0;
  border-radius: 4px 4px 0 0;
  flex: 1;
  /* each bar needs an inline height, e.g.:
     <div style="height:60%"></div><div style="height:35%"></div><div style="height:80%"></div> */
}

/* UI primitives — hand-drawn borders on interactive elements */
.sk { border: 1.6px solid #222; border-radius: var(--sketch-radius); }
.inp { border: 1.6px solid #222; border-radius: var(--sketch-radius); padding: 5px 10px; color: #999; background: #fff; }
.btn { border: 1.6px solid #222; border-radius: var(--sketch-radius); padding: 6px 16px; background: #1a1a1a; color: #fff; text-align: center; display: inline-block; }
.btn2 { border: 1.6px solid #222; border-radius: var(--sketch-radius); padding: 6px 16px; background: #fff; color: #1a1a1a; text-align: center; display: inline-block; }
.sel { border: 1.6px solid #222; border-radius: 10px; padding: 5px 10px; display: flex; justify-content: space-between; gap: 10px; color: #555; }
.chip { border: 1.4px solid #222; border-radius: 999px; padding: 1px 10px; font-size: 13px; display: inline-block; }
.chip-active { border: 1.4px solid #222; border-radius: 999px; padding: 1px 10px; font-size: 13px; display: inline-block; background: #1a1a1a; color: #fff; }
.lbl { font-size: 14px; margin: 0 0 3px; color: #333; }
.bar { background: #e8e6e0; border: 1.4px solid #222; height: 14px; border-radius: 4px; }
.tr { display: flex; gap: 10px; align-items: center; border-bottom: 1px dashed #aaa; padding: 7px 0; }
.hd { display: flex; justify-content: space-between; align-items: center; border-bottom: 1.6px solid #222; padding: 10px 20px; font-size: 17px; }

/* Status pills */
.st-p { background: #fff; border: 1.4px solid #222; border-radius: 999px; padding: 1px 10px; font-size: 13px; }
.st-a { background: #d9f0dd; border: 1.4px solid #2c7a3f; border-radius: 999px; padding: 1px 10px; font-size: 13px; color: #2c7a3f; }
.st-r { background: #fbe3e3; border: 1.4px solid #b03a3a; border-radius: 999px; padding: 1px 10px; font-size: 13px; color: #b03a3a; }
```

## Two-column layout

Use CSS grid for side-by-side panels (sitemap + flow, role A + role B):

```css
.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  align-items: start;
}
```

## Containers and nesting

`.sk` is the primary container — a hand-drawn bordered box. Use it for sections, cards, grouped content. Add inline padding/width as needed. `.card` (faint dashed) is available for softer grouping when you need a container that recedes visually.

```html
<div class="sk" style="padding:12px">
  <h4>Student</h4>
  <div class="tr">My dashboard — activities, points, statuses <span class="section-label">1b</span></div>
  <div class="tr">New submission — Certificate <span class="section-label">1c</span></div>
  <div class="tr" style="border:none">Edit & resubmit — rejected item</div>
  <div style="margin-top:8px"><span class="btn">Submit</span> <span class="btn2">Cancel</span></div>
  <span class="note">same form pre-filled from the rejected submission</span>
</div>
```

Nest `.sk` containers for hierarchy (outer groups, inner items). Use `.wf` wrapper for wireframe card content that needs consistent padding and font sizing.

## The floating option switcher

All options live in one HTML file as `<section data-option="a">` blocks. The switcher shows/hides them via JS. Minimal by default — just small pills. Hover for full names and thesis. Position: bottom-right (the review overlay toolbar is bottom-left).

```css
.option-switcher { position:fixed; bottom:1.5rem; right:1.5rem; z-index:1000; font-family:var(--sketch-font); }
.os-pills { display:flex; gap:4px; }
.os-pill { width:28px; height:28px; border-radius:50%; background:#fff; border:1.5px solid var(--card-border); text-align:center; line-height:26px; font-size:12px; font-weight:600; color:var(--text); box-shadow:0 1px 4px rgba(0,0,0,0.1); cursor:pointer; transition:transform .15s; }
.os-pill:hover { transform:scale(1.1); }
.os-pill.current { background:var(--text); color:#fff; border-color:var(--text); }
.os-detail { position:absolute; bottom:40px; right:0; background:#fff; border:1.5px solid var(--card-border); border-radius:8px; box-shadow:0 4px 12px rgba(0,0,0,0.12); padding:10px 12px; min-width:220px; opacity:0; pointer-events:none; transform:translateY(4px); transition:opacity .2s,transform .2s; }
.option-switcher:hover .os-detail { opacity:1; pointer-events:auto; transform:translateY(0); }
.os-detail-item { display:block; padding:4px 8px; border-radius:6px; cursor:pointer; font-size:0.85rem; color:var(--text); }
.os-detail-item:hover { background:#f0f0f0; }
.os-detail-item.current { background:var(--highlight-green); font-weight:600; }
.os-thesis { font-family:var(--annotation-font); font-weight:600; color:var(--annotation-blue); font-size:0.9rem; margin-top:6px; padding-top:6px; border-top:1px solid var(--card-border); line-height:1.2; }
section[data-option] { display:none; }
section[data-option].active { display:block; }
```

```html
<!-- Option sections — one per approach -->
<section data-option="a" class="active">
  <!-- option A wireframe content here -->
</section>
<section data-option="b">
  <!-- option B wireframe content here -->
</section>
<section data-option="c">
  <!-- option C wireframe content here -->
</section>

<!-- Switcher — pills + hover detail -->
<div class="option-switcher">
  <div class="os-pills">
    <div class="os-pill current" data-target="a">A</div>
    <div class="os-pill" data-target="b">B</div>
    <div class="os-pill" data-target="c">C</div>
  </div>
  <div class="os-detail">
    <div class="os-detail-item current" data-target="a">A — Option Name</div>
    <div class="os-detail-item" data-target="b">B — Option Name</div>
    <div class="os-detail-item" data-target="c">C — Option Name</div>
    <div class="os-thesis" data-thesis-a="Thesis for A." data-thesis-b="Thesis for B." data-thesis-c="Thesis for C.">Thesis for A.</div>
  </div>
</div>

<script>
document.querySelector('.option-switcher').addEventListener('click', e => {
  const t = e.target.closest('[data-target]');
  if (!t) return;
  const key = t.dataset.target;
  document.querySelectorAll('section[data-option]').forEach(s => s.classList.toggle('active', s.dataset.option === key));
  document.querySelectorAll('.os-pill').forEach(p => p.classList.toggle('current', p.dataset.target === key));
  document.querySelectorAll('.os-detail-item').forEach(d => d.classList.toggle('current', d.dataset.target === key));
  const thesis = document.querySelector('.os-thesis');
  thesis.textContent = thesis.dataset['thesis' + key.charAt(0).toUpperCase() + key.slice(1)] || '';
  window.scrollTo({ top: 0, behavior: 'instant' });
});
</script>
```
