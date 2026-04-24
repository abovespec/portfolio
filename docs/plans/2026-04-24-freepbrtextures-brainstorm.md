# freepbrtextures.com - Brainstorm Document

Generated: 2026-04-24
Status: Brainstorming phase - pre-plan

## Situation

- Domain freepbrtextures.com registered, placeholder site scaffolded
- GPU rig (2x RTX 5060 Ti/5070 Ti 16GB) occupied running LLM
- CPU: Ryzen 9 7900X 12C/24T, 96GB DDR5 - available for texture generation
- Goal: Build a free seamless PBR texture download site for game devs and 3D artists

---

## Part A: CPU-Based Texture Generation Strategy

### The Core Insight

Procedural texture generation is NOT a compromise here -- it's potentially a *strength*.

Why:
1. **Inherently tileable** - Wrapping noise coordinates guarantees seamless edges. AI-generated textures require post-processing to fix seams, which often introduces artifacts.
2. **Zero copyright concerns** - No training data, no model weights, no AI legal gray zone. Pure math.
3. **PBR-native** - The same noise functions that generate height maps can derive normal maps, roughness maps, and metallic maps with different parameters. One procedural call produces the entire PBR set.
4. **Instant generation** - 4K textures in seconds, not minutes.
5. **Infinite variety** - Randomize seed + parameters = endless unique textures.
6. **Deterministic** - Same seed always produces the same texture. Users can share seeds.

### Recommended Approach: Python Procedural Pipeline

**Core library: numpy + scipy.ndimage**

No heavy dependencies needed. NumPy for array operations, scipy for filters (Gaussian blur, Sobel for normal maps).

**Noise functions to implement/use:**
- Perlin/Simplex noise (for smooth organic patterns - wood grain, stone veining)
- Worley/Cell noise (for granular patterns - concrete, stone, fabric weave)
- Value noise (general purpose)
- FBM (Fractal Brownian Motion) - layer noise at multiple octaves for realistic detail
- Domain warping - use one noise to distort another, creates organic flowing patterns (great for wood grain, marble veining)

**Texture category -> noise mapping:**

| Category | Primary Noise | Secondary Noise | Key Technique |
|----------|--------------|-----------------|---------------|
| Wood | FBM + directional bias | Domain warped Perlin | Ring patterns via radial noise modulation |
| Stone | Worley + FBM | Erosion via noise thresholding | Multi-scale granularity |
| Concrete | FBM + Worley | Gaussian blur + contrast | Stain patterns via domain warping |
| Metal | Directional noise | FBM micro-scratches | Brushed lines via anisotropic noise |
| Fabric | Crosshatch Worley | Fine-grained FBM | Weave pattern via grid + noise overlay |
| Brick | Grid pattern | Worley per-brick | Regular pattern + per-instance variation |
| Marble | Domain warped Perlin | FBM micro-veins | Flowing veins via noise masking |
| Leather | Worley + FBM | Crease patterns via directional noise | Organic folds |

**Pipeline per texture:**
1. Generate base height map (4K, numpy float32 array)
2. Derive normal map: Sobel filters on height map (dx, dy -> normal RGB)
3. Derive roughness map: FBM noise or constant value
4. Derive metallic map: Constant or noise-based
5. Albedo/diffuse: Colorize the height map with HSL variations
6. Save as PNG (RGBA for albedo, RGB for maps)
7. Generate thumbnail (downscale to 256x256, 512x512, 1024x1024)
8. Auto-generate metadata JSON (seed, parameters, category, tags)

**Existing tools to evaluate:**
- **texgen** (github.com/mikeaseven/texgen) - C++ library for procedural textures, can be used via Python bindings
- **NoiseGen** - Python noise libraries
- Custom Python with numpy (most flexible, full control)

**Throughput estimate:**
- 4K procedural texture generation: ~0.1-0.5 seconds per map
- Full PBR set (5 maps): ~0.5-2 seconds per texture
- 200 textures: ~100-400 seconds total (~2-7 minutes)
- Compare: AI SDXL on CPU would take 5-10 minutes PER texture = 1000-2000 minutes for 200

**Verdict: Build a custom Python procedural pipeline.** It's the right tool for this job.

### Hybrid Future Path

Once GPUs are available, we can:
1. Use procedural as the base layer
2. Run AI refinement pass for "organic polish"
3. Offer both "Procedural" and "AI-enhanced" texture collections

---

## Part B: Site Structure and User Experience

### Competitive Analysis (Key Competitors)

**ambientCG** (ambientcg.com) - CC0, clean dark UI, category grid, per-texture page with all PBR maps visible, download individual or ZIP. Simple, effective.

**PolyHaven** (polyhaven.com) - CC0, beautiful previews, 360 HDRI + textures + models. Strong search, filtering, 3D preview.

**Poliigon** (poliigon.com) - Freemium, gorgeous previews, live material preview in browser. Strong but paywalled for best content.

