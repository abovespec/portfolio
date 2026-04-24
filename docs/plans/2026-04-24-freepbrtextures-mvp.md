# FreePBRTextures.com MVP Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Transform the placeholder freepbrtextures.com site into a functional free PBR texture download site with dark theme, texture browsing, category pages, and individual texture detail pages.

**Architecture:** Astro 5 static site with content collections for textures. Procedural textures generated via Python pipeline (numpy/scipy) and stored as static assets. Dark theme throughout. Amber accent color to differentiate from other network sites.

**Tech Stack:** Astro 5, Tailwind CSS 4, Preact (for interactive tile preview), TypeScript, content collections.

**Key Decision:** Site copy says "generated" textures, NOT "AI-generated". Procedural generation is the approach. AI can come later when GPUs are available.

---

## Phase 1: Foundation — Theme, Config, Content Schema

### Task 1: Update site config with texture-site identity

**Objective:** Replace the generic placeholder config with freepbrtextures branding.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/config/site.config.ts`

**Steps:**

1. Update `siteConfig` object:
   - `identity.name`: "FreePBRTextures"
   - `identity.description`: "Free seamless PBR textures for game devs and 3D artists. 4K resolution. CC0 license. No signup required."
   - `branding.themeColor`: "#0f172a" (deep slate - already set)
   - `branding.accentColor`: "#f59e0b" (amber - replaces blue)
   - `branding.logoText`: "FreePBRTextures"
   - `org.organizationName`: "FreePBRTextures"
   - `features.hasBlog`: true
   - `features.hasTool`: false
   - `features.hasGame`: false
   - `features.hasSponsoredIntake`: false
   - `nav.primary`: [{ label: "Textures", href: "/textures/" }, { label: "Categories", href: "/categories/" }, { label: "Blog", href: "/blog/" }, { label: "About", href: "/about/" }]

2. Update `package.json` description to match.

**Verify:** Site builds without errors: `cd ~/site-network/sites/freepbrtextures.com && pnpm build`

**Commit:** `feat: update site config for FreePBRTextures branding`

---

### Task 2: Add textures content collection schema

**Objective:** Define the Astro content collection schema for texture entries.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/content/config.ts`
- Create: `~/site-network/sites/freepbrtextures.com/src/content/textures/` (directory)

**Steps:**

1. Add a `textures` collection to `config.ts`:

```typescript
const textures = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string().max(80),
    description: z.string().max(200),
    category: z.string(),
    tags: z.array(z.string()).default([]),
    resolution: z.string().default('4K'),
    maps: z.object({
      albedo: z.boolean().default(true),
      normal: z.boolean().default(true),
      roughness: z.boolean().default(true),
      metallic: z.boolean().default(false),
      height: z.boolean().default(false),
    }),
    license: z.string().default('CC0'),
    seed: z.string().optional(),
    generatedDate: z.coerce.date(),
    publishDate: z.coerce.date(),
    draft: z.boolean().default(false),
    urlSlug: z.string(),
    // Image paths relative to /public/textures/
    thumbnail: z.string(),
    preview: z.string(),
    fullSize: z.string(),
  }),
});
```

2. Export it in the collections object: `export const collections = { blog, tools, games, textures };`

3. Create the `src/content/textures/` directory.

**Verify:** `pnpm build` succeeds, TypeScript types generated for textures collection.

**Commit:** `feat: add textures content collection schema`

---

### Task 3: Create dark theme global styles

