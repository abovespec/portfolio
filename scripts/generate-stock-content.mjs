#!/usr/bin/env node
/**
 * generate-stock-content.mjs
 *
 * Copies 980 WebP images from /tmp/stock_images/ into the stocksnap.fyi site's
 * public/images/ directory, and generates src/data/images.json with SEO metadata
 * for every image.
 *
 * Usage: node scripts/generate-stock-content.mjs
 */
import { cp, mkdir, writeFile, readdir } from 'node:fs/promises';
import { join, basename, extname } from 'node:path';

const SRC = '/tmp/stock_images';
const SITE = '/home/abovespec/site-network/sites/stocksnap.fyi';
const DEST_IMAGES = join(SITE, 'public', 'images');
const DEST_DATA = join(SITE, 'src', 'data', 'images.json');

const STYLE_LABELS = {
  warm: 'Warm',
  cool: 'Cool',
  neutral: 'Neutral',
  dramatic: 'Dramatic',
  bright: 'Bright',
};

const NICHE_META = {
  abstract_backgrounds: {
    display: 'Abstract Backgrounds',
    slug: 'abstract-backgrounds',
    clusters: {
      gradient_backgrounds: { display: 'Gradient Backgrounds', slug: 'gradient-backgrounds', keywords: ['gradient background', 'color gradient wallpaper', 'smooth gradient background', 'abstract gradient'] },
      watercolor_textures: { display: 'Watercolor Textures', slug: 'watercolor-textures', keywords: ['watercolor background', 'paint texture background', 'artistic watercolor splash', 'watercolor texture'] },
      minimalist_color_wash: { display: 'Minimalist Color Wash', slug: 'minimalist-color-wash', keywords: ['minimalist background', 'solid color background', 'clean color texture', 'minimalist abstract'] },
      dark_backgrounds: { display: 'Dark Backgrounds', slug: 'dark-backgrounds', keywords: ['dark abstract background', 'dark moody background', 'deep color background', 'dark texture'] },
      pastel_backgrounds: { display: 'Pastel Backgrounds', slug: 'pastel-backgrounds', keywords: ['pastel background', 'soft pastel colors', 'light pastel texture', 'pastel color'] },
      geometric_abstract: { display: 'Geometric Abstract', slug: 'geometric-abstract', keywords: ['geometric abstract background', 'abstract shapes background', 'modern geometric pattern', 'geometric design'] },
      blurred_soft_focus: { display: 'Blurred Soft Focus', slug: 'blurred-soft-focus', keywords: ['blurred background', 'out of focus background', 'soft abstract texture', 'bokeh blur'] },
    },
  },
  bokeh_backgrounds: {
    display: 'Bokeh Backgrounds',
    slug: 'bokeh-backgrounds',
    clusters: {
      abstract_color_bokeh: { display: 'Abstract Color Bokeh', slug: 'abstract-color-bokeh', keywords: ['abstract bokeh background', 'colorful bokeh', 'color bokeh blur', 'bokeh lights'] },
      city_lights_bokeh: { display: 'City Lights Bokeh', slug: 'city-lights-bokeh', keywords: ['city lights bokeh', 'urban bokeh background', 'night lights blur', 'city blur'] },
      cool_bokeh: { display: 'Cool Bokeh', slug: 'cool-bokeh', keywords: ['cool bokeh background', 'blue bokeh', 'cold tone bokeh', 'cool light blur'] },
      holiday_bokeh: { display: 'Holiday Bokeh', slug: 'holiday-bokeh', keywords: ['holiday bokeh background', 'christmas bokeh lights', 'festive blur', 'holiday lights background'] },
      nature_bokeh: { display: 'Nature Bokeh', slug: 'nature-bokeh', keywords: ['nature bokeh background', 'green bokeh', 'outdoor bokeh', 'nature blur background'] },
      seasonal_bokeh: { display: 'Seasonal Bokeh', slug: 'seasonal-bokeh', keywords: ['seasonal bokeh', 'spring bokeh background', 'autumn bokeh', 'seasonal blur'] },
      warm_light_bokeh: { display: 'Warm Light Bokeh', slug: 'warm-light-bokeh', keywords: ['warm bokeh background', 'golden bokeh lights', 'warm light blur', 'orange bokeh'] },
    },
  },
  food_flatlay: {
    display: 'Food & Drink Flatlay',
    slug: 'food-flatlay',
    clusters: {
      baking: { display: 'Baking', slug: 'baking', keywords: ['baking flatlay', 'baked goods overhead', 'pastry photography', 'baking ingredients flatlay'] },
      breakfast_overhead: { display: 'Breakfast Overhead', slug: 'breakfast-overhead', keywords: ['breakfast flatlay', 'breakfast overhead photo', 'morning food photography', 'eggs and toast overhead'] },
      coffee_flatlay: { display: 'Coffee Flatlay', slug: 'coffee-flatlay', keywords: ['coffee flatlay', 'coffee overhead photo', 'coffee and book', 'morning coffee photography'] },
      dark_moody_food: { display: 'Dark Moody Food', slug: 'dark-moody-food', keywords: ['dark moody food photography', 'dark food flatlay', 'moody food background', 'dark aesthetic food'] },
      drinks_cocktails: { display: 'Drinks & Cocktails', slug: 'drinks-cocktails', keywords: ['cocktail flatlay', 'drinks overhead photo', 'cocktail photography', 'beverage flatlay'] },
      healthy_food: { display: 'Healthy Food', slug: 'healthy-food', keywords: ['healthy food flatlay', 'salad overhead', 'health food photography', 'clean eating flatlay'] },
      tea_reading: { display: 'Tea & Reading', slug: 'tea-reading', keywords: ['tea flatlay', 'tea and book', 'cozy reading photo', 'tea cup overhead'] },
    },
  },
  minimalist_workspace: {
    display: 'Minimalist Workspace',
    slug: 'minimalist-workspace',
    clusters: {
      coffee_and_work: { display: 'Coffee & Work', slug: 'coffee-and-work', keywords: ['coffee and notebook', 'coffee on desk', 'morning work setup', 'work and coffee flatlay'] },
      dark_mode_workspace: { display: 'Dark Mode Workspace', slug: 'dark-mode-workspace', keywords: ['dark desk setup', 'black and white workspace', 'moody desk setup', 'dark office flatlay'] },
      desk_flatlay: { display: 'Desk Flatlay', slug: 'desk-flatlay', keywords: ['desk flatlay overhead', 'office flatlay', 'workspace flatlay', 'desk overhead photo'] },
      laptop_setup: { display: 'Laptop Setup', slug: 'laptop-setup', keywords: ['laptop on desk', 'minimal laptop setup', 'laptop and coffee', 'clean laptop desk'] },
      plant_and_work: { display: 'Plant & Work', slug: 'plant-and-work', keywords: ['succulent on desk', 'plant and laptop', 'green plant workspace', 'plant desk setup'] },
      remote_work: { display: 'Remote Work', slug: 'remote-work', keywords: ['home office setup', 'work from home desk', 'remote work setup', 'work from home flatlay'] },
      stationery: { display: 'Stationery', slug: 'stationery', keywords: ['pen and notebook flatlay', 'stationery flatlay', 'planner and coffee', 'stationery overhead'] },
    },
  },
  modern_interior: {
    display: 'Modern Interior',
    slug: 'modern-interior',
    clusters: {
      bathroom: { display: 'Bathroom', slug: 'bathroom', keywords: ['modern bathroom', 'bathroom interior photo', 'minimalist bathroom', 'clean bathroom design'] },
      bedroom: { display: 'Bedroom', slug: 'bedroom', keywords: ['modern bedroom', 'Scandinavian bedroom', 'minimalist bedroom', 'cozy bedroom interior'] },
      dining_room: { display: 'Dining Room', slug: 'dining-room', keywords: ['modern dining room', 'dining table photo', 'minimalist dining room', 'dining room interior'] },
      home_office: { display: 'Home Office', slug: 'home-office', keywords: ['home office interior', 'modern home office', 'work from home room', 'office room photo'] },
      interior_details: { display: 'Interior Details', slug: 'interior-details', keywords: ['interior detail photo', 'home decor close up', 'decorative details interior', 'home styling photo'] },
      kitchen: { display: 'Kitchen', slug: 'kitchen', keywords: ['modern kitchen', 'kitchen interior photo', 'white kitchen design', 'minimalist kitchen'] },
      living_room: { display: 'Living Room', slug: 'living-room', keywords: ['modern living room', 'Scandinavian living room', 'minimalist living room', 'cozy living room interior'] },
    },
  },
  nature_macro: {
    display: 'Nature Macro',
    slug: 'nature-macro',
    clusters: {
      bark_wood_grain: { display: 'Bark & Wood Grain', slug: 'bark-wood-grain', keywords: ['tree bark texture close up', 'wood grain macro', 'rough bark pattern', 'bark close up'] },
      flower_macro: { display: 'Flower Macro', slug: 'flower-macro', keywords: ['flower petal macro', 'pollen close up', 'flower close up photo', 'macro flower photography'] },
      frost_ice: { display: 'Frost & Ice', slug: 'frost-ice', keywords: ['frost pattern macro', 'ice crystal close up', 'frozen texture photo', 'frost photography'] },
      moss_lichen: { display: 'Moss & Lichen', slug: 'moss-lichen', keywords: ['moss texture close up', 'green moss macro', 'lichen on rock', 'moss photography'] },
      sand_earth: { display: 'Sand & Earth', slug: 'sand-earth', keywords: ['sand texture close up', 'soil macro photo', 'earth texture photography', 'sand pattern macro'] },
      spider_web_insect: { display: 'Spider Web & Insects', slug: 'spider-web-insect', keywords: ['spider web dew drops', 'spider web macro', 'dew drops on web', 'insect macro photo'] },
      water_drops: { display: 'Water Drops', slug: 'water-drops', keywords: ['water drops on leaf', 'dew drops macro', 'rain drops close up', 'water drop photography'] },
    },
  },
  sci_tech_abstract: {
    display: 'Science & Tech Abstract',
    slug: 'sci-tech-abstract',
    clusters: {
      ai_neural: { display: 'AI & Neural Networks', slug: 'ai-neural', keywords: ['AI neural network background', 'artificial intelligence abstract', 'neural network visualization', 'AI technology background'] },
      circuit_tech: { display: 'Circuit Tech', slug: 'circuit-tech', keywords: ['circuit board background', 'tech circuit abstract', 'PCB close up', 'electronic circuit background'] },
      cybersecurity: { display: 'Cybersecurity', slug: 'cybersecurity', keywords: ['cybersecurity background', 'digital security abstract', 'hacker background', 'cyber abstract photo'] },
      data_network: { display: 'Data Network', slug: 'data-network', keywords: ['data network background', 'network connection abstract', 'big data visualization', 'data flow background'] },
      dna_biology: { display: 'DNA & Biology', slug: 'dna-biology', keywords: ['DNA helix background', 'biology abstract', 'double helix photo', 'science DNA background'] },
      quantum_physics: { display: 'Quantum Physics', slug: 'quantum-physics', keywords: ['quantum physics abstract', 'physics background', 'particle physics visualization', 'quantum background'] },
      space_cosmos: { display: 'Space & Cosmos', slug: 'space-cosmos', keywords: ['space background', 'cosmos abstract photo', 'galaxy background', 'universe background image'] },
    },
  },
};

