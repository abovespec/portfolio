// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import preact from '@astrojs/preact';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';
import { siteConfig } from './src/config/site.config.ts';

// Derive canonical site URL from per-site config. Each fork sets its own domain
// in src/config/site.config.ts; Astro uses this for sitemap + canonical links.
const siteUrl = `https://${siteConfig.identity.domain}`;

export default defineConfig({
  site: siteUrl,
  output: 'static',
  prefetch: {
    defaultStrategy: 'viewport',
  },
  integrations: [
    mdx(),
    preact({ compat: false }),
    sitemap(),
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },
  build: {
    inlineStylesheets: 'auto',
  },
  vite: {
    // Cast: Tailwind's Vite plugin is typed against Vite 7, Astro 5.18 still
    // bundles Vite 6. Runtime interop is fine; the cast silences the type
    // conflict and can be removed when Astro moves to Vite 7.
    plugins: [/** @type {any} */ (tailwindcss())],
    ssr: {
      noExternal: [],
    },
  },
});
