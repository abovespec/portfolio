#!/usr/bin/env python3
"""
Generate hero images for stocksnap.fyi blog articles.
Uses ERNIE-Image-Turbo pipeline (same as ai_generate_textures.py).

Output: sites/stocksnap.fyi/public/images/blog/<slug>-hero.png
Format: 1200x630 (OG image ratio)

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_heroes.py
"""

import os
import sys
import time

# ---------------------------------------------------------------------------
# Blog article prompts — visually distinct, relevant to each article topic
# ---------------------------------------------------------------------------
HEROES = [
    {
        "slug": "abstract-background-images-free-download",
        "prompt": (
            "vibrant colorful abstract digital artwork, swirling gradient waves of blue purple "
            "and orange, geometric shapes and bokeh light effects, modern creative background, "
            "wide panoramic banner, professional graphic design"
        ),
    },
    {
        "slug": "ai-generated-stock-photos",
        "prompt": (
            "futuristic artificial intelligence concept art, glowing neural network nodes and "
            "connections, digital brain with luminous synapses, deep blue and cyan tones, "
            "technology and innovation, wide panoramic hero image"
        ),
    },
    {
        "slug": "best-free-stock-photo-sites-2026",
        "prompt": (
            "professional photography workspace, DSLR camera on clean white desk, photo editing "
            "software on monitor, film strips and photo prints arranged aesthetically, natural "
            "window light, wide banner composition"
        ),
    },
    {
        "slug": "free-stock-photos-no-attribution",
        "prompt": (
            "open creative freedom concept, hands releasing colorful butterflies from photo "
            "gallery, bright open doors leading to sunny landscape, liberation and accessibility "
            "theme, warm golden light, wide panoramic hero image"
        ),
    },
    {
        "slug": "free-workspace-photos-for-blog",
        "prompt": (
            "beautiful minimalist home office workspace flatlay, MacBook laptop with coffee mug "
            "and succulent plant, clean white desk with notebook and pen, soft natural morning "
            "light, top-down aerial view, wide banner format"
        ),
    },
    {
        "slug": "stock-photo-alternatives-free",
        "prompt": (
            "creative photography collage mosaic, diverse collection of lifestyle travel nature "
            "and business photos arranged in grid pattern, vibrant colors, professional quality "
            "stock images overview, wide panoramic banner"
        ),
    },
]

OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "sites",
    "stocksnap.fyi",
    "public",
    "images",
    "blog",
)


def get_pipeline():
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

    pipe = ErnieImagePipeline.from_pretrained(
        "baidu/ERNIE-Image-Turbo",
        torch_dtype=torch.bfloat16,
        quantization_config=quant_config,
        cache_dir="/data/huggingface",
    )

    snap_dir = [
        d
        for d in os.listdir("/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/")
        if not d.startswith(".")
    ][0]
    snap_path = f"/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/{snap_dir}"

    del pipe.text_encoder
    gc.collect()
    pipe.text_encoder = AutoModel.from_pretrained(
        f"{snap_path}/text_encoder",
        quantization_config=bnb_4bit,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    del pipe.pe
    gc.collect()
    pipe.pe = AutoModelForCausalLM.from_pretrained(
        f"{snap_path}/pe",
        quantization_config=bnb_4bit,
        torch_dtype=torch.bfloat16,
        device_map="auto",
    )

    pipe.transformer = pipe.transformer.to("cuda:0")
    pipe.vae = pipe.vae.to("cuda:0")
    print(
        f"Pipeline ready. GPU0: {torch.cuda.mem_get_info(0)[1]/1e9:.1f}GB",
        file=sys.stderr,
    )
    return pipe


def generate_hero(pipe, slug, prompt, seed=42):
    from PIL import Image
    import torch

    torch.cuda.empty_cache()

    print(f"\n[{slug}]", file=sys.stderr)
    print(f"  Prompt: {prompt[:80]}...", file=sys.stderr)
    t0 = time.time()

    # Generate at 1024x576 (16:9-ish, close to 1200x630 ratio)
    image = pipe(
        prompt=prompt,
        height=576,
        width=1024,
        num_inference_steps=8,
        generator=torch.Generator(device="cpu").manual_seed(seed),
    ).images[0]

    # Resize to exact OG dimensions
    image = image.resize((1200, 630), Image.LANCZOS)

    out_path = os.path.join(OUTPUT_DIR, f"{slug}-hero.png")
    image.save(out_path, optimize=True)
    elapsed = time.time() - t0
    print(f"  Saved {out_path} in {elapsed:.1f}s", file=sys.stderr)
    return out_path


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Skip already-generated images
    pending = [h for h in HEROES if not os.path.exists(os.path.join(OUTPUT_DIR, f"{h['slug']}-hero.png"))]

    if not pending:
        print("All hero images already exist.", file=sys.stderr)
        return

    print(f"Generating {len(pending)} hero image(s)...", file=sys.stderr)
    pipe = get_pipeline()

    for i, hero in enumerate(pending):
        seed = 1000 + i  # deterministic, distinct seeds
        generate_hero(pipe, hero["slug"], hero["prompt"], seed=seed)

    print("\nDone.", file=sys.stderr)


if __name__ == "__main__":
    main()
