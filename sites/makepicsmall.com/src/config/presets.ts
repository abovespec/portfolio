export type Format = 'jpg' | 'png' | 'webp' | 'auto';

export interface Preset {
  /** Output format. 'auto' preserves input format. */
  format: Format;
  /** Hard target size in KB. If set, triggers quality binary search. */
  targetKB?: number;
  /** Initial quality 1-100. Default 80. */
  initialQuality?: number;
  /** If set, downscale so longest side ≤ this value (px). */
  maxLongSide?: number;
  /** If set, center-crop and resize to these exact dimensions. */
  lockDimensions?: { w: number; h: number };
  /** Short human-readable label for UI. */
  label?: string;
}

/**
 * URL → Preset mapping. Must stay in sync with the routes we ship.
 * When adding a new URL, also add a page file under src/pages/.
 */
export const PRESETS: Record<string, Preset> = {
  '/': { format: 'auto', label: 'Compress any image' },

  '/compress/jpg': { format: 'jpg', label: 'Compress JPG' },
  '/compress/png': { format: 'png', label: 'Compress PNG' },
  '/compress/webp': { format: 'webp', label: 'Compress WebP' },

  '/compress/jpg/to/100kb': { format: 'jpg', targetKB: 100, label: 'Compress JPG to 100 KB' },
  '/compress/jpg/to/500kb': { format: 'jpg', targetKB: 500, label: 'Compress JPG to 500 KB' },
  '/compress/png/to/100kb': { format: 'png', targetKB: 100, label: 'Compress PNG to 100 KB' },

  '/to/50kb':  { format: 'auto', targetKB: 50,   label: 'Compress to 50 KB' },
  '/to/100kb': { format: 'auto', targetKB: 100,  label: 'Compress to 100 KB' },
  '/to/500kb': { format: 'auto', targetKB: 500,  label: 'Compress to 500 KB' },
  '/to/1mb':   { format: 'auto', targetKB: 1000, label: 'Compress to 1 MB' },

  '/for/whatsapp':         { format: 'jpg', targetKB: 1500, maxLongSide: 1600, label: 'For WhatsApp (full quality)' },
  '/for/whatsapp-dp':      { format: 'jpg', targetKB: 100,  lockDimensions: { w: 640, h: 640 },   label: 'For WhatsApp DP' },
  '/for/instagram':        { format: 'jpg', targetKB: 500,  maxLongSide: 1080, label: 'For Instagram' },
  '/for/instagram-story':  { format: 'jpg', targetKB: 600,  lockDimensions: { w: 1080, h: 1920 }, label: 'For Instagram Story' },
  '/for/resume':           { format: 'jpg', targetKB: 100,  lockDimensions: { w: 600, h: 600 },   label: 'For Resume Photo' },
  '/for/passport-us':      { format: 'jpg', targetKB: 240,  lockDimensions: { w: 600, h: 600 },   label: 'For US Passport Photo' },
  '/for/passport-canada':  { format: 'jpg', targetKB: 240,  lockDimensions: { w: 420, h: 540 },   label: 'For Canadian Passport Photo' },
  '/for/passport-uk':      { format: 'jpg', targetKB: 1000, lockDimensions: { w: 600, h: 750 },   label: 'For UK Passport Photo' },
  '/for/linkedin':         { format: 'jpg', targetKB: 200,  lockDimensions: { w: 400, h: 400 },   label: 'For LinkedIn Profile' },
};

export function getPresetByUrl(url: string): Preset {
  // Strip trailing slash unless it's root
  const normalized = url === '/' ? url : url.replace(/\/$/, '');
  return PRESETS[normalized] ?? PRESETS['/'];
}
