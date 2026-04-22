/** @jsxImportSource preact */
import { useCallback, useEffect, useRef, useState } from 'preact/hooks';
import type { Preset } from '../../config/presets';

interface Props {
  preset: Preset;
  onFiles: (files: File[]) => void;
}

export function DropZone({ preset, onFiles }: Props) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  // Track dragging at the document level too — drop events can leave the
  // dragging state stuck in some browsers if dragleave fires on children.
  useEffect(() => {
    const cancel = () => setDragging(false);
    window.addEventListener('drop', cancel);
    window.addEventListener('dragend', cancel);
    return () => {
      window.removeEventListener('drop', cancel);
      window.removeEventListener('dragend', cancel);
    };
  }, []);

  const handleDrop = useCallback((e: DragEvent) => {
    e.preventDefault();
    setDragging(false);
    const files = Array.from(e.dataTransfer?.files ?? []);
    if (files.length) onFiles(files);
  }, [onFiles]);

  const handleInputChange = useCallback((e: Event) => {
    const input = e.currentTarget as HTMLInputElement;
    const files = Array.from(input.files ?? []);
    if (files.length) onFiles(files);
    // CRITICAL: reset value so re-selecting the same file (or picking more
    // files in a subsequent interaction) reliably fires onChange again.
    input.value = '';
  }, [onFiles]);

  return (
    <div
      class={`rounded-xl border-2 border-dashed p-8 text-center transition cursor-pointer ${
        dragging ? 'border-[var(--site-accent-color)] bg-[var(--surface)]' : 'border-[var(--border)]'
      }`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDragEnd={() => setDragging(false)}
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
        onChange={handleInputChange}
      />
    </div>
  );
}