**Objective:** Override the light theme with a dark theme throughout the site.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/styles/global.css`

**Steps:**

1. Update `:root` CSS variables for dark theme:
```css
:root {
  --site-theme-color: #0f172a;
  --site-accent-color: #f59e0b;
  --site-font-sans: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --site-font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  --ink: #f1f5f9;
  --muted: #94a3b8;
  --surface: #1e293b;
  --border: #334155;
  --card-bg: #1e293b;
  --card-hover: #334155;
}
```

2. Update `body` styles:
```css
body {
  font-family: var(--site-font-sans);
  background: #0f172a;
  color: var(--ink);
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
```

3. Add texture-specific utility classes:
```css
/* Texture card grid */
.texture-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

/* Tiled texture preview - shows 4x4 tiles to demonstrate seamlessness */
.texture-tiled {
  background-repeat: repeat;
  background-size: 12.5% 12.5%;
  image-rendering: auto;
}

/* Texture map swatch strip */
.map-strip {
  display: flex;
  gap: 0.5rem;
}
.map-strip img {
  width: 48px;
  height: 48px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid var(--border);
}

/* Category card */
.category-card {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--border);
  aspect-ratio: 16 / 10;
  transition: border-color 0.2s;
}
.category-card:hover {
  border-color: var(--site-accent-color);
}
```

4. Update prose styles for dark theme:
```css
.prose { color: var(--ink); }
.prose h2, .prose h3, .prose h4 { color: var(--ink); }
.prose a { color: var(--site-accent-color); }
.prose code { background: var(--surface); color: var(--ink); }
.prose blockquote { border-left-color: var(--site-accent-color); color: var(--muted); }
.prose hr { border-top-color: var(--border); }
.prose th { background: var(--surface); }
.prose td { border-bottom-color: var(--border); }
```

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: add dark theme global styles for texture site`

---

### Task 4: Update BaseLayout for dark theme

**Objective:** Update the base layout to use dark theme colors.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/layouts/BaseLayout.astro`

**Steps:**

1. Change `<body>` class from `bg-white text-slate-900` to use the dark theme:
```html
<body class="flex min-h-screen flex-col bg-slate-900 text-slate-100">
```

2. Update the skip-link styling for dark background.

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: update BaseLayout for dark theme`

---

### Task 5: Update Header for dark theme and texture nav

**Objective:** Restyle the header for dark theme and update nav items.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/components/Header.astro`

**Steps:**

1. Update header styles for dark theme:
```html
<header class="border-b border-slate-700 bg-slate-900/80 backdrop-blur-sm sticky top-0 z-50">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
    <a href="/" class="text-xl font-bold tracking-tight text-amber-400">{logoText}</a>
    <nav aria-label="Primary">
      <ul class="flex items-center gap-6 text-sm font-medium text-slate-300">
        {items.map((l) => (
          <li><a href={l.href} class="hover:text-amber-400 transition-colors">{l.label}</a></li>
        ))}
      </ul>
    </nav>
  </div>
</header>
```

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: update Header for dark theme`

---

### Task 6: Update Footer for dark theme and texture links

**Objective:** Restyle footer for dark theme with texture-relevant links.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/components/Footer.astro`

**Steps:**

1. Update footer for dark theme:
```html
<footer class="mt-16 border-t border-slate-700 bg-slate-800">
  <div class="mx-auto max-w-6xl px-4 py-8 text-sm text-slate-400">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <p>&copy; {year} {organizationName}. All textures are CC0 licensed.</p>
      <nav aria-label="Legal">
        <ul class="flex gap-4">
          <li><a href="/about/" class="hover:text-amber-400">About</a></li>
          <li><a href="/contact/" class="hover:text-amber-400">Contact</a></li>
          <li><a href="/privacy/" class="hover:text-amber-400">Privacy</a></li>
          <li><a href="/terms/" class="hover:text-amber-400">Terms</a></li>
        </ul>
      </nav>
    </div>
  </div>
</footer>
```

2. Remove AffiliateDisclosure since `hasBlog` and `hasTool` may not apply in the same way.

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: update Footer for dark theme`

---

## Phase 2: Homepage

### Task 7: Build homepage hero + category grid

