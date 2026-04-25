import { useState, useMemo } from 'preact/hooks';

function calcTip(bill: number, tipPct: number, people: number) {
  if (bill <= 0 || tipPct < 0 || people < 1) return null;
  const tipAmount = bill * (tipPct / 100);
  const total = bill + tipAmount;
  const perPerson = total / people;
  const tipPerPerson = tipAmount / people;
  return { tipAmount, total, perPerson, tipPerPerson };
}

function fmtUsd(n: number) {
  return '$' + n.toFixed(2);
}

const QUICK_TIPS = [10, 15, 18, 20, 25];

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function TipCalculator() {
  const [bill, setBill]     = useState('50.00');
  const [tipPct, setTipPct] = useState('18');
  const [people, setPeople] = useState('1');

  const result = useMemo(
    () => calcTip(parseFloat(bill) || 0, parseFloat(tipPct) || 0, parseInt(people) || 1),
    [bill, tipPct, people],
  );

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Bill Amount</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input
            type="number" min="0" step="0.01" placeholder="50.00"
            value={bill}
            onInput={(e) => setBill((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`}
            aria-label="Bill amount in dollars"
          />
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Tip Percentage</label>
        <div class="relative">
          <input
            type="number" min="0" max="100" step="1" placeholder="18"
            value={tipPct}
            onInput={(e) => setTipPct((e.target as HTMLInputElement).value)}
            class={inputCls}
            aria-label="Tip percentage"
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
        <div class="mt-2 flex flex-wrap gap-1.5">
          {QUICK_TIPS.map((pct) => (
            <button
              key={pct}
              type="button"
              onClick={() => setTipPct(String(pct))}
              class={`rounded-lg border px-3 py-1 text-xs font-medium transition ${
                tipPct === String(pct)
                  ? 'border-brand bg-brand text-white'
                  : 'border-slate-200 bg-white text-slate-600 hover:border-brand/50'
              }`}
            >
              {pct}%
            </button>
          ))}
        </div>
      </div>

      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Number of People</label>
        <input
          type="number" min="1" max="50" step="1" placeholder="1"
          value={people}
          onInput={(e) => setPeople((e.target as HTMLInputElement).value)}
          class={inputCls}
          aria-label="Number of people splitting the bill"
        />
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/30 bg-orange-50 p-4">
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Tip Amount</span>
            <span class="text-2xl font-bold tabular-nums text-brand">{fmtUsd(result.tipAmount)}</span>
          </div>
          <div class="flex items-baseline justify-between">
            <span class="text-sm text-slate-600">Total Bill</span>
            <span class="text-xl font-bold tabular-nums text-slate-900">{fmtUsd(result.total)}</span>
          </div>
          {parseInt(people) > 1 && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div>
                  <div class="text-slate-500">Per Person (total)</div>
                  <div class="font-semibold tabular-nums text-slate-900">{fmtUsd(result.perPerson)}</div>
                </div>
                <div>
                  <div class="text-slate-500">Tip per Person</div>
                  <div class="font-semibold tabular-nums text-slate-900">{fmtUsd(result.tipPerPerson)}</div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Tipping is customary but not legally required in most places.
      </p>
    </div>
  );
}
