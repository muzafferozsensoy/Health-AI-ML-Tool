# Accessibility Fix Log — HEALTH-AI

**Last reviewed:** 2026-05-03
**Audit target:** Lighthouse Accessibility ≥ 85, WCAG 2.1 AA compliance
**Scope:** `frontend/` React + Vite app (all 7 workflow steps + shared chrome)

---

## 1. Acceptance Criteria

| # | Criterion | Status |
|---|-----------|--------|
| 1 | Lighthouse Accessibility score ≥ 85 | ✅ Met |
| 2 | All images / graphics / logos carry appropriate alt or aria-label text | ✅ Met |
| 3 | Color contrast complies with WCAG 2.1 AA (≥ 4.5 : 1 normal text, ≥ 3 : 1 large text & UI components) | ✅ Met |
| 4 | This Accessibility Fix Log published on the project Wiki | ✅ Met (this document) |

---

## 2. Issues Found and Resolutions

### 2.1 Color contrast

| # | Where | Issue | Measurement (before) | Fix | Measurement (after) |
|---|-------|-------|----------------------|-----|---------------------|
| C-1 | `--color-text-muted` (#6e7681) on `--color-bg-primary` (#0d1117) — used in chart axis labels, table sub-labels, footnotes | Failed normal-text contrast | **4.08 : 1** | Lifted muted to `#8b949e` and secondary to `#adbac7` | **6.13 : 1** / **9.13 : 1** |
| C-2 | "Help" header button — white text on bright `--color-accent-green` (#10B77F) | Failed normal-text contrast | **2.56 : 1** | Routed solid-fill buttons through new `--color-accent-green-solid` (#047857) | **5.48 : 1** |
| C-3 | "Next" footer button (`.nextBtn`) — white on bright green | Same as C-2 | **2.56 : 1** | Switched to `--color-accent-green-solid` | **5.48 : 1** |
| C-4 | Header logo tile — white "+" on bright green | Same as C-2 | **2.56 : 1** | Switched to `--color-accent-green-solid` | **5.48 : 1** |
| C-5 | DomainPillBar active pill — white on bright green | Same as C-2 | **2.56 : 1** | Switched to `--color-accent-green-solid` | **5.48 : 1** |
| C-6 | Light theme accent green (#10B77F) used as text on white | Failed normal-text contrast | **2.56 : 1** | Light theme override → `#047857` | **5.48 : 1** |
| C-7 | Light theme accent orange (#d29922) used as text on white | Failed normal-text contrast | **2.51 : 1** | Light theme override → `#9a6700` | **5.18 : 1** |
| C-8 | Light theme accent red (#f85149) used as text on white | Failed normal-text contrast | **3.39 : 1** | Light theme override → `#b91c1c` | **6.42 : 1** |
| C-9 | HelpModal section headings (h3) — bright accent green text on dark panel | Borderline at 14 px/600 weight | ~ 4.4 : 1 | Heading text now uses `--color-text-primary`; green retained as a 4 px decorative bar (UI element, ≥ 3 : 1) | **15.3 : 1** for the heading text |

> Contrast values were computed with the WCAG 2.1 relative-luminance formula (sRGB → linear → L = 0.2126·R + 0.7152·G + 0.0722·B; ratio = (L₁+0.05)/(L₂+0.05)).

### 2.2 Non-text alternatives (alt / aria-label)

| # | Where | Issue | Fix |
|---|-------|-------|-----|
| A-1 | Header logo — `<div>` with literal "+" character, no accessible name | Logo announced as plain text or skipped | Added `role="img"` + `aria-label="HEALTH-AI logo"`; the "+" glyph is now `aria-hidden="true"` |
| A-2 | Header theme-toggle SVG icons (sun / moon) | Inline SVGs without `aria-hidden` were exposed as graphics with no name | Added `aria-hidden="true"` + `focusable="false"` to decorative icons; the parent `<button>` already has a descriptive `aria-label` and now `aria-pressed` |
| A-3 | DomainPillBar arrow buttons rendered just "‹" / "›" | Glyphs leaked into the accessible name | Glyph wrapped in `aria-hidden="true"`; button keeps its `aria-label` |
| A-4 | Footer "Back" / "Next" buttons | Arrow glyphs `&larr;` / `&rarr;` were part of the name | Glyphs wrapped in `aria-hidden="true"`; explicit `aria-label` added to "Back" |
| A-5 | ROC Curve SVG | Only had `aria-label` summarising AUC — no machine-readable description | Added `<title>` and `<desc>` (`role="img"`, `aria-labelledby`) describing axes, the dashed diagonal, and the AUC value |
| A-6 | ProgressRing SVG | No accessible name | Added `role="img"` + `aria-label` reporting current progress percent and a `<title>` element |
| A-7 | DomainPillBar reset banner ↻ glyph, Stepper "✓" glyph, HelpModal close "×" glyph | Symbols read aloud as "anticlockwise gapped circle arrow", "check mark", "multiplication sign" | Wrapped in `aria-hidden="true"`; container/button retains accessible text or `aria-label` |
| A-8 | CSVUploader hidden file `<input type="file">` | Unlabelled hidden input flagged by Lighthouse | Added `aria-label="CSV file"` and `tabIndex="-1"` (the visible buttons are the actual control) |

The app uses **no `<img>` tags** today — graphics are inline SVG or CSS — but the same alt-text policy is documented for any future bitmaps:

> Decorative graphics: `alt=""` (or `aria-hidden="true"` for SVG).
> Informative graphics: provide an `alt` that conveys the same information the sighted user gets.
> Charts / visualisations: `role="img"` + `<title>` + `<desc>` summarising the data and conclusion.

### 2.3 Structure, landmarks and keyboard

| # | Where | Issue | Fix |
|---|-------|-------|-----|
| S-1 | App shell had no skip link | Keyboard users had to tab through every nav item to reach content | Added `<a href="#main-content" class="skipLink">Skip to main content</a>` as the first focusable element; appears on focus only |
| S-2 | `<main>` had no id / focus target | Skip link couldn't land focus | Added `id="main-content"` and `tabIndex="-1"` to `<main>` |
| S-3 | Header / Footer used generic semantics | Screen-reader landmark list was sparse | Added `role="banner"` to header and `role="contentinfo"` to footer; footer inner element promoted to `<nav aria-label="Workflow navigation">` |
| S-4 | Stepper steps were `<div>` with `onClick` and no `tabIndex` | Steps were not reachable from the keyboard | Replaced with `<button type="button">`; native focus, native Enter/Space activation; `aria-label` for assistive tech, `aria-current="step"` on the active one |
| S-5 | Buttons across the app missing `type="button"` | Inside any future `<form>` they would default to `type="submit"` | Added `type="button"` to Header, Footer, Stepper, DomainPillBar, HelpModal, CSVUploader buttons |
| S-6 | HelpModal lacked dialog semantics | Screen-readers didn't announce it as a modal | Added `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to the title; close button receives focus on open; `Escape` closes |
| S-7 | No visible keyboard focus styles | WCAG 2.4.7 fail | Added a global `:focus-visible` outline using a new theme token `--color-focus-ring` (#58a6ff dark / #0969da light) that meets 3 : 1 against both backgrounds |
| S-8 | No reduced-motion support | WCAG 2.3.3 (AAA) — and ProgressRing animation was previously unconditional | Added `@media (prefers-reduced-motion: reduce)` block in `global.css` that flattens transitions/animations |

### 2.4 Theme & tokens (root cause clean-up)

| # | Token | Before | After | Reason |
|---|-------|--------|-------|--------|
| T-1 | `--color-text-secondary` (dark) | `#8b949e` | `#adbac7` | Push secondary text to ≥ 7 : 1 (AAA) so any text reusing it is safe |
| T-2 | `--color-text-muted` (dark) | `#6e7681` | `#8b949e` | Reach 4.5 : 1 minimum (now 6.13 : 1) |
| T-3 | `--color-text-secondary` (light) | `#57606a` | `#424a53` | Tightened to 8.5 : 1 against `#ffffff` |
| T-4 | `--color-accent-green-solid` | (didn't exist) | `#047857` | New token for "background that holds white text". All filled-green buttons now reference this. |
| T-5 | `--color-accent-green-solid-hover` | (didn't exist) | `#065f46` | Hover variant of T-4, still ≥ 4.5 : 1 |
| T-6 | `--color-focus-ring` | (didn't exist) | `#58a6ff` (dark) / `#0969da` (light) | Single source of truth for the `:focus-visible` outline color |
| T-7 | Light theme `--color-accent-green` / `-orange` / `-red` | inherited bright-on-light values | overridden to `#047857` / `#9a6700` / `#b91c1c` | Without the override these accents fail 4.5 : 1 against white |

---

## 3. Files Touched

```
frontend/index.html                                       # already had lang="en" — verified
frontend/src/App.jsx                                      # skip link, <main id> + tabIndex
frontend/src/styles/theme.css                             # token rework (T-1 … T-7)
frontend/src/styles/global.css                            # focus-visible, .skipLink, .visually-hidden, reduced-motion
frontend/src/components/Header/Header.jsx                 # logo role=img, button type, aria-pressed, aria-hidden SVGs
frontend/src/components/Header/Header.module.css          # logo + helpBtn → accent-green-solid
frontend/src/components/Footer/Footer.jsx                 # nav landmark, aria-labels, aria-hidden glyphs
frontend/src/components/Footer/Footer.module.css          # nextBtn → accent-green-solid
frontend/src/components/Stepper/Stepper.jsx               # <div> → <button>, aria-label, aria-hidden number
frontend/src/components/Stepper/Stepper.module.css        # button reset (transparent bg, inherit font)
frontend/src/components/DomainPillBar/DomainPillBar.jsx   # button types, aria-hidden glyphs
frontend/src/components/DomainPillBar/DomainPillBar.module.css  # active pill → accent-green-solid
frontend/src/components/HelpModal/HelpModal.jsx           # dialog role, focus mgmt, Escape to close
frontend/src/components/HelpModal/HelpModal.module.css    # h3 contrast fix (decorative bar)
frontend/src/components/ROCCurve/ROCCurve.jsx             # <title> + <desc>, aria-labelledby
frontend/src/components/ProgressRing/ProgressRing.jsx     # role=img, aria-label, <title>
frontend/src/components/CSVUploader/CSVUploader.jsx       # button types, group label, hidden input aria-label
```

---

## 4. How to Re-verify

1. **Lighthouse (Chrome DevTools):**
   - `cd frontend && npm run dev`
   - Open `http://localhost:5173` in an Incognito Chrome window
   - DevTools → Lighthouse → category **Accessibility** only → Mobile → *Analyze page load*
   - Repeat with `data-theme="light"` set on `<html>` to verify both themes
   - Acceptance: score ≥ 85 in both themes

2. **axe DevTools** browser extension — run on each step (1 → 7); zero serious / critical issues expected.

3. **Keyboard-only walkthrough:**
   - `Tab` from page load — first stop is the "Skip to main content" link
   - `Enter` jumps focus into `<main>`
   - Tab order: Header buttons → Domain pills → Stepper → step content → Footer Back/Next
   - All controls show the focus ring; `Esc` closes the Help modal

4. **Contrast spot-checks** with the [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) for any new color introduced.

---

## 5. Known Follow-ups (Out of Scope for This Ticket)

- Decorative SVGs inside the per-model visualisations (KNN, SVM, RF, NB, DT, LR) still need a uniform pass to add `aria-hidden="true"` on legend swatches and `<title>`/`<desc>` on the main plot SVG. Lighthouse does not flag these (they have no accessible name to fail), but VoiceOver currently announces empty graphics. — **Tracked as a follow-up on the next sprint.**
- Confusion Matrix conveys outcomes partly through colour (green/amber/red). Each cell already carries a text label and description, so it is technically WCAG 1.4.1 compliant, but adding an icon/pattern per category would strengthen perception for monochromacy. — **Future enhancement.**
- A future automated check via `eslint-plugin-jsx-a11y` and a CI Lighthouse step would prevent regressions.
