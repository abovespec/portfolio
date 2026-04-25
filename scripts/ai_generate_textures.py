#!/usr/bin/env python3
"""
AI texture generator for FreePBRTextures.
Uses ERNIE-Image-Turbo with diffusers to generate photorealistic textures,
then derives PBR maps (normal, roughness) via image processing.

Usage:
    # Use the dedicated venv on /data:
    /data/venvs/ai-image-gen/bin/python3.11 ai_generate_textures.py \\
        --category brick --count 3 --output sites/freepbrtextures.com/public/textures

    # Generate all categories:
    /data/venvs/ai-image-gen/bin/python3.11 ai_generate_textures.py \\
        --generate-all --count 2 --output sites/freepbrtextures.com/public/textures
"""

import argparse
import json
import os
import sys
import time
import hashlib
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageOps
from scipy import ndimage

# ---------------------------------------------------------------------------
# AI inference (lazy-loaded)
# ---------------------------------------------------------------------------
_pipe = None


def get_pipeline():
    global _pipe
    if _pipe is None:
        import os
        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        print("Loading ERNIE-Image-Turbo...", file=sys.stderr)
        from diffusers import ErnieImagePipeline
        from diffusers.quantizers.pipe_quant_config import PipelineQuantizationConfig
        from transformers import AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        import gc

        # Load everything in 4-bit via bitsandbytes to fit on 16GB GPUs.
        # Strategy: load pipeline with transformer 4-bit via diffusers,
        # then replace text_encoder and pe with bnb 4-bit versions.
        # All components fit on single GPU: ~7GB total at 4-bit.

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

        # Find local cache path for text_encoder and pe (custom models bundled with ERNIE)
        import os as _os
        snap_dir = [
            d
            for d in _os.listdir("/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/")
            if not d.startswith(".")
        ][0]
        snap_path = f"/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/{snap_dir}"

        # Replace text_encoder with 4-bit version
        del _pipe.text_encoder
        gc.collect()
        _pipe.text_encoder = AutoModel.from_pretrained(
            f"{snap_path}/text_encoder",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        # Replace pe with 4-bit version
        del _pipe.pe
        gc.collect()
        _pipe.pe = AutoModelForCausalLM.from_pretrained(
            f"{snap_path}/pe",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        # Move transformer + VAE to GPU 0
        _pipe.transformer = _pipe.transformer.to("cuda:0")
        _pipe.vae = _pipe.vae.to("cuda:0")
        print(f"Pipeline ready. GPU0: {torch.cuda.mem_get_info(0)[1]/1e9:.1f}GB, GPU1: {torch.cuda.mem_get_info(1)[1]/1e9:.1f}GB",
              file=sys.stderr)
    return _pipe


# ---------------------------------------------------------------------------
# Prompt templates per category
# ---------------------------------------------------------------------------
PROMPTS = {
    "wood": (
        "seamless photorealistic texture of {style}wood planks, "
        "high detail wood grain, natural colors, tileable, 4K PBR material"
    ),
    "stone": (
        "seamless photorealistic texture of {style}stone surface, "
        "detailed rock texture, natural stone colors, tileable, 4K PBR material"
    ),
    "concrete": (
        "seamless photorealistic texture of {style}concrete surface, "
        "detailed concrete finish, realistic cement texture, tileable, 4K PBR material"
    ),
    "metal": (
        "seamless photorealistic texture of {style}metal surface, "
        "detailed metallic finish, brushed metal look, tileable, 4K PBR material"
    ),
    "fabric": (
        "seamless photorealistic texture of {style}fabric material, "
        "detailed textile weave, cloth texture, tileable, 4K PBR material"
    ),
    "brick": (
        "seamless photorealistic texture of {style}brick wall, "
        "detailed brick pattern with mortar lines, realistic masonry, tileable, 4K PBR material"
    ),
    "marble": (
        "seamless photorealistic texture of {style}marble surface, "
        "detailed marble veining, polished stone look, tileable, 4K PBR material"
    ),
    "leather": (
        "seamless photorealistic texture of {style}leather surface, "
        "detailed leather grain, natural material texture, tileable, 4K PBR material"
    ),
}

STYLE_MODIFIERS = {
    "default": "",
    "dark": "dark ",
    "light": "light ",
    "rough": "rough ",
    "polished": "polished ",
    "weathered": "weathered aged ",
    "cracked": "cracked damaged ",
    "smooth": "smooth ",
    "textured": "textured ",
    "rustic": "rustic ",
    "modern": "modern clean ",
    "vintage": "vintage old ",
}


# ---------------------------------------------------------------------------
# Post-processing for seamless tiling
# ---------------------------------------------------------------------------
def make_seamless(img):
    """Apply edge blending to make an image tile seamlessly.

    Uses the overlap-and-blend approach: places the image in a 2x2 grid,
    blends overlapping strips at the center seams with a gradient mask,
    then crops back to original size.
    """
    w, h = img.size
    overlap = w // 8  # 12.5% overlap on each side

    # Create 2x2 grid
    tiled = Image.new(img.mode, (w * 2, h * 2))
    for tx in range(2):
        for ty in range(2):
            tiled.paste(img, (tx * w, ty * h))

    # Horizontal blend strip at center
    blend_width = overlap * 2
    # Build a gradient mask from 0 to 1 over the blend region
    mask_h = np.zeros((blend_width, w * 2), dtype=np.float32)
    for i in range(blend_width):
        t = i / blend_width
        val = np.sin(t * np.pi / 2) ** 2  # smoothstep-like
        mask_h[i, :] = 1 - val

    # Extract the top inner edge (last `overlap` rows of top half) and
    # bottom inner edge (first `overlap` rows of bottom half)
    center_y = h
    top_strip = np.array(tiled.crop((0, center_y - overlap, w * 2, center_y + overlap)))
    bot_strip = np.array(tiled.crop((0, center_y - overlap, w * 2, center_y + overlap)))

    if len(top_strip.shape) == 3:
        mask_3d = np.stack([mask_h] * top_strip.shape[2], axis=-1)
    else:
        mask_3d = mask_h

    blended_section = (top_strip.astype(np.float32) * mask_3d +
                       bot_strip.astype(np.float32) * (1 - mask_3d))
    blended_section = np.clip(blended_section, 0, 255).astype(np.uint8)

    # Paste blended section back
    result = np.array(tiled)
    result[center_y - overlap:center_y + overlap, :] = blended_section

    # Repeat for vertical blend
    blend_width_v = overlap * 2
    mask_v = np.zeros((h * 2, blend_width_v), dtype=np.float32)
    for i in range(blend_width_v):
        t = i / blend_width_v
        mask_v[:, i] = 1 - np.sin(t * np.pi / 2) ** 2

    center_x = w
    left_strip = result[:, center_x - overlap:center_x + overlap].copy()
    right_strip = result[:, center_x - overlap:center_x + overlap].copy()

    if len(left_strip.shape) == 3:
        mask_3d_v = np.stack([mask_v] * left_strip.shape[2], axis=-1)
    else:
        mask_3d_v = mask_v

    blended_v = (left_strip.astype(np.float32) * mask_3d_v +
                 right_strip.astype(np.float32) * (1 - mask_3d_v))
    blended_v = np.clip(blended_v, 0, 255).astype(np.uint8)
    result[:, center_x - overlap:center_x + overlap] = blended_v

    # Crop center back to original size
    result_img = Image.fromarray(result)
    cropped = result_img.crop((w // 2, h // 2, w // 2 + w, h // 2 + h))

    # Light blur to soften seam
    cropped = cropped.filter(ImageFilter.GaussianBlur(radius=1))
    return cropped


# ---------------------------------------------------------------------------
# PBR map derivation
# ---------------------------------------------------------------------------
def derive_normal_map(img_rgb):
    """Derive a normal map from an RGB image using Sobel filters.

    Returns a PIL Image with normal vectors encoded as RGB (range 0-255).
    """
    arr = np.array(img_rgb.convert("L")).astype(np.float32) / 255.0

    # Sobel gradients
    gx = ndimage.sobel(arr, axis=1)
    gy = ndimage.sobel(arr, axis=0)

    # Normal from gradient (in tangent space)
    strength = 2.0  # normal map strength
    gx = gx * strength
    gy = gy * strength
    gz = np.ones_like(arr)

    norm = np.sqrt(gx ** 2 + gy ** 2 + gz ** 2)
    norm = np.where(norm == 0, 1, norm)

    nx = (gx / norm * 0.5 + 0.5) * 255
    ny = (gy / norm * 0.5 + 0.5) * 255
    nz = (gz / norm * 0.5 + 0.5) * 255

    normal_arr = np.stack([nx, ny, nz], axis=-1).astype(np.uint8)
    return Image.fromarray(normal_arr)


def derive_roughness_map(img_rgb, base_roughness=0.6):
    """Derive a roughness map from an RGB image.

    Uses local contrast/variance as a proxy for surface roughness.
    Returns PIL Image (grayscale).
    """
    arr = np.array(img_rgb.convert("L")).astype(np.float32) / 255.0

    # Local variance via Sobel magnitude
    gx = ndimage.sobel(arr, axis=1)
    gy = ndimage.sobel(arr, axis=0)
    magnitude = np.sqrt(gx ** 2 + gy ** 2)

    # Normalize and scale
    mag_norm = magnitude / (magnitude.max() + 1e-8)
    roughness = np.clip(base_roughness + (mag_norm - 0.5) * 0.5, 0.05, 0.95)
    rough_img = (roughness * 255).astype(np.uint8)
    return Image.fromarray(rough_img, mode="L")


def upscale_4x(img):
    """Simple 4x upscale using LANCZOS resampling.

    For generating 4K output from 1024x1024 AI generations.
    """
    w, h = img.size
    return img.resize((w * 4, h * 4), Image.LANCZOS)


# ---------------------------------------------------------------------------
# Texture generation
# ---------------------------------------------------------------------------
def generate_texture(category, seed_name, seed_val, output_base, prompt_style="default", prompt_override=None):
    """Generate a single AI texture with full PBR set."""
    pipe = get_pipeline()

    # Build prompt
    if prompt_override:
        prompt = prompt_override
    else:
        style_mod = STYLE_MODIFIERS.get(prompt_style, STYLE_MODIFIERS["default"])
        prompt_template = PROMPTS.get(category, PROMPTS["stone"])
        prompt = prompt_template.format(style=style_mod)

    print(f"  [{category}/{seed_name}] Generating '{prompt}'...", file=sys.stderr)
    t0 = time.time()

    # Generate base image at 1024x1024
    import torch

    # Clear any stale GPU memory before inference
    torch.cuda.empty_cache()

    image = pipe(
        prompt=prompt,
        height=1024,
        width=1024,
        num_inference_steps=8,
        generator=torch.Generator(device="cpu").manual_seed(seed_val),
    ).images[0]

    gen_time = time.time() - t0
    print(f"  Generated in {gen_time:.1f}s", file=sys.stderr)

    # Make seamless
    seamless = make_seamless(image)

    # Derive PBR maps
    normal = derive_normal_map(seamless)
    roughness = derive_roughness_map(seamless)
    albedo = seamless

    # Upscale to 4K for full-size
    albedo_4k = upscale_4x(albedo)
    normal_4k = upscale_4x(normal)
    roughness_4k = upscale_4x(roughness)

    # Save
    slug = seed_name.lower().replace(" ", "-").replace("_", "-")
    output_dir = os.path.join(output_base, category, slug)
    os.makedirs(output_dir, exist_ok=True)

    albedo_4k.save(os.path.join(output_dir, "albedo.png"))
    normal_4k.save(os.path.join(output_dir, "normal.png"))
    roughness_4k.save(os.path.join(output_dir, "roughness.png"))
    albedo.resize((1024, 1024), Image.LANCZOS).save(os.path.join(output_dir, "preview.png"))
    albedo.resize((256, 256), Image.LANCZOS).save(os.path.join(output_dir, "thumbnail.png"))

    elapsed = time.time() - t0
    print(f"  Saved to {output_dir} in {elapsed:.1f}s", file=sys.stderr)

    # Metadata
    params = {"roughness": 0.6, "metallic": 0.0}
    metadata = {
        "title": slug.replace("-", " ").title(),
        "description": f"Seamless 4K AI-generated {category} texture. Photorealistic PBR material.",
        "category": category,
        "seed": seed_val,
        "seedName": seed_name,
        "prompt": prompt,
        "params": params,
        "shape": [4096, 4096],
        "generatedDate": time.strftime("%Y-%m-%d"),
    }
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    return metadata


def generate_content_md(texture_dir, output_dir):
    """Generate Astro content collection .md files from texture metadata."""
    os.makedirs(output_dir, exist_ok=True)

    for root, dirs, files in os.walk(texture_dir):
        if "metadata.json" not in files:
            continue
        slug = os.path.basename(root)
        md_path = os.path.join(output_dir, f"{slug}.md")
        if os.path.exists(md_path):
            continue  # skip already-existing content files
        with open(os.path.join(root, "metadata.json")) as f:
            meta = json.load(f)

        category = meta["category"]
        is_metallic = meta.get("params", {}).get("metallic", 0) > 0.5

        content = f"""---
title: "{meta['title']}"
description: "{meta['description']}"
category: "{category}"
tags:
  - "{category}"
  - "seamless"
  - "tileable"
  - "4k"
  - "texture"
  - "PBR"
resolution: "4K"
maps:
  albedo: true
  normal: true
  roughness: true
  metallic: {str(is_metallic)}
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

{meta['description']}

## Maps included

- **Albedo** --- 4K color map
- **Normal** --- 4K tangent-space normal map  
- **Roughness** --- 4K surface roughness map

## Details

- Resolution: 4096 x 4096 pixels
- Format: PNG
- License: CC0 (public domain, no attribution required)
- Generated via AI (ERNIE-Image-Turbo)

Download the full-resolution PBR set and use in your favorite 3D software.
"""
        md_path = os.path.join(output_dir, f"{slug}.md")
        with open(md_path, "w") as f:
            f.write(content.strip())
        print(f"  Content: {md_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI PBR texture generator using ERNIE-Image-Turbo")
    parser.add_argument("--category", choices=list(PROMPTS.keys()), help="Texture category")
    parser.add_argument("--count", type=int, default=3, help="Number of textures per category")
    parser.add_argument("--seed", type=str, default=None, help="Seed name prefix")
    parser.add_argument("--style", choices=list(STYLE_MODIFIERS.keys()), default="default",
                        help="Texture style modifier")
    parser.add_argument("--generate-all", action="store_true", help="All categories")
    parser.add_argument("--output", required=True, help="Output base directory (e.g., public/textures)")
    parser.add_argument("--content-dir", default=None,
                        help="Output directory for Astro content .md files")
    parser.add_argument("--no-pbr", action="store_true",
                        help="Skip PBR map derivation (albedo only)")
    parser.add_argument("--prompt", type=str, default=None,
                        help="Override prompt directly (skips category template and style modifier)")

    args = parser.parse_args()
    categories = list(PROMPTS.keys()) if args.generate_all else [args.category]
    if not categories or categories == [None]:
        parser.error("Specify --category or --generate-all")

    output_base = os.path.abspath(args.output)
    os.makedirs(output_base, exist_ok=True)

    print(f"Generating AI textures -> {output_base}")
    print(f"Categories: {', '.join(categories)}")
    print(f"Count per category: {args.count}")
    print()

    all_metadata = []
    for category in categories:
        seed_prefix = args.seed or f"ai-{category}"
        for i in range(args.count):
            seed_name = f"{seed_prefix}-{i + 1}"
            seed_val = int(hashlib.md5(seed_name.encode()).hexdigest()[:8], 16)
            meta = generate_texture(category, seed_name, seed_val, output_base, args.style, args.prompt)
            all_metadata.append(meta)

    # Generate content .md files (only when content-dir is explicit or the
    # default relative path resolves to an existing parent directory).
    if args.content_dir:
        content_dir = os.path.abspath(args.content_dir)
        generate_content_md(output_base, content_dir)
    else:
        derived = os.path.abspath(os.path.join(
            os.path.dirname(output_base), "..", "src", "content", "textures"
        ))
        if os.path.exists(os.path.dirname(derived)):
            generate_content_md(output_base, derived)
        else:
            print(f"Skipping content MD generation ('{derived}' not in repo structure).", file=sys.stderr)

    print(f"\nDone! Generated {len(all_metadata)} AI textures in {output_base}")


if __name__ == "__main__":
    main()
