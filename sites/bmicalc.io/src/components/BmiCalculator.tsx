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

interface HealthyWeightRange {
  minLbs: number;
  maxLbs: number;
  minKg: number;
  maxKg: number;
  heightLabel: string;
}

function calcHealthyRange(unit: Unit, ft: number, inches: number, cm: number): HealthyWeightRange | null {
  let heightM = 0;
  let heightLabel = '';
  if (unit === 'imperial') {
    const totalIn = ft * 12 + inches;
    if (totalIn <= 0) return null;
    heightM = totalIn * 0.0254;
    heightLabel = `${ft}' ${inches}"`;
  } else {
    if (cm <= 0) return null;
    heightM = cm / 100;
    heightLabel = `${cm} cm`;
  }
  const minKg = 18.5 * heightM * heightM;
  const maxKg = 24.9 * heightM * heightM;
  const minLbs = minKg * 2.20462;
  const maxLbs = maxKg * 2.20462;
  return { minLbs, maxLbs, minKg, maxKg, heightLabel };
}

export default function BmiCalculator() {
  const [unit, setUnit]         = useState<Unit>('imperial');
  const [heightFt, setHeightFt] = useState('');
  const [heightIn, setHeightIn] = useState('');
  const [heightCm, setHeightCm] = useState('');
  const [weightLbs, setWeightLbs] = useState('');
  const [weightKg, setWeightKg]   = useState('');

  // P2: Waist state
  const [showWaist, setShowWaist] = useState(false);
  const [waistIn, setWaistIn] = useState('');
  const [waistCm, setWaistCm] = useState('');

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
  const gaugePct  = hasResult ? Math.min(Math.max(((bmi - 15) / 25) * 100, 0), 100) : 0;

  const healthyRange = useMemo(() => {
    return calcHealthyRange(
      unit,
      parseFloat(heightFt) || 0,
      parseFloat(heightIn) || 0,
      parseFloat(heightCm) || 0,
    );
  }, [unit, heightFt, heightIn, heightCm]);

  const currentWeightKg = useMemo(() => {
    if (unit === 'imperial') {
      const lbs = parseFloat(weightLbs) || 0;
      return lbs > 0 ? lbs / 2.20462 : 0;
    }
    return parseFloat(weightKg) || 0;
  }, [unit, weightLbs, weightKg]);

  const currentWeightLbs = useMemo(() => {
    if (unit === 'imperial') return parseFloat(weightLbs) || 0;
    const kg = parseFloat(weightKg) || 0;
    return kg > 0 ? kg * 2.20462 : 0;
  }, [unit, weightLbs, weightKg]);

  // P2: Waist risk
  const waistRisk = useMemo(() => {
    if (!showWaist || !hasResult) return null;
    const inches = unit === 'imperial' ? parseFloat(waistIn)||0 : (parseFloat(waistCm)||0)/2.54;
    if (!inches) return null;
    return {
      inches,
      cm: inches * 2.54,
      risk: inches > 40 ? 'High' : inches > 35 ? 'Elevated' : 'Normal',
      color: inches > 40 ? '#ef4444' : inches > 35 ? '#f97316' : '#15803d',
    };
  }, [showWaist, hasResult, waistIn, waistCm, unit]);

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

      {/* P3: Children note */}
      <div class="rounded-lg border border-blue-100 bg-blue-50 px-3 py-2 text-xs text-blue-700">
        Note: BMI interpretation differs for children under 18. These results use adult BMI ranges (18.5–24.9 = healthy).
      </div>

      {/* BMI Result */}
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

          {/* Gauge bar */}
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

      {/* P2: Waist Risk Assessment toggle */}
      {hasResult && (
        <button
          type="button"
          onClick={() => setShowWaist((v) => !v)}
          class={`w-full rounded-lg border px-3 py-2 text-sm font-medium transition ${
            showWaist
              ? 'border-orange-300 bg-orange-50 text-orange-700'
              : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
          }`}
        >
          {showWaist ? 'Hide' : 'Add'} Waist Risk Assessment
        </button>
      )}

      {/* P2: Waist input and result */}
      {hasResult && showWaist && (
        <div class="rounded-xl border border-orange-200 bg-orange-50 p-4 space-y-3">
          <div>
            <label class="mb-1 block text-sm font-medium text-slate-700">
              Waist Circumference ({unit === 'imperial' ? 'inches' : 'cm'})
            </label>
            <div class="relative">
              <input
                type="number"
                min="20"
                max="100"
                step="0.1"
                placeholder={unit === 'imperial' ? '34' : '86'}
                value={unit === 'imperial' ? waistIn : waistCm}
                onInput={(e) => {
                  const v = (e.target as HTMLInputElement).value;
                  if (unit === 'imperial') setWaistIn(v);
                  else setWaistCm(v);
                }}
                class={inputCls}
                aria-label={`Waist circumference in ${unit === 'imperial' ? 'inches' : 'centimeters'}`}
              />
              <span class="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
                {unit === 'imperial' ? 'in' : 'cm'}
              </span>
            </div>
          </div>

          {waistRisk && (
            <div class="space-y-2">
              <div class="flex items-center gap-2">
                <span
                  class="rounded-full px-2.5 py-0.5 text-xs font-semibold text-white"
                  style={{ backgroundColor: waistRisk.color }}
                >
                  {waistRisk.risk} Risk
                </span>
                <span class="text-xs text-slate-600">
                  {waistRisk.inches.toFixed(1)}" / {waistRisk.cm.toFixed(1)} cm
                </span>
              </div>
              <p class="text-xs text-slate-600">
                Abdominal obesity (&gt;40&#8243; men, &gt;35&#8243; women) is an independent cardiovascular risk factor.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Healthy Weight Range Card */}
      {healthyRange && (
        <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 space-y-2">
          <div class="flex items-center gap-2">
            <svg class="h-4 w-4 text-emerald-600 shrink-0" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-1.293-5.293a1 1 0 001.414 0l4-4a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2z" clip-rule="evenodd" />
            </svg>
            <h3 class="text-sm font-semibold text-slate-700">Healthy Weight for Your Height</h3>
          </div>
          <p class="text-sm text-slate-600">
            For a height of <strong>{healthyRange.heightLabel}</strong>, a healthy BMI (18.5–24.9) corresponds to:
          </p>
          <div class="grid grid-cols-2 gap-2 text-sm">
            <div class="rounded-lg bg-white border border-slate-200 p-3 text-center">
              <div class="font-bold text-slate-800">{healthyRange.minLbs.toFixed(0)}–{healthyRange.maxLbs.toFixed(0)} lbs</div>
              <div class="text-xs text-slate-500 mt-0.5">Imperial</div>
            </div>
            <div class="rounded-lg bg-white border border-slate-200 p-3 text-center">
              <div class="font-bold text-slate-800">{healthyRange.minKg.toFixed(1)}–{healthyRange.maxKg.toFixed(1)} kg</div>
              <div class="text-xs text-slate-500 mt-0.5">Metric</div>
            </div>
          </div>
          {/* Status relative to healthy range */}
          {(currentWeightLbs > 0) && (() => {
            const diffLbs = currentWeightLbs - healthyRange.maxLbs;
            const diffBelowLbs = healthyRange.minLbs - currentWeightLbs;
            if (currentWeightLbs >= healthyRange.minLbs && currentWeightLbs <= healthyRange.maxLbs) {
              return (
                <div class="flex items-center gap-2 rounded-lg bg-emerald-50 border border-emerald-100 px-3 py-2 text-sm text-emerald-800">
                  <span class="text-emerald-600 font-bold">✓</span>
                  <span>You're in the healthy weight range for your height.</span>
                </div>
              );
            } else if (diffLbs > 0) {
              return (
                <div class="rounded-lg bg-amber-50 border border-amber-100 px-3 py-2 text-sm text-amber-800">
                  You are <strong>{diffLbs.toFixed(0)} lbs ({(diffLbs / 2.20462).toFixed(1)} kg)</strong> above the healthy range for your height.
                </div>
              );
            } else if (diffBelowLbs > 0) {
              return (
                <div class="rounded-lg bg-amber-50 border border-amber-100 px-3 py-2 text-sm text-amber-800">
                  You are <strong>{diffBelowLbs.toFixed(0)} lbs ({(diffBelowLbs / 2.20462).toFixed(1)} kg)</strong> below the healthy range for your height.
                </div>
              );
            }
            return null;
          })()}
        </div>
      )}

      {/* Inline disclaimer */}
      <p class="text-xs leading-relaxed text-slate-500">
        For informational purposes only. Consult a healthcare professional for medical advice.
      </p>

    </div>
  );
}
