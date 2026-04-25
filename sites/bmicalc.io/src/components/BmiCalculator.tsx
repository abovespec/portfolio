import { useState, useMemo } from 'preact/hooks';

type Unit = 'imperial' | 'metric';

interface BmiCategory {
  label: string;
  range: string;
  color: string;
  textColor: string;
  bgColor: string;
}

const CATEGORIES: BmiCategory[] = [
  { label: 'Underweight',   range: 'Below 18.5',   color: '#3b82f6', textColor: '#1e40af', bgColor: '#eff6ff' },
  { label: 'Normal weight', range: '18.5 – 24.9',  color: '#15803d', textColor: '#14532d', bgColor: '#f0fdf4' },
  { label: 'Overweight',    range: '25 – 29.9',    color: '#f97316', textColor: '#9a3412', bgColor: '#fff7ed' },
  { label: 'Obese',         range: '30 and above', color: '#ef4444', textColor: '#7f1d1d', bgColor: '#fef2f2' },
];

function getCategory(bmi: number): BmiCategory {
  if (bmi < 18.5) return CATEGORIES[0]!;
  if (bmi < 25)   return CATEGORIES[1]!;
  if (bmi < 30)   return CATEGORIES[2]!;
  return CATEGORIES[3]!;
}

function calcBmiImperial(ft: number, inches: number, lbs: number): number {
  const totalIn = ft * 12 + inches;
  if (totalIn <= 0 || lbs <= 0) return 0;
  return (lbs / (totalIn * totalIn)) * 703;
}

function calcBmiMetric(cm: number, kg: number): number {
  if (cm <= 0 || kg <= 0) return 0;
  const m = cm / 100;
  return kg / (m * m);
}

export default function BmiCalculator() {
  const [unit, setUnit]         = useState<Unit>('imperial');
  const [heightFt, setHeightFt] = useState('');
  const [heightIn, setHeightIn] = useState('');
  const [heightCm, setHeightCm] = useState('');
  const [weightLbs, setWeightLbs] = useState('');
  const [weightKg, setWeightKg]   = useState('');

  const bmi = useMemo(() => {
    if (unit === 'imperial') {
      return calcBmiImperial(
        parseFloat(heightFt)  || 0,
        parseFloat(heightIn)  || 0,
        parseFloat(weightLbs) || 0,
      );
    }
    return calcBmiMetric(parseFloat(heightCm) || 0, parseFloat(weightKg) || 0);
  }, [unit, heightFt, heightIn, heightCm, weightLbs, weightKg]);

  const hasResult = bmi > 0 && isFinite(bmi);
  const category  = hasResult ? getCategory(bmi) : null;
  // Maps BMI 15–40 range to 0–100% for the gauge marker
  const gaugePct  = hasResult ? Math.min(Math.max(((bmi - 15) / 25) * 100, 0), 100) : 0;

  const inputCls =
    'w-full rounded-lg border border-slate-300 px-3 py-2 pr-10 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

  return (
    <div class="space-y-4">

      {/* Unit toggle */}
      <div class="flex gap-1 rounded-lg border border-slate-200 bg-slate-50 p-1">
        {(['imperial', 'metric'] as const).map((u) => (
          <button
            key={u}
            type="button"
            class={`flex-1 rounded-md py-1.5 text-sm font-medium capitalize transition-all ${
              unit === u
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}
            onClick={() => setUnit(u)}
            aria-pressed={unit === u}
          >
            {u}
          </button>
        ))}
      </div>

      {/* Height */}
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Height</label>
        {unit === 'imperial' ? (
          <div class="flex gap-2">
            <div class="relative flex-1">
              <input
                type="number" min="1" max="8" placeholder="5"
                value={heightFt}
                onInput={(e) => setHeightFt((e.target as HTMLInputElement).value)}
                class={inputCls}
                aria-label="Height in feet"
              />
              <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
                ft
              </span>
            </div>
            <div class="relative flex-1">
              <input
                type="number" min="0" max="11" placeholder="10"
                value={heightIn}
                onInput={(e) => setHeightIn((e.target as HTMLInputElement).value)}
                class={inputCls}
                aria-label="Height in inches"
              />
              <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
                in
              </span>
            </div>
          </div>
        ) : (
          <div class="relative">
            <input
              type="number" min="50" max="300" placeholder="170"
              value={heightCm}
              onInput={(e) => setHeightCm((e.target as HTMLInputElement).value)}
              class={inputCls}
              aria-label="Height in centimeters"
            />
            <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              cm
            </span>
          </div>
        )}
      </div>

      {/* Weight */}
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">Weight</label>
        <div class="relative">
          <input
            type="number"
            min="1"
            max={unit === 'imperial' ? '1000' : '500'}
            placeholder={unit === 'imperial' ? '150' : '70'}
            value={unit === 'imperial' ? weightLbs : weightKg}
            onInput={(e) => {
              const v = (e.target as HTMLInputElement).value;
              if (unit === 'imperial') setWeightLbs(v);
              else setWeightKg(v);
            }}
            class={inputCls}
            aria-label={unit === 'imperial' ? 'Weight in pounds' : 'Weight in kilograms'}
          />
          <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
            {unit === 'imperial' ? 'lbs' : 'kg'}
          </span>
        </div>
      </div>

      {/* Result */}
      {hasResult && category && (
        <div
          role="status"
          aria-live="polite"
          class="space-y-3 rounded-xl border-2 p-4"
          style={{ borderColor: category.color, backgroundColor: category.bgColor }}
        >
          <div class="flex items-start justify-between">
            <div>
              <div
                class="text-4xl font-bold tabular-nums"
                style={{ color: category.color }}
              >
                {bmi.toFixed(1)}
              </div>
              <div class="mt-0.5 text-sm font-semibold" style={{ color: category.textColor }}>
                {category.label}
              </div>
            </div>
            <div class="text-right text-xs text-slate-500">
              <div class="font-medium">Your BMI</div>
              <div class="mt-0.5">{category.range}</div>
            </div>
          </div>

          {/* Gauge bar — gradient from underweight (blue) to obese (red) */}
          <div>
            <div
              class="relative h-2.5 overflow-hidden rounded-full"
              style={{ background: 'linear-gradient(to right, #3b82f6 0%, #22c55e 30%, #f97316 65%, #ef4444 100%)' }}
            >
              <div
                class="absolute top-1/2 h-4 w-4 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white bg-slate-800 shadow"
                style={{ left: `${gaugePct}%` }}
                role="img"
                aria-label={`BMI ${bmi.toFixed(1)} on scale`}
              />
            </div>
            <div class="mt-1 flex justify-between text-[10px] text-slate-400">
              <span>15</span><span>18.5</span><span>25</span><span>30</span><span>40+</span>
            </div>
          </div>
        </div>
      )}

      {/* Inline disclaimer */}
      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a healthcare professional for medical advice.
      </p>

    </div>
  );
}
