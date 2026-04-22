import { describe, it, expect } from 'vitest';
import { PRESETS, getPresetByUrl, type Preset } from '../src/config/presets';

describe('presets', () => {
  it('has an entry for every MVP tool URL', () => {
    const expected = [
      '/', '/compress/jpg', '/compress/png', '/compress/webp',
      '/compress/jpg/to/100kb', '/compress/jpg/to/500kb', '/compress/png/to/100kb',
      '/to/50kb', '/to/100kb', '/to/500kb', '/to/1mb',
      '/for/whatsapp', '/for/whatsapp-dp', '/for/instagram', '/for/instagram-story',
      '/for/resume', '/for/passport-us', '/for/passport-canada', '/for/passport-uk',
      '/for/linkedin',
    ];
    for (const url of expected) {
      expect(PRESETS[url], `Missing preset: ${url}`).toBeDefined();
    }
    expect(Object.keys(PRESETS).length).toBe(20);
  });

  it('passport-us requires square 600x600 JPG ≤240KB', () => {
    const p = PRESETS['/for/passport-us'];
    expect(p.format).toBe('jpg');
    expect(p.targetKB).toBe(240);
    expect(p.lockDimensions).toEqual({ w: 600, h: 600 });
  });

  it('whatsapp-dp is 640x640 JPG ≤100KB', () => {
    const p = PRESETS['/for/whatsapp-dp'];
    expect(p.lockDimensions).toEqual({ w: 640, h: 640 });
    expect(p.targetKB).toBe(100);
  });

  it('getPresetByUrl returns preset or default for unknown URL', () => {
    expect(getPresetByUrl('/for/passport-us').targetKB).toBe(240);
    expect(getPresetByUrl('/unknown-url')).toEqual(PRESETS['/']);
  });
});
