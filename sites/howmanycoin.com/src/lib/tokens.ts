/**
 * Token registry (plan §8).
 *
 * Single source of truth for every symbol, name, CoinGecko ID,
 * supply type and DEX route used by the static pages and the
 * rate-fetcher worker.
 *
 * Add a new token here → write its MDX page → run `pnpm
 * build` and everything just works.
 */

export type SupplyType = 'fixed' | 'capped' | 'emission' | 'burning' | 'flex';

export interface TokenMeta {
  /** lowercase symbol, e.g. 'btc' */
  symbol: string;
  /** full name, e.g. 'Bitcoin' */
  name: string;
  /** CoinGecko API ID (case-sensitive) */
  coingeckoId: string;
  /** total supply figure (for supply pages) */
  supplyTotal?: string;
  /** circulating supply figure */
  supplyCirculating?: string;
  /** max supply — only for capped / fixed */
  supplyMax?: string;
  /** how the supply changes over time */
  supplyType: SupplyType;
  /** EVM chain slug (for 1inch deep-link). null for Solana / non-EVM. */
  dexChain?: string;
  /** DEX token list key for Jupiter (Solana only). null for EVM. */
  jupiterKey?: string;
}

/**
 * Core launch set: 17 tokens across the 25 pair converters
 * and 10 supply pages.
 */
export const TOKENS: Record<string, TokenMeta> = {
  btc: {
    symbol: 'btc',
    name: 'Bitcoin',
    coingeckoId: 'bitcoin',
    supplyTotal: '21,000,000',
    supplyCirculating: '19,800,000',
    supplyMax: '21,000,000',
    supplyType: 'fixed',
  },
  eth: {
    symbol: 'eth',
    name: 'Ethereum',
    coingeckoId: 'ethereum',
    supplyTotal: '120,230,000',
    supplyCirculating: '120,230,000',
    supplyType: 'emission',
    dexChain: 'ethereum',
  },
  sol: {
    symbol: 'sol',
    name: 'Solana',
    coingeckoId: 'solana',
    supplyTotal: '477,000,000',
    supplyCirculating: '472,000,000',
    supplyType: 'emission',
    jupiterKey: 'Solana',
  },
  usdc: {
    symbol: 'usdc',
    name: 'USD Coin',
    coingeckoId: 'usd-coin',
    supplyTotal: '42,000,000,000',
    supplyCirculating: '42,000,000,000',
    supplyType: 'flex',
    dexChain: 'ethereum',
  },
  usdt: {
    symbol: 'usdt',
    name: 'Tether',
    coingeckoId: 'tether',
    supplyTotal: '124,000,000,000',
    supplyCirculating: '124,000,000,000',
    supplyType: 'flex',
    dexChain: 'ethereum',
  },
  dai: {
    symbol: 'dai',
    name: 'Dai',
    coingeckoId: 'dai',
    supplyTotal: '5,300,000,000',
    supplyCirculating: '5,300,000,000',
    supplyType: 'flex',
    dexChain: 'ethereum',
  },
  bnb: {
    symbol: 'bnb',
    name: 'BNB',
    coingeckoId: 'binancecoin',
    supplyTotal: '153,856,150',
    supplyCirculating: '153,856,150',
    supplyMax: '200,000,000',
    supplyType: 'capped',
    dexChain: 'bsc',
  },
  matic: {
    symbol: 'matic',
    name: 'Polygon',
    coingeckoId: 'matic-network',
    supplyTotal: '10,000,000,000',
    supplyCirculating: '9,284,669,962',
    supplyMax: '10,000,000,000',
    supplyType: 'capped',
    dexChain: 'polygon',
  },
  avax: {
    symbol: 'avax',
    name: 'Avalanche',
    coingeckoId: 'avalanche-2',
    supplyTotal: '430,271,500',
    supplyCirculating: '397,051,300',
    supplyMax: '720,000,000',
    supplyType: 'capped',
    dexChain: 'avalanche',
  },
  doge: {
    symbol: 'doge',
    name: 'Dogecoin',
    coingeckoId: 'dogecoin',
    supplyTotal: '147,000,000,000',
    supplyCirculating: '147,000,000,000',
    supplyType: 'emission',
  },
  shib: {
    symbol: 'shib',
    name: 'Shiba Inu',
    coingeckoId: 'shiba-inu',
    supplyTotal: '999,982,287,232,215',
    supplyCirculating: '589,299,370,189,573',
    supplyMax: '999,982,287,232,215',
    supplyType: 'fixed',
  },
  pepe: {
    symbol: 'pepe',
    name: 'Pepe',
    coingeckoId: 'pepe',
    supplyTotal: '420,690,000,000,000',
    supplyCirculating: '420,690,000,000,000',
    supplyMax: '420,690,000,000,000',
    supplyType: 'fixed',
  },
  arb: {
    symbol: 'arb',
    name: 'Arbitrum',
    coingeckoId: 'arbitrum',
    supplyTotal: '10,000,000,000',
    supplyCirculating: '3,038,307,723',
    supplyMax: '10,000,000,000',
    supplyType: 'capped',
    dexChain: 'arbitrum',
  },
  op: {
    symbol: 'op',
    name: 'Optimism',
    coingeckoId: 'optimism',
    supplyTotal: '4,294,967,296',
    supplyCirculating: '1,631,935,485',
    supplyMax: '4,294,967,296',
    supplyType: 'capped',
    dexChain: 'optimism',
  },
  xrp: {
    symbol: 'xrp',
    name: 'XRP',
    coingeckoId: 'ripple',
    supplyTotal: '100,000,000,000',
    supplyCirculating: '56,962,671,351',
    supplyMax: '100,000,000,000',
    supplyType: 'fixed',
  },
  ada: {
    symbol: 'ada',
    name: 'Cardano',
    coingeckoId: 'cardano',
    supplyTotal: '45,000,000,000',
    supplyCirculating: '36,144,594,406',
    supplyMax: '45,000,000,000',
    supplyType: 'capped',
  },
  ton: {
    symbol: 'ton',
    name: 'Toncoin',
    coingeckoId: 'the-open-network',
    supplyTotal: '5,000,000,000',
    supplyCirculating: '3,136,933,432',
    supplyMax: '5,000,000,000',
    supplyType: 'capped',
  },
};

/**
 * Deduped, comma-separated CoinGecko IDs for batch API requests.
 *
 * We de-duplicate because many pair pages share the same base/quote
 * tokens and the rate-fetcher worker sends one batched request.
 */
export const COINGECKO_IDS = Object.values(TOKENS)
  .map((t) => t.coingeckoId)
  .filter(Boolean)
  .join(',');

/**
 * Safe lookup — returns undefined for unknown symbols so pages
 * degrade gracefully instead of throwing.
 */
export function getToken(symbol: string): TokenMeta | undefined {
  return TOKENS[symbol.toLowerCase()];
}
