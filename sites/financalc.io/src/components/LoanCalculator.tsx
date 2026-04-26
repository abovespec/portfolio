import { useState, useMemo } from 'preact/hooks';

const TERM_PRESETS = [1, 2, 3, 5, 7] as const;

function calcLoan(principal: number, annualRate: number, years: number) {
  if (principal <= 0 || annualRate < 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = r === 0
    ? principal / n
    : (principal * r) / (1 - Math.pow(1 + r, -n));
  const total = monthly * n;
  const interest = total - principal;
  return { monthly, total, interest, interestPct: (interest / total) * 100, r, n };
}

function calcExtraPayment(principal: number, r: number, monthlyBase: number, extra: number) {
  if (extra <= 0) return null;
  const payment = monthlyBase + extra;
  let balance = principal;
  let months = 0;
  let totalInterest = 0;
  while (balance > 0 && months < 1200) {
    const interestCharge = balance * r;
    totalInterest += interestCharge;
    balance = balance + interestCharge - payment;
    months++;
    if (balance < 0) balance = 0;
  }
  return { months, totalInterest };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function LoanCalculator() {
  const [principal, setPrincipal] = useState('20000');
  const [rate, setRate]           = useState('6.5');
  const [years, setYears]         = useState('5');
  const [extraPayment, setExtraPayment] = useState('0');

  const result = useMemo(
    () => calcLoan(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0),
    [principal, rate, years],
  );

  const extraResult = useMemo(() => {
    if (!result) return null;
    const extra = parseFloat(extraPayment) || 0;
    if (extra <= 0) return null;
    const withExtra = calcExtraPayment(
      parseFloat(principal) || 0,
      result.r,
      result.monthly,
      extra,
    );
    if (!withExtra) return null;
    const originalInterest = result.interest;
    const interestSaved = originalInterest - withExtra.totalInterest;
    const monthsSaved = result.n - withExtra.months;
    return { months: withExtra.months, monthsSaved, interestSaved };
  }, [result, extraPayment, principal]);

  const payoffDate = useMemo(() => {
    if (!result) return null;
    const d = new Date();
    d.setMonth(d.getMonth() + result.n);
    return d.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
  }, [result]);

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="20000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Loan amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Interest Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="6.5"
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
        <div class="relative">
          <input
            type="number" min="1" max="30" placeholder="5"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Loan term in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
        </div>
        <div class="mt-2 flex gap-2">
          {TERM_PRESETS.map((y) => (
            <button
              key={y}
              type="button"
              class={`flex-1 rounded-lg border py-1.5 text-xs font-medium transition-all ${
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

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Extra Monthly Payment <span class="font-normal text-slate-400">(optional)</span></label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="0"
            value={extraPayment}
            onInput={(e) => setExtraPayment((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Extra monthly payment in dollars"
          />
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
              <div class="text-slate-500">Total Paid</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.total)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Interest</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.interest)}</div>
            </div>
            {payoffDate && (
              <div class="col-span-2 border-t border-slate-200 pt-2">
                <div class="text-slate-500">Loan paid off</div>
                <div class="font-semibold text-slate-900">{payoffDate}</div>
              </div>
            )}
          </div>
          <div>
            <div class="mb-1 flex justify-between text-[11px] text-slate-500">
              <span>Principal {(100 - result.interestPct).toFixed(0)}%</span>
              <span>Interest {result.interestPct.toFixed(0)}%</span>
            </div>
            <div class="flex h-2.5 overflow-hidden rounded-full">
              <div class="bg-brand" style={{ width: `${100 - result.interestPct}%` }} />
              <div class="bg-orange-400" style={{ width: `${result.interestPct}%` }} />
            </div>
          </div>

          {extraResult && (
            <div class="space-y-2 border-t border-slate-200 pt-3">
              <p class="text-xs font-semibold uppercase tracking-wide text-slate-500">With extra payments</p>
              <div class="grid grid-cols-3 gap-2 text-sm">
                <div>
                  <div class="text-slate-500">Payoff</div>
                  <div class="font-semibold text-slate-900">
                    {extraResult.months >= 12
                      ? `${Math.floor(extraResult.months / 12)}y ${extraResult.months % 12}m`
                      : `${extraResult.months}mo`}
                  </div>
                </div>
                <div>
                  <div class="text-slate-500">Months Saved</div>
                  <div class="font-semibold text-green-700">{extraResult.monthsSaved}</div>
                </div>
                <div>
                  <div class="text-slate-500">Interest Saved</div>
                  <div class="font-semibold text-green-700">{fmtUsd(extraResult.interestSaved)}</div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
