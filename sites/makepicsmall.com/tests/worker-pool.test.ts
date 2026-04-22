import { describe, it, expect } from 'vitest';
import { WorkerPool, type PoolJob } from '../src/lib/worker-pool';

// Fake worker that "completes" after microtask delay.
class FakeWorker {
  onmessage: ((ev: MessageEvent) => void) | null = null;
  postMessage(data: { id: string }) {
    queueMicrotask(() => {
      this.onmessage?.(new MessageEvent('message', { data: { id: data.id, ok: true, result: { fake: true } } }));
    });
  }
  terminate() {}
}

describe('WorkerPool', () => {
  it('runs jobs up to pool size concurrently', async () => {
    const pool = new WorkerPool({
      size: 2,
      createWorker: () => new FakeWorker() as unknown as Worker,
    });
    const jobs: PoolJob[] = [
      { id: '1', input: {} as never },
      { id: '2', input: {} as never },
      { id: '3', input: {} as never },
    ];
    const results = await Promise.all(jobs.map(j => pool.run(j)));
    expect(results.length).toBe(3);
    for (const r of results) expect(r.ok).toBe(true);
    pool.destroy();
  });

  it('caps concurrency at size', async () => {
    const order: string[] = [];
    class SlowWorker {
      onmessage: ((ev: MessageEvent) => void) | null = null;
      postMessage(data: { id: string }) {
        order.push(`start-${data.id}`);
        setTimeout(() => {
          order.push(`end-${data.id}`);
          this.onmessage?.(new MessageEvent('message', { data: { id: data.id, ok: true, result: {} } }));
        }, 10);
      }
      terminate() {}
    }
    const pool = new WorkerPool({ size: 1, createWorker: () => new SlowWorker() as unknown as Worker });
    await Promise.all([
      pool.run({ id: 'a', input: {} as never }),
      pool.run({ id: 'b', input: {} as never }),
    ]);
    expect(order).toEqual(['start-a', 'end-a', 'start-b', 'end-b']);
    pool.destroy();
  });
});
