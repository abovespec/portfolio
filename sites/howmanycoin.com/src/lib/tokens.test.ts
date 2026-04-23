import { describe, it, expect } from 'vitest';
import { TOKENS, getToken, COINGECKO_IDS } from './tokens';

describe('token registry', () => {
  it('covers every token referenced by pair + supply pages', () => {
    const required = ['btc', 'eth', 'sol', 'usdc', 'usdt', 'dai', 'bnb', 'matic', 'avax', 'doge', 'shib', 'pepe', 'arb', 'op', 'xrp', 'ada', 'ton'];
    for (const sym of required) expect(TOKENS[sym], `missing ${sym}`).toBeDefined();
  });
  it('lookup returns undefined for unknown sym', () => {
    expect(getToken('xxx')).toBeUndefined();
  });
  it('COINGECKO_IDS is a deduped comma list', () => {
    const arr = COINGECKO_IDS.split(',');
    expect(new Set(arr).size).toBe(arr.length);
  });
});
