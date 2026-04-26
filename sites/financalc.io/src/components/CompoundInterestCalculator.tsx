import { useState, useMemo } from 'preact/hooks';

const FREQ_OPTIONS = [
  { label: 'Annually (1×)', value: 1 },
  { label: 'Semi-annually (2×)', value: 2 },
  { label: 'Quarterly (4×)', value: 4 },
  { label: 'Monthly (12×)', value: 12 },
  { label: 'Daily (365×)', value: 365 },
];

const GROWTH_YEARS = [1, 2, 3, 5, 10, 15, 20];

function calcCI(principal: number, rate: number, years: number, freq: number, monthlyContrib: number) {
  if (principal <= 0 || rate < 0 || years <= 0 || freq <= 0) return null;
  const compounded = principal * Math.pow(1 + rate / 100 / freq, freq * years);
  const monthly_r = rate / 100 / 12;
  const totalMonths = years * 12;
  const fvContrib = monthly_r > 0
    ? monthlyContrib * ((Math.pow(1 + monthly_r, totalMonths) - 1) / monthly_r)
    : monthlyContrib * totalMonths;
  const finalAmount = compounded + fvContrib;
  const totalInvested = principal + monthlyContrib * totalMonths;
  const interest = finalAmount - totalInvested;
  const principalPct = (totalInvested / finalAmount) * 100;
  return { finalAmount, interest, principalPct, totalInvested, monthly_r, totalMonths };
}

function calcBalanceAtYear(
  principal: number,
  rate: number,
  freq: number,
  monthlyContrib: number,
  monthly_r: number,
  yr: number,
) {
  const compounded = principal * Math.pow(1 + rate / 100 / freq, freq * yr);
  const months = yr * 12;
  const fvContrib = monthly_r > 0
    ? monthlyContrib * ((Math.pow(1 + monthly_r, months) - 1) / monthly_r)
    : monthlyContrib * months;
  return compounded + fvContrib;
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function CompoundInterestCalculator() {
  const [principal, setPrincipal]       = useState('10000');
  const [rate, setRate]                 = useState('7');
  const [years, setYears]               = useState('10');
  const [freq, setFreq]                 = useState(12);
  const [monthlyContrib, setMonthlyContrib] = useState('100');
  const [showGrowth, setShowGrowth]     = useState(false);
  const [showChart, setShowChart]       = useState(false);

  const result = useMemo(
    () => calcCI(
      parseFloat(principal) || 0,
      parseFloat(rate) || 0,
      parseFloat(years) || 0,
      freq,
      parseFloat(monthlyContrib) || 0,
    ),
    [principal, rate, years, freq, monthlyContrib],
  );

  const growthRows = useMemo(() => {
    if (!result || (!showGrowth && !showChart)) return [];
    const p = parseFloat(principal) || 0;
    const r = parseFloat(rate) || 0;
    const totalYears = parseFloat(years) || 0;
    const mc = parseFloat(monthlyContrib) || 0;
    return GROWTH_YEARS
      .filter((y) => y <= totalYears)
      .map((y) => {
        const balance = calcBalanceAtYear(p, r, freq, mc, result.monthly_r, y);
        const invested = p + mc * y * 12;
        return { year: y, balance, interestEarned: balance - invested };
      });
  }, [result, showGrowth, showChart, principal, rate, years, freq, monthlyContrib]);

  const chartPoints = useMemo(() => {
    if (!showChart || growthRows.length < 2) return '';
    const getVal = (r: any) => r.balance ?? 0;
    const maxBal = Math.max(...growthRows.map(getVal));
    if (maxBal <= 0) return '';
    const W = 400, H = 120, PAD = 12;
    return growthRows.map((r, i) => {
      const x = PAD + (i / (growthRows.length - 1)) * (W - PAD * 2);
      const y = (H - PAD) - (getVal(r) / maxBal) * (H - PAD * 2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }, [showChart, growthRows]);

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
        <label class="mb-1 block text-sm font-medium text-slate-700">Monthly Contribution</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="100"
            value={monthlyContrib}
            onInput={(e) => setMonthlyContrib((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Monthly contribution in dollars"
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
              <div class="text-slate-500">Total Invested</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalInvested)}</div>
            </div>
            <div>
              <div class="text-slate-500">Interest Earned</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.interest)}</div>
            </div>
          </div>
          <div>
            <div class="mb-1 flex justify-between text-[11px] text-slate-500">
              <span>Invested {result.principalPct.toFixed(0)}%</span>
              <span>Growth {(100 - result.principalPct).toFixed(0)}%</span>
            </div>
            <div class="flex h-2.5 overflow-hidden rounded-full">
              <div class="bg-brand" style={{ width: `${result.principalPct}%` }} />
              <div class="bg-green-400" style={{ width: `${100 - result.principalPct}%` }} />
            </div>
          </div>
        </div>
      )}

      {result && (
        <div class="space-y-2">
          <div class="flex gap-2">
            <button
              type="button"
              class="flex flex-1 items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:border-brand/50 hover:text-brand"
              onClick={() => setShowGrowth((v) => !v)}
              aria-expanded={showGrowth}
            >
              <span>{showGrowth ? 'Hide' : 'Show'} growth table</span>
              <span class="text-slate-400">{showGrowth ? '▲' : '▼'}</span>
            </button>
            <button
              type="button"
              class="flex flex-1 items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:border-brand/50 hover:text-brand"
              onClick={() => setShowChart((v) => !v)}
              aria-expanded={showChart}
            >
              <span>{showChart ? 'Hide' : 'Show'} Chart</span>
              <span class="text-slate-400">{showChart ? '▲' : '▼'}</span>
            </button>
          </div>

          {showChart && chartPoints && (
            <div class="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3">
              <p class="text-xs font-medium text-slate-500 mb-2">Balance Over Time</p>
              <svg viewBox="0 0 400 120" class="w-full h-24" aria-hidden="true">
                <polyline points={chartPoints} fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="flex justify-between text-xs text-slate-400 mt-1">
                <span>Year 1</span>
                <span>Year {growthRows[growthRows.length - 1]?.year}</span>
              </div>
            </div>
          )}

          {showGrowth && growthRows.length > 0 && (
            <div class="overflow-x-auto rounded-xl border border-slate-200">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-slate-200 bg-slate-50">
                    <th class="px-3 py-2 text-left font-medium text-slate-600">Year</th>
                    <th class="px-3 py-2 text-right font-medium text-slate-600">Balance</th>
                    <th class="px-3 py-2 text-right font-medium text-slate-600">Interest Earned</th>
                  </tr>
                </thead>
                <tbody>
                  {growthRows.map((row, i) => (
                    <tr key={row.year} class={i % 2 === 0 ? 'bg-white' : 'bg-slate-50'}>
                      <td class="px-3 py-2 tabular-nums text-slate-700">{row.year}</td>
                      <td class="px-3 py-2 text-right tabular-nums font-medium text-brand">{fmtUsd(row.balance)}</td>
                      <td class="px-3 py-2 text-right tabular-nums text-green-700">{fmtUsd(row.interestEarned)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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
