#!/usr/bin/env python3
"""
Quality-neutral image performance pass.

Adds two attributes to every <img> tag whose src= points to a real
image file in the repo:

  loading="lazy"   — defers off-screen image fetches until needed
  width="W" height="H" — intrinsic pixel dimensions so the browser
                          reserves correct space and avoids CLS layout
                          shift while images load

Both are HTML attribute additions only — no pixel data is touched and
no file is re-encoded. Hero scenes use CSS layers, not <img>, so blanket
loading="lazy" is safe (the LCP element isn't an <img>).

Skips:
  - <img src="">   (dynamic placeholders populated by JS)
  - <video> tags   (already have preload="metadata")
  - CSS background-image: url(...) refs
  - <img> tags that already have width / height / loading set

Idempotent — safe to re-run.
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "website pages"
DIMS_TSV = Path("/tmp/mcol_dims/dimensions.tsv")


def load_dims() -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for line in DIMS_TSV.read_text().splitlines():
        path, wh = line.split("\t", 1)
        w, h = wh.split()
        out[path] = (int(w), int(h))
    return out


SRC_RE = re.compile(r'src="([^"]*)"')
ATTR_PRESENT = {
    "width":   re.compile(r'\bwidth\s*='),
    "height":  re.compile(r'\bheight\s*='),
    "loading": re.compile(r'\bloading\s*='),
}

IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)


def augment_img(tag: str, dims: dict[str, tuple[int, int]]) -> str:
    m = SRC_RE.search(tag)
    if not m:
        return tag
    src = m.group(1).strip()
    if not src:
        return tag  # dynamic placeholder

    wh = dims.get(src)
    if not wh:
        # Try alt-prefix lookups (some pages may not use "../" prefix
        # for the same logical file).
        alt = src.lstrip("../")
        wh = dims.get(alt) or dims.get(f"../{alt}")
    if not wh:
        return tag  # unknown image, leave alone

    w, h = wh
    new = tag
    if not ATTR_PRESENT["width"].search(new):
        new = new[:-1] + f' width="{w}"' + ">"
    if not ATTR_PRESENT["height"].search(new):
        new = new[:-1] + f' height="{h}"' + ">"
    if not ATTR_PRESENT["loading"].search(new):
        new = new[:-1] + ' loading="lazy"' + ">"
    return new


def patch(path: Path, dims: dict[str, tuple[int, int]]) -> int:
    text = path.read_text(encoding="utf-8")
    edits = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal edits
        tag = m.group(0)
        new = augment_img(tag, dims)
        if new != tag:
            edits += 1
        return new

    new_text = IMG_TAG_RE.sub(repl, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
    return edits


def main() -> None:
    dims = load_dims()
    print(f"Loaded {len(dims)} image dimensions")
    total_edits = 0
    files_touched = 0
    for path in list(PAGES.glob("*.html")) + list(PAGES.glob("*/*.html")):
        n = patch(path, dims)
        if n:
            files_touched += 1
            total_edits += n
    print(f"Files touched: {files_touched}")
    print(f"<img> tags augmented: {total_edits}")


if __name__ == "__main__":
    main()
