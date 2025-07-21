import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  await page.goto('/login');
  await page.getByPlaceholder('Email').fill('volunteer@example.com');
  await page.getByPlaceholder('Password').fill('pw');
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page).toHaveURL(/dashboard/);
  await expect(page.locator('text=volunteer@example.com')).toBeVisible();
});
