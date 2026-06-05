import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://favicongen.io',
  integrations: [preact(), sitemap()],
  vite: {
    plugins: [tailwindcss()]
  }
});
