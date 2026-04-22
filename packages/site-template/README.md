# site-template

Foundational Astro 5 scaffold used to launch every site in the network. One
template, many forks — each derivative site is a thin repo under `sites/`
with its own `site.config.ts`, content, and Cloudflare Pages project.

## Stack

- Astro 5 (SSG)
- Tailwind CSS v4 (via `@tailwindcss/vite`; theme tokens in `src/styles/global.css`)
- MDX for long-form content
- Preact (via `@astrojs/preact`, `compat: false`) for interactive tool islands
- `@astrojs/sitemap` + `@astrojs/rss` for feeds

## What's included

- Typed per-site config at `src/config/site.config.ts`
- Layouts: `BaseLayout`, `PostLayout` (Article JSON-LD), `ToolLayout`
  (SoftwareApplication), `GameLayout` (VideoGame)
- Schema components covering Organization, WebSite, Article, FAQ,
  SoftwareApplication, VideoGame, BreadcrumbList
- Standard pages: home, about, contact, privacy, terms, sponsored intake,
  404, `rss.xml`, `robots.txt`
- Content collections: `blog`, `tools`, `games` (all Zod-validated)
- Feature flags (`hasBlog`, `hasTool`, `hasGame`, `hasSponsoredIntake`)
  that gate routes and nav
- Minimal first-party cookie banner (localStorage; no third-party deps)
- Accessible baseline: skip-link, landmarks, visible focus rings

## How to fork into a new site

Use the root CLI — it copies this package, rewrites tokens, and (optionally)
initializes a git repo:

    node scripts/create-site.mjs --name acme --domain acme.com --niche health --description "Short description"

Next steps the CLI prints:

    cd sites/acme.com
    pnpm install
    pnpm dev

## How `site.config.ts` works

Every layout, component, and schema block reads from the single exported
`siteConfig` object. To brand a site, edit only this file: identity,
branding colors, org / social links, SEO defaults, feature flags,
monetization strings, schema defaults, and primary nav.

Two values are projected into CSS at render time via `BaseLayout.astro`:
`branding.themeColor` → `--site-theme-color`, `branding.accentColor` →
`--site-accent-color`. Tailwind v4's `@theme` directive (see
`src/styles/global.css`) aliases these to `--color-brand` /
`--color-accent` so you can use `text-brand`, `bg-accent`, etc. in markup.

## Overriding layouts / components per site

Two patterns, pick whichever fits:

1. Edit the copied file inside `sites/<domain>/src/...`. Each site owns its
   full source — the template is a starting point, not a runtime dependency.
2. Shadow only what you need by creating a file at the same relative path in
   the site repo. Since the site owns the whole tree after forking, this is
   just normal file editing.

## Cloudflare Pages deploy

Required secrets on the site's GitHub repo:

- `CLOUDFLARE_API_TOKEN` — scoped to "Pages: Edit"
- `CLOUDFLARE_ACCOUNT_ID` — Cloudflare account ID

Required repo variable:

- `CLOUDFLARE_PROJECT_NAME` — the Pages project slug (must match
  `wrangler.toml`)

Workflow: `.github/workflows/deploy.yml` runs on push to `main`.

## Analytics plug-in point

`BaseLayout.astro` exposes two slots:

- `<slot name="head" />` — inject Plausible/GA4/Fathom tags
- `<slot name="body-end" />` — inject scripts that must be at end of `<body>`

The cookie banner dispatches `window` CustomEvent `cookie-consent-changed`
with the user's choice, so gated loaders can listen and conditionally
initialize.

## Scripts

- `pnpm dev` — local dev
- `pnpm build` — static build into `dist/`
- `pnpm preview` — preview the built site
- `pnpm check` — `astro check` (TypeScript + Astro diagnostics)
