---
title: "QR Code in HTML and JavaScript: Generate QR Codes in the Browser"
description: "Generate QR codes in HTML with JavaScript libraries: qrcode.js, QRCode.react, and the Canvas API. Includes examples for URL, WiFi, and vCard QR codes."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["qr code", "javascript", "html", "qrcode.js", "web development"]
draft: false
---

You can generate QR codes entirely in the browser using JavaScript — no server required. This guide covers the main libraries and patterns for embedding QR code generation in web pages.

## Option 1: qrcode.js (vanilla JS)

[qrcode.js](https://github.com/davidshimjs/qrcodejs) is a simple, dependency-free library that works in any browser.

For more on this topic, see [*QR Code for Website: Link Any Page to a Scannable Code*](/blog/qr-code-for-website).

**CDN setup:**

```html
<script src="https://cdn.jsdelivr.net/npm/qrcodejs/qrcode.min.js"></script>

<div id="qrcode"></div>

<script>
  new QRCode(document.getElementById("qrcode"), {
    text: "https://example.com",
    width: 256,
    height: 256,
    colorDark: "#000000",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M,
  });
</script>
```

For more on this topic, see [*QR Code for Business Card: vCard Setup and Best Practices*](/blog/qr-code-for-business-card).

**Generate from input:**

```html
<input type="text" id="url-input" placeholder="Enter URL" />
<button id="generate-btn">Generate</button>
<div id="qrcode"></div>

<script src="https://cdn.jsdelivr.net/npm/qrcodejs/qrcode.min.js"></script>
<script>
  let qr = null;

  document.getElementById('generate-btn').addEventListener('click', () => {
    const text = document.getElementById('url-input').value.trim();
    if (!text) return;

    const container = document.getElementById('qrcode');
    container.innerHTML = '';  // clear previous

    qr = new QRCode(container, {
      text,
      width: 256,
      height: 256,
      correctLevel: QRCode.CorrectLevel.H,
    });
  });
</script>
```

## Option 2: qrcode (Node.js / npm)

The `qrcode` npm package works in Node.js and in the browser via a bundler.

**Install:**
```bash
npm install qrcode
```

**Node.js — generate PNG file:**

```javascript
const QRCode = require('qrcode');

// Write to file
await QRCode.toFile('qrcode.png', 'https://example.com', {
  errorCorrectionLevel: 'M',
  type: 'image/png',
  scale: 8,
});

// Get as data URL (for embedding in HTML)
const dataUrl = await QRCode.toDataURL('https://example.com');
// → "data:image/png;base64,..."

// Get as SVG string
const svg = await QRCode.toString('https://example.com', { type: 'svg' });

// Render to canvas (browser)
await QRCode.toCanvas(canvasElement, 'https://example.com');
```

**Browser with bundler:**

```javascript
import QRCode from 'qrcode';

const canvas = document.getElementById('canvas');
await QRCode.toCanvas(canvas, 'https://example.com', {
  errorCorrectionLevel: 'H',
  color: {
    dark: '#000000',
    light: '#ffffff',
  },
});
```

## Option 3: QRCode.react (React)

For React applications, `qrcode.react` renders QR codes as SVG or canvas:

```bash
npm install qrcode.react
```

```jsx
import { QRCodeSVG, QRCodeCanvas } from 'qrcode.react';

function QRDemo() {
  return (
    <div>
      {/* SVG output (scales perfectly) */}
      <QRCodeSVG
        value="https://example.com"
        size={256}
        level="H"
        includeMargin={true}
      />

      {/* Canvas output */}
      <QRCodeCanvas
        value="https://example.com"
        size={256}
        level="M"
        bgColor="#ffffff"
        fgColor="#000000"
      />
    </div>
  );
}
```

**With logo in the center:**

```jsx
<QRCodeSVG
  value="https://example.com"
  size={256}
  level="H"
  imageSettings={{
    src: "/logo.png",
    x: undefined,
    y: undefined,
    height: 48,
    width: 48,
    excavate: true,  // clears modules under the logo
  }}
/>
```

## WiFi QR code format

```javascript
// WiFi QR code format string
function wifiQrString(ssid, password, security = 'WPA') {
  return `WIFI:T:${security};S:${ssid};P:${password};;`;
}

const qrText = wifiQrString('MyNetwork', 'MyPassword123', 'WPA');
// → "WIFI:T:WPA;S:MyNetwork;P:MyPassword123;;"
```

## vCard QR code

```javascript
function vCardString({ name, phone, email, url, company }) {
  return [
    'BEGIN:VCARD',
    'VERSION:3.0',
    `FN:${name}`,
    company ? `ORG:${company}` : '',
    phone ? `TEL:${phone}` : '',
    email ? `EMAIL:${email}` : '',
    url ? `URL:${url}` : '',
    'END:VCARD',
  ].filter(Boolean).join('\n');
}

const qrText = vCardString({
  name: 'Jane Smith',
  phone: '+15555551234',
  email: 'jane@example.com',
  url: 'https://janesmith.com',
  company: 'Acme Corp',
});
```

## Download as PNG

```javascript
function downloadQR(canvasElement, filename = 'qrcode.png') {
  const link = document.createElement('a');
  link.download = filename;
  link.href = canvasElement.toDataURL('image/png');
  link.click();
}

// Usage after generating to canvas
const canvas = document.getElementById('canvas');
await QRCode.toCanvas(canvas, 'https://example.com');
downloadQR(canvas);
```

## Styling with CSS

The QR code is usually a canvas or SVG element — style the container:

For more on this topic, see [*How to Create a QR Code: A Complete Beginner's Guide*](/blog/how-to-create-a-qr-code).

```css
.qr-container {
  display: inline-block;
  padding: 16px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.qr-container canvas,
.qr-container svg {
  display: block;
}
```

Generate QR codes online at [qrcodegen.io](/).
