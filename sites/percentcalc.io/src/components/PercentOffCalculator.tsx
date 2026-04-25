import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
function fmtN(n: number) { return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
export default function PercentOffCalculator() {
  const [price, setPrice] = useState('120');
  const [off, setOff]     = useState('20');
  const result = useMemo(() => {
    const p = parseFloat(price) || 0;
    const o = parseFloat(off) || 0;
    if (!p) return null;
    const savings = p * (o / 100);
    return { savings, finalPrice: p - savings };
  }, [price, off]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Original Price</label>
        <input type="number" min="0" step="0.01" value={price}
          onInput={(e) => setPrice((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Original price" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Discount</label>
        <div class="relative">
          <input type="number" min="0" max="100" step="0.1" value={off}
            onInput={(e) => setOff((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Discount percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">% off</span>
        </div>
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm"><span class="text-slate-600">You Save</span><span class="text-xl font-bold tabular-nums text-green-700">{fmtN(result.savings)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Final Price</span><span class="text-2xl font-bold tabular-nums text-brand">{fmtN(result.finalPrice)}</span></div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: Final = Price × (1 − Discount% ÷ 100)</p>
    </div>
  );
}
