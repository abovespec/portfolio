import { useState, useMemo } from 'preact/hooks';

function calcRetirement(
  currentAge: number,
  retirementAge: number,
  currentSavings: number,
  monthlyContrib: number,
  annualReturn: number,
  monthlyIncomeNeeded: number,
) {
  if (retirementAge <= currentAge || currentAge <= 0) return null;
  const yearsToRetirement = retirementAge - currentAge;
  const r = annualReturn / 100 / 12;
  const n = yearsToRetirement * 12;

  const fvLump = currentSavings * Math.pow(1 + r, n);
  const fvAnnuity = r > 0
    ? monthlyContrib * ((Math.pow(1 + r, n) - 1) / r)
    : monthlyContrib * n;
  const balanceAtRetirement = fvLump + fvAnnuity;

  let drawdownMonths = 0;
  if (monthlyIncomeNeeded > 0) {
    let balance = balanceAtRetirement;
    while (balance > 0 && drawdownMonths < 600) {
      balance = balance * (1 + r) - monthlyIncomeNeeded;
      drawdownMonths++;
    }
  }

  const totalContributed = currentSavings + monthlyContrib * n;
  const growthEarned = balanceAtRetirement - totalContributed;

  return {
    balanceAtRetirement,
    totalContributed,
    growthEarned,
    drawdownYears: drawdownMonths > 0 ? drawdownMonths / 12 : null,
    drawdownForever: monthlyIncomeNeeded <= 0 || drawdownMonths >= 600,
    yearsToRetirement,
  };
}

function fmtUsd(n: number) {
  if (n >= 1_000_000) return '$' + (n / 1_000_000).toFixed(2) + 'M';
  if (n >= 1_000) return '$' + (n / 1_000).toFixed(0) + 'K';
  return '$' + n.toFixed(0);
}

