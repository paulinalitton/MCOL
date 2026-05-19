#!/usr/bin/env python3
"""
SEO schema pass for the 108 city service pages.

Per the brief: every page's LocalBusiness JSON-LD must carry city-specific
addressLocality, geo coordinates, and areaServed. The current address block
hardcodes "streetAddress: Franklin, TN" on all 108 files — semantically
broken and identical across cities, so Google sees no locale differentiator
in the structured data. This script replaces that block in-place and trims
the 22 meta descriptions that exceeded 155 chars.

City coordinates are city-center values rounded to 4 decimals
(public US Census / Wikipedia geometry).
"""
from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "website pages"

CITIES = {
    "belle-meade":     ("Belle Meade",     36.1067, -86.8589),
    "bellevue":        ("Bellevue",        36.0742, -86.9492),
    "brentwood":       ("Brentwood",       35.9890, -86.7833),
    "forest-hills":    ("Forest Hills",    36.0570, -86.8086),
    "franklin":        ("Franklin",        35.9251, -86.8689),
    "gallatin":        ("Gallatin",        36.3879, -86.4475),
    "green-hills":     ("Green Hills",     36.1083, -86.8181),
    "hendersonville":  ("Hendersonville",  36.3047, -86.6200),
    "lebanon":         ("Lebanon",         36.2081, -86.2911),
    "mt-juliet":       ("Mt. Juliet",      36.2009, -86.5186),
    "nashville":       ("Nashville",       36.1627, -86.7816),
    "spring-hill":     ("Spring Hill",     35.7512, -86.9300),
}

SERVICES = [
    "bistro-lighting", "christmas-lights", "commercial-lighting",
    "home-exterior-lighting", "landscape-lighting", "outdoor-audio",
    "outdoor-lighting", "pool-lighting", "security-lighting",
]

OLD_ADDRESS_BLOCK = re.compile(
    r'  "address": \{\n'
    r'    "@type": "PostalAddress",\n'
    r'    "streetAddress": "Franklin, TN",\n'
    r'    "addressCountry": "US"\n'
    r'  \},\n'
)


def new_address_block(city_name: str, lat: float, lng: float) -> str:
    return (
        '  "address": {\n'
        '    "@type": "PostalAddress",\n'
        f'    "addressLocality": "{city_name}",\n'
        '    "addressRegion": "TN",\n'
        '    "addressCountry": "US"\n'
        '  },\n'
        '  "geo": {\n'
        '    "@type": "GeoCoordinates",\n'
        f'    "latitude": {lat},\n'
        f'    "longitude": {lng}\n'
        '  },\n'
        '  "areaServed": {\n'
        '    "@type": "City",\n'
        f'    "name": "{city_name}, TN"\n'
        '  },\n'
    )


