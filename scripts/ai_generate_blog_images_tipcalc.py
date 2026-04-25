#!/usr/bin/env python3
"""
AI blog image generator for tipcalc.io — restaurant/dining YMYL-financial-light articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_tipcalc.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_tipcalc.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — 18 images for 6 tipcalc.io YMYL-financial-light articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG / header)
# size "body"  -> 900x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — average-tip-percentage
    {
        "slug": "average-tip-percentage-hero",
        "size": "hero",
        "prompt": (
            "Close-up of a restaurant check paper bill on a white tablecloth, "
            "tip line visible at the bottom with pen resting beside it, "
            "warm soft lighting, shallow depth of field, "
            "clean editorial food photography, professional and approachable"
        ),
    },
    {
        "slug": "average-tip-percentage-1",
        "size": "body",
        "prompt": (
            "Clean bar chart infographic showing tipping percentage ranges from 10 to 25 percent, "
            "restaurant service context, professional flat design data visualization, "
            "warm orange and cream color palette, white background"
        ),
    },
    {
        "slug": "average-tip-percentage-2",
        "size": "body",
        "prompt": (
            "Scattered coins and folded dollar bills lying next to a restaurant receipt on a wooden table, "
            "warm ambient light, editorial lifestyle photography, "
            "clean composition, no people, approachable dining atmosphere"
        ),
    },
    # Article 2 — how-much-to-tip-a-server
    {
        "slug": "how-much-to-tip-a-server-hero",
        "size": "hero",
        "prompt": (
            "Friendly server in a white apron carrying multiple plates through a bright restaurant dining room, "
            "warm interior lighting, bokeh background of other diners, "
            "professional editorial food-service photography, positive welcoming tone"
        ),
    },
    {
        "slug": "how-much-to-tip-a-server-1",
        "size": "body",
        "prompt": (
            "Restaurant server smiling and receiving cash tip from a satisfied diner, "
            "warm restaurant interior, candid editorial photography, "
            "tip jar on counter visible in background, approachable positive tone"
        ),
    },
    {
        "slug": "how-much-to-tip-a-server-2",
        "size": "body",
        "prompt": (
            "Overhead flat-lay of a beautifully set restaurant dining table, "
            "white tablecloth, wine glasses, bread basket, silverware arranged neatly, "
            "warm editorial food photography, no people, inviting atmosphere"
        ),
    },
    # Article 3 — how-to-calculate-a-tip
    {
        "slug": "how-to-calculate-a-tip-hero",
        "size": "hero",
        "prompt": (
            "Smartphone lying on a restaurant dinner table displaying a tip calculator app, "
            "wine glass and dinner plate blurred in background, "
            "warm ambient restaurant lighting, editorial lifestyle photography, "
            "clean and modern composition"
        ),
    },
    {
        "slug": "how-to-calculate-a-tip-1",
        "size": "body",
        "prompt": (
            "Handwritten tip calculation on a paper napkin showing percentage math, "
            "15 percent and 20 percent annotations, restaurant table setting in background, "
            "warm editorial photography, approachable financial concept"
        ),
    },
    {
        "slug": "how-to-calculate-a-tip-2",
        "size": "body",
        "prompt": (
            "Credit card lying beside a folded restaurant check on a clean leather bill presenter, "
            "warm soft directional lighting, editorial close-up photography, "
            "clean composition, no people, professional dining atmosphere"
        ),
    },
    # Article 4 — how-to-split-a-bill-with-tip
    {
        "slug": "how-to-split-a-bill-with-tip-hero",
        "size": "hero",
        "prompt": (
            "Group of four friends laughing and dining together at a restaurant table, "
            "food and drinks on the table, warm interior lighting, "
            "candid editorial lifestyle photography, positive social dining atmosphere"
        ),
    },
    {
        "slug": "how-to-split-a-bill-with-tip-1",
        "size": "body",
        "prompt": (
            "Restaurant bill torn into equal sections lying on a table, "
            "bill-splitting concept illustration, clean editorial photography, "
            "warm wood table surface, no people, financial fairness concept"
        ),
    },
    {
        "slug": "how-to-split-a-bill-with-tip-2",
        "size": "body",
        "prompt": (
            "Several people at a restaurant table each placing a credit card on a bill tray, "
            "group payment moment, candid editorial photography, "
            "warm restaurant lighting, positive and friendly tone"
        ),
    },
    # Article 5 — tipping-by-country
    {
        "slug": "tipping-by-country-hero",
        "size": "hero",
        "prompt": (
            "Illustrated world map with currency symbols and tipping icons overlaid on different countries, "
            "euros dollars yen pounds scattered across regions, "
            "clean flat design infographic, warm color palette, white background, "
            "professional editorial design, no people"
        ),
    },
    {
        "slug": "tipping-by-country-1",
        "size": "body",
        "prompt": (
            "Flat-lay of international banknotes and coins from multiple countries arranged neatly, "
            "small country flags visible, clean editorial product photography, "
            "white background, global money travel concept"
        ),
    },
    {
        "slug": "tipping-by-country-2",
        "size": "body",
        "prompt": (
            "Collage of international money — euro coins, US dollar bills, British pounds, Japanese yen, "
            "clean editorial flat-lay photography on neutral background, "
            "travel and global tipping concept, no people"
        ),
    },
    # Article 6 — tipping-etiquette-united-states
    {
        "slug": "tipping-etiquette-united-states-hero",
        "size": "hero",
        "prompt": (
            "Classic American diner interior with red booth seating, chrome stools, "
            "and a checkered floor, retro Americana aesthetic, "
            "warm nostalgic editorial photography, no people, inviting atmosphere"
        ),
    },
    {
        "slug": "tipping-etiquette-united-states-1",
        "size": "body",
        "prompt": (
            "Tip envelope with cash dollars placed on a restaurant table beside a coffee cup, "
            "white tablecloth, warm soft light, editorial close-up photography, "
            "clean American dining etiquette concept, no people"
        ),
    },
    {
        "slug": "tipping-etiquette-united-states-2",
        "size": "body",
        "prompt": (
            "Smiling restaurant server in uniform standing in a bright American casual dining room, "
            "welcoming expression, warm interior lighting, "
            "editorial food-service photography, positive professional tone"
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
        description="Generate hero + body images for tipcalc.io restaurant/dining articles"
    )
    parser.add_argument(
        "--output",
        default="sites/tipcalc.io/public/images/blog",
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
