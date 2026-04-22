import type { Preset } from '../config/presets';
import { detectFormat, type DetectedFormat } from './detect-format';
import { computeOutputDims } from './preprocess';
import { searchQualityForTarget } from './target-search';

export interface CompressInput {
  file: File;
  preset: Preset;
}

export interface CompressResult {
  format: DetectedFormat;
  originalSize: number;
  compressedSize: number;
  quality: number;
  blob: Blob;
  elapsedMs: number;
  hitTarget: boolean;
  attempts: number;
}

export async function compressOne(input: CompressInput): Promise<CompressResult> {
  const t0 = performance.now();
  const inputFormat = await detectFormat(input.file);
  if (inputFormat === 'unsupported') throw new Error('Unsupported file format');

  const outputFormat = input.preset.format === 'auto' ? inputFormat : input.preset.format;

  const bitmap = await createImageBitmap(input.file);
  try {
    const dims = computeOutputDims(bitmap.width, bitmap.height, input.preset);
    const canvas = new OffscreenCanvas(dims.w, dims.h);
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Could not get 2D canvas context');
    if (dims.cropSrc) {
      ctx.drawImage(bitmap, dims.cropSrc.x, dims.cropSrc.y, dims.cropSrc.w, dims.cropSrc.h, 0, 0, dims.w, dims.h);
    } else {
      ctx.drawImage(bitmap, 0, 0, dims.w, dims.h);
    }
    const imageData = ctx.getImageData(0, 0, dims.w, dims.h);

    const encode = async (quality: number): Promise<Uint8Array> => {
      if (outputFormat === 'jpg') {
        const m = await import('@jsquash/jpeg');
        return new Uint8Array(await m.encode(imageData, { quality }));
      }
      if (outputFormat === 'webp') {
        const m = await import('@jsquash/webp');
        return new Uint8Array(await m.encode(imageData, { quality }));
      }
      if (outputFormat === 'png') {
        const m = await import('@jsquash/png');
        // PNG is lossless; quality param is ignored.
        void quality;
        const encoded = await m.encode(imageData);
        return new Uint8Array(encoded);
      }
      throw new Error(`Unsupported output format: ${outputFormat}`);
    };

    let bytes: Uint8Array;
    let quality = input.preset.initialQuality ?? 80;
    let hitTarget = true;
    let attempts = 1;

    if (input.preset.targetKB) {
      const result = await searchQualityForTarget({
        targetKB: input.preset.targetKB,
        encode,
        initialQuality: quality,
      });
      bytes = result.bytes;
      quality = result.quality;
      hitTarget = result.hitTarget;
      attempts = result.attempts;
    } else {
      bytes = await encode(quality);
    }

    const mime = outputFormat === 'jpg' ? 'image/jpeg' : outputFormat === 'png' ? 'image/png' : 'image/webp';
    // Blob requires BlobPart; pass the ArrayBuffer slice.
    const blob = new Blob(
      [bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer],
      { type: mime },
    );

    return {
      format: outputFormat as DetectedFormat,
      originalSize: input.file.size,
      compressedSize: blob.size,
      quality,
      blob,
      elapsedMs: performance.now() - t0,
      hitTarget,
      attempts,
    };
  } finally {
    // Always release the ImageBitmap's memory, even on error paths.
    // Forgetting this is a classic cause of "works once, fails after a couple runs"
    // bugs on memory-constrained devices (mobile Safari, older Chromebooks).
    if (typeof bitmap.close === 'function') {
      try { bitmap.close(); } catch { /* noop */ }
    }
  }
}
