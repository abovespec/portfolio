#!/usr/bin/env python3
"""
FLUX.2-klein-4B stock image probe script.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_stock.py \
        --prompts prompts.json --output /tmp/stock_probe --steps 4

Generates images using FLUX.2-klein-4B (Flux2KleinPipeline).
Falls back to ERNIE-Image-Turbo if FLUX fails.
"""

import argparse
import json
import os
import sys
import time
import torch

FLUX_CACHE = "/data/huggingface"
ERNIE_CACHE = "/data/huggingface"
FLUX_MODEL = "black-forest-labs/FLUX.2-klein-4B"
ERNIE_MODEL = "baidu/ERNIE-Image-Turbo"

_pipe = None
_pipe_type = None


def load_flux():
    global _pipe, _pipe_type
    print("Loading FLUX.2-klein-4B...", file=sys.stderr)
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    from diffusers import Flux2KleinPipeline

    pipe = Flux2KleinPipeline.from_pretrained(
        FLUX_MODEL,
        torch_dtype=torch.bfloat16,
        cache_dir=FLUX_CACHE,
    )
    # Model is ~15GB weights — use cpu offload so activations have room on GPU
    pipe.enable_model_cpu_offload(gpu_id=0)
    print(f"FLUX loaded (model_cpu_offload). GPU0 free: {torch.cuda.mem_get_info(0)[0]/1e9:.1f}GB", file=sys.stderr)
    _pipe = pipe
    _pipe_type = "flux"
    return pipe


def load_ernie():
    global _pipe, _pipe_type
    print("Loading ERNIE-Image-Turbo (4-bit fallback)...", file=sys.stderr)
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

    from diffusers import ErnieImagePipeline
    from diffusers.quantizers.pipe_quant_config import PipelineQuantizationConfig
    from transformers import AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
    import gc

    bnb_4bit = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    quant_config = PipelineQuantizationConfig(
        quant_backend="bitsandbytes_4bit",
        quant_kwargs={"load_in_4bit": True, "bnb_4bit_compute_dtype": torch.bfloat16, "bnb_4bit_use_double_quant": True},
        components_to_quantize=["transformer"],
    )

    pipe = ErnieImagePipeline.from_pretrained(
        ERNIE_MODEL, torch_dtype=torch.bfloat16, quantization_config=quant_config, cache_dir=ERNIE_CACHE
    )

    snap_dir = [d for d in os.listdir(f"{ERNIE_CACHE}/models--baidu--ERNIE-Image-Turbo/snapshots/") if not d.startswith(".")][0]
    snap_path = f"{ERNIE_CACHE}/models--baidu--ERNIE-Image-Turbo/snapshots/{snap_dir}"

    del pipe.text_encoder
    gc.collect()
    pipe.text_encoder = AutoModel.from_pretrained(f"{snap_path}/text_encoder", quantization_config=bnb_4bit, torch_dtype=torch.bfloat16, device_map="auto")
    del pipe.pe
    gc.collect()
    pipe.pe = AutoModelForCausalLM.from_pretrained(f"{snap_path}/pe", quantization_config=bnb_4bit, torch_dtype=torch.bfloat16, device_map="auto")

    pipe.transformer = pipe.transformer.to("cuda:0")
    pipe.vae = pipe.vae.to("cuda:0")
    _pipe = pipe
    _pipe_type = "ernie"
    return pipe


def get_pipeline(backend="flux"):
    global _pipe, _pipe_type
    if _pipe is not None:
        return _pipe, _pipe_type
    if backend == "flux":
        try:
            return load_flux(), "flux"
        except Exception as e:
            print(f"FLUX load failed: {e}\nFalling back to ERNIE.", file=sys.stderr)
            return load_ernie(), "ernie"
    else:
        return load_ernie(), "ernie"


def generate_image(prompt, seed, output_path, steps=4, width=1024, height=1024, backend="flux"):
    pipe, pipe_type = get_pipeline(backend)
    torch.cuda.empty_cache()

    t0 = time.time()
    generator = torch.Generator(device="cpu").manual_seed(seed)

    if pipe_type == "flux":
        result = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=steps,
            generator=generator,
        )
    else:
        result = pipe(
            prompt=prompt,
            height=height,
            width=width,
            num_inference_steps=8,
            generator=generator,
        )

    img = result.images[0]
    elapsed = time.time() - t0

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # Save as WebP near-lossless (quality=95) to match makepicsmall.com compression pipeline
    if output_path.endswith(".webp"):
        img.save(output_path, format="WEBP", quality=95, method=6, lossless=False)
    else:
        img.save(output_path)
    print(f"  [{pipe_type}] {os.path.basename(output_path)} in {elapsed:.1f}s", file=sys.stderr)
    return elapsed, pipe_type


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True, help="JSON file with list of {id, niche, prompt, seed}")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--steps", type=int, default=4)
    parser.add_argument("--backend", choices=["flux", "ernie"], default="flux")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    args = parser.parse_args()

    with open(args.prompts) as f:
        prompts = json.load(f)

    os.makedirs(args.output, exist_ok=True)
    results = []

    for item in prompts:
        img_id = item["id"]
        niche = item["niche"]
        prompt = item["prompt"]
        seed = item.get("seed", 42)
        out_path = os.path.join(args.output, f"{img_id}.png")

        print(f"\n[{img_id}] {niche}: {prompt[:80]}...", file=sys.stderr)
        elapsed, pipe_type = generate_image(
            prompt=prompt, seed=seed, output_path=out_path,
            steps=args.steps, width=args.width, height=args.height, backend=args.backend
        )
        results.append({"id": img_id, "niche": niche, "prompt": prompt, "seed": seed, "path": out_path, "elapsed": elapsed, "backend": pipe_type})

    results_path = os.path.join(args.output, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

    total = sum(r["elapsed"] for r in results)
    print(f"\nDone. {len(results)} images in {total:.0f}s ({total/len(results):.1f}s avg). Results: {results_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