**Objective:** Create the homepage with hero section, category grid, featured textures, and CC0 callout.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/pages/index.astro`

**Steps:**

1. Replace the entire homepage content with:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import { getCollection } from 'astro:content';

const allTextures = (await getCollection('textures', ({ data }) => !data.draft))
  .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf());

const categories = [...new Set(allTextures.map(t => t.data.category))];
const recentlyAdded = allTextures.slice(0, 8);

const categoryLabels: Record<string, string> = {
  wood: 'Wood',
  stone: 'Stone',
  metal: 'Metal',
  concrete: 'Concrete',
  fabric: 'Fabric',
  brick: 'Brick',
  marble: 'Marble',
  leather: 'Leather',
  grass: 'Grass',
  dirt: 'Dirt',
  sand: 'Sand',
  asphalt: 'Asphalt',
  tile: 'Tile',
  carpet: 'Carpet',
};
---
<BaseLayout title={siteConfig.identity.name} description={siteConfig.identity.description}>
  <!-- Hero Section -->
  <section class="py-16 sm:py-24 text-center">
    <h1 class="text-4xl sm:text-5xl font-bold tracking-tight text-white max-w-3xl mx-auto">
      Free Seamless PBR Textures for Game Devs and 3D Artists
    </h1>
    <p class="mt-4 text-lg text-slate-400 max-w-2xl mx-auto">
      4K resolution. CC0 license. No signup required. Generated procedurally for infinite variety.
    </p>
    <div class="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
      <a href="/textures/" class="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-slate-900 font-semibold rounded-lg transition-colors">
        Browse All Textures
      </a>
      <a href="/categories/" class="px-6 py-3 border border-slate-600 hover:border-amber-400 text-slate-300 hover:text-amber-400 font-semibold rounded-lg transition-colors">
        View Categories
      </a>
    </div>
    <!-- Stats bar -->
    <div class="mt-12 flex flex-wrap items-center justify-center gap-8 text-sm text-slate-500">
      <span class="flex items-center gap-2">
        <span class="text-amber-400 font-bold text-lg">{allTextures.length}+</span> textures
      </span>
      <span class="flex items-center gap-2">
        <span class="text-amber-400 font-bold text-lg">4K</span> resolution
      </span>
      <span class="flex items-center gap-2">
        <span class="text-amber-400 font-bold text-lg">CC0</span> licensed
      </span>
      <span class="flex items-center gap-2">
        <span class="text-amber-400 font-bold text-lg">{categories.length}</span> categories
      </span>
    </div>
  </section>

  <!-- Category Grid -->
  {categories.length > 0 && (
    <section class="py-12">
      <h2 class="text-2xl font-bold text-white mb-6">Browse by Category</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        {categories.map((cat) => {
          const catTextures = allTextures.filter(t => t.data.category === cat);
          const sample = catTextures[0];
          return (
            <a href={`/textures/?category=${cat}`} class="category-card group">
              {sample && (
                <img
                  src={sample.data.thumbnail}
                  alt={`${categoryLabels[cat] || cat} textures`}
                  class="w-full h-full object-cover"
                  loading="lazy"
                />
              )}
              <div class="absolute inset-0 bg-gradient-to-t from-slate-900/90 to-transparent flex items-end p-4">
                <div>
                  <h3 class="text-white font-semibold text-lg">{categoryLabels[cat] || cat}</h3>
                  <p class="text-slate-400 text-sm">{catTextures.length} textures</p>
                </div>
              </div>
            </a>
          );
        })}
      </div>
    </section>
  )}

  <!-- Recently Added -->
  {recentlyAdded.length > 0 && (
    <section class="py-12">
      <h2 class="text-2xl font-bold text-white mb-6">Recently Added</h2>
      <div class="texture-grid">
        {recentlyAdded.map((texture) => (
          <a href={`/textures/${texture.data.category}/${texture.data.urlSlug}/`} class="group rounded-lg border border-slate-700 bg-slate-800 hover:border-amber-400 transition-colors overflow-hidden">
            <div class="aspect-square overflow-hidden">
              <img
                src={texture.data.preview}
                alt={texture.data.title}
                class="w-full h-full object-cover group-hover:scale-105 transition-transform"
                loading="lazy"
              />
            </div>
            <div class="p-4">
              <h3 class="text-white font-medium text-sm">{texture.data.title}</h3>
              <p class="text-slate-400 text-xs mt-1 capitalize">{texture.data.category}</p>
            </div>
          </a>
        ))}
      </div>
    </section>
  )}

  <!-- CC0 Callout -->
  <section class="py-12 text-center border-t border-slate-800">
    <h2 class="text-2xl font-bold text-white">All Textures Are CC0 Licensed</h2>
    <p class="mt-2 text-slate-400 max-w-xl mx-auto">
      Use them commercially. Modify them. Share them. No attribution required.
    </p>
    <a href="/about/" class="mt-4 inline-block text-amber-400 hover:text-amber-300 underline">
      Learn more about our license
    </a>
  </section>
</BaseLayout>
```

