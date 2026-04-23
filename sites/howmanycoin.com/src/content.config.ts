import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date().optional(),
    draft: z.boolean().default(false),
  }),
});

const tools = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    urlSlug: z.string(),
    draft: z.boolean().default(false),
  }),
});

const games = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    urlSlug: z.string(),
    draft: z.boolean().default(false),
  }),
});

const pairs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    base: z.string(),
    quote: z.string(),
    category: z.enum(['major', 'stablecoin', 'l1', 'meme', 'defi']),
    featured: z.boolean().default(false),
    seoKeywords: z.array(z.string()),
  }),
});

const supply = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    token: z.string(),
    supplyType: z.enum(['fixed', 'capped', 'emission', 'burning', 'flex']),
    totalSupply: z.string(),
    circulatingSupply: z.string(),
    maxSupply: z.string().optional(),
    burnMechanism: z.boolean().default(false),
    seoKeywords: z.array(z.string()),
  }),
});

const guides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    topic: z.enum(['market-cap', 'fully-diluted', 'circulating-vs-total', 'token-emissions', 'supply-shocks']),
    seoKeywords: z.array(z.string()),
  }),
});

export const collections = { blog, tools, games, pairs, supply, guides };
