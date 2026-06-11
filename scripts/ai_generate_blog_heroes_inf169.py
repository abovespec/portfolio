#!/usr/bin/env python3
"""
Generate hero images for 60 Tier-2 blog articles across 10 sites (INF-169).
Articles added in commit a1070d0 (INF-162).

Uses ERNIE-Image-Turbo with:
  - transformer: 4-bit bnb on CUDA (fast GPU denoising)
  - text_encoder: bfloat16 on CPU (fast BLAS text encoding, avoids bnb CPU bottleneck)
  - pe: disabled (prompts are pre-written and detailed; skipping saves ~10s/image)

Output: sites/{site}/public/images/blog/{slug}-hero.png
Format: 1200x630 (OG image ratio)

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_heroes_inf169.py
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_heroes_inf169.py --test
"""

import argparse
import glob
import os
import sys
import time
import types
import gc

# ---------------------------------------------------------------------------
# CUDA allocator config — must be set before any torch.cuda usage.
# expandable_segments prevents fragmentation OOM across multiple images.
# ---------------------------------------------------------------------------
os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")

# ---------------------------------------------------------------------------
# CUDA 11.8 lib bootstrap for sm_61 (GTX 1060) compatibility.
# PyTorch 2.7.1+cu118 needs libcudart.so.11.0 etc., provided by the
# nvidia-*-cu11 pip packages. Re-exec with the right LD_LIBRARY_PATH so
# the dynamic linker finds them before any CUDA imports happen.
# ---------------------------------------------------------------------------
_VENV_SITE = os.path.join(
    os.path.dirname(sys.executable), "..", "lib", "python3.11", "site-packages"
)
_VENV_SITE = os.path.normpath(_VENV_SITE)
_CU11_LIBS = glob.glob(os.path.join(_VENV_SITE, "nvidia", "*", "lib"))
if _CU11_LIBS:
    _CU11_PATH = ":".join(_CU11_LIBS)
    _CURRENT_LD = os.environ.get("LD_LIBRARY_PATH", "")
    if _CU11_PATH not in _CURRENT_LD:
        os.environ["LD_LIBRARY_PATH"] = _CU11_PATH + (":" + _CURRENT_LD if _CURRENT_LD else "")
        os.execv(sys.executable, [sys.executable] + sys.argv)

