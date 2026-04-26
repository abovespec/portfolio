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

// P3: Venue type suggestions
const VENUE_TIPS = [
  {label:'Restaurant', pct:18},
  {label:'Delivery',   pct:15},
  {label:'Bar',        pct:20},
  {label:'Taxi',       pct:15},
  {label:'Hotel',      pct:10},
];

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

// ── Itemized split types ──
interface Person {
  id: number;
  name: string;
}
interface LineItem {
  id: number;
  name: string;
  price: string;
  assignees: number[]; // person ids
}

let _nextPersonId = 3;
let _nextItemId = 1;

function newPerson(id: number): Person {
  return { id, name: 'Person ' + id };
}

function ItemizedSplit({ tipPct, setTipPct }: { tipPct: string; setTipPct: (v: string) => void }) {
  const [people, setPeople] = useState<Person[]>([newPerson(1), newPerson(2)]);
  const [items, setItems] = useState<LineItem[]>([]);

  function addPerson() {
    if (people.length >= 8) return;
    const id = _nextPersonId++;
    setPeople([...people, newPerson(id)]);
  }
  function removePerson(id: number) {
    if (people.length <= 1) return;
    setPeople(people.filter((p) => p.id !== id));
    setItems(items.map((item) => ({
      ...item,
      assignees: item.assignees.filter((a) => a !== id),
    })));
  }
  function updatePersonName(id: number, name: string) {
    setPeople(people.map((p) => (p.id === id ? { ...p, name } : p)));
  }

  function addItem() {
    const id = _nextItemId++;
    setItems([...items, { id, name: '', price: '', assignees: people.map((p) => p.id) }]);
  }
  function removeItem(id: number) {
    setItems(items.filter((item) => item.id !== id));
  }
  function updateItemName(id: number, name: string) {
    setItems(items.map((item) => (item.id === id ? { ...item, name } : item)));
  }
  function updateItemPrice(id: number, price: string) {
    setItems(items.map((item) => (item.id === id ? { ...item, price } : item)));
  }
  function toggleAssignee(itemId: number, personId: number) {
    setItems(items.map((item) => {
      if (item.id !== itemId) return item;
      const has = item.assignees.includes(personId);
      return {
        ...item,
        assignees: has
          ? item.assignees.filter((a) => a !== personId)
          : [...item.assignees, personId],
      };
    }));
  }

  // Compute subtotals per person
  const summary = useMemo(() => {
    const subtotals: Record<number, number> = {};
    people.forEach((p) => { subtotals[p.id] = 0; });

    items.forEach((item) => {
      const price = parseFloat(item.price) || 0;
      const assigned = item.assignees.filter((a) => people.some((p) => p.id === a));
      if (assigned.length === 0) return;
      const share = price / assigned.length;
      assigned.forEach((id) => { subtotals[id] = (subtotals[id] || 0) + share; });
    });

    const grandSubtotal = Object.values(subtotals).reduce((a, b) => a + b, 0);
    const tipRate = (parseFloat(tipPct) || 0) / 100;
    const tipTotal = grandSubtotal * tipRate;

    const rows = people.map((p) => {
      const sub = subtotals[p.id] || 0;
      const tipShare = grandSubtotal > 0 ? tipTotal * (sub / grandSubtotal) : 0;
      return { person: p, subtotal: sub, tipShare, total: sub + tipShare };
    });

    return { rows, grandSubtotal, tipTotal, grandTotal: grandSubtotal + tipTotal };
  }, [people, items, tipPct]);

  return (
    <div class="space-y-5">
      {/* Tip selector */}
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

      {/* People */}
      <div>
        <div class="mb-2 flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">People ({people.length})</label>
          {people.length < 8 && (
            <button
              type="button"
              onClick={addPerson}
              class="rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
            >
              + Add Person
            </button>
          )}
        </div>
        <div class="space-y-2">
          {people.map((p) => (
            <div key={p.id} class="flex items-center gap-2">
              <input
                type="text"
                value={p.name}
                onInput={(e) => updatePersonName(p.id, (e.target as HTMLInputElement).value)}
                class="flex-1 rounded-lg border border-slate-300 px-3 py-1.5 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
                placeholder="Name"
              />
              {people.length > 1 && (
                <button
                  type="button"
                  onClick={() => removePerson(p.id)}
                  class="shrink-0 rounded-lg border border-slate-200 px-2 py-1.5 text-xs text-slate-500 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition"
                  aria-label={'Remove ' + p.name}
                >
                  Remove
                </button>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Line items */}
      <div>
        <div class="mb-2 flex items-center justify-between">
          <label class="text-sm font-medium text-slate-700">Items</label>
          <button
            type="button"
            onClick={addItem}
            class="rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50 transition"
          >
            + Add Item
          </button>
        </div>
        {items.length === 0 && (
          <p class="text-xs text-slate-400">No items yet. Click "+ Add Item" to start.</p>
        )}
        <div class="space-y-3">
          {items.map((item) => (
            <div key={item.id} class="rounded-lg border border-slate-200 bg-slate-50 p-3 space-y-2">
              <div class="flex gap-2">
                <input
                  type="text"
                  value={item.name}
                  onInput={(e) => updateItemName(item.id, (e.target as HTMLInputElement).value)}
                  class="flex-1 rounded-lg border border-slate-300 px-2.5 py-1.5 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand bg-white"
                  placeholder="Item name"
                />
                <div class="relative w-28 shrink-0">
                  <span class="pointer-events-none absolute left-2.5 top-1/2 -translate-y-1/2 text-xs text-slate-400">$</span>
                  <input
                    type="number" min="0" step="0.01"
                    value={item.price}
                    onInput={(e) => updateItemPrice(item.id, (e.target as HTMLInputElement).value)}
                    class="w-full rounded-lg border border-slate-300 pl-6 pr-2 py-1.5 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand bg-white"
                    placeholder="0.00"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => removeItem(item.id)}
                  class="shrink-0 rounded-lg border border-slate-200 bg-white px-2 py-1.5 text-xs text-slate-500 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition"
                  aria-label="Remove item"
                >
                  &#x2715;
                </button>
              </div>
              <div class="flex flex-wrap gap-x-4 gap-y-1">
                {people.map((p) => (
                  <label key={p.id} class="flex items-center gap-1.5 text-xs text-slate-600 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={item.assignees.includes(p.id)}
                      onChange={() => toggleAssignee(item.id, p.id)}
                      class="accent-brand"
                    />
                    {p.name}
                  </label>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Summary table */}
      {items.length > 0 && (
        <div role="status" aria-live="polite" class="rounded-xl border border-brand/30 bg-orange-50 overflow-hidden">
          <div class="px-4 pt-4 pb-2">
            <p class="text-sm font-semibold text-slate-700 mb-3">Summary</p>
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="text-xs text-slate-500 border-b border-orange-200">
                    <th class="text-left pb-2 font-medium">Person</th>
                    <th class="text-right pb-2 font-medium">Subtotal</th>
                    <th class="text-right pb-2 font-medium">Tip ({tipPct || '0'}%)</th>
                    <th class="text-right pb-2 font-medium font-semibold text-slate-700">Total</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-orange-100">
                  {summary.rows.map((row) => (
                    <tr key={row.person.id}>
                      <td class="py-2 text-slate-700 font-medium">{row.person.name}</td>
                      <td class="py-2 text-right tabular-nums text-slate-600">{fmtUsd(row.subtotal)}</td>
                      <td class="py-2 text-right tabular-nums text-brand">{fmtUsd(row.tipShare)}</td>
                      <td class="py-2 text-right tabular-nums font-bold text-slate-900">{fmtUsd(row.total)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr class="border-t border-orange-200 bg-orange-100/60">
                    <td class="py-2 text-xs font-semibold text-slate-500">Total</td>
                    <td class="py-2 text-right tabular-nums text-xs font-semibold text-slate-600">{fmtUsd(summary.grandSubtotal)}</td>
                    <td class="py-2 text-right tabular-nums text-xs font-semibold text-brand">{fmtUsd(summary.tipTotal)}</td>
                    <td class="py-2 text-right tabular-nums font-bold text-slate-900">{fmtUsd(summary.grandTotal)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          <div class="px-4 py-2 text-xs text-slate-500">
            Items assigned to multiple people are split equally among those people.
          </div>
        </div>
      )}
    </div>
  );
}

export default function TipCalculator() {
  const [tab, setTab] = useState<'basic' | 'itemized'>('basic');
  const [bill, setBill]     = useState('50.00');
  const [tipPct, setTipPct] = useState('18');
  const [people, setPeople] = useState('1');

  // P2: Round mode
  const [roundMode, setRoundMode] = useState<'none'|'up'|'down'>('none');

  // P2: Pre-tax vs post-tax
  const [tipBase, setTipBase] = useState<'pretax'|'posttax'>('posttax');
  const [taxRate, setTaxRate] = useState('0');

  // Shared tip pct for itemized tab
  const [itemTipPct, setItemTipPct] = useState('18');

  // Effective bill for tip calculation
  const effectiveBillForTip = useMemo(() => {
    const b = parseFloat(bill) || 0;
    if (tipBase === 'pretax') {
      return b / (1 + (parseFloat(taxRate)||0)/100);
    }
    return b;
  }, [bill, tipBase, taxRate]);

  const result = useMemo(
    () => calcTip(effectiveBillForTip, parseFloat(tipPct) || 0, parseInt(people) || 1),
    [effectiveBillForTip, tipPct, people],
  );

  const perPersonDisplay = useMemo(() => {
    if (!result) return null;
    if (roundMode === 'up') return Math.ceil(result.perPerson);
    if (roundMode === 'down') return Math.floor(result.perPerson);
    return result.perPerson;
  }, [result, roundMode]);

  return (
    <div class="space-y-4">
      {/* Tab bar */}
      <div class="flex rounded-xl border border-slate-200 bg-slate-50 p-1 gap-1">
        <button
          type="button"
          onClick={() => setTab('basic')}
          class={`flex-1 rounded-lg py-2 text-sm font-medium transition ${
            tab === 'basic'
              ? 'bg-white shadow-sm text-slate-900'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Basic
        </button>
        <button
          type="button"
          onClick={() => setTab('itemized')}
          class={`flex-1 rounded-lg py-2 text-sm font-medium transition ${
            tab === 'itemized'
              ? 'bg-white shadow-sm text-slate-900'
              : 'text-slate-500 hover:text-slate-700'
          }`}
        >
          Itemized Split
        </button>
      </div>

      {tab === 'basic' && (
        <>
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

          {/* P2: Pre-tax / Post-tax toggle */}
          <div class="space-y-2">
            <div class="flex items-center gap-2">
              <span class="text-sm font-medium text-slate-700">Tip on:</span>
              <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-0.5">
                {(['posttax', 'pretax'] as const).map((mode) => (
                  <button
                    key={mode}
                    type="button"
                    onClick={() => setTipBase(mode)}
                    class={`rounded-md px-3 py-1 text-xs font-medium transition ${
                      tipBase === mode
                        ? 'bg-white text-slate-900 shadow-sm'
                        : 'text-slate-500 hover:text-slate-700'
                    }`}
                  >
                    {mode === 'posttax' ? 'Post-tax' : 'Pre-tax'}
                  </button>
                ))}
              </div>
            </div>
            {tipBase === 'pretax' && (
              <div class="flex items-center gap-2">
                <label class="text-xs text-slate-600 shrink-0">Tax rate:</label>
                <div class="relative w-28">
                  <input
                    type="number" min="0" max="30" step="0.1" placeholder="8.5"
                    value={taxRate}
                    onInput={(e) => setTaxRate((e.target as HTMLInputElement).value)}
                    class="w-full rounded-lg border border-slate-300 px-3 py-1.5 pr-8 text-xs focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand"
                    aria-label="Tax rate percentage"
                  />
                  <span class="pointer-events-none absolute right-2 top-1/2 -translate-y-1/2 text-xs text-slate-400">%</span>
                </div>
                {(parseFloat(taxRate)||0) > 0 && (
                  <span class="text-xs text-slate-500">
                    Pre-tax: {fmtUsd(effectiveBillForTip)}
                  </span>
                )}
              </div>
            )}
          </div>

          {/* P3: Venue type suggestions */}
          <div>
            <label class="mb-1 block text-xs font-medium text-slate-500 uppercase tracking-wide">Quick venue tip</label>
            <div class="flex flex-wrap gap-1.5">
              {VENUE_TIPS.map((v) => (
                <button
                  key={v.label}
                  type="button"
                  onClick={() => setTipPct(String(v.pct))}
                  class={`rounded-lg border px-2.5 py-1 text-xs font-medium transition ${
                    tipPct === String(v.pct)
                      ? 'border-brand bg-brand text-white'
                      : 'border-slate-200 bg-white text-slate-600 hover:border-brand/50'
                  }`}
                >
                  {v.label} {v.pct}%
                </button>
              ))}
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
                      <div class="font-semibold tabular-nums text-slate-900">
                        {fmtUsd(perPersonDisplay!)}
                      </div>
                    </div>
                    <div>
                      <div class="text-slate-500">Tip per Person</div>
                      <div class="font-semibold tabular-nums text-slate-900">{fmtUsd(result.tipPerPerson)}</div>
                    </div>
                  </div>
                  {/* P2: Round mode toggle */}
                  <div class="flex items-center gap-2 pt-1">
                    <span class="text-xs text-slate-500 shrink-0">Per person:</span>
                    <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-0.5">
                      {(['none', 'up', 'down'] as const).map((mode) => (
                        <button
                          key={mode}
                          type="button"
                          onClick={() => setRoundMode(mode)}
                          class={`rounded-md px-2.5 py-1 text-xs font-medium transition ${
                            roundMode === mode
                              ? 'bg-white text-slate-900 shadow-sm'
                              : 'text-slate-500 hover:text-slate-700'
                          }`}
                        >
                          {mode === 'none' ? 'Exact' : mode === 'up' ? 'Round Up' : 'Round Down'}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}
            </div>
          )}
        </>
      )}

      {tab === 'itemized' && (
        <ItemizedSplit tipPct={itemTipPct} setTipPct={setItemTipPct} />
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Tipping is customary but not legally required in most places.
      </p>
    </div>
  );
}
