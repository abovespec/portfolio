import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentDifferenceCalculator() {
  const [a, setA] = useState('80');
  const [b, setB] = useState('100');
  const result = useMemo(() => {
    const va = parseFloat(a) || 0;
    const vb = parseFloat(b) || 0;
    const avg = (Math.abs(va) + Math.abs(vb)) / 2;
    if (!avg) return null;
    return { diff: (Math.abs(va - vb) / avg) * 100, absDiff: Math.abs(va - vb) };
  }, [a, b]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Value A</label>
        <input type="number" step="any" value={a}
          onInput={(e) => setA((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Value A" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Value B</label>
        <input type="number" step="any" value={b}
          onInput={(e) => setB((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Value B" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class="space-y-2 rounded-xl border border-brand/30 bg-yellow-50 p-4">
          <div class="flex justify-between text-sm"><span class="text-slate-600">Percent Difference</span><span class="text-2xl font-bold tabular-nums text-brand">{result.diff.toFixed(2)}%</span></div>
          <div class="flex justify-between text-sm text-slate-500"><span>Absolute Difference</span><span class="tabular-nums">{result.absDiff.toLocaleString('en-US', { maximumFractionDigits: 4 })}</span></div>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: |A − B| / ((|A| + |B|) / 2) × 100</p>
    </div>
  );
}