# ---------------------------------------------------------------------------
# 60 hero articles across 10 Tier-2 sites (INF-162 / commit a1070d0)
# Sites: citefast.io, passwordgen.io, colorpalette.io, pomotimer.io,
#        worldclock.io, regexbuilder.io, caseconvert.io, uuidgen.io,
#        crontab.io, encodeonline.io
# ---------------------------------------------------------------------------
SITES = {
    "citefast.io": [
        (
            "apa-7th-edition-guide",
            "open academic style manual with colorful sticky notes and highlighted pages, "
            "scholarly reference book on clean library desk, citation formatting concept, "
            "warm ivory tones with academic blue accents, wide panoramic hero banner",
        ),
        (
            "harvard-referencing-guide",
            "stacked academic books on university library shelf with crimson color accents, "
            "scholarly research concept, organized reference materials and open notebook, "
            "warm intellectual library atmosphere, wide hero banner",
        ),
        (
            "how-to-cite-a-journal-article",
            "academic journal printed on glossy paper beside a pencil and research notebook, "
            "peer-reviewed publication concept, highlighted author and title header sections, "
            "clean scholarly composition on white desk, wide panoramic banner",
        ),
        (
            "how-to-cite-website-apa",
            "laptop on desk with browser open, handwritten citation notes on paper beside it, "
            "digital research and note-taking concept, clean home-office setting, "
            "academic workflow visualization, wide hero banner",
        ),
        (
            "how-to-cite-youtube-video",
            "tablet displaying video player with pause frame visible, notepad with reference "
            "notes beside it, digital media citation concept, casual academic study setting, "
            "warm natural lighting, wide panoramic banner",
        ),
        (
            "in-text-citation-apa",
            "open textbook page with parenthetical notation highlighted in yellow, "
            "academic reading and annotation concept, pen marking key passages, "
            "clean scholarly desk atmosphere, wide hero banner",
        ),
    ],
    "passwordgen.io": [
        (
            "how-long-should-a-password-be",
            "measuring tape unrolled beside a login form visualization, length comparison "
            "concept with graduated scale, security and size measurement, "
            "minimal tech design with blue accents, wide panoramic hero banner",
        ),
        (
            "multi-factor-authentication",
            "smartphone displaying one-time code next to laptop login screen, layered "
            "security concept with multiple verification steps, modern secure workspace, "
            "clean tech aesthetic, wide hero banner",
        ),
        (
            "nist-password-guidelines",
            "official government-style security policy document with compliance checklist, "
            "cybersecurity standards visualization, organized professional setting, "
            "crisp navy and white color palette, wide panoramic banner",
        ),
        (
            "password-entropy",
            "abstract visualization of random data scatter transforming into an ordered "
            "cryptographic strength meter, entropy concept with particle field, "
            "dark technical aesthetic with glowing blue elements, wide hero banner",
        ),
        (
            "passwordless-authentication-passkeys",
            "fingerprint scan glowing blue beside phone unlock animation, "
            "biometric authentication concept, modern secure login without a password field, "
            "sleek minimalist tech visualization, wide panoramic banner",
        ),
        (
            "two-factor-authentication",
            "two interlocking security shields with padlock icons, dual-layer protection "
            "concept, phone and laptop working together for identity verification, "
            "clean security infographic style, wide hero banner",
        ),
    ],
    "colorpalette.io": [
        (
            "analogous-colors",
            "smooth color wheel showing adjacent hues blending naturally from yellow to orange "
            "to red, analogous color harmony visualization, artist palette with neighboring "
            "warm tones, clean design concept, wide panoramic banner",
        ),
        (
            "color-palette-inspiration",
            "scattered paint chips and color swatches on a light table, mood board with "
            "harmonious color combinations inspired by nature, designer inspiration concept, "
            "beautiful arrangement of tiles, wide hero banner",
        ),
        (
            "color-psychology-marketing",
            "colorful brand color blocks arranged with emotional association labels, marketing "
            "color wheel concept, consumer psychology visualization, clean professional "
            "infographic design, wide panoramic banner",
        ),
        (
            "dark-mode-color-palette",
            "sleek dark UI mockup showing elegantly contrasted interface colors on deep "
            "charcoal background, night mode design with glowing accent hues, "
            "developer design concept, wide hero banner",
        ),
        (
            "hex-color-codes",
            "vibrant color swatches arranged in a grid pattern, design tool aesthetic, "
            "colorful mosaic of digital color tiles, flat graphic design concept "
            "with bold saturated palette, wide panoramic banner",
        ),
        (
            "warm-vs-cool-colors",
            "split-view image with warm orange and golden tones on the left versus cool "
            "blue and teal tones on the right, color temperature contrast concept, "
            "visual design comparison, wide hero banner",
        ),
    ],
    "pomotimer.io": [
        (
            "free-pomodoro-timer",
            "red tomato kitchen timer on a tidy wooden desk beside notebook and pen, "
            "classic 25-minute work session concept, minimalist productivity setup, "
            "warm focused workspace atmosphere, wide panoramic banner",
        ),
        (
            "how-to-stay-focused-studying",
            "student sitting at a clean well-lit desk with open books and zero distractions, "
            "deep focus and concentration concept, calm and organized study environment, "
            "soft natural light, wide hero banner",
        ),
        (
            "pomodoro-technique-adhd",
            "colorful sticky notes organizing tasks into short intervals on a bright wall, "
            "structured time management for focus concept, energetic and organized workspace, "
            "cheerful productivity visualization, wide panoramic banner",
        ),
        (
            "pomodoro-technique-for-students",
            "college student at campus library table with textbooks stacked and timer nearby, "
            "study session intervals concept, campus academic life, "
            "warm scholarly atmosphere, wide hero banner",
        ),
        (
            "pomodoro-technique-work-from-home",
            "cozy home office setup with laptop, coffee mug, and small timer on a wooden desk, "
            "work-from-home productivity concept, comfortable yet focused workspace, "
            "natural window light, wide panoramic banner",
        ),
        (
            "time-management-for-students",
            "open student planner showing weekly schedule with color-coded time blocks, "
            "organized academic planning concept, calendar spread with pen and highlighters, "
            "clean productivity design, wide hero banner",
        ),
    ],
    "worldclock.io": [
        (
            "gmt-vs-utc",
            "two large wall clocks side by side labeled GMT and UTC, time reference comparison "
            "concept, global time standard visualization, clean minimalist design on pale wall, "
            "wide panoramic banner",
        ),
        (
            "military-time-24-hour-clock",
            "24-hour analog clock face with bold numerals running to 24, "
            "military time notation concept, precision time display, "
            "clean technical design on dark background, wide hero banner",
        ),
        (
            "pst-vs-pdt",
            "US West Coast map silhouette with sun and clock overlay showing daylight saving "
            "transition, Pacific time zones concept, seasonal clock change visualization, "
            "warm golden and blue tones, wide panoramic banner",
        ),
        (
            "spring-forward-fall-back",
            "two clocks side by side with arrows showing one hour forward in spring and one "
            "hour back in fall, seasonal time adjustment concept, sun and moon symbolism, "
            "warm and cool lighting contrast, wide hero banner",
        ),
        (
            "time-zone-converter-guide",
            "world map with multiple city clock faces overlaid at their geographic locations, "
            "international time conversion concept, global connectivity visualization, "
            "clean cartographic style, wide panoramic banner",
        ),
        (
            "time-zone-map",
            "detailed world map with distinct colored bands for each time zone, "
            "international date line visible, rich cartographic visualization, "
            "geographic information style, wide hero banner",
        ),
    ],
    "regexbuilder.io": [
        (
            "regex-catastrophic-backtracking",
            "complex maze with many dead ends and looping paths creating exponential "
            "complexity, problem-solving challenge concept, abstract labyrinth pattern, "
            "dark moody visualization, wide panoramic banner",
        ),
        (
            "regex-find-replace",
            "magnifying glass hovering over highlighted text with a replacement arrow "
            "pointing to transformed output, text find-and-replace concept, "
            "clean editorial visualization, wide hero banner",
        ),
        (
            "regex-flags",
            "multiple colorful flag icons on poles representing modifiers and settings, "
            "toggle switch options concept, feature flags visualization, "
            "clean infographic design with bright accent colors, wide panoramic banner",
        ),
        (
            "regex-javascript",
            "abstract geometric shapes with overlapping circles and intersecting patterns "
            "representing string matching logic, filter visualization, "
            "clean modern design with yellow and dark accents, wide hero banner",
        ),
        (
            "regex-phone-number",
            "vintage rotary telephone with a glowing pattern validation overlay, "
            "phone number format recognition concept, classic and digital blend, "
            "warm nostalgic colors, wide panoramic banner",
        ),
        (
            "regex-python",
            "abstract serpentine flow of colored data segments representing pattern "
            "extraction and matching, processing concept, blue and yellow color scheme, "
            "geometric flow visualization, wide hero banner",
        ),
    ],
    "caseconvert.io": [
        (
            "database-naming-conventions",
            "organized database entity relationship diagram with tables connected by lines, "
            "data architecture concept, structured relationships visualization, "
            "clean technical infographic with blue grid, wide panoramic banner",
        ),
        (
            "javascript-naming-conventions",
            "abstract geometric shapes with different typographic labels showing naming styles, "
            "code naming standards concept, clean modern design with yellow JavaScript "
            "color palette accents, wide hero banner",
        ),
        (
            "python-naming-conventions-pep8",
            "clean style guide book with blue cover beside an organized notebook, "
            "coding standards and PEP8 compliance concept, software quality visualization, "
            "professional desk setting, wide panoramic banner",
        ),
        (
            "snake-case-vs-kebab-case",
            "two parallel horizontal paths: one with underscore connectors and one with "
            "hyphen connectors, naming convention comparison concept, "
            "clean split-view design with contrasting colors, wide hero banner",
        ),
        (
            "what-is-camelcase",
            "abstract camel silhouette with humps corresponding to capitalized word segments, "
            "playful naming convention visualization, warm desert sunset gradient, "
            "creative infographic design, wide panoramic banner",
        ),
        (
            "what-is-kebab-case",
            "segmented word pieces threaded on a horizontal skewer like a kebab, "
            "playful wordplay naming concept, warm earthy food tones, "
            "creative visual analogy design, wide hero banner",
        ),
    ],
    "uuidgen.io": [
        (
            "nanoid-vs-uuid",
            "two physical ID card designs side by side, one compact and one full-length, "
            "unique identifier comparison concept, modern minimalist design, "
            "clean professional style, wide panoramic banner",
        ),
        (
            "uuid-collision-probability",
            "vast star field in deep space with billions of points of light, "
            "astronomical improbability concept, near-zero collision chance visualization, "
            "dark cosmic wide hero image",
        ),
        (
            "uuid-database-performance",
            "sleek server rack with glowing performance metric gauges on display, "
            "database speed benchmark visualization, data storage efficiency concept, "
            "modern technical infrastructure, wide panoramic banner",
        ),
        (
            "uuid-python",
            "abstract hexadecimal character stream forming a unique digital fingerprint, "
            "identifier generation concept, blue and white geometric pattern, "
            "data uniqueness visualization, wide hero banner",
        ),
        (
            "uuid-vs-auto-increment",
            "sequential numbered tags on the left versus complex unique fingerprint pattern "
            "on the right, two database key strategies comparison, "
            "clean side-by-side infographic visualization, wide panoramic banner",
        ),
        (
            "what-is-ulid",
            "horizontal timeline with sortable unique tokens placed in chronological order, "
            "time-ordered identifier concept, sequential data visualization, "
            "clean minimal design with gradient timeline, wide hero banner",
        ),
    ],
    "crontab.io": [
        (
            "cron-environment-variables",
            "server configuration panel with labeled environment variable slots, "
            "system settings visualization concept, clean technical infrastructure, "
            "data center aesthetic with status indicators, wide panoramic banner",
        ),
        (
            "cron-path-variable",
            "branching directory pathway diagram showing system path resolution steps, "
            "route finding and navigation concept, hierarchical flow visualization, "
            "clean technical flowchart design, wide hero banner",
        ),
        (
            "cron-timezone",
            "server rack with world clocks mounted on wall showing different city times, "
            "scheduled job timezone concept, global infrastructure visualization, "
            "professional data center setting, wide panoramic banner",
        ),
        (
            "github-actions-schedule",
            "automated assembly line with synchronized gears turning on a repeating schedule, "
            "CI and CD workflow automation concept, clock-triggered pipeline visualization, "
            "industrial precision aesthetic, wide hero banner",
        ),
        (
            "kubernetes-cronjob",
            "large ship helm wheel with container shipping icons arranged in circular gear "
            "pattern around it, orchestration and scheduling concept, "
            "cloud infrastructure visualization, wide panoramic banner",
        ),
        (
            "systemd-timer-vs-cron",
            "two clock mechanisms placed side by side, traditional mechanical gear clock "
            "versus modern digital timer display, scheduling technology comparison concept, "
            "clean technical split-view, wide hero banner",
        ),
    ],
    "encodeonline.io": [
        (
            "base64-python",
            "stream of plain text characters on the left flowing and transforming into "
            "encoded alphanumeric groups on the right, encoding transformation concept, "
            "clean abstract data flow visualization, wide panoramic banner",
        ),
        (
            "encoding-vs-encryption",
            "open book on the left side versus a locked vault with padlock on the right, "
            "encoding for transmission versus encryption for security concept, "
            "clear visual distinction design, wide hero banner",
        ),
        (
            "hex-to-ascii",
            "hexadecimal values shown transforming with an arrow into readable alphabet "
            "characters, data format conversion concept, clean technical two-panel "
            "visualization, wide panoramic banner",
        ),
        (
            "md5-vs-sha256",
            "two hash function digest visualizations side by side with different lengths "
            "and complexities, cryptographic hash comparison concept, "
            "security strength infographic design, wide hero banner",
        ),
        (
            "sha256-hash-explained",
            "abstract one-way transformation showing diverse colorful inputs merging into a "
            "single fixed-length digital fingerprint, cryptographic hash concept, "
            "data integrity visualization, clean design, wide panoramic banner",
        ),
        (
            "utf8-character-encoding",
            "diverse international scripts and language symbols flowing from multiple "
            "directions into a unified digital encoding standard symbol, "
            "global character set concept, multilingual digital communication, wide hero banner",
        ),
    ],
}

