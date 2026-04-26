export interface ClusterMeta {
  display: string;
  slug: string;
  description: string;
  keywords: string[];
}

export interface NicheMeta {
  display: string;
  slug: string;
  description: string;
  clusters: Record<string, ClusterMeta>;
}

export const NICHES: Record<string, NicheMeta> = {
  abstract_backgrounds: {
    display: 'Abstract Backgrounds',
    slug: 'abstract-backgrounds',
    description: 'Free abstract background stock photos. High-quality AI-generated images perfect for web design, social media, and presentations.',
    clusters: {
      gradient_backgrounds: { display: 'Gradient Backgrounds', slug: 'gradient-backgrounds', description: 'Smooth color gradient backgrounds free to download.', keywords: ['gradient background', 'color gradient wallpaper', 'smooth gradient background'] },
      watercolor_textures: { display: 'Watercolor Textures', slug: 'watercolor-textures', description: 'Artistic watercolor and paint texture backgrounds.', keywords: ['watercolor background', 'paint texture background', 'artistic watercolor'] },
      minimalist_color_wash: { display: 'Minimalist Color Wash', slug: 'minimalist-color-wash', description: 'Clean, minimal single-color wash backgrounds.', keywords: ['minimalist background', 'solid color background', 'clean color texture'] },
      dark_backgrounds: { display: 'Dark Backgrounds', slug: 'dark-backgrounds', description: 'Dark and moody abstract backgrounds for dramatic designs.', keywords: ['dark abstract background', 'dark moody background', 'deep color background'] },
      pastel_backgrounds: { display: 'Pastel Backgrounds', slug: 'pastel-backgrounds', description: 'Soft pastel color backgrounds for gentle, elegant designs.', keywords: ['pastel background', 'soft pastel colors', 'light pastel texture'] },
      geometric_abstract: { display: 'Geometric Abstract', slug: 'geometric-abstract', description: 'Modern geometric shape and pattern backgrounds.', keywords: ['geometric abstract background', 'abstract shapes', 'modern geometric pattern'] },
      blurred_soft_focus: { display: 'Blurred Soft Focus', slug: 'blurred-soft-focus', description: 'Dreamy blurred and out-of-focus abstract backgrounds.', keywords: ['blurred background', 'out of focus background', 'soft abstract texture'] },
    },
  },
  bokeh_backgrounds: {
    display: 'Bokeh Backgrounds',
    slug: 'bokeh-backgrounds',
    description: 'Free bokeh background stock photos. Dreamy, atmospheric bokeh images for headers, invitations, and social media.',
    clusters: {
      abstract_color_bokeh: { display: 'Abstract Color Bokeh', slug: 'abstract-color-bokeh', description: 'Colorful abstract bokeh light backgrounds.', keywords: ['abstract bokeh background', 'colorful bokeh', 'bokeh lights'] },
      city_lights_bokeh: { display: 'City Lights Bokeh', slug: 'city-lights-bokeh', description: 'Urban city lights bokeh for nighttime aesthetics.', keywords: ['city lights bokeh', 'urban bokeh background', 'night lights blur'] },
      cool_bokeh: { display: 'Cool Bokeh', slug: 'cool-bokeh', description: 'Cool-toned blue and green bokeh backgrounds.', keywords: ['cool bokeh background', 'blue bokeh', 'cold tone bokeh'] },
      holiday_bokeh: { display: 'Holiday Bokeh', slug: 'holiday-bokeh', description: 'Festive holiday and Christmas bokeh backgrounds.', keywords: ['holiday bokeh background', 'christmas bokeh lights', 'festive blur'] },
      nature_bokeh: { display: 'Nature Bokeh', slug: 'nature-bokeh', description: 'Natural outdoor bokeh for organic, fresh designs.', keywords: ['nature bokeh background', 'green bokeh', 'outdoor bokeh'] },
      seasonal_bokeh: { display: 'Seasonal Bokeh', slug: 'seasonal-bokeh', description: 'Seasonal bokeh perfect for year-round content.', keywords: ['seasonal bokeh', 'spring bokeh background', 'autumn bokeh'] },
      warm_light_bokeh: { display: 'Warm Light Bokeh', slug: 'warm-light-bokeh', description: 'Golden warm-toned bokeh light backgrounds.', keywords: ['warm bokeh background', 'golden bokeh lights', 'warm light blur'] },
    },
  },
  food_flatlay: {
    display: 'Food & Drink Flatlay',
    slug: 'food-flatlay',
    description: 'Free food and drink flatlay stock photos. Professional overhead food photography for recipe blogs, food brands, and lifestyle content.',
    clusters: {
      baking: { display: 'Baking', slug: 'baking', description: 'Overhead baking and pastry flatlay photos.', keywords: ['baking flatlay', 'baked goods overhead', 'pastry photography'] },
      breakfast_overhead: { display: 'Breakfast Overhead', slug: 'breakfast-overhead', description: 'Morning breakfast overhead flatlay photography.', keywords: ['breakfast flatlay', 'breakfast overhead photo', 'morning food photography'] },
      coffee_flatlay: { display: 'Coffee Flatlay', slug: 'coffee-flatlay', description: 'Coffee cup and accessories flatlay photos.', keywords: ['coffee flatlay', 'coffee overhead photo', 'morning coffee photography'] },
      dark_moody_food: { display: 'Dark Moody Food', slug: 'dark-moody-food', description: 'Dark and dramatic food photography for editorial use.', keywords: ['dark moody food photography', 'dark food flatlay', 'moody food'] },
      drinks_cocktails: { display: 'Drinks & Cocktails', slug: 'drinks-cocktails', description: 'Cocktails and beverages overhead flatlay photos.', keywords: ['cocktail flatlay', 'drinks overhead photo', 'cocktail photography'] },
      healthy_food: { display: 'Healthy Food', slug: 'healthy-food', description: 'Clean eating and healthy food overhead photography.', keywords: ['healthy food flatlay', 'salad overhead', 'health food photography'] },
      tea_reading: { display: 'Tea & Reading', slug: 'tea-reading', description: 'Cozy tea and book flatlay lifestyle photos.', keywords: ['tea flatlay', 'tea and book', 'cozy reading photo'] },
    },
  },
  minimalist_workspace: {
    display: 'Minimalist Workspace',
    slug: 'minimalist-workspace',
    description: 'Free minimalist workspace stock photos. Clean desk setups and work flatlay images for blogs, presentations, and social media.',
    clusters: {
      coffee_and_work: { display: 'Coffee & Work', slug: 'coffee-and-work', description: 'Productivity flatlay with coffee and work items.', keywords: ['coffee and notebook', 'coffee on desk', 'morning work setup'] },
      dark_mode_workspace: { display: 'Dark Mode Workspace', slug: 'dark-mode-workspace', description: 'Dark aesthetic desk setups for tech content.', keywords: ['dark desk setup', 'black and white workspace', 'moody desk'] },
      desk_flatlay: { display: 'Desk Flatlay', slug: 'desk-flatlay', description: 'Overhead desk and office flatlay photography.', keywords: ['desk flatlay overhead', 'office flatlay', 'workspace flatlay'] },
      laptop_setup: { display: 'Laptop Setup', slug: 'laptop-setup', description: 'Minimal laptop on desk setup photos.', keywords: ['laptop on desk', 'minimal laptop setup', 'laptop and coffee'] },
      plant_and_work: { display: 'Plant & Work', slug: 'plant-and-work', description: 'Biophilic workspace with plants and work items.', keywords: ['succulent on desk', 'plant and laptop', 'green plant workspace'] },
      remote_work: { display: 'Remote Work', slug: 'remote-work', description: 'Home office and work-from-home setup photos.', keywords: ['home office setup', 'work from home desk', 'remote work setup'] },
      stationery: { display: 'Stationery', slug: 'stationery', description: 'Pen, notebook, and stationery flatlay photos.', keywords: ['pen and notebook flatlay', 'stationery flatlay', 'planner and coffee'] },
    },
  },
  modern_interior: {
    display: 'Modern Interior',
    slug: 'modern-interior',
    description: 'Free modern interior stock photos. Clean residential interior images for real estate, interior design, and home decor content.',
    clusters: {
      bathroom: { display: 'Bathroom', slug: 'bathroom', description: 'Modern minimalist bathroom interior photography.', keywords: ['modern bathroom', 'bathroom interior photo', 'minimalist bathroom'] },
      bedroom: { display: 'Bedroom', slug: 'bedroom', description: 'Cozy and modern bedroom interior photos.', keywords: ['modern bedroom', 'Scandinavian bedroom', 'minimalist bedroom'] },
      dining_room: { display: 'Dining Room', slug: 'dining-room', description: 'Modern dining room and table setting photos.', keywords: ['modern dining room', 'dining table photo', 'minimalist dining room'] },
      home_office: { display: 'Home Office', slug: 'home-office', description: 'Styled home office and work room interior photos.', keywords: ['home office interior', 'modern home office', 'work from home room'] },
      interior_details: { display: 'Interior Details', slug: 'interior-details', description: 'Decorative interior detail and styling close-ups.', keywords: ['interior detail photo', 'home decor close up', 'decorative details'] },
      kitchen: { display: 'Kitchen', slug: 'kitchen', description: 'Clean and modern kitchen interior photography.', keywords: ['modern kitchen', 'kitchen interior photo', 'white kitchen design'] },
      living_room: { display: 'Living Room', slug: 'living-room', description: 'Modern and Scandinavian living room interior photos.', keywords: ['modern living room', 'Scandinavian living room', 'minimalist living room'] },
    },
  },
  nature_macro: {
    display: 'Nature Macro',
    slug: 'nature-macro',
    description: 'Free nature macro stock photos. Close-up nature photography of water drops, frost, flowers, and textures for editorial and educational content.',
    clusters: {
      bark_wood_grain: { display: 'Bark & Wood Grain', slug: 'bark-wood-grain', description: 'Close-up tree bark and wood grain texture photography.', keywords: ['tree bark texture', 'wood grain macro', 'rough bark pattern'] },
      flower_macro: { display: 'Flower Macro', slug: 'flower-macro', description: 'Extreme close-up flower petal and pollen macro photography.', keywords: ['flower petal macro', 'pollen close up', 'flower close up'] },
      frost_ice: { display: 'Frost & Ice', slug: 'frost-ice', description: 'Frozen crystal and frost pattern macro photography.', keywords: ['frost pattern macro', 'ice crystal close up', 'frozen texture'] },
      moss_lichen: { display: 'Moss & Lichen', slug: 'moss-lichen', description: 'Lush moss and lichen texture close-up photography.', keywords: ['moss texture close up', 'green moss macro', 'lichen on rock'] },
      sand_earth: { display: 'Sand & Earth', slug: 'sand-earth', description: 'Sand and soil texture macro photography.', keywords: ['sand texture close up', 'soil macro photo', 'earth texture'] },
      spider_web_insect: { display: 'Spider Web & Insects', slug: 'spider-web-insect', description: 'Dew-covered spider webs and insect macro photography.', keywords: ['spider web dew drops', 'spider web macro', 'insect macro photo'] },
      water_drops: { display: 'Water Drops', slug: 'water-drops', description: 'Water drop and dew macro photography on leaves and surfaces.', keywords: ['water drops on leaf', 'dew drops macro', 'rain drops close up'] },
    },
  },
  sci_tech_abstract: {
    display: 'Science & Tech Abstract',
    slug: 'sci-tech-abstract',
    description: 'Free science and tech abstract stock photos. AI concepts, circuit boards, DNA helixes, and space imagery for tech companies and educational publishers.',
    clusters: {
      ai_neural: { display: 'AI & Neural Networks', slug: 'ai-neural', description: 'Artificial intelligence and neural network abstract visuals.', keywords: ['AI neural network background', 'artificial intelligence abstract', 'neural network visualization'] },
      circuit_tech: { display: 'Circuit Tech', slug: 'circuit-tech', description: 'Circuit board and electronic technology close-up photos.', keywords: ['circuit board background', 'tech circuit abstract', 'PCB close up'] },
      cybersecurity: { display: 'Cybersecurity', slug: 'cybersecurity', description: 'Digital security and cybersecurity abstract imagery.', keywords: ['cybersecurity background', 'digital security abstract', 'cyber abstract'] },
      data_network: { display: 'Data Network', slug: 'data-network', description: 'Data network connection and big data visualization photos.', keywords: ['data network background', 'network connection abstract', 'big data visualization'] },
      dna_biology: { display: 'DNA & Biology', slug: 'dna-biology', description: 'DNA helix and biology science abstract photography.', keywords: ['DNA helix background', 'biology abstract', 'double helix photo'] },
      quantum_physics: { display: 'Quantum Physics', slug: 'quantum-physics', description: 'Quantum physics and particle science abstract imagery.', keywords: ['quantum physics abstract', 'physics background', 'particle physics'] },
      space_cosmos: { display: 'Space & Cosmos', slug: 'space-cosmos', description: 'Space and cosmos abstract photography for tech and editorial.', keywords: ['space background', 'cosmos abstract photo', 'galaxy background'] },
    },
  },
};

export const NICHE_LIST = Object.entries(NICHES).map(([key, meta]) => ({
  key,
  ...meta,
  clusterList: Object.entries(meta.clusters).map(([cKey, cMeta]) => ({ key: cKey, ...cMeta })),
}));
