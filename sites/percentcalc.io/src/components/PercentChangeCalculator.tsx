import { useState, useMemo } from 'preact/hooks';
const inputCls = 'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
export default function PercentChangeCalculator() {
  const [from, setFrom] = useState('80');
  const [to, setTo]     = useState('100');
  const result = useMemo(() => {
    const f = parseFloat(from) || 0;
    const t = parseFloat(to);
    if (!f) return null;
    const change = ((t - f) / Math.abs(f)) * 100;
    return { change, isIncrease: change >= 0 };
  }, [from, to]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Original Value</label>
        <input type="number" step="any" value={from}
          onInput={(e) => setFrom((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="Original value" />
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">New Value</label>
        <input type="number" step="any" value={to}
          onInput={(e) => setTo((e.target as HTMLInputElement).value)}
          class={inputCls} aria-label="New value" />
      </div>
      {result && (
        <div role="status" aria-live="polite" class={`space-y-2 rounded-xl border p-4 ${result.isIncrease ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Percent Change</span>
            <span class={`text-2xl font-bold tabular-nums ${result.isIncrease ? 'text-green-700' : 'text-red-600'}`}>
              {result.isIncrease ? '+' : ''}{result.change.toFixed(2)}%
            </span>
          </div>
          <p class="text-xs text-slate-500">
            {result.isIncrease ? '↑ Increase' : '↓ Decrease'} of {Math.abs(result.change).toFixed(2)}%
          </p>
        </div>
      )}
      <p class="text-xs text-slate-500">Formula: ((New − Original) / |Original|) × 100</p>
    </div>
  );
}