PRIORITY_ORDER = [
    "citefast.io",
    "passwordgen.io",
    "colorpalette.io",
    "pomotimer.io",
    "worldclock.io",
    "regexbuilder.io",
    "caseconvert.io",
    "uuidgen.io",
    "crontab.io",
    "encodeonline.io",
]

BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "sites")


def output_path(site, slug):
    return os.path.join(BASE_DIR, site, "public", "images", "blog", f"{slug}-hero.png")


def get_pending():
    pending = []
    for site in PRIORITY_ORDER:
        for slug, prompt in SITES[site]:
            path = output_path(site, slug)
            if not os.path.exists(path):
                pending.append((site, slug, prompt, path))
    return pending


def get_pipeline():
    print("Loading ERNIE-Image-Turbo (transformer 4-bit GPU, text_encoder bf16 CPU)...", file=sys.stderr)

    import torch
    from diffusers import ErnieImagePipeline
    from diffusers.quantizers.pipe_quant_config import PipelineQuantizationConfig
    from transformers import AutoModel

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
        torch_dtype=torch.bfloat16,
        device_map="cpu",
    )

    del pipe.pe
    gc.collect()
    pipe.pe = None

    pipe.transformer = pipe.transformer.to("cuda:0")
    pipe.vae = pipe.vae.to("cuda:0")

    # Force execution device to CUDA so _pad_text moves embeddings to GPU
    ErnieImagePipeline._execution_device = property(lambda self: torch.device("cuda:0"))

    # Patch encode_prompt to use text_encoder's actual device (CPU) for inputs,
    # avoiding bitsandbytes CPU compute bottleneck.
    def _encode_prompt_cpu(self, prompt, device, num_images_per_prompt=1):
        if isinstance(prompt, str):
            prompt = [prompt]
        text_hiddens = []
        te_device = next(self.text_encoder.parameters()).device
        for p in prompt:
            ids = self.tokenizer(p, add_special_tokens=True, truncation=True, padding=False)["input_ids"]
            if not ids:
                ids = [self.tokenizer.bos_token_id or 0]
            input_ids = torch.tensor([ids], device=te_device)
            with torch.no_grad():
                outputs = self.text_encoder(input_ids=input_ids, output_hidden_states=True)
                hidden = outputs.hidden_states[-2][0]
            for _ in range(num_images_per_prompt):
                text_hiddens.append(hidden)
        return text_hiddens

    pipe.encode_prompt = types.MethodType(_encode_prompt_cpu, pipe)

    # Slice attention to reduce peak VRAM — essential on 6 GB card.
    pipe.enable_attention_slicing(slice_size=1)

    print(
        f"Pipeline ready. GPU free: {torch.cuda.mem_get_info(0)[0]/1e9:.1f} GB",
        file=sys.stderr,
    )
    return pipe


