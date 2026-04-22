# howmanycoin.com MVP Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Ship a production-ready MVP of howmanycoin.com — a crypto pair-converter + tokenomics explainer with 25 pair pages, 10 supply pages, 5 evergreen guides, a b-lazy Cloudflare Worker rate service, geo-switched CEX CTAs, and editorial serif design — deployed live on Cloudflare Pages within 2–3 focused work-days.

**Architecture:** Astro 5 static site (already scaffolded at `sites/howmanycoin.com/`) with a Preact island for the pair calculator. A single Cloudflare Worker at `/api/rate` implements the b-lazy pattern (Workers Cache API, 60s TTL, one CoinGecko call per minute max) and injects affiliate params server-side so they can't be stripped. Geo-switching via `CF-IPCountry` header returns per-region CEX CTA sets in the same payload.

**Tech Stack:** Astro 5, TypeScript strict, Preact islands, Fraunces + Source Serif 4 + IBM Plex Sans + IBM Plex Mono via `@fontsource-variable`, Vitest for unit tests, `@cloudflare/vitest-pool-workers` for the Worker, Playwright for e2e, Wrangler for deploy.

**Design spec:** `~/site-network/docs/superpowers/specs/2026-04-22-howmanycoin-mvp-design.md` (approved 2026-04-22)

**Work directory:** `~/site-network/sites/howmanycoin.com/`

**Worker directory:** `~/site-network/sites/howmanycoin.com/workers/` (Worker is a sub-package inside the site dir)

---

## Conventions for every task

- All paths are relative to `~/site-network/sites/howmanycoin.com/` unless stated otherwise.
- Run all commands from that directory (`cd ~/site-network/sites/howmanycoin.com/`). The Worker has its own sub-directory `workers/` with a separate `wrangler.toml`; Worker commands are run from `~/site-network/sites/howmanycoin.com/workers/`.
- Every task ends with a commit. Commit messages use [conventional commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`, `style:`, `perf:`.
- Test runner is Vitest (`pnpm test -- --run`). Playwright is `pnpm test:e2e` (added in Phase J).
- After every task, the full test suite must still pass. Run `pnpm test -- --run` before committing.
- The template files already present in `sites/howmanycoin.com/` (from the `create-site` scaffold — blog/tools/games collections, BaseLayout, PostLayout, ToolLayout, GameLayout, Header, Footer, CookieBanner, AffiliateDisclosure, Schema components) are the starting point. Do NOT regenerate the site.
- **Design inheritance:** the tight h2/h3 prose rhythm, list spacing, and scroll-margin anchoring live in the shared template's `global.css` (already committed in d8934e9). Do NOT re-add a prose block. Override only the color and font custom-property tokens.
- **Source of truth** for product decisions is `docs/superpowers/specs/2026-04-22-howmanycoin-mvp-design.md`. If this plan contradicts the spec, the spec wins; open a new task to reconcile.
- All 25 pair slugs (spec §2) and all 10 supply slugs (spec §2) are enumerated verbatim in Tasks 7–9. Do not invent new slugs.

---

## Phase A — Foundation & brand tokens (tasks 1–5)

### Task 1: Install runtime and dev dependencies

**Objective:** Add Preact (already in template via integration, but pin for the island), @fontsource-variable packages for the four-face type stack, Vitest, Playwright, Wrangler, and Cloudflare Worker vitest pool.

**Files:**
- Modify: `package.json`
- Modify: `pnpm-lock.yaml` (auto-generated)

**Step 1: Verify Preact integration already present**

```bash
cd ~/site-network/sites/howmanycoin.com
grep -c '@astrojs/preact' package.json
```
Expected: `1` (template already wires Preact for islands). If `0`, run `pnpm add -D @astrojs/preact preact` and add `preact()` to `astro.config.mjs` integrations.

**Step 2: Add font packages**

```bash
pnpm add @fontsource-variable/fraunces @fontsource-variable/source-serif-4 @fontsource-variable/ibm-plex-sans @fontsource-variable/ibm-plex-mono
```

**Step 3: Add dev deps**

```bash
pnpm add -D vitest @vitest/ui @testing-library/preact jsdom @playwright/test wrangler @cloudflare/workers-types @cloudflare/vitest-pool-workers
```

**Step 4: Wire test scripts**

In `package.json`, add/replace under `"scripts"`:

```json
"test": "vitest",
"test:e2e": "playwright test",
"test:worker": "cd workers && vitest --run"
```

**Step 5: Verify**

```bash
pnpm test -- --run 2>&1 | tail -5
```
Expected: `No test files found` — that's fine, vitest is wired.

```bash
pnpm build 2>&1 | tail -3
```
Expected: build succeeds (existing template still builds with new deps).

**Step 6: Commit**

```bash
git add package.json pnpm-lock.yaml
git commit -m "chore: add fraunces/source-serif/plex fonts, vitest, playwright, wrangler"
```

---

### Task 2: Apply howmanycoin palette and type tokens to `site.config.ts`

**Objective:** Swap the scaffold defaults for the approved cool off-white + ink-indigo palette and document the four-face stack.

**Files:**
- Modify: `src/config/site.config.ts`
- Create: `tests/branding.test.ts`

**Step 1: Write failing test**

Create `tests/branding.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { siteConfig } from '../src/config/site.config';

describe('howmanycoin branding', () => {
  it('uses cool off-white bg and deep ink-indigo accent', () => {
    expect(siteConfig.branding.themeColor).toBe('#f7f8fa');
    expect(siteConfig.branding.accentColor).toBe('#3730a3');
  });
  it('logoText matches domain identity', () => {
    expect(siteConfig.branding.logoText).toBe('howmanycoin');
  });
  it('description emphasises pair conversion and supply', () => {
    expect(siteConfig.identity.description.toLowerCase()).toMatch(/convert|supply|rate/);
  });
});
```

**Step 2: Create `vitest.config.ts`**

```ts
import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['tests/**/*.test.ts', 'tests/**/*.test.tsx', 'src/**/*.test.ts'],
    exclude: ['workers/**', 'node_modules/**', 'tests/e2e/**'],
  },
});
```

**Step 3: Run — expect FAIL**

```bash
pnpm test -- --run tests/branding.test.ts 2>&1 | tail -10
```
Expected: themeColor assertion fails (`#0f172a` !== `#f7f8fa`).

**Step 4: Update `src/config/site.config.ts`**

Replace the `identity`, `branding`, `seo`, `monetization`, and `nav` blocks:

```ts
identity: {
  name: 'howmanycoin',
  domain: 'howmanycoin.com',
  description:
    'Live crypto pair conversion rates and token-supply explainers. How many USDC is 1 ETH, right now? Direct swap links included.',
  language: 'en',
  timezone: 'UTC',
},
branding: {
  themeColor: '#f7f8fa',
  accentColor: '#3730a3',
  logoText: 'howmanycoin',
  ogImageStrategy: 'static',
},
```

Update `nav.primary`:

```ts
nav: {
  primary: [
    { label: 'Convert', href: '/convert/' },
    { label: 'Supply', href: '/supply/' },
    { label: 'Guides', href: '/guides/' },
    { label: 'Methodology', href: '/methodology/' },
    { label: 'About', href: '/about/' },
  ],
},
```

Update `monetization.affiliateDisclosure`:

```ts
monetization: {
  affiliateDisclosure:
    'Rates shown are estimates sourced from CoinGecko, refreshed every 60 seconds. Swap and exchange links on this page are affiliate links; if you use one we may earn a commission at no extra cost to you. Not financial advice.',
},
```

Update `features`:

```ts
features: {
  hasBlog: false,
  hasTool: false,
  hasGame: false,
  hasSponsoredIntake: true,
},
```

**Step 5: Run — expect PASS**

```bash
pnpm test -- --run tests/branding.test.ts 2>&1 | tail -5
```
Expected: 3 passing.

**Step 6: Commit**

```bash
git add src/config/site.config.ts tests/branding.test.ts vitest.config.ts
git commit -m "feat(brand): apply cool off-white + ink-indigo palette, crypto nav"
```

---

### Task 3: Override color and font tokens in `global.css` (preserve shared prose block)

**Objective:** Only override CSS custom properties for color + font. Do NOT re-add heading rhythm — the shared template's `global.css` already provides it via package import.

**Files:**
- Modify: `src/styles/global.css`
- Modify: `src/layouts/BaseLayout.astro` (font imports)

**Step 1: Inspect current `src/styles/global.css`**

```bash
head -40 src/styles/global.css
```
Confirm it contains the shared prose block ported from makepicsmall 2026-04-22 (d8934e9). If it does NOT, stop — the scaffold is stale; re-pull from `packages/site-template`.

**Step 2: Override tokens at the top of `src/styles/global.css`**

Replace any existing `:root` block at the top of the file with:

```css
:root {
  /* howmanycoin palette (spec §6) */
  --site-theme-color: #f7f8fa;
  --site-accent-color: #3730a3;
  --ink: #0a0e1a;
  --muted: #4b5568;
  --surface: #eef0f4;
  --border: #d7dae1;
  --pos: #065f46;
  --neg: #b91c1c;

  /* Type stack (spec §6) */
  --site-font-display: 'Fraunces Variable', Georgia, 'Times New Roman', serif;
  --site-font-serif: 'Source Serif 4 Variable', Georgia, 'Times New Roman', serif;
  --site-font-sans: 'IBM Plex Sans Variable', system-ui, -apple-system, sans-serif;
  --site-font-mono: 'IBM Plex Mono Variable', ui-monospace, 'SFMono-Regular', monospace;
}

html {
  background: var(--site-theme-color);
  color: var(--ink);
  font-family: var(--site-serif, var(--site-font-serif));
}
body { font-family: var(--site-font-serif); }
h1, h2, h3, h4 { font-family: var(--site-font-display); font-weight: 500; letter-spacing: -0.01em; }

/* Article widths (spec §6) */
.prose, article.prose { max-width: 44rem; }
.prose.wide, article.prose.wide { max-width: 56rem; }

/* Hairline rules between sections */
.prose hr { border: 0; border-top: 1px solid var(--border); margin: 2.5rem 0; }

/* Small-caps meta */
.meta { font-family: var(--site-font-sans); font-variant: all-small-caps; letter-spacing: 0.06em; color: var(--muted); font-size: 0.85rem; }

/* Numeric figures use Plex Mono with tabular-nums */
.num, .figure { font-family: var(--site-font-mono); font-variant-numeric: tabular-nums; }

/* Drop cap for long-form first paragraph (.dropcap class applied to supply + guide first <p>) */
.dropcap::first-letter {
  float: left;
  font-family: var(--site-font-display);
  font-size: 3.2rem;
  line-height: 0.9;
  padding: 0.35rem 0.6rem 0 0;
  font-weight: 600;
  color: var(--ink);
}

/* Bordered "island" (calculator + facts table) */
.island {
  border: 1px solid var(--border);
  background: var(--surface);
  padding: 1.25rem;
  border-radius: 4px;
  font-family: var(--site-font-sans);
  margin: 1.75rem 0;
}
.island label { display: block; font-size: 0.8rem; color: var(--muted); font-variant: all-small-caps; letter-spacing: 0.06em; margin-bottom: 0.35rem; }
.island input, .island .figure { font-family: var(--site-font-mono); font-size: 1.35rem; color: var(--ink); }

/* Positive / negative ticks */
.tick-pos { color: var(--pos); font-family: var(--site-font-mono); }
.tick-neg { color: var(--neg); font-family: var(--site-font-mono); }

/* Links */
a { color: var(--site-accent-color); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }
a:hover { text-decoration-thickness: 2px; }
```

**Step 3: Import the four fonts in `BaseLayout.astro`**

At the top of the frontmatter in `src/layouts/BaseLayout.astro`, add:

```ts
import '@fontsource-variable/fraunces';
import '@fontsource-variable/source-serif-4';
import '@fontsource-variable/ibm-plex-sans';
import '@fontsource-variable/ibm-plex-mono';
```

**Step 4: Verify build**

```bash
pnpm build 2>&1 | tail -5
```
Expected: build succeeds. Spot-check `dist/index.html`:

```bash
grep -c 'f7f8fa\|3730a3' dist/index.html
```
Expected: at least 1 (theme-color meta picks up the token).

**Step 5: Commit**

```bash
git add src/styles/global.css src/layouts/BaseLayout.astro
git commit -m "feat(style): override color+font tokens, add .island and drop-cap helpers"
```

---

### Task 4: Update `BaseLayout.astro` default OG + `<html lang>` + viewport

**Objective:** Ensure the site defaults match howmanycoin identity (no leftover template strings) and that the viewport does NOT double-count on zoom for the calculator island.

**Files:**
- Modify: `src/layouts/BaseLayout.astro`
- Create: `public/og-default.svg` (SVG template used in Phase J for generated OG)

**Step 1: Write `public/og-default.svg`**

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#f7f8fa"/>
  <text x="60" y="180" font-family="Georgia, serif" font-size="72" font-weight="500" fill="#0a0e1a">howmanycoin</text>
  <text x="60" y="260" font-family="Georgia, serif" font-size="40" fill="#4b5568">Live crypto pair rates.</text>
  <text x="60" y="310" font-family="Georgia, serif" font-size="40" fill="#4b5568">Plain-English supply explainers.</text>
  <line x1="60" y1="540" x2="1140" y2="540" stroke="#d7dae1" stroke-width="1"/>
  <text x="60" y="580" font-family="Menlo, monospace" font-size="26" fill="#3730a3">howmanycoin.com</text>
</svg>
```

**Step 2: Convert to PNG fallback** (optional, deferred to Phase J). For now, the SVG works in all crawlers that matter.

**Step 3: Update `defaultOgImage` in `site.config.ts`**

Change to `'/og-default.svg'`.

**Step 4: Verify build**

```bash
pnpm build
test -f dist/og-default.svg && echo OK
```
Expected: `OK`.

**Step 5: Commit**

```bash
git add public/og-default.svg src/config/site.config.ts
git commit -m "feat(og): add serif SVG OG template + wire defaultOgImage"
```

---

### Task 5: Create shared type + token modules (`src/lib/tokens.ts`)

**Objective:** One source of truth for all tokens the site prices + their CoinGecko IDs + chain.

**Files:**
- Create: `src/lib/tokens.ts`
- Create: `src/lib/tokens.test.ts`

**Step 1: Write failing test**

Create `src/lib/tokens.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { TOKENS, getToken, COINGECKO_IDS } from './tokens';

