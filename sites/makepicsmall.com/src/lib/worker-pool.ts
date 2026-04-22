import type { CompressInput, CompressResult } from './compress';

export interface PoolJob {
  id: string;
  input: CompressInput;
}

export interface PoolResult {
  id: string;
  ok: boolean;
  result?: CompressResult;
  error?: string;
}

interface PendingJob {
  job: PoolJob;
  resolve: (r: PoolResult) => void;
}

export interface WorkerPoolOptions {
  size: number;
  createWorker: () => Worker;
}

interface Slot {
  worker: Worker;
  busy: boolean;
}

export class WorkerPool {
  private slots: Slot[];
  private queue: PendingJob[] = [];
  private pending = new Map<string, (r: PoolResult) => void>();

  constructor(opts: WorkerPoolOptions) {
    this.slots = Array.from({ length: opts.size }, () => {
      const worker = opts.createWorker();
      worker.onmessage = (ev: MessageEvent<PoolResult>) => this.onWorkerMessage(ev.data, worker);
      return { worker, busy: false };
    });
  }

  run(job: PoolJob): Promise<PoolResult> {
    return new Promise((resolve) => {
      const free = this.slots.find((s) => !s.busy);
      if (free) {
        free.busy = true;
        this.dispatch(free, { job, resolve });
      } else {
        this.queue.push({ job, resolve });
      }
    });
  }

  destroy(): void {
    for (const s of this.slots) s.worker.terminate();
    this.slots = [];
    this.queue = [];
    this.pending.clear();
  }

  private dispatch(slot: Slot, pending: PendingJob): void {
    this.pending.set(pending.job.id, pending.resolve);
    slot.worker.postMessage({ id: pending.job.id, input: pending.job.input });
  }

  private onWorkerMessage(data: PoolResult, worker: Worker): void {
    const resolve = this.pending.get(data.id);
    this.pending.delete(data.id);
    resolve?.(data);
    // Free this worker's slot, take next from queue.
    const slot = this.slots.find((s) => s.worker === worker);
    if (!slot) return;
    const next = this.queue.shift();
    if (next) this.dispatch(slot, next);
    else slot.busy = false;
  }
}

export function computePoolSize(): number {
  const cores = (typeof navigator !== 'undefined' && navigator.hardwareConcurrency) || 2;
  return Math.min(3, Math.max(1, cores));
}
