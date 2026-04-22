# makepicsmall.com — MVP Design

Spec drafted 2026-04-22 during brainstorming session. Approved by human before writing-plans phase.

## 1. Goal

Ship a launchable, indexable MVP of makepicsmall.com — a free, browser-based image compression tool — within ~2 days of focused work. Site must validate the full Astro template + Cloudflare Pages + programmatic SEO playbook for the site network.

Success criteria (90 days post-launch):
- ≥ 20 tool URLs and ≥ 10 content URLs indexed by Google
- ≥ 500 organic impressions in GSC
- ≥ 50 real tool-completion events (user dropped file and downloaded compressed output)
- Core Web Vitals green on mobile

## 2. Scope decisions (locked via brainstorming)

| Question | Decision | Defers to Phase 2 |
|---|---|---|
| Formats supported | JPG, PNG, WebP | AVIF, GIF, SVG, HEIC, TIFF |
| UX mode | Target-aware (quality slider + target size input) | Advanced codec knobs |
| Concurrency | Parallel workers, capped at 3 | Server-assisted cloud batch |
| Page structure | Per-format + per-preset + combined landing pages (19 tool URLs) | Programmatic full matrix |
| Content at launch | 10 posts: 6 tool-companion + 3 educational pillars + 1 data study | Subsequent 2-3 posts/week |
| Branding | "Friendly utility" — coral accent on warm white, Geist Sans + Mono, simple squish mascot | — |

## 3. Architecture

### 3.1 Component model

```
┌─────────────────────────────────────────────────────────────┐
│ Astro page (static, per-URL)                                │
│  • landing copy                                             │
│  • FAQPage + SoftwareApplication JSON-LD                    │
│  • tool preset props (format, target_size, max_dim)         │
│  └─► <Compressor client:load preset={...}> (Preact island)  │
│        ├─ drop/click zone                                   │
│        ├─ quality slider / target size input                │
│        ├─ file list (one row per dropped file)              │
│        └─ worker pool (3 Web Workers, ea w/ WASM codec set) │
└─────────────────────────────────────────────────────────────┘
```

- **Landing pages** are static HTML; tool is a hydrated Preact island on each
- **Preset** is passed as props; URL is canonical source of truth for preset values
- **Worker pool** is created lazily on first drop/file-select; WASM loaded on demand (not at page load) for CWV
- **No server state**; zero uploads; tool runs 100% client-side

### 3.2 Worker pool design

- Pool size: `Math.min(navigator.hardwareConcurrency ?? 2, 3)` — cap at 3 (not 4 as originally specced)
- Per-worker bundle: mozjpeg-enc + oxipng + libwebp-enc, loaded as WASM at first use
- Queue: FIFO; workers pull jobs via `postMessage`
- Per-file result: `{ originalSize, compressedBlob, compressedSize, elapsed, attempts }`
- Target-size binary search: max 8 quality iterations, tolerance ±5%, stops at quality floor 20 or ceiling 95
- Memory safety: refuse files > 50 MB with clear error; warn at 20+ files queued

### 3.3 Format handling

| Format | Decoder | Encoder | Notes |
|---|---|---|---|
| JPG / JPEG | browser native (Image/createImageBitmap) | mozjpeg-enc (WASM) | target-size via quality binary search |
| PNG | browser native | oxipng (WASM) lossless + optional quant via pngquant (WASM) for aggressive reduction | target-size: try lossless first; if miss, step down palette sizes |
| WebP | browser native (decodes WebP on all evergreen browsers) | libwebp-enc (WASM) | target-size via quality binary search |

Transcoding (e.g. PNG upload → WebP download) is **out of scope for MVP** — user sees same-format-out. Phase 2 adds a "convert to" dropdown.

### 3.4 Preset mechanism

A preset is a JSON config:

```ts
type Preset = {
  format: 'jpg' | 'png' | 'webp' | 'auto'; // 'auto' = preserve input format
  targetKB?: number;              // optional hard target; overrides quality
  initialQuality?: number;        // 1-100, default 80
  maxLongSide?: number;           // downscale if image long side exceeds this
  /**
   * Optional aspect-lock. If provided, image is center-cropped then resized
   * to these exact pixel dimensions before encoding.
   * Examples: {w:600, h:600} for resume; {w:420, h:540} for Canadian passport.
   */
  lockDimensions?: { w: number; h: number };
};
```

Each landing page passes a preset literal at build time. The Compressor island reads it and applies defaults before first frame paints.

### 3.5 URL → preset mapping

See `src/config/presets.ts` (new file). Complete mapping:

| URL | Format | Target | Max long | Aspect lock |
|---|---|---|---|---|
| `/` | auto | — | — | — |
| `/compress/jpg` | jpg | — | — | — |
| `/compress/png` | png | — | — | — |
| `/compress/webp` | webp | — | — | — |
| `/compress/jpg/to/100kb` | jpg | 100 | — | — |
| `/compress/jpg/to/500kb` | jpg | 500 | — | — |
| `/compress/png/to/100kb` | png | 100 | — | — |
| `/to/50kb` | auto | 50 | — | — |
| `/to/100kb` | auto | 100 | — | — |
| `/to/500kb` | auto | 500 | — | — |
| `/to/1mb` | auto | 1000 | — | — |
| `/for/whatsapp` | jpg | 1500 | 1600 | — |
| `/for/whatsapp-dp` | jpg | 100 | — | 640×640 |
| `/for/instagram` | jpg | 500 | 1080 | — |
| `/for/instagram-story` | jpg | 600 | — | 1080×1920 |
| `/for/resume` | jpg | 100 | — | 600×600 |
| `/for/passport-us` | jpg | 240 | — | 600×600 |
| `/for/passport-canada` | jpg | 240 | — | 420×540 |
| `/for/passport-uk` | jpg | 1000 | — | 600×750 |
| `/for/linkedin` | jpg | 200 | — | 400×400 |

### 3.6 SEO structure per tool page

Every tool page renders:
- `<H1>` with exact target keyword
- 150-250 word intro explaining the specific use case
- Compressor island with preset prefilled
- 3-item FAQ (`<details>` with `FAQPage` JSON-LD)
- `SoftwareApplication` JSON-LD
- `BreadcrumbList` JSON-LD
- Related-posts strip (internal links to relevant blog posts)
- Canonical URL matches page URL; no duplicate presets sharing one canonical

### 3.7 Content collection structure

`src/content/blog/` — 10 MDX files, one per launch post. Frontmatter includes: title, description, publishDate, author, tags, image. Internal links wired during writing, not by convention.