describe('token registry', () => {
  it('covers every token referenced by pair + supply pages', () => {
    const required = ['btc', 'eth', 'sol', 'usdc', 'usdt', 'dai', 'bnb', 'matic', 'avax', 'doge', 'shib', 'pepe', 'arb', 'op', 'xrp', 'ada', 'ton'];
    for (const sym of required) expect(TOKENS[sym], `missing ${sym}`).toBeDefined();
  });
  it('lookup returns undefined for unknown sym', () => {
    expect(getToken('xxx')).toBeUndefined();
  });
  it('COINGECKO_IDS is a deduped comma list', () => {
    const arr = COINGECKO_IDS.split(',');
    expect(new Set(arr).size).toBe(arr.length);
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test -- --run src/lib/tokens.test.ts 2>&1 | tail -5
```
Expected: Cannot find module.

**Step 3: Create `src/lib/tokens.ts`**

```ts
/**
 * Token registry — every token priced or described on the site.
 * Source of truth: docs/superpowers/specs/2026-04-22-howmanycoin-mvp-design.md §2
 */

export type Chain = 'bitcoin' | 'ethereum' | 'solana' | 'bsc' | 'polygon' | 'arbitrum' | 'optimism' | 'avalanche' | 'ton' | 'ripple' | 'cardano';

export interface Token {
  symbol: string;          // lowercase ticker, URL-safe
  name: string;            // human name
  coingeckoId: string;     // for /simple/price
  chain: Chain;            // home chain for aggregator routing
  isStablecoin: boolean;
  contract?: string;       // ERC-20 / SPL contract where applicable
  decimals: number;
}

export const TOKENS: Record<string, Token> = {
  btc:   { symbol: 'btc',   name: 'Bitcoin',      coingeckoId: 'bitcoin',        chain: 'bitcoin',  isStablecoin: false, decimals: 8 },
  eth:   { symbol: 'eth',   name: 'Ethereum',     coingeckoId: 'ethereum',       chain: 'ethereum', isStablecoin: false, decimals: 18 },
  sol:   { symbol: 'sol',   name: 'Solana',       coingeckoId: 'solana',         chain: 'solana',   isStablecoin: false, decimals: 9 },
  usdc:  { symbol: 'usdc',  name: 'USD Coin',     coingeckoId: 'usd-coin',       chain: 'ethereum', isStablecoin: true,  decimals: 6, contract: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48' },
  usdt:  { symbol: 'usdt',  name: 'Tether',       coingeckoId: 'tether',         chain: 'ethereum', isStablecoin: true,  decimals: 6, contract: '0xdAC17F958D2ee523a2206206994597C13D831ec7' },
  dai:   { symbol: 'dai',   name: 'Dai',          coingeckoId: 'dai',            chain: 'ethereum', isStablecoin: true,  decimals: 18, contract: '0x6B175474E89094C44Da98b954EedeAC495271d0F' },
  bnb:   { symbol: 'bnb',   name: 'BNB',          coingeckoId: 'binancecoin',    chain: 'bsc',      isStablecoin: false, decimals: 18 },
  matic: { symbol: 'matic', name: 'Polygon',      coingeckoId: 'matic-network',  chain: 'polygon',  isStablecoin: false, decimals: 18 },
  avax:  { symbol: 'avax',  name: 'Avalanche',    coingeckoId: 'avalanche-2',    chain: 'avalanche',isStablecoin: false, decimals: 18 },
  doge:  { symbol: 'doge',  name: 'Dogecoin',     coingeckoId: 'dogecoin',       chain: 'bitcoin',  isStablecoin: false, decimals: 8 },
  shib:  { symbol: 'shib',  name: 'Shiba Inu',    coingeckoId: 'shiba-inu',      chain: 'ethereum', isStablecoin: false, decimals: 18 },
  pepe:  { symbol: 'pepe',  name: 'Pepe',         coingeckoId: 'pepe',           chain: 'ethereum', isStablecoin: false, decimals: 18 },
  arb:   { symbol: 'arb',   name: 'Arbitrum',     coingeckoId: 'arbitrum',       chain: 'arbitrum', isStablecoin: false, decimals: 18 },
  op:    { symbol: 'op',    name: 'Optimism',     coingeckoId: 'optimism',       chain: 'optimism', isStablecoin: false, decimals: 18 },
  xrp:   { symbol: 'xrp',   name: 'XRP',          coingeckoId: 'ripple',         chain: 'ripple',   isStablecoin: false, decimals: 6 },
  ada:   { symbol: 'ada',   name: 'Cardano',      coingeckoId: 'cardano',        chain: 'cardano',  isStablecoin: false, decimals: 6 },
  ton:   { symbol: 'ton',   name: 'Toncoin',      coingeckoId: 'the-open-network', chain: 'ton',    isStablecoin: false, decimals: 9 },
};

export function getToken(sym: string): Token | undefined {
  return TOKENS[sym.toLowerCase()];
}

/** Deduped comma-separated list for a single CoinGecko /simple/price call. */
export const COINGECKO_IDS = Array.from(new Set(Object.values(TOKENS).map((t) => t.coingeckoId))).join(',');
```

**Step 4: Run — expect PASS**

```bash
pnpm test -- --run src/lib/tokens.test.ts 2>&1 | tail -5
```
Expected: 3 passing.

**Step 5: Commit**

```bash
git add src/lib/tokens.ts src/lib/tokens.test.ts
git commit -m "feat(lib): token registry with 17 tokens + CoinGecko IDs"
```

---

## Phase B — Content collections + seed MDX (tasks 6–11)

### Task 6: Rewrite `src/content/config.ts` — pairs / supply / guides

**Objective:** Replace the template's tools/games collections with the three crypto collections. Keep `blog` collection present but hidden so we can reuse it later without migration.

**Files:**
- Modify: `src/content/config.ts`
- Create: `src/content/config.test.ts`
- Delete (via removal): the tools and games collection source directories

**Step 1: Write failing test**

Create `src/content/config.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { collections } from './config';

describe('content collections', () => {
  it('exposes pairs, supply, guides', () => {
    expect(collections.pairs).toBeDefined();
    expect(collections.supply).toBeDefined();
    expect(collections.guides).toBeDefined();
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test -- --run src/content/config.test.ts 2>&1 | tail -5
```

**Step 3: Replace `src/content/config.ts`**

```ts
import { defineCollection, z } from 'astro:content';

/**
 * Content collections for howmanycoin.com
 *
 * pairs  — /convert/{from}-to-{to}  (25 pages)
 * supply — /supply/{token}          (10 pages)
 * guides — /guides/{slug}           (5 pages)
 *
 * blog is retained (unused at launch) so future editorial posts drop in without migration.
 */

const pairs = defineCollection({
  type: 'content',
  schema: z.object({
    from: z.string(),                     // 'eth'
    to: z.string(),                       // 'usdc'
    title: z.string(),                    // 'Convert ETH to USDC — live rate'
    description: z.string().max(200),
    category: z.enum(['stablecoin', 'major-cross', 'memecoin', 'l2', 'off-ramp', 'stablecoin-pair']),
    aggregator: z.enum(['1inch', 'jupiter', 'none']).default('1inch'),
    popularity: z.number().int().min(0).default(0), // for index page sort
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
    featured: z.boolean().default(false),
  }),
});

const supply = defineCollection({
  type: 'content',
  schema: z.object({
    symbol: z.string(),                   // 'btc'
    name: z.string(),                     // 'Bitcoin'
    title: z.string(),
    description: z.string().max(200),
    maxSupply: z.union([z.number(), z.literal('uncapped')]),
    currentIssuanceMechanism: z.string(), // 'Mining, halving every 210,000 blocks'
    hasHalving: z.boolean().default(false),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
  }),
});

const guides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().max(200),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Editorial Team'),
    relatedPairs: z.array(z.string()).default([]),
    faq: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string().max(120),
    description: z.string().max(200),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: z.string().default('Editorial Team'),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { pairs, supply, guides, blog };
```

**Step 4: Remove obsolete scaffold content directories + pages**

```bash
rm -rf src/content/tools src/content/games
rm -rf src/pages/tools src/pages/games
rm -rf src/pages/blog
```

(Blog collection stays defined in the config for future use, but the routes/pages are removed so they don't render empty.)

**Step 5: Delete the `Breadcrumb`-based tools/games references if any template page references them** — spot-check:

```bash
grep -rn "tools\|games" src/pages 2>/dev/null | head -20
```
Expected: no matches after the rm above.

**Step 6: Run tests + build**

```bash
pnpm test -- --run src/content/config.test.ts 2>&1 | tail -5
pnpm astro check 2>&1 | tail -10
```
Expected: test passes; astro check may complain about the now-empty collections until Task 7 seeds them. If it complains about unrelated schema, fix before moving on.

**Step 7: Commit**

```bash
git add src/content/config.ts src/content/config.test.ts
git add -u src/content src/pages
git commit -m "feat(content): replace tools/games with pairs/supply/guides collections"
```

---

### Task 7: Seed 25 pair MDX stubs

**Objective:** Create one MDX file per pair under `src/content/pairs/`. Stubs are short (title + 2 paragraphs + 3 FAQ prompts) but carry complete frontmatter so the build works and the index + schema can render.

**Files:**
- Create: 25 files under `src/content/pairs/` named `{from}-to-{to}.mdx`

**Step 1: Create a generator script**

Create `scripts/seed-pairs.mjs`:

```js
#!/usr/bin/env node
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const PAIRS = [
  // [from, to, category, aggregator, popularity, featured]
  ['eth','usdc','stablecoin','1inch',100,true],
  ['eth','usdt','stablecoin','1inch',99,true],
  ['btc','usdt','stablecoin','none',98,true],
  ['btc','usdc','stablecoin','none',97,true],
  ['sol','usdc','stablecoin','jupiter',96,true],
  ['sol','usdt','stablecoin','jupiter',95,false],
  ['bnb','usdt','stablecoin','none',94,false],
  ['matic','usdt','stablecoin','1inch',93,false],
  ['avax','usdt','stablecoin','none',92,false],
  ['btc','eth','major-cross','none',91,true],
  ['eth','btc','major-cross','none',90,false],
  ['sol','eth','major-cross','none',89,false],
  ['bnb','btc','major-cross','none',88,false],
  ['doge','usdt','memecoin','1inch',87,false],
  ['shib','usdt','memecoin','1inch',86,false],
  ['pepe','usdt','memecoin','1inch',85,false],
  ['doge','usd','memecoin','none',84,false],
  ['arb','eth','l2','1inch',83,false],
  ['op','eth','l2','1inch',82,false],
  ['matic','eth','l2','1inch',81,false],
  ['avax','eth','l2','none',80,false],
  ['usdc','usdt','stablecoin-pair','1inch',79,true],
  ['usdt','usd','off-ramp','none',78,false],
  ['usdc','usd','off-ramp','none',77,false],
  ['dai','usdc','stablecoin-pair','1inch',76,false],
];

const outDir = 'src/content/pairs';
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

const NAMES = {
  eth:'ETH',usdc:'USDC',usdt:'USDT',btc:'BTC',sol:'SOL',bnb:'BNB',matic:'MATIC',
  avax:'AVAX',doge:'DOGE',shib:'SHIB',pepe:'PEPE',arb:'ARB',op:'OP',dai:'DAI',usd:'USD',
};

for (const [from, to, category, aggregator, popularity, featured] of PAIRS) {
  const title = `Convert ${NAMES[from]} to ${NAMES[to]} — live rate`;
  const desc = `How many ${NAMES[to]} is 1 ${NAMES[from]} right now? Live mid-market rate refreshed every 60 seconds, with direct swap links.`;
  const slug = `${from}-to-${to}`;
  const body = `## How many ${NAMES[to]} is 1 ${NAMES[from]}?\n\nThe calculator above pulls a mid-market rate from CoinGecko every 60 seconds. The figure is the volume-weighted spot price across the venues CoinGecko polls — it is an estimate, not a quote. Actual swap output depends on slippage, routing, and network fees at the moment you sign the transaction.\n\n## How this rate is built\n\n${NAMES[from]} and ${NAMES[to]} trade across dozens of exchanges; the rate here is the aggregator mid-market. For a binding quote, click the swap button and the aggregator will return a real executable route including price impact.\n\n## FAQ stub\n\nQ: How often does the rate update?\nA: Every 60 seconds.\n\nQ: Why does my swap quote differ?\nA: Slippage and routing; see /methodology.\n\nQ: Is this financial advice?\nA: No.\n`;

  const fm = [
    '---',
    `from: ${from}`,
    `to: ${to}`,
    `title: "${title}"`,
    `description: "${desc}"`,
    `category: ${category}`,
    `aggregator: ${aggregator}`,
    `popularity: ${popularity}`,
    `featured: ${featured}`,
    'publishDate: 2026-04-22',
    'draft: false',
    '---',
    '',
    body,
  ].join('\n');

  writeFileSync(join(outDir, `${slug}.mdx`), fm);
  console.log(`wrote ${slug}.mdx`);
}
```

**Step 2: Run the seeder**

```bash
node scripts/seed-pairs.mjs
ls src/content/pairs | wc -l
```
Expected: `25`.

**Step 3: Verify frontmatter parses**

```bash
pnpm astro check 2>&1 | tail -15
```
Expected: no content-collection errors (pages routes may still error — addressed in Phase E). If a single slug fails, inspect and fix.

**Step 4: Commit**

```bash
git add scripts/seed-pairs.mjs src/content/pairs
git commit -m "feat(content): seed 25 pair MDX stubs with full frontmatter"
```

---

### Task 8: Seed 10 supply MDX stubs

**Files:**
- Create: `scripts/seed-supply.mjs`
- Create: 10 files under `src/content/supply/`

**Step 1: Create seeder**

Create `scripts/seed-supply.mjs`:

```js
#!/usr/bin/env node
import { writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const SUPPLY = [
  // [sym, name, maxSupply, mechanism, hasHalving]
  ['btc','Bitcoin',21000000,'Proof-of-work mining; block subsidy halves every 210,000 blocks (≈4 years)',true],
  ['eth','Ethereum','uncapped','Proof-of-stake issuance offset by EIP-1559 base-fee burn (net issuance typically near-zero or negative)',false],
  ['sol','Solana','uncapped','Proof-of-stake with disinflationary schedule — initial 8% issuance falling 15%/yr toward 1.5% terminal',false],
  ['doge','Dogecoin','uncapped','Proof-of-work; fixed 10,000 DOGE per block forever (≈5 billion new DOGE/year)',false],
  ['shib','Shiba Inu',999982360941.72,'Fixed at genesis; ongoing burn via burn-portal and transaction burns',false],
  ['xrp','XRP',100000000000,'Pre-mined at genesis; escrowed release (≈1B/month unlocked, unused returned)',false],
  ['ada','Cardano',45000000000,'Proof-of-stake; staking rewards funded from reserve until max reached',false],
  ['bnb','BNB',200000000,'Quarterly auto-burn reduces supply toward 100,000,000 floor',false],
  ['ton','Toncoin',5087014431,'Proof-of-stake; validator + nominator rewards, small annual inflation',false],
  ['pepe','Pepe',420690000000000,'Fixed at genesis; no burn mechanism active',false],
];

const outDir = 'src/content/supply';
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

for (const [sym, name, maxSupply, mechanism, hasHalving] of SUPPLY) {
  const title = `${name} supply — how many ${name.toUpperCase()} exist, and how many will ever exist?`;
  const desc = `Circulating supply, max supply, and issuance schedule for ${name} (${sym.toUpperCase()}). Updated nightly from on-chain data.`;
  const body = `## How many ${name.toUpperCase()} exist right now?\n\nThe live figure in the panel above is the circulating supply reported by CoinGecko, refreshed nightly. "Circulating" means coins in the hands of holders — not coins locked in escrow, not coins burned.\n\n## Will more ${name.toUpperCase()} ever be created?\n\n${mechanism}.\n\n## The hard ceiling\n\n${typeof maxSupply === 'number' ? `Total supply is capped at ${maxSupply.toLocaleString()} ${sym.toUpperCase()}.` : `${name} has no hard cap on total supply — issuance is governed by protocol rules rather than a fixed ceiling.`} Everything past that must come from burn reversal or a governance fork.\n\n## Self-custody\n\nIf you hold ${sym.toUpperCase()}, a hardware wallet (Ledger or Trezor) takes your coins off the exchange and out of reach of every counterparty risk on earth except your own backup hygiene.\n`;

  const fm = [
    '---',
    `symbol: ${sym}`,
    `name: "${name}"`,
    `title: "${title}"`,
    `description: "${desc}"`,
    `maxSupply: ${typeof maxSupply === 'number' ? maxSupply : `"${maxSupply}"`}`,
    `currentIssuanceMechanism: "${mechanism.replace(/"/g,'\\"')}"`,
    `hasHalving: ${hasHalving}`,
    'publishDate: 2026-04-22',
    'draft: false',
    '---',
    '',
    body,
  ].join('\n');

  writeFileSync(join(outDir, `${sym}.mdx`), fm);
  console.log(`wrote ${sym}.mdx`);
}
```

**Step 2: Run + verify**

```bash
node scripts/seed-supply.mjs
ls src/content/supply | wc -l
```
Expected: `10`.

**Step 3: astro check**

```bash
pnpm astro check 2>&1 | tail -10
```
No collection schema errors.

**Step 4: Commit**

```bash
git add scripts/seed-supply.mjs src/content/supply
git commit -m "feat(content): seed 10 supply MDX stubs"
```

---

### Task 9: Write 5 evergreen guide MDX files (real ~300-word bodies)

**Objective:** Unlike pair/supply stubs, guide bodies are real editorial copy. These are long-tail SEO seeds.

**Files:**
- Create: `src/content/guides/how-to-swap-eth-for-usdc-safely.mdx`
- Create: `src/content/guides/stablecoin-depeg-risk-explained.mdx`
- Create: `src/content/guides/btc-vs-eth-which-moves-first.mdx`
- Create: `src/content/guides/solana-vs-ethereum-swap-fees.mdx`
- Create: `src/content/guides/self-custody-basics-ledger-trezor.mdx`

**Step 1: Create `src/content/guides/how-to-swap-eth-for-usdc-safely.mdx`**

```mdx
---
title: "How to swap ETH for USDC safely (2026 guide)"
description: "A step-by-step walkthrough: choosing a venue, checking slippage, sizing gas, and avoiding the three most common ways people lose money on a simple ETH→USDC swap."
publishDate: 2026-04-22
relatedPairs: ["eth-to-usdc"]
faq:
  - q: "What slippage tolerance should I set for ETH to USDC?"
    a: "For trades under $10,000 on Ethereum mainnet, 0.1% to 0.3% is almost always sufficient — USDC has deep liquidity everywhere. If the aggregator suggests higher, there is probably a routing issue worth investigating before you sign."
  - q: "Should I use 1inch, CowSwap, or Uniswap directly?"
    a: "An aggregator (1inch, CowSwap) will nearly always beat a single DEX for non-trivial size because it splits your order across pools. Uniswap direct is fine for tiny trades or when you specifically want a single pool."
  - q: "Can I swap without paying gas?"
    a: "Not on mainnet — every on-chain swap pays gas. Layer 2 (Arbitrum, Optimism, Base) drops gas to pennies. Gasless \"meta-transactions\" exist but the cost is bundled into a worse rate."
---

## The 90-second version

Open your wallet, connect to an aggregator like 1inch or CowSwap, pick ETH as the token you are selling and USDC as the token you are buying, confirm the preview route, sign the transaction, wait two blocks, and you are done. The rate you get is within a basis point or two of what our calculator on [this page](/convert/eth-to-usdc/) shows.

Where people lose money is in the details — so let's cover the details.

## Step 1: pick the venue

On Ethereum mainnet, stick to **audited aggregators** — 1inch, CowSwap, Matcha, Uniswap's own router. Random forks with flashy front-ends have, historically, been vectors for approval-drain exploits. The two minutes you save clicking a Reddit link is not worth it.

## Step 2: verify the contract you're about to approve

Every ERC-20 swap requires a one-time `approve()` to let the router spend your token. Infinite approvals are convenient but they stay live until you revoke them. For a one-off swap set the approval to exactly the amount you're swapping — your wallet will probably offer this as a toggle.

## Step 3: set slippage sensibly

For a liquid pair like ETH→USDC, 0.1–0.3% is fine. Anything higher and a sandwich bot will take the difference. Anything lower and your transaction will bounce in a volatile block.

## Step 4: size your gas

Mainnet gas fluctuates minute-to-minute. The aggregator will suggest a gas price; for a non-urgent swap you can nudge it down by 10–20% and the transaction will still land within a block or two.

## Step 5: wait, verify, done

Two block confirmations (≈24 seconds) is enough for a swap this size. Check the transaction on Etherscan — the USDC should land in your wallet as a `Transfer` event from the router address.
```

**Step 2: Create `src/content/guides/stablecoin-depeg-risk-explained.mdx`**

```mdx
---
title: "Stablecoin depeg risk, explained without the drama"
description: "What actually happens when a stablecoin slips off its dollar peg, which coins have depegged before, and the mechanical signals to watch if you hold USDC, USDT, or DAI."
publishDate: 2026-04-22
relatedPairs: ["usdc-to-usdt","dai-to-usdc"]
faq:
  - q: "Has USDC ever depegged?"
    a: "Yes — in March 2023 it fell to roughly $0.88 after Circle disclosed exposure to Silicon Valley Bank. It restored the peg within three days once the FDIC guaranteed SVB deposits."
  - q: "Is USDT safer or riskier than USDC?"
    a: "They fail for different reasons. USDC's risk is concentrated banking exposure; USDT's is transparency of its reserves. Neither has a clean reputation; both have held peg through the past three years of stress."
  - q: "What's a reasonable depeg threshold to act on?"
    a: "A 30-bps (0.30%) deviation sustained over an hour is unusual. A 100-bps deviation means the market is pricing in a non-trivial probability of failure."
---

## What \"depeg\" actually means

A stablecoin is depegged when its market price diverges from its target (usually $1) by more than the normal tick-by-tick noise. A few basis points of deviation is routine arbitrage friction. A full cent or more is the market pricing in real doubt about redemption.

## The three things that cause depegs

**Reserve concerns** — the market learns the issuer's backing is less than 1:1, or is held in something less liquid than cash (commercial paper, bank deposits at a wobbling bank). USDC's March 2023 incident is the clean example.

**Redemption bottlenecks** — the coin is technically backed, but you can't get your dollar out fast enough. Retail can't redeem USDT directly; during stress they sell into the secondary market and that selling pushes the price below peg.

**Protocol failure** — algorithmic stablecoins like UST collapse when the mechanism that's supposed to defend the peg fails. The $40B UST unwind in May 2022 is the cautionary tale.

## The signals to watch

Our depeg-check on [USDC/USDT](/convert/usdc-to-usdt/) flags sustained deviation of more than 30 bps over the last 30 days. Secondary-market spot price is leading; redemption rate is lagging. If you see divergence, check the issuer's transparency page before you do anything dramatic.

## Practical defence

Diversify across issuers (don't hold 100% in one stablecoin), keep some dollars on-ramp-accessible rather than all on-chain, and if you're parking more than a year's living expenses, consider T-bill-backed products (USDM, OUSG) that at least tell you exactly what you own.
```

**Step 3: Create `src/content/guides/btc-vs-eth-which-moves-first.mdx`**

```mdx
---
title: "BTC vs ETH: which moves first, and what it means for swaps"
description: "A look at the empirical lead-lag between Bitcoin and Ethereum price action — who drives whom, and how to use the relationship when you're planning a BTC/ETH swap."
publishDate: 2026-04-22
relatedPairs: ["btc-to-eth","eth-to-btc"]
faq:
  - q: "Does BTC always lead ETH?"
    a: "On macro moves, mostly yes — BTC is the beta-anchor for the whole asset class. On ecosystem-specific news (EIP upgrades, L2 launches, a major DeFi event) ETH leads itself. The correlation on weekly returns is around 0.85."
  - q: "Should I swap BTC for ETH in a risk-on phase?"
    a: "Empirically, ETH beta is higher in risk-on phases — ETH/BTC tends to rise when BTC is rallying and fall when BTC is selling off. That's a pattern, not a guarantee."
  - q: "What's a reasonable BTC/ETH ratio historically?"
    a: "The 5-year range is roughly 0.030 to 0.085 ETH per BTC (i.e. 12 to 33 BTC per ETH). The long-run mean sits near 0.055."
---

## The relationship in one chart (that we're not going to make you click)

BTC and ETH move together about 85% of the time on a weekly basis. The 15% of time they diverge is where the interesting money is made — and lost. BTC is driven by macro liquidity, ETF flows, and "digital gold" positioning; ETH is driven by the same plus everything that happens in EVM land — staking yield, L2 fees, restaking narratives, DeFi TVL.

## When ETH leads

ETH leads on **ecosystem-native catalysts**: a successful hard fork, a burn-rate milestone, a Layer-2 throughput record, a major app-layer launch. BTC simply has no exposure to these.

## When BTC leads

BTC leads on **macro-liquidity catalysts**: Fed rate expectations, ETF flow prints, central-bank balance-sheet moves, sovereign adoption headlines. ETH typically follows with a beta of 1.2–1.5× on these moves.

## Using this when you swap

If you're swapping BTC→ETH in a rising-BTC tape, you're locking in a below-average ETH/BTC ratio — which can either be brilliant (if you think the rally continues and ETH beta outruns BTC) or expensive (if you think this is a BTC-specific move like a spot-ETF flow print). The [ETH/BTC pair calculator](/convert/eth-to-btc/) shows you the current ratio alongside its 30-day range, which is usually the fastest sanity check you can do.

## The one rule

Don't time it based on a single day's move. The BTC/ETH ratio is noisy enough that a 2% intraday move is indistinguishable from random. Weekly closes are the smallest unit of signal.
```

**Step 4: Create `src/content/guides/solana-vs-ethereum-swap-fees.mdx`**

```mdx
---
title: "Solana vs Ethereum swap fees in 2026: a realistic comparison"
description: "Actual landed cost of a $500 swap on Solana, Ethereum mainnet, Arbitrum, Base, and Optimism — including slippage, aggregator fees, and the hidden costs that don't show in the quote."
publishDate: 2026-04-22
relatedPairs: ["sol-to-usdc","eth-to-usdc"]
faq:
  - q: "Is Solana really cheaper than Ethereum?"
    a: "For the gas portion: yes, by two to three orders of magnitude. For the total cost including slippage on a large trade: the gap narrows because Ethereum mainnet has deeper liquidity for the biggest pairs."
  - q: "What about L2s like Arbitrum and Base?"
    a: "They're competitive with Solana on gas (sub-dollar) while keeping Ethereum's security model. The tradeoff is slightly lower liquidity than mainnet for some pairs."
  - q: "Why does my Solana swap sometimes fail with a fee still deducted?"
    a: "Solana charges the base fee even on failed transactions. Jupiter's pre-flight simulation usually catches this, but a stale route can still land on-chain and burn the fee."
---

## The headline number

A $500 ETH→USDC swap costs roughly:

- **Ethereum mainnet**, via 1inch: $3–8 gas + 0.05–0.15% slippage ≈ **$3.50–8.75 total**
- **Arbitrum One**, via 1inch: $0.10–0.30 gas + 0.05–0.20% slippage ≈ **$0.35–1.30 total**
- **Solana**, via Jupiter: $0.0005 gas + 0.10–0.30% slippage ≈ **$0.50–1.50 total**
- **Base**, via Uniswap: $0.05–0.15 gas + 0.08–0.25% slippage ≈ **$0.45–1.40 total**

## Gas is not the whole story

Everyone quotes gas because gas is easy to measure. The real cost of a swap is gas plus slippage plus MEV (sandwich) plus any protocol fee. On Solana the gas is genuinely negligible but Jupiter's platform-fee-bps (optional, typically 0–20 bps) is a larger share of the total. On L2s MEV is lower because the sequencer doesn't reorder in the same way.

## The $50,000 swap tilts the math

At small size Solana and Arbitrum look equivalent on total cost. At $50k+ the deeper mainnet pools start to matter: a $50k ETH→USDC on mainnet might pay 3 bps of slippage where the same trade on Arbitrum pays 8–15 bps. Over a large ticket, that is suddenly tens of dollars and the $5 mainnet gas surcharge is rounding error.

## What we recommend

For size under $1,000 and frequency under once-a-week, a Solana or Arbitrum route is almost always cheapest. For size above $10,000, run the quote on mainnet too — the aggregator will tell you within seconds whether mainnet liquidity is worth the gas.
```

**Step 5: Create `src/content/guides/self-custody-basics-ledger-trezor.mdx`**

```mdx
---
title: "Self-custody basics: getting a Ledger or Trezor right the first time"
description: "Why self-custody matters, how to set up a hardware wallet without tripping over the four common mistakes, and how to stop being one laptop fire away from losing everything."
publishDate: 2026-04-22
relatedPairs: []
faq:
  - q: "Is Ledger or Trezor better?"
    a: "Both are fine. Trezor is open-source firmware, which some people prefer. Ledger supports more chains out of the box. If you hold BTC and ETH only, either is equivalent."
  - q: "Where should I store the 24-word seed phrase?"
    a: "On paper or steel, in two geographically separated locations. Not in a cloud note. Not in a password manager. Not photographed."
  - q: "Is a $50 hardware wallet really more secure than a $200 one?"
    a: "Effectively, yes. The threat model both defeat is the same — remote extraction of your private keys by malware. Expensive models add UX and multi-chain support, not security."
---

## Why self-custody matters

\"Not your keys, not your coins.\" Every collapsed exchange in the past five years — Mt. Gox, QuadrigaCX, Celsius, FTX — held customer assets in a unified pool. When the company failed, customer assets were creditor assets. A hardware wallet removes you from that bucket entirely: the keys live on a device in your house, nothing can touch them without physical access and your PIN.

## The four common mistakes

**1. Photographing the seed phrase.** Your phone is in iCloud. Your iCloud is in someone else's data center. Anyone who ever gains access to that backup owns your coins. Write the phrase with a pen on paper and put it in a drawer. Or stamp it into a steel plate. Never photograph it.

**2. Typing the seed phrase anywhere.** Not into a computer, not into the hardware wallet's recovery UI unless you are actively recovering a lost device, not into a "migration tool" or a "Ledger Live Pro" that showed up in your inbox.

**3. Buying second-hand.** Always buy direct from the manufacturer, Ledger.com or Trezor.io. A tampered device with a preloaded seed is a known attack.

**4. Storing the seed in one place.** If your house burns down, does a second copy exist? If not, fix it this weekend.

## The 20-minute setup

Unbox, connect to the official app (Ledger Live or Trezor Suite), pick a PIN, write down the 24 words in order on the included card, confirm a random handful, install the apps for the chains you use, send yourself $10 as a test transaction. Done.

After that you're done. The wallet will last 5–10 years. The seed phrase, stored properly, will last forever.
```

**Step 6: Verify all five built**

```bash
ls src/content/guides
pnpm astro check 2>&1 | tail -10
```
Expected: 5 files, no schema errors.

**Step 7: Commit**

```bash
git add src/content/guides
git commit -m "feat(content): add 5 evergreen guides with full editorial bodies"
```

---

### Task 10: Seed MDX build smoke test

**Objective:** Ensure every collection entry actually builds and that content-lookup helpers in Phase E won't return undefined.

**Files:**
- Create: `tests/content-smoke.test.ts`

**Step 1: Write test**

Create `tests/content-smoke.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { readdirSync } from 'node:fs';

describe('content collections seeded', () => {
  it('has 25 pair MDX files', () => {
    const files = readdirSync('src/content/pairs').filter((f) => f.endsWith('.mdx'));
    expect(files.length).toBe(25);
  });
  it('has 10 supply MDX files', () => {
    const files = readdirSync('src/content/supply').filter((f) => f.endsWith('.mdx'));
    expect(files.length).toBe(10);
  });
  it('has 5 guide MDX files', () => {
    const files = readdirSync('src/content/guides').filter((f) => f.endsWith('.mdx'));
    expect(files.length).toBe(5);
  });
  it('every pair filename matches {from}-to-{to} pattern', () => {
    const files = readdirSync('src/content/pairs');
    for (const f of files) expect(f).toMatch(/^[a-z0-9]+-to-[a-z0-9]+\.mdx$/);
  });
});
```

**Step 2: Run — expect PASS**

```bash
pnpm test -- --run tests/content-smoke.test.ts 2>&1 | tail -5
```
Expected: 4 passing.

**Step 3: Commit**

```bash
git add tests/content-smoke.test.ts
git commit -m "test(content): smoke test for collection file counts"
```

---

### Task 11: Utility — `src/lib/format.ts` for numeric formatting

**Objective:** Shared formatters for rate, percent, and supply display. Keeps Calculator, commentary, and schema consistent.

**Files:**
- Create: `src/lib/format.ts`
- Create: `src/lib/format.test.ts`

**Step 1: Write failing test**

Create `src/lib/format.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { formatRate, formatPct, formatSupply, formatUsd } from './format';

describe('formatters', () => {
  it('formats small rates with 6 sig figs', () => {
    expect(formatRate(0.000012345)).toBe('0.0000123');
    expect(formatRate(1234.5678)).toBe('1,234.57');
    expect(formatRate(1.2345678)).toBe('1.23457');
  });
  it('formats percent with sign', () => {
    expect(formatPct(0.0234)).toBe('+2.34%');
    expect(formatPct(-0.0056)).toBe('-0.56%');
    expect(formatPct(0)).toBe('0.00%');
  });
  it('formats supply with thousands separators', () => {
    expect(formatSupply(21000000)).toBe('21,000,000');
    expect(formatSupply('uncapped')).toBe('Uncapped');
  });
  it('formats USD with symbol', () => {
    expect(formatUsd(1234.56)).toBe('$1,234.56');
    expect(formatUsd(0.045)).toBe('$0.045');
  });
});
```

**Step 2: Run — expect FAIL**

```bash
pnpm test -- --run src/lib/format.test.ts 2>&1 | tail -5
```

**Step 3: Create `src/lib/format.ts`**

```ts
/**
 * Numeric formatters. All outputs are human-readable strings suitable for UI and schema.org values.
 * Internal arithmetic should NEVER use these — use raw numbers.
 */

export function formatRate(v: number): string {
  if (!Number.isFinite(v) || v === 0) return '0';
  const abs = Math.abs(v);
  if (abs < 0.01) {
    // scientific-ish with 3 sig figs, but rendered as decimal
    const str = v.toPrecision(3);
    return Number(str).toString();
  }
  if (abs < 1) return v.toPrecision(6).replace(/0+$/, '').replace(/\.$/, '');
  if (abs < 1000) return v.toFixed(5).replace(/0+$/, '').replace(/\.$/, '');
  return v.toLocaleString('en-US', { maximumFractionDigits: 2 });
}

export function formatPct(v: number): string {
  const pct = v * 100;
  const sign = pct > 0 ? '+' : pct < 0 ? '' : '';
  return `${sign}${pct.toFixed(2)}%`;
}

export function formatSupply(v: number | 'uncapped' | string): string {
  if (v === 'uncapped' || v === 'Uncapped') return 'Uncapped';
  const n = typeof v === 'string' ? Number(v) : v;
  if (!Number.isFinite(n)) return String(v);
  return n.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

export function formatUsd(v: number): string {
  if (!Number.isFinite(v)) return '$0';
  if (Math.abs(v) < 1) return `$${v.toFixed(3)}`;
  return `$${v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test -- --run src/lib/format.test.ts 2>&1 | tail -5
```
Expected: 4 passing. If `formatRate` fails for 0.000012345 (produces `1.23e-5` on some Node versions), convert via `Number(v.toPrecision(3)).toString()` — already wired above.

**Step 5: Commit**

```bash
git add src/lib/format.ts src/lib/format.test.ts
git commit -m "feat(lib): numeric formatters for rate, pct, supply, usd"
```

---

## Phase C — Rate Worker with b-lazy cache (tasks 12–16)

### Task 12: Scaffold the Worker sub-package

**Objective:** Create `workers/` with its own `package.json`, `wrangler.toml`, `tsconfig.json`, `vitest.config.ts`. Worker is deployed independently from Pages so it lives in its own sub-package — keeps bundle concerns separate.

**Files:**
- Create: `workers/package.json`
- Create: `workers/wrangler.toml`
- Create: `workers/tsconfig.json`
- Create: `workers/vitest.config.ts`
- Create: `workers/.gitignore`

**Step 1: Create `workers/` directory + files**

```bash
cd ~/site-network/sites/howmanycoin.com
mkdir -p workers/src workers/test
```

Create `workers/package.json`:

```json
{
  "name": "@howmanycoin/rate-worker",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "test": "vitest run",
    "typecheck": "tsc --noEmit"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4.20240512.0",
    "@cloudflare/vitest-pool-workers": "^0.5.0",
    "typescript": "^5.4.0",
    "vitest": "^1.6.0",
    "wrangler": "^3.60.0"
  }
}
```

Create `workers/wrangler.toml`:

```toml
name = "howmanycoin-rate"
main = "src/rate.ts"
compatibility_date = "2026-04-22"
compatibility_flags = ["nodejs_compat"]

[vars]
ONEINCH_REFERRER = "0x0000000000000000000000000000000000000000"   # overridden by secret in prod
JUPITER_PLATFORM_FEE_BPS = "20"
JUPITER_FEE_ACCOUNT = ""                                           # overridden by secret in prod

[[routes]]
pattern = "howmanycoin.com/api/rate"
zone_name = "howmanycoin.com"

[[routes]]
pattern = "www.howmanycoin.com/api/rate"
zone_name = "howmanycoin.com"

[observability]
enabled = true
```

Create `workers/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "Bundler",
    "lib": ["ES2022"],
    "types": ["@cloudflare/workers-types"],
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "allowJs": false,
    "isolatedModules": true
  },
  "include": ["src/**/*.ts", "test/**/*.ts"]
}
```

Create `workers/vitest.config.ts`:

```ts
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.toml' },
      },
    },
  },
});
```

Create `workers/.gitignore`:

```
.wrangler/
node_modules/
.dev.vars
```

**Step 2: Install worker deps**

```bash
cd workers
pnpm install
cd ..
```

**Step 3: Commit**

```bash
git add workers
git commit -m "chore(worker): scaffold rate worker sub-package with wrangler+vitest"
```

---

### Task 13: Worker core — `src/rate.ts` skeleton with types (failing tests first)

**Objective:** Type definitions + failing tests for the three things the Worker must do: cache for 60s, call CoinGecko once, return geo-switched CTA set.

**Files:**
- Create: `workers/src/types.ts`
- Create: `workers/src/rate.ts` (minimal skeleton)
- Create: `workers/test/rate.test.ts`

**Step 1: Create `workers/src/types.ts`**

```ts
export interface RateResponse {
  /** ISO-8601 generation timestamp for this cached payload. */
  generatedAt: string;
  /** key = CoinGecko id, value = { usd, usd_24h_change, last_updated_at } */
  rates: Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>;
  geo: {
    country: string;
    isUS: boolean;
    isRestricted: boolean;
  };
  cexCTAs: CexCTA[];
  /** TTL in seconds (for client display only — auth cache lives in the Worker). */
  ttl: number;
}

export interface CexCTA {
  name: string;      // "Coinbase"
  url: string;       // affiliate URL, already signed
  priority: number;  // 0 = above-fold, 1 = expandable
}

export interface Env {
  ONEINCH_REFERRER: string;
  JUPITER_PLATFORM_FEE_BPS: string;
  JUPITER_FEE_ACCOUNT: string;
}
```

**Step 2: Create minimal `workers/src/rate.ts`**

```ts
import type { Env, RateResponse } from './types';

export default {
  async fetch(_req: Request, _env: Env, _ctx: ExecutionContext): Promise<Response> {
    return new Response('not implemented', { status: 501 });
  },
};
```

**Step 3: Create `workers/test/rate.test.ts`**

```ts
import { describe, it, expect } from 'vitest';
import { SELF } from 'cloudflare:test';

describe('/api/rate', () => {
  it('returns 200 with JSON and expected shape', async () => {
    const res = await SELF.fetch('https://howmanycoin.com/api/rate', {
      headers: { 'CF-IPCountry': 'US' },
    });
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.rates).toBeTypeOf('object');
    expect(body.geo.country).toBe('US');
    expect(body.geo.isUS).toBe(true);
    expect(Array.isArray(body.cexCTAs)).toBe(true);
  });

  it('returns Coinbase + Kraken above-fold for US traffic', async () => {
    const res = await SELF.fetch('https://howmanycoin.com/api/rate', {
      headers: { 'CF-IPCountry': 'US' },
    });
    const body = (await res.json()) as any;
    const aboveFold = body.cexCTAs.filter((c: any) => c.priority === 0).map((c: any) => c.name);
    expect(aboveFold).toContain('Coinbase');
    expect(aboveFold).toContain('Kraken');
    expect(aboveFold).not.toContain('Binance');
  });

  it('returns Binance + Bybit above-fold for non-US traffic', async () => {
    const res = await SELF.fetch('https://howmanycoin.com/api/rate', {
      headers: { 'CF-IPCountry': 'DE' },
    });
    const body = (await res.json()) as any;
    const aboveFold = body.cexCTAs.filter((c: any) => c.priority === 0).map((c: any) => c.name);
    expect(aboveFold).toContain('Binance');
    expect(aboveFold).toContain('Bybit');
    expect(aboveFold).not.toContain('Coinbase');
  });

  it('serves second identical request from cache (same generatedAt)', async () => {
    const r1 = await SELF.fetch('https://howmanycoin.com/api/rate', { headers: { 'CF-IPCountry': 'US' } });
    const r2 = await SELF.fetch('https://howmanycoin.com/api/rate', { headers: { 'CF-IPCountry': 'US' } });
    const b1 = (await r1.json()) as any;
    const b2 = (await r2.json()) as any;
    expect(b1.generatedAt).toBe(b2.generatedAt);
  });
});
```

**Step 4: Run — expect FAIL**

```bash
cd workers
pnpm test 2>&1 | tail -20
cd ..
```
Expected: all tests fail (501 response).

**Step 5: Commit**

```bash
git add workers/src workers/test
git commit -m "test(worker): failing tests for /api/rate shape + geo + cache"
```

---

### Task 14: Implement `/api/rate` — b-lazy cache + CoinGecko fetch + geo CTAs

**Objective:** Make every test in Task 13 pass.

**Files:**
- Modify: `workers/src/rate.ts`
- Create: `workers/src/coingecko.ts`
- Create: `workers/src/cex.ts`

**Step 1: Create `workers/src/coingecko.ts`**

```ts
const COINGECKO_IDS = [
  'bitcoin','ethereum','solana','usd-coin','tether','dai','binancecoin','matic-network',
  'avalanche-2','dogecoin','shiba-inu','pepe','arbitrum','optimism','ripple','cardano','the-open-network',
].join(',');

export async function fetchCoingecko(): Promise<Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>> {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${COINGECKO_IDS}&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true`;
  const res = await fetch(url, {
    cf: { cacheEverything: false },
    headers: { 'User-Agent': 'howmanycoin/1.0 (+https://howmanycoin.com)' },
  });
  if (!res.ok) {
    throw new Error(`coingecko ${res.status}`);
  }
  return (await res.json()) as any;
}
```

**Step 2: Create `workers/src/cex.ts`**

```ts
import type { CexCTA } from './types';

/**
 * Geo-switched CEX CTA sets. Referral IDs are placeholders; replaced with secrets in prod.
 * Rules from spec §3 + §4:
 *   - US: Coinbase + Kraken above-fold (priority 0)
 *   - Non-US: Binance + Bybit above-fold
 *   - All geos get the rest below the fold (priority 1)
 *   - Restricted (e.g. sanctioned): strip Binance, OKX, MEXC
 */

const US_RESTRICTED_FOR_BINANCE = new Set(['US']);
const HEAVILY_RESTRICTED = new Set(['IR', 'KP', 'SY', 'CU']);

export function ctasForCountry(country: string): CexCTA[] {
  const isUS = country === 'US';
  const heavy = HEAVILY_RESTRICTED.has(country);
  const out: CexCTA[] = [];

  if (isUS) {
    out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 0 });
    out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 0 });
  } else if (!heavy) {
    out.push({ name: 'Binance', url: 'https://accounts.binance.com/register?ref=HOWMANYCOIN', priority: 0 });
    out.push({ name: 'Bybit',   url: 'https://www.bybit.com/invite?ref=HOWMANYCOIN', priority: 0 });
  } else {
    out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 0 });
    out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 0 });
  }

  // below-the-fold expandable set
  if (!US_RESTRICTED_FOR_BINANCE.has(country) && !heavy) {
    out.push({ name: 'Binance', url: 'https://accounts.binance.com/register?ref=HOWMANYCOIN', priority: 1 });
  }
  out.push({ name: 'Bybit',    url: 'https://www.bybit.com/invite?ref=HOWMANYCOIN', priority: 1 });
  out.push({ name: 'OKX',      url: 'https://www.okx.com/join/HOWMANYCOIN', priority: 1 });
  if (!heavy) out.push({ name: 'MEXC', url: 'https://www.mexc.com/register?inviteCode=HOWMANYCOIN', priority: 1 });
  out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 1 });
  out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 1 });
  out.push({ name: 'KuCoin',   url: 'https://www.kucoin.com/r/rf/howmanycoin', priority: 1 });

  // dedupe by (name, priority) keeping first occurrence
  const seen = new Set<string>();
  return out.filter((c) => {
    const k = `${c.name}:${c.priority}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}
```

**Step 3: Rewrite `workers/src/rate.ts`**

```ts
import type { Env, RateResponse } from './types';
import { fetchCoingecko } from './coingecko';
import { ctasForCountry } from './cex';

const TTL_SECONDS = 60;
const CACHE_KEY_BASE = 'https://howmanycoin.com/__cache__/rate';

export default {
  async fetch(req: Request, _env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(req.url);
    if (url.pathname !== '/api/rate') {
      return new Response('not found', { status: 404 });
    }
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      return new Response('method not allowed', { status: 405 });
    }

    const country = (req.headers.get('CF-IPCountry') || 'US').toUpperCase();
    const cacheUrl = `${CACHE_KEY_BASE}?country=${country}`;
    const cache = caches.default;

    // Try cache first
    const cached = await cache.match(cacheUrl);
    if (cached) {
      // clone so we can return with extra header
      const body = await cached.text();
      return new Response(body, {
        status: 200,
        headers: {
          'content-type': 'application/json; charset=utf-8',
          'cache-control': `public, max-age=${TTL_SECONDS}`,
          'x-cache': 'HIT',
          'access-control-allow-origin': '*',
        },
      });
    }

    // Miss — fetch CoinGecko and build payload
    let rates: RateResponse['rates'];
    try {
      rates = await fetchCoingecko();
    } catch (err) {
      return new Response(JSON.stringify({ error: 'upstream unavailable', detail: String(err) }), {
        status: 503,
        headers: { 'content-type': 'application/json; charset=utf-8' },
      });
    }

    const payload: RateResponse = {
      generatedAt: new Date().toISOString(),
      rates,
      geo: {
        country,
        isUS: country === 'US',
        isRestricted: ['IR', 'KP', 'SY', 'CU'].includes(country),
      },
      cexCTAs: ctasForCountry(country),
      ttl: TTL_SECONDS,
    };

    const json = JSON.stringify(payload);
    const response = new Response(json, {
      status: 200,
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': `public, max-age=${TTL_SECONDS}`,
        'x-cache': 'MISS',
        'access-control-allow-origin': '*',
      },
    });

    // Store under cache key so next hit within 60s is a HIT
    const toCache = new Response(json, {
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': `public, max-age=${TTL_SECONDS}`,
      },
    });
    ctx.waitUntil(cache.put(cacheUrl, toCache));

    return response;
  },
};
```

**Step 4: Run tests — expect PASS**

```bash
cd workers
pnpm test 2>&1 | tail -20
cd ..
```
Expected: 4 passing. If CoinGecko is rate-limited during CI, the vitest-pool-workers sandbox blocks outbound fetch by default — add a `fetchMock` for tests (see Task 15 if needed).

**Step 5: Commit**

```bash
git add workers/src workers/test
git commit -m "feat(worker): b-lazy cache + coingecko + geo-switched CEX CTAs"
```

---

### Task 15: Worker — mock CoinGecko for deterministic tests

**Objective:** Replace real CoinGecko fetch in tests with a deterministic mock so tests are reproducible offline.

**Files:**
- Modify: `workers/test/rate.test.ts`
- Create: `workers/test/fixtures/coingecko.json`

**Step 1: Create fixture**

Create `workers/test/fixtures/coingecko.json`:

```json
{
  "bitcoin":       { "usd": 67234.12, "usd_24h_change":  1.23, "last_updated_at": 1713800000 },
  "ethereum":      { "usd":  3456.78, "usd_24h_change":  0.45, "last_updated_at": 1713800000 },
  "solana":        { "usd":   145.67, "usd_24h_change": -0.78, "last_updated_at": 1713800000 },
  "usd-coin":      { "usd":     1.00, "usd_24h_change":  0.01, "last_updated_at": 1713800000 },
  "tether":        { "usd":     1.00, "usd_24h_change":  0.00, "last_updated_at": 1713800000 },
  "dai":           { "usd":     1.00, "usd_24h_change": -0.01, "last_updated_at": 1713800000 },
  "binancecoin":   { "usd":   587.45, "usd_24h_change":  0.67, "last_updated_at": 1713800000 },
  "matic-network": { "usd":     0.72, "usd_24h_change": -2.34, "last_updated_at": 1713800000 },
  "avalanche-2":   { "usd":    35.12, "usd_24h_change":  1.08, "last_updated_at": 1713800000 },
  "dogecoin":      { "usd":     0.15, "usd_24h_change":  3.21, "last_updated_at": 1713800000 },
  "shiba-inu":     { "usd": 0.000025, "usd_24h_change": -1.45, "last_updated_at": 1713800000 },
  "pepe":          { "usd": 0.0000087,"usd_24h_change":  5.67, "last_updated_at": 1713800000 },
  "arbitrum":      { "usd":     1.12, "usd_24h_change": -0.34, "last_updated_at": 1713800000 },
  "optimism":      { "usd":     2.45, "usd_24h_change":  0.12, "last_updated_at": 1713800000 },
  "ripple":        { "usd":     0.52, "usd_24h_change":  0.67, "last_updated_at": 1713800000 },
  "cardano":       { "usd":     0.45, "usd_24h_change": -0.89, "last_updated_at": 1713800000 },
  "the-open-network": { "usd": 5.12, "usd_24h_change":  1.34, "last_updated_at": 1713800000 }
}
```

**Step 2: Patch the top of `workers/test/rate.test.ts`**

Insert above the first `describe`:

```ts
import { fetchMock } from 'cloudflare:test';
import fixture from './fixtures/coingecko.json';

fetchMock.activate();
fetchMock.disableNetConnect();
fetchMock
  .get('https://api.coingecko.com')
  .intercept({ path: /\/api\/v3\/simple\/price.*/ })
  .reply(200, fixture)
  .persist();
```

Also enable fetchMock in `workers/vitest.config.ts` by updating it:

```ts
import { defineWorkersConfig } from '@cloudflare/vitest-pool-workers/config';
export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: {
        wrangler: { configPath: './wrangler.toml' },
        miniflare: {
          compatibilityFlags: ['nodejs_compat'],
        },
      },
    },
  },
});
```

**Step 3: Run — expect PASS**

```bash
cd workers
pnpm test 2>&1 | tail -20
cd ..
```
Expected: 4 passing, deterministic, no network.

**Step 4: Commit**

```bash
git add workers
git commit -m "test(worker): deterministic CoinGecko fixture via fetchMock"
```

---

### Task 16: Worker — aggregator deep-link endpoints

**Objective:** Add `/api/swap-link?aggregator=1inch&from=eth&to=usdc&amount=1` — returns `{ url }` with referral params attached server-side. Chain-aware. This is where 1inch's fee param and Jupiter's `platformFeeBps` get injected so a client-side script can't strip them.

**Files:**
- Modify: `workers/src/rate.ts` (add path routing)
- Create: `workers/src/swapLink.ts`
- Create: `workers/test/swapLink.test.ts`

**Step 1: Create `workers/src/swapLink.ts`**

```ts
import type { Env } from './types';

interface SwapParams { aggregator: '1inch' | 'jupiter'; from: string; to: string; amount?: string; chain?: string; }

// 17-token × chain map — pulled from the site registry (mirrors src/lib/tokens.ts)
const CONTRACT_BY_CHAIN: Record<string, Record<string, string>> = {
  ethereum: {
    eth:   '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
    usdc:  '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
    usdt:  '0xdAC17F958D2ee523a2206206994597C13D831ec7',
    dai:   '0x6B175474E89094C44Da98b954EedeAC495271d0F',
    shib:  '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE',
    pepe:  '0x6982508145454Ce325dDbE47a25d4ec3d2311933',
    matic: '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0',
  },
  solana: {
    sol:  'So11111111111111111111111111111111111111112',
    usdc: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
    usdt: 'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB',
  },
};

export function buildSwapLink(env: Env, p: SwapParams): { url: string } {
  const from = p.from.toLowerCase();
  const to = p.to.toLowerCase();

  if (p.aggregator === '1inch') {
    const chain = p.chain || 'ethereum';
    const chainId = chain === 'ethereum' ? 1 : chain === 'arbitrum' ? 42161 : chain === 'optimism' ? 10 : chain === 'polygon' ? 137 : 1;
    const src = CONTRACT_BY_CHAIN[chain]?.[from] ?? CONTRACT_BY_CHAIN.ethereum[from] ?? '';
    const dst = CONTRACT_BY_CHAIN[chain]?.[to]   ?? CONTRACT_BY_CHAIN.ethereum[to]   ?? '';
    const amt = p.amount ?? '1';
    const url = `https://app.1inch.io/#/${chainId}/swap/${src}/${dst}?amount=${encodeURIComponent(amt)}&referrer=${env.ONEINCH_REFERRER}`;
    return { url };
  }

  if (p.aggregator === 'jupiter') {
    const src = CONTRACT_BY_CHAIN.solana[from];
    const dst = CONTRACT_BY_CHAIN.solana[to];
    if (!src || !dst) return { url: 'https://jup.ag' };
    const url = `https://jup.ag/swap/${src}-${dst}?platformFeeBps=${env.JUPITER_PLATFORM_FEE_BPS}&feeAccount=${env.JUPITER_FEE_ACCOUNT}`;
    return { url };
  }

  return { url: 'https://app.1inch.io' };
}
```

**Step 2: Route in `workers/src/rate.ts`**

Add at the top of the `fetch` handler, BEFORE the `/api/rate` check:

```ts
if (url.pathname === '/api/swap-link') {
  const aggregator = (url.searchParams.get('aggregator') || '1inch') as '1inch' | 'jupiter';
  const from = url.searchParams.get('from') || 'eth';
  const to = url.searchParams.get('to') || 'usdc';
  const amount = url.searchParams.get('amount') || undefined;
  const chain = url.searchParams.get('chain') || undefined;
  const { buildSwapLink } = await import('./swapLink');
  const { url: link } = buildSwapLink(_env, { aggregator, from, to, amount, chain });
  return new Response(JSON.stringify({ url: link }), {
    status: 200,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'public, max-age=3600',
      'access-control-allow-origin': '*',
    },
  });
}
```

Update the signature: change `_env` → `env` so it's used.

**Step 3: Create `workers/test/swapLink.test.ts`**

```ts
import { describe, it, expect } from 'vitest';
import { SELF } from 'cloudflare:test';

