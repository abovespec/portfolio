#!/usr/bin/env python3
"""
AI blog image generator — Phase-2 calculator sites.
Covers: agecalc.io, tipcalc.io, amortcalc.io, margincalc.io, percentcalc.io
5 site OG heroes + 30 article heroes = 35 images total.

Uses ERNIE-Image-Turbo. Generates at 1024x1024, center-crops to target size.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_phase2.py --site agecalc.io --all
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_phase2.py --all-sites
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_phase2.py --site tipcalc.io --test
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

SIZES = {
    "hero": (1200, 630),
}

# ---------------------------------------------------------------------------
# Per-site manifests
# ---------------------------------------------------------------------------
# Each entry: slug (filename without .png), size, prompt, optional output_dir_override
# OG site heroes use output_dir_override pointing to sites/{site}/public/

SITE_MANIFESTS = {
    # -----------------------------------------------------------------------
    "agecalc.io": [
        # Site OG hero
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/agecalc.io/public",
            "prompt": (
                "Elegant abstract timeline stretching from childhood to adulthood, "
                "milestone markers as glowing dots on a warm golden gradient ribbon, "
                "clean minimal illustration, birthday and life stages concept, "
                "warm amber tones, white background, non-kitschy editorial design"
            ),
        },
        # Article 1 — age-in-years-months-days
        {
            "slug": "age-in-years-months-days-hero",
            "size": "hero",
            "prompt": (
                "Abstract calendar with layered rings or nested segments representing "
                "years months and days units, clean time visualization infographic, "
                "warm golden tones, white background, minimal editorial design"
            ),
        },
        # Article 2 — how-many-days-have-i-been-alive
        {
            "slug": "how-many-days-have-i-been-alive-hero",
            "size": "hero",
            "prompt": (
                "Endless calendar grid fading into the distance representing thousands of life days, "
                "subtle warm amber gradient, conceptual editorial illustration, "
                "life-days visualization, clean minimal design, white background"
            ),
        },
        # Article 3 — how-many-days-until-my-birthday
        {
            "slug": "how-many-days-until-my-birthday-hero",
            "size": "hero",
            "prompt": (
                "Circular countdown calendar with a single birthday date highlighted "
                "and remaining countdown days shown around the ring, "
                "warm celebratory tones, clean birthday concept illustration, minimal design"
            ),
        },
        # Article 4 — how-old-am-i-born-in-year
        {
            "slug": "how-old-am-i-born-in-year-hero",
            "size": "hero",
            "prompt": (
                "Decade progression visualization transitioning from vintage sepia tones on the left "
                "to modern clean design on the right, horizontal timeline editorial, "
                "warm golden gradient, white background, age concept illustration"
            ),
        },
        # Article 5 — how-to-calculate-age-from-date-of-birth
        {
            "slug": "how-to-calculate-age-from-date-of-birth-hero",
            "size": "hero",
            "prompt": (
                "Clean mathematical formula showing current date minus birth date equals age, "
                "simple age calculation on a minimal white card, "
                "educational illustration style, warm accent colors, white background"
            ),
        },
        # Article 6 — what-is-chronological-age
        {
            "slug": "what-is-chronological-age-hero",
            "size": "hero",
            "prompt": (
                "Stacked clock faces or layered concentric time rings representing chronological time layers, "
                "abstract time concept illustration, warm amber tones, "
                "clean editorial design, white background, minimal style"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "tipcalc.io": [
        # Site OG hero
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/tipcalc.io/public",
            "prompt": (
                "Modern restaurant table close-up with a dining receipt and a few coins placed beside it, "
                "warm ambient restaurant lighting, clean editorial food photography aesthetic, "
                "tip concept, white tablecloth, no people"
            ),
        },
        # Article 1 — average-tip-percentage
        {
            "slug": "average-tip-percentage-hero",
            "size": "hero",
            "prompt": (
                "Clean radial percentage dial showing tip ranges from 10 to 25 percent, "
                "warm neutral tones, clean infographic design, "
                "pointer indicating typical 18 percent range, white background"
            ),
        },
        # Article 2 — how-much-to-tip-a-server
        {
            "slug": "how-much-to-tip-a-server-hero",
            "size": "hero",
            "prompt": (
                "Friendly restaurant server presenting a check holder at a dining table, "
                "warm professional editorial photography, tasteful service scene, "
                "restaurant setting, welcoming ambiance"
            ),
        },
        # Article 3 — how-to-calculate-a-tip
        {
            "slug": "how-to-calculate-a-tip-hero",
            "size": "hero",
            "prompt": (
                "Restaurant paper bill laid next to a smartphone showing a tip calculator interface, "
                "clean table surface, warm editorial photography, "
                "practical tip calculation concept, modern dining aesthetic"
            ),
        },
        # Article 4 — how-to-split-a-bill-with-tip
        {
            "slug": "how-to-split-a-bill-with-tip-hero",
            "size": "hero",
            "prompt": (
                "Restaurant dining table scene with multiple payment cards spread beside a shared bill, "
                "splitting concept, warm social dining editorial photography, "
                "group dining ambiance, clean overhead or angled shot"
            ),
        },
        # Article 5 — tipping-by-country
        {
            "slug": "tipping-by-country-hero",
            "size": "hero",
            "prompt": (
                "Minimalist world map infographic with selected countries highlighted and small "
                "percentage tip labels beside them, clean editorial travel infographic, "
                "warm neutral tones, white background, globe tipping concept"
            ),
        },
        # Article 6 — tipping-etiquette-united-states
        {
            "slug": "tipping-etiquette-united-states-hero",
            "size": "hero",
            "prompt": (
                "Classic American diner scene, tip bills left on table beside a check, "
                "warm nostalgic editorial photography, American restaurant aesthetic, "
                "coffee cup and receipt in frame, no faces"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "amortcalc.io": [
        # Site OG hero
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/amortcalc.io/public",
            "prompt": (
                "Silver house keys resting on a stack of mortgage loan documents on a clean desk, "
                "professional real estate financial editorial, blue-grey tones, "
                "clean product photography, no people, trustworthy mortgage concept"
            ),
        },
        # Article 1 — 15-year-vs-30-year-mortgage
        {
            "slug": "15-year-vs-30-year-mortgage-hero",
            "size": "hero",
            "prompt": (
                "Two-path fork infographic showing 15-year mortgage on the left and 30-year on the right, "
                "each path labeled with payment and interest comparisons, "
                "clean financial comparison editorial, blue-grey palette, white background"
            ),
        },
        # Article 2 — amortization-schedule-explained
        {
            "slug": "amortization-schedule-explained-hero",
            "size": "hero",
            "prompt": (
                "Close-up of a clean amortization schedule table with columns "
                "for month payment interest principal and remaining balance, "
                "rows highlighted in alternating blue-grey, professional financial document editorial"
            ),
        },
        # Article 3 — extra-mortgage-payments
        {
            "slug": "extra-mortgage-payments-hero",
            "size": "hero",
            "prompt": (
                "Stack of coins being placed on top of a mortgage payment ledger or loan statement, "
                "extra payment debt reduction concept, clean financial editorial, "
                "professional blue-grey tones, white background"
            ),
        },
        # Article 4 — how-amortization-works
        {
            "slug": "how-amortization-works-hero",
            "size": "hero",
            "prompt": (
                "Area chart showing principal versus interest portions of mortgage payments over time, "
                "interest-heavy early years transitioning to principal-heavy later years, "
                "blue and grey color areas, clean financial data visualization, white background"
            ),
        },
        # Article 5 — interest-vs-principal
        {
            "slug": "interest-vs-principal-hero",
            "size": "hero",
            "prompt": (
                "Horizontal split bar diagram or pie chart showing interest portion versus principal portion "
                "of a typical mortgage payment, clearly labeled, "
                "clean financial infographic, blue and grey palette, white background"
            ),
        },
        # Article 6 — what-is-amortization
        {
            "slug": "what-is-amortization-hero",
            "size": "hero",
            "prompt": (
                "Professional financial definition card or document with amortization concept illustrated, "
                "declining balance bar chart beside clean text, "
                "blue-grey professional tones, desk editorial, clean design"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "margincalc.io": [
        # Site OG hero
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/margincalc.io/public",
            "prompt": (
                "Business bar chart with upward trending profit margin bars, "
                "green and teal accent colors on clean white background, "
                "professional financial editorial design, no people, clean data visualization"
            ),
        },
        # Article 1 — gross-margin-vs-net-margin
        {
            "slug": "gross-margin-vs-net-margin-hero",
            "size": "hero",
            "prompt": (
                "Two-column comparison infographic showing gross margin on the left and net margin on the right, "
                "P&L statement style layout, clean business editorial design, "
                "green and teal palette, white background"
            ),
        },
        # Article 2 — how-to-calculate-gross-profit-margin
        {
            "slug": "how-to-calculate-gross-profit-margin-hero",
            "size": "hero",
            "prompt": (
                "Gross profit margin formula displayed cleanly on a white card, "
                "revenue minus cost of goods sold divided by revenue equals gross margin percentage, "
                "clean financial education editorial, green accent, white background"
            ),
        },
        # Article 3 — how-to-improve-profit-margins
        {
            "slug": "how-to-improve-profit-margins-hero",
            "size": "hero",
            "prompt": (
                "Upward growth arrow overlaying a bar chart with improving margin percentages over time, "
                "business growth concept, clean green and teal editorial design, "
                "professional financial illustration, white background"
            ),
        },
        # Article 4 — markup-vs-margin
        {
            "slug": "markup-vs-margin-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side labeled comparison cards — markup percentage on the left versus "
                "margin percentage on the right with their formulas shown, "
                "clean business infographic, teal and green palette, white background"
            ),
        },
        # Article 5 — what-is-a-good-profit-margin
        {
            "slug": "what-is-a-good-profit-margin-hero",
            "size": "hero",
            "prompt": (
                "Industry benchmark horizontal bar chart showing different business sectors "
                "and their typical profit margin percentage ranges, "
                "green accent bars on white background, clean financial data visualization"
            ),
        },
        # Article 6 — what-is-profit-margin
        {
            "slug": "what-is-profit-margin-hero",
            "size": "hero",
            "prompt": (
                "Percentage symbol with surrounding profit and revenue icons, "
                "clean minimal profit margin concept illustration, "
                "green accent tones, professional business editorial, white background"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "percentcalc.io": [
        # Site OG hero
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/percentcalc.io/public",
            "prompt": (
                "Large percent symbol rendered in modern minimal design, "
                "surrounded by floating numbers and decimal points, "
                "clean blue accent on white background, math utility editorial, no people"
            ),
        },
        # Article 1 — how-to-calculate-discount
        {
            "slug": "how-to-calculate-discount-hero",
            "size": "hero",
            "prompt": (
                "Retail price tag with a bold discount badge showing a percentage off label, "
                "clean minimal product photography concept, "
                "sale editorial illustration, blue and red accents, white background"
            ),
        },
        # Article 2 — how-to-calculate-percentage
        {
            "slug": "how-to-calculate-percentage-hero",
            "size": "hero",
            "prompt": (
                "Percentage formula displayed cleanly — part divided by whole times 100, "
                "educational card design, textbook editorial feel, "
                "blue accent on white background, clean math illustration"
            ),
        },
        # Article 3 — how-to-work-out-percentages-without-calculator
        {
            "slug": "how-to-work-out-percentages-without-calculator-hero",
            "size": "hero",
            "prompt": (
                "Open notebook with mental math percentage shortcuts written by hand, "
                "pencil resting beside it on a clean study desk, "
                "educational concept editorial, warm paper tones, blue ink accents"
            ),
        },
        # Article 4 — percentage-change-formula
        {
            "slug": "percentage-change-formula-hero",
            "size": "hero",
            "prompt": (
                "Before and after arrow diagram showing percentage change formula, "
                "new value minus old value divided by old value times 100, "
                "clean infographic card design, blue accent, white background, educational editorial"
            ),
        },
        # Article 5 — percentage-difference-vs-change
        {
            "slug": "percentage-difference-vs-change-hero",
            "size": "hero",
            "prompt": (
                "Two-bar comparison diagram side by side labeled percentage difference "
                "versus percentage change, clearly annotated differences, "
                "clean educational infographic, blue and grey palette, white background"
            ),
        },
        # Article 6 — what-percentage-is-x-of-y
        {
            "slug": "what-percentage-is-x-of-y-hero",
            "size": "hero",
            "prompt": (
                "Fraction converting to percentage visualization showing X over Y equals percentage, "
                "clean mathematical diagram with visual fraction bar and percent result, "
                "blue accent, white background, educational editorial"
            ),
        },
    ],
}

SITE_ORDER = ["agecalc.io", "tipcalc.io", "amortcalc.io", "margincalc.io", "percentcalc.io"]

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


def run_site(site: str, force: bool = False, test: bool = False):
    if site not in SITE_MANIFESTS:
        print(f"Unknown site: {site}. Available: {', '.join(SITE_ORDER)}", file=sys.stderr)
        sys.exit(1)

    specs = SITE_MANIFESTS[site]
    blog_output_dir = os.path.abspath(f"sites/{site}/public/images/blog")
    os.makedirs(blog_output_dir, exist_ok=True)

    if test:
        specs = [specs[0]]  # OG image only for test

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Site: {site} ({len(specs)} images)", file=sys.stderr)
    print(f"Blog output: {blog_output_dir}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    for spec in specs:
        generate_image(spec, blog_output_dir, skip_existing=not force)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate Phase-2 imagery for 5 calculator sites"
    )
    parser.add_argument(
        "--site",
        choices=SITE_ORDER,
        help="Run for a specific site only",
    )
    parser.add_argument(
        "--all-sites",
        action="store_true",
        help="Run all 5 sites in sequence (35 images total)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all images for the selected --site",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Test mode: generate only the OG hero for the selected site",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing images",
    )

    args = parser.parse_args()

    if args.all_sites:
        for site in SITE_ORDER:
            run_site(site, force=args.force, test=False)
        return

    if args.site:
        run_site(args.site, force=args.force, test=args.test)
        return

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
