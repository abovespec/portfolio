import { useState, useMemo } from 'preact/hooks';

function calcSavings(goal: number, initial: number, monthly: number, annualRate: number) {
  if (goal <= 0 || monthly < 0) return null;
  const r = annualRate / 100 / 12;
  let balance = initial;
  let months = 0;
  while (balance < goal && months < 600) {
    balance = balance * (1 + r) + monthly;
    months++;
  }
  if (balance < goal) return null;
  const totalContributed = initial + monthly * months;
  const interestEarned = balance - totalContributed;
  return { months, years: months / 12, totalContributed, interestEarned, finalBalance: balance };
}

function calcMonthsToTarget(target: number, initial: number, monthly: number, annualRate: number) {
  if (target <= 0 || monthly < 0 || target > 1e9) return null;
  const r = annualRate / 100 / 12;
  let balance = initial;
  let months = 0;
  while (balance < target && months < 600) {
    balance = balance * (1 + r) + monthly;
    months++;
  }
  return balance >= target ? months : null;
}

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function SavingsGoalCalculator() {
  const [goal, setGoal]       = useState('50000');
  const [initial, setInitial] = useState('1000');
  const [monthly, setMonthly] = useState('500');
  const [rate, setRate]       = useState('4');
  const [inflationRate, setInflationRate] = useState('3');
  const [extraMonthly, setExtraMonthly]   = useState(0);

  const result = useMemo(
    () => calcSavings(
      parseFloat(goal) || 0,
      parseFloat(initial) || 0,
      parseFloat(monthly) || 0,
      parseFloat(rate) || 0,
    ),
    [goal, initial, monthly, rate],
  );

  const inflationAdjusted = useMemo(() => {
    const goalAmt = parseFloat(goal) || 0;
    const yrs = result ? result.years : 0;
    const inf = parseFloat(inflationRate) || 0;
    if (!goalAmt || !yrs) return null;
    return goalAmt * Math.pow(1 + inf / 100, yrs);
  }, [goal, result, inflationRate]);

  const extraResult = useMemo(() => {
    if (!result || extraMonthly <= 0) return null;
    const goalAmt = parseFloat(goal) || 0;
    const baseMonthly = parseFloat(monthly) || 0;
    const withExtraMonths = calcMonthsToTarget(
      goalAmt,
      parseFloat(initial) || 0,
      baseMonthly + extraMonthly,
      parseFloat(rate) || 0,
    );
    if (withExtraMonths === null) return null;
    const monthsSaved = result.months - withExtraMonths;
    return { months: withExtraMonths, monthsSaved };
  }, [result, extraMonthly, goal, initial, monthly, rate]);

  const goalAmt = parseFloat(goal) || 0;
  const milestones = useMemo(() => {
    if (!result || goalAmt <= 10000) return [];
    const targets = [10000, 25000, 50000].filter((t) => t < goalAmt);
    return targets.map((t) => {
      const m = calcMonthsToTarget(
        t,
        parseFloat(initial) || 0,
        parseFloat(monthly) || 0,
        parseFloat(rate) || 0,
      );
      return { target: t, months: m };
    }).filter((x) => x.months !== null) as { target: number; months: number }[];
  }, [result, goalAmt, initial, monthly, rate]);

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Savings Goal</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="1" placeholder="50000"
            value={goal}
            onInput={(e) => setGoal((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Savings goal in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Initial Deposit</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="1000"
            value={initial}
            onInput={(e) => setInitial((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Initial deposit in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Monthly Contribution</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" placeholder="500"
            value={monthly}
            onInput={(e) => setMonthly((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Monthly contribution in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Annual Return Rate</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="0.1" placeholder="4"
            value={rate}
            onInput={(e) => setRate((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Annual return rate as percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Inflation Rate: {inflationRate}%
        </label>
        <input
          type="range" min="1" max="10" step="0.5"
          value={inflationRate}
          onInput={(e) => setInflationRate((e.target as HTMLInputElement).value)}
          class="w-full accent-brand"
          aria-label="Inflation rate as percentage"
        />
        <div class="flex justify-between text-[11px] text-slate-400 mt-0.5">
          <span>1%</span>
          <span>10%</span>
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Extra monthly contribution: ${extraMonthly}
        </label>
        <input
          type="range" min="0" max="500" step="50"
          value={extraMonthly}
          onInput={(e) => setExtraMonthly(parseInt((e.target as HTMLInputElement).value, 10))}
          class="w-full accent-brand"
          aria-label="Extra monthly contribution in dollars"
        />
        <div class="flex justify-between text-[11px] text-slate-400 mt-0.5">
          <span>$0</span>
          <span>$500</span>
        </div>
      </div>

      {result ? (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-indigo-200 bg-indigo-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Time to Goal</span>
            <span class="text-2xl font-bold tabular-nums text-brand">
              {result.years < 1
                ? `${result.months} mo`
                : `${result.years.toFixed(1)} yrs`}
            </span>
          </div>
          <div class="h-px bg-slate-200" />
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Contributed</div>
              <div class="font-semibold text-slate-900">{fmtUsd(result.totalContributed)}</div>
            </div>
            <div>
              <div class="text-slate-500">Interest Earned</div>
              <div class="font-semibold text-green-700">{fmtUsd(result.interestEarned)}</div>
            </div>
          </div>
          {/* Contribution vs interest bar */}
          {(() => {
            const contribPct = (result.totalContributed / result.finalBalance) * 100;
            return (
              <div>
                <div class="mb-1 flex justify-between text-[11px] text-slate-500">
                  <span>Contributions {contribPct.toFixed(0)}%</span>
                  <span>Interest {(100 - contribPct).toFixed(0)}%</span>
                </div>
                <div class="flex h-2.5 overflow-hidden rounded-full">
                  <div class="bg-brand" style={{ width: `${contribPct}%` }} />
                  <div class="bg-green-400" style={{ width: `${100 - contribPct}%` }} />
                </div>
              </div>
            );
          })()}

          {extraResult && (
            <div class="rounded-lg bg-green-100 px-3 py-2 text-sm text-green-800">
              With +${extraMonthly}/mo extra: reach goal in <span class="font-semibold">{extraResult.months} months</span> — saves {extraResult.monthsSaved} months
            </div>
          )}

          {inflationAdjusted && (
            <div class="rounded-lg bg-slate-100 px-3 py-2 text-sm text-slate-700">
              At {inflationRate}% inflation, your {fmtUsd(parseFloat(goal) || 0)} goal needs to be <span class="font-semibold">{fmtUsd(inflationAdjusted)}</span> in {result.years.toFixed(1)} years
            </div>
          )}

          {milestones.length > 0 && (
            <div class="space-y-1">
              <p class="text-[11px] font-semibold uppercase tracking-wide text-slate-500">Milestones</p>
              <div class="flex flex-wrap gap-2">
                {milestones.map((m) => (
                  <span
                    key={m.target}
                    class="inline-flex items-center rounded-full bg-indigo-100 px-2.5 py-0.5 text-xs font-medium text-indigo-700"
                  >
                    {fmtUsd(m.target)} in {m.months} mo
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div class="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
          Goal unreachable in 50 years with these inputs. Try increasing your monthly contribution or rate.
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a licensed financial advisor.
      </p>
    </div>
  );
}