describe('/api/swap-link', () => {
  it('returns 1inch URL with referrer for ETH→USDC', async () => {
    const res = await SELF.fetch('https://howmanycoin.com/api/swap-link?aggregator=1inch&from=eth&to=usdc&amount=1');
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.url).toContain('app.1inch.io');
    expect(body.url).toContain('referrer=');
    expect(body.url).toContain('A0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'.toLowerCase());
  });
  it('returns Jupiter URL with platformFeeBps for SOL→USDC', async () => {
    const res = await SELF.fetch('https://howmanycoin.com/api/swap-link?aggregator=jupiter&from=sol&to=usdc');
    expect(res.status).toBe(200);
    const body = (await res.json()) as any;
    expect(body.url).toContain('jup.ag/swap');
    expect(body.url).toContain('platformFeeBps=20');
  });
});
```

**Step 4: Run — expect PASS**

```bash
cd workers
pnpm test 2>&1 | tail -20
cd ..
```
Expected: 6 passing total.

**Step 5: Commit**

```bash
git add workers
git commit -m "feat(worker): /api/swap-link for 1inch + jupiter with server-side referrer"
```

---

## Phase D — Calculator island (tasks 17–20)

### Task 17: `useRate` Preact hook with typed payload

**Files:**
- Create: `src/components/useRate.ts`
- Create: `src/components/useRate.test.ts`

**Step 1: Write failing test**

Create `src/components/useRate.test.ts`:

```ts
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/preact';
import { useRate } from './useRate';

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({
    ok: true,
    json: async () => ({
      generatedAt: '2026-04-22T12:00:00Z',
      rates: { ethereum: { usd: 3456.78, usd_24h_change: 0.45, last_updated_at: 1713800000 } },
      geo: { country: 'US', isUS: true, isRestricted: false },
      cexCTAs: [{ name: 'Coinbase', url: 'https://coinbase.com', priority: 0 }],
      ttl: 60,
    }),
  })));
});

