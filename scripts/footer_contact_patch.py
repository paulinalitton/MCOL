#!/usr/bin/env python3
"""
Footer rebuild + contact-CTA wiring across all 122 site pages.

Why this exists: the prior footer was a single bottom-bar (copyright + Privacy/
Terms/etc.) with no internal links. After publishing 108 city service pages,
those pages were only discoverable from the Home page's Service Areas section
and a small grid on root service pages. To give every page footer-level
discoverability into the 12 city hubs and to give every page a working
Contact route, this script:

  1. Replaces the existing <footer>...</footer> on every HTML page with a
     four-column footer: Service Areas (12 cities) | Services (9) |
     Company (5) | bottom bar (copyright + legal).
  2. Resolves href prefixes per page depth — root pages get bare hrefs,
     pages inside city/ folders get ../ prefix.
  3. Replaces the placeholder <!-- FOOTER_PLACEHOLDER --> in the new
     contact.html with the same footer.
  4. Wires the dummy `href="#"` on Free Consultation / Free Design
     Consultation / Book Free Consultation CTAs to point at contact.html.

Sitemap and robots.txt updates run in a separate script.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "website pages"

CITIES = [
    ("Belle Meade",     "belle-meade"),
    ("Bellevue",        "bellevue"),
    ("Brentwood",       "brentwood"),
    ("Forest Hills",    "forest-hills"),
    ("Franklin",        "franklin"),
    ("Gallatin",        "gallatin"),
    ("Green Hills",     "green-hills"),
    ("Hendersonville",  "hendersonville"),
    ("Lebanon",         "lebanon"),
    ("Mt. Juliet",      "mt-juliet"),
    ("Nashville",       "nashville"),
    ("Spring Hill",     "spring-hill"),
]

# (label, filename inside the city folder)
CITY_SERVICES = [
    ("Landscape Lighting",  "landscape-lighting.html"),
    ("Outdoor Lighting",    "outdoor-lighting.html"),
    ("Home Exterior",       "home-exterior-lighting.html"),
    ("Pool Lighting",       "pool-lighting.html"),
    ("Bistro & String",     "bistro-lighting.html"),
    ("Security Lighting",   "security-lighting.html"),
    ("Christmas Lights",    "christmas-lights.html"),
    ("Commercial Lighting", "commercial-lighting.html"),
    ("Outdoor Audio",       "outdoor-audio.html"),
]

# Root-level services column (one canonical page per service, not city-scoped)
SERVICE_LINKS = [
    ("Landscape Lighting",      "Landscape_Lighting.html"),
    ("Outdoor Lighting",        "outdoor-lighting.html"),
    ("Bistro & String",         "bistro-lighting.html"),
    ("Pool Lighting",           "pool-lighting.html"),
    ("Home Exterior",           "home-exterior-lighting.html"),
    ("Security Lighting",       "security-lighting.html"),
    ("Christmas Lights",        "christmas-lights.html"),
    ("Commercial Lighting",     "commercial-lighting.html"),
    ("Outdoor Audio",           "outdoor-audio.html"),
]

COMPANY_LINKS = [
    ("Home",      "Home.html"),
    ("About",     "about.html"),
    ("Portfolio", "Portfolio.html"),
    ("FAQ",       "faq.html"),
    ("Estimator", "estimator.html"),
    ("Contact",   "contact.html"),
]


def build_footer(prefix: str) -> str:
    """prefix is "" for root-level pages, "../" for files inside city folders."""
    def render_links(items: list[tuple[str, str]]) -> str:
        return "\n".join(
            f'          <a href="{prefix}{href}" onmouseover="this.style.color=\'var(--amber)\'" onmouseout="this.style.color=\'\'" '
            f'style="color:var(--ink-dim);transition:color .2s;font-size:13px">{label}</a>'
            for label, href in items
        )

    def render_city_details() -> str:
        """A <details> accordion per city listing all 9 city-specific service pages.
        Footer-level discoverability for all 108 city service pages."""
        out = []
        for city_label, city_slug in CITIES:
            services_html = "\n".join(
                f'              <a href="{prefix}{city_slug}/{fname}" '
                f'onmouseover="this.style.color=\'var(--amber)\'" onmouseout="this.style.color=\'var(--ink-faint)\'" '
                f'style="color:var(--ink-faint);font-size:12px;transition:color .2s;padding:2px 0">{slabel}</a>'
                for slabel, fname in CITY_SERVICES
            )
            out.append(
                f'          <details style="font-size:13px">\n'
                f'            <summary onmouseover="this.style.color=\'var(--amber)\'" onmouseout="this.style.color=\'var(--ink-dim)\'" '
                f'style="cursor:pointer;color:var(--ink-dim);padding:4px 0;transition:color .2s;user-select:none">{city_label}</summary>\n'
                f'            <div style="display:flex;flex-direction:column;gap:3px;padding:6px 0 10px 14px;margin:4px 0 4px 3px;border-left:1px solid rgba(245,239,225,.1)">\n'
                f'{services_html}\n'
                f'            </div>\n'
                f'          </details>'
            )
        return "\n".join(out)

    bottom_links = [("Privacy", "#"), ("Terms", "#"), ("ADA", "#"),
                    ("Instagram", "#"), ("Facebook", "#")]
    bottom = "\n".join(
        f'      <a href="{href}" onmouseover="this.style.color=\'var(--amber)\'" onmouseout="this.style.color=\'\'">{label}</a>'
        for label, href in bottom_links
    )

    return f"""<footer style="border-top:1px solid var(--rule);padding:56px 48px 32px;font-size:13px;color:var(--ink-dim);background:rgba(7,11,22,.6);margin-top:0">
  <div style="max-width:1400px;margin:0 auto">
    <div style="display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:48px;margin-bottom:40px;padding-bottom:36px;border-bottom:1px solid var(--rule)">
      <div>
        <div style="font-family:var(--serif);font-weight:300;font-style:italic;font-size:20px;color:var(--ink);margin-bottom:18px">Service Areas</div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:2px 24px;align-content:start">
{render_city_details()}
        </div>
      </div>
      <div>
        <div style="font-family:var(--serif);font-weight:300;font-style:italic;font-size:20px;color:var(--ink);margin-bottom:18px">Services</div>
        <div style="display:flex;flex-direction:column;gap:8px">
{render_links(SERVICE_LINKS)}
        </div>
      </div>
      <div>
        <div style="font-family:var(--serif);font-weight:300;font-style:italic;font-size:20px;color:var(--ink);margin-bottom:18px">Company</div>
        <div style="display:flex;flex-direction:column;gap:8px">
{render_links(COMPANY_LINKS)}
        </div>
      </div>
    </div>
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:24px">
      <div>© 2026 Music City Outdoor Lighting · Locally owned in Franklin, TN</div>
      <div style="display:flex;gap:28px;flex-wrap:wrap">
{bottom}
      </div>
    </div>
  </div>
