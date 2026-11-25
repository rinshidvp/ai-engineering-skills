# iOS/Safari gesture failure modes

Use these as competing hypotheses, not automatic patches. Consult current
documentation for the target OS/browser versions; no compatibility claim in a
previous project's handover substitutes for reproduction.

## 1. The page scrolls or the gesture is cancelled

**Observe:** log pointer start/move/cancel and inspect computed `touch-action`
on the target and its ancestors. Check whether a modal, overlay, image or
transparent element receives the contact instead. Verify the deployed code
matches the version being tested.

**Principle:** browsers negotiate gesture ownership using `touch-action` before
the gesture starts. Changing it mid-gesture does not renegotiate that contact.
An ancestor may restrict the target's allowed actions. Modern Safari supports
`touch-action`; do not claim it universally ignores the property.

```css
/* A horizontal deck inside a vertically scrolling document. */
.deck-stage { touch-action: pan-y pinch-zoom; }
```

Use a dead zone, then compare horizontal/vertical travel. On vertical intent,
give up the custom gesture and preserve scrolling. Test diagonal starts too.
Do not disable zoom or document scrolling just to make the carousel test pass.

**Conditional fallback:** if an affected target demonstrably needs touch-event
cancellation, register a native listener with `{ passive: false }` on the small
gesture surface, remove it on teardown, and cancel only a cancelable, single-touch,
already-owned horizontal gesture. The cancellation must happen early enough;
late `preventDefault()` after native scrolling begins is not a guaranteed fix.

```js
function onTouchMove(event) {
  if (event.touches.length !== 1) return; // do not consume pinch zoom
  if (ownsHorizontalGesture() && event.cancelable) event.preventDefault();
}
surface.addEventListener('touchmove', onTouchMove, { passive: false });
// On teardown:
surface.removeEventListener('touchmove', onTouchMove);
```

This is a cancellation example, not a complete recognizer. Listener order and
intent locking must be verified. Some frameworks use passive touch listeners;
inspect their version/registration instead of assuming all React pointer or
touch handlers are passive. Avoid duplicate pointer/touch selection updates.

## 2. Movement stops at a card edge or capture transfer

**Observe:** record pointer ID, capture owner, `hasPointerCapture`, cancellation
and `lostpointercapture` event target/currentTarget. Touch may start with implicit
capture; a transfer from a child to the stage can emit capture-loss events.

**Fix when confirmed:** capture the active pointer once horizontal intent is
established, release if still held, and clean up the recognizer. A bubbled child
capture-loss event should not indiscriminately cancel the stage's valid gesture.
Similarly, reset an uncaptured abandoned mouse gesture on leave, but do not
cancel a captured touch just because the pointer moved outside its visual bounds.

`setPointerCapture` can throw if the pointer is no longer active. Check lifecycle
and supported API before adding a fallback. Catch only an expected, diagnosed
failure; do not silently swallow all exceptions or claim a fallback works before
testing move/release outside the element.

## 3. Finger input is rejected at gesture start

**Observe:** actual `pointerType`, `button`, `buttons`, `isPrimary`, target and
whether the listener runs. Verify no overlay or `inert` ancestor blocks it.
Touch pointer events commonly report primary-button-compatible values; do not
teach that every iPhone uses a special or nonzero button value.

If the intended behaviour is mouse-left-button plus touch/pen, express it:

```js
if (!event.isPrimary) return;
if (event.pointerType === 'mouse' && event.button !== 0) return;
```

That filter is not proof of a root cause. Test movement -> release -> selection,
not just a tap that leaves the initial card unchanged. Repeated swipes should
not use a stale captured active index or advance twice.

## 4. A tap activates navigation, selection, image dragging or a callout

Avoid native image drag on a draggable card (`draggable="false"`), and scope
`user-select: none` / `-webkit-user-select: none` / `-webkit-touch-callout: none`
to the actual gesture artwork when needed. Do not disable selection for the page
or suppress meaningful link actions and accessibility gestures.

Distinguish tapping a control from swiping a card. If a completed drag synthesizes
a click, suppress that one drag-associated activation, not all future clicks.

## 5. Modal closes but focus returns to body

Safari's default pointer-click focus behaviour differs from browsers that focus
buttons on every click. Record the real opener before opening a modal rather
than relying solely on `document.activeElement` after the click.

One appropriate pattern for a button-based opener:

```js
function openFromButton(event) {
  const opener = event.currentTarget;
  opener.focus({ preventScroll: true });
  openDialog({ returnFocusTo: opener });
}
```

Store the opener explicitly if the app's dialog API supports it. After closing,
restore a connected, visible, enabled opener; if a breakpoint hid/removed it,
use a visible equivalent. Preserve intentional destination focus, e.g. a search
result that scrolls to a card. Test menu -> search -> close, not only one modal.

WebKit/iOS keyboard defaults can differ from full keyboard access settings.
Do not weaken the whole keyboard test to obtain a pass: distinguish testing the
skip-link destination by explicit focus from testing whether Tab reaches it.
Record the settings/input path actually tested.

## 6. Multi-touch, interrupted gestures and browser UI

Pinch zoom, orientation change, page backgrounding, native scrolling, system
gestures and nested scrollers can interrupt a contact. Cancel safely without
advancing a card or leaving transformed artwork stuck. Do not intercept the
OS's edge/back gestures or apply non-passive listeners to the document as a
blanket workaround. Check gesture surfaces inside dialogs as well as the page.

## Documentation to consult

- MDN: `https://developer.mozilla.org/en-US/docs/Web/CSS/touch-action`
- MDN: `https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events`
- MDN: `https://developer.mozilla.org/en-US/docs/Web/API/Element/setPointerCapture`
- MDN: `https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener`
- MDN: `https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button`

These are reference pointers, not a claim that current browser support was
checked during every task. Re-fetch the relevant source when version details matter.
