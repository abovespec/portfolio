import { useState, useMemo } from 'preact/hooks';

const FREQ_OPTIONS = [
  { label: 'Annually (1×)', value: 1 },
  { label: 'Semi-annually (2×)', value: 2 },
  { label: 'Quarterly (4×)', value: 4 },
  { label: 'Monthly (12×)', value: 12 },
  { label: 'Daily (365×)', value: 365 },
];

function calcCI(principal: number, rate: number, years: number, freq: number) {
  if (principal <= 0 || rate < 0 || years <= 0 || freq <= 0) return null;
  const r = rate / 100;
  const A = principal * Math.pow(1 + r / freq, freq * years);
  const interest = A - principal;
  return { finalAmount: A, interest, principalPct: (principal / A) * 100 };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function CompoundInterestCalculator() {
  const [principal, setPrincipal] = useState('10000');
  const [rate, setRate]           = useState('7');
  const [years, setYears]         = useState('10');
  const [freq, setFreq]           = useState(12);

  const result = useMemo(
    () => calcCI(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0, freq),
    [principal, rate, years, freq],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Principal</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="10000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Principal amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="7"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual interest rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Time Period</label>
        <div class="relative">
          <input
            type="number" min="1" max="50" placeholder="10"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Investment period in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Compounding Frequency</label>
        <select
          class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
          value={freq}
          onChange={(e) => setFreq(parseInt((e.target as HTMLSelectElement).value, 10))}
          aria-label="Compounding frequency"
        >
          {FREQ_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Final Amount</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.finalAmount)}</span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Principal</div>
              <div class="font-semibold text-slate-900">{fmtUsd(parseFloat(principal))}</div>
            </div>
            <div>
              <div class="text-slate-500">Interest Earned</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.interest)}</div>
            </div>
          </div>
          {/* Principal vs growth bar */}
          <div>
            <div class="mb-1 flex justify-between text-[11px] text-slate-500">
              <span>Principal {result.principalPct.toFixed(0)}%</span>
              <span>Growth {(100 - result.principalPct).toFixed(0)}%</span>
            </div>
            <div class="flex h-2.5 overflow-hidden rounded-full">
              <div class="bg-brand" style={{ width: `${result.principalPct}%` }} />
              <div class="bg-green-400" style={{ width: `${100 - result.principalPct}%` }} />
            </div>
          </div>
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
