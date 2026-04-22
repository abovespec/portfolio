/** @jsxImportSource preact */
import { useEffect, useRef, useState } from 'preact/hooks';
import type { Preset } from '../../config/presets';
import { DropZone } from './DropZone';
import { FileRow, type FileRowState } from './FileRow';
import type { CompressResult } from '../../lib/compress';
import { WorkerPool, computePoolSize } from '../../lib/worker-pool';

interface Props {
  preset: Preset;
}

interface Row {
  id: string;
  file: File;
  state: FileRowState;
  resultBlob?: Blob;
  outputName?: string;
}

const MAX_FILE_BYTES = 50 * 1024 * 1024;

// Allow ?target=200 URL override of targetKB.
function withUrlOverrides(preset: Preset): Preset {
  if (typeof window === 'undefined') return preset;
  const params = new URLSearchParams(window.location.search);
  const target = params.get('target');
  if (target) {
    const n = parseInt(target, 10);
    if (!Number.isNaN(n) && n > 0 && n < 100_000) {
      return { ...preset, targetKB: n };
    }
  }
  return preset;
}

export function Compressor({ preset: rawPreset }: Props) {
  const preset = withUrlOverrides(rawPreset);
  const [rows, setRows] = useState<Row[]>([]);
  const poolRef = useRef<WorkerPool | null>(null);

  useEffect(() => {
    return () => poolRef.current?.destroy();
  }, []);

  function ensurePool(): WorkerPool {
    if (poolRef.current) return poolRef.current;
    const pool = new WorkerPool({
      size: computePoolSize(),
      createWorker: () => new Worker(new URL('../../workers/compress.worker.ts', import.meta.url), { type: 'module' }),
    });
    poolRef.current = pool;
    return pool;
  }

  async function handleFiles(files: File[]) {
    const valid = files.filter((f) => {
      if (f.size > MAX_FILE_BYTES) return false;
      return /^image\/(jpeg|png|webp)$/.test(f.type);
    });
    const newRows: Row[] = valid.map((f, i) => ({
      id: `${Date.now()}-${i}-${f.name}`,
      file: f,
      state: { kind: 'queued' },
    }));
    setRows((prev) => [...prev, ...newRows]);

    const pool = ensurePool();
    for (const row of newRows) {
      setRows((prev) => prev.map((r) => (r.id === row.id ? { ...r, state: { kind: 'processing' } } : r)));
      const result = await pool.run({
        id: row.id,
        input: { file: row.file, preset },
      });
      if (result.ok && result.result) {
        const r = result.result as CompressResult;
        const ext = r.format === 'jpg' ? 'jpg' : r.format === 'png' ? 'png' : 'webp';
        const base = row.file.name.replace(/\.[^.]+$/, '');
        setRows((prev) => prev.map((x) =>
          x.id === row.id
            ? { ...x, resultBlob: r.blob, outputName: `${base}.squished.${ext}`,
                state: { kind: 'done', compressedSize: r.compressedSize, blob: r.blob, hitTarget: r.hitTarget } }
            : x,
        ));
        // Plausible event (if available on window)
        const p = (window as unknown as { plausible?: (n: string, o: unknown) => void }).plausible;
        p?.('tool_completed', { props: { format: r.format, hitTarget: r.hitTarget } });
      } else {
        console.error('[Compressor] job failed', { id: row.id, file: row.file.name, error: result.error });
        setRows((prev) => prev.map((x) =>
          x.id === row.id ? { ...x, state: { kind: 'error', message: result.error ?? 'Unknown error' } } : x,
        ));
      }
    }
  }

  function download(row: Row) {
    if (!row.resultBlob || !row.outputName) return;
    const url = URL.createObjectURL(row.resultBlob);
    const a = document.createElement('a');
    a.href = url;
    a.download = row.outputName;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  return (
    <div class="space-y-4">
      <DropZone preset={preset} onFiles={handleFiles} />
      {rows.length > 0 && (
        <div class="space-y-2">
          {rows.map((r) => (
            <FileRow key={r.id} file={r.file} state={r.state} onDownload={() => download(r)} />
          ))}
        </div>
      )}
    </div>
  );
}