# Per-page trimmed meta descriptions for the 22 pages that exceeded 155 chars.
# Each rewrite preserves city + service keywords; cuts mainly trailing flourish.
DESC_TRIMS: dict[str, tuple[str, str]] = {
    "belle-meade/christmas-lights.html": (
        "Belle Meade Christmas light installation done quietly — warm-white LEDs, classic rooflines, clips never staples, and seasonal display sensibility the city expects.",
        "Belle Meade Christmas light installation — warm-white LEDs, classic rooflines, clips never staples, seasonal display sensibility the city expects.",
    ),
    "belle-meade/outdoor-audio.html": (
        "Outdoor audio for Belle Meade estates — disguised rock speakers, buried subs, and tight-spill coverage designed around tree-protection and neighbor sightlines.",
        "Outdoor audio for Belle Meade estates — disguised rock speakers, buried subs, tight-spill coverage built around tree-protection ordinances.",
    ),
    "belle-meade/security-lighting.html": (
        "Discreet security lighting for Belle Meade estates — full-cutoff motion fixtures, warm 3000K LEDs, and concealed sensors engineered around city aesthetic codes.",
        "Discreet security lighting for Belle Meade estates — full-cutoff motion fixtures, warm 3000K LEDs, concealed sensors built for city aesthetic codes.",
    ),
    "brentwood/christmas-lights.html": (
        "Estate Christmas light installation in Brentwood TN — long rooflines, mature trees, full-service hang, maintain, takedown, and storage across Williamson County.",
        "Estate Christmas light installation in Brentwood TN — long rooflines, mature trees, full-service hang, maintain, takedown, and storage.",
    ),
    "brentwood/commercial-lighting.html": (
        "Commercial outdoor lighting for Brentwood TN — Maryland Way corporate corridor, restaurants, HOA entries, and Williamson County office park service contracts.",
        "Commercial outdoor lighting for Brentwood TN — Maryland Way corridor, restaurants, HOA entries, Williamson County office park contracts.",
    ),
    "brentwood/home-exterior-lighting.html": (
        "Architectural exterior lighting for Brentwood TN estate homes. Façade, soffit, column uplight, and lantern replacement for Annandale, Governors Club, Maryland Way.",
        "Architectural exterior lighting for Brentwood TN estates — façade, soffit, column uplight, lantern swap for Annandale and Governors Club.",
    ),
    "brentwood/outdoor-audio.html": (
        "Estate outdoor audio for Brentwood TN — zoned coverage across 1–5 acre Williamson County yards, disguised rock speakers near pools, Annandale and Governors Club.",
        "Estate outdoor audio for Brentwood TN — zoned coverage across 1–5 acre yards, disguised rock speakers, Annandale and Governors Club.",
    ),
    "brentwood/pool-lighting.html": (
        "Estate pool lighting in Brentwood TN — underwater LED retrofit and perimeter design for Williamson County backyards near Crockett Park and Brentwood Country Club.",
        "Estate pool lighting in Brentwood TN — underwater LED retrofit and perimeter design for backyards near Crockett Park and Brentwood Country Club.",
    ),
    "brentwood/security-lighting.html": (
        "Estate security lighting for Brentwood TN — long-driveway approach, perimeter, gate, and camera-paired motion zones for 1–5 acre Williamson County properties.",
        "Estate security lighting for Brentwood TN — long-driveway approach, perimeter, gate, and camera-paired motion zones for 1–5 acre lots.",
    ),
    "gallatin/christmas-lights.html": (
        "Professional Christmas light installation in Gallatin TN — historic Public Square homes to acreage along Long Hollow Pike. We install, maintain, take down, store.",
        "Christmas light installation in Gallatin TN — Public Square historic homes to Long Hollow Pike acreage. Hang, maintain, take down, store.",
    ),
    "gallatin/commercial-lighting.html": (
        "Commercial outdoor lighting for Gallatin TN businesses — Public Square storefronts, Volunteer State Community College, Long Hollow Pike retail, service contracts.",
        "Commercial outdoor lighting for Gallatin TN — Public Square storefronts, Volunteer State campus, Long Hollow Pike retail, service contracts.",
    ),
    "gallatin/home-exterior-lighting.html": (
        "Architectural exterior lighting for Gallatin TN homes — historic brick around Public Square to columned acreage along Long Hollow Pike. Smart-control ready.",
        "Architectural exterior lighting for Gallatin TN — Public Square historic brick to Long Hollow Pike columned acreage. Smart-control ready.",
    ),
    "gallatin/outdoor-audio.html": (
        "Outdoor audio design and installation across Gallatin TN — Foxland Harbor patios, Long Hollow Pike acreage, Triple Creek pools. App-controlled, zoned, weatherproof.",
        "Outdoor audio across Gallatin TN — Foxland Harbor patios, Long Hollow Pike acreage, Triple Creek pools. App-controlled, zoned, weatherproof.",
    ),
    "mt-juliet/bistro-lighting.html": (
        "Engineered bistro & catenary string lighting for Mt. Juliet patios and pergolas — humid-rated bulbs, hidden feeds, HOA-friendly mounting near Old Hickory Lake.",
        "Bistro & catenary string lighting for Mt. Juliet patios — humid-rated bulbs, hidden feeds, HOA-friendly mounting near Old Hickory Lake.",
    ),
    "mt-juliet/christmas-lights.html": (
        "Full-service Christmas light installation for Mt. Juliet TN — we supply, hang, maintain, take down, and store. HOA-friendly displays, no climbing your ladder.",
        "Full-service Christmas light installation for Mt. Juliet TN — supply, hang, maintain, take down, store. HOA-friendly, no ladder for you.",
    ),
    "mt-juliet/home-exterior-lighting.html": (
        "Architectural exterior lighting for Mt. Juliet homes — facade uplighting, soffit downlights, hidden wiring for new-build subdivisions and lakefront properties.",
        "Architectural exterior lighting for Mt. Juliet TN — façade uplighting, soffit downlights, hidden wiring for new-builds and lakefront homes.",
    ),
    "mt-juliet/security-lighting.html": (
        "Motion-sensor & dusk-to-dawn security lighting for Mt. Juliet TN homes — deters intruders, integrates with cameras, designed for Wilson County subdivisions.",
        "Motion-sensor & dusk-to-dawn security lighting for Mt. Juliet TN — camera-integrated, glare-controlled, built for Wilson County subdivisions.",
    ),
    "nashville/commercial-lighting.html": (
        "Commercial lighting in Nashville TN — Lower Broadway storefronts, Nissan Stadium area venues, Germantown restaurants. Service contracts and overlay-compliant builds.",
        "Commercial lighting in Nashville TN — Lower Broadway storefronts, Nissan Stadium venues, Germantown restaurants. Overlay-compliant builds.",
    ),
    "nashville/landscape-lighting.html": (
        "Custom low-voltage landscape lighting in Nashville TN — from 12 South cottages to Radnor Lake estates. Plant-safe, code-aware, designed at dusk on your lot.",
        "Low-voltage landscape lighting in Nashville TN — 12 South cottages to Radnor Lake estates. Plant-safe, code-aware, designed at dusk on-site.",
    ),
    "nashville/pool-lighting.html": (
        "Pool lighting in Nashville TN — underwater LEDs and perimeter design for Belmont, Hillsboro Village, and Radnor Lake area backyards. Shielded, code-aware, swim-safe.",
        "Pool lighting in Nashville TN — underwater LEDs and perimeter design for Belmont, Hillsboro Village, Radnor Lake backyards. Shielded, swim-safe.",
    ),
    "nashville/security-lighting.html": (
        "Security lighting in Nashville TN — code-conscious motion and dusk-to-dawn coverage from East Nashville bungalows to the Brentwood line. No floodlight glare.",
        "Security lighting in Nashville TN — code-aware motion and dusk-to-dawn from East Nashville bungalows to the Brentwood line. No glare.",
    ),
    "spring-hill/christmas-lights.html": (
        "Professional Christmas light installation in Spring Hill TN. HOA-approved displays from Wades Grove to McEwen Town Center — we hang, maintain, take down, store.",
        "Christmas light installation in Spring Hill TN — HOA-approved displays from Wades Grove to McEwen Town Center. Hang, maintain, take down, store.",
    ),
}