**Verify:** `pnpm build` succeeds. Homepage renders with hero, categories, recent textures, CC0 callout.

**Commit:** `feat: build homepage with hero, category grid, recently added, CC0 callout`

---

## Phase 3: Texture Browsing Pages

### Task 8: Create textures browse page with filtering

**Objective:** Build the main textures browse page at `/textures/` with category filtering and search.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/textures/index.astro`

**Steps:**

1. Create the browse page:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import { getCollection } from 'astro:content';

const allTextures = (await getCollection('textures', ({ data }) => !data.draft))
  .sort((a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf());

const categories = [...new Set(allTextures.map(t => t.data.category))].sort();
const categoryLabels: Record<string, string> = { /* same as homepage */ };

// Get category filter from URL
const url = new URL(Astro.url);
const filterCategory = url.searchParams.get('category');

const filteredTextures = filterCategory
  ? allTextures.filter(t => t.data.category === filterCategory)
  : allTextures;
---
<BaseLayout title="Browse Textures" description="Browse all free PBR textures by category, resolution, and more.">
  <div class="flex flex-col lg:flex-row gap-8">
    <!-- Sidebar Filters -->
    <aside class="lg:w-64 flex-shrink-0">
      <div class="rounded-lg border border-slate-700 bg-slate-800 p-6 sticky top-20">
        <h2 class="text-white font-semibold mb-4">Filters</h2>

        <h3 class="text-slate-400 text-sm font-medium mb-2 uppercase tracking-wide">Category</h3>
        <ul class="space-y-1 mb-6">
          <li>
            <a href="/textures/" class={`text-sm hover:text-amber-400 ${!filterCategory ? 'text-amber-400 font-medium' : 'text-slate-300'}`}>
              All ({allTextures.length})
            </a>
          </li>
          {categories.map(cat => (
            <li>
              <a href={`/textures/?category=${cat}`} class={`text-sm hover:text-amber-400 ${filterCategory === cat ? 'text-amber-400 font-medium' : 'text-slate-300'}`}>
                {categoryLabels[cat] || cat} ({allTextures.filter(t => t.data.category === cat).length})
              </a>
            </li>
          ))}
        </ul>

        <h3 class="text-slate-400 text-sm font-medium mb-2 uppercase tracking-wide">Resolution</h3>
        <ul class="space-y-1">
          <li><span class="text-sm text-slate-300">4K (4096 x 4096)</span></li>
        </ul>

        <h3 class="text-slate-400 text-sm font-medium mb-2 mt-6 uppercase tracking-wide">License</h3>
        <ul class="space-y-1">
          <li><span class="text-sm text-slate-300">CC0 (Public Domain)</span></li>
        </ul>
      </div>
    </aside>

    <!-- Texture Grid -->
    <div class="flex-1">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold text-white">
          {filterCategory ? `${categoryLabels[filterCategory] || filterCategory} Textures` : 'All Textures'}
        </h1>
        <span class="text-slate-400 text-sm">{filteredTextures.length} textures</span>
      </div>

      <div class="texture-grid">
        {filteredTextures.map(texture => (
          <a href={`/textures/${texture.data.category}/${texture.data.urlSlug}/`} class="group rounded-lg border border-slate-700 bg-slate-800 hover:border-amber-400 transition-colors overflow-hidden">
            <div class="aspect-square overflow-hidden bg-slate-900">
              <img
                src={texture.data.preview}
                alt={texture.data.title}
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                loading="lazy"
              />
            </div>
            <div class="p-4">
              <h3 class="text-white font-medium text-sm truncate">{texture.data.title}</h3>
              <div class="flex items-center justify-between mt-2">
                <span class="text-slate-400 text-xs capitalize">{texture.data.category}</span>
                <span class="text-slate-500 text-xs">{texture.data.resolution}</span>
              </div>
            </div>
          </a>
        ))}
      </div>

      {filteredTextures.length === 0 && (
        <p class="text-center text-slate-400 py-12">No textures found in this category yet. Check back soon!</p>
      )}
    </div>
  </div>
</BaseLayout>
```

