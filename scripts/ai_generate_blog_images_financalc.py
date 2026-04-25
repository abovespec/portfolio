#!/usr/bin/env python3
"""
AI blog image generator for financalc.io YMYL-financial articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_financalc.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_financalc.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — 18 images for 6 financalc.io YMYL-financial articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG / header)
# size "body"  -> 800x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — APR vs. Interest Rate
    {
        "slug": "apr-vs-interest-rate-hero",
        "size": "hero",
        "prompt": (
            "Split-column infographic comparing APR versus interest rate, "
            "two labeled columns with percentage symbol icons and dollar signs, "
            "professional clean financial editorial design, "
            "neutral white background, no people, flat design"
        ),
    },
    {
        "slug": "apr-vs-interest-rate-1",
        "size": "body",
        "prompt": (
            "Close-up of a loan agreement document with annual percentage rate "
            "and interest rate line items visible, professional financial paperwork "
            "on a clean desk, editorial business photography"
        ),
    },
    {
        "slug": "apr-vs-interest-rate-2",
        "size": "body",
        "prompt": (
            "Financial advisor presenting mortgage documents across a desk, "
            "two professionals in a bank office setting, "
            "clean editorial business photography, professional tone"
        ),
    },
    # Article 2 — How Does Compound Interest Work?
    {
        "slug": "how-does-compound-interest-work-hero",
        "size": "hero",
        "prompt": (
            "Exponential growth curve chart showing compound interest versus simple interest, "
            "two lines diverging upward over time, clean financial data visualization, "
            "blue and green color scheme, white background, professional editorial"
        ),
    },
    {
        "slug": "how-does-compound-interest-work-1",
        "size": "body",
        "prompt": (
            "Stack of gold coins arranged in ascending columns from left to right "
            "illustrating geometric growth, financial concept photography, "
            "clean white background, professional studio lighting"
        ),
    },
    {
        "slug": "how-does-compound-interest-work-2",
        "size": "body",
        "prompt": (
            "Calendar page with clock and dollar sign illustrating time value of money, "
            "clean flat design financial illustration, "
            "blue and gold accent colors, white background"
        ),
    },
    # Article 3 — How Long to Pay Off Debt?
    {
        "slug": "how-long-to-pay-off-debt-hero",
        "size": "hero",
        "prompt": (
            "Horizontal timeline infographic showing debt payoff milestones month by month, "
            "shrinking debt bar with final zero balance, "
            "clean financial planning editorial design, blue and green palette, white background"
        ),
    },
    {
        "slug": "how-long-to-pay-off-debt-1",
        "size": "body",
        "prompt": (
            "Person cutting a credit card with scissors, debt-free concept, "
            "clean editorial lifestyle photography, neutral background, "
            "professional non-judgmental tone"
        ),
    },
    {
        "slug": "how-long-to-pay-off-debt-2",
        "size": "body",
        "prompt": (
            "Organized budget spreadsheet on laptop screen showing debt tracker "
            "with monthly payment columns, professional financial planning, "
            "clean home office setting, editorial photography"
        ),
    },
    # Article 4 — How Much House Can I Afford?
    {
        "slug": "how-much-house-can-i-afford-hero",
        "size": "hero",
        "prompt": (
            "Modern suburban house exterior with financial infographic callouts overlaid, "
            "monthly payment, down payment, debt-to-income ratio labels, "
            "clean real estate editorial design, white background, professional"
        ),
    },
    {
        "slug": "how-much-house-can-i-afford-1",
        "size": "body",
        "prompt": (
            "Young couple reviewing home affordability documents with a mortgage broker, "
            "professional office or bank setting, financial consultation, "
            "clean editorial business photography"
        ),
    },
    {
        "slug": "how-much-house-can-i-afford-2",
        "size": "body",
        "prompt": (
            "Miniature house model next to a calculator and mortgage application documents "
            "on a clean wooden desk, real estate finance concept, "
            "clean product photography style, warm editorial lighting"
        ),
    },
    # Article 5 — How to Save for Retirement
    {
        "slug": "how-to-save-for-retirement-hero",
        "size": "hero",
        "prompt": (
            "401k and IRA comparison infographic side by side, "
            "account type icons with annual contribution limit numbers, "
            "clean financial education chart, blue palette, white background, "
            "no people, professional flat design"
        ),
    },
    {
        "slug": "how-to-save-for-retirement-1",
        "size": "body",
        "prompt": (
            "Piggy bank beside an upward-trending investment portfolio chart, "
            "retirement savings concept illustration, "
            "clean financial editorial, green and blue accent colors, white background"
        ),
    },
    {
        "slug": "how-to-save-for-retirement-2",
        "size": "body",
        "prompt": (
            "Investment portfolio allocation pie chart showing stocks bonds cash diversification, "
            "professional financial data visualization, "
            "clean chart design, blue and green color scheme, white background"
        ),
    },
    # Article 6 — What Is ROI in Investing?
    {
        "slug": "what-is-roi-in-investing-hero",
        "size": "hero",
        "prompt": (
            "ROI formula prominently displayed on a clean white surface, "
            "net profit divided by cost of investment notation, "
            "financial education editorial, professional typography, "
            "minimal flat design, white background"
        ),
    },
    {
        "slug": "what-is-roi-in-investing-1",
        "size": "body",
        "prompt": (
            "Stock market candlestick chart trending upward on a laptop screen, "
            "investment portfolio monitoring, clean business photography, "
            "professional office environment, editorial style"
        ),
    },
    {
        "slug": "what-is-roi-in-investing-2",
        "size": "body",
        "prompt": (
            "Magnifying glass examining a bar chart with positive returns highlighted in green, "
            "investment analysis concept, clean white background, "
            "financial editorial illustration, professional design"
        ),
    },
]

SIZES = {
    "hero": (1200, 630),
    "body": (800, 500),
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
        description="Generate hero + body images for financalc.io YMYL articles"
    )
    parser.add_argument(
        "--output",
        default="sites/financalc.io/public/images/blog",
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
