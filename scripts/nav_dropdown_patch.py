#!/usr/bin/env python3
"""
Add a Services dropdown to the nav of every non-Home page.

Home.html and faq.html already use Template A — a "rich" nav with the
<div class="nav-drop"> Services widget. The other 121 pages (about,
Portfolio, estimator, contact, 9 root service pages, 108 city pages)
use Template B — a "pill" nav where Services is just a single link
to Home.html#services. That forces visitors to detour through Home
to reach any service from anywhere else.

This script upgrades Template B in place:
  - Markup: replaces the single Services anchor with the same
    <div class="nav-drop"> widget Home uses, panel listing all 9
    root service pages.
  - CSS:    injects nav-drop styles scoped under .page-head .nav so
    the dropdown inherits the existing pill nav colors (--ink-dim,
    --amber, --rule, etc.).
  - Path prefix: pages inside city/ folders get "../" on every
    service link; root-level pages get bare hrefs.
  - Active state: if the current page's Services link was marked
    class="on", that class transfers to the new trigger.

Idempotent — re-running is a no-op (sentinel "/* nav-drop styles */"
on the CSS, presence of <div class="nav-drop"> in the nav for markup).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "website pages"

# These already use Template A — don't touch their nav.
SKIP = {"Home.html", "faq.html"}

SERVICE_LINKS = [
    ("Outdoor Lighting",         "outdoor-lighting.html"),
    ("Landscape Lighting",       "Landscape_Lighting.html"),
    ("Bistro &amp; String Lighting", "bistro-lighting.html"),
    ("Pool Lighting",            "pool-lighting.html"),
    ("Home Exterior Lighting",   "home-exterior-lighting.html"),
    ("Security Lighting",        "security-lighting.html"),
    ("Christmas Lights",         "christmas-lights.html"),
    ("Commercial Lighting",      "commercial-lighting.html"),
    ("Outdoor Audio",            "outdoor-audio.html"),
]

NAV_DROP_CSS_SENTINEL = "/* nav-drop styles */"

NAV_DROP_CSS = """  /* nav-drop styles */
  .page-head .nav .nav-drop{position:relative;display:inline-block}
  .page-head .nav .nav-drop-trigger{
    padding:8px 14px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;
    color:var(--ink-dim);border:1px solid transparent;border-radius:999px;
    cursor:pointer;display:inline-flex;align-items:center;gap:4px;
    transition:all .2s;user-select:none;outline:none;
  }
  .page-head .nav .nav-drop-trigger.on{color:var(--amber);border-color:var(--rule)}
  .page-head .nav .nav-drop:hover .nav-drop-trigger,
  .page-head .nav .nav-drop:focus-within .nav-drop-trigger{color:var(--ink)}
  .page-head .nav .nav-drop-trigger svg{transition:transform .25s}
  .page-head .nav .nav-drop:hover .nav-drop-trigger svg,
  .page-head .nav .nav-drop:focus-within .nav-drop-trigger svg{transform:rotate(180deg)}
  .page-head .nav .nav-drop-panel{
    position:absolute;top:calc(100% + 8px);right:0;
    background:rgba(7,11,22,.96);border:1px solid var(--rule);border-radius:8px;
    padding:8px 0;min-width:240px;opacity:0;visibility:hidden;
    transform:translateY(-6px);
    transition:opacity .15s,transform .15s,visibility 0s linear .15s;
    backdrop-filter:blur(12px);z-index:90;
  }
  .page-head .nav .nav-drop:hover .nav-drop-panel,
  .page-head .nav .nav-drop:focus-within .nav-drop-panel{
    opacity:1;visibility:visible;transform:translateY(0);
    transition:opacity .15s,transform .15s;
  }
  .page-head .nav .nav-drop-panel a{
    display:block;padding:10px 20px;font-size:12px;letter-spacing:.1em;
    text-transform:none;color:var(--ink-dim);border:0;border-radius:0;
  }
  .page-head .nav .nav-drop-panel a:hover{color:var(--amber);background:rgba(245,239,225,.04)}
"""


# Match the existing Services anchor — both "Home.html#services" and "../Home.html#services" variants,
# with or without class="on".
SERVICES_LINK_RE = re.compile(
    r'<a\s+(?:class="on"\s+)?href="(?:\.\./)?Home\.html#services"(?:\s+class="on")?\s*>Services</a>',
    re.IGNORECASE,
)


def build_dropdown(prefix: str, is_active: bool) -> str:
    trigger_classes = "nav-drop-trigger on" if is_active else "nav-drop-trigger"
    items = "\n".join(
        f'        <a href="{prefix}{href}">{label}</a>'
        for label, href in SERVICE_LINKS
    )
    return (
        f'<div class="nav-drop">\n'
        f'      <span class="{trigger_classes}" tabindex="0">\n'
        f'        Services\n'
        f'        <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M6 9l6 6 6-6"/></svg>\n'
        f'      </span>\n'
        f'      <div class="nav-drop-panel">\n'
        f'{items}\n'
        f'      </div>\n'
        f'    </div>'
    )


def patch_nav_markup(text: str, prefix: str) -> tuple[str, bool]:
    if 'class="nav-drop"' in text:
        return text, False  # already has dropdown
    m = SERVICES_LINK_RE.search(text)
    if not m:
        return text, False
    is_active = 'class="on"' in m.group(0)
    new = SERVICES_LINK_RE.sub(build_dropdown(prefix, is_active), text, count=1)
    return new, True


def patch_css(text: str) -> tuple[str, bool]:
    if NAV_DROP_CSS_SENTINEL in text:
        return text, False
    # Inject before the last </style> in the file (the main page <style> block,
    # which closes near the end of <head> on these pages).
    idx = text.rfind("</style>")
    if idx == -1:
        return text, False
    new = text[:idx] + NAV_DROP_CSS + text[idx:]
    return new, True


def main() -> None:
    pages: list[Path] = []
    for p in PAGES.glob("*.html"):
        if p.name not in SKIP:
            pages.append(p)
    for d in sorted(x for x in PAGES.iterdir() if x.is_dir()):
        for p in d.glob("*.html"):
            pages.append(p)

    nav_n = css_n = skip_no_link = 0
    home_anomalies: list[str] = []

    for path in pages:
        rel = path.relative_to(PAGES)
        prefix = "" if len(rel.parts) == 1 else "../"

        text = path.read_text(encoding="utf-8")

        # Audit Home link as part of the same pass.
        expected_home = f'href="{prefix}Home.html"'
        if expected_home not in text:
            home_anomalies.append(str(rel))

        text, nav_changed = patch_nav_markup(text, prefix)
        text, css_changed = patch_css(text)

        if nav_changed:
            nav_n += 1
        elif 'class="nav-drop"' not in text:
            # Couldn't find the Services link AND no dropdown present.
            skip_no_link += 1
            print(f"  no Services link found, skipped: {rel}")

        if css_changed:
            css_n += 1

        if nav_changed or css_changed:
            path.write_text(text, encoding="utf-8")

    print(f"Pages considered: {len(pages)}")
    print(f"Nav dropdown injected: {nav_n}")
    print(f"CSS block injected: {css_n}")
    print(f"Pages skipped (no Services link to swap): {skip_no_link}")
    if home_anomalies:
        print(f"Home-link anomalies ({len(home_anomalies)}):")
        for a in home_anomalies:
            print(f"  {a}")


if __name__ == "__main__":
    main()
