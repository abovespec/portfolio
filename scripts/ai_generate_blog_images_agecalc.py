#!/usr/bin/env python3
"""
AI blog image generator for agecalc.io lifestyle/birthday/time articles.
Uses ERNIE-Image-Turbo. Generates at 1024x1024, then center-crops + resizes.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_agecalc.py --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_agecalc.py --all
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

# ---------------------------------------------------------------------------
# Image manifest — 18 images for 6 agecalc.io articles
# ---------------------------------------------------------------------------
# size "hero"  -> 1200x630  (OG / header)
# size "body"  -> 900x500   (inline article image)
BLOG_IMAGES = [
    # Article 1 — How to Calculate Age in Years, Months, and Days
    {
        "slug": "age-in-years-months-days-hero",
        "size": "hero",
        "prompt": (
            "Clean flat design calendar illustration showing age milestone markers, "
            "years months days labels with colorful section dividers, "
            "warm orange and teal color scheme, white background, "
            "friendly lifestyle editorial style, no people"
        ),
    },
    {
        "slug": "age-in-years-months-days-1",
        "size": "body",
        "prompt": (
            "Horizontal timeline infographic showing progression from years to months to days, "
            "colorful segmented bar with labeled time units, "
            "warm pastel tones, clean flat design, white background"
        ),
    },
    {
        "slug": "age-in-years-months-days-2",
        "size": "body",
        "prompt": (
            "Analog clock face overlapping with a wall calendar, "
            "warm golden hour lighting, soft focus lifestyle photography, "
            "friendly approachable aesthetic, warm tones"
        ),
    },
    # Article 2 — How Many Days Have I Been Alive?
    {
        "slug": "how-many-days-have-i-been-alive-hero",
        "size": "hero",
        "prompt": (
            "Large bold number like 10000 displayed as a milestone celebration graphic, "
            "confetti and sparkles surrounding the number, "
            "warm festive colors orange yellow gold, clean editorial illustration, "
            "white background, celebratory joyful mood"
        ),
    },
    {
        "slug": "how-many-days-have-i-been-alive-1",
        "size": "body",
        "prompt": (
            "Person raising arms in celebration outdoors at a milestone birthday party, "
            "bright sunny day, warm lifestyle photography, "
            "joyful moment, editorial stock photography style"
        ),
    },
    {
        "slug": "how-many-days-have-i-been-alive-2",
        "size": "body",
        "prompt": (
            "Stack of calendar pages fanning out illustrating days passing, "
            "warm golden tones, flat lay photography on wooden surface, "
            "lifestyle editorial aesthetic"
        ),
    },
    # Article 3 — How Many Days Until My Birthday?
    {
        "slug": "how-many-days-until-my-birthday-hero",
        "size": "hero",
        "prompt": (
            "Countdown calendar with red circle around a birthday date, "
            "days remaining number displayed prominently, "
            "warm festive illustration, orange pink and gold color palette, "
            "flat design, white background, celebratory mood"
        ),
    },
    {
        "slug": "how-many-days-until-my-birthday-1",
        "size": "body",
        "prompt": (
            "Colorful birthday cake with lit candles on a white background, "
            "warm studio photography, festive celebration atmosphere, "
            "pastel frosting, cheerful lifestyle imagery"
        ),
    },
    {
        "slug": "how-many-days-until-my-birthday-2",
        "size": "body",
        "prompt": (
            "Wrapped gift boxes with colorful ribbons and bows, "
            "warm flat lay on white background, birthday celebration lifestyle photography, "
            "pastel pink and gold accents, cheerful editorial style"
        ),
    },
    # Article 4 — How Old Am I If I Was Born in [Year]?
    {
        "slug": "how-old-am-i-born-in-year-hero",
        "size": "hero",
        "prompt": (
            "Vintage calendar with a bold year stamp mark, retro aesthetic, "
            "warm sepia and gold tones, editorial illustration style, "
            "aged paper texture, nostalgic birthday year graphic"
        ),
    },
    {
        "slug": "how-old-am-i-born-in-year-1",
        "size": "body",
        "prompt": (
            "Old newspaper front page showing a birth year date in the masthead, "
            "vintage black and white editorial aesthetic, "
            "clean detail shot, nostalgic historical style"
        ),
    },
    {
        "slug": "how-old-am-i-born-in-year-2",
        "size": "body",
        "prompt": (
            "Bold age number typography like 30 or 40 as milestone celebration graphic, "
            "warm gold and cream color scheme, festive editorial design, "
            "white background, clean modern type"
        ),
    },
    # Article 5 — How to Calculate Your Exact Age from Date of Birth
    {
        "slug": "how-to-calculate-age-from-date-of-birth-hero",
        "size": "hero",
        "prompt": (
            "Calculator device with a birthdate typed on the display screen, "
            "clean product photography on white background, "
            "warm neutral tones, professional editorial style"
        ),
    },
    {
        "slug": "how-to-calculate-age-from-date-of-birth-1",
        "size": "body",
        "prompt": (
            "Abstract birth certificate document illustration with name and date of birth fields, "
            "clean flat design, soft blue and white color scheme, "
            "no personal information, editorial illustration style"
        ),
    },
    {
        "slug": "how-to-calculate-age-from-date-of-birth-2",
        "size": "body",
        "prompt": (
            "Calendar page with mathematical symbols plus minus and equals signs, "
            "calculation concept illustration, warm cream and orange palette, "
            "flat design, white background, friendly educational aesthetic"
        ),
    },
    # Article 6 — What Is Chronological Age?
    {
        "slug": "what-is-chronological-age-hero",
        "size": "hero",
        "prompt": (
            "Horizontal timeline of human life stages from birth to senior years, "
            "clean illustrated icons at each milestone, "
            "warm pastel color gradient, flat design editorial style, white background"
        ),
    },
    {
        "slug": "what-is-chronological-age-1",
        "size": "body",
        "prompt": (
            "Silhouette progression from baby toddler child teen adult to elder, "
            "side profile outlines in warm toned gradient, "
            "clean flat design illustration, white background, life stages concept"
        ),
    },
    {
        "slug": "what-is-chronological-age-2",
        "size": "body",
        "prompt": (
            "Light clean medical chart or growth record form with age entries, "
            "clinical but friendly aesthetic, soft blue and white, "
            "editorial illustration, no personal data visible"
        ),
    },
]

SIZES = {
    "hero": (1200, 630),
    "body": (900, 500),
}

# ---------------------------------------------------------------------------
# Pipeline (lazy-loaded, identical to ai_generate_blog_images_financalc.py)
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
        description="Generate hero + body images for agecalc.io articles"
    )
    parser.add_argument(
        "--output",
        default="sites/agecalc.io/public/images/blog",
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
