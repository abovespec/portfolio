import { describe, it, expect } from 'vitest';
import { searchQualityForTarget } from '../src/lib/target-search';

describe('searchQualityForTarget', () => {
  // Simulated encoder: higher quality = bigger output. linear model for test.
  const fakeEncoder = async (quality: number) => {
    // bytes = quality * 1024 (so quality 50 = 50KB, quality 100 = 100KB)
    return new Uint8Array(quality * 1024);
  };

  it('finds quality within 5% of 50KB target', async () => {
    const { quality, size, hitTarget } = await searchQualityForTarget({
      targetKB: 50,
      encode: fakeEncoder,
      tolerancePct: 5,
      maxIterations: 8,
    });
    expect(quality).toBeGreaterThanOrEqual(47);
    expect(quality).toBeLessThanOrEqual(53);
    expect(hitTarget).toBe(true);
    expect(size).toBeGreaterThan(0);
  });

  it('caps iterations and returns best result if unreachable', async () => {
    // target 200KB but encoder max is 100KB (quality 100)
    const { quality, size, hitTarget, attempts } = await searchQualityForTarget({
      targetKB: 200,
      encode: fakeEncoder,
      tolerancePct: 5,
      maxIterations: 8,
    });
    expect(attempts).toBeLessThanOrEqual(8);
    expect(quality).toBe(95);
    expect(hitTarget).toBe(false);
  });

  it('never goes below floor or above ceiling', async () => {
    const { quality } = await searchQualityForTarget({
      targetKB: 1, // impossibly small
      encode: fakeEncoder,
      qualityFloor: 20,
      qualityCeiling: 95,
      maxIterations: 8,
    });
    expect(quality).toBeGreaterThanOrEqual(20);
    expect(quality).toBeLessThanOrEqual(95);
  });
});
