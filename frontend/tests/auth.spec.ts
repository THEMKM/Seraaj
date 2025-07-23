import { test, expect } from '@playwright/test';

test('signup flow redirects to dashboard', async ({ page }) => {
  await page.goto('/signup');
  await page.fill('input[type=email]', 'user@example.com');
  await page.fill('input[type=password]', 'password123');
  await page.click('text=Create Account');
  await expect(page).toHaveURL(/\/dashboard$/);
});

test('login flow redirects to dashboard', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[type=email]', 'user@example.com');
  await page.fill('input[type=password]', 'password123');
  await page.click('text=Log In');
  await expect(page).toHaveURL(/\/dashboard$/);
});
