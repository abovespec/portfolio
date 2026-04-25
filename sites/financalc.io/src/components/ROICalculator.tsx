import { useState, useMemo } from 'preact/hooks';

function calcROI(initial: number, finalVal: number, years: number | null) {
  if (initial <= 0 || finalVal < 0) return null;
  const roi = ((finalVal - initial) / initial) * 100;
  const netProfit = finalVal - initial;
  const annualized = (years && years > 0)
    ? (Math.pow(finalVal / initial, 1 / years) - 1) * 100
    : null;
  return { roi, netProfit, annualized };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function fmtPct(n: number) {
  return (n >= 0 ? '+' : '') + n.toFixed(2) + '%';
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function ROICalculator() {
  const [initial, setInitial]   = useState('5000');
  const [finalVal, setFinalVal] = useState('7500');
  const [years, setYears]       = useState('');

  const result = useMemo(
    () => calcROI(
      parseFloat(initial) || 0,
      parseFloat(finalVal) || 0,
      years ? parseFloat(years) : null,
    ),
    [initial, finalVal, years],
  );

  const isPositive = result ? result.roi >= 0 : true;

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Initial Investment</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0.01" step="any" placeholder="5000"
            value={initial}
            onInput={(e) => setInitial((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Initial investment in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Final Value</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" step="any" placeholder="7500"
            value={finalVal}
            onInput={(e) => setFinalVal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Final value in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Time Period <span class="font-normal text-slate-400">(optional, for annualized return)</span>
        </label>
        <div class="relative">
          <input
            type="number" min="0.1" step="any" placeholder="e.g. 3"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Investment period in years (optional)"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      {result && (
        <div
          role="status"
          aria-live="polite"
          class={`space-y-3 rounded-xl border p-4 ${isPositive ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}
        >
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">ROI</span>
            <span class={`text-3xl font-bold tabular-nums ${isPositive ? 'text-green-700' : 'text-red-600'}`}>
              {fmtPct(result.roi)}
            </span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class={`grid gap-2 text-sm ${result.annualized !== null ? 'grid-cols-3' : 'grid-cols-2'}`}>
            <div>
              <div class="text-slate-500">Net Profit</div>
              <div class={`font-semibold ${isPositive ? 'text-green-700' : 'text-red-600'}`}>
                {fmtUsd(result.netProfit)}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Initial</div>
              <div class="font-semibold text-slate-900">{fmtUsd(parseFloat(initial))}</div>
            </div>
            {result.annualized !== null && (
              <div>
                <div class="text-slate-500">Annualized</div>
                <div class="font-semibold text-slate-900">{fmtPct(result.annualized)}</div>
              </div>
            )}
          </div>
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
