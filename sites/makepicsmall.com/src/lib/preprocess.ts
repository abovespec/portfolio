import type { Preset } from '../config/presets';

export interface OutputDims {
  w: number;
  h: number;
  cropSrc: { x: number; y: number; w: number; h: number } | null;
}

export function computeOutputDims(
  srcW: number,
  srcH: number,
  preset: Pick<Preset, 'maxLongSide' | 'lockDimensions'>,
): OutputDims {
  if (preset.lockDimensions) {
    const tgtAspect = preset.lockDimensions.w / preset.lockDimensions.h;
    const srcAspect = srcW / srcH;
    let cropW: number, cropH: number, x: number, y: number;
    if (srcAspect > tgtAspect) {
      // source wider than target → crop horizontally
      cropH = srcH;
      cropW = Math.round(srcH * tgtAspect);
      x = Math.round((srcW - cropW) / 2);
      y = 0;
    } else if (srcAspect < tgtAspect) {
      // source taller than target → crop vertically
      cropW = srcW;
      cropH = Math.round(srcW / tgtAspect);
      x = 0;
      y = Math.round((srcH - cropH) / 2);
    } else {
      // same aspect, no crop
      cropW = srcW; cropH = srcH; x = 0; y = 0;
    }
    return {
      w: preset.lockDimensions.w,
      h: preset.lockDimensions.h,
      cropSrc: { x, y, w: cropW, h: cropH },
    };
  }

  if (preset.maxLongSide) {
    const long = Math.max(srcW, srcH);
    if (long > preset.maxLongSide) {
      const scale = preset.maxLongSide / long;
      return {
        w: Math.round(srcW * scale),
        h: Math.round(srcH * scale),
        cropSrc: null,
      };
    }
  }

  return { w: srcW, h: srcH, cropSrc: null };
}

/** Browser-only. Takes ImageBitmap, returns an ImageData ready for encoder. */
export function preprocess(
  bitmap: ImageBitmap,
  preset: Preset,
): ImageData {
  const dims = computeOutputDims(bitmap.width, bitmap.height, preset);
  const canvas = new OffscreenCanvas(dims.w, dims.h);
  const ctx = canvas.getContext('2d');
  if (!ctx) throw new Error('Could not get 2D context');

  if (dims.cropSrc) {
    ctx.drawImage(
      bitmap,
      dims.cropSrc.x, dims.cropSrc.y, dims.cropSrc.w, dims.cropSrc.h,
      0, 0, dims.w, dims.h,
    );
  } else {
    ctx.drawImage(bitmap, 0, 0, dims.w, dims.h);
  }

  return ctx.getImageData(0, 0, dims.w, dims.h);
}
