#!/usr/bin/env python3
"""
Add heroImage frontmatter field to the 60 Tier-2 blog articles (INF-169).
Runs after ai_generate_blog_heroes_inf169.py has produced all PNG files.

For each article that has a corresponding {slug}-hero.png in public/images/blog/,
inserts `heroImage: "/images/blog/{slug}-hero.png"` into the YAML frontmatter
(after the existing `draft:` field, or before the closing `---`).

Usage:
    python3 scripts/update_hero_frontmatter_inf169.py [--dry-run]
"""

import argparse
import os
import re
import sys

SITES = {
    "citefast.io": [
        "apa-7th-edition-guide",
        "harvard-referencing-guide",
        "how-to-cite-a-journal-article",
        "how-to-cite-website-apa",
        "how-to-cite-youtube-video",
        "in-text-citation-apa",
    ],
    "passwordgen.io": [
        "how-long-should-a-password-be",
        "multi-factor-authentication",
        "nist-password-guidelines",
        "password-entropy",
        "passwordless-authentication-passkeys",
        "two-factor-authentication",
    ],
    "colorpalette.io": [
        "analogous-colors",
        "color-palette-inspiration",
        "color-psychology-marketing",
        "dark-mode-color-palette",
        "hex-color-codes",
        "warm-vs-cool-colors",
    ],
    "pomotimer.io": [
        "free-pomodoro-timer",
        "how-to-stay-focused-studying",
        "pomodoro-technique-adhd",
        "pomodoro-technique-for-students",
        "pomodoro-technique-work-from-home",
        "time-management-for-students",
    ],
    "worldclock.io": [
        "gmt-vs-utc",
        "military-time-24-hour-clock",
        "pst-vs-pdt",
        "spring-forward-fall-back",
        "time-zone-converter-guide",
        "time-zone-map",
    ],
    "regexbuilder.io": [
        "regex-catastrophic-backtracking",
        "regex-find-replace",
        "regex-flags",
        "regex-javascript",
        "regex-phone-number",
        "regex-python",
    ],
    "caseconvert.io": [
        "database-naming-conventions",
        "javascript-naming-conventions",
        "python-naming-conventions-pep8",
        "snake-case-vs-kebab-case",
        "what-is-camelcase",
        "what-is-kebab-case",
    ],
    "uuidgen.io": [
        "nanoid-vs-uuid",
        "uuid-collision-probability",
        "uuid-database-performance",
        "uuid-python",
        "uuid-vs-auto-increment",
        "what-is-ulid",
    ],
    "crontab.io": [
        "cron-environment-variables",
        "cron-path-variable",
        "cron-timezone",
        "github-actions-schedule",
        "kubernetes-cronjob",
        "systemd-timer-vs-cron",
    ],
    "encodeonline.io": [
        "base64-python",
        "encoding-vs-encryption",
        "hex-to-ascii",
        "md5-vs-sha256",
        "sha256-hash-explained",
        "utf8-character-encoding",
    ],
}

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "sites")


def insert_hero_image(md_path, hero_image_path, dry_run):
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "heroImage:" in content:
        print(f"  SKIP (already has heroImage): {md_path}")
        return False

    # Find the closing --- of the frontmatter
    # Content starts with ---\n...\n---\n
    match = re.match(r"^(---\n)(.*?)(^---\n)", content, re.MULTILINE | re.DOTALL)
    if not match:
        print(f"  ERROR: no frontmatter found in {md_path}", file=sys.stderr)
        return False

    front_open = match.group(1)
    front_body = match.group(2)
    front_close = match.group(3)
    rest = content[match.end():]

    # Insert heroImage before the closing ---
    new_front_body = front_body.rstrip("\n") + f'\nheroImage: "{hero_image_path}"\n'
    new_content = front_open + new_front_body + front_close + rest

    if dry_run:
        print(f"  [dry-run] would insert heroImage in {md_path}")
        return True

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  Updated: {md_path}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    updated = 0
    skipped = 0
    missing_image = 0

    for site, slugs in SITES.items():
        for slug in slugs:
            hero_png = os.path.join(BASE_DIR, site, "public", "images", "blog", f"{slug}-hero.png")
            md_file = os.path.join(BASE_DIR, site, "src", "content", "blog", f"{slug}.md")

            if not os.path.exists(hero_png):
                print(f"  MISSING IMAGE: {hero_png}", file=sys.stderr)
                missing_image += 1
                continue

            if not os.path.exists(md_file):
                print(f"  MISSING MD: {md_file}", file=sys.stderr)
                continue

            hero_image_path = f"/images/blog/{slug}-hero.png"
            result = insert_hero_image(md_file, hero_image_path, args.dry_run)
            if result:
                updated += 1
            else:
                skipped += 1

    print(f"\nDone: {updated} updated, {skipped} skipped, {missing_image} missing images.")
    if missing_image > 0:
        print("Re-run image generation to fill missing images, then re-run this script.")
        sys.exit(1)


if __name__ == "__main__":
    main()
