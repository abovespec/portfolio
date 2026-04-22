import { describe, it, expect } from 'vitest';
import { siteConfig } from '../src/config/site.config';

describe('branding', () => {
  it('uses coral accent on warm off-white background', () => {
    expect(siteConfig.branding.themeColor).toBe('#fffdf8');
    expect(siteConfig.branding.accentColor).toBe('#ff6b52');
  });
  it('logo text matches domain identity', () => {
    expect(siteConfig.branding.logoText).toBe('makepicsmall');
  });
});