**Verify:** `pnpm build` succeeds. Browse page shows grid with sidebar filters.

**Commit:** `feat: create textures browse page with category filtering`

---

### Task 9: Create individual texture detail page

**Objective:** Build the per-texture page at `/textures/[category]/[slug]/` with tiled preview, PBR map gallery, and download buttons.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/textures/[category]/[...slug].astro`

**Steps:**

1. Create the dynamic texture page:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import { getCollection } from 'astro:content';

const { category, slug } = Astro.params;
const allTextures = await getCollection('textures', ({ data }) => !data.draft);

const texture = allTextures.find(
  t => t.data.category === category && t.data.urlSlug === slug
);

if (!texture) {
  return Astro.redirect('/textures/');
}

const { data } = texture;
const siblings = allTextures
  .filter(t => t.data.category === category && t.data.urlSlug !== slug)
  .slice(0, 4);

const mapLabels = {
  albedo: 'Albedo / Diffuse',
  normal: 'Normal Map',
  roughness: 'Roughness Map',
  metallic: 'Metallic Map',
  height: 'Height Map',
};
---
<BaseLayout title={data.title} description={data.description}>
  <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
    <!-- Left: Preview -->
    <div class="lg:col-span-2">
      <!-- Main tiled preview -->
      <div class="rounded-lg border border-slate-700 bg-slate-800 p-4 mb-6">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-2xl font-bold text-white">{data.title}</h1>
          <span class="px-3 py-1 bg-amber-500/20 text-amber-400 text-xs font-medium rounded-full">
            {data.license}
          </span>
        </div>

        <!-- Tiled preview showing seamlessness -->
        <div class="rounded-lg overflow-hidden bg-slate-900 aspect-square">
          <img
            src={data.preview}
            alt={`${data.title} - tiled preview`}
            class="w-full h-full object-cover texture-tiled"
            style={`background-image: url(${data.preview}); background-size: 12.5% 12.5%;`}
          />
        </div>
        <p class="text-slate-500 text-xs mt-2">Preview shown as 4x4 tiled pattern to demonstrate seamless edges.</p>
      </div>

      <!-- PBR Map Gallery -->
      <div class="rounded-lg border border-slate-700 bg-slate-800 p-6">
        <h2 class="text-lg font-semibold text-white mb-4">PBR Maps</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          {Object.entries(data.maps).map(([map, available]) => {
            if (!available) return null;
            return (
              <div class="rounded-lg border border-slate-700 overflow-hidden group">
                <a href={data.fullSize} download class="block">
                  <div class="aspect-square bg-slate-900 overflow-hidden">
                    <img
                      src={data.preview}
                      alt={`${mapLabels[map as keyof typeof mapLabels]} for ${data.title}`}
                      class="w-full h-full object-cover"
                      loading="lazy"
                    />
                  </div>
                  <div class="p-3">
                    <p class="text-white text-sm font-medium">{mapLabels[map as keyof typeof mapLabels]}</p>
                    <p class="text-slate-500 text-xs mt-1">Click to download</p>
                  </div>
                </a>
              </div>
            );
          })}
        </div>
      </div>
    </div>

    <!-- Right: Details + Downloads (sticky) -->
    <div class="lg:col-span-1">
      <div class="rounded-lg border border-slate-700 bg-slate-800 p-6 sticky top-20">
        <h2 class="text-lg font-semibold text-white mb-4">Download</h2>

        <div class="space-y-3 mb-6">
          {Object.entries(data.maps).map(([map, available]) => {
            if (!available) return null;
            return (
              <a
                href={data.fullSize}
                download
                class="flex items-center justify-between p-3 rounded-lg border border-slate-600 hover:border-amber-400 bg-slate-700/50 hover:bg-slate-700 transition-colors block"
              >
                <span class="text-slate-300 text-sm">{mapLabels[map as keyof typeof mapLabels]}</span>
                <span class="text-amber-400 text-xs font-medium">PNG</span>
              </a>
            );
          })}
        </div>

        <a
          href={data.fullSize}
          download
          class="w-full py-3 bg-amber-500 hover:bg-amber-400 text-slate-900 font-semibold text-center rounded-lg transition-colors block mb-6"
        >
          Download All Maps (ZIP)
        </a>

        <div class="border-t border-slate-700 pt-4">
          <h3 class="text-slate-400 text-sm font-medium mb-3 uppercase tracking-wide">Details</h3>
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-slate-500">Resolution</dt>
              <dd class="text-slate-300">{data.resolution} (4096 x 4096)</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-slate-500">Category</dt>
              <dd class="text-slate-300 capitalize">{data.category}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-slate-500">License</dt>
              <dd class="text-amber-400 font-medium">{data.license}</dd>
            </div>
            {data.seed && (
              <div class="flex justify-between">
                <dt class="text-slate-500">Seed</dt>
                <dd class="text-slate-300 font-mono text-xs">{data.seed}</dd>
              </div>
            )}
            <div class="flex justify-between">
              <dt class="text-slate-500">Generated</dt>
              <dd class="text-slate-300">{data.generatedDate.toLocaleDateString()}</dd>
            </div>
          </dl>
        </div>

        {data.tags.length > 0 && (
          <div class="border-t border-slate-700 pt-4 mt-4">
            <h3 class="text-slate-400 text-sm font-medium mb-2 uppercase tracking-wide">Tags</h3>
            <div class="flex flex-wrap gap-2">
              {data.tags.map(tag => (
                <span class="px-2 py-1 bg-slate-700 text-slate-400 text-xs rounded">{tag}</span>
              ))}
            </div>
          </div>
        )}

        {siblings.length > 0 && (
          <div class="border-t border-slate-700 pt-4 mt-4">
            <h3 class="text-slate-400 text-sm font-medium mb-3 uppercase tracking-wide">Similar Textures</h3>
            <div class="grid grid-cols-2 gap-2">
              {siblings.map(sibling => (
                <a href={`/textures/${sibling.data.category}/${sibling.data.urlSlug}/`} class="group">
                  <img
                    src={sibling.data.thumbnail}
                    alt={sibling.data.title}
                    class="w-full aspect-square object-cover rounded border border-slate-700 group-hover:border-amber-400 transition-colors"
                    loading="lazy"
                  />
                  <p class="text-slate-400 text-xs mt-1 truncate">{sibling.data.title}</p>
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  </div>
</BaseLayout>
```

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: create individual texture detail page with preview, maps, downloads`

---

### Task 10: Create categories hub page

**Objective:** Build `/categories/` page showing all categories with visual cards and texture counts.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/categories/index.astro`

