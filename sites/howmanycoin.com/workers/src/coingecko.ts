const COINGECKO_IDS = [
  'bitcoin','ethereum','solana','usd-coin','tether','dai','binancecoin','matic-network',
  'avalanche-2','dogecoin','shiba-inu','pepe','arbitrum','optimism','ripple','cardano','the-open-network',
].join(',');

export async function fetchCoingecko(): Promise<Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>> {
  const url = `https://api.coingecko.com/api/v3/simple/price?ids=${COINGECKO_IDS}&vs_currencies=usd&include_24hr_change=true&include_last_updated_at=true`;
  const res = await fetch(url, {
    cf: { cacheEverything: false },
    headers: { 'User-Agent': 'howmanycoin/1.0 (+https://howmanycoin.com)' },
  });
  if (!res.ok) {
    throw new Error(`coingecko ${res.status}`);
  }
  return (await res.json()) as any;
}