**Textures.com** - Freemium, huge library, free tier limited. Not CC0.

**Key patterns from competitors:**
- Dark UI (all of them) - makes textures pop
- Category-based browsing with visual thumbnails
- Per-texture page shows all PBR maps as separate previews
- One-click download (individual + full set ZIP)
- Search + filters (category, resolution, license, PBR maps available)
- CC0 prominently displayed

### Information Architecture

```
/                              Homepage - hero + featured + categories
/textures/                     All textures browse page (paginated, filterable)
/textures/[category]/          Category hub (wood, stone, metal, concrete, fabric, brick, marble, tile, fabric, leather, grass, dirt, sand, water, asphalt, carpet)
/textures/[category]/[slug]    Individual texture page
/search?q=                     Search results
/cc0-textures/                 License landing page (SEO)
/4k-textures/                  Resolution landing page (SEO)
/blender-materials/            Engine-specific landing (SEO)
/unity-textures/               Engine-specific landing (SEO)
/unreal-materials/             Engine-specific landing (SEO)
/godot-textures/               Engine-specific landing (SEO)
/blog/                         Educational content
/about/                        About + license explanation
/contact/                      Contact
/privacy/, /terms/, /sponsored/ Legal pages
```

### Homepage Design

**Hero section:**
- Bold headline: "Free Seamless PBR Textures for Game Devs and 3D Artists"
- Subheadline: "4K resolution. CC0 license. No signup required."
- Search bar prominently placed
- Below: Category grid (6-8 categories with thumbnail previews showing the textures tiled)
- Stats bar: "200+ textures | 4K resolution | CC0 licensed"