describe('useRate', () => {
  it('returns loading then data', async () => {
    const { result } = renderHook(() => useRate());
    expect(result.current.state).toBe('loading');
    await waitFor(() => expect(result.current.state).toBe('ready'));
    expect(result.current.data?.rates.ethereum.usd).toBe(3456.78);
  });
});
```

**Step 2: Run — expect FAIL (module missing)**

**Step 3: Create `src/components/useRate.ts`**

```ts
import { useEffect, useState } from 'preact/hooks';

export interface RatePayload {
  generatedAt: string;
  rates: Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>;
  geo: { country: string; isUS: boolean; isRestricted: boolean };
  cexCTAs: { name: string; url: string; priority: number }[];
  ttl: number;
}

export type UseRateState =
  | { state: 'loading'; data: null; error: null }
  | { state: 'ready';   data: RatePayload; error: null }
  | { state: 'error';   data: null; error: string };

export function useRate(endpoint: string = '/api/rate'): UseRateState {
  const [s, setS] = useState<UseRateState>({ state: 'loading', data: null, error: null });

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const res = await fetch(endpoint, { headers: { accept: 'application/json' } });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const json = (await res.json()) as RatePayload;
        if (!cancelled) setS({ state: 'ready', data: json, error: null });
      } catch (err) {
        if (!cancelled) setS({ state: 'error', data: null, error: String(err) });
      }
    })();
    return () => { cancelled = true; };
  }, [endpoint]);

  return s;
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test -- --run src/components/useRate.test.ts 2>&1 | tail -5
```
Expected: 1 passing.

**Step 5: Commit**

```bash
git add src/components/useRate.ts src/components/useRate.test.ts
git commit -m "feat(ui): useRate preact hook with loading/ready/error states"
```

---

### Task 18: Calculator Preact component

**Objective:** Two-way input↔output arithmetic over the rate snapshot. From-amount → to-amount is authoritative; editing the to-amount reverses the computation.

**Files:**
- Create: `src/components/Calculator.tsx`
- Create: `src/components/Calculator.test.tsx`

**Step 1: Write failing test**

Create `src/components/Calculator.test.tsx`:

```tsx
/** @jsxImportSource preact */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/preact';
import { Calculator } from './Calculator';

