import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { handleRequest, buildRatePayload } from '../src/rate';
import * as coingecko from '../src/coingecko';
import type { RateResponse, CexCTA } from '../src/types';

const mockRates: Record<string, { usd: number; usd_24h_change: number; last_updated_at: number }> = {
  bitcoin: { usd: 67500, usd_24h_change: 2.34, last_updated_at: 1713800000 },
  ethereum: { usd: 3500, usd_24h_change: -0.56, last_updated_at: 1713800000 },
  'usd-coin': { usd: 1, usd_24h_change: 0, last_updated_at: 1713800000 },
  tether: { usd: 1, usd_24h_change: 0, last_updated_at: 1713800000 },
  solana: { usd: 175, usd_24h_change: 5.2, last_updated_at: 1713800000 },
  dai: { usd: 1, usd_24h_change: 0, last_updated_at: 1713800000 },
  binancecoin: { usd: 600, usd_24h_change: 1.1, last_updated_at: 1713800000 },
  'matic-network': { usd: 0.55, usd_24h_change: -2.0, last_updated_at: 1713800000 },
  'avalanche-2': { usd: 38, usd_24h_change: 3.4, last_updated_at: 1713800000 },
  dogecoin: { usd: 0.175, usd_24h_change: 8.0, last_updated_at: 1713800000 },
  'shiba-inu': { usd: 0.000024, usd_24h_change: -1.2, last_updated_at: 1713800000 },
  pepe: { usd: 0.0000123, usd_24h_change: 15.0, last_updated_at: 1713800000 },
  arbitrum: { usd: 1.15, usd_24h_change: 0.8, last_updated_at: 1713800000 },
  optimism: { usd: 2.5, usd_24h_change: -0.3, last_updated_at: 1713800000 },
  ripple: { usd: 0.52, usd_24h_change: 1.5, last_updated_at: 1713800000 },
  cardano: { usd: 0.72, usd_24h_change: -1.8, last_updated_at: 1713800000 },
  'the-open-network': { usd: 6.8, usd_24h_change: 4.1, last_updated_at: 1713800000 },
};

function mockRequest(path: string, country?: string): Request {
  const headers = new Headers();
  if (country) headers.set('CF-IPCountry', country);
  return new Request(`https://howmanycoin.com${path}`, { headers });
}

beforeEach(() => {
  vi.spyOn(coingecko, 'fetchCoingecko').mockResolvedValue(mockRates);
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe('buildRatePayload', () => {
  it('returns correct shape with rates and geo', async () => {
    const payload = await buildRatePayload('US');
    expect(payload.rates).toBeDefined();
    expect(payload.rates.bitcoin.usd).toBe(67500);
    expect(payload.geo.country).toBe('US');
    expect(payload.geo.isUS).toBe(true);
    expect(payload.geo.isRestricted).toBe(false);
    expect(Array.isArray(payload.cexCTAs)).toBe(true);
  });

  it('marks restricted countries correctly', async () => {
    const payload = await buildRatePayload('IR');
    expect(payload.geo.isRestricted).toBe(true);
    const names = payload.cexCTAs.map((c: CexCTA) => c.name);
    expect(names).not.toContain('Binance');
    expect(names).not.toContain('MEXC');
  });

  it('throws on upstream failure', async () => {
    vi.spyOn(coingecko, 'fetchCoingecko').mockRejectedValueOnce(new Error('network error'));
    await expect(buildRatePayload('US')).rejects.toThrow('upstream unavailable');
  });
});

describe('handleRequest', () => {
  it('returns 200 with JSON and expected shape', async () => {
    const res = await handleRequest(mockRequest('/api/rate'));
    expect(res.status).toBe(200);
    const body = (await res.json()) as RateResponse;
    expect(body.rates).toBeTypeOf('object');
    expect(body.geo.country).toBe('US');
    expect(body.geo.isUS).toBe(true);
    expect(Array.isArray(body.cexCTAs)).toBe(true);
  });

  it('returns Coinbase + Kraken above-fold for US traffic', async () => {
    const res = await handleRequest(mockRequest('/api/rate', 'US'));
    const body = (await res.json()) as RateResponse;
    const aboveFold = body.cexCTAs
      .filter((c: CexCTA) => c.priority === 0)
      .map((c: CexCTA) => c.name);
    expect(aboveFold).toContain('Coinbase');
    expect(aboveFold).toContain('Kraken');
    expect(aboveFold).not.toContain('Binance');
  });

  it('returns Binance + Bybit above-fold for non-US traffic', async () => {
    const res = await handleRequest(mockRequest('/api/rate', 'DE'));
    const body = (await res.json()) as RateResponse;
    const aboveFold = body.cexCTAs
      .filter((c: CexCTA) => c.priority === 0)
      .map((c: CexCTA) => c.name);
    expect(aboveFold).toContain('Binance');
    expect(aboveFold).toContain('Bybit');
    expect(aboveFold).not.toContain('Coinbase');
  });

  it('returns correct BTC and ETH rates', async () => {
    const res = await handleRequest(mockRequest('/api/rate'));
    const body = (await res.json()) as RateResponse;
    expect(body.rates.bitcoin.usd).toBe(67500);
    expect(body.rates.ethereum.usd).toBe(3500);
  });

  it('returns 404 for non-/api/rate paths', async () => {
    const res = await handleRequest(new Request('https://howmanycoin.com/other'));
    expect(res.status).toBe(404);
  });

  it('returns 405 for non-GET/HEAD methods', async () => {
    const res = await handleRequest(
      new Request('https://howmanycoin.com/api/rate', { method: 'POST' })
    );
    expect(res.status).toBe(405);
  });

  it('returns 503 on upstream failure', async () => {
    vi.spyOn(coingecko, 'fetchCoingecko').mockRejectedValueOnce(
      new Error('network error')
    );
    const res = await handleRequest(mockRequest('/api/rate'));
    expect(res.status).toBe(503);
    const body = await res.json();
    expect(body.error).toBe('upstream unavailable');
  });
});
