import { test, expect } from '@playwright/test';

test('dark mode toggle persists', async ({ page }) => {
  await page.goto('/');
  await page.click('button[aria-label="Toggle dark mode"]');
  await expect(page.locator('html')).toHaveClass(/dark/);
  await page.reload();
  await expect(page.locator('html')).toHaveClass(/dark/);
});
