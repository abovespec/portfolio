import { defineCollection, z } from 'astro:content';

/* ------------------------------------------------------------------ */
/*  PAIR CONVERTER PAGES (25)                                         */
/* ------------------------------------------------------------------ */
const pairs = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    base: z.string(),      // e.g. 'btc'
    quote: z.string(),     // e.g. 'usd'
    category: z.enum(['major', 'stablecoin', 'l1', 'meme', 'defi']),
    featured: z.boolean().default(false),
    seoKeywords: z.array(z.string()),
  }),
});

/* ------------------------------------------------------------------ */
/*  SUPPLY / TOKENOMICS PAGES (10)                                    */
/* ------------------------------------------------------------------ */
const supply = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    token: z.string(),          // maps to TOKENS.key
    supplyType: z.enum(['fixed', 'capped', 'emission', 'burning', 'flex']),
    totalSupply: z.string(),
    circulatingSupply: z.string(),
    maxSupply: z.string().optional(),
    burnMechanism: z.boolean().default(false),
    seoKeywords: z.array(z.string()),
  }),
});

/* ------------------------------------------------------------------ */
/*  EVERGREEN GUIDE PAGES (5)                                        */
/* ------------------------------------------------------------------ */
const guides = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    topic: z.enum([
      'market-cap',
      'fully-diluted',
      'circulating-vs-total',
      'token-emissions',
      'supply-shocks',
    ]),
    seoKeywords: z.array(z.string()),
  }),
});

/* ------------------------------------------------------------------ */
/*  EXPORT                                                            */
/* ------------------------------------------------------------------ */
export const collections = { pairs, supply, guides };