def patch_address(text: str, city_name: str, lat: float, lng: float) -> tuple[str, int]:
    new_block = new_address_block(city_name, lat, lng)
    new_text, n = OLD_ADDRESS_BLOCK.subn(new_block, text, count=1)
    return new_text, n


def patch_description(text: str, old_desc: str, new_desc: str) -> tuple[str, int]:
    if len(new_desc) > 155:
        raise ValueError(f"Replacement still over 155 chars ({len(new_desc)}): {new_desc!r}")
    n = 0
    # Replace the bare meta description (do NOT touch og:description / twitter:description
    # — those have looser limits and stay as the long-form social card copy).
    pat = f'name="description" content="{re.escape(old_desc)}"'
    repl = f'name="description" content="{new_desc}"'
    new_text, count = re.subn(pat, repl, text)
    n += count
    return new_text, n


def main() -> None:
    address_fixed = 0
    desc_fixed = 0
    for city_slug, (city_name, lat, lng) in CITIES.items():
        for service in SERVICES:
            rel = f"{city_slug}/{service}.html"
            path = ROOT / rel
            text = path.read_text(encoding="utf-8")

            text, addr_n = patch_address(text, city_name, lat, lng)
            if addr_n != 1:
                raise RuntimeError(f"{rel}: expected 1 address replacement, got {addr_n}")
            address_fixed += addr_n

            if rel in DESC_TRIMS:
                old_desc, new_desc = DESC_TRIMS[rel]
                text, desc_n = patch_description(text, old_desc, new_desc)
                if desc_n != 1:
                    raise RuntimeError(f"{rel}: expected 1 description replacement, got {desc_n}")
                desc_fixed += desc_n

            path.write_text(text, encoding="utf-8")

    print(f"address blocks rewritten: {address_fixed}")
    print(f"meta descriptions trimmed: {desc_fixed}")


if __name__ == "__main__":
    main()