function parseFilename(filename) {
  const name = basename(filename, extname(filename));
  const parts = name.split('-');
  const index = parts[0];
  const style = parts[parts.length - 1];
  return { index, style };
}

async function main() {
  const images = [];

  const nicheEntries = await readdir(SRC, { withFileTypes: true });
  for (const nicheDir of nicheEntries.filter(d => d.isDirectory())) {
    const nicheName = nicheDir.name;
    const nicheMeta = NICHE_META[nicheName];
    if (!nicheMeta) {
      console.warn(`  skipping unknown niche: ${nicheName}`);
      continue;
    }

    const clusterEntries = await readdir(join(SRC, nicheName), { withFileTypes: true });
    for (const clusterDir of clusterEntries.filter(d => d.isDirectory())) {
      const clusterName = clusterDir.name;
      const clusterMeta = nicheMeta.clusters[clusterName];
      if (!clusterMeta) {
        console.warn(`  skipping unknown cluster: ${nicheName}/${clusterName}`);
        continue;
      }

      const destDir = join(DEST_IMAGES, nicheName, clusterName);
      await mkdir(destDir, { recursive: true });

      const files = (await readdir(join(SRC, nicheName, clusterName)))
        .filter(f => f.endsWith('.webp'))
        .sort();

      for (const file of files) {
        const { index, style } = parseFilename(file);
        const styleLabel = STYLE_LABELS[style] || style.charAt(0).toUpperCase() + style.slice(1);

        await cp(
          join(SRC, nicheName, clusterName, file),
          join(destDir, file),
        );

        const imagePath = `/images/${nicheName}/${clusterName}/${file}`;
        const slug = `${index}-${style}`;

        const title = `${styleLabel} ${clusterMeta.display} - Free Stock Photo`;
        const description = `Download this free ${styleLabel.toLowerCase()} ${clusterMeta.display.toLowerCase()} stock photo in high-quality WebP format. AI-generated, free to use for web design, social media, and creative projects.`;
        const altText = `${styleLabel} ${clusterMeta.display.toLowerCase()} - ${nicheMeta.display.toLowerCase()} free stock photo`;
        const tags = [
          ...clusterMeta.keywords.slice(0, 3),
          'free stock photo',
          'download free',
          'AI generated',
          style,
        ];

        images.push({
          index,
          slug,
          niche: nicheName,
          nicheSlug: nicheMeta.slug,
          nicheDisplay: nicheMeta.display,
          cluster: clusterName,
          clusterSlug: clusterMeta.slug,
          clusterDisplay: clusterMeta.display,
          style,
          styleLabel,
          title,
          description,
          altText,
          tags,
          imagePath,
          publishDate: '2026-04-26',
        });
      }
    }
  }

  images.sort((a, b) => a.index.localeCompare(b.index));

  await mkdir(join(SITE, 'src', 'data'), { recursive: true });
  await writeFile(DEST_DATA, JSON.stringify(images, null, 2) + '\n');

  console.log(`✓ Copied ${images.length} images to ${DEST_IMAGES}`);
  console.log(`✓ Wrote ${DEST_DATA}`);
}

main().catch(e => { console.error(e); process.exit(1); });
