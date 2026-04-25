#!/usr/bin/env python3
"""
AI blog image generator for jsonformat.io dev-aesthetic articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Outputs:
  - 11 hero images -> sites/jsonformat.io/public/images/blog/<slug>-hero.png (1200x630)
  -  1 OG default  -> sites/jsonformat.io/public/og-default.png              (1200x630)

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_jsonformat.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_jsonformat.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — hero images for 11 jsonformat.io articles + 1 OG default
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (used for all images here)
BLOG_IMAGES = [
    # Site OG default image (output to public/, not images/blog/)
    {
        "slug": "og-default",
        "size": "hero",
        "output_dir_override": "sites/jsonformat.io/public",
        "prompt": (
            "Online JSON formatter tool interface, split-pane code editor with raw JSON "
            "on left and formatted indented JSON on right, dark syntax-highlighted theme, "
            "clean modern developer tool design, no people, abstract data visualization"
        ),
    },
    # Article 1 — 8 Common JSON Errors
    {
        "slug": "common-json-errors-hero",
        "size": "hero",
        "prompt": (
            "Code editor with a JSON file showing multiple red error highlight underlines, "
            "trailing comma and missing quote errors visible, dark terminal theme, "
            "syntax-highlighted monospace font, developer editing environment"
        ),
    },
    # Article 2 — Format JSON in Python
    {
        "slug": "format-json-python-hero",
        "size": "hero",
        "prompt": (
            "Python IDE with json.dumps code and formatted JSON output in console below, "
            "syntax-highlighted Python code with indented JSON result, "
            "dark terminal monospace theme, developer aesthetic"
        ),
    },
    # Article 3 — Format JSON in VS Code
    {
        "slug": "format-json-vscode-hero",
        "size": "hero",
        "prompt": (
            "VS Code editor open with a JSON file, command palette overlay showing "
            "Format Document option highlighted, dark developer theme, "
            "code editor interface, developer aesthetic"
        ),
    },
    # Article 4 — How to Minify JSON
    {
        "slug": "how-to-minify-json-hero",
        "size": "hero",
        "prompt": (
            "Side-by-side terminal comparison, formatted multi-line JSON on the left "
            "versus compact minified single-line JSON on the right, "
            "dark monospace terminal theme, before and after developer editorial"
        ),
    },
    # Article 5 — How to Validate JSON
    {
        "slug": "how-to-validate-json-hero",
        "size": "hero",
        "prompt": (
            "Code editor showing JSON schema validation results, "
            "green checkmarks beside valid fields and red error markers beside invalid ones, "
            "dark terminal syntax-highlighted theme, developer aesthetic"
        ),
    },
    # Article 6 — JSON Schema Guide
    {
        "slug": "json-schema-guide-hero",
        "size": "hero",
        "prompt": (
            "Abstract diagram of a JSON object tree structure, "
            "nested nodes with type annotation labels like string number boolean array, "
            "clean technical illustration on dark background, developer editorial style"
        ),
    },
    # Article 7 — JSON vs XML
    {
        "slug": "json-vs-xml-hero",
        "size": "hero",
        "prompt": (
            "Split-pane code editor showing JSON curly-brace data on the left "
            "and equivalent verbose XML markup on the right, "
            "dark syntax-highlighted terminal theme, developer comparison editorial"
        ),
    },
    # Article 8 — JSON vs YAML
    {
        "slug": "json-vs-yaml-hero",
        "size": "hero",
        "prompt": (
            "Side-by-side code editor panels, JSON with curly braces on the left "
            "and clean YAML indented syntax for the same data on the right, "
            "dark terminal monospace font, developer editorial comparison"
        ),
    },
    # Article 9 — Pretty-Print JSON in JavaScript
    {
        "slug": "pretty-print-json-javascript-hero",
        "size": "hero",
        "prompt": (
            "Browser DevTools console showing JSON.stringify output with 2-space indentation, "
            "JavaScript code snippet visible in editor panel, "
            "dark developer theme, browser debugging interface"
        ),
    },
    # Article 10 — Unexpected Token in JSON
    {
        "slug": "unexpected-token-json-error-hero",
        "size": "hero",
        "prompt": (
            "Code editor or terminal showing a SyntaxError Unexpected token error message "
            "with red error highlight on a problematic JSON line, "
            "developer debugging session, dark monospace theme, error traceback visible"
        ),
    },
    # Article 11 — What Is JSON?
    {
        "slug": "what-is-json-hero",
        "size": "hero",
        "prompt": (
            "Elegant abstract visualization of a JSON object with nested keys and values "
            "floating on a dark gradient background, curly braces and colon notation visible, "
            "clean minimal developer editorial, glowing blue code aestheticA"
        ),
    },
]

SIZES = {
    "hero": (1200, 630),
}

# ---------------------------------------------------------------------------
# Pipeline (lazy-loaded, identical to ai_generate_blog_images.py)
# ---------------------------------------------------------------------------
_pipe = None


def get_pipeline():
    global _pipe
    if _pipe is None:
        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        print("Loading ERNIE-Image-Turbo...", file=sys.stderr)
        from diffusers import ErnieImagePipeline
        from diffusers.quantizers.pipe_quant_config import PipelineQuantizationConfig
        from transformers import AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        import gc

        bnb_4bit = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        quant_config = PipelineQuantizationConfig(
            quant_backend="bitsandbytes_4bit",
            quant_kwargs={
                "load_in_4bit": True,
                "bnb_4bit_compute_dtype": torch.bfloat16,
                "bnb_4bit_use_double_quant": True,
            },
            components_to_quantize=["transformer"],
        )

        _pipe = ErnieImagePipeline.from_pretrained(
            "baidu/ERNIE-Image-Turbo",
            torch_dtype=torch.bfloat16,
            quantization_config=quant_config,
            cache_dir="/data/huggingface",
        )

        snap_dir = [
            d
            for d in os.listdir(
                "/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/"
            )
            if not d.startswith(".")
        ][0]
        snap_path = (
            f"/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/{snap_dir}"
        )

        del _pipe.text_encoder
        gc.collect()
        _pipe.text_encoder = AutoModel.from_pretrained(
            f"{snap_path}/text_encoder",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        del _pipe.pe
        gc.collect()
        _pipe.pe = AutoModelForCausalLM.from_pretrained(
            f"{snap_path}/pe",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        _pipe.transformer = _pipe.transformer.to("cuda:0")
        _pipe.vae = _pipe.vae.to("cuda:0")
        print(
            f"Pipeline ready. GPU0: {torch.cuda.mem_get_info(0)[1]/1e9:.1f}GB, "
            f"GPU1: {torch.cuda.mem_get_info(1)[1]/1e9:.1f}GB",
            file=sys.stderr,
        )
    return _pipe


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------
def center_crop_to_ratio(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def generate_image(spec: dict, default_output_dir: str, skip_existing: bool = True) -> str:
    slug = spec["slug"]
    size_key = spec["size"]
    prompt = spec["prompt"]
    target_w, target_h = SIZES[size_key]

    # Respect per-entry output dir override (for og-default)
    if "output_dir_override" in spec:
        output_dir = os.path.abspath(spec["output_dir_override"])
    else:
        output_dir = default_output_dir

    out_path = os.path.join(output_dir, f"{slug}.png")
    if skip_existing and os.path.exists(out_path):
        print(f"  [skip] {slug}.png already exists", file=sys.stderr)
        return out_path

    pipe = get_pipeline()
    import torch

    seed_val = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    print(f"  [{slug}] Generating ({target_w}x{target_h})...", file=sys.stderr)
    t0 = time.time()

    torch.cuda.empty_cache()
    raw = pipe(
        prompt=prompt,
        height=1024,
        width=1024,
        num_inference_steps=8,
        generator=torch.Generator(device="cpu").manual_seed(seed_val),
    ).images[0]

    final = center_crop_to_ratio(raw, target_w, target_h)
    os.makedirs(output_dir, exist_ok=True)
    final.save(out_path, "PNG", optimize=True)

    elapsed = time.time() - t0
    print(f"  Saved {out_path} in {elapsed:.1f}s", file=sys.stderr)
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate hero images for jsonformat.io articles"
    )
    parser.add_argument(
        "--output",
        default="sites/jsonformat.io/public/images/blog",
        help="Output directory for blog hero images (default: sites/jsonformat.io/public/images/blog)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all 12 images (11 heroes + 1 OG default)",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test: generate only the OG default image",
    )
    parser.add_argument(
        "--slug",
        default=None,
        help="Generate a single image by slug",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing images",
    )

    args = parser.parse_args()
    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    if args.test:
        specs = [BLOG_IMAGES[0]]  # OG default
    elif args.slug:
        specs = [s for s in BLOG_IMAGES if s["slug"] == args.slug]
        if not specs:
            print(f"Unknown slug: {args.slug}", file=sys.stderr)
            sys.exit(1)
    elif args.all:
        specs = BLOG_IMAGES
    else:
        parser.print_help()
        sys.exit(0)

    print(f"Default output: {output_dir}")
    print(f"Images to generate: {len(specs)}")

    generated = []
    for spec in specs:
        path = generate_image(spec, output_dir, skip_existing=not args.force)
        generated.append(path)

    print(f"\nDone — {len(generated)} image(s)")


if __name__ == "__main__":
    main()
