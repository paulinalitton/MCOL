# Music City Outdoor Lighting — Codebase README

> Locally owned in Franklin, TN · 12+ years · 1,400+ projects lit across Middle Tennessee

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [File Structure](#2-file-structure)
3. [Brand Identity](#3-brand-identity)
4. [Typography](#4-typography)
5. [UI Component Patterns](#5-ui-component-patterns)
6. [Copywriting & Messaging Guidelines](#6-copywriting--messaging-guidelines)
7. [SEO Strategy & Keywords](#7-seo-strategy--keywords)
8. [Interactive Features](#8-interactive-features)
9. [Performance & Accessibility Notes](#9-performance--accessibility-notes)

---

## 1. Project Overview

**Business:** Music City Outdoor Lighting (MCOL)
**Service area:** Nashville · Franklin · Brentwood · Forest Hills · Belle Meade · Green Hills · Cool Springs
**Phone:** 615-905-1905
**Email:** musiccityoutdoorlighting@gmail.com
**Address:** 725 Cool Springs, Suite 600, Franklin, Tennessee 37067
**Hours:** Mon – Fri · 7:00 AM – 6:00 PM

### Pages in This Build

| File | Purpose |
|------|---------|
| `Services.html` | Main landing page with scroll-driven frame animation and service overview |
| `Landscape Lighting.html` | Landscape service page with three interactive hero layout variations |
| `Portfolio.html` | Project gallery with hover-to-light video cards |

---

## 2. File Structure

```
/
├── Services.html
├── Landscape Lighting.html
├── Portfolio.html
├── uploads/
│   ├── ezgif-3851a5f810730186-jpg/   # 25 frames for scroll animation (ezgif-frame-001.jpg … 025.jpg)
│   └── llp-house-lit.jpg             # Hero image for landscape lighting fixture demo
└── MCOL_Videos/
    ├── 231006 LLP-100.mp4
    ├── 250619 Mulholland-21.mp4
    ├── 2505 Sanfilippo-61.mp4
    ├── 250611 Ryan-20.mp4
    ├── Adams Drone-6.mp4
    ├── Hawks-13.mp4
    └── 0731 Dunco-17.mp4
```

### Frame Animation (Services.html)
- 25 sequential JPEG frames drive the background as the user scrolls
- Speed is controlled by the `revealSpeed` tweak (default `1.6`)
- Canvas is fixed, full-viewport; all content sections sit above it via `z-index: 1`

---

## 3. Brand Identity

### Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `--bg` | `#070b16` | Page background (deep navy-black) |
| `--bg-2` | `#0d1426` | Elevated surfaces, panels |
| `--ink` | `#f5efe1` | Primary text (warm off-white) |
| `--ink-dim` | `#a9a394` | Secondary / supporting text |
| `--ink-faint` | `#5a5547` | Tertiary text, disabled states |
| `--amber` | `#f0c074` | PRIMARY ACCENT — all gold iconography, highlights, CTAs |
| `--amber-soft` | `#e8b86a` | Hover variant |
| `--amber-glow` | `#ffd89a` | Glow/shadow tint on amber elements |
| `--rule` | `rgba(245,239,225,.12)` | Subtle dividers |
| `--rule-strong` | `rgba(245,239,225,.22)` | More visible dividers, ghost button borders |

> **Rule:** All iconography must render in `--amber` (`#f0c074`). Never use emojis. Use inline SVG icons with `stroke:currentColor` and `color: var(--amber)`.

### Accent Color Override (Tweaks Panel)
The accent color is runtime-overridable via `applyTweak('accent', hexValue)`. Any hardcoded amber reference should use the CSS variable `var(--amber)`, not a static hex, so overrides propagate correctly.

### Atmosphere
The brand palette simulates warm outdoor lighting at dusk — the dark background reads as a night sky / dark landscape; amber is the light source. Every design decision should reinforce this metaphor.

---

## 4. Typography

### Font Stack

```css
--serif: "Cormorant Garamond", "Times New Roman", serif;
--sans:  "Plus Jakarta Sans", system-ui, sans-serif;
```

Both are loaded from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale & Usage Rules

| Element | Font | Weight | Notes |
|---------|------|--------|-------|
| Display headings (`h1`, `h2`) | Cormorant Garamond | 300 | Italic `em` spans in amber for key phrase emphasis |
| Section titles | Cormorant Garamond | 300–400 | `clamp()` for fluid sizing |
| Body / UI text | Plus Jakarta Sans | 400 | Default running text |
| Labels / eyebrows | Plus Jakarta Sans | 600 | `letter-spacing: .28–.32em`, `text-transform: uppercase`, `font-size: 10–12px` |
| Decorative numerals | Cormorant Garamond | italic | Used for section numbering, card indices |
| Form labels | Plus Jakarta Sans | — | `font-size: 11px`, `.22em` tracking, uppercase |

### Headline Pattern
Headings consistently follow the pattern: plain statement + `<em>` italic colored phrase.

```html
<h2>Twelve years of <em>lit nights.</em></h2>
<h1>We light the night, <em>brilliantly.</em></h1>
```

---

## 5. UI Component Patterns

### Buttons

Two primary variants. Always `border-radius: 999px` (pill shape). No square buttons.

```css
/* Primary CTA */
.btn-amber { background: var(--amber); color: #1a1305; }
.btn-amber:hover { background: var(--amber-glow); box-shadow: 0 12px 32px -10px rgba(240,192,116,.6); }

/* Ghost / secondary */
.btn-ghost { border: 1px solid var(--rule-strong); color: var(--ink); }
.btn-ghost:hover { border-color: var(--amber); color: var(--amber); }
```

Arrow icon pattern for primary CTAs:
```html
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <path d="M5 12h14M13 5l7 7-7 7"/>
</svg>
```

### Eyebrow / Section Labels

```html
<div class="section-eyebrow">
  <span class="num">01</span>
  <span>SECTION TITLE</span>
</div>
```
Style: `font-size: 11px`, `letter-spacing: .32em`, `text-transform: uppercase`, `color: var(--amber)`.

### Pill Toggle (Landscape Lighting page)

Active state uses amber border + background tint + LED glow dot:
```css
.pill.on {
  color: var(--amber);
  border-color: var(--amber);
  background: rgba(240,192,116,.12);
  box-shadow: 0 0 24px -4px rgba(240,192,116,.45);
}
.pill.on .led {
  background: var(--amber);
  box-shadow: 0 0 10px var(--amber-glow);
}
```

### Nav

- Fixed, transparent on load → `background: rgba(7,11,22,.78)` + `backdrop-filter: blur(14px)` once `window.scrollY > 40`
- Active link: `color: var(--ink)` + 1px amber underline pseudo-element
- Hides `.nav-links` below 1024px, hides `.nav-phone` below 640px
- CTA button always visible

### Cards (Portfolio)

- `aspect-ratio: 4/3` default; `.feat` spans 2 columns + 2 rows on ≥1280px screens
- Dark `filter` on video until `.lit` class applied on hover/tap
- Progress bar (`2px` strip, bottom edge) appears when lit
- State pill + category tag positioned in top corners

### Service Cards (`.svc`)

- 3-column grid, 1px gap on `var(--rule)` background (creates hairline dividers)
- Hover: radial amber glow from bottom, background lifts to `rgba(13,20,38,.96)`
- Arrow gap widens on hover (`gap: 8px` → `gap: 14px`) as motion cue

### Contact Form

- All inputs borderless except bottom border (`border-bottom: 1px solid var(--rule-strong)`)
- Focus state: bottom border color → `var(--amber)`
- Submit button: full-width, `background: var(--amber)`, `border-radius: 0`

### Reveal on Scroll

```js
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('in'); });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));
```
Elements start at `opacity: 0; transform: translateY(28px)` and transition to visible.

---

## 6. Copywriting & Messaging Guidelines

### Brand Voice

| Attribute | Description |
|-----------|-------------|
| Confident | Statements, not questions. "We light the night." not "We can help you." |
| Poetic | Short, punchy. Serif italics for the emotional punch word. |
| Local | Always reference specific Tennessee cities; "Middle Tennessee" over generic "the area" |
| Understated | Let imagery and lighting do the talking; avoid hyperbole |
| Action-first | CTAs lead with the value, not the ask: "Free Design Consultation" not "Contact Us" |

### Headline Formula

```
[Simple declarative verb phrase] + [italic amber kicker]
```

Examples from the site:
- "We light the night, *brilliantly.*"
- "Five layers, one *signature* after-dark."
- "Every property has a *second face* after dark."
- "Let's design your *evenings.*"
- "Twelve years of *lit nights.*"

### CTA Copy Standards

| Context | Primary CTA | Secondary CTA |
|---------|------------|---------------|
| Hero sections | "Free Design Consultation" | "615-905-1905" |
| Section closers | "Free Design Consultation" | "Read Client Stories" / "See Our Work" |
| Contact section | "Request Free Consultation" | — |

### Trust Signals (use consistently across pages)
- ★★★★★ 5-Star Rated (Google & BBB)
- 12+ Years Lighting Nashville
- 1,400+ Projects
- Locally owned in Franklin, TN

### Tone to Avoid
- Exclamation points
- Emoji (use gold SVG iconography instead)
- Generic phrases: "world-class," "best-in-class," "cutting-edge"
- First-person plural overuse ("we we we"); vary with second-person ("your evenings")
- Em dashes (use a comma, period, or rewrite the sentence instead)
- Contrast phrasing: avoid constructions like "not just X, but Y," "more than just X," or "it's not about X, it's about Y" — these read as filler and weaken the voice

---

## 7. SEO Strategy & Keywords

### Primary Target Keywords

These are the terms all page copy and meta tags should be optimized for. Use naturally — do not force.

| Priority | Keyword | Search Intent |
|----------|---------|---------------|
| ★★★ | outdoor lighting Nashville TN | Local service, high commercial intent |
| ★★★ | landscape lighting Nashville | Local service |
| ★★★ | outdoor lighting Franklin TN | Local service |
| ★★★ | landscape lighting Brentwood TN | Local service |
| ★★ | architectural lighting Nashville | Specific service |
| ★★ | pool lighting Nashville | Specific service |
| ★★ | outdoor lighting company Middle Tennessee | Regional |
| ★★ | custom outdoor lighting design Nashville | Transactional |
| ★ | bistro string lights outdoor Nashville | Long-tail |
| ★ | holiday lighting installation Nashville | Seasonal |
| ★ | commercial outdoor lighting Nashville | Commercial segment |
| ★ | outdoor lighting contractor Tennessee | Contractor-specific |

### Long-Tail Phrases to Weave Into Body Copy

- "outdoor lighting specialists in Middle Tennessee"
- "landscape lighting design and installation Nashville"
- "custom architectural façade lighting Franklin TN"
- "pool and patio lighting Brentwood"
- "outdoor lighting company near me Nashville"
- "LED landscape lighting upgrade Nashville"

### Page-Level SEO Assignments

**Services.html** — target: `outdoor lighting Nashville TN`, `landscape lighting Nashville`
- `<title>`: "Outdoor Lighting Services — Music City Outdoor Lighting | Nashville, TN"
- Meta description (~155 chars): "Custom landscape, architectural, and pool lighting designed for Middle Tennessee homes. Nashville's most-requested outdoor lighting specialists. Free consultation."

**Landscape Lighting.html** — target: `landscape lighting Nashville`, `landscape lighting Brentwood TN`
- `<title>`: "Landscape Lighting Nashville & Brentwood | Music City Outdoor Lighting"
- Meta description: "Expert landscape lighting installation across Nashville, Franklin, and Brentwood. Uplighting, moonlighting, path lights, and more. See your home lit up — free design consultation."

**Portfolio.html** — target: `outdoor lighting Nashville portfolio`, `landscape lighting before and after Nashville`
- `<title>`: "Outdoor Lighting Portfolio — Nashville TN | Music City Outdoor Lighting"
- Meta description: "Browse 1,400+ outdoor lighting projects across Nashville, Franklin, Brentwood, and Middle Tennessee. Hover to watch every home light up."

### Recommended Meta Tags (add to all pages)

```html
<meta name="description" content="[page-specific, see above]">
<meta name="keywords" content="outdoor lighting Nashville, landscape lighting Nashville TN, architectural lighting Franklin TN, pool lighting Brentwood">
<meta name="geo.region" content="US-TN">
<meta name="geo.placename" content="Franklin, Tennessee">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="Music City Outdoor Lighting">
<meta property="og:locale" content="en_US">

<!-- Schema.org Local Business (add to Services.html) -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Music City Outdoor Lighting",
  "telephone": "+16159051905",
  "email": "musiccityoutdoorlighting@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "725 Cool Springs, Suite 600",
    "addressLocality": "Franklin",
    "addressRegion": "TN",
    "postalCode": "37067",
    "addressCountry": "US"
  },
  "openingHours": "Mo-Fr 07:00-18:00",
  "areaServed": ["Nashville", "Franklin", "Brentwood", "Forest Hills", "Belle Meade", "Green Hills", "Cool Springs"],
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5",
    "reviewCount": "100"
  }
}
</script>
```

### SEO Content Checklist (per page)

- [ ] `<title>` includes primary keyword + brand name
- [ ] `<meta name="description">` is 140–160 chars, includes keyword and a CTA phrase
- [ ] `<h1>` contains primary keyword naturally (not forced)
- [ ] Service city names appear in body copy (Nashville, Franklin, Brentwood, etc.)
- [ ] Schema.org LocalBusiness JSON-LD on Services.html
- [ ] All images have descriptive `alt` attributes (e.g., `alt="Landscape lighting installation in Brentwood TN backyard"`)
- [ ] All videos have `<track>` caption files or descriptive surrounding text for crawlability
- [ ] Internal links between pages use keyword-rich anchor text
- [ ] Page loads fast — videos use `preload="metadata"`, images use modern formats where possible
- [ ] Canonical tags set on each page

### Internal Linking Strategy

Link anchor text should be descriptive, not generic:

| Instead of | Use |
|-----------|-----|
| "click here" | "see our Nashville landscape lighting portfolio" |
| "learn more" | "learn about our outdoor lighting process" |
| "contact us" | "schedule a free lighting design consultation" |

---

## 8. Interactive Features

### Scroll-Driven Frame Animation (Services.html)

- 25 JPEG frames loaded on init; frame index is `p * (TOTAL - 1)` where `p` is scroll progress clamped by `revealSpeed`
- Canvas draws cover-fit (letterbox if portrait, pillarbox if landscape)
- HUD strip (bottom-left, desktop only) shows progress bar + percentage

### Fixture Layer Toggle (Landscape Lighting.html)

- CSS `data-fix-*` attributes on `.stage` control layer opacity via attribute selectors
- Six fixture layers: `uplight`, `moonlight`, `path`, `bed`, `specimen`, `window`
- "All On" adds `.all-on` class which reveals `.l-ambient` (full-brightness composite) at `opacity: 1`
- "Play Sequence" animates fixtures on one by one at 700ms intervals using `setTimeout`
- Progress bar (`requestAnimationFrame` loop) tracks sequence duration

### Hover-to-Light Video (Portfolio.html)

- `mouseenter` → `classList.add('lit')` + `video.play()`
- `mouseleave` → removes `.lit`, pauses, resets `currentTime = 0`
- Mobile: tap toggles; tapping a second card unlights the first
- Filter chips show/hide cards by `data-cats` attribute; hidden cards are paused

---

## 9. Performance & Accessibility Notes

### Performance

- Videos use `preload="metadata"` and `muted loop playsinline` — never autoplay with sound
- Frame images should stay ≤ 150KB each (JPEG, 1920px wide max)
- `will-change: opacity` on `.layer` elements in Landscape Lighting for GPU compositing
- Backdrop-filter (`blur`) used extensively — test on low-power mobile devices; consider `@media (prefers-reduced-motion)` fallback removing blur

### Accessibility

- All decorative elements use `aria-hidden="true"` (marquee, HUD, page-bg canvas)
- Form uses `<label>` elements correctly associated with inputs
- Color contrast: `--ink` (#f5efe1) on `--bg` (#070b16) passes WCAG AA (contrast ~14:1)
- Amber (#f0c074) on dark bg passes AA for large text; verify for small UI text
- `prefers-reduced-motion` block in Portfolio.html disables all card transitions — extend this pattern to other pages
- Add `<track kind="descriptions">` to portfolio videos for screen reader support

### Browser Support

- `backdrop-filter` requires prefix for older Safari: `-webkit-backdrop-filter` (already applied)
- CSS `mask-image` compound values (Landscape Lighting fixture layers) require `-webkit-mask-image` prefix (already applied)
- `aspect-ratio` supported in all modern browsers; no fallback needed

---

*Last updated: 2026 · Music City Outdoor Lighting · Franklin, TN*
