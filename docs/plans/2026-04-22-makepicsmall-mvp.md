# makepicsmall MVP Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Ship a production-ready MVP of makepicsmall.com — a friendly, privacy-first, browser-based image compressor (JPG/PNG/WebP) with 19 SEO-optimized tool URLs and 4 launch blog posts, deployed live on Cloudflare Pages within 2 focused work-days.

**Architecture:** Astro 5 static site (already scaffolded at `sites/makepicsmall.com/`) with a Preact island for the compression UI. A 3-worker pool runs WASM codecs (mozjpeg, oxipng, libwebp via jSquash) entirely in the browser. Each landing page is a static HTML file that passes a typed `Preset` object to the Preact island at hydration. No backend, no uploads, no user accounts.

**Tech Stack:** Astro 5, Tailwind 4, TypeScript strict, Preact islands, `@jsquash/*` codec packages, Geist Sans + Mono via `@fontsource-variable`, Vitest for unit tests, Playwright for integration tests, Wrangler for deploy.

**Design spec:** `docs/superpowers/specs/2026-04-22-makepicsmall-mvp-design.md` (approved)

**Work directory:** `~/site-network/sites/makepicsmall.com/`

---

## Conventions for every task

- All paths are relative to `~/site-network/sites/makepicsmall.com/` unless stated otherwise.
- Run all commands from that directory (`cd ~/site-network/sites/makepicsmall.com/`).
- Every task ends with a commit. Commit messages use [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`, `style:`, `perf:`.
- Test runner is Vitest (`pnpm test`). Playwright is `pnpm test:e2e` (added in Phase E).
- After every task, the full test suite must still pass. Run `pnpm test -- --run` before committing.
- The template files already present in `sites/makepicsmall.com/` (from the `create-site` scaffold) are the starting point. Do NOT regenerate the site.

---

## Phase A — Foundation & brand (tasks 1–6)

### Task 1: Install compression dependencies

**Objective:** Add the three jSquash codec packages, Preact already present, font packages, and dev test deps.

**Files:**
- Modify: `package.json`

**Step 1: Add runtime deps**

```bash
cd ~/site-network/sites/makepicsmall.com
pnpm add @jsquash/jpeg @jsquash/png @jsquash/webp
pnpm add @fontsource-variable/geist @fontsource-variable/geist-mono
```

**Step 2: Add dev deps for testing**

```bash
pnpm add -D vitest @vitest/ui @testing-library/preact jsdom
```

**Step 3: Add vitest script**

Modify `package.json` scripts section to include:
```json
"test": "vitest",
"test:run": "vitest run"
```

**Step 4: Verify**

```bash
pnpm test:run 2>&1 | head -5
```
Expected: `No test files found` (exits non-zero but that's fine — confirms vitest is wired).

**Step 5: Commit**

```bash
git add package.json pnpm-lock.yaml
git commit -m "chore: add jsquash codecs, geist fonts, vitest"
```

---

### Task 2: Apply brand palette & Geist fonts to the template

**Objective:** Swap the default dark palette for the warm "friendly utility" palette; wire up Geist.

**Files:**
- Modify: `src/config/site.config.ts` (branding section)
- Modify: `src/styles/global.css`
- Modify: `src/layouts/BaseLayout.astro` (font imports)

**Step 1: Write failing test**

Create `tests/branding.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { siteConfig } from '../src/config/site.config';

describe('branding', () => {
  it('uses coral accent on warm off-white background', () => {
    expect(siteConfig.branding.themeColor).toBe('#fffdf8');
    expect(siteConfig.branding.accentColor).toBe('#ff6b52');
  });
  it('logo text matches domain identity', () => {
    expect(siteConfig.branding.logoText).toBe('makepicsmall');
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test:run tests/branding.test.ts
```
Expected: both tests FAIL (themeColor is still `#0f172a`).

**Step 3: Update `src/config/site.config.ts`**

Change the `branding` object:
```ts
branding: {
  themeColor: '#fffdf8',
  accentColor: '#ff6b52',
  logoText: 'makepicsmall',
  ogImageStrategy: 'static',
},
```

**Step 4: Run — expect PASS**

```bash
pnpm test:run tests/branding.test.ts
```
Expected: both tests PASS.

**Step 5: Update `src/styles/global.css`**

At the top of the file, define the full palette as CSS custom properties on `:root`:
```css
:root {
  --site-theme-color: #fffdf8;
  --site-accent-color: #ff6b52;
  --ink: #1a1a1a;
  --muted: #5a5a5a;
  --surface: #fef3ed;
  --border: #e8ddd4;
  --success: #059669;
  --warn: #d97706;
  --site-font-sans: 'Geist Variable', system-ui, -apple-system, sans-serif;
  --site-font-mono: 'Geist Mono Variable', ui-monospace, monospace;
}

html { background: var(--site-theme-color); color: var(--ink); font-family: var(--site-font-sans); }
```

**Step 6: Import fonts in BaseLayout**

In `src/layouts/BaseLayout.astro`, top-of-file script frontmatter, add:
```ts
import '@fontsource-variable/geist';
import '@fontsource-variable/geist-mono';
```

**Step 7: Verify build**

```bash
pnpm build
```
Expected: build succeeds with no errors. Inspect `dist/index.html` briefly — check `<meta name="theme-color" content="#fffdf8">`.

**Step 8: Commit**

```bash
git add src/config/site.config.ts src/styles/global.css src/layouts/BaseLayout.astro tests/branding.test.ts
git commit -m "feat(brand): apply coral-on-cream palette and Geist fonts"
```

---

### Task 3: Create the "squish" mascot SVG

**Objective:** Inline SVG icon (~1KB) used for logo, favicon, and OG image default.

**Files:**
- Create: `src/components/SquishIcon.astro`
- Create: `public/favicon.svg`
- Create: `public/og-default.svg` (will be converted to PNG in Task 6)

**Step 1: Create `src/components/SquishIcon.astro`**

```astro
---
interface Props {
  size?: number;
  class?: string;
}
const { size = 24, class: className } = Astro.props;
---
<svg
  xmlns="http://www.w3.org/2000/svg"
  width={size}
  height={size}
  viewBox="0 0 24 24"
  fill="none"
  stroke="currentColor"
  stroke-width="2.4"
  stroke-linecap="round"
  stroke-linejoin="round"
  class={className}
  aria-hidden="true"
>
  <!-- Two curved lines suggesting vertical compression. -->
  <path d="M4 7 C 8 4, 16 4, 20 7" />
  <path d="M4 17 C 8 20, 16 20, 20 17" />
  <!-- A small dot in the middle as the "squished" subject. -->
  <circle cx="12" cy="12" r="2" fill="currentColor" stroke="none" />
</svg>
```

**Step 2: Create `public/favicon.svg`** (same SVG, hardcoded coral color for favicon)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#ff6b52" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
  <path d="M4 7 C 8 4, 16 4, 20 7"/>
  <path d="M4 17 C 8 20, 16 20, 20 17"/>
  <circle cx="12" cy="12" r="2" fill="#ff6b52" stroke="none"/>
</svg>
```

**Step 3: Verify**

```bash
pnpm build
ls -la dist/favicon.svg
```
Expected: file exists and is < 500 bytes.

**Step 4: Commit**

```bash
git add src/components/SquishIcon.astro public/favicon.svg
git commit -m "feat(brand): add squish mascot SVG + favicon"
```

---

### Task 4: Update Header and Footer with brand

**Objective:** Header shows the squish icon + logoText; Footer has plain, warm copy.

**Files:**
- Modify: `src/components/Header.astro`
- Modify: `src/components/Footer.astro`

**Step 1: Update Header**

Replace the contents of `src/components/Header.astro` with:
```astro
---
import { siteConfig } from '../config/site.config';
import SquishIcon from './SquishIcon.astro';
---
<header class="sticky top-0 z-40 border-b border-[var(--border)] bg-[var(--site-theme-color)]/90 backdrop-blur">
  <div class="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
    <a href="/" class="flex items-center gap-2 font-semibold text-[var(--ink)] no-underline">
      <SquishIcon size={22} class="text-[var(--site-accent-color)]" />
      <span>{siteConfig.branding.logoText}</span>
    </a>
    <nav aria-label="Primary">
      <ul class="flex gap-4 text-sm">
        {siteConfig.nav.primary.map((link) => (
          <li><a href={link.href} class="text-[var(--muted)] hover:text-[var(--ink)]">{link.label}</a></li>
        ))}
      </ul>
    </nav>
  </div>
</header>
```

**Step 2: Update Footer**

Replace the contents of `src/components/Footer.astro` with:
```astro
---
import { siteConfig } from '../config/site.config';
const year = new Date().getFullYear();
---
<footer class="mt-16 border-t border-[var(--border)] bg-[var(--surface)]">
  <div class="mx-auto max-w-5xl px-4 py-8 text-sm text-[var(--muted)]">
    <p>
      Your photos. Smaller. Squished in your browser — no uploads, ever.
    </p>
    <div class="mt-4 flex flex-wrap gap-4">
      <a href="/about/" class="hover:text-[var(--ink)]">About</a>
      <a href="/contact/" class="hover:text-[var(--ink)]">Contact</a>
      <a href="/privacy/" class="hover:text-[var(--ink)]">Privacy</a>
      <a href="/terms/" class="hover:text-[var(--ink)]">Terms</a>
      <a href="/sponsored/" class="hover:text-[var(--ink)]">Sponsored</a>
    </div>
    <p class="mt-4">© {year} {siteConfig.branding.logoText}</p>
  </div>
</footer>
```

**Step 3: Verify build**

```bash
pnpm build
```
Expected: succeeds. Spot-check `dist/index.html` — should contain `makepicsmall` and the SVG markup.

**Step 4: Commit**

```bash
git add src/components/Header.astro src/components/Footer.astro
git commit -m "feat(brand): warm header/footer with squish mascot"
```

---

### Task 5: Update BaseLayout default title and meta

**Objective:** Ensure the placeholder tokens (`__SITE_NAME__`, etc.) from the template are now driven by siteConfig, not left as literals.

**Files:**
- Modify: `src/layouts/BaseLayout.astro`

**Step 1: Read the current layout**

```bash
cat src/layouts/BaseLayout.astro | head -80
```

Check whether it reads from `siteConfig` for title/description/domain. If any literals remain (`__SITE_NAME__`, `__SITE_DOMAIN__`, `__SITE_DESCRIPTION__`), replace them with interpolated `siteConfig.identity.*` values.

**Step 2: Write a build-output smoke test**

Create `tests/base-layout.test.ts`:
```ts
import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';

describe('baseLayout build output', () => {
  it('renders siteConfig values, not placeholder tokens', () => {
    if (!existsSync('dist/index.html')) {
      execSync('pnpm build', { stdio: 'ignore' });
    }
    const html = readFileSync('dist/index.html', 'utf8');
    expect(html).not.toMatch(/__SITE_[A-Z_]+__/);
    expect(html).toContain('makepicsmall');
    expect(html).toContain('Free, instant image compression');
  });
});
```

**Step 3: Run — expect FAIL if placeholders remain**

```bash
pnpm test:run tests/base-layout.test.ts
```

If FAIL: find and replace every `__SITE_NAME__` → `{siteConfig.identity.name}`, `__SITE_DESCRIPTION__` → `{siteConfig.identity.description}`, `__SITE_DOMAIN__`/`__site_domain__` → `{siteConfig.identity.domain}` in `BaseLayout.astro`. Re-run build then test.

**Step 4: Commit**

```bash
git add src/layouts/BaseLayout.astro tests/base-layout.test.ts
git commit -m "fix(template): wire BaseLayout to siteConfig (remove placeholders)"
```

---

### Task 6: Generate static OG image

**Objective:** Create a 1200×630 coral-on-cream OG image with icon + site name. Static PNG, committed.

**Files:**
- Create: `public/og-default.png`
- Create: `scripts/generate-og.mjs` (one-shot, not run at build time)

**Step 1: Create the generator script**

Create `scripts/generate-og.mjs`:
```js
import { createCanvas, registerFont } from '@napi-rs/canvas';
import { writeFileSync } from 'fs';

const W = 1200, H = 630;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background
ctx.fillStyle = '#fffdf8';
ctx.fillRect(0, 0, W, H);

// Coral accent band at top
ctx.fillStyle = '#ff6b52';
ctx.fillRect(0, 0, W, 8);

// Title
ctx.fillStyle = '#1a1a1a';
ctx.font = 'bold 96px sans-serif';
ctx.fillText('makepicsmall', 80, 300);

// Subtitle
ctx.fillStyle = '#5a5a5a';
ctx.font = '42px sans-serif';
ctx.fillText('Your photos. Smaller. Squished in your browser.', 80, 380);

// Domain
ctx.fillStyle = '#ff6b52';
ctx.font = '28px sans-serif';
ctx.fillText('makepicsmall.com', 80, 550);

writeFileSync('public/og-default.png', canvas.toBuffer('image/png'));
console.log('Wrote public/og-default.png');
```

**Step 2: Install `@napi-rs/canvas` as dev dep and run**

```bash
pnpm add -D @napi-rs/canvas
node scripts/generate-og.mjs
```

Expected: `public/og-default.png` exists, ~30–80 KB.

**Step 3: Verify in build**

```bash
pnpm build
ls -la dist/og-default.png
```

**Step 4: Commit**

```bash
git add public/og-default.png scripts/generate-og.mjs package.json pnpm-lock.yaml
git commit -m "feat(brand): generate static OG image"
```

---

## Phase B — Preset engine & worker pool (tasks 7–14)

### Task 7: Define the Preset type and URL presets table

**Objective:** Single source of truth for every tool URL's compression preset.

**Files:**
- Create: `src/config/presets.ts`
- Create: `tests/presets.test.ts`

**Step 1: Write failing test**

```ts
// tests/presets.test.ts
import { describe, it, expect } from 'vitest';
import { PRESETS, getPresetByUrl, type Preset } from '../src/config/presets';

describe('presets', () => {
  it('has an entry for every MVP tool URL', () => {
    const expected = [
      '/', '/compress/jpg', '/compress/png', '/compress/webp',
      '/compress/jpg/to/100kb', '/compress/jpg/to/500kb', '/compress/png/to/100kb',
      '/to/50kb', '/to/100kb', '/to/500kb', '/to/1mb',
      '/for/whatsapp', '/for/whatsapp-dp', '/for/instagram', '/for/instagram-story',
      '/for/resume', '/for/passport-us', '/for/passport-canada', '/for/passport-uk',
      '/for/linkedin',
    ];
    for (const url of expected) {
      expect(PRESETS[url], `Missing preset: ${url}`).toBeDefined();
    }
    expect(Object.keys(PRESETS).length).toBe(20);
  });

  it('passport-us requires square 600x600 JPG ≤240KB', () => {
    const p = PRESETS['/for/passport-us'];
    expect(p.format).toBe('jpg');
    expect(p.targetKB).toBe(240);
    expect(p.lockDimensions).toEqual({ w: 600, h: 600 });
  });

  it('whatsapp-dp is 640x640 JPG ≤100KB', () => {
    const p = PRESETS['/for/whatsapp-dp'];
    expect(p.lockDimensions).toEqual({ w: 640, h: 640 });
    expect(p.targetKB).toBe(100);
  });

  it('getPresetByUrl returns preset or default for unknown URL', () => {
    expect(getPresetByUrl('/for/passport-us').targetKB).toBe(240);
    expect(getPresetByUrl('/unknown-url')).toEqual(PRESETS['/']);
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test:run tests/presets.test.ts
```

**Step 3: Create `src/config/presets.ts`**

```ts
export type Format = 'jpg' | 'png' | 'webp' | 'auto';

export interface Preset {
  /** Output format. 'auto' preserves input format. */
  format: Format;
  /** Hard target size in KB. If set, triggers quality binary search. */
  targetKB?: number;
  /** Initial quality 1-100. Default 80. */
  initialQuality?: number;
  /** If set, downscale so longest side ≤ this value (px). */
  maxLongSide?: number;
  /** If set, center-crop and resize to these exact dimensions. */
  lockDimensions?: { w: number; h: number };
  /** Short human-readable label for UI. */
  label?: string;
}

/**
 * URL → Preset mapping. Must stay in sync with the routes we ship.
 * When adding a new URL, also add a page file under src/pages/.
 */
export const PRESETS: Record<string, Preset> = {
  '/': { format: 'auto', label: 'Compress any image' },

  '/compress/jpg': { format: 'jpg', label: 'Compress JPG' },
  '/compress/png': { format: 'png', label: 'Compress PNG' },
  '/compress/webp': { format: 'webp', label: 'Compress WebP' },

  '/compress/jpg/to/100kb': { format: 'jpg', targetKB: 100, label: 'Compress JPG to 100 KB' },
  '/compress/jpg/to/500kb': { format: 'jpg', targetKB: 500, label: 'Compress JPG to 500 KB' },
  '/compress/png/to/100kb': { format: 'png', targetKB: 100, label: 'Compress PNG to 100 KB' },

  '/to/50kb':  { format: 'auto', targetKB: 50,   label: 'Compress to 50 KB' },
  '/to/100kb': { format: 'auto', targetKB: 100,  label: 'Compress to 100 KB' },
  '/to/500kb': { format: 'auto', targetKB: 500,  label: 'Compress to 500 KB' },
  '/to/1mb':   { format: 'auto', targetKB: 1000, label: 'Compress to 1 MB' },

  '/for/whatsapp':         { format: 'jpg', targetKB: 1500, maxLongSide: 1600, label: 'For WhatsApp (full quality)' },
  '/for/whatsapp-dp':      { format: 'jpg', targetKB: 100,  lockDimensions: { w: 640, h: 640 },   label: 'For WhatsApp DP' },
  '/for/instagram':        { format: 'jpg', targetKB: 500,  maxLongSide: 1080, label: 'For Instagram' },
  '/for/instagram-story':  { format: 'jpg', targetKB: 600,  lockDimensions: { w: 1080, h: 1920 }, label: 'For Instagram Story' },
  '/for/resume':           { format: 'jpg', targetKB: 100,  lockDimensions: { w: 600, h: 600 },   label: 'For Resume Photo' },
  '/for/passport-us':      { format: 'jpg', targetKB: 240,  lockDimensions: { w: 600, h: 600 },   label: 'For US Passport Photo' },
  '/for/passport-canada':  { format: 'jpg', targetKB: 240,  lockDimensions: { w: 420, h: 540 },   label: 'For Canadian Passport Photo' },
  '/for/passport-uk':      { format: 'jpg', targetKB: 1000, lockDimensions: { w: 600, h: 750 },   label: 'For UK Passport Photo' },
  '/for/linkedin':         { format: 'jpg', targetKB: 200,  lockDimensions: { w: 400, h: 400 },   label: 'For LinkedIn Profile' },
};

export function getPresetByUrl(url: string): Preset {
  // Strip trailing slash unless it's root
  const normalized = url === '/' ? url : url.replace(/\/$/, '');
  return PRESETS[normalized] ?? PRESETS['/'];
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test:run tests/presets.test.ts
```
Expected: 4 tests PASS.

**Step 5: Commit**

```bash
git add src/config/presets.ts tests/presets.test.ts
git commit -m "feat(presets): define URL→Preset table for 20 tool routes"
```

---

### Task 8: Format detection helper

**Objective:** Given a File or Blob, return the detected format ('jpg' | 'png' | 'webp' | 'unsupported').

**Files:**
- Create: `src/lib/detect-format.ts`
- Create: `tests/detect-format.test.ts`
- Create: `tests/fixtures/tiny-jpg.jpg` (minimal 2×2 JPG), `tiny-png.png`, `tiny-webp.webp`

**Step 1: Create fixtures**

```bash
mkdir -p tests/fixtures
# Minimal valid JPG (~400 bytes, 2x2 white)
printf '\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00\xff\xdb\x00\x43\x00' > tests/fixtures/tiny-jpg.jpg
# Truncate-but-enough for magic-byte detection. Simpler: copy real tiny fixtures later.
```

Better approach — generate them from the canvas lib we already added:

Create `scripts/generate-fixtures.mjs`:
```js
import { createCanvas } from '@napi-rs/canvas';
import { writeFileSync } from 'fs';

const c = createCanvas(2, 2);
const ctx = c.getContext('2d');
ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 2, 2);
writeFileSync('tests/fixtures/tiny-jpg.jpg', c.toBuffer('image/jpeg'));
writeFileSync('tests/fixtures/tiny-png.png', c.toBuffer('image/png'));
writeFileSync('tests/fixtures/tiny-webp.webp', c.toBuffer('image/webp'));
console.log('Fixtures generated.');
```

Run:
```bash
node scripts/generate-fixtures.mjs
```

**Step 2: Write failing test**

```ts
// tests/detect-format.test.ts
import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { detectFormat } from '../src/lib/detect-format';

function loadAsBlob(path: string, mime: string): Blob {
  const buf = readFileSync(path);
  return new Blob([buf], { type: mime });
}

describe('detectFormat', () => {
  it('detects JPG by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-jpg.jpg', 'image/jpeg');
    expect(await detectFormat(b)).toBe('jpg');
  });
  it('detects PNG by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-png.png', 'image/png');
    expect(await detectFormat(b)).toBe('png');
  });
  it('detects WebP by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-webp.webp', 'image/webp');
    expect(await detectFormat(b)).toBe('webp');
  });
  it('returns unsupported for a text blob', async () => {
    const b = new Blob(['hello world'], { type: 'text/plain' });
    expect(await detectFormat(b)).toBe('unsupported');
  });
});
```

**Step 3: Run — expect FAIL**

```bash
pnpm test:run tests/detect-format.test.ts
```

**Step 4: Implement**

Create `src/lib/detect-format.ts`:
```ts
export type DetectedFormat = 'jpg' | 'png' | 'webp' | 'unsupported';

export async function detectFormat(blob: Blob): Promise<DetectedFormat> {
  const header = new Uint8Array(await blob.slice(0, 12).arrayBuffer());
  // JPEG: FF D8 FF
  if (header[0] === 0xff && header[1] === 0xd8 && header[2] === 0xff) return 'jpg';
  // PNG: 89 50 4E 47 0D 0A 1A 0A
  if (header[0] === 0x89 && header[1] === 0x50 && header[2] === 0x4e && header[3] === 0x47) return 'png';
  // WebP: 'RIFF....WEBP'
  if (
    header[0] === 0x52 && header[1] === 0x49 && header[2] === 0x46 && header[3] === 0x46 &&
    header[8] === 0x57 && header[9] === 0x45 && header[10] === 0x42 && header[11] === 0x50
  ) return 'webp';
  return 'unsupported';
}
```

**Step 5: Run — expect PASS**

```bash
pnpm test:run tests/detect-format.test.ts
```
Expected: 4 PASS.

**Step 6: Add vitest config for jsdom env**

Create `vitest.config.ts`:
```ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'jsdom',
    globals: false,
    include: ['tests/**/*.test.ts'],
  },
});
```

**Step 7: Commit**

```bash
git add src/lib/detect-format.ts tests/detect-format.test.ts tests/fixtures/ scripts/generate-fixtures.mjs vitest.config.ts
git commit -m "feat(lib): detect image format by magic bytes"
```

---

### Task 9: Quality-to-target-size binary search utility

**Objective:** Pure function (no WASM involved) — given an encoder callback and a target KB, find the optimal quality.

**Files:**
- Create: `src/lib/target-search.ts`
- Create: `tests/target-search.test.ts`

**Step 1: Write failing test**

```ts
// tests/target-search.test.ts
import { describe, it, expect } from 'vitest';
import { searchQualityForTarget } from '../src/lib/target-search';

