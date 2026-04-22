/** @jsxImportSource preact */
import { useEffect, useState } from 'preact/hooks';

export type FileRowState =
  | { kind: 'queued' }
  | { kind: 'processing' }
  | { kind: 'done'; compressedSize: number; blob: Blob; hitTarget: boolean }
  | { kind: 'error'; message: string };

interface Props {
  file: File;
  state: FileRowState;
  onDownload: () => void;
}

function humanBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(1)} MB`;
}

export function FileRow({ file, state, onDownload }: Props) {
  // Generate a thumbnail URL from the file once; release it on unmount.
  const [thumbUrl, setThumbUrl] = useState<string | null>(null);
  useEffect(() => {
    const url = URL.createObjectURL(file);
    setThumbUrl(url);
    return () => URL.revokeObjectURL(url);
  }, [file]);

  const statusText = (() => {
    switch (state.kind) {
      case 'queued': return 'queued';
      case 'processing': return 'squishing...';
      case 'done': {
        const saved = Math.round((1 - state.compressedSize / file.size) * 100);
        return `${saved}% smaller · ${humanBytes(state.compressedSize)}`;
      }
      case 'error': return state.message;
    }
  })();

  const targetNote = state.kind === 'done' && !state.hitTarget
    ? ' (close to target; cannot go smaller without heavier quality loss)'
    : '';

  return (
    <div class="flex items-center gap-3 rounded-lg border border-[var(--border)] bg-white px-3 py-2.5 sm:gap-4 sm:px-4 sm:py-3">
      {/* Thumbnail */}
      <div class="relative h-12 w-12 shrink-0 overflow-hidden rounded-md bg-[var(--surface)] sm:h-14 sm:w-14">
        {thumbUrl ? (
          <img
            src={thumbUrl}
            alt=""
            class="h-full w-full object-cover"
            loading="lazy"
            decoding="async"
          />
        ) : null}
        {state.kind === 'processing' && (
          <div class="absolute inset-0 flex items-center justify-center bg-black/30">
            <div class="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
          </div>
        )}
      </div>

      {/* Name + status */}
      <div class="min-w-0 flex-1">
        <div class="truncate text-sm font-medium text-[var(--ink)]" title={file.name}>{file.name}</div>
        <div class={`mt-0.5 font-mono text-xs ${state.kind === 'error' ? 'text-[var(--warn)]' : 'text-[var(--muted)]'}`}>
          {humanBytes(file.size)} · {statusText}{targetNote}
        </div>
      </div>

      {/* Download */}
      {state.kind === 'done' && (
        <button
          type="button"
          class="shrink-0 rounded-md bg-[var(--site-accent-color)] px-3 py-1.5 text-sm font-medium text-white hover:opacity-90"
          onClick={onDownload}
        >
          Download
        </button>
      )}
    </div>
  );
}
