#!/usr/bin/env python3
"""
AI blog image generator for margincalc.io — YMYL-financial margin/profit articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_margincalc.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_margincalc.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — 18 images for 6 margincalc.io YMYL-financial articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG / header)
# size "body"  -> 900x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — gross-margin-vs-net-margin
    {
        "slug": "gross-margin-vs-net-margin-hero",
        "size": "hero",
        "prompt": (
            "Split bar chart comparing gross margin versus net profit margin percentages, "
            "clean corporate infographic design, navy blue and teal color palette, "
            "white background, professional business data visualization, "
            "labeled axes and legend, no people"
        ),
    },
    {
        "slug": "gross-margin-vs-net-margin-1",
        "size": "body",
        "prompt": (
            "Waterfall chart showing revenue at top flowing down through cost of goods sold "
            "and operating expenses to net profit at bottom, "
            "professional financial waterfall diagram, dark blue green and red bars, "
            "clean flat design infographic, white background, no people"
        ),
    },
    {
        "slug": "gross-margin-vs-net-margin-2",
        "size": "body",
        "prompt": (
            "Income statement document graphic with clean rows showing revenue gross profit "
            "operating income and net income, professional financial report layout, "
            "white paper corporate style, dark navy text on white, business finance report, no people"
        ),
    },
    # Article 2 — how-to-calculate-gross-profit-margin
    {
        "slug": "how-to-calculate-gross-profit-margin-hero",
        "size": "hero",
        "prompt": (
            "Profit margin formula written in clean chalk on a dark corporate whiteboard, "
            "Revenue minus COGS divided by Revenue equals Gross Margin, "
            "professional business education concept, clean and modern, no people"
        ),
    },
    {
        "slug": "how-to-calculate-gross-profit-margin-1",
        "size": "body",
        "prompt": (
            "Stacked bar chart infographic showing total revenue bar with cost of goods sold "
            "subtracted leaving gross profit highlighted in green, "
            "clean flat design data visualization, navy and teal on white background, "
            "professional financial infographic, no people"
        ),
    },
    {
        "slug": "how-to-calculate-gross-profit-margin-2",
        "size": "body",
        "prompt": (
            "Horizontal bar chart comparing gross profit margin percentages across different "
            "industries or product lines, clean professional business infographic, "
            "navy blue and teal color palette, white background, labeled percentage values, no people"
        ),
    },
    # Article 3 — how-to-improve-profit-margins
    {
        "slug": "how-to-improve-profit-margins-hero",
        "size": "hero",
        "prompt": (
            "Upward trending line graph showing profit margin percentage improving over time, "
            "bold green upward arrow overlay, clean corporate analytics dashboard chart, "
            "dark navy and emerald green color scheme, white background, "
            "professional business growth visualization, no people"
        ),
    },
    {
        "slug": "how-to-improve-profit-margins-1",
        "size": "body",
        "prompt": (
            "Business levers diagram showing four operational levers to improve margins: "
            "reduce costs, increase prices, improve efficiency, cut overheads, "
            "clean flat design infographic with icons, professional corporate style, "
            "navy blue accent colors on white background, no people"
        ),
    },
    {
        "slug": "how-to-improve-profit-margins-2",
        "size": "body",
        "prompt": (
            "Business professionals in suits reviewing profit margin charts and graphs "
            "on a laptop in a bright modern corporate meeting room, "
            "financial analysis session, professional editorial photography, "
            "clean office environment, focused and strategic atmosphere"
        ),
    },
    # Article 4 — markup-vs-margin
    {
        "slug": "markup-vs-margin-hero",
        "size": "hero",
        "prompt": (
            "Side-by-side comparison infographic showing markup formula on the left "
            "and margin formula on the right, clean split-panel design, "
            "professional flat business graphic, navy and teal color palette, "
            "white background, clear labels and percentage examples, no people"
        ),
    },
    {
        "slug": "markup-vs-margin-1",
        "size": "body",
        "prompt": (
            "Price build-up diagram showing cost at bottom plus markup equals selling price at top, "
            "stacked block infographic, markup equals cost plus profit percentage annotation, "
            "clean professional flat design, navy and orange color scheme, "
            "white background, business pricing concept, no people"
        ),
    },
    {
        "slug": "markup-vs-margin-2",
        "size": "body",
        "prompt": (
            "Revenue pie chart split into cost portion and margin profit portion, "
            "margin equals profit divided by revenue fraction diagram, "
            "clean professional infographic design, teal and navy color palette, "
            "white background, business finance education, no people"
        ),
    },
    # Article 5 — what-is-a-good-profit-margin
    {
        "slug": "what-is-a-good-profit-margin-hero",
        "size": "hero",
        "prompt": (
            "Industry benchmark bar chart showing average profit margin percentages "
            "for software retail food service manufacturing and consulting industries, "
            "clean corporate data visualization, navy and teal bars on white background, "
            "professional financial infographic, labeled axes, no people"
        ),
    },
    {
        "slug": "what-is-a-good-profit-margin-1",
        "size": "body",
        "prompt": (
            "Side-by-side grouped bar chart comparing profit margins of small business "
            "versus enterprise companies across multiple industry sectors, "
            "clean professional business infographic, navy blue and teal color palette, "
            "white background, data-driven financial comparison, no people"
        ),
    },
    {
        "slug": "what-is-a-good-profit-margin-2",
        "size": "body",
        "prompt": (
            "Profit margin gauge meter dashboard widget showing zones from red warning "
            "to yellow caution to green healthy profit territory, "
            "clean corporate dashboard design, professional financial KPI indicator, "
            "dark navy background with colored gauge arc, no people"
        ),
    },
    # Article 6 — what-is-profit-margin
    {
        "slug": "what-is-profit-margin-hero",
        "size": "hero",
        "prompt": (
            "Clean minimalist definition card design with Profit Margin as bold headline, "
            "professional typographic corporate card on white background, "
            "subtle navy blue border and accent, clean sans-serif typography, "
            "financial education visual, no people"
        ),
    },
    {
        "slug": "what-is-profit-margin-1",
        "size": "body",
        "prompt": (
            "P&L profit and loss summary chart showing total revenue operating costs "
            "gross profit and net income rows, clean professional financial report layout, "
            "white paper corporate document style, dark navy text, "
            "business finance overview graphic, no people"
        ),
    },
    {
        "slug": "what-is-profit-margin-2",
        "size": "body",
        "prompt": (
            "Money flow diagram with green arrows showing cash flowing into a business "
            "and red arrows showing expenses flowing out, net profit highlighted at bottom, "
            "clean flat design infographic, professional corporate cash flow visual, "
            "white background, navy and green color palette, no people"
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
        description="Generate hero + body images for margincalc.io financial articles"
    )
    parser.add_argument(
        "--output",
        default="sites/margincalc.io/public/images/blog",
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
