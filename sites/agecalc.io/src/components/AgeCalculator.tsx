import { useState, useMemo } from 'preact/hooks';

function calcAge(dob: string) {
  if (!dob) return null;
  const birth = new Date(dob);
  const now = new Date();
  if (isNaN(birth.getTime()) || birth > now) return null;

  let years = now.getFullYear() - birth.getFullYear();
  let months = now.getMonth() - birth.getMonth();
  let days = now.getDate() - birth.getDate();

  if (days < 0) {
    months -= 1;
    const prevMonth = new Date(now.getFullYear(), now.getMonth(), 0);
    days += prevMonth.getDate();
  }
  if (months < 0) {
    years -= 1;
    months += 12;
  }

  const diffMs = now.getTime() - birth.getTime();
  const totalDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const totalWeeks = Math.floor(totalDays / 7);
  const totalHours = Math.floor(diffMs / (1000 * 60 * 60));
  const totalMinutes = Math.floor(diffMs / (1000 * 60));

  const nextBirthday = new Date(now.getFullYear(), birth.getMonth(), birth.getDate());
  if (nextBirthday <= now) nextBirthday.setFullYear(now.getFullYear() + 1);
  const daysToNextBirthday = Math.ceil(
    (nextBirthday.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
  );

  return { years, months, days, totalDays, totalWeeks, totalHours, totalMinutes, daysToNextBirthday };
}

const inputCls =
  'w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand focus:outline-none focus:ring-1 focus:ring-brand';

export default function AgeCalculator() {
  const today = new Date();
  const defaultDob = `${today.getFullYear() - 30}-${String(today.getMonth() + 1).padStart(2, '0')}-15`;
  const [dob, setDob] = useState(defaultDob);

  // P2: Age difference
  const [dob2, setDob2] = useState('');
  const [showDiff, setShowDiff] = useState(false);

  const result = useMemo(() => calcAge(dob), [dob]);

  // P2: Age difference calculation
  const ageDiff = useMemo(() => {
    if (!showDiff || !dob2 || !result) return null;
    const birth2 = new Date(dob2);
    if (isNaN(birth2.getTime())) return null;
    const ref = new Date(dob);
    const diffMs = Math.abs(ref.getTime() - birth2.getTime());
    const diffDays = Math.floor(diffMs / 86400000);
    const diffYears = Math.floor(diffDays / 365.25);
    const diffMonths = Math.round((diffDays % 365.25) / 30.44);
    return { diffDays, diffYears, diffMonths };
  }, [showDiff, dob, dob2, result]);

  // P2: Milestone countdown
  const milestones = useMemo(() => {
    if (!result) return [];
    return [30,40,50,60,70,80,90,100]
      .filter(m => m > result.years)
      .slice(0,3)
      .map(m => ({ age: m, yearsToGo: m - result.years }));
  }, [result]);

  // P3: Fun stats
  const funStats = useMemo(() => {
    if (!result) return null;
    const fullMoons = Math.floor(result.totalDays / 29.53);
    const breaths = Math.floor(result.totalMinutes * 15);
    return { fullMoons, breaths };
  }, [result]);

  return (
    <div class="space-y-4">
      <div>
        <label class="mb-1 block text-sm font-medium text-slate-700">
          Date of Birth
        </label>
        <input
          type="date"
          value={dob}
          max={today.toISOString().slice(0, 10)}
          onInput={(e) => setDob((e.target as HTMLInputElement).value)}
          class={inputCls}
          aria-label="Date of birth"
        />
      </div>

      {/* P2: Compare two dates toggle */}
      <div>
        <button
          type="button"
          onClick={() => setShowDiff((v) => !v)}
          class={`w-full rounded-lg border px-3 py-2 text-sm font-medium transition ${
            showDiff
              ? 'border-purple-300 bg-purple-50 text-purple-700'
              : 'border-slate-200 bg-slate-50 text-slate-600 hover:bg-slate-100'
          }`}
        >
          {showDiff ? 'Hide' : 'Compare two dates'}
        </button>
        {showDiff && (
          <div class="mt-2">
            <label class="mb-1 block text-sm font-medium text-slate-700">
              Second Date
            </label>
            <input
              type="date"
              value={dob2}
              onInput={(e) => setDob2((e.target as HTMLInputElement).value)}
              class={inputCls}
              aria-label="Second date of birth"
            />
            {ageDiff && (
              <div class="mt-2 rounded-lg border border-purple-200 bg-purple-50 px-3 py-2 text-sm text-purple-800">
                <span class="font-semibold">{ageDiff.diffYears} years, {ageDiff.diffMonths} months apart</span>
                <span class="ml-1 text-purple-600">({ageDiff.diffDays.toLocaleString()} days)</span>
              </div>
            )}
          </div>
        )}
      </div>

      {result && (
        <div role="status" aria-live="polite" class="space-y-3 rounded-xl border border-brand/30 bg-green-50 p-4">
          <div class="flex items-baseline justify-between">
            <div>
              <span class="text-4xl font-bold tabular-nums text-brand">{result.years}</span>
              <span class="ml-1.5 text-lg font-semibold text-slate-700">
                years{result.months > 0 ? `, ${result.months} months` : ''}
                {result.days > 0 ? `, ${result.days} days` : ''}
              </span>
            </div>
          </div>

          <div class="h-px bg-slate-200" />

          <div class="grid grid-cols-2 gap-2 text-sm">
            <div>
              <div class="text-slate-500">Total Days</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalDays.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Weeks</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalWeeks.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Hours</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalHours.toLocaleString()}
              </div>
            </div>
            <div>
              <div class="text-slate-500">Total Minutes</div>
              <div class="font-semibold tabular-nums text-slate-900">
                {result.totalMinutes.toLocaleString()}
              </div>
            </div>
          </div>

          {result.daysToNextBirthday > 0 && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="flex items-center gap-2 text-sm">
                <span class="text-slate-500">Next birthday in</span>
                <span class="font-semibold text-brand">
                  {result.daysToNextBirthday === 1 ? 'tomorrow!' : `${result.daysToNextBirthday} days`}
                </span>
              </div>
            </>
          )}

          {/* P2: Milestone countdown */}
          {milestones.length > 0 && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="flex flex-wrap gap-2">
                {milestones.map((m) => (
                  <span
                    key={m.age}
                    class="rounded-full border border-green-200 bg-white px-3 py-1 text-xs font-medium text-slate-700"
                  >
                    Turns {m.age} in {m.yearsToGo} {m.yearsToGo === 1 ? 'year' : 'years'}
                  </span>
                ))}
              </div>
            </>
          )}

          {/* P3: Fun stats */}
          {funStats && (
            <>
              <div class="h-px bg-slate-200" />
              <div class="grid grid-cols-2 gap-2 text-sm">
                <div class="rounded-lg bg-white border border-slate-200 p-2.5 text-center">
                  <div class="font-bold tabular-nums text-slate-800">~{funStats.fullMoons.toLocaleString()}</div>
                  <div class="text-xs text-slate-500 mt-0.5">full moons</div>
                </div>
                <div class="rounded-lg bg-white border border-slate-200 p-2.5 text-center">
                  <div class="font-bold tabular-nums text-slate-800">~{funStats.breaths.toLocaleString()}</div>
                  <div class="text-xs text-slate-500 mt-0.5">breaths taken</div>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Results are calculated based on your local system date.
      </p>
    </div>
  );
}