**Steps:**

1. Create the categories hub:

```astro
---
import BaseLayout from '~/layouts/BaseLayout.astro';
import { siteConfig } from '~/config/site.config';
import { getCollection } from 'astro:content';

const allTextures = await getCollection('textures', ({ data }) => !data.draft);
const categories = [...new Set(allTextures.map(t => t.data.category))].sort();

const categoryLabels: Record<string, string> = { /* same as above */ };
const categoryDescriptions: Record<string, string> = {
  wood: 'Wood grain, planks, logs, and timber textures.',
  stone: 'Natural stone, rock faces, and geological formations.',
  metal: 'Brushed, polished, and weathered metal surfaces.',
  concrete: 'Cast concrete, cement, and industrial surfaces.',
  fabric: 'Cloth, canvas, textile, and woven materials.',
  brick: 'Clay brick, cobblestone, and masonry patterns.',
  marble: 'Veined marble and polished stone surfaces.',
  leather: 'Grain leather, suede, and hide textures.',
  grass: 'Grass, turf, and ground cover textures.',
  dirt: 'Soil, earth, and ground textures.',
  sand: 'Sand, sandy ground, and desert surfaces.',
  asphalt: 'Road, pavement, and asphalt textures.',
  tile: 'Ceramic tile, mosaic, and patterned floor surfaces.',
  carpet: 'Carpet, rug, and floor covering textures.',
};
---
<BaseLayout title="Texture Categories" description="Browse free PBR textures organized by material category.">
  <h1 class="text-3xl font-bold text-white mb-2">Categories</h1>
  <p class="text-slate-400 mb-8">Browse all {allTextures.length} textures across {categories.length} material categories.</p>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
    {categories.map(cat => {
      const catTextures = allTextures.filter(t => t.data.category === cat);
      const sample = catTextures[0];
      return (
        <a href={`/textures/?category=${cat}`} class="group rounded-lg border border-slate-700 bg-slate-800 hover:border-amber-400 transition-colors overflow-hidden">
          <div class="aspect-video overflow-hidden bg-slate-900">
            {sample && (
              <img
                src={sample.data.preview}
                alt={`${categoryLabels[cat] || cat} category`}
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                loading="lazy"
              />
            )}
          </div>
          <div class="p-4">
            <h2 class="text-white font-semibold text-lg">{categoryLabels[cat] || cat}</h2>
            <p class="text-slate-400 text-sm mt-1">{categoryDescriptions[cat] || `${catTextures.length} free PBR textures.`}</p>
            <p class="text-amber-400 text-xs mt-2 font-medium">{catTextures.length} textures</p>
          </div>
        </a>
      );
    })}
  </div>
</BaseLayout>
```

