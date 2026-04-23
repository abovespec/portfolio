export interface RateResponse {
  /** ISO-8601 generation timestamp for this cached payload. */
  generatedAt: string;
  /** key = CoinGecko id, value = { usd, usd_24h_change, last_updated_at } */
  rates: Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }>;
  geo: {
    country: string;
    isUS: boolean;
    isRestricted: boolean;
  };
  cexCTAs: CexCTA[];
  /** TTL in seconds (for client display only — auth cache lives in the Worker). */
  ttl: number;
}

export interface CexCTA {
  name: string;
  url: string;
  priority: number;
}

export interface Env {
  ONEINCH_REFERRER: string;
  JUPITER_PLATFORM_FEE_BPS: string;
  JUPITER_FEE_ACCOUNT: string;
}
