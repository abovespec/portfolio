import { describe, it, expect } from 'vitest';
import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';

describe('baseLayout build output', () => {
  it('renders siteConfig values, not placeholder tokens', () => {
    if (!existsSync('dist/index.html')) {
      execSync('pnpm build', { stdio: 'ignore' });
    }
    const html = readFileSync('dist/index.html', 'utf8');
    expect(html).not.toMatch(/__SITE_[A-Z_]+__/);
    expect(html).toContain('makepicsmall');
    expect(html).toContain('Free, instant image compression');
  });
});