**Verify:** `pnpm build` succeeds.

**Commit:** `feat: create categories hub page`

---

## Phase 4: Seed Content — Generate Sample Textures

### Task 11: Build Python procedural texture generator

**Objective:** Create a Python script that generates procedural PBR textures using numpy.

**Files:**
- Create: `~/site-network/scripts/generate_textures.py`

**Steps:**

1. Create the generator script with:
   - Perlin/simplex noise implementation (or use `noise` library)
   - FBM (Fractal Brownian Motion) for multi-octave detail
   - Worley/cell noise for granular patterns
   - Domain warping for organic flowing patterns
   - PBR map derivation (height -> normal via Sobel, roughness, metallic)
   - Support for categories: wood, stone, metal, concrete, fabric, brick, marble, leather
   - Output: PNG files at 4K resolution with metadata JSON
   - Thumbnail generation at 256px, 512px, 1024px

2. Install dependencies: `pip install numpy scipy Pillow noise`

3. Generate 2-3 sample textures per category (15-20 total) for initial content.

4. Output structure:
   ```
   public/textures/
     wood/
       oak-planks-warm/
         albedo.png (4K)
         normal.png
         roughness.png
         preview.png (1024px)
         thumbnail.png (256px)
         metadata.json
     stone/
       ...
   ```

**Verify:** Script runs and generates valid PNG outputs.

**Commit:** `feat: create procedural texture generator script`

---

### Task 12: Generate content collection entries for sample textures

