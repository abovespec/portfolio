import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentIncreaseCalculator() {
  const [start, setStart] = useState('100');
  const [pct, setPct]     = useState('25');
  const result = useMemo(() => {
    const s = parseFloat(start) || 0;
    const p = parseFloat(pct) || 0;
    const increase = s * (p / 100);
    return { increase, final: s + increase };
  }, [start, pct]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Starting Value</label>
        <input type="number" step="any" value={start}
          onInput={(e) => setStart((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Starting value" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Increase By</label>
        <div class="relative">
          <input type="number" min="0" step="0.1" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Increase percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-green-200 bg-green-50 p-4">
        <div class="flex justify-between text-sm"><span class="text-slate-600">Increase Amount</span><span class="font-semibold text-green-700 tabular-nums">+{result.increase.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">New Value</span><span class="text-2xl font-bold tabular-nums text-brand">{result.final.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>

        {/* P2: Step-by-step explanation */}
        <div class="mt-3 rounded-lg bg-slate-50 border border-slate-200 p-3 text-sm">
          <p class="font-medium text-slate-700 mb-1">How it's calculated:</p>
          <p class="text-slate-600 font-mono text-xs">
            Increase = {start} &#215; {pct}/100 = {result.increase.toLocaleString('en-US', { maximumFractionDigits: 4 })}; New = {start} + {result.increase.toLocaleString('en-US', { maximumFractionDigits: 4 })} = {result.final.toLocaleString('en-US', { maximumFractionDigits: 4 })}
          </p>
        </div>
      </div>
      <p class="text-xs text-slate-500">Formula: New = Original &#215; (1 + Increase% &#247; 100)</p>
    </div>
  );
}
