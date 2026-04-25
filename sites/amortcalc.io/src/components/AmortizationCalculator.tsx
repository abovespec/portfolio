import { useState, useMemo } from 'preact/hooks';

interface AmortRow {
  month: number;
  payment: number;
  principal: number;
  interest: number;
  balance: number;
}

function calcAmort(principal: number, annualRate: number, years: number) {
  if (principal <= 0 || annualRate <= 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  const totalCost = monthly * n;
  const totalInterest = totalCost - principal;
  const interestPct = (totalInterest / totalCost) * 100;

  let balance = principal;
  const rows: AmortRow[] = [];
  for (let i = 1; i <= n; i++) {
    const interest = balance * r;
    const princ = monthly - interest;
    balance = Math.max(0, balance - princ);
    if (i <= 24 || i % 12 === 0 || i === n) {
      rows.push({ month: i, payment: monthly, principal: princ, interest, balance });
    }
  }

  return { monthly, totalCost, totalInterest, interestPct, rows };
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function AmortizationCalculator() {
  const [principal, setPrincipal] = useState('300000');
  const [rate, setRate]           = useState('6.5');
  const [years, setYears]         = useState('30');
  const [showTable, setShowTable] = useState(false);

  const result = useMemo(
    () => calcAmort(parseFloat(principal) || 0, parseFloat(rate) || 0, parseFloat(years) || 0),
    [principal, rate, years],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Loan Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1000" step="1000" placeholder="300000"
            value={principal}
            onInput={(e) => setPrincipal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Loan principal in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Interest Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="30" step="0.1" placeholder="6.5"
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
            type="number" min="1" max="40" step="1" placeholder="30"
            value={years}
            onInput={(e) => setYears((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Loan term in years"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">yrs</span>
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
              <div class="text-slate-500">Total Cost</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalCost)}</div>
            </div>
            <div>
              <div class="text-slate-500">Total Interest</div>
              <div class="font-semibold text-orange-600">{fmtUsd(result.totalInterest)}</div>
            </div>
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

          <button
            type="button"
            onClick={() => setShowTable((v) => !v)}
            class="mt-1 text-xs font-medium text-brand underline underline-offset-2 hover:opacity-80"
          >
            {showTable ? 'Hide' : 'Show'} amortization schedule
          </button>

          {showTable && (
            <div class="max-h-64 overflow-auto rounded-lg border border-slate-200 bg-white text-xs">
              <table class="w-full">
                <thead class="sticky top-0 bg-slate-50 text-left">
                  <tr>
                    {['Mo.', 'Principal', 'Interest', 'Balance'].map((h) => (
                      <th class="px-2 py-1.5 font-semibold text-slate-600">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100">
                  {result.rows.map((row) => (
                    <tr key={row.month} class="hover:bg-slate-50">
                      <td class="px-2 py-1 tabular-nums text-slate-500">{row.month}</td>
                      <td class="px-2 py-1 tabular-nums">{fmtUsd(row.principal)}</td>
                      <td class="px-2 py-1 tabular-nums text-orange-600">{fmtUsd(row.interest)}</td>
                      <td class="px-2 py-1 tabular-nums">{fmtUsd(row.balance)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor before borrowing.
      </p>
    </div>
  );
}
