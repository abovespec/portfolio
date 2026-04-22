/** @jsxImportSource preact */

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
    <div class="flex items-center justify-between gap-4 rounded-lg border border-[var(--border)] bg-white px-4 py-3">
      <div class="min-w-0 flex-1">
        <div class="truncate text-sm font-medium text-[var(--ink)]">{file.name}</div>
        <div class={`mt-0.5 font-mono text-xs ${state.kind === 'error' ? 'text-[var(--warn)]' : 'text-[var(--muted)]'}`}>
          {humanBytes(file.size)} · {statusText}{targetNote}
        </div>
      </div>
      {state.kind === 'done' && (
        <button
          type="button"
          class="rounded-md bg-[var(--site-accent-color)] px-3 py-1.5 text-sm font-medium text-white hover:opacity-90"
          onClick={onDownload}
        >
          Download
        </button>
      )}
    </div>
  );
}
