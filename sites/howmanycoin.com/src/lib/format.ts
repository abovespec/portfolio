/**
 * Numeric formatters. All outputs are human-readable strings suitable for UI and schema.org values.
 * Internal arithmetic should NEVER use these — use raw numbers.
 */

export function formatRate(v: number): string {
  if (!Number.isFinite(v) || v === 0) return '0';
  const abs = Math.abs(v);
  if (abs < 0.01) {
    // scientific-ish with 3 sig figs, rendered as decimal
    const str = v.toPrecision(3);
    return Number(str).toString();
  }
  if (abs < 1) return v.toPrecision(6).replace(/0+$/, '').replace(/\.$/, '');
  if (abs < 1000) return v.toFixed(5).replace(/0+$/, '').replace(/\.$/, '');
  return v.toLocaleString('en-US', { maximumFractionDigits: 2 });
}

export function formatPct(v: number): string {
  const pct = v * 100;
  const sign = pct > 0 ? '+' : pct < 0 ? '' : '';
  return `${sign}${pct.toFixed(2)}%`;
}

export function formatSupply(v: number | 'uncapped' | string): string {
  if (v === 'uncapped' || v === 'Uncapped') return 'Uncapped';
  const n = typeof v === 'string' ? Number(v) : v;
  if (!Number.isFinite(n)) return String(v);
  return n.toLocaleString('en-US', { maximumFractionDigits: 0 });
}

export function formatUsd(v: number): string {
  if (!Number.isFinite(v)) return '$0';
  if (Math.abs(v) < 1) return `$${v.toFixed(3)}`;
  return `$${v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}
