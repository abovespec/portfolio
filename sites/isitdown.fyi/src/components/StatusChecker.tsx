import { useEffect, useState, useCallback } from 'preact/hooks';

type Status = 'checking' | 'up' | 'down' | 'error';
type GHWorstStatus = 'operational' | 'degraded_performance' | 'partial_outage' | 'major_outage';

interface Props {
  domain: string;
}

const GH_STATUS_LABELS: Record<GHWorstStatus, string> = {
  operational: 'Operational',
  degraded_performance: 'Degraded Performance',
  partial_outage: 'Partial Outage',
  major_outage: 'Major Outage',
};

const GH_STATUS_COLORS: Record<GHWorstStatus, { bg: string; border: string; text: string; dot: string }> = {
  operational: { bg: 'bg-emerald-50', border: 'border-emerald-100', text: 'text-emerald-700', dot: 'bg-emerald-500' },
  degraded_performance: { bg: 'bg-yellow-50', border: 'border-yellow-100', text: 'text-yellow-700', dot: 'bg-yellow-400' },
  partial_outage: { bg: 'bg-orange-50', border: 'border-orange-100', text: 'text-orange-700', dot: 'bg-orange-500' },
  major_outage: { bg: 'bg-red-50', border: 'border-red-100', text: 'text-red-700', dot: 'bg-red-500' },
};

export default function StatusChecker({ domain }: Props) {
  const [status, setStatus] = useState<Status>('checking');
  const [responseTime, setResponseTime] = useState<number | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  // GitHub status
  const [githubStatus, setGithubStatus] = useState<GHWorstStatus | null>(null);
  const [githubChecking, setGithubChecking] = useState(false);

  const fetchGitHubStatus = useCallback(() => {
    setGithubChecking(true);
    fetch('https://www.githubstatus.com/api/v2/components.json')
      .then(r => r.json())
      .then((data: { components: { status: string }[] }) => {
        const all = data.components || [];
        const worst: GHWorstStatus = all.some((c) => c.status === 'major_outage') ? 'major_outage'
          : all.some((c) => c.status === 'partial_outage') ? 'partial_outage'
          : all.some((c) => c.status === 'degraded_performance') ? 'degraded_performance'
          : 'operational';
        setGithubStatus(worst);
      })
      .catch(() => setGithubStatus(null))
      .finally(() => setGithubChecking(false));
  }, []);

  const checkDomain = useCallback(() => {
    setStatus('checking');
    setLastChecked(null);
    fetch(`/api/check?url=${encodeURIComponent(domain)}`)
      .then((r) => r.json())
      .then((data: { up: boolean; statusCode: number | null; responseTime: number }) => {
        setStatus(data.up ? 'up' : 'down');
        setResponseTime(data.responseTime);
        setStatusCode(data.statusCode);
        setLastChecked(new Date());
      })
      .catch(() => {
        setStatus('error');
        setLastChecked(new Date());
      });
  }, [domain]);

  useEffect(() => {
    checkDomain();
    fetchGitHubStatus();
  }, [checkDomain, fetchGitHubStatus]);

  const ghColors = githubStatus ? GH_STATUS_COLORS[githubStatus] : null;

  return (
    <div class="space-y-3">
      {/* Domain check result */}
      {status === 'checking' ? (
        <div class="rounded-lg bg-slate-50 border border-slate-200 px-4 py-2">
          <span class="inline-flex items-center gap-2 text-slate-500 font-medium">
            <span class="w-3 h-3 rounded-full bg-slate-300 animate-pulse" />
            Checking…
          </span>
        </div>
      ) : status === 'up' ? (
        <div class="rounded-lg bg-emerald-50 border border-emerald-100 px-4 py-2">
          <span class="inline-flex items-center gap-2 text-emerald-700 font-bold">
            <span class="w-3 h-3 rounded-full bg-emerald-500" />
            Up
          </span>
          {responseTime !== null && (
            <p class="mt-1 text-xs text-emerald-600">
              {statusCode !== null ? `HTTP ${statusCode} · ` : ''}
              {responseTime}ms response time
            </p>
          )}
        </div>
      ) : (
        <div class="rounded-lg bg-red-50 border border-red-100 px-4 py-2">
          <span class="inline-flex items-center gap-2 text-red-700 font-bold">
            <span class="w-3 h-3 rounded-full bg-red-500" />
            May be down
          </span>
          <p class="mt-1 text-xs text-red-600">
            {status === 'error'
              ? 'Could not perform check'
              : `No response after ${responseTime ?? '—'}ms`}
          </p>
        </div>
      )}

      {/* Last checked + refresh */}
      <div class="flex items-center justify-between text-xs text-slate-400">
        <span>
          {lastChecked
            ? `Last checked: ${lastChecked.toLocaleTimeString()}`
            : status === 'checking' ? 'Checking now…' : ''}
        </span>
        <button
          type="button"
          onClick={() => { checkDomain(); fetchGitHubStatus(); }}
          disabled={status === 'checking'}
          class="flex items-center gap-1 text-xs text-slate-500 hover:text-slate-800 disabled:opacity-40 font-medium"
        >
          <svg class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
      </div>

      {/* GitHub real status */}
      {(githubChecking || githubStatus !== null) && (
        <div class="mt-2">
          <p class="text-xs font-semibold text-slate-500 uppercase mb-1">GitHub Status (Live)</p>
          {githubChecking && !githubStatus ? (
            <div class="rounded-lg bg-slate-50 border border-slate-200 px-3 py-2 text-xs text-slate-400">
              Fetching GitHub status…
            </div>
          ) : githubStatus && ghColors ? (
            <div class={`rounded-lg ${ghColors.bg} border ${ghColors.border} px-3 py-2`}>
              <span class={`inline-flex items-center gap-2 text-sm font-bold ${ghColors.text}`}>
                <span class={`w-2.5 h-2.5 rounded-full ${ghColors.dot}`} />
                {GH_STATUS_LABELS[githubStatus]}
              </span>
              <p class="mt-0.5 text-xs text-slate-500">
                Source: githubstatus.com API ·{' '}
                <a href="https://www.githubstatus.com/" target="_blank" rel="noopener noreferrer" class="underline hover:text-slate-700">View status page</a>
              </p>
            </div>
          ) : (
            <div class="rounded-lg bg-slate-50 border border-slate-200 px-3 py-2 text-xs text-slate-400">
              GitHub status unavailable
            </div>
          )}
        </div>
      )}
    </div>
  );
}