**Visual identity:**
- Dark theme (competitors all go dark, textures look better)
- Primary color: Deep slate (#0f172a) background
- Accent: Amber/warm orange (#f59e0b) - fits the "materials/texture" aesthetic, distinct from Site 1 (blue) and Site 2 (green/teal)
- Typography: System font stack for speed, monospace for technical details
- Subtle noise/grain texture on backgrounds (meta - a texture site with texture backgrounds)

**Key sections below hero:**
1. Category grid (visual, 2-3 rows)
2. Recently added textures (horizontal scroll or grid)
3. Featured collections (e.g., "Wood Pack", "Industrial Materials")
4. CTA: "All textures are CC0 - use them commercially, no attribution required"
5. Footer with engine-specific links, social, legal

### Texture Browsing Page (/textures/ and /textures/[category]/)

**Layout:**
- Left sidebar (collapsible on mobile): Filters
  - Category (checkbox list)
  - Resolution (4K, 2K, 1K)
  - Available maps (Albedo, Normal, Roughness, Metallic, Height)
  - License (CC0)
  - Sort: Newest, Popular, Name
- Main area: Grid of texture cards
  - Each card: Tiled preview thumbnail (show 2x2 tile to demonstrate seamlessness), category badge, resolution badge, download count
  - Hover: Quick preview of all available PBR maps in a small strip

**Tile preview:** Each thumbnail shows a 2x2 tiled version of the texture so users can immediately see it tiles seamlessly. This is a key differentiator we should highlight visually.

### Per-Texture Page (/textures/[category]/[slug])

**Layout (two-column on desktop):**
- Left (larger): Main preview
  - Large tiled preview (4x4 tiles to show seamlessness)
  - Toggle: Single view / Tiled view / Checkerboard view
  - All PBR maps displayed as a gallery: Albedo, Normal, Roughness, Metallic, Height
  - Click each map to view full resolution
- Right (sticky):
  - Texture name + category
  - Resolution: 4K (4096x4096)
  - License: CC0 badge
  - Download buttons:
    - Download Albedo (PNG)
    - Download Normal (PNG)
    - Download Roughness (PNG)
    - Download Metallic (PNG)
    - Download Height (PNG)
    - Download All (ZIP)
  - Tags: wood, planks, warm, indoor, floor
  - Technical info: File sizes, format, tile mode
  - Similar textures (3-4 thumbnails linked to sibling textures)

**URL structure for SEO:**
- `/textures/wood/oak-planks-warm/` - targets "oak wood pbr texture free"
- `/textures/concrete/rough-cast-wall/` - targets "rough concrete wall pbr"

### Content Collections

Need a new `textures` content collection with schema:

```typescript
const textures = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string().max(80),
    description: z.string().max(200),
    category: z.string(), // wood, stone, metal, concrete, fabric, etc.
    tags: z.array(z.string()).default([]),
    resolution: z.string(), // "4K", "2K"
    maps: z.object({
      albedo: z.boolean().default(true),
      normal: z.boolean().default(false),
      roughness: z.boolean().default(false),
      metallic: z.boolean().default(false),
      height: z.boolean().default(false),
    }),
    license: z.string().default('CC0'),
    seed: z.string().optional(), // procedural seed for reproducibility
    generatedDate: z.coerce.date(),
    publishDate: z.coerce.date(),
    draft: z.boolean().default(false),
    // SEO
    urlSlug: z.string(),
    // Image paths (relative to public/)
    thumbnail: z.string(), // 256x256 webp
    preview: z.string(), // 1024x1024 webp
    fullSize: z.string(), // 4K original
  }),
});
```

### Image Hosting Strategy

**Cloudflare R2** (zero egress fees):
- Store original 4K PNGs in R2
- Organize by category: `r2://freepbrtextures/textures/wood/oak-planks/albedo.png`

**Cloudflare Images** (responsive delivery):
- Upload optimized WebP variants: 256px, 512px, 1024px, 2048px, 4096px
- Use srcset for responsive loading

**Alternative (simpler for MVP):**
- Just store in R2 with CDN via Cloudflare
- Pre-generate WebP thumbnails at build time
- Serve directly from R2/Cloudflare edge

### Unique Features (Differentiators)

1. **Live tile preview** - Every texture shown tiled by default. Toggle to single view.
2. **Checkerboard mode** - Show texture on checkerboard (standard PBR preview mode)
3. **Seed sharing** - Since procedural, share the seed URL to get the exact same texture
4. **Batch download** - Download entire category as ZIP
5. **Engine-specific format packs** - Download pre-formatted for Unity (.unitypackage), Unreal (.uasset), Blender (addon format)
6. **PBR material preview** - Simple WebGL canvas showing the texture with lighting (later)
7. **Comparison tool** - Side-by-side comparison of textures
8. **Random generator** - "Generate new texture" button that creates a random procedural texture on the fly (WASM/JS noise in browser)

### SEO Strategy

**Sitemap:** Split sitemaps by category, max 50K URLs per sitemap. Plan for growth to 5,000+ textures.

**Internal linking:**
- Each texture page links to category hub, sibling textures, and related categories
- Category hubs link to parent browse page and child textures
- Blog posts link to relevant texture categories
- Landing pages (CC0, 4K, engine-specific) link to filtered texture grids

**Structured data:**
- `ImageObject` schema on texture pages
- `BreadcrumbList` on all pages
- `CollectionPage` on category pages
- `WebPage` on landing pages

**Content calendar:**
- Week 1: 4 educational blog posts (what is PBR, what is seamless, normal maps explained, roughness vs glossiness)
- Week 2: 4 competitor comparison posts (vs ambientCG, vs PolyHaven, etc.)
- Ongoing: 2-3 posts per week on texture techniques, tutorials, use cases

### Monetization Path

**Phase 1 (Launch):** No ads, no paywall. Pure CC0 giveaway to build traffic.
**Phase 2 (Month 3+):**
- Affiliate links: Unity Asset Store, Blender Market, Humble Bundle (3D packs)
- "Premium" packs: Curated collections with additional maps (displacement, AO, triplanar)
- Sponsored category spots
- Donation button

### Growth Loop

1. Generate 200 procedural textures (2-7 minutes on CPU)
2. Deploy site with full browse experience
3. Submit sitemaps to Google Search Console, Bing, Ahrefs Webmaster Tools
4. Publish 4 educational blog posts + 4 comparison posts
5. Generate 50 new textures every 2 weeks (1-2 minutes)
6. Add new categories based on search data
7. Phase 2: Add AI-enhanced textures when GPU available

---

## Part C: Technical Implementation Plan Overview

### Phase 1: Generation Pipeline (Week 1)
1. Build Python procedural texture generator
2. Implement noise functions (Perlin, Worley, FBM, domain warping)
3. Implement PBR map derivation (height -> normal, roughness, metallic)
4. Generate initial 200 textures across 5 categories
5. Generate thumbnails at multiple resolutions
6. Upload to R2 bucket

### Phase 2: Site Build (Week 1-2)
1. Redesign homepage with hero + category grid
2. Build texture content collection + schema
3. Build texture browse pages with filtering
4. Build per-texture pages with tiled preview + downloads
5. Build SEO landing pages (CC0, 4K, engine-specific)
6. Add sitemap generation for large URL counts
7. Deploy to Cloudflare Pages

### Phase 3: Content (Week 2-3)
1. Write 4 educational blog posts
2. Write 4 competitor comparison posts
3. Submit sitemaps
4. Set up analytics

### Phase 4: Polish (Week 3-4)
1. Add WebGL material preview
2. Add batch download feature
3. Add engine-specific format packs
4. Optimize Core Web Vitals

---

## Open Questions

1. Should we brand as "procedurally generated" or just "generated"? "AI-generated" is in some keyword targets but procedural is more honest.
2. Do we need user accounts? Competitors mostly don't require signup for downloads.
3. R2 bucket naming and access pattern - public or signed URLs?
4. Should we pre-generate engine-specific formats (Unity .unitypackage, Unreal materials) or keep it simple with PNG downloads initially?
5. Color palette confirmation - amber/warm accent vs something else?
