import { describe, it, expect } from 'vitest';
import { readFileSync } from 'fs';
import { detectFormat } from '../src/lib/detect-format';

function loadAsBlob(path: string, mime: string): Blob {
  const buf = readFileSync(path);
  return new Blob([buf], { type: mime });
}

describe('detectFormat', () => {
  it('detects JPG by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-jpg.jpg', 'image/jpeg');
    expect(await detectFormat(b)).toBe('jpg');
  });
  it('detects PNG by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-png.png', 'image/png');
    expect(await detectFormat(b)).toBe('png');
  });
  it('detects WebP by magic bytes', async () => {
    const b = loadAsBlob('tests/fixtures/tiny-webp.webp', 'image/webp');
    expect(await detectFormat(b)).toBe('webp');
  });
  it('returns unsupported for a text blob', async () => {
    const b = new Blob(['hello world'], { type: 'text/plain' });
    expect(await detectFormat(b)).toBe('unsupported');
  });
});
