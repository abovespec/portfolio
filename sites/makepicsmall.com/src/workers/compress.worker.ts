/// <reference lib="webworker" />
import { compressOne, type CompressInput } from '../lib/compress';

const scope = self as unknown as DedicatedWorkerGlobalScope;

scope.addEventListener('message', async (event: MessageEvent<{ id: string; input: CompressInput }>) => {
  const { id, input } = event.data;
  try {
    const result = await compressOne(input);
    scope.postMessage({ id, ok: true, result });
  } catch (err) {
    const message = err instanceof Error ? err.message : String(err);
    // Also log with stack to the worker console so users can see it in DevTools.
    console.error('[compress.worker] job failed', { id, message, err });
    scope.postMessage({ id, ok: false, error: message });
  }
});

// Surface unhandled errors inside the worker (e.g. WASM init failures) so
// they're visible in DevTools and we can attribute them to the right file.
scope.addEventListener('error', (ev) => {
  console.error('[compress.worker] uncaught error', ev.message, ev.filename, ev.lineno);
});
scope.addEventListener('unhandledrejection', (ev) => {
  console.error('[compress.worker] unhandled promise rejection', ev.reason);
});

export {};
