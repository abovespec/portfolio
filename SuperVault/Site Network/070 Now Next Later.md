---
tags: [ops, kanban]
---

# 070 Now Next Later

## Now
- [ ] Pick tech stack (decide Astro vs Next) — [[300 Tech Stack]] — decided: Astro default + Next for dynamic-heavy sites
- [ ] Stand up image-gen rig — [[320 Local Image Gen Rig]] — user has hardware, setting up in coming days
- [ ] Build `site-template` repo — [[310 Site Template Repo]]
- [x] Pick first 3 niches — [[100 Niches Index]] — cohort 1 locked: compression + crypto hub + seamless textures
- [x] **Decide final domains** for cohort 1 — makepicsmall.com, howmanycoin.com, freepbrtextures.com
- [x] Register domains for cohort 1 — IONOS ($1) + Spaceship ($8.88) — auto-renew disabled
- [x] Point all 3 domains to Cloudflare DNS (2026-04-21 — single account for now; can split later if footprint signals matter)
- [x] Configure SSL strict, Always-HTTPS, Brotli, minify, HTTP/3, 0-RTT, TLS 1.2 min on all 3 zones via API
- [x] Build `site-template` repo (Astro 5 + Tailwind 4 + MDX + Preact) — located at ~/site-network/packages/site-template — see [[310 Site Template Repo]]
- [x] Keyword research CSV per niche — 3 files in [[200 Sites Index|cohort 1]] site notes
- [x] Generate + deploy placeholder sites for all 3 cohort-1 domains — all live at their .com + www URLs
- [ ] GitHub repos + CI (hybrid path) — set up private repos, connect to Cloudflare Pages for git-push deploys

## Next
- [x] **Site 1 (makepicsmall.com) MVP SHIPPED 2026-04-22** — live at https://makepicsmall.com — see [[202 Site 1 - Image Compression]]
- [ ] **Pick next activation from deploy-ready scaffold pool** — 10 sites have wrangler + CI wired and just need tool implementation (see [[200 Sites Index]]): colorpalette.io, gradientcss.io, jsonformat.io, jwtinspect.io, utmbuilder.io, wordcounttools.com, encodeonline.io, financalc.io, margincalc.io, flexplay.io — CEO to pick priority order

## After user wakes up
- [ ] **Submit makepicsmall.com sitemap** to Google Search Console + Bing Webmaster Tools + Ahrefs Webmaster Tools (manual user task)
- [ ] Enable Cloudflare Web Analytics on makepicsmall.com zone (1-click dashboard toggle)
- [ ] Test the live tool with real images on mobile + desktop
- [ ] Review the 4 launch blog posts; edit voice/facts if needed before publishing remaining 6 (Phase F)
- [ ] Phase F (tasks 28-31): staggered post publishing over next 14 days — remaining 6 posts (posts 5-10 from the plan), one every 2-3 days per [[700 Content Playbook]] cadence
- [ ] Set up per-site GitHub repos + hybrid git-push CI
- [ ] Plausible analytics decision (self-host $6/mo Hetzner VPS or stick with free Cloudflare Web Analytics)

## Site 2 / Site 3 (cohort 1 remaining)
- [ ] Site 2 (howmanycoin.com) — follow the same brainstorming → spec → plan → subagent-driven-dev loop but for the crypto conversion hub. DO NOT start before Site 1 has 2+ weeks of indexing data.
- [ ] Site 3 (freepbrtextures.com) — GPU rig dependent; brainstorm + plan once user's rig is online

## (archived-completed-today)
- [ ] Build first free tool (Site 1 compression) — [[820 Image Compression Site]]
- [ ] Launch Site 1 fully — [[610 Site Launch Checklist]] — validate playbook end-to-end before starting Site 2
- [ ] Build Site 2 once Site 1 is live and indexing

## Later
- [ ] Sponsored post intake page template — [[520 Sponsored Post Engine]]
- [ ] Social accounts per site — [[900 Social Media Playbook]]
- [ ] Flipping pipeline — [[510 Flipping Sites]]
