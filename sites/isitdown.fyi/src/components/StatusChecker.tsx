import { useEffect, useState } from 'preact/hooks';

type Status = 'checking' | 'up' | 'down' | 'error';

interface Props {
  domain: string;
}

export default function StatusChecker({ domain }: Props) {
  const [status, setStatus] = useState<Status>('checking');
  const [responseTime, setResponseTime] = useState<number | null>(null);
  const [statusCode, setStatusCode] = useState<number | null>(null);

  useEffect(() => {
    fetch(`/api/check?url=${encodeURIComponent(domain)}`)
      .then((r) => r.json())
      .then((data: { up: boolean; statusCode: number | null; responseTime: number }) => {
        setStatus(data.up ? 'up' : 'down');
        setResponseTime(data.responseTime);
        setStatusCode(data.statusCode);
      })
      .catch(() => setStatus('error'));
  }, [domain]);

  if (status === 'checking') {
    return (
      <div class="rounded-lg bg-slate-50 border border-slate-200 px-4 py-2">
        <span class="inline-flex items-center gap-2 text-slate-500 font-medium">
          <span class="w-3 h-3 rounded-full bg-slate-300 animate-pulse" />
          Checking…
        </span>
      </div>
    );
  }

  if (status === 'up') {
    return (
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
    );
  }

  return (
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
  );
}
