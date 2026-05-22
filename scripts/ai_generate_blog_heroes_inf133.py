#!/usr/bin/env python3
"""
Generate hero images for 60 Tier 2 blog articles across 10 sites (INF-133).
Uses ERNIE-Image-Turbo with:
  - transformer: 4-bit bnb on CUDA (fast GPU denoising)
  - text_encoder: bfloat16 on CPU (fast BLAS text encoding, avoids bnb CPU bottleneck)
  - pe: disabled (prompts are pre-written and detailed; skipping saves ~10s/image)

Output: sites/{site}/public/images/blog/{slug}-hero.png
Format: 1200x630 (OG image ratio)

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_heroes_inf133.py
"""

import os
import sys
import time
import types
import gc

# ---------------------------------------------------------------------------
# All 60 hero articles in priority order: percentcalc → agecalc → tipcalc
# → quickcurrency → wordcounttools → workoutplanner → gradecalc → amortcalc
# → qrcodegen → financalc
# ---------------------------------------------------------------------------
SITES = {
    "percentcalc.io": [
        (
            "how-to-calculate-percentage-increase",
            "upward bar chart with green rising arrow, salary and price increase concept, "
            "percentage growth visualization, clean infographic style, wide panoramic banner",
        ),
        (
            "how-to-calculate-percentage-decrease",
            "downward arrow on a financial chart, red declining trend line, price drop and "
            "discount concept, percentage decrease visualization, wide panoramic hero image",
        ),
        (
            "how-to-calculate-sales-tax-percentage",
            "retail shopping receipt with calculator, store checkout counter, tax calculation "
            "concept, dollar bills and percentage symbols, clean commercial photography, "
            "wide banner format",
        ),
        (
            "markup-vs-margin-percentage",
            "split comparison diagram showing markup versus margin, business pricing concept, "
            "two colored columns with percentage arrows, professional infographic style, "
            "wide panoramic hero image",
        ),
        (
            "percentage-error-formula",
            "scientific laboratory with precision instruments and measurement tools, formula "
            "written on whiteboard, magnifying glass over data, accuracy and error concept, "
            "wide banner composition",
        ),
        (
            "percentage-of-a-number",
            "handwritten math equations on notebook paper, percentage symbols scattered, "
            "pencil and ruler, colorful pie chart showing proportions, clean educational "
            "concept, wide hero image",
        ),
    ],
    "agecalc.io": [
        (
            "age-difference-calculator-guide",
            "two people of different ages with birthday candles between them, calendar and "
            "timeline showing years apart, warm celebratory tones, wide panoramic banner",
        ),
        (
            "how-many-hours-old-am-i",
            "large analog clock face with glowing hour markers, hourglass with flowing sand "
            "beside it, time concept visualization, deep blue and gold tones, wide hero image",
        ),
        (
            "how-many-weeks-old-am-i",
            "calendar pages flipping through weeks, highlighted week blocks, time progression "
            "concept, warm paper texture, wide panoramic composition",
        ),
        (
            "how-old-am-i-in-months",
            "monthly calendar grid with months highlighted and circled, baby shoes next to "
            "adult shoes showing age span, soft warm tones, wide banner format",
        ),
        (
            "how-to-calculate-age-in-excel",
            "laptop with Excel spreadsheet open showing date formulas and DATEDIF function, "
            "clean office desk, data cells highlighted, professional productivity, wide banner",
        ),
        (
            "how-to-calculate-exact-age-years-months-days",
            "precise timeline ruler showing years months and days breakdown, calendar "
            "with magnifying glass, exact date calculation concept, clean flat design, "
            "wide panoramic hero image",
        ),
    ],
    "tipcalc.io": [
        (
            "hotel-tipping-etiquette",
            "luxury hotel lobby with bellhop carrying elegant luggage cart, warm golden "
            "interior lighting, marble floors and chandelier, professional hospitality, "
            "wide panoramic banner",
        ),
        (
            "how-much-to-tip-a-bartender",
            "bartender confidently mixing cocktails behind a stylish bar, glass bottles "
            "lined up, warm amber lighting, tip jar on the counter, wide hero image",
        ),
        (
            "how-much-to-tip-a-delivery-driver",
            "food delivery person at front door holding insulated bag, urban neighborhood "
            "setting, friendly interaction, doorstep delivery concept, wide panoramic banner",
        ),
        (
            "how-to-tip-on-a-credit-card",
            "customer at restaurant tapping credit card on POS terminal, tip entry screen "
            "visible, modern payment technology, warm dining atmosphere, wide banner format",
        ),
        (
            "should-you-tip-at-fast-food",
            "fast food counter with tip jar and question mark, bright chain restaurant "
            "interior, debate concept between yes and no, casual dining setting, wide hero",
        ),
        (
            "tipping-at-a-buffet",
            "lavish buffet spread with multiple serving stations, diverse dishes under "
            "warming lights, buffet restaurant interior, abundance and variety, wide banner",
        ),
    ],
    "quickcurrency.io": [
        (
            "best-apps-for-currency-conversion",
            "smartphone screen displaying currency conversion app with exchange rates, "
            "multiple currency flags, clean mobile UI, global travel concept, wide banner",
        ),
        (
            "currency-exchange-fees-explained",
            "currency exchange booth with fee schedule board, foreign banknotes and coins, "
            "hidden costs concept with magnifying glass, financial transparency, wide hero",
        ),
        (
            "how-to-convert-currency-manually",
            "handwritten currency conversion math on paper with formula, various foreign "
            "banknotes spread out, pen and calculator, simple calculation concept, wide banner",
        ),
        (
            "how-to-get-best-exchange-rate-traveling",
            "traveler at international airport comparing currency exchange options, boarding "
            "gate background, suitcase with foreign money, travel money tips, wide hero image",
        ),
        (
            "what-is-the-mid-market-rate",
            "professional forex trading screen with real-time exchange rate charts, bid and "
            "ask price spread visualization, financial data displays, wide panoramic banner",
        ),
        (
            "when-to-buy-foreign-currency",
            "calendar with currency symbols marked on optimal dates, timing strategy concept, "
            "forex chart with best moments circled, travel planning, wide banner composition",
        ),
    ],
    "wordcounttools.com": [
        (
            "average-words-per-minute-reading",
            "person reading book with speedometer overlay showing reading speed, open pages "
            "with words flowing, dynamic reading concept, warm library tones, wide hero banner",
        ),
        (
            "character-count-for-social-media",
            "smartphone showing social media posts with character limit counters, Twitter "
            "Instagram and LinkedIn icons, 280 characters display, clean mobile UI, wide banner",
        ),
        (
            "how-long-should-a-blog-post-be",
            "content ruler measuring blog post length, keyboard with word count in background, "
            "blogging concept with analytics graph showing optimal length, wide panoramic hero",
        ),
        (
            "how-long-to-read-1000-words",
            "stopwatch beside open document with exactly 1000 words highlighted, reading time "
            "concept, pages turning, focus and speed, clean editorial composition, wide banner",
        ),
        (
            "what-is-flesch-kincaid-readability",
            "readability score gauge dial from easy to difficult, text analysis with grade "
            "level visualization, educational assessment concept, clean infographic, wide hero",
        ),
        (
            "word-count-for-a-resume",
            "professional resume document on clean desk with word count indicator, pen and "
            "laptop, job application concept, crisp white and charcoal tones, wide banner",
        ),
    ],
    "workoutplanner.io": [
        (
            "4-day-workout-split-muscle-growth",
            "gym with four labeled training days on a whiteboard, dumbbells and barbell "
            "arranged by muscle group, clean modern gym interior, fitness planning, wide hero",
        ),
        (
            "5-day-workout-split-intermediate",
            "intermediate lifter performing deadlift with 5-day training schedule visible "
            "on gym wall, focused and athletic, dramatic lighting, wide panoramic banner",
        ),
        (
            "beginner-workout-plan-for-the-gym",
            "beginner entering bright modern gym for the first time, friendly personal "
            "trainer pointing to equipment, welcoming and motivating atmosphere, wide hero",
        ),
        (
            "how-to-create-your-own-workout-plan",
            "custom workout planner notebook open on gym bench with pen, exercise list "
            "and schedule being written, personal planning concept, wide banner composition",
        ),
        (
            "ppl-workout-split-for-beginners",
            "push pull legs split diagram on gym whiteboard, barbell squat and bench press "
            "equipment in background, three-day cycle visualization, wide panoramic hero image",
        ),
        (
            "upper-lower-split-workout-program",
            "split view of upper body dumbbell press and lower body barbell squat, "
            "training division concept, strong athletes in bright gym, wide banner format",
        ),
    ],
    "gradecalc.io": [
        (
            "cumulative-gpa-calculator-guide",
            "rising cumulative GPA line chart on academic transcript, student holding "
            "diploma, grade tracking dashboard, university campus in background, wide hero",
        ),
        (
            "gpa-scale-4-0-explained",
            "GPA scale from 0.0 to 4.0 displayed as colorful progress bar, letter grades "
            "A through F with points, academic grading infographic, wide panoramic banner",
        ),
        (
            "how-to-raise-your-gpa-fast",
            "student studying intensely with books and laptop, upward GPA arrow chart, "
            "library setting with warm motivational lighting, achievement concept, wide hero",
        ),
        (
            "letter-grade-to-gpa-conversion-chart",
            "grade conversion table showing A equals 4.0 B equals 3.0 and down, "
            "colorful academic chart, letter grades with GPA points, clean educational "
            "infographic, wide panoramic banner",
        ),
        (
            "semester-gpa-vs-cumulative-gpa",
            "two side-by-side GPA charts comparing semester and cumulative trends, "
            "academic report card split visualization, clean comparison design, wide hero",
        ),
        (
            "what-is-a-good-gpa-in-college",
            "college campus quad with students walking, GPA target visualization overlay, "
            "academic excellence concept, ivy-covered buildings, bright sunny day, wide banner",
        ),
    ],
    "amortcalc.io": [
        (
            "biweekly-mortgage-payments-vs-monthly",
            "biweekly vs monthly mortgage payment comparison calendar, house model beside "
            "payment schedule, savings visualization, real estate finance, wide panoramic hero",
        ),
        (
            "home-equity-loan-vs-heloc",
            "house with equity visualized as a money stack, split comparison of home equity "
            "loan versus HELOC, financial planning concept, warm home setting, wide banner",
        ),
        (
            "how-to-pay-off-30-year-mortgage-early",
            "30-year mortgage timeline being shortened with scissors concept, house key "
            "with countdown calendar, early payoff strategy visualization, wide hero image",
        ),
        (
            "how-to-read-an-amortization-schedule",
            "amortization table printed on paper with principal and interest columns "
            "highlighted, calculator and house model on desk, mortgage breakdown, wide banner",
        ),
        (
            "should-you-buy-mortgage-points",
            "mortgage points concept with interest rate reduction arrow, closing cost "
            "documents with checkmark, decision-making financial concept, wide panoramic hero",
        ),
        (
            "what-is-a-balloon-payment-mortgage",
            "balloon payment concept with large final payment visualization, mortgage "
            "schedule showing small payments then big lump sum, financial risk, wide banner",
        ),
    ],
    "qrcodegen.io": [
        (
            "how-to-add-logo-to-qr-code",
            "QR code with company logo centered inside it, branded QR code design on "
            "white background, smartphone scanning it, professional branding concept, wide hero",
        ),
        (
            "how-to-create-qr-code-for-wifi",
            "QR code displayed beside wifi router with signal waves, smartphone scanning "
            "wifi QR code, seamless wireless connection concept, tech minimal style, wide banner",
        ),
        (
            "qr-code-for-business-card",
            "elegant business card with QR code printed on it, professional networking "
            "concept, card being scanned by smartphone, clean modern design, wide panoramic hero",
        ),
        (
            "qr-code-for-restaurant-menu",
            "restaurant table with QR code menu stand, customer scanning code with phone "
            "to view digital menu, modern contactless dining, warm restaurant ambience, wide hero",
        ),
        (
            "qr-code-size-guide-for-printing",
            "QR codes shown at various print sizes on a ruler measuring guide, from "
            "tiny stamp size to large poster format, print production concept, wide banner",
        ),
        (
            "qr-code-vs-barcode",
            "QR code and traditional barcode shown side by side on retail products, "
            "comparison visualization, scanner beam on both, clean product photography, wide hero",
        ),
    ],
    "financalc.io": [
        (
            "apr-vs-apy-difference",
            "APR versus APY split comparison chart, interest rate difference visualization, "
            "banking and loan concept, financial calculation infographic, wide panoramic banner",
        ),
        (
            "compound-interest-formula-explained",
            "compound interest exponential growth curve on financial chart, formula "
            "written on whiteboard behind it, money growing over time, wide panoramic hero image",
        ),
        (
            "how-to-calculate-return-on-investment",
            "ROI percentage calculation concept, investment portfolio with returns graph "
            "trending upward, profit visualization, business finance, wide banner composition",
        ),
        (
            "how-to-use-a-loan-calculator",
            "loan calculator interface on laptop screen showing monthly payment breakdown, "
            "principal and interest visualization, financial planning desk, wide hero banner",
        ),
        (
            "rule-of-72-explained",
            "rule of 72 concept with money doubling timeline, 72 divided by interest rate "
            "equals years visualization, financial rule of thumb infographic, wide banner",
        ),
        (
            "simple-interest-vs-compound-interest",
            "side-by-side growth chart comparing simple interest flat line versus compound "
            "interest exponential curve, financial comparison, clear data visualization, wide hero",
        ),
    ],
}

