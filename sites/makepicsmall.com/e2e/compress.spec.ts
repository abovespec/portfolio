import { test, expect } from '@playwright/test';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const FIXTURE = resolve(__dirname, '../tests/fixtures/tiny-jpg.jpg');

test('homepage loads and shows drop zone', async ({ page }) => {
  await page.goto('/');
  await expect(
    page
      .getByText(/drop images to compress/i)
      .or(page.getByText(/compress any image/i))
  ).toBeVisible();
});

test('/compress/jpg compresses a file', async ({ page }) => {
  await page.goto('/compress/jpg');
  await page.setInputFiles('input[type=file]', FIXTURE);
  await expect(
    page.getByRole('button', { name: /download/i }).first()
  ).toBeVisible({ timeout: 20_000 });
});

test('/for/passport-us has correct spec copy', async ({ page }) => {
  await page.goto('/for/passport-us');
  await expect(page.getByText(/600\s*×\s*600/i).first()).toBeVisible();
  await expect(page.getByText(/240\s*KB/i).first()).toBeVisible();
});