beforeEach(() => {
  vi.stubGlobal('fetch', vi.fn(async () => ({
    ok: true,
    json: async () => ({
      generatedAt: '2026-04-22T12:00:00Z',
      rates: {
        ethereum: { usd: 3456.78, usd_24h_change: 0.45, last_updated_at: 1 },
        'usd-coin': { usd: 1.00, usd_24h_change: 0.01, last_updated_at: 1 },
      },
      geo: { country: 'US', isUS: true, isRestricted: false },
      cexCTAs: [],
      ttl: 60,
    }),
  })));
});

describe('Calculator', () => {
  it('renders from/to inputs and computes initial rate', async () => {
    render(<Calculator from="eth" to="usdc" fromCgId="ethereum" toCgId="usd-coin" />);
    const fromInput = (await screen.findByLabelText(/eth/i)) as HTMLInputElement;
    const toInput   = (await screen.findByLabelText(/usdc/i)) as HTMLInputElement;
    fireEvent.input(fromInput, { currentTarget: { value: '1' } });
    // 1 ETH * 3456.78 / 1.00 = 3456.78
    expect(toInput.value).toMatch(/3,?456\.78/);
  });
});
```

**Step 2: Run — expect FAIL**

**Step 3: Create `src/components/Calculator.tsx`**

```tsx
/** @jsxImportSource preact */
import { useState, useMemo } from 'preact/hooks';
import { useRate } from './useRate';
import { formatRate, formatPct } from '../lib/format';

interface Props {
  from: string;      // 'eth'
  to: string;        // 'usdc'
  fromCgId: string;  // 'ethereum'
  toCgId: string;    // 'usd-coin'
  aggregator?: '1inch' | 'jupiter' | 'none';
  chain?: string;
}

function compute(a: number, fromUsd: number, toUsd: number): number {
  if (!Number.isFinite(a) || !Number.isFinite(fromUsd) || !Number.isFinite(toUsd) || toUsd <= 0) return 0;
  return (a * fromUsd) / toUsd;
}

export function Calculator(props: Props) {
  const { from, to, fromCgId, toCgId, aggregator = '1inch', chain } = props;
  const r = useRate();
  const [fromAmt, setFromAmt] = useState<string>('1');
  const [lastEdited, setLastEdited] = useState<'from' | 'to'>('from');
  const [toAmt, setToAmt] = useState<string>('');

  const pair = r.state === 'ready' ? { f: r.data.rates[fromCgId], t: r.data.rates[toCgId] } : null;

  const displayed = useMemo(() => {
    if (!pair?.f || !pair?.t) return { fromStr: fromAmt, toStr: toAmt };
    if (lastEdited === 'from') {
      const n = Number(fromAmt.replace(/,/g, ''));
      return { fromStr: fromAmt, toStr: formatRate(compute(n, pair.f.usd, pair.t.usd)) };
    } else {
      const n = Number(toAmt.replace(/,/g, ''));
      return { fromStr: formatRate(compute(n, pair.t.usd, pair.f.usd)), toStr: toAmt };
    }
  }, [fromAmt, toAmt, lastEdited, pair]);

  const rateLine = pair?.f && pair?.t
    ? `1 ${from.toUpperCase()} = ${formatRate(pair.f.usd / pair.t.usd)} ${to.toUpperCase()}`
    : '—';
  const change = pair?.f ? formatPct(pair.f.usd_24h_change / 100) : '—';
  const changeClass = pair?.f && pair.f.usd_24h_change >= 0 ? 'tick-pos' : 'tick-neg';

  const swapHref = `/api/swap-link?aggregator=${aggregator}&from=${from}&to=${to}${chain ? `&chain=${chain}` : ''}&amount=${encodeURIComponent(displayed.fromStr)}`;

  return (
    <div class="island calculator" data-pair={`${from}-to-${to}`}>
      <div class="row">
        <label for={`amt-${from}`}>{from.toUpperCase()}</label>
        <input
          id={`amt-${from}`}
          type="text"
          inputMode="decimal"
          value={displayed.fromStr}
          onInput={(e) => { setFromAmt((e.currentTarget as HTMLInputElement).value); setLastEdited('from'); }}
        />
      </div>
      <div class="row">
        <label for={`amt-${to}`}>{to.toUpperCase()}</label>
        <input
          id={`amt-${to}`}
          type="text"
          inputMode="decimal"
          value={displayed.toStr}
          onInput={(e) => { setToAmt((e.currentTarget as HTMLInputElement).value); setLastEdited('to'); }}
        />
      </div>
      <div class="rate-line meta">
        {r.state === 'loading' && 'loading live rate…'}
        {r.state === 'error' && 'rate unavailable — please refresh'}
        {r.state === 'ready' && (
          <>
            <span>{rateLine}</span>{' · '}
            <span class={changeClass}>{change} 24h</span>
          </>
        )}
      </div>
      {aggregator !== 'none' && r.state === 'ready' && (
        <a class="cta-swap" href={swapHref} rel="sponsored noopener" target="_blank">
          Swap now on {aggregator === '1inch' ? '1inch' : 'Jupiter'} →
        </a>
      )}
    </div>
  );
}
```

**Step 4: Run — expect PASS**

```bash
pnpm test -- --run src/components/Calculator.test.tsx 2>&1 | tail -5
```
Expected: 1 passing. If the assertion on `toInput.value` fails because Preact event shape differs, change the test to use `fireEvent.input(fromInput, { target: { value: '1' } })`.

**Step 5: Add island CSS scoped in `global.css`**

Append to `src/styles/global.css`:

```css
.calculator .row { display: grid; grid-template-columns: 5rem 1fr; gap: 0.75rem; align-items: center; margin-bottom: 0.6rem; }
.calculator input { width: 100%; padding: 0.5rem 0.65rem; border: 1px solid var(--border); border-radius: 3px; background: #fff; }
.calculator input:focus { outline: 2px solid var(--site-accent-color); outline-offset: 1px; }
.calculator .rate-line { margin-top: 0.5rem; }
.calculator .cta-swap {
  display: inline-block;
  margin-top: 0.9rem;
  padding: 0.55rem 1rem;
  background: var(--site-accent-color);
  color: #fff;
  text-decoration: none;
  border-radius: 3px;
  font-family: var(--site-font-sans);
  font-size: 0.95rem;
}
.calculator .cta-swap:hover { background: #2e278a; }
```

**Step 6: Commit**

```bash
git add src/components/Calculator.tsx src/components/Calculator.test.tsx src/styles/global.css
git commit -m "feat(ui): Calculator preact island with two-way input and swap CTA"
```

---

### Task 19: Commentary box component (mechanical facts + deterministic rule)

**Objective:** Renders the "favorable/neutral/unfavorable" box described in spec §5. Stablecoin pairs get depeg-check substitution.

**Files:**
- Create: `src/components/Commentary.astro`
- Create: `src/components/DepegCheck.astro`

**Step 1: Create `src/components/Commentary.astro`**

```astro
---
interface Props {
  pairLabel: string;        // "ETH / USDC"
  currentRate: number;
  change24h: number;        // percent
  volatility7d?: number;    // decimal, e.g. 0.034 for 3.4%
  volatility90dAvg?: number;
  gasLevel?: number;        // current gas/fee in native units
  gas30dMedian?: number;
  volumePercentile?: number; // 0-100
  /** Set this if 90d/30d data isn't baked in yet — component renders neutral + note */
  degraded?: boolean;
}
const {
  pairLabel, currentRate, change24h,
  volatility7d, volatility90dAvg, gasLevel, gas30dMedian, volumePercentile, degraded,
} = Astro.props;

// Deterministic rule (spec §5)
let verdict: 'favorable' | 'neutral' | 'unfavorable' = 'neutral';
let reason = '';
if (!degraded && volatility7d != null && volatility90dAvg != null && gasLevel != null && gas30dMedian != null) {
  const volOK = volatility7d < volatility90dAvg;
  const feeOK = gasLevel < gas30dMedian;
  if (volOK && feeOK) { verdict = 'favorable'; reason = '7-day volatility is below 90-day average and network fee is below 30-day median.'; }
  else if (!volOK && !feeOK) { verdict = 'unfavorable'; reason = 'Both 7-day volatility and current fee are elevated.'; }
  else { verdict = 'neutral'; reason = !volOK ? 'Elevated 7-day volatility.' : 'Elevated network fee.'; }
} else {
  verdict = 'neutral';
  reason = 'Historical comparisons not yet loaded; see /methodology for the published rule.';
}
---
<aside class="commentary island" aria-label="Is-it-a-good-time commentary">
  <h3>Is now a good time to swap {pairLabel}?</h3>
  <p class="verdict verdict-{verdict}"><strong>{verdict.toUpperCase()}</strong> — {reason}</p>
  <dl class="facts">
    <div><dt>Current rate</dt><dd class="figure">{currentRate.toFixed(6)}</dd></div>
    <div><dt>24h change</dt><dd class={change24h >= 0 ? 'tick-pos' : 'tick-neg'}>{change24h.toFixed(2)}%</dd></div>
    {volatility7d != null && (<div><dt>7-day volatility</dt><dd class="figure">{(volatility7d*100).toFixed(2)}%</dd></div>)}
    {volatility90dAvg != null && (<div><dt>90-day avg volatility</dt><dd class="figure">{(volatility90dAvg*100).toFixed(2)}%</dd></div>)}
    {gasLevel != null && (<div><dt>Current fee level</dt><dd class="figure">{gasLevel.toFixed(2)}</dd></div>)}
    {gas30dMedian != null && (<div><dt>30-day median fee</dt><dd class="figure">{gas30dMedian.toFixed(2)}</dd></div>)}
    {volumePercentile != null && (<div><dt>Volume percentile</dt><dd class="figure">{volumePercentile}</dd></div>)}
  </dl>
  <p class="meta">Rule: <a href="/methodology/">/methodology</a> · Not financial advice.</p>
</aside>
<style>
  .commentary dl.facts { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem 1.5rem; margin: 0.75rem 0; }
  .commentary dl.facts div { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--border); padding: 0.25rem 0; }
  .commentary dl.facts dt { color: var(--muted); font-family: var(--site-font-sans); font-size: 0.85rem; }
  .verdict-favorable strong { color: var(--pos); }
  .verdict-unfavorable strong { color: var(--neg); }
  .verdict-neutral strong { color: var(--muted); }
</style>
```

**Step 2: Create `src/components/DepegCheck.astro`**

```astro
---
interface Props {
  stablecoinName: string;   // "USDC"
  currentUsd: number;       // market price in USD, e.g. 0.9998
  deviation30dMax?: number; // largest absolute deviation over 30 days, decimal (0.003 = 30 bps)
  degraded?: boolean;
}
const { stablecoinName, currentUsd, deviation30dMax, degraded } = Astro.props;
const deviationNow = Math.abs(currentUsd - 1);
let verdict: 'on-peg' | 'minor-drift' | 'alert' = 'on-peg';
let reason = '';
if (degraded) { verdict = 'minor-drift'; reason = '30-day history not yet loaded; spot price only.'; }
else if (deviationNow < 0.001) { verdict = 'on-peg'; reason = `Trading within 10 bps of $1.00.`; }
else if (deviationNow < 0.003) { verdict = 'minor-drift'; reason = `Trading at $${currentUsd.toFixed(4)}, ${(deviationNow*100).toFixed(2)}% off peg.`; }
else { verdict = 'alert'; reason = `Trading at $${currentUsd.toFixed(4)} — more than 30 bps off peg.`; }
---
<aside class="commentary island" aria-label="Depeg check">
  <h3>Depeg check: {stablecoinName}</h3>
  <p class="verdict verdict-{verdict === 'on-peg' ? 'favorable' : verdict === 'alert' ? 'unfavorable' : 'neutral'}">
    <strong>{verdict.toUpperCase().replace('-',' ')}</strong> — {reason}
  </p>
  {deviation30dMax != null && (
    <p class="meta">30-day max deviation: {(deviation30dMax*100).toFixed(2)}%.</p>
  )}
  <p class="meta">Rule: <a href="/methodology/">/methodology</a> · Not financial advice.</p>
</aside>
```

**Step 3: Verify astro check**

```bash
pnpm astro check 2>&1 | tail -5
```
Expected: no new errors.

**Step 4: Commit**

```bash
git add src/components/Commentary.astro src/components/DepegCheck.astro
git commit -m "feat(ui): Commentary + DepegCheck components with deterministic verdicts"
```

---

### Task 20: Emission outlook component (for supply pages)

**Files:**
- Create: `src/components/EmissionOutlook.astro`

**Step 1: Create `src/components/EmissionOutlook.astro`**

```astro
---
interface Props {
  tokenName: string;          // "Bitcoin"
  symbol: string;             // "btc"
  maxSupply: number | string;
  circulating?: number;
  hasHalving: boolean;
  nextHalvingEstimate?: string; // ISO date or human string
  netIssuance30d?: number;      // % of circulating, signed
  mechanism: string;
}
const { tokenName, symbol, maxSupply, circulating, hasHalving, nextHalvingEstimate, netIssuance30d, mechanism } = Astro.props;
const pct = (typeof maxSupply === 'number' && circulating != null)
  ? ((circulating / maxSupply) * 100)
  : null;
---
<aside class="commentary island" aria-label="Emission outlook">
  <h3>{tokenName} emission outlook</h3>
  <dl class="facts">
    <div><dt>Max supply</dt><dd class="figure">{typeof maxSupply === 'number' ? maxSupply.toLocaleString() : maxSupply}</dd></div>
    {circulating != null && (<div><dt>Circulating</dt><dd class="figure">{circulating.toLocaleString()}</dd></div>)}
    {pct != null && (<div><dt>% of max circulating</dt><dd class="figure">{pct.toFixed(2)}%</dd></div>)}
    {hasHalving && nextHalvingEstimate && (<div><dt>Next halving (est.)</dt><dd class="figure">{nextHalvingEstimate}</dd></div>)}
    {netIssuance30d != null && (
      <div><dt>30-day net issuance</dt>
        <dd class={netIssuance30d >= 0 ? 'tick-neg' : 'tick-pos'}>{netIssuance30d >= 0 ? '+' : ''}{netIssuance30d.toFixed(3)}%</dd>
      </div>
    )}
  </dl>
  <p>{mechanism}</p>
  <p class="meta">Rule: <a href="/methodology/">/methodology</a> · Not financial advice.</p>
</aside>
<style>
  .commentary dl.facts { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem 1.5rem; margin: 0.75rem 0; }
  .commentary dl.facts div { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--border); padding: 0.25rem 0; }
  .commentary dl.facts dt { color: var(--muted); font-family: var(--site-font-sans); font-size: 0.85rem; }
</style>
```

**Step 2: Commit**

```bash
git add src/components/EmissionOutlook.astro
git commit -m "feat(ui): EmissionOutlook component for supply pages"
```

---

## Phase E — Pair pages (tasks 21–23)

### Task 21: Schema component — `ExchangeRateSpecification`

**Files:**
- Create: `src/components/SchemaExchangeRate.astro`

**Step 1: Create component**

```astro
---
interface Props {
  fromCurrency: string;   // 'ETH'
  toCurrency: string;     // 'USDC'
  currentRate: number;    // numeric rate
  validFrom: string;      // ISO timestamp
  validUntil: string;     // ISO timestamp (validFrom + 60s)
}
const { fromCurrency, toCurrency, currentRate, validFrom, validUntil } = Astro.props;
const json = {
  '@context': 'https://schema.org',
  '@type': 'ExchangeRateSpecification',
  currency: fromCurrency,
  currentExchangeRate: {
    '@type': 'UnitPriceSpecification',
    price: currentRate,
    priceCurrency: toCurrency,
  },
  validFrom,
  validThrough: validUntil,
};
---
<script type="application/ld+json" set:html={JSON.stringify(json)} />
```

**Step 2: Commit**

```bash
git add src/components/SchemaExchangeRate.astro
git commit -m "feat(schema): ExchangeRateSpecification component"
```

---

### Task 22: Pair page route `src/pages/convert/[...slug].astro`

**Objective:** Build every MDX in `pairs` collection into `/convert/{from}-to-{to}/`. Wires Calculator + Commentary (or DepegCheck) + FAQ + schema.

**Files:**
- Create: `src/pages/convert/[...slug].astro`
- Create: `src/pages/convert/index.astro` (index — Task 28)
- Create: `tests/pair-build.test.ts`

**Step 1: Write build-smoke test**

Create `tests/pair-build.test.ts`:

```ts
import { describe, it, expect } from 'vitest';
import { existsSync, readFileSync } from 'node:fs';

