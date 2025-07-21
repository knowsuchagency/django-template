import { test, expect } from '@playwright/test';

test.describe('Navigation', () => {
  test('should redirect root to login when not authenticated', async ({ page }) => {
    await page.goto('/static/');
    await expect(page).toHaveURL('/static/login');
  });

  test('should have proper page titles', async ({ page }) => {
    await page.goto('/static/login');
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveTitle(/django template/i);
  });

  test('should display layout components', async ({ page }) => {
    await page.goto('/static/login');
    await page.waitForLoadState('networkidle');
    
    // Check for theme toggle (part of the layout) - it's a button with sr-only text
    await expect(page.getByRole('button').filter({ hasText: 'Toggle theme' })).toBeVisible();
    
    // Check for main content area
    await expect(page.locator('main')).toBeVisible();
  });
});