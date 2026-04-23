import type { CexCTA } from './types';

const US_RESTRICTED_FOR_BINANCE = new Set(['US']);
const HEAVILY_RESTRICTED = new Set(['IR', 'KP', 'SY', 'CU']);

export function ctasForCountry(country: string): CexCTA[] {
  const isUS = country === 'US';
  const heavy = HEAVILY_RESTRICTED.has(country);
  const out: CexCTA[] = [];

  if (isUS) {
    out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 0 });
    out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 0 });
  } else if (!heavy) {
    out.push({ name: 'Binance', url: 'https://accounts.binance.com/register?ref=HOWMANYCOIN', priority: 0 });
    out.push({ name: 'Bybit',   url: 'https://www.bybit.com/invite?ref=HOWMANYCOIN', priority: 0 });
  } else {
    out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 0 });
    out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 0 });
  }

  // below-the-fold expandable set
  if (!US_RESTRICTED_FOR_BINANCE.has(country) && !heavy) {
    out.push({ name: 'Binance', url: 'https://accounts.binance.com/register?ref=HOWMANYCOIN', priority: 1 });
  }
  out.push({ name: 'Bybit',    url: 'https://www.bybit.com/invite?ref=HOWMANYCOIN', priority: 1 });
  out.push({ name: 'OKX',      url: 'https://www.okx.com/join/HOWMANYCOIN', priority: 1 });
  if (!heavy) out.push({ name: 'MEXC', url: 'https://www.mexc.com/register?inviteCode=HOWMANYCOIN', priority: 1 });
  out.push({ name: 'Coinbase', url: 'https://coinbase.com/join/howmanycoin', priority: 1 });
  out.push({ name: 'Kraken',   url: 'https://kraken.com/sign-up?ref=howmanycoin', priority: 1 });
  out.push({ name: 'KuCoin',   url: 'https://www.kucoin.com/r/rf/howmanycoin', priority: 1 });

  // dedupe by (name, priority) keeping first occurrence
  const seen = new Set<string>();
  return out.filter((c) => {
    const k = `${c.name}:${c.priority}`;
    if (seen.has(k)) return false;
    seen.add(k);
    return true;
  });
}
