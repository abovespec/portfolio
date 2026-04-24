const COINGECKO_IDS = [
  'bitcoin','ethereum','solana','usd-coin','tether','dai','binancecoin','matic-network',
  'avalanche-2','dogecoin','shiba-inu','pepe','arbitrum','optimism','ripple','cardano','the-open-network',
].join(',');

// All currencies we fetch — includes fiat for cross-rate support
const COINGECKO_CURRENCIES = 'usd,eur,gbp,jpy';

// Fallback rates (approximate, used when CoinGecko is unavailable)
const FALLBACK_RATES: Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }> = {
  bitcoin: { usd: 77682, usd_24h_change: 0.12, last_updated_at: Math.floor(Date.now() / 1000) },
  ethereum: { usd: 3328, usd_24h_change: -1.11, last_updated_at: Math.floor(Date.now() / 1000) },
  'usd-coin': { usd: 1, usd_24h_change: 0, last_updated_at: Math.floor(Date.now() / 1000) },
  tether: { usd: 1, usd_24h_change: 0, last_updated_at: Math.floor(Date.now() / 1000) },
  solana: { usd: 168, usd_24h_change: 4.8, last_updated_at: Math.floor(Date.now() / 1000) },
  dai: { usd: 1, usd_24h_change: 0, last_updated_at: Math.floor(Date.now() / 1000) },
  binancecoin: { usd: 600, usd_24h_change: 1.1, last_updated_at: Math.floor(Date.now() / 1000) },
  'matic-network': { usd: 0.55, usd_24h_change: -2.0, last_updated_at: Math.floor(Date.now() / 1000) },
  'avalanche-2': { usd: 38, usd_24h_change: 3.4, last_updated_at: Math.floor(Date.now() / 1000) },
  dogecoin: { usd: 0.175, usd_24h_change: 8.0, last_updated_at: Math.floor(Date.now() / 1000) },
  'shiba-inu': { usd: 0.000024, usd_24h_change: -1.2, last_updated_at: Math.floor(Date.now() / 1000) },
  pepe: { usd: 0.0000123, usd_24h_change: 15.0, last_updated_at: Math.floor(Date.now() / 1000) },
  arbitrum: { usd: 1.15, usd_24h_change: 0.8, last_updated_at: Math.floor(Date.now() / 1000) },
  optimism: { usd: 2.5, usd_24h_change: -0.3, last_updated_at: Math.floor(Date.now() / 1000) },
  ripple: { usd: 0.52, usd_24h_change: 1.5, last_updated_at: Math.floor(Date.now() / 1000) },
  cardano: { usd: 0.72, usd_24h_change: -1.8, last_updated_at: Math.floor(Date.now() / 1000) },
  'the-open-network': { usd: 6.8, usd_24h_change: 4.1, last_updated_at: Math.floor(Date.now() / 1000) },
};

export async function fetchCoingecko(): Promise<Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>> {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${COINGECKO_IDS}&vs_currencies=${COINGECKO_CURRENCIES}&include_24hr_change=true&include_last_updated_at=true`;
  const res = await fetch(url, {
    cf: { cacheEverything: false },
    headers: { 'User-Agent': 'howmanycoin/1.0 (+https://howmanycoin.com)' },
  });
  if (!res.ok) {
    throw new Error(`coingecko ${res.status}`);
  }
  return (await res.json()) as any;
}

export function getFallbackRates(): Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }> {
  return { ...FALLBACK_RATES };
}