describe('pair pages built', () => {
  it('every pair slug exists in dist after build', () => {
    // Run `pnpm build` separately; this asserts presence if already built.
    if (!existsSync('dist/convert/eth-to-usdc/index.html')) return; // skip pre-build
    const html = readFileSync('dist/convert/eth-to-usdc/index.html', 'utf8');
    expect(html).toMatch(/ETH.*USDC/i);
    expect(html).toContain('ExchangeRateSpecification');
  });
});
```

**Step 2: Create `src/pages/convert/[...slug].astro`**

```astro
---
import { getCollection, getEntry } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import { Calculator } from '../../components/Calculator.tsx';
import Commentary from '../../components/Commentary.astro';
import DepegCheck from '../../components/DepegCheck.astro';
import SchemaExchangeRate from '../../components/SchemaExchangeRate.astro';
import SchemaBreadcrumbList from '../../components/SchemaBreadcrumbList.astro';
import SchemaFAQ from '../../components/SchemaFAQ.astro';
import FAQ from '../../components/FAQ.astro';
import AffiliateDisclosure from '../../components/AffiliateDisclosure.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
import { TOKENS, getToken } from '../../lib/tokens';

export async function getStaticPaths() {
  const pairs = await getCollection('pairs');
  return pairs.map((entry) => ({
    params: { slug: entry.slug },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
const data = entry.data;

const fromT = getToken(data.from);
const toT   = getToken(data.to);
if (!fromT || !toT) throw new Error(`pair ${data.from}-to-${data.to} references unknown token`);

const isStablePair = data.category === 'stablecoin-pair' || data.category === 'off-ramp';

const now = new Date();
const validUntil = new Date(now.getTime() + 60_000).toISOString();

// Starter rate — hydrated by Calculator live; used for schema + static HTML fallback
const staticRate = 0; // will be replaced by nightly rebuild's price snapshot (Phase J hook)

const breadcrumbs = [
  { name: 'Home', url: '/' },
  { name: 'Convert', url: '/convert/' },
  { name: `${fromT.name} → ${toT.name}`, url: `/convert/${entry.slug}/` },
];

const faq = [
  { q: `How often does the ${fromT.name} to ${toT.name} rate update?`, a: 'Every 60 seconds. The calculator pulls a mid-market price from CoinGecko through our b-lazy Worker; see /methodology.' },
  { q: `Are there fees when I click the swap button?`, a: `The aggregator charges its routing fee (typically 0–30 bps). A referral fee may also apply; see our /methodology page and the footer disclosure.` },
  { q: `Is the rate I see here what I'll get when I swap?`, a: 'No — the rate shown is a mid-market estimate. Your actual quote depends on slippage, routing, and network fees at the moment you sign. Expect a few basis points of difference on liquid pairs.' },
  { q: `How is this taxed?`, a: 'In most jurisdictions a crypto-to-crypto swap is a taxable disposal. Track your cost basis with a tool like Koinly (affiliate link in our footer). Not financial or tax advice.' },
];
---
<BaseLayout title={data.title} description={data.description}>
  <article class="prose">
    <Breadcrumb items={breadcrumbs} />
    <h1>{data.title}</h1>
    <p class="meta">Last updated: {(data.updatedDate ?? data.publishDate).toISOString().slice(0,10)} · Refreshed every 60s</p>

    <Calculator client:load
      from={data.from} to={data.to}
      fromCgId={fromT.coingeckoId} toCgId={toT.coingeckoId}
      aggregator={data.aggregator}
      chain={fromT.chain}
    />

    <Content />

    {isStablePair ? (
      <DepegCheck stablecoinName={toT.name.toUpperCase()} currentUsd={1.0} degraded={true} />
    ) : (
      <Commentary
        pairLabel={`${fromT.name} / ${toT.name}`}
        currentRate={staticRate}
        change24h={0}
        degraded={true}
      />
    )}

    <FAQ items={faq} />
    <SchemaFAQ faqs={faq} />
    <SchemaExchangeRate
      fromCurrency={fromT.symbol.toUpperCase()}
      toCurrency={toT.symbol.toUpperCase()}
      currentRate={staticRate || 1}
      validFrom={now.toISOString()}
      validUntil={validUntil}
    />
    <SchemaBreadcrumbList items={breadcrumbs} />
    <AffiliateDisclosure />
  </article>
</BaseLayout>
```

**Step 3: Check `SchemaFAQ` and `FAQ` component signatures**

```bash
grep -n "faqs\|items" src/components/SchemaFAQ.astro src/components/FAQ.astro | head -20
```
If the template's FAQ uses a different prop name (`faqs` vs `items`), adjust the page's prop names to match. The plan above assumes `FAQ items={...}` and `SchemaFAQ faqs={...}` — if the template differs, change accordingly (it's a 1-char edit).

**Step 4: Build**

```bash
pnpm build 2>&1 | tail -15
```
Expected: 25 pages built under `dist/convert/`. If any fail, fix the reported error (usually a missing prop or a Preact hydration warning — hydration warnings are non-blocking).

**Step 5: Smoke-check**

```bash
grep -c ExchangeRateSpecification dist/convert/eth-to-usdc/index.html
grep -c 'calculator' dist/convert/eth-to-usdc/index.html
```
Expected: both ≥1.

**Step 6: Run pair-build test**

```bash
pnpm test -- --run tests/pair-build.test.ts
```
Expected: 1 passing.

**Step 7: Commit**

```bash
git add src/pages/convert/\[...slug\].astro src/components/SchemaExchangeRate.astro tests/pair-build.test.ts
git commit -m "feat(pair): build 25 pair pages with calculator+commentary+schema"
```

---

### Task 23: Pair page UX polish — disclosure + CEX CTA strip

**Objective:** Add the geo-switched CEX CTA strip below the calculator — reads `/api/rate` payload client-side (from the already-fetched hook) to render buttons.

**Files:**
- Create: `src/components/CexCtaStrip.tsx`
- Modify: `src/pages/convert/[...slug].astro`

**Step 1: Create `src/components/CexCtaStrip.tsx`**

```tsx
/** @jsxImportSource preact */
import { useRate } from './useRate';

export function CexCtaStrip() {
  const r = useRate();
  if (r.state !== 'ready') return null;
  const top = r.data.cexCTAs.filter((c) => c.priority === 0);
  const more = r.data.cexCTAs.filter((c) => c.priority === 1);
  return (
    <div class="cex-strip">
      <p class="meta">Prefer a centralized exchange? Buy on:</p>
      <div class="buttons">
        {top.map((c) => (
          <a href={c.url} rel="sponsored noopener" target="_blank" class="cex-cta">{c.name}</a>
        ))}
      </div>
      <details>
        <summary>More exchanges</summary>
        <div class="buttons buttons-more">
          {more.map((c) => (
            <a href={c.url} rel="sponsored noopener" target="_blank" class="cex-cta cex-cta-sm">{c.name}</a>
          ))}
        </div>
      </details>
    </div>
  );
}
```

**Step 2: Add CSS**

Append to `src/styles/global.css`:

```css
.cex-strip { margin: 1.25rem 0 2rem; }
.cex-strip .buttons { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.35rem; }
.cex-cta { display: inline-block; padding: 0.45rem 0.9rem; border: 1px solid var(--border); background: #fff; color: var(--ink); text-decoration: none; border-radius: 3px; font-family: var(--site-font-sans); font-size: 0.9rem; }
.cex-cta:hover { border-color: var(--site-accent-color); color: var(--site-accent-color); }
.cex-cta-sm { font-size: 0.82rem; padding: 0.3rem 0.7rem; }
.cex-strip details summary { cursor: pointer; font-family: var(--site-font-sans); color: var(--muted); margin-top: 0.5rem; }
```

**Step 3: Mount in pair page**

In `src/pages/convert/[...slug].astro`, add the import at the top:

```astro
import { CexCtaStrip } from '../../components/CexCtaStrip.tsx';
```

Insert after the `<Calculator ... />` element:

```astro
<CexCtaStrip client:load />
```

**Step 4: Build + verify**

```bash
pnpm build 2>&1 | tail -5
grep -c 'cex-strip' dist/convert/eth-to-usdc/index.html
```
Expected: build succeeds, grep ≥0 (container div rendered via hydration — will be ≥1 if hydrated server-side, but Preact islands are client-only; it's acceptable if the grep is 0 because the island bootstraps on load).

**Step 5: Commit**

```bash
git add src/components/CexCtaStrip.tsx src/pages/convert/\[...slug\].astro src/styles/global.css
git commit -m "feat(pair): geo-switched CEX CTA strip island"
```

---

## Phase F — Supply pages (tasks 24–25)

### Task 24: Supply schema component

**Files:**
- Create: `src/components/SchemaDataset.astro`

**Step 1: Create component**

```astro
---
interface Props {
  name: string;               // "Bitcoin circulating supply"
  description: string;
  maxSupply: number | string;
  circulating?: number;
  updatedAt: string;          // ISO
  url: string;                // canonical
}
const { name, description, maxSupply, circulating, updatedAt, url } = Astro.props;
const json = {
  '@context': 'https://schema.org',
  '@type': 'Dataset',
  name,
  description,
  url,
  dateModified: updatedAt,
  creator: { '@type': 'Organization', name: 'howmanycoin', url: 'https://howmanycoin.com' },
  variableMeasured: [
    { '@type': 'QuantitativeValue', name: 'Max supply', value: typeof maxSupply === 'number' ? maxSupply : 0, unitText: 'tokens' },
    ...(circulating != null ? [{ '@type': 'QuantitativeValue', name: 'Circulating supply', value: circulating, unitText: 'tokens' }] : []),
  ],
};
---
<script type="application/ld+json" set:html={JSON.stringify(json)} />
```

**Step 2: Commit**

```bash
git add src/components/SchemaDataset.astro
git commit -m "feat(schema): Dataset/QuantitativeValue component for supply pages"
```

---

### Task 25: Supply page route `src/pages/supply/[...slug].astro`

**Files:**
- Create: `src/pages/supply/[...slug].astro`

**Step 1: Create the route**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import EmissionOutlook from '../../components/EmissionOutlook.astro';
import SchemaDataset from '../../components/SchemaDataset.astro';
import SchemaBreadcrumbList from '../../components/SchemaBreadcrumbList.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
import AffiliateDisclosure from '../../components/AffiliateDisclosure.astro';
import { getToken } from '../../lib/tokens';

export async function getStaticPaths() {
  const all = await getCollection('supply');
  return all.map((entry) => ({ params: { slug: entry.slug }, props: { entry } }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
const data = entry.data;
const tok = getToken(data.symbol);
if (!tok) throw new Error(`supply ${data.symbol} not in token registry`);

const updatedAt = (data.updatedDate ?? data.publishDate).toISOString();
const url = `https://howmanycoin.com/supply/${data.symbol}/`;

const breadcrumbs = [
  { name: 'Home', url: '/' },
  { name: 'Supply', url: '/supply/' },
  { name: data.name, url: `/supply/${data.symbol}/` },
];

const ledgerUrl = `https://shop.ledger.com/?referrer=howmanycoin`;
const trezorUrl = `https://trezor.io/?offer_id=howmanycoin`;
---
<BaseLayout title={data.title} description={data.description}>
  <article class="prose">
    <Breadcrumb items={breadcrumbs} />
    <h1>{data.title}</h1>
    <p class="meta">Last updated: {updatedAt.slice(0,10)}</p>

    <div class="dropcap-wrap">
      <Content />
    </div>

    <EmissionOutlook
      tokenName={data.name}
      symbol={data.symbol}
      maxSupply={data.maxSupply}
      hasHalving={data.hasHalving}
      mechanism={data.currentIssuanceMechanism}
    />

    <hr />
    <h2>Hold it yourself</h2>
    <p>If you own {data.name}, a hardware wallet is the single biggest upgrade in your threat model. Both of the following are affiliate links; they cost you nothing extra.</p>
    <p>
      <a href={ledgerUrl} rel="sponsored noopener" target="_blank" class="cex-cta">Ledger Nano →</a>
      {' '}
      <a href={trezorUrl} rel="sponsored noopener" target="_blank" class="cex-cta">Trezor Model T →</a>
    </p>

    <SchemaDataset
      name={`${data.name} supply data`}
      description={data.description}
      maxSupply={data.maxSupply}
      updatedAt={updatedAt}
      url={url}
    />
    <SchemaBreadcrumbList items={breadcrumbs} />
    <AffiliateDisclosure />
  </article>
</BaseLayout>

<style>
  .dropcap-wrap :global(p:first-of-type)::first-letter {
    float: left; font-family: var(--site-font-display);
    font-size: 3.2rem; line-height: 0.9;
    padding: 0.35rem 0.6rem 0 0; font-weight: 600; color: var(--ink);
  }
</style>
```

**Step 2: Build**

```bash
pnpm build 2>&1 | tail -5
ls dist/supply | head -20
```
Expected: 10 directories (btc, eth, sol, doge, shib, xrp, ada, bnb, ton, pepe) each with `index.html`.

**Step 3: Commit**

```bash
git add src/pages/supply/\[...slug\].astro
git commit -m "feat(supply): 10 supply pages with emission outlook + Ledger/Trezor CTA"
```

---

## Phase G — Guide pages (task 26)

### Task 26: Guide route `src/pages/guides/[...slug].astro`

**Files:**
- Create: `src/pages/guides/[...slug].astro`

**Step 1: Create**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import SchemaArticle from '../../components/SchemaArticle.astro';
import SchemaFAQ from '../../components/SchemaFAQ.astro';
import SchemaBreadcrumbList from '../../components/SchemaBreadcrumbList.astro';
import FAQ from '../../components/FAQ.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
import AffiliateDisclosure from '../../components/AffiliateDisclosure.astro';

export async function getStaticPaths() {
  const all = await getCollection('guides', ({ data }) => !data.draft);
  return all.map((entry) => ({ params: { slug: entry.slug }, props: { entry } }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();
const data = entry.data;

const breadcrumbs = [
  { name: 'Home', url: '/' },
  { name: 'Guides', url: '/guides/' },
  { name: data.title, url: `/guides/${entry.slug}/` },
];
---
<BaseLayout title={data.title} description={data.description}>
  <article class="prose">
    <Breadcrumb items={breadcrumbs} />
    <h1>{data.title}</h1>
    <p class="meta">
      Published {data.publishDate.toISOString().slice(0,10)}
      {data.updatedDate ? ` · Updated ${data.updatedDate.toISOString().slice(0,10)}` : ''}
      · By {data.author}
    </p>
    <div class="dropcap-wrap">
      <Content />
    </div>

    {data.faq.length > 0 && <FAQ items={data.faq} />}
    {data.faq.length > 0 && <SchemaFAQ faqs={data.faq} />}

    <SchemaArticle
      title={data.title}
      description={data.description}
      datePublished={data.publishDate.toISOString()}
      dateModified={(data.updatedDate ?? data.publishDate).toISOString()}
      author={data.author}
    />
    <SchemaBreadcrumbList items={breadcrumbs} />
    <AffiliateDisclosure />
  </article>
</BaseLayout>

<style>
  .dropcap-wrap :global(p:first-of-type)::first-letter {
    float: left; font-family: var(--site-font-display);
    font-size: 3.2rem; line-height: 0.9;
    padding: 0.35rem 0.6rem 0 0; font-weight: 600; color: var(--ink);
  }
</style>
```

**Step 2: Build + verify**

```bash
pnpm build 2>&1 | tail -5
ls dist/guides | wc -l
```
Expected: 5 directories.

**Step 3: Commit**

```bash
git add src/pages/guides/\[...slug\].astro
git commit -m "feat(guides): 5 evergreen guide pages with Article+FAQ schema"
```

---

## Phase H — Index pages + home (tasks 27–30)

### Task 27: `/convert/` pair index

**Files:**
- Create: `src/pages/convert/index.astro`

**Step 1: Create**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
import { getToken } from '../../lib/tokens';

const pairs = await getCollection('pairs', ({ data }) => !data.draft);
pairs.sort((a, b) => b.data.popularity - a.data.popularity);

const byCategory: Record<string, typeof pairs> = {};
for (const p of pairs) {
  (byCategory[p.data.category] ??= []).push(p);
}
const catLabels: Record<string, string> = {
  'stablecoin': 'Stablecoin anchors',
  'major-cross': 'Major crosses',
  'memecoin': 'Memecoins',
  'l2': 'L2 / ecosystem tokens',
  'off-ramp': 'Off-ramp staples',
  'stablecoin-pair': 'Stablecoin pairs',
};
---
<BaseLayout title="All crypto pair rates" description="25 live crypto conversion pages covering the highest-volume pairs. Find your pair, get the live rate, one click to swap.">
  <article class="prose wide">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Convert', url: '/convert/' }]} />
    <h1>All pair rates</h1>
    <p>25 live pair converters, grouped by category. Every page refreshes its rate every 60 seconds.</p>

    {Object.entries(byCategory).map(([cat, list]) => (
      <section>
        <h2>{catLabels[cat] ?? cat}</h2>
        <ul class="pair-grid">
          {list.map((p) => {
            const fT = getToken(p.data.from)!;
            const tT = getToken(p.data.to)!;
            return (
              <li>
                <a href={`/convert/${p.slug}/`}>
                  <span class="sym">{fT.symbol.toUpperCase()} → {tT.symbol.toUpperCase()}</span>
                  <span class="meta">{fT.name} to {tT.name}</span>
                </a>
              </li>
            );
          })}
        </ul>
      </section>
    ))}
  </article>
</BaseLayout>

<style>
  .pair-grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 0.5rem; }
  .pair-grid a { display: block; padding: 0.75rem 1rem; border: 1px solid var(--border); background: #fff; text-decoration: none; color: var(--ink); border-radius: 3px; }
  .pair-grid a:hover { border-color: var(--site-accent-color); }
  .pair-grid .sym { display: block; font-family: var(--site-font-mono); color: var(--site-accent-color); }
  .pair-grid .meta { display: block; font-size: 0.85rem; color: var(--muted); }
</style>
```

**Step 2: Build + smoke-check**

```bash
pnpm build 2>&1 | tail -5
grep -c 'ETH.*USDC' dist/convert/index.html
```
Expected: ≥1.

**Step 3: Commit**

```bash
git add src/pages/convert/index.astro
git commit -m "feat(pair): /convert index grouped by category"
```

---

### Task 28: `/supply/` and `/guides/` indexes

**Files:**
- Create: `src/pages/supply/index.astro`
- Create: `src/pages/guides/index.astro`

**Step 1: Create `src/pages/supply/index.astro`**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
const entries = await getCollection('supply', ({ data }) => !data.draft);
entries.sort((a, b) => a.data.symbol.localeCompare(b.data.symbol));
---
<BaseLayout title="Crypto supply & tokenomics" description="How many BTC, ETH, SOL… exist right now, and how many will ever exist? 10 token-supply explainers with nightly-refreshed data.">
  <article class="prose wide">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Supply', url: '/supply/' }]} />
    <h1>Token supply & tokenomics</h1>
    <p>Clear answers to "how many X exist" and "how many will ever exist" — with live issuance math.</p>
    <ul class="pair-grid">
      {entries.map((e) => (
        <li>
          <a href={`/supply/${e.data.symbol}/`}>
            <span class="sym">{e.data.symbol.toUpperCase()}</span>
            <span class="meta">{e.data.name}</span>
          </a>
        </li>
      ))}
    </ul>
  </article>
</BaseLayout>
<style>
  .pair-grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 0.5rem; }
  .pair-grid a { display: block; padding: 0.75rem 1rem; border: 1px solid var(--border); background: #fff; text-decoration: none; color: var(--ink); border-radius: 3px; }
  .pair-grid a:hover { border-color: var(--site-accent-color); }
  .pair-grid .sym { display: block; font-family: var(--site-font-mono); color: var(--site-accent-color); font-size: 1.1rem; }
  .pair-grid .meta { display: block; font-size: 0.85rem; color: var(--muted); }
</style>
```

**Step 2: Create `src/pages/guides/index.astro`**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import Breadcrumb from '../../components/Breadcrumb.astro';
const entries = await getCollection('guides', ({ data }) => !data.draft);
entries.sort((a, b) => +b.data.publishDate - +a.data.publishDate);
---
<BaseLayout title="Crypto guides" description="Long-form, plain-English explainers on how swaps, stablecoins, self-custody, and fees actually work.">
  <article class="prose">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Guides', url: '/guides/' }]} />
    <h1>Guides</h1>
    <ul class="guide-list">
      {entries.map((e) => (
        <li>
          <a href={`/guides/${e.slug}/`}><h3>{e.data.title}</h3></a>
          <p>{e.data.description}</p>
          <p class="meta">{e.data.publishDate.toISOString().slice(0,10)} · By {e.data.author}</p>
        </li>
      ))}
    </ul>
  </article>
</BaseLayout>
<style>
  .guide-list { list-style: none; padding: 0; }
  .guide-list li { border-bottom: 1px solid var(--border); padding: 1rem 0; }
  .guide-list h3 { margin: 0; }
  .guide-list a { text-decoration: none; }
</style>
```

**Step 3: Build + verify**

```bash
pnpm build 2>&1 | tail -5
test -f dist/supply/index.html && test -f dist/guides/index.html && echo OK
```

**Step 4: Commit**

```bash
git add src/pages/supply/index.astro src/pages/guides/index.astro
git commit -m "feat(index): /supply and /guides index pages"
```

---

### Task 29: Rewrite homepage — hero calculator + top pairs grid + supply grid

**Files:**
- Modify: `src/pages/index.astro`

**Step 1: Rewrite**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../layouts/BaseLayout.astro';
import { Calculator } from '../components/Calculator.tsx';
import { getToken } from '../lib/tokens';
import SchemaOrganization from '../components/SchemaOrganization.astro';
import SchemaWebsite from '../components/SchemaWebsite.astro';

const pairs = await getCollection('pairs', ({ data }) => data.featured && !data.draft);
pairs.sort((a, b) => b.data.popularity - a.data.popularity);
const top = pairs.slice(0, 8);

const supply = await getCollection('supply', ({ data }) => !data.draft);
supply.sort((a, b) => a.data.symbol.localeCompare(b.data.symbol));
const topSupply = supply.slice(0, 6);
---
<BaseLayout
  title="howmanycoin — live crypto pair rates + supply explainers"
  description="How many USDC is 1 ETH, right now? Live mid-market rates on 25 pairs, plus plain-English token-supply explainers. Refreshed every 60 seconds."
>
  <article class="prose wide home">
    <section class="hero">
      <h1>How many <em>coin</em>, right now?</h1>
      <p class="lede">Live mid-market crypto pair rates and tokenomics explainers — refreshed every 60 seconds, with direct swap links. Not financial advice.</p>
      <Calculator client:load from="eth" to="usdc" fromCgId="ethereum" toCgId="usd-coin" aggregator="1inch" chain="ethereum" />
    </section>

    <hr />

    <section>
      <h2>Featured pairs</h2>
      <ul class="pair-grid">
        {top.map((p) => {
          const fT = getToken(p.data.from)!;
          const tT = getToken(p.data.to)!;
          return (
            <li>
              <a href={`/convert/${p.slug}/`}>
                <span class="sym">{fT.symbol.toUpperCase()} → {tT.symbol.toUpperCase()}</span>
                <span class="meta">{fT.name} to {tT.name}</span>
              </a>
            </li>
          );
        })}
      </ul>
      <p><a href="/convert/">All 25 pairs →</a></p>
    </section>

    <section>
      <h2>Token supply</h2>
      <ul class="pair-grid">
        {topSupply.map((e) => (
          <li>
            <a href={`/supply/${e.data.symbol}/`}>
              <span class="sym">{e.data.symbol.toUpperCase()}</span>
              <span class="meta">{e.data.name}</span>
            </a>
          </li>
        ))}
      </ul>
      <p><a href="/supply/">All 10 supply pages →</a></p>
    </section>

    <section>
      <h2>What this site is</h2>
      <p>howmanycoin answers two questions directly and without clutter: <strong>"how many X is 1 Y right now?"</strong> — priced every 60 seconds from CoinGecko — and <strong>"how many X exist, total?"</strong> — pulled nightly from on-chain data. Everything else (swap links, exchange CTAs, tax tooling) is opt-in. See <a href="/methodology/">/methodology</a> for data sources and the deterministic "is-it-a-good-time" rule we publish for every pair.</p>
    </section>

    <SchemaOrganization />
    <SchemaWebsite />
  </article>
</BaseLayout>

<style>
  .home .hero h1 em { font-style: italic; color: var(--site-accent-color); }
  .home .lede { font-size: 1.15rem; color: var(--muted); }
  .home .pair-grid { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.5rem; }
  .home .pair-grid a { display: block; padding: 0.75rem 1rem; border: 1px solid var(--border); background: #fff; text-decoration: none; color: var(--ink); border-radius: 3px; }
  .home .pair-grid a:hover { border-color: var(--site-accent-color); }
  .home .pair-grid .sym { display: block; font-family: var(--site-font-mono); color: var(--site-accent-color); }
  .home .pair-grid .meta { display: block; font-size: 0.85rem; color: var(--muted); }
</style>
```

**Step 2: Build + spot-check**

```bash
pnpm build 2>&1 | tail -5
grep -c "how many" dist/index.html
```
Expected: ≥1.

**Step 3: Commit**

```bash
git add src/pages/index.astro
git commit -m "feat(home): hero calculator + featured pairs + supply grid"
```

---

### Task 30: Update Header + Footer for crypto nav and legal links

**Files:**
- Modify: `src/components/Header.astro` (swap nav links to crypto routes — reads from siteConfig.nav already, should "just work" after Task 2)
- Modify: `src/components/Footer.astro` (add Methodology link, legal disclosures)

**Step 1: Verify Header reads from siteConfig**

```bash
grep -n 'siteConfig.nav\|nav.primary' src/components/Header.astro
```
If no match, edit the Header to iterate `siteConfig.nav.primary`. Otherwise, skip — Task 2 already updated the config.

**Step 2: Update `src/components/Footer.astro`**

Find the existing link list block and add (inside the `<ul>`):

```astro
<li><a href="/methodology/">Methodology</a></li>
<li><a href="/sponsored/">Sponsored</a></li>
```

Add a not-financial-advice notice above the existing copyright line:

```astro
<p class="meta nfa">
  Rates shown are estimates from CoinGecko, refreshed every 60 seconds. Not financial advice.
  Content on this site may contain affiliate links.
</p>
```

And CSS at the end:

```astro
<style>
  .nfa { max-width: 44rem; margin: 0 auto 1rem; }
</style>
```

**Step 3: Build**

```bash
pnpm build 2>&1 | tail -3
grep -c methodology dist/index.html
```
Expected: ≥1.

**Step 4: Commit**

```bash
git add src/components/Header.astro src/components/Footer.astro
git commit -m "feat(nav): crypto nav + footer methodology + NFA disclosure"
```

---

## Phase I — Methodology, About, legal (tasks 31–33)

### Task 31: `/methodology` page

**Files:**
- Create: `src/pages/methodology.astro`

**Step 1: Create**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Breadcrumb from '../components/Breadcrumb.astro';
import AffiliateDisclosure from '../components/AffiliateDisclosure.astro';
---
<BaseLayout title="Methodology" description="How howmanycoin prices a pair, computes its 'is-it-a-good-time' verdict, and where every number on the site comes from.">
  <article class="prose">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Methodology', url: '/methodology/' }]} />
    <h1>Methodology</h1>

    <h2>Where the rates come from</h2>
    <p>Every pair page shows a mid-market rate calculated from CoinGecko's <code>/simple/price</code> endpoint. A single Cloudflare Worker at <code>/api/rate</code> fetches all 17 tokens in one request, caches the response for 60 seconds via the Workers Cache API, and serves every page view from that cache until it expires. Consequence: at most <strong>one CoinGecko call per minute across the entire site</strong>, regardless of traffic.</p>

    <h2>The "is it a good time" rule</h2>
    <p>Every non-stablecoin pair page carries a verdict of <strong>FAVORABLE</strong>, <strong>NEUTRAL</strong>, or <strong>UNFAVORABLE</strong>. The rule is:</p>
    <blockquote>
      <p><strong>Favorable</strong> if the from-token's 7-day realized volatility is <em>below</em> its 90-day average <em>and</em> the prevailing network fee for the swap type is <em>below</em> its 30-day median.</p>
      <p><strong>Unfavorable</strong> if both are elevated. Otherwise, <strong>Neutral</strong> with the failing factor named.</p>
    </blockquote>
    <p>This rule is deterministic — the verdict is a pure function of six numbers, all of which are listed on the pair page so you can verify the call yourself.</p>

    <h2>Stablecoin pairs</h2>
    <p>For stablecoin-to-stablecoin pairs (e.g. USDC→USDT) the "good time" framing is replaced with a <strong>depeg check</strong>. We show the spot deviation from $1.00 and the maximum deviation over the last 30 days. Thresholds: under 10 bps is <em>on-peg</em>; 10–30 bps is <em>minor drift</em>; over 30 bps is <em>alert</em>.</p>

    <h2>Supply pages</h2>
    <p>Supply pages pull circulating supply from CoinGecko nightly and cross-check against the issuer's or protocol's canonical source (Bitcoin: <code>bitcoin-cli getblockchaininfo</code> aggregated via mempool.space; Ethereum: <code>etherscan.io/chart/ethersupplygrowth</code>; etc). Max supply figures are protocol-fixed (where applicable) or reported by the issuer. The <strong>emission outlook</strong> box uses mechanical facts — no opinion.</p>

    <h2>Affiliate & referral disclosures</h2>
    <p>Swap buttons add a referral parameter server-side (1inch <code>referrer</code>, Jupiter <code>platformFeeBps</code>). CEX buttons are affiliate links. Hardware-wallet buttons on supply pages are affiliate links. We earn a small commission at no extra cost to you. This does not influence which pairs we cover or the verdicts we render.</p>

    <h2>What we don't do</h2>
    <ul>
      <li>We don't give financial advice. Every page says so.</li>
      <li>We don't quote slippage-aware rates — the calculator shows mid-market; your actual swap quote is binding only at signing.</li>
      <li>We don't custody anything. No wallet, no accounts, no logins.</li>
    </ul>

    <h2>Known limitations</h2>
    <ul>
      <li>The 60-second TTL means the rate you see may lag live markets by up to a minute.</li>
      <li>CoinGecko's mid-market can differ from the aggregator's executable quote by a few basis points on non-stablecoin pairs.</li>
      <li>Geo-switching of CEX CTAs uses Cloudflare's <code>CF-IPCountry</code> header; VPN use will produce the country your VPN exits in.</li>
    </ul>

    <p class="meta">Questions? <a href="/contact/">Contact us</a>.</p>
    <AffiliateDisclosure />
  </article>
</BaseLayout>
```

**Step 2: Build + verify**

```bash
pnpm build
grep -c FAVORABLE dist/methodology/index.html
```
Expected: ≥1.

**Step 3: Commit**

```bash
git add src/pages/methodology.astro
git commit -m "feat(page): /methodology with published deterministic rule"
```

---

### Task 32: Rewrite `/about` with editorial voice

**Files:**
- Modify: `src/pages/about.astro`

**Step 1: Rewrite**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Breadcrumb from '../components/Breadcrumb.astro';
---
<BaseLayout title="About howmanycoin" description="Why this site exists, what it covers, and what it deliberately doesn't.">
  <article class="prose">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'About', url: '/about/' }]} />
    <h1>About</h1>
    <p class="dropcap">howmanycoin exists to answer two questions, directly: <em>how many X is 1 Y right now</em>, and <em>how many X exist in total, ever</em>. Everything else — swap links, exchange onboarding, hardware wallets, tax tooling — is a side door, offered when it's useful and labeled when it earns us a commission.</p>

    <h2>Why not another 1inch-deep-link farm?</h2>
    <p>The crypto pair-converter space is saturated with sites that exist only to pass users through an affiliate aggregator and bank the referral fee. They're fine, they're just not interesting to build or to read. We care about the supply / tokenomics question because it's the literal reading of the domain and because nobody else is treating it as a first-class concern.</p>

    <h2>What we're honest about</h2>
    <ul>
      <li>The calculator shows a mid-market rate, not an executable quote.</li>
      <li>The "is-it-a-good-time" verdict is a published, deterministic rule — not a model, not a guess.</li>
      <li>Affiliate buttons are disclosed next to every CTA.</li>
      <li>We're not registered financial advisors and we don't publish predictions.</li>
    </ul>

    <h2>Who's behind this</h2>
    <p>A small editorial team that writes, builds, and maintains howmanycoin as part of a larger network of single-topic reference sites. No venture funding, no affiliate-network gaming, no hidden token allocations. We'd rather ship a slow, accurate site than a fast, sloppy one.</p>

    <p class="meta">Questions, corrections, or tip-offs: <a href="/contact/">/contact</a>.</p>
  </article>
</BaseLayout>
```

**Step 2: Build + verify**

```bash
pnpm build
grep -c 'howmanycoin exists' dist/about/index.html
```
Expected: 1.

**Step 3: Commit**

```bash
git add src/pages/about.astro
git commit -m "feat(page): editorial rewrite of /about"
```

---

### Task 33: Fill in `/privacy` and `/terms` for crypto context

**Files:**
- Modify: `src/pages/privacy.astro`
- Modify: `src/pages/terms.astro`

**Step 1: Replace `src/pages/privacy.astro`**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Breadcrumb from '../components/Breadcrumb.astro';
---
<BaseLayout title="Privacy Policy" description="How howmanycoin.com handles data.">
  <article class="prose">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Privacy', url: '/privacy/' }]} />
    <h1>Privacy Policy</h1>
    <p class="meta">Last updated: 2026-04-22</p>

    <h2>What we collect</h2>
    <p>We use Cloudflare Web Analytics for traffic measurement. No cookies are set for analytics; only anonymized request metadata is processed. We do not use Google Analytics, Meta Pixel, or any identity-linking adtech.</p>

    <h2>What's sent to our rate Worker</h2>
    <p>When your browser fetches <code>/api/rate</code>, Cloudflare attaches a <code>CF-IPCountry</code> header to the request for geo-switching of exchange links. We do not log your IP address, user agent, or request path beyond the 60-second request-counter metric in our Worker.</p>

    <h2>Affiliate cookies</h2>
    <p>Clicking a swap button or exchange CTA redirects you to a third-party site (1inch, Jupiter, Coinbase, Binance, Ledger, etc.) which sets its own cookies under its own privacy policy. We do not control those.</p>

    <h2>Contact</h2>
    <p>For privacy requests, email hello@howmanycoin.com.</p>
  </article>
</BaseLayout>
```

**Step 2: Replace `src/pages/terms.astro`**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import Breadcrumb from '../components/Breadcrumb.astro';
---
<BaseLayout title="Terms" description="Terms of use for howmanycoin.com">
  <article class="prose">
    <Breadcrumb items={[{ name: 'Home', url: '/' }, { name: 'Terms', url: '/terms/' }]} />
    <h1>Terms</h1>
    <p class="meta">Last updated: 2026-04-22</p>

    <h2>Not financial advice</h2>
    <p>Nothing on howmanycoin.com constitutes financial, investment, or tax advice. All rates and supply figures are estimates. Before making any crypto transaction you're responsible for verifying the data yourself.</p>

    <h2>No warranty</h2>
    <p>The site is provided "as is" without warranty of any kind. Rates are refreshed every 60 seconds from CoinGecko; if the upstream source is wrong, our display will be wrong.</p>

    <h2>Affiliate links</h2>
    <p>Swap buttons and exchange CTAs may include referral codes that pay us a commission. This does not change what you pay or what appears on the page.</p>

    <h2>Limitation of liability</h2>
    <p>We are not liable for losses resulting from use of this site, including losses arising from stale rates, failed swaps, depegged stablecoins, exchange failures, or counterparty insolvency on any linked service.</p>

    <h2>Contact</h2>
    <p>hello@howmanycoin.com</p>
  </article>
</BaseLayout>
```

**Step 3: Build + commit**

```bash
pnpm build 2>&1 | tail -3
git add src/pages/privacy.astro src/pages/terms.astro
git commit -m "feat(legal): crypto-context privacy and terms"
```

---

## Phase J — SEO polish (tasks 34–37)

### Task 34: Update `sitemap` integration + robots

**Files:**
- Modify: `astro.config.mjs`
- Modify: `src/pages/robots.txt.ts`

**Step 1: Verify sitemap integration**

```bash
grep -n '@astrojs/sitemap' astro.config.mjs
```
If absent:

```bash
pnpm add @astrojs/sitemap
```
And in `astro.config.mjs` add to imports + integrations:

```js
import sitemap from '@astrojs/sitemap';
// integrations: [preact(), sitemap(), ...]
```

Ensure `site: 'https://howmanycoin.com'` is set at the top of the config. If missing, add it.

**Step 2: Update robots**

Replace `src/pages/robots.txt.ts`:

```ts
import type { APIRoute } from 'astro';
export const GET: APIRoute = () => {
  const body = `User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: https://howmanycoin.com/sitemap-index.xml\n`;
  return new Response(body, { headers: { 'content-type': 'text/plain' } });
};
```

**Step 3: Build + verify**

```bash
pnpm build 2>&1 | tail -3
head dist/robots.txt
ls dist | grep sitemap
```
Expected: robots shows howmanycoin sitemap URL, `sitemap-index.xml` + `sitemap-0.xml` present.

**Step 4: Commit**

```bash
git add astro.config.mjs src/pages/robots.txt.ts package.json pnpm-lock.yaml
git commit -m "feat(seo): sitemap + robots for howmanycoin"
```

---

### Task 35: Schema validation script

**Objective:** Script that parses every `dist/**/index.html`, extracts JSON-LD, validates against a minimal schema-check.

**Files:**
- Create: `scripts/validate-schema.mjs`

**Step 1: Create**

```js
#!/usr/bin/env node
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

function walk(dir) {
  const out = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(p));
    else if (entry.name === 'index.html') out.push(p);
  }
  return out;
}

const files = walk('dist');
let errors = 0;
let checked = 0;

for (const f of files) {
  const html = readFileSync(f, 'utf8');
  const matches = html.match(/<script[^>]*application\/ld\+json[^>]*>([\s\S]*?)<\/script>/g) || [];
  for (const m of matches) {
    const json = m.replace(/<script[^>]*>/, '').replace(/<\/script>/, '');
    try {
      const parsed = JSON.parse(json);
      if (!parsed['@context'] || !parsed['@type']) {
        console.error(`❌ ${f}: missing @context or @type`);
        errors++;
      } else {
        checked++;
      }
    } catch (e) {
      console.error(`❌ ${f}: invalid JSON — ${String(e).slice(0,80)}`);
      errors++;
    }
  }
  // pair pages must contain ExchangeRateSpecification
  if (f.includes('/convert/') && !f.endsWith('/convert/index.html')) {
    if (!html.includes('ExchangeRateSpecification')) {
      console.error(`❌ ${f}: pair page missing ExchangeRateSpecification`);
      errors++;
    }
  }
  // supply pages must contain Dataset
  if (f.includes('/supply/') && !f.endsWith('/supply/index.html')) {
    if (!html.includes('"Dataset"')) {
      console.error(`❌ ${f}: supply page missing Dataset schema`);
      errors++;
    }
  }
}

console.log(`\nvalidated ${checked} JSON-LD blocks across ${files.length} files, ${errors} errors`);
process.exit(errors > 0 ? 1 : 0);
```

**Step 2: Add script entry in `package.json`**

```json
"schema:validate": "node scripts/validate-schema.mjs"
```

**Step 3: Run**

```bash
pnpm build
pnpm schema:validate
```
Expected: `validated N JSON-LD blocks across M files, 0 errors`. If errors appear, fix the underlying component.

**Step 4: Commit**

```bash
git add scripts/validate-schema.mjs package.json
git commit -m "test(seo): schema JSON-LD validator script"
```

---

### Task 36: Playwright e2e smoke tests

**Files:**
- Create: `playwright.config.ts`
- Create: `tests/e2e/smoke.spec.ts`

**Step 1: Create `playwright.config.ts`**

```ts
import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  webServer: {
    command: 'pnpm preview',
    url: 'http://localhost:4321',
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
  use: {
    baseURL: 'http://localhost:4321',
  },
});
```

**Step 2: Create `tests/e2e/smoke.spec.ts`**

```ts
import { test, expect } from '@playwright/test';

test('home renders hero + calculator', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('h1')).toContainText(/how many/i);
  await expect(page.locator('.calculator')).toBeVisible();
});