</footer>"""


FOOTER_RE = re.compile(r"<footer\b[\s\S]*?</footer>", re.IGNORECASE)
PLACEHOLDER_RE = re.compile(r"<!-- FOOTER_PLACEHOLDER -->")


# CTA wiring: turn dummy href="#" Free Consultation buttons into real contact links.
# Captures the prior class attribute so we only rewrite buttons (not random "#" anchors).
def cta_pattern(label: str) -> re.Pattern[str]:
    return re.compile(
        r'<a([^>]*class="btn btn-amber"[^>]*)\s+href="#"([^>]*)>(\s*'
        + re.escape(label)
        + r')',
        re.IGNORECASE,
    )

CTA_LABELS = ["Free Design Consultation", "Book Free Consultation", "Free Consultation", "Request Consultation"]


def patch_ctas(text: str, contact_href: str) -> int:
    n = 0
    for label in CTA_LABELS:
        pat = cta_pattern(label)
        text_new, count = pat.subn(
            lambda m: f'<a{m.group(1)} href="{contact_href}"{m.group(2)}>{m.group(3)}',
            text,
        )
        if count:
            n += count
            # Use the rewritten text on the next iteration
            text = text_new
    return n, text


def patch_file(path: Path) -> tuple[int, int]:
    rel = path.relative_to(PAGES)
    parts = rel.parts
    if len(parts) == 1:
        prefix = ""
        contact_href = "contact.html"
    else:
        prefix = "../"
        contact_href = "../contact.html"

    text = path.read_text(encoding="utf-8")
    footer = build_footer(prefix)

    if PLACEHOLDER_RE.search(text):
        text, footer_n = PLACEHOLDER_RE.subn(footer, text, count=1)
    else:
        text, footer_n = FOOTER_RE.subn(footer, text, count=1)

    cta_count, text = patch_ctas(text, contact_href)

    path.write_text(text, encoding="utf-8")
    return footer_n, cta_count


def main() -> None:
    pages: list[Path] = []
    # Root-level pages
    for p in PAGES.glob("*.html"):
        pages.append(p)
    # City subfolder pages
    for city_dir in sorted(d for d in PAGES.iterdir() if d.is_dir()):
        for p in city_dir.glob("*.html"):
            pages.append(p)

    total_footer = 0
    total_cta = 0
    no_footer_files: list[str] = []
    for p in pages:
        footer_n, cta_n = patch_file(p)
        if footer_n == 0:
            no_footer_files.append(str(p.relative_to(PAGES)))
        total_footer += footer_n
        total_cta += cta_n

    print(f"Pages processed: {len(pages)}")
    print(f"Footers replaced: {total_footer}")
    print(f"CTAs rewired to contact.html: {total_cta}")
    if no_footer_files:
        print(f"Pages with no <footer> block (skipped footer swap): {no_footer_files}")


if __name__ == "__main__":
    main()
