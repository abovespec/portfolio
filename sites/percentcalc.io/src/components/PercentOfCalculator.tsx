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

          {/* P2: Visual proportion bar */}
          <div class="mt-3">
            <div class="h-3 w-full rounded-full overflow-hidden bg-slate-200">
              <div
                class="h-full bg-brand rounded-full transition-all duration-300"
                style={{ width: `${Math.min(Math.max(parseFloat(pct)||0, 0), 100)}%` }}
              />
            </div>
            <p class="text-xs text-slate-500 mt-1">{pct}% of the total</p>
          </div>

          {/* P2: Step-by-step explanation */}
          <div class="mt-3 rounded-lg bg-slate-50 border border-slate-200 p-3 text-sm">
            <p class="font-medium text-slate-700 mb-1">How it's calculated:</p>
            <p class="text-slate-600 font-mono text-xs">
              {pct}% of {total} = {pct}/100 &#215; {total} = {result.value.toFixed(4)}
            </p>
          </div>

          {/* P3: Reverse calculation prompt */}
          {parseFloat(pct) > 0 && parseFloat(total) > 0 && (
            <p class="mt-2 text-xs text-slate-500">
              Flip it: {result.value.toFixed(2)} is {pct}% of {total} &#8594;&#160;
              {result.value.toFixed(2)} is what % of {total}? &#8594; {pct}%
            </p>
          )}
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: Result = (Percentage ÷ 100) × Number</p>
    </div>
  );
}
