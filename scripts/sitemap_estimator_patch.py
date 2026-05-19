#!/usr/bin/env python3
"""
Finishing pass:
  1. Insert contact.html into the sitemap (it didn't exist when sitemap.xml
     was generated).
  2. Move sitemap.xml from website%20pages/ to the repo root so Google
     Search Console gets a single canonical location at /sitemap.xml.
     URLs inside the file stay as /website%20pages/... because that's
     where the HTML actually lives on disk.
  3. Update robots.txt's Sitemap: line to point at the new root URL.
  4. Append the new footer to estimator.html — the footer patch script
     only swaps existing <footer> blocks, and estimator.html had none.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "website pages"

sys.path.insert(0, str(ROOT / "scripts"))
from footer_contact_patch import build_footer  # type: ignore  # reuse footer builder


CONTACT_URL_ENTRY = """  <url>
    <loc>https://musiccityoutdoorlighting.com/website%20pages/contact.html</loc>
    <lastmod>2026-05-20</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.9</priority>
  </url>
"""


def patch_sitemap() -> None:
    old_sitemap = PAGES / "sitemap.xml"
    new_sitemap = ROOT / "sitemap.xml"
    text = old_sitemap.read_text(encoding="utf-8")

    # Insert contact.html entry after the estimator.html block (keeps the
    # "supporting pages" cluster grouped near the top of the file).
    pattern = re.compile(
        r"(<url>\s*<loc>https://musiccityoutdoorlighting\.com/website%20pages/estimator\.html</loc>"
        r"[\s\S]*?</url>\n)"
    )
    text, n = pattern.subn(r"\1" + CONTACT_URL_ENTRY, text, count=1)
    if n != 1:
        raise RuntimeError(f"failed to find estimator.html anchor in sitemap (got {n} matches)")

    new_sitemap.write_text(text, encoding="utf-8")
    old_sitemap.unlink()
    print(f"  sitemap.xml moved: website pages/ → root, added contact.html (now {text.count('<loc>')} URLs)")


def patch_robots() -> None:
    robots = ROOT / "robots.txt"
    text = robots.read_text(encoding="utf-8")
    new = text.replace(
        "https://musiccityoutdoorlighting.com/website%20pages/sitemap.xml",
        "https://musiccityoutdoorlighting.com/sitemap.xml",
    )
    if new == text:
        raise RuntimeError("robots.txt sitemap line not found / already updated")
    robots.write_text(new, encoding="utf-8")
    print("  robots.txt sitemap URL updated → /sitemap.xml")


def patch_estimator_footer() -> None:
    estimator = PAGES / "estimator.html"
    text = estimator.read_text(encoding="utf-8")
    if "<footer" in text:
        print("  estimator.html already has a footer — skipping")
        return
    footer = build_footer(prefix="")
    new = text.replace("</body>", f"\n{footer}\n\n</body>", 1)
    if new == text:
        raise RuntimeError("estimator.html: </body> not found")
    estimator.write_text(new, encoding="utf-8")
    print("  estimator.html: footer appended before </body>")


def main() -> None:
    patch_sitemap()
    patch_robots()
    patch_estimator_footer()


if __name__ == "__main__":
    main()