PRIORITY_ORDER = [
    "percentcalc.io",
    "agecalc.io",
    "tipcalc.io",
    "quickcurrency.io",
    "wordcounttools.com",
    "workoutplanner.io",
    "gradecalc.io",
    "amortcalc.io",
    "qrcodegen.io",
    "financalc.io",
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
    os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
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

    print(
        f"Pipeline ready. GPU free: {torch.cuda.mem_get_info(0)[0]/1e9:.1f} GB",
        file=sys.stderr,
    )
    return pipe


def generate_hero(pipe, site, slug, prompt, path, seed):
    import torch
    from PIL import Image

    torch.cuda.empty_cache()
    print(f"\n[{site}/{slug}]", file=sys.stderr)
    t0 = time.time()

    image = pipe(
        prompt=prompt,
        height=576,
        width=1024,
        num_inference_steps=8,
        use_pe=False,
        generator=torch.Generator(device="cpu").manual_seed(seed),
    ).images[0]

    image = image.resize((1200, 630), Image.LANCZOS)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    image.save(path, optimize=True)
    elapsed = time.time() - t0
    print(f"  Saved in {elapsed:.1f}s → {path}", file=sys.stderr)
    return elapsed


def main():
    pending = get_pending()
    total = sum(len(v) for v in SITES.values())

    if not pending:
        print(f"All {total} hero images already exist.", file=sys.stderr)
        return

    already_done = total - len(pending)
    print(
        f"Generating {len(pending)} image(s) ({already_done}/{total} already done)...",
        file=sys.stderr,
    )

    pipe = get_pipeline()
    t_start = time.time()
    times = []

    for i, (site, slug, prompt, path) in enumerate(pending):
        seed = 2000 + i
        elapsed = generate_hero(pipe, site, slug, prompt, path, seed=seed)
        times.append(elapsed)
        done = i + 1
        remaining = len(pending) - done
        avg = sum(times) / len(times)
        eta_min = avg * remaining / 60
        print(
            f"  [{done}/{len(pending)}] avg {avg:.0f}s/img — ETA {eta_min:.1f} min",
            file=sys.stderr,
        )

    total_min = (time.time() - t_start) / 60
    print(f"\nAll {len(pending)} images done in {total_min:.1f} min.", file=sys.stderr)


if __name__ == "__main__":
    main()