**Objective:** Create `.mdx` content collection entries for the generated textures.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/content/textures/*.mdx`

**Steps:**

1. For each generated texture, create an MDX file with frontmatter matching the schema:
```mdx
---
title: 'Warm Oak Planks'
description: 'Seamless 4K procedural wood texture with warm oak grain pattern.'
category: 'wood'
tags: ['wood', 'planks', 'oak', 'warm', 'floor', 'indoor']
resolution: '4K'
maps:
  albedo: true
  normal: true
  roughness: true
  metallic: false
  height: false
license: 'CC0'
seed: 'oak-warm-42'
generatedDate: 2026-04-24
publishDate: 2026-04-24
draft: false
urlSlug: 'oak-planks-warm'
thumbnail: '/textures/wood/oak-planks-warm/thumbnail.png'
preview: '/textures/wood/oak-planks-warm/preview.png'
fullSize: '/textures/wood/oak-planks-warm/albedo.png'
---
```

2. Create entries for all generated textures (15-20 entries).

**Verify:** `pnpm build` succeeds with all textures indexed.

**Commit:** `feat: add initial texture content entries`

---

## Phase 5: SEO Pages and Polish

### Task 13: Update About page for texture site

**Objective:** Rewrite the About page to explain the project, CC0 license, and generation approach.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/pages/about.astro`

**Steps:**

1. Replace with content explaining:
   - What FreePBRTextures is
   - How textures are generated (procedural, seamless, deterministic)
   - CC0 license explanation
   - How to use the textures
   - Future roadmap hint (no AI mention yet)

**Commit:** `feat: update About page for texture site`

---

### Task 14: Create CC0 landing page (SEO)

**Objective:** Create a dedicated `/cc0-textures/` landing page targeting "free cc0 pbr textures" keyword.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/cc0-textures.astro`

**Steps:**

1. Create SEO-focused landing page with:
   - Explanation of CC0 license
   - Link to browse all textures
   - FAQ about commercial use
   - Schema markup (FAQPage)

**Commit:** `feat: create CC0 textures SEO landing page`

---

### Task 15: Create 4K textures landing page (SEO)

**Objective:** Create `/4k-textures/` landing page targeting "free 4k pbr textures" keyword.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/4k-textures.astro`

**Commit:** `feat: create 4K textures SEO landing page`

---

### Task 16: Create engine-specific landing pages (SEO)

**Objective:** Create landing pages for Unity, Unreal, Blender, Godot targeting engine-specific texture searches.

**Files:**
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/unity-textures.astro`
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/unreal-textures.astro`
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/blender-textures.astro`
- Create: `~/site-network/sites/freepbrtextures.com/src/pages/godot-textures.astro`

**Steps:**

1. Each page explains how to use CC0 PBR textures in that engine, with links to browse textures.

**Commit:** `feat: create engine-specific SEO landing pages`

---

### Task 17: Update robots.txt and sitemap

**Objective:** Ensure robots.txt and sitemap are configured correctly for the texture site.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/src/pages/robots.txt.ts`

**Steps:**

1. Verify sitemap includes all texture pages, categories, and SEO landing pages.
2. Update robots.txt to reference the sitemap.

**Commit:** `feat: configure robots.txt and sitemap for texture site`

---

### Task 18: Update favicon

**Objective:** Create a texture-themed favicon.

**Files:**
- Modify: `~/site-network/sites/freepbrtextures.com/public/favicon.svg`

**Steps:**

1. Replace with an amber-colored icon representing a texture/material (simple geometric pattern or checkerboard).

**Commit:** `feat: update favicon for FreePBRTextures`

---

### Task 19: Build and deploy

**Objective:** Final build verification and deploy to Cloudflare Pages.

**Steps:**

1. Run full build: `cd ~/site-network/sites/freepbrtextures.com && pnpm build`
2. Preview: `pnpm preview`
3. Deploy: `wrangler pages deploy dist --project-name=freepbrtextures`

**Commit:** `chore: deploy FreePBRTextures MVP`

---

## Summary

**Total tasks:** 19
**Phases:**
- Phase 1 (Foundation): Tasks 1-6 -- config, schema, dark theme, layouts
- Phase 2 (Homepage): Task 7
- Phase 3 (Browse): Tasks 8-10 -- browse page, detail page, categories
- Phase 4 (Content): Tasks 11-12 -- texture generation + content entries
- Phase 5 (SEO + Polish): Tasks 13-19 -- SEO pages, deploy

**Key decisions:**
- Dark theme throughout (competitor standard for texture sites)
- Amber accent color (#f59e0b) distinct from Site 1 (blue) and Site 2 (green/teal)
- "Generated" not "AI-generated" in all copy
- CC0 license prominently displayed
- Tiled preview on all texture cards to demonstrate seamlessness
- No user accounts needed
- No ads or paywall at launch

**Open for post-MVP:**
- WebGL material preview
- Batch download (ZIP)
- Engine-specific format packs
- Browser-based random texture generator
- AI-enhanced textures when GPU available
