#!/usr/bin/env python3
"""
AI blog image generator for bmicalc.io YMYL health articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes
to target dimensions (no PBR maps, no seamless tiling).

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images.py \
        --site bmicalc.io --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images.py \
        --site bmicalc.io --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest: all 18 blog images for 6 BMI articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG image / header)
# size "body"  -> 800x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — What Is a Healthy BMI?
    {
        "slug": "what-is-a-healthy-bmi-hero",
        "size": "hero",
        "prompt": (
            "Clean infographic illustration of BMI weight categories horizontal scale, "
            "labeled sections for underweight normal weight overweight obese, "
            "green to red color gradient bar, clinical medical editorial style, "
            "white background, no people, high quality flat design"
        ),
    },
    {
        "slug": "what-is-a-healthy-bmi-1",
        "size": "body",
        "prompt": (
            "Adult person standing next to a medical height and weight measurement station, "
            "diverse neutral representation, clinical examination room, "
            "professional healthcare setting, editorial photography style"
        ),
    },
    {
        "slug": "what-is-a-healthy-bmi-2",
        "size": "body",
        "prompt": (
            "Abstract medical infographic showing BMI number surrounded by health icons, "
            "heart, blood pressure gauge, tape measure, weighing scale, "
            "clean minimal illustration, green accent colors, white background"
        ),
    },
    # Article 2 — How Is BMI Calculated?
    {
        "slug": "how-is-bmi-calculated-hero",
        "size": "hero",
        "prompt": (
            "Clean whiteboard with the BMI formula written clearly, "
            "weight divided by height squared, neat mathematical notation, "
            "educational medical illustration, chalkboard aesthetic, white background"
        ),
    },
    {
        "slug": "how-is-bmi-calculated-1",
        "size": "body",
        "prompt": (
            "Side by side comparison of metric and imperial weighing scales, "
            "kilograms on the left pounds on the right, clean product photography, "
            "white background, medical measurement equipment"
        ),
    },
    {
        "slug": "how-is-bmi-calculated-2",
        "size": "body",
        "prompt": (
            "Healthcare professional measuring patient height and weight at a medical clinic, "
            "friendly professional clinical setting, editorial health photography"
        ),
    },
    # Article 3 — BMI Chart for Women
    {
        "slug": "bmi-chart-for-women-hero",
        "size": "hero",
        "prompt": (
            "Stylized horizontal BMI range chart showing underweight normal overweight obese, "
            "teal sage green color palette, feminine editorial health illustration, "
            "no specific person shown, clean flat infographic design, white background"
        ),
    },
    {
        "slug": "bmi-chart-for-women-1",
        "size": "body",
        "prompt": (
            "Woman measuring her waist with a tape measure, "
            "clinical wellness context, non-stigmatizing professional health photography, "
            "neutral background, editorial health style"
        ),
    },
    {
        "slug": "bmi-chart-for-women-2",
        "size": "body",
        "prompt": (
            "Medical illustration of body composition changes across age progression, "
            "simplified diagram from age 25 to age 65, "
            "clinical educational infographic, clean style, white background"
        ),
    },
    # Article 4 — Limitations of BMI
    {
        "slug": "limitations-of-bmi-hero",
        "size": "hero",
        "prompt": (
            "Medical infographic split illustration showing athletic muscular person "
            "and sedentary person side by side, both labeled with the same BMI number, "
            "illustrating muscle versus fat difference, clean clinical educational style"
        ),
    },
    {
        "slug": "limitations-of-bmi-1",
        "size": "body",
        "prompt": (
            "Medical anatomical body silhouette illustration, visceral fat highlighted "
            "in orange around the midsection versus subcutaneous fat in blue, "
            "clinical educational anatomy diagram, white background"
        ),
    },
    {
        "slug": "limitations-of-bmi-2",
        "size": "body",
        "prompt": (
            "Flexible tape measure wrapped around a person's waist, "
            "waist circumference health measurement, clean medical photography, "
            "neutral clinical style, close-up detail"
        ),
    },
    # Article 5 — BMI for Children and Teens
    {
        "slug": "bmi-for-children-and-teens-hero",
        "size": "hero",
        "prompt": (
            "CDC-style BMI percentile growth chart for children, "
            "simplified chart with multiple percentile curves, "
            "dot plotted on the healthy range, clinical educational health graph, "
            "clean infographic style, white background"
        ),
    },
    {
        "slug": "bmi-for-children-and-teens-1",
        "size": "body",
        "prompt": (
            "Friendly pediatrician measuring a child's height at a well-child visit, "
            "medical clinic setting, caring professional healthcare environment, "
            "editorial photography"
        ),
    },
    {
        "slug": "bmi-for-children-and-teens-2",
        "size": "body",
        "prompt": (
            "Three children of different ages standing side by side, "
            "approximately 5 years, 10 years, and 15 years old, "
            "showing natural body development variation, diverse neutral illustration, "
            "educational medical style"
        ),
    },
    # Article 6 — High BMI Health Risks
    {
        "slug": "high-bmi-health-risks-hero",
        "size": "hero",
        "prompt": (
            "Medical illustration of human body organs affected by high BMI, "
            "heart liver pancreas knee joints with subtle warm risk highlights, "
            "clinical educational anatomy diagram, informational not alarmist, "
            "clean editorial style, white background"
        ),
    },
    {
        "slug": "high-bmi-health-risks-1",
        "size": "body",
        "prompt": (
            "Blood pressure cuff on a person's arm, cardiovascular health monitoring, "
            "medical equipment, clean clinical photography, healthcare setting"
        ),
    },
    {
        "slug": "high-bmi-health-risks-2",
        "size": "body",
        "prompt": (
            "Colorful plate of fresh vegetables with a stethoscope beside it, "
            "healthy lifestyle and prevention concept, medical editorial photography, "
            "clean light background"
        ),
    },
]

SIZES = {
    "hero": (1200, 630),
    "body": (800, 500),
}

# ---------------------------------------------------------------------------
# Pipeline (lazy-loaded, identical strategy to ai_generate_textures.py)
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
    """Center-crop a square image to the given aspect ratio, then resize."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # src is wider — crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        # src is taller — crop top/bottom
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
        description="Generate hero + body images for BMI blog articles"
    )
    parser.add_argument(
        "--site",
        default="bmicalc.io",
        help="Site name (default: bmicalc.io)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output directory (default: sites/<site>/public/images/blog/)",
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
        help="Generate a single image by slug (e.g. what-is-a-healthy-bmi-hero)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing images",
    )

    args = parser.parse_args()

    output_dir = args.output or os.path.join(
        "sites", args.site, "public", "images", "blog"
    )
    output_dir = os.path.abspath(output_dir)
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
