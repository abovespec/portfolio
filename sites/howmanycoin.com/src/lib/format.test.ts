import { describe, it, expect } from 'vitest';
import { formatRate, formatPct, formatSupply, formatUsd } from './format';

describe('formatters', () => {
  it('formats small rates with 6 sig figs', () => {
    expect(formatRate(0.000012345)).toBe('0.0000123');
    expect(formatRate(1234.5678)).toBe('1,234.57');
    expect(formatRate(1.2345678)).toBe('1.23457');
  });
  it('formats percent with sign', () => {
    expect(formatPct(0.0234)).toBe('+2.34%');
    expect(formatPct(-0.0056)).toBe('-0.56%');
    expect(formatPct(0)).toBe('0.00%');
  });
  it('formats supply with thousands separators', () => {
    expect(formatSupply(21000000)).toBe('21,000,000');
    expect(formatSupply('uncapped')).toBe('Uncapped');
  });
  it('formats USD with symbol', () => {
    expect(formatUsd(1234.56)).toBe('$1,234.56');
    expect(formatUsd(0.045)).toBe('$0.045');
  });
});
