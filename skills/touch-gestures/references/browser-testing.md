# Browser and device verification

## Keep an evidence ladder

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| Screenshot at a phone width | Layout/crop at that viewport | Gesture functionality |
| Mouse drag changes the slide | Mouse/pointer recognizer path | Finger interaction or scroll arbitration |
| Tap leaves selection unchanged | A tap did not advance | That any swipe handler ran at all |
| DOM-dispatched pointer/touch events | State logic for synthetic events | Native gesture negotiation, passive/cancel behaviour |
| Browser-controlled touch swipe | Touch behaviour for that browser/runtime | Other engines or physical devices |
| WebKit with an iPhone descriptor | WebKit rendering/configuration and tested input paths | Physical iPhone OS/browser integration |
| Finger swipe on affected physical iPhone | Behaviour for the recorded device/build | Every iOS version, webview or browser |

## Minimal project setup example

Merge into the existing Playwright configuration; preserve current targets and
avoid inheriting Chromium's `channel: 'chrome'` into WebKit.

```ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  use: { baseURL: 'http://localhost:3000' },
  projects: [
    { name: 'mobile-chrome', use: {
      browserName: 'chromium', channel: 'chrome',
      viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true,
    } },
    { name: 'iphone-webkit', use: {
      ...devices['iPhone 15'], browserName: 'webkit',
    } },
  ],
});
```

Use a descriptor present in the installed Playwright version. Install that
version's matching WebKit binary (`npx playwright install webkit`); an older
binary elsewhere on disk is not necessarily compatible. Do not pin executable
paths to one developer's machine. Make local server startup part of the existing
test workflow where practical, and verify a response before a long suite run.

## A positive gesture test

For the browser/runtime supporting native touch automation:
1. Navigate to the actual page and settle fonts/layout.
2. Scroll the visible active card clear of sticky headers. Start on its actual
   artwork, not an empty stage or an arrow button.
3. Deliver touch start, several leftward moves and release through the automation
   tool's real touch input facility. Assert the second item is selected.
4. Reverse direction and assert the first item returns. Check repeated swipes,
   both ends/wrapping, short drags and cancellation.
5. Use a predominantly vertical gesture; selection stays unchanged and native
   page scroll moves. Ensure there is room to scroll in that direction first.
6. Check a diagonal start, tap versus activation, and pinch/cancellation when the
   available device service supports them.

Chromium CDP `Input.dispatchTouchEvent` can exercise Chrome's touch path. CDP is
not WebKit: do not send it to a WebKit context. Playwright's portable
`touchscreen.tap` is a tap, not a swipe. A WebKit mouse drag or hand-dispatched
`PointerEvent` is not a replacement for native iPhone finger movement.

If native WebKit/device swipe automation is unavailable, keep useful WebKit
mouse/tap/layout checks, label the unsupported touch-swipe check as unverified,
and arrange a physical-device retest. A skipped swipe test remains a gap even
when every other test passes. Do not mock gesture selection directly and call
that browser compatibility.

## Regression matrix

- At least one small portrait and one short landscape layout; meaningful images
  loaded, no document overflow, no original-section layout change.
- Native vertical scroll, nested scroll/overlays, zoom and interrupted contact.
- Active item announcement, inactive slide inertness and keyboard alternatives.
- Mouse and touch inputs, buttons/dots, no accidental link activation after drag.
- Focus return after close, after breakpoint changes, and after nested panel
  transitions; visible/touch-sized close control with the on-screen keyboard.
- Reduced motion: gestures still select, while movement transitions are disabled
  or reduced according to project policy. No unwanted auto-rotation.
- Console/runtime errors and the newly deployed URL/assets, not just localhost.

## Physical-device retest checklist

Record the iPhone/iPad model, iOS version, browser or in-app webview, exact URL,
deployment/build and input method. Ask for the result of a simple reproducible
sequence: scroll to the deck, swipe left on the image, swipe right, scroll
vertically over it, tap a control, open/close a preview. Recheck after reopening
the page/rotating if those caused the failure. Do not delete browsing data or
blame caching without evidence; normal reload is a reasonable first comparison.

## Report template

```text
Change: ...
Confirmed cause / evidence: ... (or: cause still unconfirmed)
Verified: browser/engine + viewport/device + input method + observed outcome
Not verified / skipped: ...
Deployment checked: URL/build + result (or: not deployed)
Physical iPhone retest: model/OS/result, or explicitly pending
```

Say “WebKit mouse drag and touch tap passed; real iPhone swipe pending” when
that is the evidence. Do not say “iOS swipe fixed and verified” on that basis.
