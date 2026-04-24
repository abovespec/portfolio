import { defineCollection, z } from 'astro:content';

/**
 * Content collections.
 *
 * All schemas use Zod so TypeScript understands frontmatter shape site-wide.
 * Add fields conservatively — every new field must be populated across the
 * network or made optional.
 */

const blog = defineCollection({
  type: 'content',
  schema: ({ image }) =>
    z.object({
      title: z.string().max(120),
      description: z.string().max(200),
      publishDate: z.coerce.date(),
      updatedDate: z.coerce.date().optional(),
      author: z.string().default('Editorial Team'),
      tags: z.array(z.string()).default([]),
      image: image().optional(),
      imageAlt: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

// Props consumed by SoftwareApplication JSON-LD.
const softwareApplicationSchema = z.object({
  applicationCategory: z.string().default('UtilitiesApplication'),
  operatingSystem: z.string().default('Web'),
  price: z.string().default('0'),
  priceCurrency: z.string().default('USD'),
  ratingValue: z.number().optional(),
  ratingCount: z.number().optional(),
});

const tools = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    urlSlug: z.string(),
    schema: softwareApplicationSchema.default({}),
    relatedTags: z.array(z.string()).default([]),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
  }),
});

const videoGameSchema = z.object({
  genre: z.string().default('Casual'),
  gamePlatform: z.array(z.string()).default(['Web']),
  applicationCategory: z.string().default('GameApplication'),
  ratingValue: z.number().optional(),
  ratingCount: z.number().optional(),
});

const games = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    urlSlug: z.string(),
    schema: videoGameSchema.default({}),
    relatedTags: z.array(z.string()).default([]),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
  }),
});

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
    thumbnail: z.string(),
    preview: z.string(),
    fullSize: z.string(),
  }),
});

export const collections = { blog, tools, games, textures };
