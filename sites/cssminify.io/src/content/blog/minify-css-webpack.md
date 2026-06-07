---
title: "Minify CSS in webpack, Vite, and Rollup"
description: "Set up CSS minification in webpack 5, Vite, and Rollup. Covers CssMinimizerPlugin, cssnano, lightningcss, and production build configuration."
publishDate: 2026-04-25
updatedDate: 2026-04-25
author: "Editorial Team"
tags: ["webpack", "vite", "css", "minification", "build tools"]
draft: false
---

Modern JavaScript bundlers handle CSS minification as part of the production build. Here's how to set it up in the three most popular bundlers.

## webpack 5

webpack doesn't minify CSS by default. You need `css-minimizer-webpack-plugin`.

For more on this topic, see [*Critical CSS: What It Is and How to Implement It*](/blog/critical-css).

```bash
npm install --save-dev css-minimizer-webpack-plugin mini-css-extract-plugin css-loader
```

```js
// webpack.config.js
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');

module.exports = {
  mode: 'production',  // enables JS minification automatically
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].[contenthash].css',
    }),
  ],
  optimization: {
    minimizer: [
      `...`,              // keep existing JS minimizer (TerserPlugin)
      new CssMinimizerPlugin(),
    ],
  },
};
```

For more on this topic, see [*How to Remove Unused CSS: PurgeCSS, UnCSS, and Tree-Shaking*](/blog/remove-unused-css).

`MiniCssExtractPlugin` extracts CSS into separate files (instead of injecting into `<style>` tags). `CssMinimizerPlugin` minifies the extracted CSS using cssnano by default.

**Check the minification worked:**

```bash
npx webpack --mode production
ls -lh dist/
```

You should see `.css` files with content hashes in their names.

### SASS/LESS with webpack

```bash
npm install --save-dev sass sass-loader
```

```js
{
  test: /\.(sa|sc|c)ss$/,
  use: [
    MiniCssExtractPlugin.loader,
    'css-loader',
    'sass-loader',
  ],
}
```

The CSS minimizer plugin works on the compiled output regardless of the preprocessor.

### Custom minifier (cssnano presets)

```js
new CssMinimizerPlugin({
  minimizerOptions: {
    preset: [
      'default',
      {
        discardComments: { removeAll: true },
        normalizeWhitespace: true,
        colormin: true,
      },
    ],
  },
})
```

### lightningcss as the minifier

[lightningcss](https://lightningcss.dev/) (Rust-based) is significantly faster than cssnano:

```bash
npm install --save-dev lightningcss
```

```js
const { LightningCSSMinifyPlugin } = require('lightningcss');

new CssMinimizerPlugin({
  minify: CssMinimizerPlugin.lightningCssMinify,
})
```

## Vite

Vite minifies CSS automatically in production using esbuild by default. No configuration needed:

```bash
vite build
```

To switch to lightningcss (faster, better browser targeting):

```bash
npm install --save-dev lightningcss vite-plugin-lightningcss
```

```js
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  css: {
    transformer: 'lightningcss',
    lightningcss: {
      targets: browserslistToTargets(browserslist('>= 0.25%')),
    },
  },
  build: {
    cssMinify: 'lightningcss',
  },
});
```

To disable CSS minification (for debugging):

```js
export default defineConfig({
  build: { cssMinify: false },
});
```

### CSS code splitting in Vite

Vite splits CSS per JS chunk by default. To force a single CSS bundle:

```js
export default defineConfig({
  build: {
    cssCodeSplit: false,  // single bundle.css
  },
});
```

## Rollup

Rollup needs `rollup-plugin-postcss` to handle CSS:

```bash
npm install --save-dev rollup-plugin-postcss cssnano
```

```js
// rollup.config.js
import postcss from 'rollup-plugin-postcss';

export default {
  input: 'src/index.js',
  output: { dir: 'dist', format: 'esm' },
  plugins: [
    postcss({
      extract: true,          // extract to separate CSS file
      minimize: true,         // minify
      plugins: [
        require('cssnano')({ preset: 'default' }),
      ],
    }),
  ],
};
```

For more on this topic, see [*CSS File Too Large? How to Diagnose and Fix It*](/blog/css-file-size-too-large).

## Verifying minification

After running your build:

```bash
# Check compressed sizes
gzip -c dist/styles.css | wc -c
brotli -c dist/styles.css | wc -c

# Compare to source
wc -c src/styles.css dist/styles.css
```

Or open the Network tab in Chrome DevTools — look for your CSS file's transferred size vs. resource size. If compression is working, the transferred size should be 20–30% of the resource size.

## Quick one-off minification

For CSS that isn't part of a build pipeline — a standalone stylesheet, a quick size check — paste into [cssminify.io](/) and copy the minified output.
