import type { Env, RateResponse } from './types';
import { fetchCoingecko, getFallbackRates } from './coingecko';
import { ctasForCountry } from './cex';

const TTL_SECONDS = 60;
const CACHE_KEY_BASE = 'https://howmanycoin.com/__cache__/rate';

// Extracted pure logic for testability
export async function buildRatePayload(
  country: string
): Promise<RateResponse> {
  let rates: Record<
    string,
    { usd: number; usd_24h_change: number; last_updated_at: number }
  >;
  try {
    rates = await fetchCoingecko();
  } catch {
    // Fallback to stale rates when CoinGecko is unavailable
    rates = getFallbackRates();
  }

  return {
    generatedAt: new Date().toISOString(),
    rates,
    geo: {
      country,
      isUS: country === 'US',
      isRestricted: ['IR', 'KP', 'SY', 'CU'].includes(country),
    },
    cexCTAs: ctasForCountry(country),
    ttl: TTL_SECONDS,
  };
}

export async function handleRequest(
  req: Request,
  _env?: Env,
  _ctx?: ExecutionContext
): Promise<Response> {
  const url = new URL(req.url);
  if (url.pathname !== '/api/rate') {
    return new Response('not found', { status: 404 });
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    return new Response('method not allowed', { status: 405 });
  }

  const country = (req.headers.get('CF-IPCountry') || 'US').toUpperCase();

  try {
    const payload = await buildRatePayload(country);
    const json = JSON.stringify(payload);
    return new Response(json, {
      status: 200,
      headers: {
        'content-type': 'application/json; charset=utf-8',
        'cache-control': `public, max-age=${TTL_SECONDS}`,
        'access-control-allow-origin': '*',
      },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: 'upstream unavailable', detail: String(err) }),
      {
        status: 503,
        headers: { 'content-type': 'application/json; charset=utf-8' },
      }
    );
  }
}

// Default export for CF Workers runtime
export default {
  async fetch(
    req: Request,
    env: Env,
    ctx: ExecutionContext
  ): Promise<Response> {
    return handleRequest(req, env, ctx);
  },
};
