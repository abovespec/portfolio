import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/preact';
import { FileRow } from '../../src/components/tool/FileRow';

describe('FileRow', () => {
  const baseFile = new File([new Uint8Array(500_000)], 'photo.jpg', { type: 'image/jpeg' });

  it('shows queued state', () => {
    render(<FileRow file={baseFile} state={{ kind: 'queued' }} onDownload={() => {}} />);
    expect(screen.getByText(/queued/i)).toBeTruthy();
    expect(screen.getByText('photo.jpg')).toBeTruthy();
  });
  it('shows done state with savings', () => {
    render(
      <FileRow
        file={baseFile}
        state={{
          kind: 'done',
          compressedSize: 150_000,
          blob: new Blob([new Uint8Array(150_000)]),
          hitTarget: true,
        }}
        onDownload={() => {}}
      />
    );
    expect(screen.getByText(/70% smaller/i)).toBeTruthy();
  });
  it('shows warning when target not hit', () => {
    render(
      <FileRow
        file={baseFile}
        state={{ kind: 'done', compressedSize: 450_000, blob: new Blob(), hitTarget: false }}
        onDownload={() => {}}
      />
    );
    expect(screen.getByText(/close to target/i)).toBeTruthy();
  });
});
