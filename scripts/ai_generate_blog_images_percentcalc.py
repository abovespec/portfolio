#!/usr/bin/env python3
"""
AI blog image generator for percentcalc.io — math/percentage educational articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_percentcalc.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_percentcalc.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — 18 images for 6 percentcalc.io educational articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG / header)
# size "body"  -> 900x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — how-to-calculate-discount
    {
        "slug": "how-to-calculate-discount-hero",
        "size": "hero",
        "prompt": (
            "Bright red sale price tag with a bold percent-off badge hanging on a white background, "
            "clean product photography, vivid discount concept, "
            "modern retail aesthetic, soft drop shadow, no people"
        ),
    },
    {
        "slug": "how-to-calculate-discount-1",
        "size": "body",
        "prompt": (
            "Minimalist flat-design illustration of a shopping cart filled with items, "
            "large percent discount label floating above the cart, "
            "blue and orange color palette, white background, "
            "clean educational infographic style"
        ),
    },
    {
        "slug": "how-to-calculate-discount-2",
        "size": "body",
        "prompt": (
            "Side-by-side before and after price comparison graphic, "
            "original price crossed out in red and new discounted price highlighted in green, "
            "clean flat design infographic, neutral background, "
            "modern data visualization style, no people"
        ),
    },
    # Article 2 — how-to-calculate-percentage
    {
        "slug": "how-to-calculate-percentage-hero",
        "size": "hero",
        "prompt": (
            "Giant bold percent symbol in a modern sans-serif font surrounded by floating numbers and math symbols, "
            "clean abstract mathematics concept, deep blue and white color palette, "
            "professional editorial design, no people, minimal background"
        ),
    },
    {
        "slug": "how-to-calculate-percentage-1",
        "size": "body",
        "prompt": (
            "Clean colorful pie chart divided into percentage segments with labels, "
            "flat design data visualization infographic, "
            "blue green and orange slices on white background, "
            "professional educational illustration"
        ),
    },
    {
        "slug": "how-to-calculate-percentage-2",
        "size": "body",
        "prompt": (
            "Modern scientific calculator on a white desk beside a handwritten percentage formula on graph paper, "
            "clean overhead flat-lay photography, "
            "crisp editorial product shot, no people, math education concept"
        ),
    },
    # Article 3 — how-to-work-out-percentages-without-calculator
    {
        "slug": "how-to-work-out-percentages-without-calculator-hero",
        "size": "hero",
        "prompt": (
            "Illustrated human brain with glowing mathematical symbols and percentage signs floating around it, "
            "mental math concept, clean modern flat design illustration, "
            "purple and white color palette, no people, educational and approachable"
        ),
    },
    {
        "slug": "how-to-work-out-percentages-without-calculator-1",
        "size": "body",
        "prompt": (
            "Step-by-step percentage formula written in chalk on a green chalkboard, "
            "divide multiply percent symbols in neat handwriting, "
            "clean educational photography, warm chalk texture, "
            "no people, math learning concept"
        ),
    },
    {
        "slug": "how-to-work-out-percentages-without-calculator-2",
        "size": "body",
        "prompt": (
            "Flat design illustration showing a fraction converting to a decimal then to a percentage, "
            "step-by-step arrows connecting the values, "
            "clean blue and white infographic style, white background, "
            "educational math concept, no people"
        ),
    },
    # Article 4 — percentage-change-formula
    {
        "slug": "percentage-change-formula-hero",
        "size": "hero",
        "prompt": (
            "Bold upward and downward arrows side by side with large percentage change labels, "
            "increase and decrease concept illustration, "
            "green arrow up red arrow down, clean flat design, "
            "white background, modern data visualization, no people"
        ),
    },
    {
        "slug": "percentage-change-formula-1",
        "size": "body",
        "prompt": (
            "Clean line chart showing percentage change over time with data point labels, "
            "percentage annotations on the Y-axis, "
            "blue line on white grid background, "
            "professional flat design data visualization infographic"
        ),
    },
    {
        "slug": "percentage-change-formula-2",
        "size": "body",
        "prompt": (
            "Percentage change formula written clearly on a white marker board, "
            "new value minus old value divided by old value times 100, "
            "clean educational photography, marker pen handwriting, "
            "bright lighting, no people, math tutorial concept"
        ),
    },
    # Article 5 — percentage-difference-vs-change
    {
        "slug": "percentage-difference-vs-change-hero",
        "size": "hero",
        "prompt": (
            "Two tall vertical columns side by side, one labeled Difference and one labeled Change, "
            "contrast comparison layout, clean flat design infographic, "
            "blue and orange column colors on white background, "
            "modern educational illustration, no people"
        ),
    },
    {
        "slug": "percentage-difference-vs-change-1",
        "size": "body",
        "prompt": (
            "Side-by-side formula comparison layout, percentage difference formula on the left "
            "and percentage change formula on the right, "
            "clean divided infographic card design, "
            "blue and green typography on white background, math education"
        ),
    },
    {
        "slug": "percentage-difference-vs-change-2",
        "size": "body",
        "prompt": (
            "Venn diagram showing two overlapping circles labeled Percentage Difference and Percentage Change, "
            "shared and distinct properties labeled in each section, "
            "clean flat design illustration, blue and purple palette, white background, "
            "educational math concept"
        ),
    },
    # Article 6 — what-percentage-is-x-of-y
    {
        "slug": "what-percentage-is-x-of-y-hero",
        "size": "hero",
        "prompt": (
            "Abstract illustration of a large fraction X over Y transforming into a percent symbol, "
            "clean modern mathematical concept art, "
            "teal and white color palette, minimal background, "
            "professional editorial flat design, no people"
        ),
    },
    {
        "slug": "what-percentage-is-x-of-y-1",
        "size": "body",
        "prompt": (
            "Colorful pie chart with one highlighted slice labeled X out of Y total, "
            "percentage annotation on the slice, "
            "clean flat design data visualization, "
            "blue highlighted slice on grey background, white background, educational"
        ),
    },
    {
        "slug": "what-percentage-is-x-of-y-2",
        "size": "body",
        "prompt": (
            "Horizontal number line from 0 to 100 percent with a marker placed at a specific percentage point, "
            "clean flat design educational illustration, "
            "blue marker and tick marks on white background, "
            "math concept visualization, no people"
        ),
    },
]

SIZES = {
    "hero": (1200, 630),
    "body": (900, 500),
}

# ---------------------------------------------------------------------------
# Pipeline (lazy-loaded)
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


def generate_image(spec: dict, output_dir: str, skip_existing: bool = True) -> str:
    slug = spec["slug"]
    size_key = spec["size"]
    prompt = spec["prompt"]
    target_w, target_h = SIZES[size_key]

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
        description="Generate hero + body images for percentcalc.io math/percentage articles"
    )
    parser.add_argument(
        "--output",
        default="sites/percentcalc.io/public/images/blog",
        help="Output directory",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all 18 images",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test: generate only the first hero image",
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
        specs = [BLOG_IMAGES[0]]
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

    print(f"Output: {output_dir}")
    print(f"Images to generate: {len(specs)}")

    generated = []
    for spec in specs:
        path = generate_image(spec, output_dir, skip_existing=not args.force)
        generated.append(path)

    print(f"\nDone — {len(generated)} image(s) in {output_dir}")


if __name__ == "__main__":
    main()
