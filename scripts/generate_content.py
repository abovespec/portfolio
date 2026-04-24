#!/usr/bin/env python3
"""
Generate Astro content collection entries for texture images.
Reads metadata.json from each texture directory and creates corresponding .md files.

Usage:
    python generate_content.py --textures-dir ./public/textures --content-dir ./src/content/textures
"""

import argparse
import glob
import json
import os


def generate_content(textures_dir, content_dir):
    os.makedirs(content_dir, exist_ok=True)

    texture_dirs = sorted(glob.glob(os.path.join(textures_dir, '*/*')))
    created = 0

    for td in texture_dirs:
        meta_path = os.path.join(td, 'metadata.json')
        if not os.path.exists(meta_path):
            continue

        with open(meta_path) as f:
            meta = json.load(f)

        slug = meta['seedName'].lower().replace(' ', '-').replace('_', '-')
        category = meta['category']

        md = f"""---
title: "{meta['title']}"
description: "{meta['description']}"
category: "{category}"
tags:
  - "{category}"
  - "seamless"
  - "tileable"
  - "4k"
resolution: "4K"
maps:
  albedo: true
  normal: true
  roughness: true
  metallic: {meta['params'].get('metallic', 0) > 0}
  height: false
license: "CC0"
seed: "{meta['seed']}"
generatedDate: "{meta['generatedDate']}"
publishDate: "{meta['generatedDate']}"
urlSlug: "{slug}"
thumbnail: "/textures/{category}/{slug}/thumbnail.png"
preview: "/textures/{category}/{slug}/preview.png"
fullSize: "/textures/{category}/{slug}/albedo.png"
draft: false
---
"""
        md_path = os.path.join(content_dir, f'{slug}.md')
        with open(md_path, 'w') as f:
            f.write(md)
        created += 1
        print(f"  Created {md_path}")

    print(f"\nDone! Created {created} content entries")


def main():
    parser = argparse.ArgumentParser(description='Generate content entries from texture metadata')
    parser.add_argument('--textures-dir', required=True, help='Path to public/textures directory')
    parser.add_argument('--content-dir', required=True, help='Path to src/content/textures directory')
    args = parser.parse_args()
    generate_content(args.textures_dir, args.content_dir)


if __name__ == '__main__':
    main()
