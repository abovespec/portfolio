import { useState, useEffect, useCallback, useRef } from 'preact/hooks';
import { computed } from '@preact/signals';

interface RateData {
  usd: number;
  usd_24h_change: number;
  last_updated_at: number;
}

interface CoinGeckoResponse {
  [id: string]: RateData;
}

interface Props {
  base: string;
  quote: string;
}

// Crypto asset IDs in CoinGecko
const CRYPTO_CG: Record<string, string> = {
  btc: 'bitcoin',
  eth: 'ethereum',
  sol: 'solana',
  usdc: 'usd-coin',
  usdt: 'tether',
  dai: 'dai',
  bnb: 'binancecoin',
  matic: 'matic-network',
  avax: 'avalanche-2',
  doge: 'dogecoin',
  shib: 'shiba-inu',
  pepe: 'pepe',
  arb: 'arbitrum',
  op: 'optimism',
  xrp: 'ripple',
  ada: 'cardano',
  ton: 'the-open-network',
};

// Fiat currencies — used as vs_currencies, not asset IDs
const FIAT = ['usd', 'eur', 'gbp', 'jpy'];
const CRYPTO = Object.keys(CRYPTO_CG);

const BASE_TO_CG = CRYPTO_CG;
const QUOTE_TO_CG = { ...CRYPTO_CG };

function formatRate(rate: number, quote: string): string {
  const q = quote.toLowerCase();
  if (q === 'jpy') return Math.round(rate).toLocaleString() + ' JPY';
  if (q === 'usd' || q === 'eur' || q === 'gbp') {
    const sym = q === 'usd' ? '$' : q === 'eur' ? '\u20ac' : '\u00a3';
    if (rate >= 1) return sym + rate.toLocaleString(undefined, { maximumFractionDigits: 2 });
    return sym + rate.toFixed(6);
  }
  if (rate >= 1) return rate.toFixed(6);
  return rate.toFixed(8);
}

function format24hChange(change: number): string {
  const sign = change >= 0 ? '+' : '';
  return sign + change.toFixed(2) + '%';
}

function isGoodTime(change24h: number, quote: string): { label: string; positive: boolean } {
  const isFiat = ['usd', 'eur', 'gbp'].includes(quote.toLowerCase());
  if (!isFiat) return { label: 'Check trend before converting', positive: false };
  if (change24h < -3) return { label: 'Dip - good entry opportunity', positive: true };
  if (change24h > 5) return { label: 'Pump - consider taking profits', positive: false };
  return { label: 'Neutral - no strong signal', positive: false };
}

