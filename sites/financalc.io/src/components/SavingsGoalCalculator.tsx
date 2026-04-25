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

  const result = useMemo(
    () => calcSavings(
      parseFloat(goal) || 0,
      parseFloat(initial) || 0,
      parseFloat(monthly) || 0,
      parseFloat(rate) || 0,
    ),
    [goal, initial, monthly, rate],
  );

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
