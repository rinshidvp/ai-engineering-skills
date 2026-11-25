---
name: touch-gestures
description: Build, debug and verify browser touch interactions across mobile Chrome and iOS Safari. Use for swipeable carousels or stacked cards, touch drag-and-drop, gesture-versus-page-scroll conflicts, pointer cancellation/capture, or reports such as "works on desktop but not on my iPhone". Apply even when Chrome tests already pass. Not a general responsive-layout, performance or native-mobile SDK skill.
---

# Touch gestures

Ship a usable interaction, not just a layout that fits a phone screenshot.
Keep the existing design and unrelated behaviours intact.

## 1. Define observable behaviour

Before editing, inspect the component, styles, existing library and tests.
Prefer the project's existing, accessible carousel/gesture implementation to a
new parallel event system.

Record the acceptance criteria relevant to the feature:
- A left/right finger swipe selects the expected item, in both directions.
- A tap, short movement, vertical gesture or cancellation does not select it.
- A vertical finger gesture still scrolls the page when there is scroll room;
  pinch zoom remains available unless an explicitly approved interaction owns it.
- Buttons and keyboard provide alternatives; selected content, focus return and
  reduced-motion behaviour remain correct. Controls have comfortable touch targets.

For a reported failure, request the device, OS/browser version, browser versus
in-app webview, exact URL and observed result. Continue reproduction work while
awaiting these details; do not assume which Safari quirk caused it.

## 2. Diagnose before prescribing

Read [iOS/Safari failure modes](references/ios-safari-gotchas.md) for a touch bug
or custom pointer handler. Use the [debugging workflow](../debugging/SKILL.md)
when the cause is unknown.

Compare at least two plausible explanations using event/runtime evidence:
`pointerdown`, `pointerType`, movement, capture ownership, `pointercancel`,
`touch-action` on ancestors, hit targets and current deployment version.
Temporary instrumentation must not record sensitive form data.

Distinguish **observed**, **inferred**, and **not tested**. Do not turn a previous
project's hypotheses into universal browser facts. Fix the responsible layer,
not every conceivable compatibility problem at once.

## 3. Implement deliberately

- Establish gesture ownership before movement. For a horizontal deck embedded in
  a scrolling page, CSS `touch-action: pan-y pinch-zoom` is a starting contract,
  not evidence that the device is working. Avoid page-wide `touch-action: none`.
- Lock horizontal intent after a small dead zone and directional comparison;
  abandon vertical intent without blocking the page. Keep selection thresholds
  separate from the intent threshold.
- Track one pointer and current state. Clean up on completion, cancellation,
  relevant capture loss and unmount. Do not let an incidental pointer-leave or a
  child-to-parent capture transfer erase a valid captured swipe.
- Keep mouse button filtering specific to the intended input. Check actual event
  values rather than assuming all touch events use a different button value.
- Preserve native controls, links and zoom; avoid blanket `preventDefault()`.
  Add a non-passive native touch listener only if reproduced evidence requires
  it, with narrow scope, cleanup and multi-touch/scroll checks. Do not process
  the same contact through independent pointer and touch recognizers.
- Handle focus return explicitly where browser click-focus behaviour differs.
  Do not auto-focus every draggable surface or open the on-screen keyboard on a tap.

## 4. Verify the real input path

Read [browser testing](references/browser-testing.md) before adding tests or
claiming compatibility. Follow [test discipline](../writing-unit-tests/SKILL.md).

Require a new positive test that starts a gesture on meaningful content,
delivers movement through the intended input path, releases, and observes a
different selected item. It should fail if the swipe handler is removed.
An unchanged-card tap test alone can pass when touch handling is completely dead.

Test relevant Chrome and WebKit targets, narrow portrait and short landscape,
actual touch input where the tooling supports it, cancellation, diagonal/vertical
motion, page scrolling, keyboard/button alternatives and reduced motion. Check
both styles and gestures after opening/closing overlays or changing viewport size.

For a real iPhone report, retest on the affected physical device or an explicitly
available remote real-device service. Browser-engine emulation is useful but not
equivalent to that device. If unavailable, ship only with the limitation stated
and request the user's retest; do not invent a successful device check.

## 5. Close with evidence

Report: what changed; tested browser/engine and input method; observable outcomes;
skips/tool limitations; and any pending physical-device check. Separate local
verification from verification of a newly deployed URL. A successful build or
an aggregate pass count is not proof that iPhone finger swipes work.
