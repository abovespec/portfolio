/// <reference lib="webworker" />
import { compressOne, type CompressInput } from '../lib/compress';

self.addEventListener('message', async (event: MessageEvent<{ id: string; input: CompressInput }>) => {
  const { id, input } = event.data;
  try {
    const result = await compressOne(input);
    (self as unknown as DedicatedWorkerGlobalScope).postMessage({ id, ok: true, result });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    (self as unknown as DedicatedWorkerGlobalScope).postMessage({ id, ok: false, error: message });
  }
});

export {};