Data study post (#10) has a companion `src/content/data-studies/jpg-vs-webp-1000.mdx` with a chart generator reading a committed JSON dataset.

## 4. Brand identity

### 4.1 Palette (CSS custom properties)

```
--site-theme-color: #fffdf8   (warm off-white, background)
--site-accent-color: #ff6b52  (coral)
--ink: #1a1a1a                (body text, high contrast)
--muted: #5a5a5a              (secondary text)
--surface: #fef3ed            (card / preset chip background)
--border: #e8ddd4             (soft borders)
--success: #059669            (compressed-size delta positive)
--warn: #d97706               (compression failed to hit target)
```

Dark mode: out of scope for MVP (defer to Phase 2 — not a ranking factor, adds design work).

### 4.2 Typography

- Headers + UI: **Geist Sans** (self-hosted via `@fontsource-variable/geist`)
- Numbers + code: **Geist Mono** (file sizes, quality values, percentages)
- Fallback: system sans

### 4.3 Mascot / visual motif

A single inline-SVG "squish" icon — two parallel curved lines suggesting compression from above/below. ~1KB, used in:
- Header logo (text + icon)
- Favicon (32×32 and SVG)
- OG image default (coral bg + icon + site name)
- Per-tool success state ("Squished X → Y!")

No full illustration / character work for MVP. Icon is the brand.

### 4.4 Voice & tone

- Second-person, plain-English, slightly self-aware
- Avoid marketing hype ("ultimate", "best-in-class")
- Do own the squish metaphor: "Your photos. Smaller. Squished in your browser."
- Error states say what happened and what to do: "That's a 64 MB file — we can only handle files up to 50 MB. Try splitting it or starting with a smaller source."

### 4.5 Layout primitives

- Max content width: 64rem (matches Astro `container-5xl` token)
- Vertical rhythm: 1.5x line-height on body, 1.1 on headers
- Corner radius: 12px on cards, 8px on buttons, 6px on inputs
- Shadows: soft, two-level system (`--shadow-sm`, `--shadow-md`) — no glass/glow effects

## 5. Data flow — the compress happy path

```
User drops file
  → Preact island reads preset from props + URL params (?target=50 can override)
  → File validated (type, size)
  → If aspect-locked preset: crop to fit via canvas (center crop)
  → If maxLongSide: downscale via createImageBitmap + canvas
  → Enqueue job to worker pool
  → Worker decodes → encodes (with target-size binary search if targetKB set)
  → Worker postMessages { originalSize, compressedBlob, compressedSize, elapsed }
  → UI updates file row with before/after + Download button
  → User clicks Download → Blob URL served via anchor download
  → (Optional) Plausible event: tool_completed { format, target_hit_pct }
```

Failure paths:
- File > 50MB → reject with clear error
- File type unsupported → reject with list of supported types
- Can't hit target in 8 attempts at floor quality → offer best result + warning "smallest we got: 143 KB (target was 100 KB). Try further cropping / downsampling."
- WASM load failure → fallback message + link to browser support info

## 6. Analytics

BaseLayout has a plug-in slot for analytics. For makepicsmall MVP:
- Self-hosted Plausible (user decides when to stand up the VPS; default: Cloudflare Web Analytics free tier if Plausible not ready)
- Events to track: `tool_completed`, `tool_failed`, `download_zip`, `preset_changed`, `shared_result`

Google Search Console + Bing Webmaster Tools + Ahrefs Webmaster Tools all connected during launch-day SOP.

## 7. Deployment & ops

- Existing Cloudflare Pages project `makepicsmall` already live (initial scaffold deploy done).
- Build via `pnpm build` in `sites/makepicsmall.com/`, deploy via wrangler in the same flow as the initial deploy.
- Cloudflare Pages automatically picks up git pushes if we wire up a GitHub repo (hybrid path — scheduled for after MVP ship).
- No edge functions needed for MVP. All static.
- `robots.txt` allows all; `sitemap-index.xml` auto-generated; GSC submission is part of launch SOP.

## 8. Testing

Per the Superpowers TDD skill, every code-producing task uses the red-green-refactor cycle.

Test types:
- **Unit** — preset parsing, quality binary-search math, target-size validation, URL→preset mapping
- **Integration** — full compress pipeline against a fixture image set (committed to `tests/fixtures/`)
- **Visual regression** — Playwright snapshot of each landing page at 375px and 1280px (post-MVP if time)
- **Lighthouse CI** — budget enforced: LCP ≤ 2.5s, CLS ≤ 0.1, bundle ≤ 150KB JS initial (WASM lazy-loaded)

Fixture set: 20 images across the 3 formats, spanning small (200KB) to large (15MB), with edge cases (tiny photos, very wide panoramas, mostly-transparent PNGs).

## 9. Out of scope for MVP (explicit — do not build)

- AVIF, GIF, SVG support
- HEIC decoding
- Format conversion (e.g. PNG → WebP output)
- Cropping UI (only preset-driven center crops)
- Advanced codec knobs (chroma subsampling, progressive JPEG, etc.)
- Background removal, EXIF stripping, resizing tool as a separate feature
- Dark mode
- i18n
- User accounts, saved preferences, history
- Server-assisted processing for large batches
- API or embeddable widget
- OG image generation per tool URL (static site-wide OG image for MVP)
- Social-share card generation

## 10. Open risks & mitigations

| Risk | Mitigation |
|---|---|
| WASM bundle too heavy for CWV on mobile | Lazy-load: don't import WASM until first file drop; show UI immediately; measure LCP on CI |
| Target-size binary search is slow | Cap at 8 iterations; show "Computing best quality..." spinner; benchmark on CI |
| Programmatic near-duplicate pages flagged by Google | Each landing page has unique preset behavior + unique 150-250w intro + unique FAQ — not just template swap |
| Passport photo pages give wrong dimensions and Google spots the inaccuracy | Each spec triple-checked against the respective government URL; link to source in FAQ |
| Data-study post requires real data | Spend ~1 day generating: pull 1000 stock images across Unsplash/Pexels APIs, run through compression matrix, commit dataset + generated charts |
| New domain publishes 20 URLs + 10 posts on day 1 — looks like AI farm | All 10 posts human-edited pre-publish; blog posts staggered across 2 weeks (not all day 1); 19 tool URLs are genuinely different tool states not thin content |

## 11. What ships on launch day

- 19 tool URLs live
- 4 posts live (posts 1-4 from content plan); posts 5-10 staggered over 14 days
- 5 standard pages (home, about, contact, privacy, terms) + sponsored intake page
- Sitemap submitted to GSC + Bing + Ahrefs
- First HARO/outreach pitches sent within week 1
- Analytics live

## 12. What ships in the next 30 days (post-launch)

- Remaining 6 posts (1 every ~2-3 days)
- Phase 2 format additions (AVIF first — it's the biggest marginal SEO win)
- One programmatic page expansion if the first 10 tool URLs are indexing well
- First Reddit post (only in a genuinely-useful sub with a working tool + valuable content; no spam)
- Product Hunt launch decision (go/no-go based on whether the tool has differentiated polish by week 3)

---

## Appendix: Dependency acceptance list (WASM codecs)

- `@jsquash/jpeg` (mozjpeg wrapper, active, used by Squoosh) — MIT
- `@jsquash/png` (oxipng+pngquant wrapper, active) — MIT
- `@jsquash/webp` (libwebp wrapper, active) — MIT
- `@fontsource-variable/geist` — OFL
- No other runtime deps for the tool itself beyond Preact (already in template)

All three codec packages are maintained by jamsinclair/jSquash (actively updated), are MIT, and are the same packages used by Google's Squoosh. Low supply-chain risk; well-tested.