def generate_hero(pipe, site, slug, prompt, path, seed):
    import torch
    from PIL import Image

    gc.collect()
    torch.cuda.empty_cache()
    print(f"\n[{site}/{slug}]", file=sys.stderr)
    t0 = time.time()

    # Generate at 384x224 (~17:9) — smaller than 512x288 to reduce VAE
    # peak memory (fragmentation OOM on GTX 1060 after ~35 images).
    # 224 and 384 are both divisible by 16. Upscale to 1200x630 via LANCZOS.
    image = pipe(
        prompt=prompt,
        height=224,
        width=384,
        num_inference_steps=8,
        use_pe=False,
        generator=torch.Generator(device="cpu").manual_seed(seed),
    ).images[0]

    image = image.resize((1200, 630), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path, optimize=True)
    elapsed = time.time() - t0

    # Aggressively free memory after each image to prevent fragmentation OOM.
    del image
    gc.collect()
    torch.cuda.empty_cache()

    print(f"  Saved in {elapsed:.1f}s → {path}", file=sys.stderr)
    return elapsed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Generate only the first image then exit")
    args = parser.parse_args()

    pending = get_pending()
    total = sum(len(v) for v in SITES.values())

    if not pending:
        print(f"All {total} hero images already exist.", file=sys.stderr)
        return

    already_done = total - len(pending)
    to_run = pending[:1] if args.test else pending
    print(
        f"Generating {len(to_run)} image(s) ({already_done}/{total} already done)...",
        file=sys.stderr,
    )

    pipe = get_pipeline()
    t_start = time.time()
    times = []

    for i, (site, slug, prompt, path) in enumerate(to_run):
        seed = 3000 + i
        elapsed = generate_hero(pipe, site, slug, prompt, path, seed=seed)
        times.append(elapsed)
        done = i + 1
        remaining = len(to_run) - done
        avg = sum(times) / len(times)
        eta_min = avg * remaining / 60
        print(
            f"  [{done}/{len(to_run)}] avg {avg:.0f}s/img — ETA {eta_min:.1f} min",
            file=sys.stderr,
        )

    total_min = (time.time() - t_start) / 60
    print(f"\nAll {len(to_run)} images done in {total_min:.1f} min.", file=sys.stderr)


if __name__ == "__main__":
    main()
