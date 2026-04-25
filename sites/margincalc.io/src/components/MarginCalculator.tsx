import { useState, useMemo } from 'preact/hooks';

type Tab = 'profit-margin' | 'markup' | 'break-even' | 'reverse-margin';

function fmtUsd(n: number) {
  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}
function fmtPct(n: number) { return n.toFixed(2) + '%'; }

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';
const resultCls = 'space-y-3 rounded-xl border border-brand/30 bg-green-50 p-4';

function ProfitMarginTab() {
  const [cost, setCost]   = useState('50');
  const [price, setPrice] = useState('100');
  const r = useMemo(() => {
    const c = parseFloat(cost) || 0;
    const p = parseFloat(price) || 0;
    if (p <= 0) return null;
    const profit = p - c;
    return { profit, margin: (profit / p) * 100, markup: (profit / c) * 100 };
  }, [cost, price]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Selling Price</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={price}
            onInput={(e) => setPrice((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Selling price" />
        </div>
      </div>
      {r && (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit Margin</span><span class="font-bold text-brand">{fmtPct(r.margin)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Markup</span><span class="font-bold text-slate-900">{fmtPct(r.markup)}</span></div>
        </div>
      )}
    </div>
  );
}

function MarkupTab() {
  const [cost, setCost] = useState('50');
  const [pct, setPct]   = useState('50');
  const r = useMemo(() => {
    const c = parseFloat(cost) || 0;
    const p = parseFloat(pct) || 0;
    const price = c * (1 + p / 100);
    const profit = price - c;
    return { price, profit, margin: (profit / price) * 100 };
  }, [cost, pct]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Markup</label>
        <div class="relative">
          <input type="number" min="0" step="0.1" value={pct}
            onInput={(e) => setPct((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Markup percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div role="status" aria-live="polite" class={resultCls}>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Selling Price</span><span class="font-bold text-slate-900">{fmtUsd(r.price)}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
        <div class="flex justify-between text-sm"><span class="text-slate-600">Profit Margin</span><span class="font-bold text-brand">{fmtPct(r.margin)}</span></div>
      </div>
    </div>
  );
}

function BreakEvenTab() {
  const [fixed, setFixed]    = useState('5000');
  const [variable, setVar]   = useState('20');
  const [sellPrice, setSell] = useState('50');
  const r = useMemo(() => {
    const f = parseFloat(fixed) || 0;
    const v = parseFloat(variable) || 0;
    const s = parseFloat(sellPrice) || 0;
    if (s <= v) return null;
    const units = f / (s - v);
    return { units: Math.ceil(units), revenue: Math.ceil(units) * s };
  }, [fixed, variable, sellPrice]);
  return (
    <div class="space-y-4">
      {([
        { id: 'fixed', label: 'Fixed Costs', val: fixed, set: setFixed },
        { id: 'var',   label: 'Variable Cost / Unit', val: variable, set: setVar },
        { id: 'sell',  label: 'Selling Price / Unit', val: sellPrice, set: setSell },
      ] as { id: string; label: string; val: string; set: (v: string) => void }[]).map(({ id, label, val, set }) => (
        <div key={id}>
          <label class="mb-1 block text-sm font-medium text-slate-700">{label}</label>
          <div class="relative">
            <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
            <input type="number" min="0" step="1" value={val}
              onInput={(e) => set((e.target as HTMLInputElement).value)}
              class={`${inputCls} pl-6`} aria-label={label} />
          </div>
        </div>
      ))}
      {r ? (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Break-Even Units</span><span class="font-bold text-slate-900">{r.units.toLocaleString()}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Break-Even Revenue</span><span class="font-bold text-brand">{fmtUsd(r.revenue)}</span></div>
        </div>
      ) : (
        <p class="text-xs text-red-600">Selling price must be greater than variable cost.</p>
      )}
    </div>
  );
}

function ReverseMarginTab() {
  const [margin, setMargin] = useState('30');
  const [cost, setCost]     = useState('70');
  const r = useMemo(() => {
    const m = parseFloat(margin) || 0;
    const c = parseFloat(cost) || 0;
    if (m >= 100 || c <= 0) return null;
    const price = c / (1 - m / 100);
    return { price, profit: price - c };
  }, [margin, cost]);
  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Desired Margin</label>
        <div class="relative">
          <input type="number" min="0" max="99.9" step="0.1" value={margin}
            onInput={(e) => setMargin((e.target as HTMLInputElement).value)}
            class={inputCls} aria-label="Desired profit margin percentage" />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
        </div>
      </div>
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Cost</label>
        <div class="relative">
          <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
          <input type="number" min="0" step="0.01" value={cost}
            onInput={(e) => setCost((e.target as HTMLInputElement).value)}
            class={`${inputCls} pl-6`} aria-label="Cost" />
        </div>
      </div>
      {r ? (
        <div role="status" aria-live="polite" class={resultCls}>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Required Price</span><span class="font-bold text-brand">{fmtUsd(r.price)}</span></div>
          <div class="flex justify-between text-sm"><span class="text-slate-600">Profit</span><span class="font-bold text-slate-900">{fmtUsd(r.profit)}</span></div>
        </div>
      ) : (
        <p class="text-xs text-red-600">Margin must be less than 100%.</p>
      )}
    </div>
  );
}

const TABS: { id: Tab; label: string }[] = [
  { id: 'profit-margin',  label: 'Profit Margin' },
  { id: 'markup',         label: 'Markup' },
  { id: 'break-even',     label: 'Break-Even' },
  { id: 'reverse-margin', label: 'Reverse' },
];

export default function MarginCalculator() {
  const [tab, setTab] = useState<Tab>('profit-margin');
  return (
    <div class="space-y-4">
      <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
        {TABS.map(({ id, label }) => (
          <button
            key={id}
            type="button"
            onClick={() => setTab(id)}
            aria-pressed={tab === id}
            class={`flex-1 rounded-md py-1.5 text-xs font-medium transition-all ${
              tab === id
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>
      {tab === 'profit-margin'  && <ProfitMarginTab />}
      {tab === 'markup'         && <MarkupTab />}
      {tab === 'break-even'     && <BreakEvenTab />}
      {tab === 'reverse-margin' && <ReverseMarginTab />}
    </div>
  );
}
