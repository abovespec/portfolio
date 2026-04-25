import { useState, useMemo } from 'preact/hooks';

function calcMortgage(homePrice: number, downPayment: number, annualRate: number, years: number) {
  const principal = homePrice - downPayment;
  if (principal <= 0 || annualRate < 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = r === 0
    ? principal / n
    : (principal * r) / (1 - Math.pow(1 + r, -n));
  const total = monthly * n;
  const interest = total - principal;
  const downPct = homePrice > 0 ? (downPayment / homePrice) * 100 : 0;
  return { monthly, total, interest, principal, downPct };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function MortgageCalculator() {
  const [homePrice, setHomePrice]   = useState('400000');
  const [downPayment, setDownPayment] = useState('80000');
  const [rate, setRate]             = useState('7.0');
  const [years, setYears]           = useState('30');

  const result = useMemo(
    () => calcMortgage(
      parseFloat(homePrice) || 0,
      parseFloat(downPayment) || 0,
      parseFloat(rate) || 0,
      parseFloat(years) || 0,
    ),
    [homePrice, downPayment, rate, years],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Home Price</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="400000"
            value={homePrice}
            onInput={(e) => setHomePrice((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Home price in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Down Payment</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="80000"
            value={downPayment}
            onInput={(e) => setDownPayment((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Down payment in dollars"
          />
        </div>
        {result && (
          <p class="mt-1 text-[11px] text-slate-400">
            {result.downPct.toFixed(1)}% of home price
          </p>
        )}
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Interest Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="30" step="0.01" placeholder="7.0"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual interest rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Term</label>
        <div class="flex gap-2">
          {([15, 20, 30] as const).map((y) => (
            <button
              key={y}
              type="button"
              class={`flex-1 rounded-lg border py-2 text-sm font-medium transition-all ${
                parseInt(years, 10) === y
                  ? 'border-brand bg-brand text-white'
                  : 'border-slate-300 text-slate-600 hover:border-brand/50'
              }`}
              onClick={() => setYears(String(y))}
              aria-pressed={parseInt(years, 10) === y}
            >
              {y} yr
            </button>
          ))}
        </div>
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Monthly Payment</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.monthly)}</span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Loan Amount</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.principal)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Interest</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.interest)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Paid</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.total)}</div>
            </div>
            <div>
              <div class="text-slate-500">Down Payment</div>
              <div class="font-semibold text-slate-900">{fmtUsd(parseFloat(downPayment) || 0)}</div>
            </div>
          </div>
          {/* Principal vs interest bar */}
          {(() => {
            const interestPct = (result.interest / result.total) * 100;
            return (
              <div>
                <div class="mb-1 flex justify-between text-[11px] text-slate-500">
                  <span>Principal {(100 - interestPct).toFixed(0)}%</span>
                  <span>Interest {interestPct.toFixed(0)}%</span>
                </div>
                <div class="flex h-2.5 overflow-hidden rounded-full">
                  <div class="bg-brand" style={{ width: `${100 - interestPct}%` }} />
                  <div class="bg-orange-400" style={{ width: `${interestPct}%` }} />
                </div>
              </div>
            );
          })()}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Estimates principal and interest only. Does not include property tax, insurance, or PMI.
      </p>
    </div>
  );
}