describe('searchQualityForTarget', () => {
  // Simulated encoder: higher quality = bigger output. linear model for test.
  const fakeEncoder = async (quality: number) => {
    // bytes = quality * 1024 (so quality 50 = 50KB, quality 100 = 100KB)
    return new Uint8Array(quality * 1024);
  };

  it('finds quality within 5% of 50KB target', async () => {
    const { quality, size, hitTarget } = await searchQualityForTarget({
      targetKB: 50,
      encode: fakeEncoder,
      tolerancePct: 5,
      maxIterations: 8,
    });
    expect(quality).toBeGreaterThanOrEqual(47);
    expect(quality).toBeLessThanOrEqual(53);
    expect(hitTarget).toBe(true);
    expect(size).toBeGreaterThan(0);
  });

  it('caps iterations and returns best result if unreachable', async () => {
    // target 200KB but encoder max is 100KB (quality 100)
    const { quality, size, hitTarget, attempts } = await searchQualityForTarget({
      targetKB: 200,
      encode: fakeEncoder,
      tolerancePct: 5,
      maxIterations: 8,
    });
    expect(attempts).toBeLessThanOrEqual(8);
    expect(quality).toBe(95);
    expect(hitTarget).toBe(false);
  });

  it('never goes below floor or above ceiling', async () => {
    const { quality } = await searchQualityForTarget({
      targetKB: 1, // impossibly small
      encode: fakeEncoder,
      qualityFloor: 20,
      qualityCeiling: 95,
      maxIterations: 8,
    });
    expect(quality).toBeGreaterThanOrEqual(20);
    expect(quality).toBeLessThanOrEqual(95);
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test:run tests/target-search.test.ts
```

**Step 3: Implement**

Create `src/lib/target-search.ts`:
```ts
export interface TargetSearchOptions {
  targetKB: number;
  encode: (quality: number) => Promise<Uint8Array>;
  qualityFloor?: number;
  qualityCeiling?: number;
  tolerancePct?: number;
  maxIterations?: number;
  initialQuality?: number;
}

export interface TargetSearchResult {
  quality: number;
  bytes: Uint8Array;
  size: number;
  hitTarget: boolean;
  attempts: number;
}

/**
 * Binary-search for the highest quality value whose encoded output is
 * within `tolerancePct` of `targetKB`. If unreachable, returns the
 * encoded result closest to target (capped at ceiling/floor).
 */
export async function searchQualityForTarget(opts: TargetSearchOptions): Promise<TargetSearchResult> {
  const {
    targetKB,
    encode,
    qualityFloor = 20,
    qualityCeiling = 95,
    tolerancePct = 5,
    maxIterations = 8,
    initialQuality = 80,
  } = opts;

  const targetBytes = targetKB * 1024;
  const toleranceBytes = targetBytes * (tolerancePct / 100);

  let lo = qualityFloor;
  let hi = qualityCeiling;
  let bestBytes: Uint8Array | null = null;
  let bestQuality = initialQuality;
  let bestDelta = Infinity;
  let attempts = 0;
  let q = Math.min(Math.max(initialQuality, qualityFloor), qualityCeiling);

  while (attempts < maxIterations && lo <= hi) {
    attempts++;
    const bytes = await encode(q);
    const size = bytes.byteLength;
    const delta = Math.abs(size - targetBytes);
    if (delta < bestDelta) {
      bestDelta = delta;
      bestBytes = bytes;
      bestQuality = q;
    }
    if (delta <= toleranceBytes) break;
    if (size > targetBytes) hi = q - 1;
    else lo = q + 1;
    q = Math.round((lo + hi) / 2);
  }

  const finalBytes = bestBytes ?? new Uint8Array();
  const size = finalBytes.byteLength;
  const hitTarget = Math.abs(size - targetBytes) <= toleranceBytes;
  return { quality: bestQuality, bytes: finalBytes, size, hitTarget, attempts };
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test:run tests/target-search.test.ts
```

**Step 5: Commit**

```bash
git add src/lib/target-search.ts tests/target-search.test.ts
git commit -m "feat(lib): binary-search quality for target file size"
```

---

### Task 10: Canvas preprocessor (downscale + lock-dimensions)

**Objective:** Given an ImageBitmap and a preset, return a canvas with the transformed pixels ready for encoding.

**Files:**
- Create: `src/lib/preprocess.ts`
- Create: `tests/preprocess.test.ts`

**Step 1: Write failing test**

```ts
// tests/preprocess.test.ts
import { describe, it, expect } from 'vitest';
import { preprocess, computeOutputDims } from '../src/lib/preprocess';

describe('computeOutputDims', () => {
  it('passes through when no constraints', () => {
    expect(computeOutputDims(1000, 800, {})).toEqual({ w: 1000, h: 800, cropSrc: null });
  });
  it('downscales by maxLongSide preserving aspect', () => {
    expect(computeOutputDims(4000, 3000, { maxLongSide: 1080 })).toEqual({
      w: 1080, h: 810, cropSrc: null,
    });
  });
  it('no upscale when image already smaller than maxLongSide', () => {
    expect(computeOutputDims(800, 600, { maxLongSide: 1080 })).toEqual({
      w: 800, h: 600, cropSrc: null,
    });
  });
  it('center-crops then resizes for lockDimensions (square from wide)', () => {
    // 1200x800 -> 600x600: crop to 800x800 centered, resize to 600x600
    const r = computeOutputDims(1200, 800, { lockDimensions: { w: 600, h: 600 } });
    expect(r.w).toBe(600);
    expect(r.h).toBe(600);
    expect(r.cropSrc).toEqual({ x: 200, y: 0, w: 800, h: 800 });
  });
  it('center-crops to portrait lock (420x540 from square)', () => {
    const r = computeOutputDims(1000, 1000, { lockDimensions: { w: 420, h: 540 } });
    expect(r.w).toBe(420);
    expect(r.h).toBe(540);
    // aspect 420/540 = 0.777..., source square → keep full width, crop height? no — we're locking a taller ratio from a square source, so crop WIDTH.
    // target aspect = 420/540 = 0.7778 (portrait). source square (1:1) is wider than target. so crop horizontal.
    // desired source width = 1000 * (420/540) = 777.78 → round to 778
    expect(r.cropSrc?.w).toBe(778);
    expect(r.cropSrc?.h).toBe(1000);
    expect(r.cropSrc?.x).toBe(111); // (1000-778)/2
    expect(r.cropSrc?.y).toBe(0);
  });
});
```

**Step 2: Run — expect FAIL**

**Step 3: Implement**

Create `src/lib/preprocess.ts`:
```ts
import type { Preset } from '../config/presets';

export interface OutputDims {
  w: number;
  h: number;
  cropSrc: { x: number; y: number; w: number; h: number } | null;
}

export function computeOutputDims(
  srcW: number,
  srcH: number,
  preset: Pick<Preset, 'maxLongSide' | 'lockDimensions'>,
): OutputDims {
  if (preset.lockDimensions) {
    const tgtAspect = preset.lockDimensions.w / preset.lockDimensions.h;
    const srcAspect = srcW / srcH;
    let cropW: number, cropH: number, x: number, y: number;
    if (srcAspect > tgtAspect) {
      // source wider than target → crop horizontally
      cropH = srcH;
      cropW = Math.round(srcH * tgtAspect);
      x = Math.round((srcW - cropW) / 2);
      y = 0;
    } else if (srcAspect < tgtAspect) {
      // source taller than target → crop vertically
      cropW = srcW;
      cropH = Math.round(srcW / tgtAspect);
      x = 0;
      y = Math.round((srcH - cropH) / 2);
    } else {
      // same aspect, no crop
      cropW = srcW; cropH = srcH; x = 0; y = 0;
    }
    return {
      w: preset.lockDimensions.w,
      h: preset.lockDimensions.h,
      cropSrc: { x, y, w: cropW, h: cropH },
    };
  }

  if (preset.maxLongSide) {
    const long = Math.max(srcW, srcH);
    if (long > preset.maxLongSide) {
      const scale = preset.maxLongSide / long;
      return {
        w: Math.round(srcW * scale),
        h: Math.round(srcH * scale),
        cropSrc: null,
      };
    }
  }

  return { w: srcW, h: srcH, cropSrc: null };
}

/** Browser-only. Takes ImageBitmap, returns an ImageData ready for encoder. */
export function preprocess(
  bitmap: ImageBitmap,
  preset: Preset,
): ImageData {
  const dims = computeOutputDims(bitmap.width, bitmap.height, preset);
  const canvas = new OffscreenCanvas(dims.w, dims.h);
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Could not get 2D context');

  if (dims.cropSrc) {
    ctx.drawImage(
      bitmap,
      dims.cropSrc.x, dims.cropSrc.y, dims.cropSrc.w, dims.cropSrc.h,
      0, 0, dims.w, dims.h,
    );
  } else {
    ctx.drawImage(bitmap, 0, 0, dims.w, dims.h);
  }

  return ctx.getImageData(0, 0, dims.w, dims.h);
}
```

**Step 4: Run — expect PASS** (only the `computeOutputDims` tests run; `preprocess` is browser-only and skipped in node).

**Step 5: Commit**

```bash
git add src/lib/preprocess.ts tests/preprocess.test.ts
git commit -m "feat(lib): crop/downscale preprocessor for preset constraints"
```

---

### Task 11: Single-file compression pipeline (main thread version)

**Objective:** Glue format-detect + preprocess + encode + optional target-search into one async function. Runs on the main thread for MVP simplicity; workers come in Task 12.

**Files:**
- Create: `src/lib/compress.ts`
- Create: `tests/compress-integration.test.ts`

**Step 1: Create `src/lib/compress.ts`**

```ts
import type { Preset } from '../config/presets';
import { detectFormat, type DetectedFormat } from './detect-format';
import { computeOutputDims } from './preprocess';
import { searchQualityForTarget } from './target-search';

export interface CompressInput {
  file: File;
  preset: Preset;
}

export interface CompressResult {
  format: DetectedFormat;
  originalSize: number;
  compressedSize: number;
  quality: number;
  blob: Blob;
  elapsedMs: number;
  hitTarget: boolean;
  attempts: number;
}

export async function compressOne(input: CompressInput): Promise<CompressResult> {
  const t0 = performance.now();
  const inputFormat = await detectFormat(input.file);
  if (inputFormat === 'unsupported') throw new Error('Unsupported file format');

  const outputFormat = input.preset.format === 'auto' ? inputFormat : input.preset.format;

  const bitmap = await createImageBitmap(input.file);
  const dims = computeOutputDims(bitmap.width, bitmap.height, input.preset);
  const canvas = new OffscreenCanvas(dims.w, dims.h);
  const ctx = canvas.getContext('2d')!;
  if (dims.cropSrc) {
    ctx.drawImage(bitmap, dims.cropSrc.x, dims.cropSrc.y, dims.cropSrc.w, dims.cropSrc.h, 0, 0, dims.w, dims.h);
  } else {
    ctx.drawImage(bitmap, 0, 0, dims.w, dims.h);
  }
  const imageData = ctx.getImageData(0, 0, dims.w, dims.h);

  const encode = async (quality: number): Promise<Uint8Array> => {
    if (outputFormat === 'jpg') {
      const m = await import('@jsquash/jpeg');
      return new Uint8Array(await m.encode(imageData, { quality }));
    }
    if (outputFormat === 'webp') {
      const m = await import('@jsquash/webp');
      return new Uint8Array(await m.encode(imageData, { quality }));
    }
    if (outputFormat === 'png') {
      const m = await import('@jsquash/png');
      // oxipng doesn't take a quality integer; map quality to optimization level (2-6)
      const level = Math.max(2, Math.min(6, Math.round((quality / 100) * 6)));
      const encoded = await m.encode(imageData);
      const optimized = await m.optimise(encoded, { level });
      return new Uint8Array(optimized);
    }
    throw new Error(`Unsupported output format: ${outputFormat}`);
  };

  let bytes: Uint8Array;
  let quality = input.preset.initialQuality ?? 80;
  let hitTarget = true;
  let attempts = 1;

  if (input.preset.targetKB) {
    const result = await searchQualityForTarget({
      targetKB: input.preset.targetKB,
      encode,
      initialQuality: quality,
    });
    bytes = result.bytes;
    quality = result.quality;
    hitTarget = result.hitTarget;
    attempts = result.attempts;
  } else {
    bytes = await encode(quality);
  }

  const mime = outputFormat === 'jpg' ? 'image/jpeg' : outputFormat === 'png' ? 'image/png' : 'image/webp';
  // Blob requires BlobPart; pass the ArrayBuffer slice.
  const blob = new Blob([bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer], { type: mime });

  return {
    format: outputFormat as DetectedFormat,
    originalSize: input.file.size,
    compressedSize: blob.size,
    quality,
    blob,
    elapsedMs: performance.now() - t0,
    hitTarget,
    attempts,
  };
}
```

**Step 2: Integration test (browser-only, so skip for this task — we'll test via Playwright in Phase E)**

For node-level verification, just ensure the file type-checks:
```bash
pnpm astro check
```
Expected: 0 errors.

**Step 3: Commit**

```bash
git add src/lib/compress.ts
git commit -m "feat(lib): single-file compress pipeline (main thread)"
```

---

### Task 12: Worker implementation

**Objective:** Move compression to a Web Worker so the UI stays responsive.

**Files:**
- Create: `src/workers/compress.worker.ts`
- Modify: `src/lib/compress.ts` (add worker-based alternative)

**Step 1: Create worker**

Create `src/workers/compress.worker.ts`:
```ts
import { compressOne, type CompressInput } from '../lib/compress';

self.addEventListener('message', async (event: MessageEvent<{ id: string; input: CompressInput }>) => {
  const { id, input } = event.data;
  try {
    const result = await compressOne(input);
    (self as unknown as DedicatedWorkerGlobalScope).postMessage({ id, ok: true, result });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    (self as unknown as DedicatedWorkerGlobalScope).postMessage({ id, ok: false, error: message });
  }
});

export {};
```

**Step 2: Verify build recognizes the worker**

```bash
pnpm astro check
```

**Step 3: Commit**

```bash
git add src/workers/compress.worker.ts
git commit -m "feat(worker): compress worker entry"
```

---

### Task 13: Worker pool

**Objective:** Manage up to 3 compression workers with a queue.

**Files:**
- Create: `src/lib/worker-pool.ts`
- Create: `tests/worker-pool.test.ts` (uses fake worker class, tests scheduling logic only)

**Step 1: Write failing test**

```ts
// tests/worker-pool.test.ts
import { describe, it, expect, vi } from 'vitest';
import { WorkerPool, type PoolJob } from '../src/lib/worker-pool';

// Fake worker that "completes" after microtask delay.
class FakeWorker {
  onmessage: ((ev: MessageEvent) => void) | null = null;
  postMessage(data: { id: string }) {
    queueMicrotask(() => {
      this.onmessage?.(new MessageEvent('message', { data: { id: data.id, ok: true, result: { fake: true } } }));
    });
  }
  terminate() {}
}

describe('WorkerPool', () => {
  it('runs jobs up to pool size concurrently', async () => {
    const pool = new WorkerPool({
      size: 2,
      createWorker: () => new FakeWorker() as unknown as Worker,
    });
    const jobs: PoolJob[] = [
      { id: '1', input: {} as never },
      { id: '2', input: {} as never },
      { id: '3', input: {} as never },
    ];
    const results = await Promise.all(jobs.map(j => pool.run(j)));
    expect(results.length).toBe(3);
    for (const r of results) expect(r.ok).toBe(true);
    pool.destroy();
  });

  it('caps concurrency at size', async () => {
    const order: string[] = [];
    class SlowWorker {
      onmessage: ((ev: MessageEvent) => void) | null = null;
      postMessage(data: { id: string }) {
        order.push(`start-${data.id}`);
        setTimeout(() => {
          order.push(`end-${data.id}`);
          this.onmessage?.(new MessageEvent('message', { data: { id: data.id, ok: true, result: {} } }));
        }, 10);
      }
      terminate() {}
    }
    const pool = new WorkerPool({ size: 1, createWorker: () => new SlowWorker() as unknown as Worker });
    await Promise.all([
      pool.run({ id: 'a', input: {} as never }),
      pool.run({ id: 'b', input: {} as never }),
    ]);
    // Strictly sequential: a-start, a-end, b-start, b-end
    expect(order).toEqual(['start-a', 'end-a', 'start-b', 'end-b']);
    pool.destroy();
  });
});
```

**Step 2: Run — expect FAIL**

**Step 3: Implement**

Create `src/lib/worker-pool.ts`:
```ts
import type { CompressInput, CompressResult } from './compress';

export interface PoolJob {
  id: string;
  input: CompressInput;
}

export interface PoolResult {
  id: string;
  ok: boolean;
  result?: CompressResult;
  error?: string;
}

interface PendingJob {
  job: PoolJob;
  resolve: (r: PoolResult) => void;
}

export interface WorkerPoolOptions {
  size: number;
  createWorker: () => Worker;
}

interface Slot {
  worker: Worker;
  busy: boolean;
}

export class WorkerPool {
  private slots: Slot[];
  private queue: PendingJob[] = [];
  private pending = new Map<string, (r: PoolResult) => void>();

  constructor(opts: WorkerPoolOptions) {
    this.slots = Array.from({ length: opts.size }, () => {
      const worker = opts.createWorker();
      worker.onmessage = (ev: MessageEvent<PoolResult>) => this.onWorkerMessage(ev.data, worker);
      return { worker, busy: false };
    });
  }

  run(job: PoolJob): Promise<PoolResult> {
    return new Promise((resolve) => {
      const free = this.slots.find((s) => !s.busy);
      if (free) {
        free.busy = true;
        this.dispatch(free, { job, resolve });
      } else {
        this.queue.push({ job, resolve });
      }
    });
  }

  destroy(): void {
    for (const s of this.slots) s.worker.terminate();
    this.slots = [];
    this.queue = [];
    this.pending.clear();
  }

  private dispatch(slot: Slot, pending: PendingJob): void {
    this.pending.set(pending.job.id, pending.resolve);
    slot.worker.postMessage({ id: pending.job.id, input: pending.job.input });
  }

  private onWorkerMessage(data: PoolResult, worker: Worker): void {
    const resolve = this.pending.get(data.id);
    this.pending.delete(data.id);
    resolve?.(data);
    // Free this worker's slot, take next from queue.
    const slot = this.slots.find((s) => s.worker === worker);
    if (!slot) return;
    const next = this.queue.shift();
    if (next) this.dispatch(slot, next);
    else slot.busy = false;
  }
}

export function computePoolSize(): number {
  const cores = (typeof navigator !== 'undefined' && navigator.hardwareConcurrency) || 2;
  return Math.min(3, Math.max(1, cores));
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test:run tests/worker-pool.test.ts
```

**Step 5: Commit**

```bash
git add src/lib/worker-pool.ts tests/worker-pool.test.ts
git commit -m "feat(lib): worker pool with FIFO queue, cap 3"
```

---

### Task 14: Run the full test suite; checkpoint

**Objective:** Verify all Phase B tests pass together; no regressions.

**Step 1: Run everything**

```bash
cd ~/site-network/sites/makepicsmall.com
pnpm test:run
pnpm astro check
pnpm build
```

Expected:
- Vitest: 5 test files, ~14 tests total, all PASS
- astro check: 0 errors
- build: succeeds

**Step 2: Commit checkpoint (no code change — just a tag)**

```bash
git tag phase-b-complete
git log --oneline | head -15
```

---

## Phase C — Compressor UI island (tasks 15–18)

### Task 15: Drop zone component (static, no logic)

**Objective:** The pure-UI drop area users see above the fold. Accepts preset as prop.

**Files:**
- Create: `src/components/tool/DropZone.tsx` (Preact component — TSX)

**Step 1: Write failing test**

```tsx
// tests/components/DropZone.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/preact';
import { DropZone } from '../../src/components/tool/DropZone';

describe('DropZone', () => {
  it('renders with preset label', () => {
    render(<DropZone preset={{ format: 'jpg', targetKB: 100, label: 'Compress JPG to 100 KB' }} onFiles={() => {}} />);
    expect(screen.getByText(/compress jpg to 100 kb/i)).toBeTruthy();
  });
  it('shows the accepted formats hint', () => {
    render(<DropZone preset={{ format: 'auto' }} onFiles={() => {}} />);
    expect(screen.getByText(/jpg, png, webp/i)).toBeTruthy();
  });
});
```

**Step 2: Run — expect FAIL**

**Step 3: Add `jest-dom` assertion-friendly types (Preact Testing Library ships this)**

Not needed — testing-library exports `screen` which returns elements that can be checked with `.toBeTruthy()`.

**Step 4: Implement**

Create `src/components/tool/DropZone.tsx`:
```tsx
/** @jsxImportSource preact */
import { useCallback, useRef, useState } from 'preact/hooks';
import type { Preset } from '../../config/presets';

interface Props {
  preset: Preset;
  onFiles: (files: File[]) => void;
}

export function DropZone({ preset, onFiles }: Props) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const files = Array.from(e.dataTransfer?.files ?? []);
    if (files.length) onFiles(files);
  }, [onFiles]);

  return (
    <div
      class={`rounded-xl border-2 border-dashed p-8 text-center transition ${
        dragging ? 'border-[var(--site-accent-color)] bg-[var(--surface)]' : 'border-[var(--border)]'
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
    >
      <p class="text-lg font-medium text-[var(--ink)]">{preset.label ?? 'Drop images to compress'}</p>
      <p class="mt-2 text-sm text-[var(--muted)]">
        or click to pick files · JPG, PNG, WebP up to 50 MB each
      </p>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        multiple
        class="hidden"
        onChange={(e) => {
          const files = Array.from((e.currentTarget as HTMLInputElement).files ?? []);
          if (files.length) onFiles(files);
        }}
      />
    </div>
  );
}
```

**Step 5: Run — expect PASS**

```bash
pnpm test:run tests/components/DropZone.test.tsx
```

**Step 6: Commit**

```bash
git add src/components/tool/DropZone.tsx tests/components/DropZone.test.tsx
git commit -m "feat(tool): drop zone component"
```

---

### Task 16: File row component

**Objective:** One row per queued/processing/done file showing original size, progress, result, download.

**Files:**
- Create: `src/components/tool/FileRow.tsx`
- Create: `tests/components/FileRow.test.tsx`

**Step 1: Write failing test**

```tsx
// tests/components/FileRow.test.tsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/preact';
import { FileRow } from '../../src/components/tool/FileRow';

describe('FileRow', () => {
  const baseFile = new File([new Uint8Array(500_000)], 'photo.jpg', { type: 'image/jpeg' });

  it('shows queued state', () => {
    render(<FileRow file={baseFile} state={{ kind: 'queued' }} onDownload={() => {}} />);
    expect(screen.getByText(/queued/i)).toBeTruthy();
    expect(screen.getByText('photo.jpg')).toBeTruthy();
  });
  it('shows done state with savings', () => {
    render(
      <FileRow
        file={baseFile}
        state={{
          kind: 'done',
          compressedSize: 150_000,
          blob: new Blob([new Uint8Array(150_000)]),
          hitTarget: true,
        }}
        onDownload={() => {}}
      />
    );
    expect(screen.getByText(/70% smaller/i)).toBeTruthy();
  });
  it('shows warning when target not hit', () => {
    render(
      <FileRow
        file={baseFile}
        state={{ kind: 'done', compressedSize: 450_000, blob: new Blob(), hitTarget: false }}
        onDownload={() => {}}
      />
    );
    expect(screen.getByText(/close to target/i)).toBeTruthy();
  });
});
```

**Step 2: Run — expect FAIL**

**Step 3: Implement**

Create `src/components/tool/FileRow.tsx`:
```tsx
/** @jsxImportSource preact */

export type FileRowState =
  | { kind: 'queued' }
  | { kind: 'processing' }
  | { kind: 'done'; compressedSize: number; blob: Blob; hitTarget: boolean }
  | { kind: 'error'; message: string };

interface Props {
  file: File;
  state: FileRowState;
  onDownload: () => void;
}

function humanBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

export function FileRow({ file, state, onDownload }: Props) {
  const statusText = (() => {
    switch (state.kind) {
      case 'queued': return 'queued';
      case 'processing': return 'squishing...';
      case 'done': {
        const saved = Math.round((1 - state.compressedSize / file.size) * 100);
        return `${saved}% smaller · ${humanBytes(state.compressedSize)}`;
      }
      case 'error': return state.message;
    }
  })();

  const targetNote = state.kind === 'done' && !state.hitTarget
    ? ' (close to target; cannot go smaller without heavier quality loss)'
    : '';

  return (
    <div class="flex items-center justify-between gap-4 rounded-lg border border-[var(--border)] bg-white px-4 py-3">
      <div class="min-w-0 flex-1">
        <div class="truncate text-sm font-medium text-[var(--ink)]">{file.name}</div>
        <div class={`mt-0.5 font-mono text-xs ${state.kind === 'error' ? 'text-[var(--warn)]' : 'text-[var(--muted)]'}`}>
          {humanBytes(file.size)} · {statusText}{targetNote}
        </div>
      </div>
      {state.kind === 'done' && (
        <button
          type="button"
          class="rounded-md bg-[var(--site-accent-color)] px-3 py-1.5 text-sm font-medium text-white hover:opacity-90"
          onClick={onDownload}
        >
          Download
        </button>
      )}
    </div>
  );
}
```

**Step 4: Run — expect PASS**

**Step 5: Commit**

```bash
git add src/components/tool/FileRow.tsx tests/components/FileRow.test.tsx
git commit -m "feat(tool): file row component with state machine UI"
```

---

### Task 17: Compressor island (orchestrator)

**Objective:** The top-level hydrated component. Manages queue, pool, URL params override, analytics events.

**Files:**
- Create: `src/components/tool/Compressor.tsx`

**Step 1: Implement**

Create `src/components/tool/Compressor.tsx`:
```tsx
/** @jsxImportSource preact */
import { useEffect, useRef, useState } from 'preact/hooks';
import type { Preset } from '../../config/presets';
import { DropZone } from './DropZone';
import { FileRow, type FileRowState } from './FileRow';
import type { CompressResult } from '../../lib/compress';
import { WorkerPool, computePoolSize } from '../../lib/worker-pool';

interface Props {
  preset: Preset;
}

interface Row {
  id: string;
  file: File;
  state: FileRowState;
  resultBlob?: Blob;
  outputName?: string;
}

const MAX_FILE_BYTES = 50 * 1024 * 1024;

// Allow ?target=200 URL override of targetKB.
function withUrlOverrides(preset: Preset): Preset {
  if (typeof window === 'undefined') return preset;
  const params = new URLSearchParams(window.location.search);
  const target = params.get('target');
  if (target) {
    const n = parseInt(target, 10);
    if (!Number.isNaN(n) && n > 0 && n < 100_000) {
      return { ...preset, targetKB: n };
    }
  }
  return preset;
}

export function Compressor({ preset: rawPreset }: Props) {
  const preset = withUrlOverrides(rawPreset);
  const [rows, setRows] = useState<Row[]>([]);
  const poolRef = useRef<WorkerPool | null>(null);

  useEffect(() => {
    return () => poolRef.current?.destroy();
  }, []);

  function ensurePool(): WorkerPool {
    if (poolRef.current) return poolRef.current;
    const pool = new WorkerPool({
      size: computePoolSize(),
      createWorker: () => new Worker(new URL('../../workers/compress.worker.ts', import.meta.url), { type: 'module' }),
    });
    poolRef.current = pool;
    return pool;
  }

  async function handleFiles(files: File[]) {
    const valid = files.filter((f) => {
      if (f.size > MAX_FILE_BYTES) return false;
      return /^image\/(jpeg|png|webp)$/.test(f.type);
    });
    const newRows: Row[] = valid.map((f, i) => ({
      id: `${Date.now()}-${i}-${f.name}`,
      file: f,
      state: { kind: 'queued' },
    }));
    setRows((prev) => [...prev, ...newRows]);

    const pool = ensurePool();
    for (const row of newRows) {
      setRows((prev) => prev.map((r) => (r.id === row.id ? { ...r, state: { kind: 'processing' } } : r)));
      const result = await pool.run({
        id: row.id,
        input: { file: row.file, preset },
      });
      if (result.ok && result.result) {
        const r = result.result as CompressResult;
        const ext = r.format === 'jpg' ? 'jpg' : r.format === 'png' ? 'png' : 'webp';
        const base = row.file.name.replace(/\.[^.]+$/, '');
        setRows((prev) => prev.map((x) =>
          x.id === row.id
            ? { ...x, resultBlob: r.blob, outputName: `${base}.squished.${ext}`,
                state: { kind: 'done', compressedSize: r.compressedSize, blob: r.blob, hitTarget: r.hitTarget } }
            : x,
        ));
        // Plausible event (if available on window)
        const p = (window as unknown as { plausible?: (n: string, o: unknown) => void }).plausible;
        p?.('tool_completed', { props: { format: r.format, hitTarget: r.hitTarget } });
      } else {
        setRows((prev) => prev.map((x) =>
          x.id === row.id ? { ...x, state: { kind: 'error', message: result.error ?? 'Unknown error' } } : x,
        ));
      }
    }
  }

  function download(row: Row) {
    if (!row.resultBlob || !row.outputName) return;
    const url = URL.createObjectURL(row.resultBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = row.outputName;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  return (
    <div class="space-y-4">
      <DropZone preset={preset} onFiles={handleFiles} />
      {rows.length > 0 && (
        <div class="space-y-2">
          {rows.map((r) => (
            <FileRow key={r.id} file={r.file} state={r.state} onDownload={() => download(r)} />
          ))}
        </div>
      )}
    </div>
  );
}
```

**Step 2: Verify type-check**

```bash
pnpm astro check
```

**Step 3: Commit**

```bash
git add src/components/tool/Compressor.tsx
git commit -m "feat(tool): Compressor orchestrator island"
```

---

### Task 18: Smoke-test the tool in dev

**Objective:** Render the Compressor on the homepage (temporary). Dev-server smoke check. Remove after Phase D wires it properly.

**Files:**
- Modify: `src/pages/index.astro` (temporary stub)

**Step 1: Add a temporary mount**

In `src/pages/index.astro`, inside the existing main content area, add:
```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { Compressor } from '../components/tool/Compressor';
import { PRESETS } from '../config/presets';
---
<BaseLayout title="makepicsmall — free image compression">
  <main class="mx-auto max-w-5xl px-4 py-12">
    <h1 class="text-3xl font-bold">Compress any image, in your browser</h1>
    <p class="mt-2 text-[var(--muted)]">Drop JPG, PNG, or WebP files below.</p>
    <div class="mt-8">
      <Compressor preset={PRESETS['/']} client:load />
    </div>
  </main>
</BaseLayout>
```

**Step 2: Run dev server**

```bash
pnpm dev
```

Open http://localhost:4321 in a browser, drag a real JPG into the drop zone. Confirm it compresses and the download button works.

Human review expected: once confirmed, continue. If not, debug via systematic-debugging skill.

**Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(pages): wire Compressor to homepage (placeholder)"
```

---

## Phase D — Tool pages (tasks 19–22)

### Task 19: Shared ToolPage template

**Objective:** One Astro template all 20 tool URLs use. Takes a URL slug, looks up its preset, renders consistent shell: H1, intro, Compressor, FAQ, related posts.

**Files:**
- Create: `src/components/ToolPage.astro`

**Step 1: Create component**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { Compressor } from './tool/Compressor';
import FAQ from './FAQ.astro';
import SchemaSoftwareApplication from './SchemaSoftwareApplication.astro';
import { type Preset } from '../config/presets';
import { siteConfig } from '../config/site.config';

interface Props {
  title: string;        // H1 and <title>
  description: string;  // meta description + intro lead
  intro: string;        // markdown-free 150-250w intro
  preset: Preset;
  faq: Array<{ q: string; a: string }>;
  canonicalPath: string; // e.g. "/for/passport-us"
}
const { title, description, intro, preset, faq, canonicalPath } = Astro.props;
const canonical = `https://${siteConfig.identity.domain}${canonicalPath}`;
---
<BaseLayout title={title} description={description} canonical={canonical}>
  <main class="mx-auto max-w-5xl px-4 py-10">
    <nav aria-label="Breadcrumb" class="mb-4 text-sm text-[var(--muted)]">
      <a href="/" class="hover:text-[var(--ink)]">Home</a>
      <span class="mx-1">/</span>
      <span>{preset.label ?? title}</span>
    </nav>
    <h1 class="text-3xl font-bold text-[var(--ink)]">{title}</h1>
    <p class="mt-3 text-lg text-[var(--muted)]">{description}</p>
    <div class="mt-8">
      <Compressor preset={preset} client:load />
    </div>
    <section class="mx-auto mt-12 max-w-3xl space-y-4">
      <div class="text-base leading-relaxed text-[var(--ink)]" set:html={intro.replace(/\n/g, '<br/>')} />
    </section>
    <section class="mx-auto mt-12 max-w-3xl">
      <h2 class="text-xl font-semibold">Frequently asked questions</h2>
      <div class="mt-4">
        <FAQ items={faq} />
      </div>
    </section>
  </main>
  <SchemaSoftwareApplication
    name={`${siteConfig.identity.name} — ${title}`}
    url={canonical}
    applicationCategory="MultimediaApplication"
    description={description}
    operatingSystem="Any (browser)"
    offers={{ price: '0', priceCurrency: 'USD' }}
  />
</BaseLayout>
```

**Step 2: Commit**

```bash
git add src/components/ToolPage.astro
git commit -m "feat(tool): shared ToolPage template"
```

---

### Task 20: Format and target pages (/compress/*, /to/*)

**Objective:** Create the 7 format-oriented and target-oriented pages.

**Files:**
- Create: `src/pages/compress/jpg.astro`
- Create: `src/pages/compress/png.astro`
- Create: `src/pages/compress/webp.astro`
- Create: `src/pages/compress/jpg/to/100kb.astro`
- Create: `src/pages/compress/jpg/to/500kb.astro`
- Create: `src/pages/compress/png/to/100kb.astro`
- Create: `src/pages/to/50kb.astro`
- Create: `src/pages/to/100kb.astro`
- Create: `src/pages/to/500kb.astro`
- Create: `src/pages/to/1mb.astro`
- Modify: `src/pages/index.astro` (replace Phase-C placeholder with real home)

**Step 1: Create a content source-of-truth**

Create `src/content/tool-copy.ts`:
```ts
export interface ToolCopy {
  title: string;
  description: string;
  intro: string;
  faq: Array<{ q: string; a: string }>;
}
export const TOOL_COPY: Record<string, ToolCopy> = {
  '/': {
    title: 'Compress any image, in your browser',
    description: 'Shrink JPG, PNG, and WebP files instantly — no uploads, no account, no nonsense.',
    intro: `makepicsmall runs 100% in your browser. Your photos never touch our servers. Drop a file, we squish it, you download — simple.\n\nWhen you need more than "smaller," use a preset: compress specifically for WhatsApp, Instagram, your resume, or a passport photo. Every preset uses the exact size, dimensions, and format each destination actually expects.`,
    faq: [
      { q: 'Are my photos uploaded?', a: 'No. Compression runs entirely in your browser using WebAssembly. No file leaves your device.' },
      { q: 'What formats are supported?', a: 'JPG, PNG, and WebP at launch. AVIF, GIF, and HEIC support is coming.' },
      { q: 'Is there a file size limit?', a: 'Yes — 50 MB per file so browsers don\'t run out of memory. Bigger files? Downscale first.' },
    ],
  },
  '/compress/jpg': {
    title: 'Compress JPG — free, browser-based, no uploads',
    description: 'Shrink JPG file size instantly. Pick a quality or target size, download the result. Nothing uploaded.',
    intro: `Drop any JPG and we'll squish it using mozjpeg — the same optimizer Google's Squoosh uses, running in your browser. You can set a quality level (1–100) or a hard target size in KB.\n\nFor most photos, quality 75–85 is visually identical to the original at roughly half the size. Below 50, most people start noticing artifacts around edges.`,
    faq: [
      { q: 'How much can a JPG be compressed?', a: 'Typically 40–70% size reduction with no visible quality loss. Photos from smartphones often shrink the most because they ship with very high quality settings.' },
      { q: 'Will my EXIF data be preserved?', a: 'No — our compressor strips metadata. This is usually what you want; it makes the file smaller and removes location data before sharing.' },
      { q: 'What if I need the smallest possible file?', a: 'Set a target size (100 KB, 500 KB, etc.) — we\'ll binary-search quality to hit it.' },
    ],
  },
  '/compress/png': {
    title: 'Compress PNG — lossless shrinking in your browser',
    description: 'Reduce PNG file size while keeping the transparency and crisp edges. Runs fully client-side.',
    intro: `PNG compression is different from JPG. PNGs use lossless compression by default, so we're reorganizing the file structure, not throwing away pixels. Typical savings: 30–50%, sometimes more on screenshots and flat-color graphics.\n\nIf you need more aggressive savings and your PNG has lots of colors (like a photo), consider switching to JPG or WebP instead — click the format selector above.`,
    faq: [
      { q: 'Does this preserve transparency?', a: 'Yes. We use oxipng, which is lossless — alpha channels, color profiles, everything stays intact.' },
      { q: 'Why is my PNG still big after compression?', a: 'PNG is meant for lossless compression. Photos in PNG format are rarely compressible much — switch to JPG or WebP for 80%+ smaller files.' },
      { q: 'What\'s the difference between PNG and WebP?', a: 'WebP offers lossless compression like PNG but smaller files, and also supports lossy mode. All modern browsers support it.' },
    ],
  },
  '/compress/webp': {
    title: 'Compress WebP — squeeze more out of modern images',
    description: 'Further reduce WebP file size with adjustable quality. Client-side, no uploads.',
    intro: `WebP is already a modern, efficient format. If you got a WebP from a camera app or web source and it's still big, we can squeeze more out of it — especially if the original was saved at a conservatively high quality.\n\nLike JPG, WebP supports lossy compression. Quality 80 is the sweet spot for most use cases.`,
    faq: [
      { q: 'Should I use WebP or JPG?', a: 'WebP is ~25–35% smaller than equivalent-quality JPG. All modern browsers and most platforms support it. Prefer WebP unless you\'re serving to very old systems.' },
      { q: 'Can I convert to WebP from JPG?', a: 'Format conversion is in Phase 2 — for now, we only re-encode WebP to WebP on this page.' },
      { q: 'Does WebP support transparency?', a: 'Yes — both lossy and lossless WebP support alpha channels.' },
    ],
  },
  '/compress/jpg/to/100kb': {
    title: 'Compress JPG to 100 KB (or less)',
    description: 'Shrink any JPG to 100 KB with automatic quality adjustment. Runs in your browser.',
    intro: `100 KB is the standard upload limit for many document forms, resume portals, and government ID applications. We automatically find the highest quality that fits under 100 KB.\n\nFor portrait-style photos, 100 KB typically gives you usable quality at 600–800 pixels on the long side. For very large source images, we recommend also setting a max dimension or using our resume / passport presets.`,
    faq: [
      { q: 'What if my photo can\'t fit in 100 KB?', a: 'We\'ll get as close as possible and show you the result. Very large or detailed images may need to be cropped or resized first.' },
      { q: 'Which platforms need 100 KB JPGs?', a: 'Common requirements: resume portals, some passport applications (check country), older web forms, email signatures.' },
      { q: 'Will it look pixelated?', a: 'At 100 KB for a full-size photo, yes. For profile-photo sized images (600×600 or smaller), quality is usually good.' },
    ],
  },
  '/compress/jpg/to/500kb': {
    title: 'Compress JPG to 500 KB',
    description: 'Get a JPG under 500 KB while keeping as much quality as possible. Binary-search is automatic.',
    intro: `500 KB is a comfortable upload ceiling for most social posts, email attachments, and blog images. Our quality search finds the setting that hits as close to 500 KB as possible without going over.\n\nFor typical photos from a phone (2–10 MB source), this works out to a visually-identical result most people won't notice is compressed.`,
    faq: [
      { q: 'Why 500 KB specifically?', a: 'It\'s a common soft limit: fast loading on blogs, fits in most email providers comfortably, and generally indistinguishable from the original to a casual viewer.' },
      { q: 'Can I set a custom target?', a: 'Yes — use our main compress tool and type a custom KB value in the target field.' },
      { q: 'Does this change the image dimensions?', a: 'No — this page compresses only. To also resize, use one of our preset pages like "for Instagram" or set max dimensions in the main tool.' },
    ],
  },
  '/compress/png/to/100kb': {
    title: 'Compress PNG to 100 KB',
    description: 'Lossless PNG compression targeting 100 KB. Transparency and edges preserved.',
    intro: `PNG compression is fundamentally different from JPG — we can\'t just lower "quality." To hit 100 KB on a photo-style PNG, we may need to reduce the palette or transition through a lossy step. For logos, screenshots, and flat graphics, 100 KB is usually easy to achieve losslessly.\n\nIf your PNG is a photo, consider converting to JPG or WebP — you\'ll get 100 KB with much better visual quality.`,
    faq: [
      { q: 'What if my PNG can\'t be compressed to 100 KB losslessly?', a: 'We\'ll get it as close as possible. For complex photos, you may need to switch to JPG or WebP.' },
      { q: 'Will transparency be preserved?', a: 'Yes, if we stay in lossless mode. For heavy compression, some PNGs drop to 8-bit palette which preserves transparency but reduces color count.' },
      { q: 'Why are PNG files so large?', a: 'PNG is lossless, so it preserves every pixel exactly. Perfect for graphics with sharp edges. Terrible for photographs.' },
    ],
  },
  '/to/50kb': {
    title: 'Compress image to 50 KB',
    description: 'Shrink any JPG, PNG, or WebP to under 50 KB. Pick a file — we\'ll try to fit it.',
    intro: `50 KB is tight — this is what small-form document upload portals often require. We keep the input format and automatically find the best quality that fits.\n\nFor typical phone photos, reaching 50 KB requires significant downsampling. If you just need a thumbnail or small profile picture, 50 KB often works well.`,
    faq: [
      { q: 'Is 50 KB too small to look good?', a: 'For a full-size photo: often yes. For small thumbnails (300×300 or smaller): usually fine.' },
      { q: 'Can you resize my image too?', a: 'Not on this page — use a preset page like /for/resume for both resize and compress.' },
      { q: 'Why would I need 50 KB?', a: 'Some government forms and old-school web forms enforce strict size limits. Check the requirements of whatever you\'re uploading to.' },
    ],
  },
  '/to/100kb': {
    title: 'Compress image to 100 KB',
    description: 'Any JPG, PNG, or WebP down to 100 KB — quality preserved where possible.',
    intro: `100 KB is the classic document-upload limit. Our tool finds the best quality under that ceiling for whichever format you upload.\n\nIf you specifically need a JPG output, use /compress/jpg/to/100kb instead — it forces JPG format regardless of input.`,
    faq: [
      { q: 'What file format will I get back?', a: 'The same format as your input. Upload a PNG, get a smaller PNG. Upload a JPG, get a smaller JPG.' },
      { q: 'What if I want to change format?', a: 'Format conversion is in Phase 2. For now, pick a format-specific page from our home.' },
      { q: 'Does this work on transparent PNGs?', a: 'Yes — transparency is preserved in PNG output.' },
    ],
  },
  '/to/500kb': {
    title: 'Compress image to 500 KB',
    description: 'Generous ceiling, minimal visible quality loss. For most photos this is "invisible" compression.',
    intro: `500 KB is where smart compression shines — visually identical to the original for most photos, but half to a quarter of the file size. Great for email attachments, blog posts, and social media.`,
    faq: [
      { q: 'Will viewers notice the difference?', a: 'Typically no. 500 KB is above the threshold where most compression artifacts are visible on a screen.' },
      { q: 'Good for blog posts?', a: 'Perfect. Most blog themes display images at 800–1200px wide — 500 KB is more than enough resolution for that.' },
      { q: 'What if I need smaller?', a: 'Try /to/100kb or /to/50kb for tighter targets.' },
    ],
  },
  '/to/1mb': {
    title: 'Compress image to 1 MB',
    description: 'A safe upper bound for most web and email use. Retains near-original quality.',
    intro: `1 MB (1000 KB) is a comfortable ceiling for almost any online use. Most photos compress to 1 MB with zero visible quality loss.\n\nIf your upload destination is more strict (many are 500 KB or 100 KB), use one of those pages instead.`,
    faq: [
      { q: 'Can I email a 1 MB photo?', a: 'Yes, easily — all major email providers accept attachments up to 20–25 MB.' },
      { q: 'Is 1 MB small enough for WordPress?', a: 'Fine for upload, but for page speed aim lower (~300 KB per image on a blog post).' },
      { q: 'When would I use 1 MB specifically?', a: 'Forms with strict-ish limits where you still want maximum quality. Not common — most forms are stricter.' },
    ],
  },
};
```

**Step 2: Create the page files**

Each page is a thin wrapper. Example — `src/pages/compress/jpg.astro`:

```astro
---
import ToolPage from '../../components/ToolPage.astro';
import { PRESETS } from '../../config/presets';
import { TOOL_COPY } from '../../content/tool-copy';
const path = '/compress/jpg';
const copy = TOOL_COPY[path];
---
<ToolPage
  title={copy.title}
  description={copy.description}
  intro={copy.intro}
  preset={PRESETS[path]}
  faq={copy.faq}
  canonicalPath={path}
/>
```

Repeat the same 6-line pattern for each of: `compress/png.astro`, `compress/webp.astro`, `compress/jpg/to/100kb.astro`, `compress/jpg/to/500kb.astro`, `compress/png/to/100kb.astro`, `to/50kb.astro`, `to/100kb.astro`, `to/500kb.astro`, `to/1mb.astro`. Only the `path` constant differs.

**Step 3: Update `src/pages/index.astro`** to use the same wrapper with `path = '/'`.

**Step 4: Verify**

```bash
pnpm build
ls -la dist/compress/ dist/to/
```

Expected: all pages generated; each has its own `index.html`.

**Step 5: Commit**

```bash
git add src/content/tool-copy.ts src/pages/
git commit -m "feat(pages): 10 format/target tool pages (with copy)"
```

---

### Task 21: Platform preset pages (/for/*)

**Objective:** The other 9 tool pages. Same pattern as Task 20, just per-platform copy.

**Files:**
- Modify: `src/content/tool-copy.ts` (add 9 more entries)
- Create: `src/pages/for/whatsapp.astro`, `whatsapp-dp.astro`, `instagram.astro`, `instagram-story.astro`, `resume.astro`, `passport-us.astro`, `passport-canada.astro`, `passport-uk.astro`, `linkedin.astro`

**Step 1: Extend `tool-copy.ts`** with the 9 new entries. Each follows the same ToolCopy shape. Key phrases that must appear in each `intro` for SEO:

| URL | Must-contain phrases in intro/FAQ |
|---|---|
| `/for/whatsapp` | "WhatsApp", "1600 pixels", "without losing quality", "Document mode" |
| `/for/whatsapp-dp` | "WhatsApp DP", "640 × 640", "profile picture", "100 KB" |
| `/for/instagram` | "Instagram", "1080 pixels", "feed post" |
| `/for/instagram-story` | "Instagram Story", "1080 × 1920", "9:16" |
| `/for/resume` | "resume", "CV", "600 × 600", "ATS" |
| `/for/passport-us` | "US passport", "state.gov", "600 × 600", "240 KB" |
| `/for/passport-canada` | "Canadian passport", "IRCC", "420 × 540", "240 KB" |
| `/for/passport-uk` | "UK passport", "600 × 750" |
| `/for/linkedin` | "LinkedIn", "400 × 400", "profile photo" |

Each entry needs 3 FAQ items. Each FAQ answer is 1–3 sentences. Example for `/for/passport-us`:
```ts
'/for/passport-us': {
  title: 'Compress photo for US passport application',
  description: 'Resize and compress a photo to meet state.gov requirements: 600×600 JPG, under 240 KB.',
  intro: `The US Department of State requires a 600×600 pixel JPG under 240 KB for digital passport applications. We automatically crop your photo to square, resize to 600×600, and compress to fit.\n\nBefore using this tool: make sure your source photo matches the other state.gov requirements — full-face view, plain white background, no glasses, no hat. We only handle the file dimensions and size — composition is up to you.`,
  faq: [
    { q: 'What are the official US passport photo specs?', a: '600×600 to 1200×1200 pixels (we default to 600×600), JPG only, under 240 KB file size. See travel.state.gov for the full guidance on composition, lighting, and background.' },
    { q: 'Will this tool auto-center my face?', a: 'No — we center-crop geometrically. Start with a photo where your face is already in the middle.' },
    { q: 'Can I use this for Canadian or UK passports?', a: 'No — those have different requirements. See /for/passport-canada or /for/passport-uk.' },
  ],
},
```

Write all 9 with the same care.

**Step 2: Create 9 page files** following the same 6-line wrapper pattern as Task 20.

**Step 3: Verify**

```bash
pnpm build
```

Expected: 20 tool URLs in the build output.

**Step 4: Commit**

```bash
git add src/content/tool-copy.ts src/pages/for/
git commit -m "feat(pages): 9 platform preset pages (/for/*)"
```

---

### Task 22: Homepage layout — hero + preset grid

**Objective:** Make the homepage feel like a real product, not just a tool. Hero, preset grid (category cards), brief about.

**Files:**
- Modify: `src/pages/index.astro`

**Step 1: Implement**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { Compressor } from '../components/tool/Compressor';
import { PRESETS } from '../config/presets';
import { TOOL_COPY } from '../content/tool-copy';

const presetCategories = [
  {
    heading: 'By format',
    items: [
      { href: '/compress/jpg', label: 'Compress JPG' },
      { href: '/compress/png', label: 'Compress PNG' },
      { href: '/compress/webp', label: 'Compress WebP' },
    ],
  },
  {
    heading: 'By size target',
    items: [
      { href: '/to/50kb',  label: 'To 50 KB' },
      { href: '/to/100kb', label: 'To 100 KB' },
      { href: '/to/500kb', label: 'To 500 KB' },
      { href: '/to/1mb',   label: 'To 1 MB' },
    ],
  },
  {
    heading: 'For a specific use',
    items: [
      { href: '/for/whatsapp',        label: 'WhatsApp' },
      { href: '/for/whatsapp-dp',     label: 'WhatsApp DP' },
      { href: '/for/instagram',       label: 'Instagram post' },
      { href: '/for/instagram-story', label: 'Instagram story' },
      { href: '/for/resume',          label: 'Resume photo' },
      { href: '/for/passport-us',     label: 'US passport photo' },
      { href: '/for/passport-canada', label: 'Canadian passport' },
      { href: '/for/passport-uk',     label: 'UK passport' },
      { href: '/for/linkedin',        label: 'LinkedIn profile' },
    ],
  },
];
---
<BaseLayout title="makepicsmall — shrink images in your browser">
  <main class="mx-auto max-w-5xl px-4 py-10">
    <section class="py-6">
      <h1 class="text-4xl font-bold text-[var(--ink)]">Your photos. Smaller. Squished in your browser.</h1>
      <p class="mt-3 max-w-2xl text-lg text-[var(--muted)]">
        Free, private image compression — nothing uploaded. Drop a JPG, PNG, or WebP.
      </p>
    </section>
    <section class="mt-2">
      <Compressor preset={PRESETS['/']} client:load />
    </section>
    <section class="mt-14">
      <h2 class="text-2xl font-semibold">Presets — one page per job</h2>
      <p class="mt-2 text-[var(--muted)]">Every preset uses the exact dimensions and size the destination actually expects.</p>
      <div class="mt-6 grid gap-8 md:grid-cols-3">
        {presetCategories.map((cat) => (
          <div>
            <h3 class="text-sm font-medium uppercase tracking-wide text-[var(--muted)]">{cat.heading}</h3>
            <ul class="mt-3 space-y-2">
              {cat.items.map((item) => (
                <li>
                  <a href={item.href} class="inline-block rounded-md bg-[var(--surface)] px-3 py-1.5 text-sm text-[var(--ink)] hover:bg-[var(--site-accent-color)] hover:text-white">
                    {item.label}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
    <section class="mx-auto mt-16 max-w-3xl prose">
      <h2 class="text-2xl font-semibold">Why makepicsmall?</h2>
      <p class="mt-3 text-[var(--ink)]">Most image compressors upload your photos to their servers. We don\'t. Everything runs in your browser using WebAssembly — the same engines Google uses in Squoosh, just wrapped in a friendlier coat.</p>
      <p class="mt-3 text-[var(--ink)]">That means: your photos stay on your device. It works offline. There\'s nothing to sign up for. And it\'s free.</p>
    </section>
  </main>
</BaseLayout>
```

**Step 2: Verify**

```bash
pnpm build
pnpm dev
# open http://localhost:4321 and spot-check
```

**Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(home): hero + preset grid + about"
```

---

## Phase E — Content, blog, and legal (tasks 23–27)

### Task 23: Write 4 launch blog posts (MDX)

**Objective:** Draft posts 1–4 from the content plan. These publish on launch day.

**Files:**
- Create: `src/content/blog/compress-jpg-to-100kb.mdx` (post 1)
- Create: `src/content/blog/compress-jpg-to-500kb.mdx` (post 2)
- Create: `src/content/blog/compress-png-to-100kb.mdx` (post 3)
- Create: `src/content/blog/shrink-photo-for-whatsapp.mdx` (post 4)

**Step 1: Template frontmatter**

Every post starts with:
```mdx
---
title: "How to compress a JPG to 100 KB online (free, private)"
description: "Step-by-step guide: shrink any JPG photo to under 100 KB using makepicsmall. Works in your browser, no uploads."
publishDate: 2026-04-23
updatedDate: 2026-04-23
author: "makepicsmall team"
tags: [jpg, compression, tutorial]
image: /og-default.png
---
```

**Step 2: Content brief for each post**

Each post must be 800–1200 words, contain:
- Intro (~150w) stating the problem
- Step-by-step section with 3–5 numbered steps, each with a screenshot placeholder (we'll add images post-launch)
- "How it works" section (150w) on what makepicsmall does under the hood
- "When it won't work" section with honest limitations
- CTA linking to the relevant tool URL
- At least 2 internal links to other tool URLs
- A small FAQ section (2–3 Q&A) with unique content (not duplicated from the tool page's FAQ)

**Step 3: Write each post**

Use the post titles from the content plan. I'm not inlining the full 800+ word drafts in this plan — a subagent will write them guided by:
- Target keyword (from `202 Site 1 Keywords.md` in the Obsidian vault)
- Post archetype from section 3 of the design spec
- The tool URL it anchors to
- The TOOL_COPY for that URL (so facts stay consistent)

The implementing subagent should:
1. Read `Sites/202 Site 1 Keywords.md` in the SuperVault
2. Read the matching `TOOL_COPY[path]` object
3. Write the post with the constraints above
4. Keep voice plain-English per the spec's section 4.4

**Step 4: Verify build**

```bash
pnpm build
# blog posts should appear in the build
ls dist/blog/
```

**Step 5: Commit**

```bash
git add src/content/blog/
git commit -m "content: 4 launch blog posts (tool-companion archetype)"
```

---

### Task 24: Fill in legal pages

**Objective:** Replace placeholder text in `/privacy`, `/terms`, `/about`, `/contact`, `/sponsored`.

**Files:**
- Modify: `src/pages/privacy.astro`
- Modify: `src/pages/terms.astro`
- Modify: `src/pages/about.astro`
- Modify: `src/pages/contact.astro`
- Modify: `src/pages/sponsored.astro`

**Step 1: Privacy policy**

The site uploads nothing — this is our biggest trust differentiator. The privacy page should say exactly that and nothing more dishonest. Draft:

- "Compression happens in your browser. Files never leave your device."
- "We use Cloudflare as our CDN; Cloudflare sees normal HTTP request logs (IP, user agent, referer) which they retain per their own policies."
- "We use Cloudflare Web Analytics / Plausible for privacy-preserving analytics (no cookies, no user identification)."
- "We do not use ad-tracking cookies."
- "We do not sell data."
- Standard GDPR/PIPEDA user rights section.
- Contact email for privacy requests.
- Last updated date.

**Step 2: Terms of service**

- Free tool, no warranty, "as is"
- Don't upload copyrighted material you don't own
- We may change the service
- Limitation of liability
- Last updated date.

**Step 3: About**

Short. "makepicsmall is a privacy-first image compressor built by [site-network holding company TBD]. We think image tools shouldn't need your data to shrink a photo. That's the whole pitch."

**Step 4: Contact**

Plain page — email address + brief "here's what we answer" list. No form for MVP (adds backend complexity).

**Step 5: Sponsored**

Keep the template's existing sponsored-intake page structure; just fill in niche-specific details: "makepicsmall reaches [TBD] users/month interested in [photography, blogging, web development, social media]. We accept sponsored posts that genuinely help our audience. Not: generic backlink-stuffing guest posts."

**Step 6: Commit**

```bash
git add src/pages/
git commit -m "content: fill in privacy, terms, about, contact, sponsored pages"
```

---

### Task 25: Update robots, sitemap, RSS

**Objective:** Verify these are auto-generating the right thing after all new pages.

**Files:**
- Check: `dist/robots.txt`, `dist/sitemap-index.xml`, `dist/sitemap-0.xml`, `dist/rss.xml`

**Step 1: Build and inspect**

```bash
pnpm build
cat dist/robots.txt
head -30 dist/sitemap-0.xml
cat dist/rss.xml | head -20
```

Expected:
- robots.txt: allow all, sitemap URL present
- sitemap: contains all 20 tool URLs + 4 blog posts + legal pages (~30 URLs)
- rss.xml: contains the 4 blog posts

**Step 2: If anything missing — add to the `src/pages/rss.xml.ts` or `sitemap.config`**

**Step 3: Commit (if any changes)**

```bash
git commit -am "fix(seo): ensure all tool/blog URLs in sitemap + RSS"
```

---

### Task 26: Playwright integration smoke tests

**Objective:** One end-to-end test per page type confirming the tool actually works in a real browser.

**Files:**
- Create: `playwright.config.ts`
- Create: `e2e/compress.spec.ts`
- Modify: `package.json` (add `test:e2e`)

**Step 1: Install Playwright**

```bash
pnpm add -D @playwright/test
npx playwright install chromium
```

**Step 2: Config**

Create `playwright.config.ts`:
```ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './e2e',
  use: { baseURL: 'http://localhost:4321' },
  webServer: {
    command: 'pnpm preview --port 4321',
    port: 4321,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
```

**Step 3: Test**

Create `e2e/compress.spec.ts`:
```ts
import { test, expect } from '@playwright/test';

const FIXTURE = 'tests/fixtures/tiny-jpg.jpg';

test('homepage loads and shows drop zone', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByText(/drop images to compress/i).or(page.getByText(/compress any image/i))).toBeVisible();
});

test('/compress/jpg compresses a file', async ({ page }) => {
  await page.goto('/compress/jpg');
  await page.setInputFiles('input[type=file]', FIXTURE);
  await expect(page.getByRole('button', { name: 'Download' })).toBeVisible({ timeout: 10_000 });
});

test('/for/passport-us has correct spec copy', async ({ page }) => {
  await page.goto('/for/passport-us');
  await expect(page.getByText(/600\s*×\s*600/i)).toBeVisible();
  await expect(page.getByText(/240\s*KB/i)).toBeVisible();
});
```

**Step 4: Build and run**

```bash
pnpm build
pnpm exec playwright test
```

**Step 5: Commit**

```bash
git add playwright.config.ts e2e/ package.json pnpm-lock.yaml
git commit -m "test(e2e): playwright smoke tests for 3 page types"
```

---

### Task 27: Final build + redeploy to Cloudflare Pages

**Objective:** Ship it.

**Step 1: Final build**

```bash
cd ~/site-network/sites/makepicsmall.com
pnpm test:run          # all vitest tests green
pnpm exec playwright test    # all e2e tests green
pnpm astro check       # 0 errors
pnpm build             # production build succeeds
```

**Step 2: Deploy**

Use the same wrangler pattern as the initial deploy. From my monorepo root:

```bash
cd ~/site-network/sites/makepicsmall.com
CLOUDFLARE_API_TOKEN=<token> CLOUDFLARE_ACCOUNT_ID=<account> \
  npx wrangler@latest pages deploy dist \
  --project-name=makepicsmall --branch=main \
  --commit-message="mvp launch: v0.1.0"
```

**Step 3: Smoke-test the live URL**

```bash
curl -s -H "User-Agent: Mozilla/5.0" https://makepicsmall.com/ | grep -c "makepicsmall"
curl -s -H "User-Agent: Mozilla/5.0" https://makepicsmall.com/for/passport-us/ | grep -c "600"
```

Expected: both > 0.

**Step 4: Submit sitemap to GSC + Bing + Ahrefs** (manual, user task — document in a launch SOP in the vault).

**Step 5: Tag the release**

```bash
git tag v0.1.0 -m "makepicsmall MVP launch"
git log --oneline | head -30
```

---

## Phase F — Staggered post publish (tasks 28–31, over 2 weeks)

These run AFTER the MVP launches. Each task is identical: write one post, commit, push, deploy.

### Task 28: Post 5 — "Resize photo for US passport application"
### Task 29: Post 6 — "Shrink resume photo under 100KB"
### Task 30: Post 7–8 — Educational pillars
### Task 31: Post 9–10 — Remaining pillar + data study

Details of each follow the same Task-23 template. The data study (post 10) has a prerequisite: generate a 1000-image dataset and run the compression matrix. Create a separate `docs/plans/2026-05-XX-data-study.md` when we reach that task.

---

## Stop-and-assess criteria

After Task 27, pause and evaluate before Phase F:
- Did the site deploy cleanly to production?
- Are all 20 tool URLs returning 200 with correct preset behavior?
- Is GSC showing the sitemap indexed?
- Any runtime errors in browser console on real devices?

If any blocker → address before continuing Phase F. If all green → proceed with post staggering per [[700 Content Playbook]] cadence rules.

---

## Dependency summary

**Runtime:** `@jsquash/jpeg`, `@jsquash/png`, `@jsquash/webp`, `@fontsource-variable/geist`, `@fontsource-variable/geist-mono`, `preact` (already in template)

**Dev:** `vitest`, `@vitest/ui`, `@testing-library/preact`, `jsdom`, `@playwright/test`, `@napi-rs/canvas` (for OG + fixtures, not in bundle)

No backend. No edge functions. No API keys baked in.

---

## What this plan explicitly does NOT cover

- AVIF, GIF, SVG, HEIC support (Phase 2)
- Format conversion (Phase 2)
- Dark mode (Phase 2)
- OG image generation per-URL (MVP uses single static OG)
- Social-share card generation (Phase 2)
- Product Hunt launch (decision: week 3 post-launch)
- Reddit/HN outreach (week 1 post-launch, manual)
- Plausible self-hosting (deferred; use Cloudflare Web Analytics stub until ready)
- GitHub repo + Pages git-push CI (hybrid path, post-MVP)

---

**End of plan.**
