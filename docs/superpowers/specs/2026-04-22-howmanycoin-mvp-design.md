# howmanycoin.com MVP Design

**Status:** Approved 2026-04-22
**Site:** Cohort 1 / Site 2
**Domain:** howmanycoin.com (secured 2026-04-21 via Spaceship, Cloudflare zone live, Astro template already scaffolded)
**Parent concept:** [830 Crypto Conversion Rate Estimators](obsidian://open?vault=SuperVault&file=Site%20Network%2FTools%2F830%20Crypto%20Conversion%20Rate%20Estimators)

## 1. Positioning

A crypto pair-converter and supply/tokenomics explainer. Lead product is pair conversion pages (the transactional engine that drives affiliate revenue); differentiation is the supply/tokenomics angle that matches the literal domain reading ("how many [X] coin…") and hedges against the generic me-too "1inch deep-link farm" look that dominates crypto pair sites.

howmanycoin is positioned as the **brandable hub** of the future crypto cluster. EMD satellites and chain-vertical sites come in later waves; this MVP is entirely self-contained and does not cross-link to unbuilt siblings.

## 2. Scope at launch — 40 pages

**25 pair pages** under `/convert/{from}-to-{to}`:

- Stablecoin anchors (volume winners): eth-usdc, eth-usdt, btc-usdt, btc-usdc, sol-usdc, sol-usdt, bnb-usdt, matic-usdt, avax-usdt
- Major crosses: btc-eth, eth-btc, sol-eth, bnb-btc
- Memecoins: doge-usdt, shib-usdt, pepe-usdt, doge-usd
- L2 / ecosystem tokens (paired with eth, not stables, matching real user intent): arb-eth, op-eth, matic-eth, avax-eth
- Off-ramp staples: usdc-usdt, usdt-usd, usdc-usd, dai-usdc

**10 supply / tokenomics pages** under `/supply/{token}`:

btc, eth, sol, doge, shib, xrp, ada, bnb, ton, pepe

Each answers: circulating supply, max supply, emission / burn rate, halving or emission schedule where relevant, historical supply snapshot, "will ever exist" framing.

**5 evergreen guides** under `/guides/{slug}`:

Covering the five highest-volume pair routes (exact slugs chosen during implementation). Hedges the programmatic-calculator "thin content" risk and seeds internal linking.

**Scope shift vs parent concept:** [203 Site 2 - Crypto Conversion Hub](obsidian://open?vault=SuperVault&file=Site%20Network%2FSites%2F203%20Site%202%20-%20Crypto%20Conversion%20Hub) originally called for 100 pair pages at launch. Reduced to a lean 25 + 10 + 5 to match the Site 1 launch philosophy (ship the smallest thing that earns its keep, scale after indexing health is proven). Programmatic expansion to 100 → 500 → 5k pairs is a post-launch wave, not a launch blocker.

## 3. Architecture

Astro 5 static site deployed to Cloudflare Pages, same topology as makepicsmall.com. Three new content collections replace the template defaults:

- `pairs` collection — typed frontmatter per pair (from, to, fromChain, toChain, aggregator, category), MDX body for the optional pair-specific commentary
- `supply` collection — typed frontmatter per token (symbol, name, chain, maxSupply, circulatingSupplySource, halvingSchedule), MDX body for explainer copy
- `guides` collection — standard blog-like collection for evergreen long-form content

**Calculator:** Preact island on each pair page. Client-side arithmetic over a live rate snapshot. Bordered "island" UI inside the editorial page — Plex Sans labels, Plex Mono figures — so the calculator reads as a tool inside a serif explainer, not as the page hero.

**Live rate service — b-lazy pattern:** One Cloudflare Worker endpoint at `/api/rate`. Uses the Workers Cache API keyed on the token-id set. On request:

1. If a cached response younger than 60s exists, return it.
2. Otherwise, fetch a single CoinGecko `/simple/price` call covering all tokens on the site (one request, comma-separated IDs), cache for 60s, return it.

Consequences: at most one CoinGecko call per minute across the entire site regardless of traffic or pair count; zero background jobs; zero KV; zero cron; scales with traffic rather than with page count. Worker invocation count stays inside the Cloudflare free tier for the foreseeable future.

**Geo-switched CEX CTAs:** The same Worker endpoint reads the `CF-IPCountry` request header and returns the appropriate CEX affiliate link set alongside the price payload:

- US traffic → Coinbase + Kraken above-fold
- Non-US → Binance + Bybit above-fold
- All pages show a "more exchanges" expandable section with the rest

**Nightly rebuild:** Cloudflare Pages build hook runs daily to refresh historical chart snapshots, supply figures baked into HTML, and `lastUpdated` timestamps in schema.

## 4. Monetization stack

**DEX aggregator deep-links** (primary on-chain CTA):

- 1inch for all EVM pairs (referral fee param attached server-side)
- Jupiter for all Solana pairs (`platformFeeBps` attached server-side)
- Chain-aware routing logic lives in the Worker so affiliate params cannot be stripped client-side

**CEX affiliate CTAs** (primary fiat on/off-ramp revenue):

- Above-fold: 2 geo-switched buttons (rules in §3)
- Expandable: Binance, Bybit, OKX, MEXC, Coinbase, Kraken, KuCoin depending on geo

**Secondary affiliates:**

- Ledger + Trezor on supply pages ("after you hold your X, self-custody it")
- Koinly in pair-page tax-implications FAQ blocks

**Dropped from launch:** Changelly / ChangeNOW / SimpleSwap instant-swap widgets. Decision rationale: site cleanliness and regulatory-smell minimization. Can revisit in a later wave.

## 5. "Is it a good time" commentary (thin-content hedge)

Each pair page carries a short, mechanical commentary box whose output follows a single **published deterministic heuristic rule**:

> **Favorable** if the from-token's 7-day realized volatility is below its 90-day average **and** the prevailing network fee for the swap type is below its 30-day median.
>
> Otherwise: **Neutral / Unfavorable** with the specific failing factor named.

The rule itself is documented on `/methodology`. The page also lists the underlying facts (current rate, 24h change, 7d volatility, gas/fee level, volume percentile) so a reader can verify the rule's output themselves.

**Stablecoin pair substitution:** For usdc-usdt, usdt-usd, usdc-usd, dai-usdc, the "good time" framing is replaced with a **depeg-check** section ("USDC is trading at $X.XXXX, within ±Y% of peg over the last 30 days").

**Supply page equivalent:** Each supply page carries an **emission outlook** box — next halving / issuance schedule / % of max supply circulating / 30-day net issuance — using the same mechanical philosophy.

Every pair and supply page carries a persistent "Not financial advice" disclosure. FTC affiliate disclosure sits adjacent to every monetized CTA.

## 6. Visual identity

Maximum differentiation from makepicsmall.com. At-a-glance side-by-side, the two sites must not read as siblings.

**Palette:**

- Background: cool off-white `#f7f8fa` (makepicsmall uses warm cream `#fffdf8`)
- Ink: near-black `#0a0e1a` (makepicsmall uses softer `#1a1a1a`)
- Primary accent: deep ink-indigo `#3730a3` for links and CTAs (opposite pole from makepicsmall's coral)
- Price ticks: forest `#065f46` positive, crimson `#b91c1c` negative
- Surface (calculator, tables): cool-gray `#eef0f4`
- Border: cool `#d7dae1`

**Typography:**

- Display / H1 / H2: **Fraunces** variable serif
- Body prose: **Source Serif 4**
- UI / nav / calculator labels: **IBM Plex Sans**
- Numbers / tickers / monospace: **IBM Plex Mono**

Serif body is the single biggest visual break from makepicsmall's all-Geist sans world.

**Layout texture:**

- Article max width 44rem; data-heavy pages widen to 56rem for tables
- Drop cap on the first paragraph of every supply page and guide
- Hairline horizontal rules (1px cool-gray) between article sections
- Small caps for table headers and metadata ("LAST UPDATED", "MAX SUPPLY")
- Calculator block: 1px border + subtle surface; serif stops at its edge; Plex Sans labels + Plex Mono figures inside so live updates stay snappy
- No playful iconography; minimal line icons at 1.5px stroke if needed

**Shared prose rhythm:** Inherits the tight h2 / h3 typography block now baked into `packages/site-template/src/styles/global.css` (ported from makepicsmall 2026-04-22). Sites override the color tokens (`--ink`, `--muted`, `--surface`, `--border`, `--site-accent-color`) but the heading rhythm, list spacing, and scroll-margin anchoring stay consistent across the network.

## 7. Legal / compliance

- "Not financial advice" banner/footer on every pair and supply page
- FTC affiliate disclosure beside every CEX CTA (reuses the template's `AffiliateDisclosure` component)
- `/methodology` page publishing the heuristic rule, data sources, cache TTL, and known limitations
- Geo-gating of CEX CTAs for restricted jurisdictions handled by the same geo-switching Worker (e.g. suppress Binance for US IPs, suppress Coinbase for sanctioned regions)
- All rates labelled as "estimate"; slippage tolerances named explicitly
- Cookie banner from the template (already scaffolded)

## 8. SEO / schema

- `ExchangeRateSpecification` on pair pages
- `QuantitativeValue` / `Dataset` on supply pages
- `FAQPage` + `Article` on guides
- `BreadcrumbList` on every URL beyond `/`
- `Organization` + `WebSite` site-wide (already in template)
- Per-page Open Graph images: generated from a static SVG template at build time (numbers baked in from the nightly rebuild snapshot)
- Stagger any future programmatic URL expansion at ≤100 URLs/day submitted to GSC to avoid "discovered, not indexed" flags

## 9. URL structure

```
/                           home — hero calculator + top pairs grid + supply grid
/convert/{from}-to-{to}     pair pages (25)
/convert/                   pair index (sortable by volume/popularity)
/supply/{token}             supply/tokenomics pages (10)
/supply/                    supply index
/guides/{slug}              evergreen guides (5)
/guides/                    guides index
/methodology                heuristic rule, data sources, cache TTL, disclosures
/about                      editorial voice + who-we-are
/contact
/privacy
/terms
/sponsored                  (template default)
```

## 10. Explicitly out of scope for MVP

- Programmatic expansion beyond 25 pair pages (deferred to post-launch wave once GSC indexing health is verified)
- Slippage-aware live quote proxy to 1inch / Jupiter quote endpoints (b-lazy already leaves room to add this without refactor; deferred)
- Cross-chain bridge UX (LI.FI / Rango) — single-chain swaps only at launch
- EMD satellite cluster cross-linking (no siblings built yet)
- Sponsored post intake (month 6+ gated behind traffic threshold)
- User accounts, watchlists, portfolio tracking
- On-chain price sourcing via RPC — CoinGecko is authoritative for MVP
- Cross-site footprint-hygiene infrastructure beyond distinct visual identity (separate concern tracked in vault [650 Footprint Hygiene] when it exists)

## 11. Affiliate / API prerequisites

Spec-level dependencies; specific signup timing handled in the implementation plan:

- CoinGecko API (free tier sufficient for single-call-per-minute pattern)
- 1inch referral params (self-serve, no approval needed)
- Jupiter platform fee setup (self-serve)
- CEX affiliate programs: Binance, Bybit, Coinbase, Kraken, MEXC — application in parallel with build; site ships with placeholder links if any aren't approved by launch
- Ledger, Trezor affiliate programs (Impact-network style)
- Koinly affiliate program

## 12. Dependencies / shared packages

- Consumes `packages/site-template` via pnpm workspace (same as makepicsmall)
- Adds nothing net-new to the shared template — the pair/supply/guide collections, calculator island, and Worker are site-local so they don't contaminate future sites with crypto-specific code
- If Worker patterns generalize (e.g. geo-switched CTAs) they get extracted to `packages/` in a later refactor after the pattern proves itself

## 13. Success criteria (what "done" means for MVP)

- All 40 pages built and live at https://howmanycoin.com
- Lighthouse Performance ≥90, Accessibility ≥95, SEO ≥95 on mobile for at least the home, one pair page, one supply page, and one guide
- `/api/rate` Worker returns cached responses within 30ms p95 and triggers at most one CoinGecko call per minute under synthetic load of 100 req/s
- Geo-switching verified on US and non-US IPs (manual spot-check via a VPN or curl with synthetic headers)
- All pair and supply pages validate against their declared schema.org types (Google Rich Results Test)
- `/methodology` published, linked in footer, and referenced from every commentary box
- Sitemap submitted to GSC; robots.txt allows indexing
- No reference to makepicsmall, no shared coral or Geist in the rendered output
