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

  const result = useMemo(() => calcAge(dob), [dob]);

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
        </div>
      )}

      <p class="text-xs leading-relaxed text-slate-500">
        Results are calculated based on your local system date.
      </p>
    </div>
  );
}
