import { createCanvas } from '@napi-rs/canvas';
import { writeFileSync } from 'fs';

const W = 1200, H = 630;
const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Background
ctx.fillStyle = '#fffdf8';
ctx.fillRect(0, 0, W, H);

// Coral accent band at top
ctx.fillStyle = '#ff6b52';
ctx.fillRect(0, 0, W, 8);

// Title
ctx.fillStyle = '#1a1a1a';
ctx.font = 'bold 96px sans-serif';
ctx.fillText('makepicsmall', 80, 300);

// Subtitle
ctx.fillStyle = '#5a5a5a';
ctx.font = '42px sans-serif';
ctx.fillText('Your photos. Smaller. Squished in your browser.', 80, 380);

// Domain
ctx.fillStyle = '#ff6b52';
ctx.font = '28px sans-serif';
ctx.fillText('makepicsmall.com', 80, 550);

writeFileSync('public/og-default.png', canvas.toBuffer('image/png'));
console.log('Wrote public/og-default.png');
