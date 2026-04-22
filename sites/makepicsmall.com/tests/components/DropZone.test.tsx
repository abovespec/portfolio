import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/preact';
import { DropZone } from '../../src/components/tool/DropZone';

describe('DropZone', () => {
  it('renders with preset label', () => {
    render(<DropZone preset={{ format: 'jpg', targetKB: 100, label: 'Compress JPG to 100 KB' }} onFiles={() => {}} />);
    expect(screen.getByText(/compress jpg to 100 kb/i)).toBeTruthy();
  });
  it('shows the accepted formats hint', () => {
    render(<DropZone preset={{ format: 'auto' }} onFiles={() => {}} />);
    expect(screen.getByText(/jpg, png, webp/i)).toBeTruthy();
  });
});