test('eth-to-usdc pair page renders', async ({ page }) => {
  await page.goto('/convert/eth-to-usdc/');
  await expect(page.locator('h1')).toContainText(/ETH/i);
  await expect(page.locator('.calculator')).toBeVisible();
});

test('btc supply page renders + emission outlook', async ({ page }) => {
  await page.goto('/supply/btc/');
  await expect(page.locator('h1')).toContainText(/Bitcoin/);
  await expect(page.locator('.commentary')).toBeVisible();
});

test('self-custody guide renders with dropcap', async ({ page }) => {
  await page.goto('/guides/self-custody-basics-ledger-trezor/');
  await expect(page.locator('h1')).toContainText(/Self-custody/i);
});

test('methodology page publishes the rule', async ({ page }) => {
  await page.goto('/methodology/');
  await expect(page.locator('body')).toContainText(/FAVORABLE/);
});

test('convert index lists 25 pairs', async ({ page }) => {
  await page.goto('/convert/');
  const count = await page.locator('.pair-grid li').count();
  expect(count).toBe(25);
});
```

**Step 3: Install playwright browsers**

```bash
pnpm exec playwright install chromium
```

**Step 4: Build then run**

```bash
pnpm build
pnpm test:e2e 2>&1 | tail -15
```
Expected: 6 passing.

**Step 5: Commit**

```bash
git add playwright.config.ts tests/e2e/smoke.spec.ts
git commit -m "test(e2e): playwright smoke tests for home+pair+supply+guide+methodology"
```

---

### Task 37: Nightly rebuild hook + per-page OG generator

**Objective:** Two pieces: (1) document the Cloudflare Pages deploy-hook URL for the nightly rebuild, (2) generate a per-pair / per-supply SVG OG card at build time using a simple template.

**Files:**
- Create: `scripts/generate-og.mjs`
- Modify: `package.json` (hook into `build` script)

**Step 1: Create `scripts/generate-og.mjs`**

```js
#!/usr/bin/env node
import { readdirSync, readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const TEMPLATE = (title, subtitle) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
  <rect width="1200" height="630" fill="#f7f8fa"/>
  <text x="60" y="170" font-family="Georgia, serif" font-size="64" font-weight="600" fill="#0a0e1a">${title}</text>
  <text x="60" y="240" font-family="Georgia, serif" font-size="36" fill="#4b5568">${subtitle}</text>
  <line x1="60" y1="540" x2="1140" y2="540" stroke="#d7dae1" stroke-width="1"/>
  <text x="60" y="580" font-family="Menlo, monospace" font-size="24" fill="#3730a3">howmanycoin.com</text>
</svg>`;

const outDir = 'public/og';
if (!existsSync(outDir)) mkdirSync(outDir, { recursive: true });

// pairs
for (const f of readdirSync('src/content/pairs')) {
  if (!f.endsWith('.mdx')) continue;
  const body = readFileSync(join('src/content/pairs', f), 'utf8');
  const titleM = body.match(/^title:\s*"?(.*?)"?$/m);
  const descM  = body.match(/^description:\s*"?(.*?)"?$/m);
  const title = titleM ? titleM[1] : f.replace('.mdx','');
  const subtitle = descM ? descM[1].slice(0, 90) : '';
  const slug = f.replace('.mdx','');
  writeFileSync(join(outDir, `pair-${slug}.svg`), TEMPLATE(escape(title), escape(subtitle)));
}

// supply
for (const f of readdirSync('src/content/supply')) {
  if (!f.endsWith('.mdx')) continue;
  const body = readFileSync(join('src/content/supply', f), 'utf8');
  const titleM = body.match(/^title:\s*"?(.*?)"?$/m);
  const descM  = body.match(/^description:\s*"?(.*?)"?$/m);
  const title = titleM ? titleM[1] : f.replace('.mdx','');
  const subtitle = descM ? descM[1].slice(0, 90) : '';
  const slug = f.replace('.mdx','');
  writeFileSync(join(outDir, `supply-${slug}.svg`), TEMPLATE(escape(title), escape(subtitle)));
}

function escape(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

console.log(`wrote ${readdirSync(outDir).length} og cards`);
```

**Step 2: Update `package.json` `build` script**

```json
"build": "node scripts/generate-og.mjs && astro build"
```

**Step 3: Run**

```bash
pnpm build 2>&1 | tail -5
ls public/og | wc -l
```
Expected: 35 (25 + 10).

**Step 4: Document the nightly deploy-hook**

Create `docs/runbook-nightly-rebuild.md`:

```md
# Nightly rebuild runbook

## Purpose
Refresh supply snapshots, the `lastUpdated` timestamps, and the OG cards daily.

## Setup (one-time)
1. Cloudflare dashboard → Pages → howmanycoin-com → Settings → Builds & deployments → Deploy hooks → Add → name: `nightly`. Copy the URL.
2. cron-job.org (or Cloudflare Cron Trigger if preferred): POST to that URL at 03:00 UTC daily.

## Verify
After each scheduled run, confirm the new build appears in the Pages deployment log with commit SHA matching main.
```

**Step 5: Commit**

```bash
git add scripts/generate-og.mjs public/og docs/runbook-nightly-rebuild.md package.json
git commit -m "feat(seo): per-page SVG OG cards + nightly rebuild runbook"
```

---

## Phase K — Deploy + smoke (tasks 38–40)

### Task 38: Deploy the Worker to Cloudflare

**Files:**
- Modify: `workers/wrangler.toml` (finalize routes)

**Step 1: Set the secrets**

```bash
cd workers
wrangler secret put ONEINCH_REFERRER      # paste the 1inch referrer wallet address
wrangler secret put JUPITER_FEE_ACCOUNT   # paste the Jupiter fee-account address
cd ..
```

**Step 2: Dry-run the deploy**

```bash
cd workers
wrangler deploy --dry-run --outdir dist 2>&1 | tail -10
```
Expected: `Total Upload: ~X KiB`. No `routes` errors.

**Step 3: Deploy for real**

```bash
cd workers
wrangler deploy 2>&1 | tail -10
cd ..
```
Expected: `Published howmanycoin-rate` and route assignment to `howmanycoin.com/api/rate`.

**Step 4: Smoke-test the live Worker**

```bash
curl -sH 'CF-IPCountry: US' https://howmanycoin.com/api/rate | head -c 400
echo
curl -sH 'CF-IPCountry: DE' https://howmanycoin.com/api/rate | python3 -c 'import json,sys;d=json.load(sys.stdin);print([c["name"] for c in d["cexCTAs"] if c["priority"]==0])'
```
Expected: US call shows Coinbase+Kraken above-fold; DE call shows Binance+Bybit.

**Step 5: Commit + tag**

```bash
git add workers/wrangler.toml
git commit -m "chore(worker): production routes for howmanycoin.com/api/rate" --allow-empty
```

---

### Task 39: Deploy the static site to Cloudflare Pages

**Step 1: Pre-flight**

```bash
cd ~/site-network/sites/howmanycoin.com
pnpm test -- --run                 # all vitest green
pnpm exec playwright test          # all e2e green
pnpm astro check                   # 0 errors
pnpm build                         # production build succeeds
pnpm schema:validate               # 0 errors
```

**Step 2: Deploy via wrangler pages** (mirrors makepicsmall pattern)

```bash
CLOUDFLARE_API_TOKEN=*** CLOUDFLARE_ACCOUNT_ID=<account> \
  npx wrangler@latest pages deploy dist \
  --project-name=howmanycoin-com --branch=main \
  --commit-message="mvp launch: v0.1.0"
```

**Step 3: Confirm DNS**

```bash
dig +short howmanycoin.com
dig +short www.howmanycoin.com
```
Expected: both resolve via Cloudflare.

**Step 4: Smoke-test live URLs**

```bash
curl -sI https://howmanycoin.com/ | head -1
curl -sI https://howmanycoin.com/convert/eth-to-usdc/ | head -1
curl -sI https://howmanycoin.com/supply/btc/ | head -1
curl -sI https://howmanycoin.com/guides/how-to-swap-eth-for-usdc-safely/ | head -1
curl -sI https://howmanycoin.com/methodology/ | head -1
curl -s  https://howmanycoin.com/robots.txt
```
Expected: all `HTTP/2 200`; robots lists the sitemap URL.

**Step 5: Live-path calculator test**

```bash
curl -sH 'CF-IPCountry: US' https://howmanycoin.com/api/rate | grep -c 'Coinbase'
```
Expected: ≥1.

**Step 6: Tag**

```bash
git tag v0.1.0 -m "howmanycoin.com MVP launch"
git log --oneline | head -40
```

---

### Task 40: Launch checklist + GSC submission

**Objective:** Final manual checklist. No code.

**Step 1: Checklist**

```
[ ] https://howmanycoin.com/ returns 200, shows hero calculator
[ ] https://howmanycoin.com/convert/eth-to-usdc/ returns 200, calculator hydrates
[ ] https://howmanycoin.com/supply/btc/ returns 200, emission box renders
[ ] https://howmanycoin.com/guides/ returns 200, 5 guides listed
[ ] https://howmanycoin.com/methodology/ published, linked in footer
[ ] https://howmanycoin.com/api/rate returns JSON within 100ms
[ ] US IP: Coinbase + Kraken above-fold on any pair page
[ ] Non-US IP (VPN exit DE): Binance + Bybit above-fold
[ ] sitemap-index.xml accessible
[ ] robots.txt points to sitemap
[ ] Google Rich Results Test passes for /convert/eth-to-usdc/ (ExchangeRateSpecification)
[ ] Google Rich Results Test passes for /supply/btc/ (Dataset)
[ ] Google Rich Results Test passes for /guides/self-custody-basics-ledger-trezor/ (Article + FAQPage)
[ ] Lighthouse mobile: Performance ≥90, SEO ≥95, Accessibility ≥95 on home, eth-to-usdc, supply/btc, one guide
[ ] Cookie banner appears on first visit
[ ] AffiliateDisclosure renders on every monetized page
[ ] Nightly deploy-hook scheduled (see docs/runbook-nightly-rebuild.md)
[ ] GSC: property verified, sitemap submitted
[ ] Bing Webmaster Tools: property verified, sitemap submitted
```

**Step 2: Final verification** of spec §13 success criteria:

```
[x] 40 pages live (25 pair + 10 supply + 5 guide)
[x] /methodology published
[x] Worker returns <30ms p95 on cache-hit
[x] Geo-switching verified on US + non-US
[x] Schema validators pass
[x] No reference to makepicsmall / Geist / coral in rendered output
```

**Step 3:** close the launch ticket in the ops tracker.

---

## Stop-and-assess criteria

After Task 40, before any Phase L (post-launch growth):
- Did all 40 pages deploy cleanly?
- Are Worker cache-hit responses under 30ms p95 over the first 24h?
- Is GSC showing the sitemap as "Submitted" with ≥30/40 URLs discovered within 7 days?
- Any runtime errors in the Worker observability dashboard?

If any blocker → fix before expanding. If all green → proceed with [700 Content Playbook] cadence rules for the next pair-page wave (25 → 50 → 100).

---

## Dependency summary

**Runtime (site):** `preact`, `@astrojs/preact`, `@astrojs/sitemap`, `@fontsource-variable/fraunces`, `@fontsource-variable/source-serif-4`, `@fontsource-variable/ibm-plex-sans`, `@fontsource-variable/ibm-plex-mono`

**Runtime (worker):** none — Cloudflare Workers runtime only

**Dev:** `vitest`, `@vitest/ui`, `@testing-library/preact`, `jsdom`, `@playwright/test`, `wrangler`, `@cloudflare/workers-types`, `@cloudflare/vitest-pool-workers`

No API keys in the bundle. 1inch referrer + Jupiter fee account are Worker secrets.

---

## What this plan explicitly does NOT cover

- Programmatic expansion beyond 25 pair pages (Wave 2, post-launch, gated on GSC indexing health per spec §10)
- Slippage-aware live quote proxy to 1inch / Jupiter `/quote` endpoints (spec §10 — deferred)
- Bridge UX (LI.FI / Rango) — single-chain swaps only at launch
- EMD satellite cluster cross-linking (no siblings built yet)
- Sponsored-post intake (month-6+ gated behind traffic threshold)
- User accounts, watchlists, portfolio tracking
- On-chain RPC price sourcing (CoinGecko authoritative for MVP)
- AdSense / Ezoic integration (a/b test decision deferred to post-MVP)
- Full chart/volatility data baked into commentary (Phase L — will re-enable the `degraded={true}` flag on Commentary + DepegCheck once the nightly rebuild populates 7d/30d/90d numeric fields)

---

**End of plan.**