export default function PairConverter({ base, quote }: Props) {
  const [amount, setAmount] = useState('1');
  const [rate, setRate] = useState<number | null>(null);
  const [result, setResult] = useState<number | null>(null);
  const [change24h, setChange24h] = useState<number | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const goodTime = computed(() => {
    if (change24h === null) return null;
    return isGoodTime(change24h, quote);
  });

  const fetchRate = useCallback(async () => {
    try {
      // Try the Worker endpoint first (b-lazy rate service)
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 5000);

      const res = await fetch('/api/rate', { signal: controller.signal });
      clearTimeout(timeoutId);

      if (!res.ok) throw new Error('Worker returned ' + res.status);
      const data = await res.json() as { rates: CoinGeckoResponse; generatedAt: string };

      const baseCG = BASE_TO_CG[base];
      const quoteCG = QUOTE_TO_CG[quote];

      if (!baseCG) throw new Error('Unsupported base: ' + base);

      let convertedRate: number;

      if (quoteCG && CRYPTO.includes(quoteCG)) {
        // Both are crypto assets - cross-rate via USD
        if (data.rates[baseCG]?.usd && data.rates[quoteCG]?.usd) {
          convertedRate = data.rates[baseCG].usd / data.rates[quoteCG].usd;
        } else {
          throw new Error('Rate data unavailable for this pair');
        }
      } else {
        // Quote is fiat or stablecoin
        convertedRate = data.rates[baseCG]?.usd ?? 0;
      }

      setRate(convertedRate);
      setChange24h(data.rates[baseCG]?.usd_24h_change ?? null);
      setLastUpdated(new Date(data.generatedAt));
      setError(null);
    } catch {
      // Fallback: fetch directly from CoinGecko
      try {
        const baseCG = BASE_TO_CG[base];
        if (!baseCG) throw new Error('Unsupported base: ' + base);

        // Always fetch USD and compute cross-rate (CoinGecko free tier limits vs_currencies)
        const ids = baseCG;
        const res = await fetch(
          'https://api.coingecko.com/api/v3/simple/price?ids=' + ids +
          '&vs_currencies=usd&include_24hr_change=true'
        );

        if (!res.ok) throw new Error('CoinGecko returned ' + res.status);
        const data = await res.json() as CoinGeckoResponse;

        const baseRate = data[baseCG]?.usd ?? 0;

        // For fiat quotes, fetch both USD and the fiat currency
        const quoteCG = QUOTE_TO_CG[quote];
        const isCryptoQuote = quoteCG && CRYPTO.includes(quoteCG);

        let convertedRate: number;

        if (isCryptoQuote) {
          // Crypto-to-crypto: cross-rate via USD
          const res2 = await fetch(
            'https://api.coingecko.com/api/v3/simple/price?ids=' + baseCG + ',' + quoteCG +
            '&vs_currencies=usd&include_24hr_change=true'
          );
          if (!res2.ok) throw new Error('CoinGecko returned ' + res2.status);
          const data2 = await res2.json() as CoinGeckoResponse;
          const quoteRate = data2[quoteCG]?.usd ?? 1;
          convertedRate = baseRate / quoteRate;
          setChange24h(data2[baseCG]?.usd_24h_change ?? null);
        } else {
          // Fiat quote: fetch base in USD, then convert using a simple rate
          // For a proper solution, fetch the fiat pair directly
          const fiatCurrencies = 'usd,gbp,eur,jpy';
          const res2 = await fetch(
            'https://api.coingecko.com/api/v3/simple/price?ids=' + baseCG +
            '&vs_currencies=' + fiatCurrencies + '&include_24hr_change=true'
          );
          if (res2.ok) {
            const data2 = await res2.json() as CoinGeckoResponse;
            const fiatRate = data2[baseCG]?.[quote.toLowerCase()] ?? 0;
            convertedRate = fiatRate;
            setChange24h(data2[baseCG]?.usd_24h_change ?? 0);
          } else {
            // If that fails, use rough approximation
            const fiatUSDMap: Record<string, number> = {
              gbp: 1.27, eur: 1.08, jpy: 0.0067,
            };
            const fiatUsdRate = fiatUSDMap[quote.toLowerCase()] ?? 1;
            convertedRate = baseRate * fiatUsdRate;
            setChange24h(data[baseCG]?.usd_24h_change ?? 0);
          }
        }

        setRate(convertedRate);
        setLastUpdated(new Date());
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch rate');
        setRate(null);
        setChange24h(null);
        setLastUpdated(null);
      } finally {
        setLoading(false);
      }
    }
  }, [base, quote]);

  // Initial fetch
  useEffect(() => {
    setLoading(true);
    fetchRate();

    // Poll every 60 seconds
    intervalRef.current = setInterval(fetchRate, 60000);
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [fetchRate]);

  // Update result when amount or rate changes
  useEffect(() => {
    if (rate !== null) {
      const amt = parseFloat(amount) || 0;
      setResult(amt * rate);
    }
  }, [rate, amount]);

  const handleAmountChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    setAmount(target.value || '0');
  };

  const baseSymbol = base.toUpperCase();
  const quoteSymbol = quote.toUpperCase();
  const convertedResult = result !== null
    ? formatRate(result, quote)
    : null;

  return (
    <div id="pair-rate-card" class="mt-6">
      <p class="meta mb-2">
        {baseSymbol}/{quoteSymbol}
        {lastUpdated ? (
          <span class="live-time"> updated {lastUpdated.toLocaleTimeString()}</span>
        ) : (
          <span class="live-time"> loading...</span>
        )}
      </p>

      {loading && !error ? (
        <div class="mt-4 flex items-center gap-3 text-slate-500">
          <div class="h-4 w-4 animate-spin rounded-full border-2 border-accent border-t-transparent" />
          Fetching live rates...
        </div>
      ) : error ? (
        <div class="mt-4 rounded border border-red-200 bg-red-50 p-3 text-sm text-red-700">
          <p>Unable to load rate: {error}</p>
          <button
            class="mt-2 text-sm font-medium text-red-700 underline"
            onClick={() => { setLoading(true); fetchRate(); }}
          >
            Retry
          </button>
        </div>
      ) : (
        <>
          {rate !== null && (
            <div class="mt-3 rounded-lg bg-slate-50 p-3">
              <p class="text-sm text-slate-600">
                1 {baseSymbol} = {formatRate(rate, quote)} {quoteSymbol}
              </p>
              {change24h !== null && (
                <p class={"mt-1 text-sm " + (change24h >= 0 ? 'text-emerald-600' : 'text-red-600')}>
                  24h change: {format24hChange(change24h)}
                </p>
              )}
              {goodTime.value && (
                <p class={"mt-1 text-xs font-medium " + (goodTime.value.positive ? 'text-emerald-600' : 'text-slate-500')}>
                  {goodTime.value.label}
                </p>
              )}
            </div>
          )}

          <div class="grid gap-4 md:grid-cols-2">
            <div>
              <label for="amount-input" class="sr-only">Amount</label>
              <input
                id="amount-input"
                type="number"
                min="0"
                step="any"
                value={amount}
                onInput={handleAmountChange}
                class="w-full rounded border border-slate-300 bg-white px-3 py-2 text-2xl font-mono focus:border-accent focus:ring-2 focus:ring-accent/20"
              />
            </div>
            <div>
              <label class="opacity-0">Result</label>
              <p class="figure mt-2 text-2xl font-mono" id="pair-result">
                {convertedResult || '\u2014'}
              </p>
              <p class="mt-1 text-sm text-slate-500">
                {convertedResult ? convertedResult + ' ' + quoteSymbol : '\u2014'}
              </p>
            </div>
          </div>

          <div class="mt-3 flex flex-wrap gap-2">
            <button
              id="btn-1inch"
              type="button"
              class="rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:brightness-110"
              onClick={() => {
                const baseCG = BASE_TO_CG[base];
                const chain = base === 'eth' ? 'ethereum' : base;
                const quoteCG = QUOTE_TO_CG[quote] || 'usd-coin';
                const url = 'https://app.1inch.io/#/' + chain + '/1/uniswap/v2/swap/' + baseCG + '/' + quoteCG + '?amount=' + encodeURIComponent(amount);
                window.open(url, '_blank', 'noopener,noreferrer');
              }}
            >
              Swap on 1inch
            </button>
            <button
              id="btn-jupiter"
              type="button"
              class={"rounded bg-accent px-4 py-2 text-sm font-medium text-white hover:brightness-110 " + (base === 'sol' ? '' : 'hidden')}
              onClick={() => {
                const amountVal = parseFloat(amount) || 0;
                const url = 'https://jup.ag/swap/' + base + '-' + quote + '?amount=' + amountVal;
                window.open(url, '_blank', 'noopener,noreferrer');
              }}
            >
              Swap on Jupiter
            </button>
          </div>

          <p class="mt-3 text-xs text-slate-500">
            Rates refresh every 60 seconds. Swap links are affiliate links.
          </p>
        </>
      )}
    </div>
  );
}
