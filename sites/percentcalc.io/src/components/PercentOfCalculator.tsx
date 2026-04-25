import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentOfCalculator() {
  const [pct, setPct]     = useState('15');
  const [total, setTotal] = useState('200');
  const result = useMemo(() => {
    const p = parseFloat(pct) || 0;
    const t = parseFloat(total) || 0;
    if (t === 0) return null;
    return { value: (p / 100) * t, remainder: t - (p / 100) * t };
  }, [pct, total]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Percentage</label>
        <div class="relative">
          <input type="number" min="0" step="0.01" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Of what number?</label>
        <input type="number" min="0" step="any" value={total}
          onInput={(e) => setTotal((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Base number" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm">
            <span class="text-slate-600">{pct}% of {total}</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{result.value.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span>
          </div>
          <div class="flex justify-between text-sm text-slate-500">
            <span>Remainder</span>
            <span class="tabular-nums">{result.remainder.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span>
          </div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: Result = (Percentage ÷ 100) × Number</p>
    </div>
  );
}