function fmtUsdFull(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function RetirementCalculator() {
  const [currentAge, setCurrentAge]         = useState('35');
  const [retirementAge, setRetirementAge]   = useState('65');
  const [currentSavings, setCurrentSavings] = useState('50000');
  const [monthlyContrib, setMonthlyContrib] = useState('1000');
  const [annualReturn, setAnnualReturn]     = useState('7');
  const [monthlyIncome, setMonthlyIncome]   = useState('5000');
  const [inflationRate, setInflationRate]   = useState('3');
  const [socialSecurity, setSocialSecurity] = useState('0');
  const [showSS, setShowSS]                 = useState(false);
  const [showTrajectory, setShowTrajectory] = useState(false);

  const incomeGoal = parseFloat(monthlyIncome) || 0;
  const ssMonthly  = parseFloat(socialSecurity) || 0;
  const monthlyGap = Math.max(0, incomeGoal - ssMonthly);

  const result = useMemo(
    () => calcRetirement(
      parseFloat(currentAge) || 0,
      parseFloat(retirementAge) || 0,
      parseFloat(currentSavings) || 0,
      parseFloat(monthlyContrib) || 0,
      parseFloat(annualReturn) || 0,
      monthlyGap,
    ),
    [currentAge, retirementAge, currentSavings, monthlyContrib, annualReturn, monthlyGap],
  );

  const isOnTrack = result
    ? (result.drawdownForever || (result.drawdownYears !== null && result.drawdownYears >= 25))
    : null;

  const withdrawalMonthly = result ? result.balanceAtRetirement * 0.04 / 12 : 0;
  const withdrawalMeetsGoal = withdrawalMonthly >= monthlyGap;

  const inflationAdjusted = useMemo(() => {
    if (!result) return 0;
    const inf = parseFloat(inflationRate) || 0;
    return incomeGoal * Math.pow(1 + inf / 100, result.yearsToRetirement);
  }, [result, inflationRate, incomeGoal]);

  const trajectoryRows = useMemo(() => {
    const currAge = parseFloat(currentAge) || 0;
    const retAge  = parseFloat(retirementAge) || 65;
    const currentBal = parseFloat(currentSavings) || 0;
    const annual = (parseFloat(monthlyContrib) || 0) * 12;
    const r = (parseFloat(annualReturn) || 7) / 100;
    if (!currAge || !retAge || retAge <= currAge) return [];
    const rows: { age: number; balance: number }[] = [];
    let bal = currentBal;
    for (let a = currAge; a <= retAge; a += 1) {
      rows.push({ age: a, balance: bal });
      bal = bal * (1 + r) + annual;
    }
    return rows;
  }, [currentAge, retirementAge, currentSavings, monthlyContrib, annualReturn]);

  const trajectoryPoints = useMemo(() => {
    if (!showTrajectory || trajectoryRows.length < 2) return '';
    const maxBal = Math.max(...trajectoryRows.map((r) => r.balance));
    if (maxBal <= 0) return '';
    const W = 400, H = 120, PAD = 12;
    return trajectoryRows.map((r, i) => {
      const x = PAD + (i / (trajectoryRows.length - 1)) * (W - PAD * 2);
      const y = (H - PAD) - (r.balance / maxBal) * (H - PAD * 2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
  }, [showTrajectory, trajectoryRows]);

  return (
    <div class="space-y-4">
      <div class="grid grid-cols-2 gap-3">
        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">Current Age</label>
          <input
            type="number" min="18" max="80" placeholder="35"
            value={currentAge}
            onInput={(e) => setCurrentAge((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Current age"
          />
        </div>
        <div>
          <label class="mb-1 block text-sm font-medium text-slate-700">Retirement Age</label>
          <input
            type="number" min="40" max="90" placeholder="65"
            value={retirementAge}
            onInput={(e) => setRetirementAge((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Target retirement age"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Current Savings</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="50000"
            value={currentSavings}
            onInput={(e) => setCurrentSavings((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Current retirement savings in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Monthly Contribution</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="1000"
            value={monthlyContrib}
            onInput={(e) => setMonthlyContrib((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Monthly retirement contribution in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Expected Annual Return</label>
        <div class="relative">
          <input
            type="number" min="0" max="30" step="0.1" placeholder="7"
            value={annualReturn}
            onInput={(e) => setAnnualReturn((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Expected annual return as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Monthly Income Needed in Retirement</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="5000"
            value={monthlyIncome}
            onInput={(e) => setMonthlyIncome((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Monthly income needed in retirement"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Inflation Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="20" step="0.1" placeholder="3"
            value={inflationRate}
            onInput={(e) => setInflationRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Expected annual inflation rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <button
          type="button"
          class="flex w-full items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:border-brand/50 hover:text-brand"
          onClick={() => setShowSS((v) => !v)}
          aria-expanded={showSS}
        >
          <span>Social Security income {showSS ? '' : '(optional)'}</span>
          <span class="text-slate-400">{showSS ? '▲' : '▼'}</span>
        </button>
        {showSS && (
          <div class="mt-2 rounded-xl border border-slate-200 bg-slate-50 p-3">
            <label class="mb-1 block text-xs font-medium text-slate-600">Expected Social Security ($/month)</label>
            <div class="relative">
              <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
              <input
                type="number" min="0" placeholder="0"
                value={socialSecurity}
                onInput={(e) => setSocialSecurity((e.target as HTMLInputElement).value)}
                class={`${inputCls} pl-6`}
                aria-label="Expected Social Security monthly benefit"
              />
            </div>
            {ssMonthly > 0 && (
              <p class="mt-1 text-[11px] text-slate-500">
                Retirement income gap after SS: {fmtUsdFull(monthlyGap)}/mo
              </p>
            )}
          </div>
        )}
      </div>

      {result && (
        <div
          role="status"
          aria-live="polite"
          class={`space-y-3 rounded-xl border p-4 ${
            isOnTrack ? 'border-green-200 bg-green-50' : 'border-amber-200 bg-amber-50'
          }`}
        >
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Balance at Retirement</span>
            <span class={`text-2xl font-bold tabular-nums ${isOnTrack ? 'text-green-700' : 'text-amber-700'}`}>
              {fmtUsd(result.balanceAtRetirement)}
            </span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Contributed</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalContributed)}</div>
            </div>
            <div>
              <div class="text-slate-500">Investment Growth</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.growthEarned)}</div>
            </div>
          </div>

          <div class={`rounded-lg px-3 py-2 text-sm ${withdrawalMeetsGoal ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'}`}>
            <span class="font-medium">4% Rule:</span> {fmtUsdFull(withdrawalMonthly)}/mo sustainable income
            {ssMonthly > 0 && ` + ${fmtUsdFull(ssMonthly)}/mo SS`}
            {withdrawalMeetsGoal
              ? ' — meets your income goal'
              : ' — below your income goal'}
          </div>

          {result.yearsToRetirement > 0 && incomeGoal > 0 && (
            <div class="rounded-lg bg-slate-100 px-3 py-2 text-sm text-slate-700">
              In {result.yearsToRetirement} years, {fmtUsdFull(incomeGoal)}/mo today = <span class="font-semibold">{fmtUsdFull(inflationAdjusted)}/mo needed</span> (at {inflationRate}% inflation)
            </div>
          )}

          {result.drawdownYears !== null && !result.drawdownForever && (
            <div class={`rounded-lg px-3 py-2 text-sm ${isOnTrack ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'}`}>
              {isOnTrack
                ? `✓ Covers ~${result.drawdownYears.toFixed(0)} years of retirement income`
                : `⚠ Covers only ~${result.drawdownYears.toFixed(0)} years — consider increasing contributions`
              }
            </div>
          )}
          {result.drawdownForever && (
            <div class="rounded-lg bg-green-100 px-3 py-2 text-sm text-green-800">
              ✓ Projected to last 50+ years at this withdrawal rate
            </div>
          )}
          {(() => {
            const contribPct = (result.totalContributed / result.balanceAtRetirement) * 100;
            return (
              <div>
                <div class="mb-1 flex justify-between text-[11px] text-slate-500">
                  <span>Contributions {contribPct.toFixed(0)}%</span>
                  <span>Growth {(100 - contribPct).toFixed(0)}%</span>
                </div>
                <div class="flex h-2.5 overflow-hidden rounded-full">
                  <div class="bg-brand" style={{ width: `${contribPct}%` }} />
                  <div class="bg-green-400" style={{ width: `${100 - contribPct}%` }} />
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {result && (
        <div>
          <button
            type="button"
            class="flex w-full items-center justify-between rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:border-brand/50 hover:text-brand"
            onClick={() => setShowTrajectory((v) => !v)}
            aria-expanded={showTrajectory}
          >
            <span>{showTrajectory ? 'Hide' : 'Show'} balance trajectory</span>
            <span class="text-slate-400">{showTrajectory ? '▲' : '▼'}</span>
          </button>

          {showTrajectory && trajectoryPoints && (
            <div class="mt-2 rounded-xl border border-slate-200 bg-slate-50 p-3">
              <p class="text-xs font-medium text-slate-500 mb-2">Balance Trajectory</p>
              <svg viewBox="0 0 400 120" class="w-full h-24" aria-hidden="true">
                <polyline points={trajectoryPoints} fill="none" stroke="#6366f1" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <div class="flex justify-between text-xs text-slate-400 mt-1">
                <span>Age {trajectoryRows[0]?.age}</span>
                <span>Age {trajectoryRows[trajectoryRows.length - 1]?.age}</span>
              </div>
            </div>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Assumes constant rate of return. Consult a certified financial planner.
      </p>
    </div>
  );
}
