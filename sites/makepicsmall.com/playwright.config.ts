import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  use: { baseURL: 'http://localhost:4321' },
  webServer: {
    command: 'pnpm exec astro preview --port 4321',
    port: 4321,
    reuseExistingServer: !process.env.CI,
    timeout: 60_000,
  },
});
