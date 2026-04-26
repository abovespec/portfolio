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

  // P2: Scenario comparison — second product
  const [fixed2, setFixed2]     = useState('5000');
  const [variable2, setVariable2] = useState('25');
  const [sellPrice2, setSell2]   = useState('60');

  // P2: Break-even chart
  const [showBepChart, setShowBepChart] = useState(false);

  const r = useMemo(() => {
    const f = parseFloat(fixed) || 0;
    const v = parseFloat(variable) || 0;
    const s = parseFloat(sellPrice) || 0;
    if (s <= v) return null;
    const units = f / (s - v);
    return { units: Math.ceil(units), revenue: Math.ceil(units) * s, fixedCosts: f, variableCostPerUnit: v, pricePerUnit: s };
  }, [fixed, variable, sellPrice]);

  const r2 = useMemo(() => {
    const f = parseFloat(fixed2) || 0;
    const v = parseFloat(variable2) || 0;
    const s = parseFloat(sellPrice2) || 0;
    if (s <= v) return null;
    const units = f / (s - v);
    return { units: Math.ceil(units), revenue: Math.ceil(units) * s };
  }, [fixed2, variable2, sellPrice2]);

  const bepChartPoints = useMemo(() => {
    if (!showBepChart || !r) return { revenue: '', cost: '' };
    const fixedCost = r.fixedCosts;
    const varCost = r.variableCostPerUnit;
    const price = r.pricePerUnit;
    const bepUnits = r.units;
    const maxUnits = Math.ceil(bepUnits * 2.2);
    const steps = 8;
    const W = 400, H = 140, PAD = 12;
    const maxRevenue = maxUnits * price;
    const revPoints = Array.from({length:steps+1}, (_,i) => {
      const u = (i/steps)*maxUnits;
      const x = PAD + (i/steps)*(W-PAD*2);
      const y = (H-PAD) - (u*price/maxRevenue)*(H-PAD*2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
    const costPoints = Array.from({length:steps+1}, (_,i) => {
      const u = (i/steps)*maxUnits;
      const x = PAD + (i/steps)*(W-PAD*2);
      const totalCost = fixedCost + u*varCost;
      const y = (H-PAD) - (totalCost/maxRevenue)*(H-PAD*2);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    }).join(' ');
    return { revenue: revPoints, cost: costPoints };
  }, [showBepChart, r]);

  return (
    <div class="space-y-4">
      {/* Scenario comparison - 2-column layout */}
      <div class="grid grid-cols-2 gap-3">
        {/* Scenario A */}
        <div class="space-y-3">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Scenario A</div>
          {([
            { id: 'fixed-a', label: 'Fixed Costs', val: fixed, set: setFixed },
            { id: 'var-a',   label: 'Var. Cost / Unit', val: variable, set: setVar },
            { id: 'sell-a',  label: 'Price / Unit', val: sellPrice, set: setSell },
          ] as { id: string; label: string; val: string; set: (v: string) => void }[]).map(({ id, label, val, set }) => (
            <div key={id}>
              <label class="mb-0.5 block text-xs font-medium text-slate-600">{label}</label>
              <div class="relative">
                <span class="pointer-events-none absolute left-2 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
                <input type="number" min="0" step="1" value={val}
                  onInput={(e) => set((e.target as HTMLInputElement).value)}
                  class="w-full rounded-lg border border-slate-300 pl-5 pr-2 py-1.5 text-xs focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
                  aria-label={label} />
              </div>
            </div>
          ))}
        </div>
        {/* Scenario B */}
        <div class="space-y-3">
          <div class="text-xs font-semibold text-slate-500 uppercase tracking-wide">Scenario B</div>
          {([
            { id: 'fixed-b', label: 'Fixed Costs', val: fixed2, set: setFixed2 },
            { id: 'var-b',   label: 'Var. Cost / Unit', val: variable2, set: setVariable2 },
            { id: 'sell-b',  label: 'Price / Unit', val: sellPrice2, set: setSell2 },
          ] as { id: string; label: string; val: string; set: (v: string) => void }[]).map(({ id, label, val, set }) => (
            <div key={id}>
              <label class="mb-0.5 block text-xs font-medium text-slate-600">{label}</label>
              <div class="relative">
                <span class="pointer-events-none absolute left-2 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
                <input type="number" min="0" step="1" value={val}
                  onInput={(e) => set((e.target as HTMLInputElement).value)}
                  class="w-full rounded-lg border border-slate-300 pl-5 pr-2 py-1.5 text-xs focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
                  aria-label={label} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Side-by-side results */}
      <div class="grid grid-cols-2 gap-3">
        <div>
          {r ? (
            <div role="status" aria-live="polite" class={resultCls}>
              <div class="text-xs font-semibold text-slate-500 mb-1">Scenario A</div>
              <div class="flex justify-between text-sm"><span class="text-slate-600">BEP Units</span><span class="font-bold text-slate-900">{r.units.toLocaleString()}</span></div>
              <div class="flex justify-between text-sm"><span class="text-slate-600">BEP Revenue</span><span class="font-bold text-brand">{fmtUsd(r.revenue)}</span></div>
            </div>
          ) : (
            <p class="text-xs text-red-600">Price must exceed variable cost.</p>
          )}
        </div>
        <div>
          {r2 ? (
            <div role="status" aria-live="polite" class={resultCls}>
              <div class="text-xs font-semibold text-slate-500 mb-1">Scenario B</div>
              <div class="flex justify-between text-sm"><span class="text-slate-600">BEP Units</span><span class="font-bold text-slate-900">{r2.units.toLocaleString()}</span></div>
              <div class="flex justify-between text-sm"><span class="text-slate-600">BEP Revenue</span><span class="font-bold text-brand">{fmtUsd(r2.revenue)}</span></div>
            </div>
          ) : (
            <p class="text-xs text-red-600">Price must exceed variable cost.</p>
          )}
        </div>
      </div>

      {/* P2: Break-even chart toggle */}
      {r && (
        <>
          <button
            type="button"
            onClick={() => setShowBepChart((v) => !v)}
            class={`w-full rounded-lg border px-3 py-2 text-sm font-medium transition ${
              showBepChart
                ? 'border-green-300 bg-green-50 text-green-700'
                : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
            }`}
          >
            {showBepChart ? 'Hide' : 'Show'} Break-Even Chart (Scenario A)
          </button>

          {showBepChart && bepChartPoints.revenue && (
            <div class="rounded-lg border border-slate-200 bg-white p-3">
              <div class="flex gap-4 text-[11px] text-slate-500 mb-2">
                <span class="flex items-center gap-1">
                  <span class="inline-block w-5 h-0.5 bg-green-500"></span>Revenue
                </span>
                <span class="flex items-center gap-1">
                  <span class="inline-block w-5 h-0.5 bg-red-500"></span>Total Cost
                </span>
              </div>
              <svg viewBox="0 0 400 140" class="w-full" style={{ height: '140px' }} aria-label="Break-even chart">
                <polyline
                  points={bepChartPoints.revenue}
                  fill="none"
                  stroke="#22c55e"
                  stroke-width="2"
                  stroke-linejoin="round"
                  stroke-linecap="round"
                />
                <polyline
                  points={bepChartPoints.cost}
                  fill="none"
                  stroke="#ef4444"
                  stroke-width="2"
                  stroke-linejoin="round"
                  stroke-linecap="round"
                />
              </svg>
              <p class="text-xs text-slate-400 mt-1 text-center">
                Break-even at {r.units.toLocaleString()} units ({fmtUsd(r.revenue)})
              </p>
            </div>
          )}
        </>
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
