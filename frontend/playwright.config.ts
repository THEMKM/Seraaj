import { defineConfig, devices } from '@playwright/test';

const port = process.env.FRONTEND_PORT || '5173';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: { baseURL: `http://localhost:${port}` },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
