---
title: "How to Minify CSS: Every Method Explained"
description: "Minify CSS files using online tools, build tools (webpack, Vite, Gulp), npm packages (cssnano, clean-css), and CLI commands. Covers all major workflows."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["css", "minification", "web performance", "build tools", "optimization"]
draft: false
---

CSS minification removes whitespace, comments, and redundant characters from your stylesheets without changing what they do. A minified CSS file can be 20–80% smaller, reducing page load time and bandwidth costs.

## What minification does

A minifier performs several transformations:

- **Removes whitespace** — indentation, line breaks, spaces around colons and braces
- **Removes comments** — `/* ... */` blocks
- **Shortens values** — `#ffffff` → `#fff`, `0px` → `0`, `0.5` → `.5`
- **Merges duplicate rules** — combines selectors with identical declarations
- **Removes redundant properties** — last declaration wins in cascade; earlier duplicates removed
- **Shortens `font`, `margin`, `padding`** — expands shorthand, removes defaults

Before:
```css
/* Main button styles */
.button {
    display: inline-block;
    padding: 12px 24px;
    background-color: #0066ff;
    color: #ffffff;
    border-radius: 4px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
}
```

For more on this topic, see [*How to Remove Unused CSS: PurgeCSS, UnCSS, and Tree-Shaking*](/blog/remove-unused-css).

After:
```css
.button{display:inline-block;padding:12px 24px;background-color:#06f;color:#fff;border-radius:4px;font-size:16px;font-weight:600;cursor:pointer}
```

For more on this topic, see [*CSS File Too Large? How to Diagnose and Fix It*](/blog/css-file-size-too-large).

## Method 1: Online minifier

For one-off files or quick checks, paste into [cssminify.io](/) — no installation required.

## Method 2: cssnano (recommended for most projects)

[cssnano](https://cssnano.github.io/cssnano/) is the most widely used CSS minifier. It's PostCSS-based and highly configurable.

```bash
npm install --save-dev cssnano postcss postcss-cli
```

Create `postcss.config.js`:

```js
module.exports = {
  plugins: [
    require('cssnano')({
      preset: 'default',
    }),
  ],
};
```

Run it:

```bash
npx postcss styles.css --output styles.min.css
```

## Method 3: Webpack (MiniCssExtractPlugin + CssMinimizerPlugin)

For webpack projects, add the CSS minimizer plugin:

For more on this topic, see [*Minify CSS in webpack, Vite, and Rollup*](/blog/minify-css-webpack).

```bash
npm install --save-dev css-minimizer-webpack-plugin mini-css-extract-plugin
```

```js
// webpack.config.js
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: 'production',
  plugins: [new MiniCssExtractPlugin({ filename: '[name].min.css' })],
  optimization: {
    minimizer: [
      '...',  // preserve JS minimizer
      new CssMinimizerPlugin(),
    ],
  },
};
```

CSS minification runs automatically in `mode: 'production'`.

## Method 4: Vite

Vite uses esbuild for CSS minification in production builds — it's enabled by default:

```bash
vite build
```

To configure:

```js
// vite.config.js
export default {
  build: {
    cssMinify: true,      // default true in production
    cssCodeSplit: true,   // split CSS per chunk
  },
};
```

For more aggressive minification (using lightningcss):

```bash
npm install --save-dev lightningcss
```

```js
export default {
  css: { transformer: 'lightningcss' },
  build: { cssMinify: 'lightningcss' },
};
```

## Method 5: clean-css CLI

```bash
npm install -g clean-css-cli

cleancss -o output.min.css input.css

# Multiple files merged into one
cleancss -o bundle.min.css file1.css file2.css file3.css

# Show compression statistics
cleancss --debug -o output.min.css input.css
```

## Method 6: Gulp

```bash
npm install --save-dev gulp gulp-clean-css gulp-rename
```

```js
// gulpfile.js
const { src, dest } = require('gulp');
const cleanCSS = require('gulp-clean-css');
const rename = require('gulp-rename');

function minifyCSS() {
  return src('src/css/*.css')
    .pipe(cleanCSS({ level: 2 }))
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest('dist/css'));
}

exports.default = minifyCSS;
```

## Source maps

Always generate source maps so you can debug minified CSS in browser DevTools:

```bash
# postcss with source map
npx postcss styles.css --output styles.min.css --map

# clean-css with source map
cleancss --source-map -o output.min.css input.css
```

Source maps let DevTools show the original file and line when you inspect an element, even though the browser is loading the minified version.

## Compression levels

Most minifiers offer compression levels:

- **Level 1** — safe transformations only (whitespace, comments, redundant semicolons)
- **Level 2** — structural optimizations (merging rules, removing overridden properties, shorthand optimization)

Level 2 is more aggressive and occasionally introduces bugs with complex CSS (especially with specificity-dependent overrides). Test thoroughly when enabling it.

```js
new CssMinimizerPlugin({
  minimizerOptions: {
    preset: ['default', { discardComments: { removeAll: true } }],
  },
})
```

## Check the result

After minifying, verify in DevTools that styles apply correctly — especially for complex selectors, media queries, and `@keyframes`. Then check the file size reduction:

```bash
ls -lh styles.css styles.min.css
```

Or use [cssminify.io](/) to paste and compare sizes directly.
