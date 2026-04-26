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

function calcAmortWithExtra(principal: number, annualRate: number, years: number, extraMonthly: number) {
  if (principal <= 0 || annualRate <= 0 || years <= 0) return null;
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
  const totalPayment = monthly + extraMonthly;

  let balance = principal;
  let totalInterestPaid = 0;
  let month = 0;
  while (balance > 0 && month < n) {
    month++;
    const interest = balance * r;
    totalInterestPaid += interest;
    const princ = Math.min(totalPayment - interest, balance);
    balance = Math.max(0, balance - princ);
  }

  return { months: month, totalInterest: totalInterestPaid };
}

// Build yearly balance snapshots for chart (standard + extra payment)
function buildChartPoints(
  principal: number, annualRate: number, years: number, extraMonthly: number
): { yr: number; std: number; extra: number }[] {
  if (principal <= 0 || annualRate <= 0 || years <= 0) return [];
  const r = annualRate / 100 / 12;
  const n = years * 12;
  const monthly = (principal * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);

  // Simulate month by month for both scenarios
  const stdBalances: number[] = [principal];
  const extraBalances: number[] = [principal];
  let stdBal = principal;
  let extraBal = principal;

  for (let i = 1; i <= n; i++) {
    if (stdBal > 0) {
      const interest = stdBal * r;
      stdBal = Math.max(0, stdBal - (monthly - interest));
    }
    if (extraBal > 0) {
      const interest = extraBal * r;
      extraBal = Math.max(0, extraBal - (monthly + extraMonthly - interest));
    }
    stdBalances.push(stdBal);
    extraBalances.push(extraBal);
  }

  // Sample 12 data points (year 0 through year N)
  const points: { yr: number; std: number; extra: number }[] = [];
  for (let p = 0; p < 12; p++) {
    const monthIdx = Math.round((p / 11) * n);
    const clampedIdx = Math.min(monthIdx, n);
    points.push({
      yr: Math.round(clampedIdx / 12 * 10) / 10,
      std: stdBalances[clampedIdx] ?? 0,
      extra: extraBalances[clampedIdx] ?? 0,
    });
  }
  return points;
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

// P3: CSV download function
function downloadAmortCsv(rows: {month:number;payment:number;principal:number;interest:number;balance:number}[]) {
  const header = 'Month,Payment,Principal,Interest,Balance\n';
  const body = rows.map(r =>
    `${r.month},${r.payment.toFixed(2)},${r.principal.toFixed(2)},${r.interest.toFixed(2)},${r.balance.toFixed(2)}`
  ).join('\n');
  const blob = new Blob([header + body], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'amortization-schedule.csv';
  a.click();
  URL.revokeObjectURL(url);
}

export default function AmortizationCalculator() {
  const [principal, setPrincipal] = useState('300000');
  const [rate, setRate]           = useState('6.5');
  const [years, setYears]         = useState('30');
  const [extra, setExtra]         = useState('0');
  const [showTable, setShowTable] = useState(false);

  const p = parseFloat(principal) || 0;
  const r = parseFloat(rate) || 0;
  const y = parseFloat(years) || 0;
  const ex = parseFloat(extra) || 0;

  const result = useMemo(() => calcAmort(p, r, y), [p, r, y]);
  const extraResult = useMemo(() => ex > 0 ? calcAmortWithExtra(p, r, y, ex) : null, [p, r, y, ex]);
  const chartPoints = useMemo(() => buildChartPoints(p, r, y, ex > 0 ? ex : 0), [p, r, y, ex]);

  const SVG_H = 120;
  const SVG_PAD = { top: 8, bottom: 20, left: 8, right: 8 };
  const chartWidth = 100; // percent-based via viewBox
  const chartInnerW = chartWidth - SVG_PAD.left - SVG_PAD.right;
  const chartInnerH = SVG_H - SVG_PAD.top - SVG_PAD.bottom;

  function toSvgPts(balances: number[], maxBal: number) {
    return chartPoints.map((pt, i) => {
      const x = SVG_PAD.left + (i / (chartPoints.length - 1)) * chartInnerW;
      const y = SVG_PAD.top + (1 - balances[i] / maxBal) * chartInnerH;
      return `${x.toFixed(2)},${y.toFixed(2)}`;
    }).join(' ');
  }

  const maxBal = chartPoints.length > 0 ? chartPoints[0].std : 1;
  const stdPts = chartPoints.map(pt => pt.std);
  const extraPts = chartPoints.map(pt => pt.extra);

  // Full amort rows for CSV (all months)
  const fullRows = useMemo(() => {
    if (p <= 0 || r <= 0 || y <= 0) return [];
    const rate = r / 100 / 12;
    const n = y * 12;
    const monthly = (p * rate * Math.pow(1 + rate, n)) / (Math.pow(1 + rate, n) - 1);
    let balance = p;
    const rows: AmortRow[] = [];
    for (let i = 1; i <= n; i++) {
      const interest = balance * rate;
      const princ = monthly - interest;
      balance = Math.max(0, balance - princ);
      rows.push({ month: i, payment: monthly, principal: princ, interest, balance });
    }
    return rows;
  }, [p, r, y]);

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

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Extra Monthly Payment <span class="text-slate-400 font-normal">(optional)</span>
        </label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" step="50" placeholder="0"
            value={extra}
            onInput={(e) => setExtra((e.target as HTMLInputElement).value)}
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

          {/* Extra payment results */}
          {extraResult && ex > 0 && (
            <div class="rounded-lg border border-green-200 bg-green-50 p-3 text-sm space-y-1">
              <div class="font-semibold text-green-800 text-xs uppercase tracking-wide mb-2">Extra Payment Impact</div>
              <div class="flex justify-between">
                <span class="text-slate-600">Paid off in</span>
                <span class="font-semibold text-slate-900">
                  {Math.floor(extraResult.months / 12)}y {extraResult.months % 12}mo
                  <span class="text-slate-400 font-normal ml-1">vs {y}y 0mo</span>
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-600">Months saved</span>
                <span class="font-semibold text-green-700">{y * 12 - extraResult.months} months</span>
              </div>
              <div class="flex justify-between">
                <span class="text-slate-600">Interest saved</span>
                <span class="font-semibold text-green-700">{fmtUsd(result.totalInterest - extraResult.totalInterest)}</span>
              </div>
            </div>
          )}

          {/* Balance-over-time SVG chart */}
          {chartPoints.length > 1 && (
            <div class="space-y-1">
              <div class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Balance Over Time</div>
              {ex > 0 && (
                <div class="flex gap-4 text-[11px] text-slate-500">
                  <span class="flex items-center gap-1">
                    <span class="inline-block w-6 h-0.5 bg-indigo-500"></span>Standard
                  </span>
                  <span class="flex items-center gap-1">
                    <span class="inline-block w-6 h-0.5 bg-green-500"></span>With extra payment
                  </span>
                </div>
              )}
              <div class="rounded-lg bg-white border border-slate-200 overflow-hidden">
                <svg
                  viewBox={`0 0 ${chartWidth} ${SVG_H}`}
                  preserveAspectRatio="none"
                  class="w-full"
                  style={{ height: '120px' }}
                  aria-label="Loan balance over time chart"
                >
                  {/* Horizontal grid line at midpoint */}
                  <line
                    x1={SVG_PAD.left} y1={SVG_PAD.top + chartInnerH / 2}
                    x2={SVG_PAD.left + chartInnerW} y2={SVG_PAD.top + chartInnerH / 2}
                    stroke="#e2e8f0" stroke-width="0.5"
                  />
                  {/* Standard payoff line */}
                  <polyline
                    points={toSvgPts(stdPts, maxBal)}
                    fill="none"
                    stroke="#6366f1"
                    stroke-width="1.2"
                    stroke-linejoin="round"
                    stroke-linecap="round"
                  />
                  {/* Extra payment line */}
                  {ex > 0 && (
                    <polyline
                      points={toSvgPts(extraPts, maxBal)}
                      fill="none"
                      stroke="#22c55e"
                      stroke-width="1.2"
                      stroke-linejoin="round"
                      stroke-linecap="round"
                      stroke-dasharray="2,1"
                    />
                  )}
                  {/* Y-axis labels */}
                  <text x={SVG_PAD.left} y={SVG_PAD.top - 1} font-size="3.5" fill="#94a3b8">${Math.round(maxBal / 1000)}k</text>
                  <text x={SVG_PAD.left} y={SVG_PAD.top + chartInnerH + 6} font-size="3.5" fill="#94a3b8">Yr 0</text>
                  <text x={SVG_PAD.left + chartInnerW - 8} y={SVG_PAD.top + chartInnerH + 6} font-size="3.5" fill="#94a3b8">Yr {y}</text>
                </svg>
              </div>
            </div>
          )}

          <div class="flex items-center justify-between">
            <button
              type="button"
              onClick={() => setShowTable((v) => !v)}
              class="mt-1 text-xs font-medium text-brand underline underline-offset-2 hover:opacity-80"
            >
              {showTable ? 'Hide' : 'Show'} amortization schedule
            </button>

            {/* P3: Download CSV button */}
            {fullRows.length > 0 && (
              <button
                type="button"
                onClick={() => downloadAmortCsv(fullRows)}
                class="text-sm px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium"
              >
                Download CSV
              </button>
            )}
          </div>

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
