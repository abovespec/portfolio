/** @jsxImportSource preact */
import { useCallback, useRef, useState } from 'preact/hooks';
import type { Preset } from '../../config/presets';

interface Props {
  preset: Preset;
  onFiles: (files: File[]) => void;
}

export function DropZone({ preset, onFiles }: Props) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const files = Array.from(e.dataTransfer?.files ?? []);
    if (files.length) onFiles(files);
  }, [onFiles]);

  return (
    <div
      class={`rounded-xl border-2 border-dashed p-8 text-center transition ${
        dragging ? 'border-[var(--site-accent-color)] bg-[var(--surface)]' : 'border-[var(--border)]'
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
    >
      <p class="text-lg font-medium text-[var(--ink)]">{preset.label ?? 'Drop images to compress'}</p>
      <p class="mt-2 text-sm text-[var(--muted)]">
        or click to pick files · JPG, PNG, WebP up to 50 MB each
      </p>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        multiple
        class="hidden"
        onChange={(e) => {
          const files = Array.from((e.currentTarget as HTMLInputElement).files ?? []);
          if (files.length) onFiles(files);
        }}
      />
    </div>
  );
}
