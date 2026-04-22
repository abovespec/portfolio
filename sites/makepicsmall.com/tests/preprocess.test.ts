import { describe, it, expect } from 'vitest';
import { computeOutputDims } from '../src/lib/preprocess';

describe('computeOutputDims', () => {
  it('passes through when no constraints', () => {
    expect(computeOutputDims(1000, 800, {})).toEqual({ w: 1000, h: 800, cropSrc: null });
  });
  it('downscales by maxLongSide preserving aspect', () => {
    expect(computeOutputDims(4000, 3000, { maxLongSide: 1080 })).toEqual({
      w: 1080, h: 810, cropSrc: null,
    });
  });
  it('no upscale when image already smaller than maxLongSide', () => {
    expect(computeOutputDims(800, 600, { maxLongSide: 1080 })).toEqual({
      w: 800, h: 600, cropSrc: null,
    });
  });
  it('center-crops then resizes for lockDimensions (square from wide)', () => {
    const r = computeOutputDims(1200, 800, { lockDimensions: { w: 600, h: 600 } });
    expect(r.w).toBe(600);
    expect(r.h).toBe(600);
    expect(r.cropSrc).toEqual({ x: 200, y: 0, w: 800, h: 800 });
  });
  it('center-crops to portrait lock (420x540 from square)', () => {
    const r = computeOutputDims(1000, 1000, { lockDimensions: { w: 420, h: 540 } });
    expect(r.w).toBe(420);
    expect(r.h).toBe(540);
    expect(r.cropSrc?.w).toBe(778);
    expect(r.cropSrc?.h).toBe(1000);
    expect(r.cropSrc?.x).toBe(111);
    expect(r.cropSrc?.y).toBe(0);
  });
});
