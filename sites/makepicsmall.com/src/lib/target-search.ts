export interface TargetSearchOptions {
  targetKB: number;
  encode: (quality: number) => Promise<Uint8Array>;
  qualityFloor?: number;
  qualityCeiling?: number;
  tolerancePct?: number;
  maxIterations?: number;
  initialQuality?: number;
}

export interface TargetSearchResult {
  quality: number;
  bytes: Uint8Array;
  size: number;
  hitTarget: boolean;
  attempts: number;
}

/**
 * Binary-search for the highest quality value whose encoded output is
 * within `tolerancePct` of `targetKB`. If unreachable, returns the
 * encoded result closest to target (capped at ceiling/floor).
 */
export async function searchQualityForTarget(opts: TargetSearchOptions): Promise<TargetSearchResult> {
  const {
    targetKB,
    encode,
    qualityFloor = 20,
    qualityCeiling = 95,
    tolerancePct = 5,
    maxIterations = 8,
    initialQuality = 80,
  } = opts;

  const targetBytes = targetKB * 1024;
  const toleranceBytes = targetBytes * (tolerancePct / 100);

  let lo = qualityFloor;
  let hi = qualityCeiling;
  let bestBytes: Uint8Array | null = null;
  let bestQuality = initialQuality;
  let bestDelta = Infinity;
  let attempts = 0;
  let q = Math.min(Math.max(initialQuality, qualityFloor), qualityCeiling);

  while (attempts < maxIterations && lo <= hi) {
    attempts++;
    const bytes = await encode(q);
    const size = bytes.byteLength;
    const delta = Math.abs(size - targetBytes);
    if (delta < bestDelta) {
      bestDelta = delta;
      bestBytes = bytes;
      bestQuality = q;
    }
    if (delta <= toleranceBytes) break;
    if (size > targetBytes) hi = q - 1;
    else lo = q + 1;
    q = Math.round((lo + hi) / 2);
  }

  const finalBytes = bestBytes ?? new Uint8Array();
  const size = finalBytes.byteLength;
  const hitTarget = Math.abs(size - targetBytes) <= toleranceBytes;
  return { quality: bestQuality, bytes: finalBytes, size, hitTarget, attempts };
}
