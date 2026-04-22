# Site Network

Monorepo for the site network project. See `~/SuperVault/Site Network/` for full plans.

## Structure

- `packages/site-template/` — the reusable Astro template every site is forked from
- `sites/` — actual site instances (one folder per domain)
- `scripts/` — `create-site.mjs` and other automation
- `packages/internal-*` — shared logic packages (compression codecs, crypto-rate fetchers, etc.) extracted as we go

## Quick start

```bash
pnpm install
pnpm create:site --name makepicsmall --domain makepicsmall.com --niche image-compression
```
