import { createCanvas } from '@napi-rs/canvas';
import { writeFileSync } from 'fs';

const c = createCanvas(2, 2);
const ctx = c.getContext('2d');
ctx.fillStyle = '#fff'; ctx.fillRect(0, 0, 2, 2);
writeFileSync('tests/fixtures/tiny-jpg.jpg', c.toBuffer('image/jpeg'));
writeFileSync('tests/fixtures/tiny-png.png', c.toBuffer('image/png'));
writeFileSync('tests/fixtures/tiny-webp.webp', c.toBuffer('image/webp'));
console.log('Fixtures generated.');
