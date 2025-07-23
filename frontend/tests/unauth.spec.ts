import { test, expect } from '@playwright/test';

test('401 from search redirects to login', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('token', 't');
  });
  await page.route('**/api/opportunity/search**', route => {
    route.fulfill({ status: 401, body: 'Unauthorized' });
  });
  await page.goto('/opportunities');
  await page.waitForURL('**/login');
  const token = await page.evaluate(() => localStorage.getItem('token'));
  expect(token).toBeNull();
});

test('401 from org dashboard redirects to login', async ({ page }) => {
  await page.addInitScript(() => {
    localStorage.setItem('token', 't');
  });
  await page.route('**/api/org/opportunities', route => {
    route.fulfill({ status: 401, body: 'Unauthorized' });
  });
  await page.goto('/org/dashboard');
  await page.waitForURL('**/login');
  const token = await page.evaluate(() => localStorage.getItem('token'));
  expect(token).toBeNull();
});
