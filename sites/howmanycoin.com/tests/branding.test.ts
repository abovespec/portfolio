import { describe, it, expect } from 'vitest';
import { siteConfig } from '../src/config/site.config';

describe('howmanycoin branding', () => {
  it('uses cool off-white bg and deep ink-indigo accent', () => {
    expect(siteConfig.branding.themeColor).toBe('#f7f8fa');
    expect(siteConfig.branding.accentColor).toBe('#3730a3');
  });
  it('logoText matches domain identity', () => {
    expect(siteConfig.branding.logoText).toBe('howmanycoin');
  });
  it('description emphasises pair conversion and supply', () => {
    expect(siteConfig.identity.description.toLowerCase()).toMatch(/convert|supply|rate/);
  });
});
