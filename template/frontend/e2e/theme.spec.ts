import { test, expect } from '@playwright/test';

test.describe('Theme Persistence', () => {
  test('should persist theme selection across page reloads', async ({ page }) => {
    await page.goto('/static/');
    
    // Find and click the theme toggle button
    const themeToggle = page.getByRole('button').filter({ hasText: 'Toggle theme' });
    await expect(themeToggle).toBeVisible();
    
    // Get initial theme
    const initialTheme = await page.evaluate(() => 
      document.documentElement.classList.contains('dark') ? 'dark' : 'light'
    );
    
    // Click theme toggle to open dropdown
    await themeToggle.click();
    
    // Wait for dropdown to be visible and select a different theme
    const targetTheme = initialTheme === 'dark' ? 'Light' : 'Dark';
    await page.getByRole('menuitem', { name: targetTheme }).click();
    
    // Wait for theme to change
    await page.waitForFunction(
      (initialTheme) => {
        const currentTheme = document.documentElement.classList.contains('dark') ? 'dark' : 'light';
        return currentTheme !== initialTheme;
      },
      initialTheme,
      { timeout: 5000 }
    );
    
    // Get the new theme
    const newTheme = await page.evaluate(() => 
      document.documentElement.classList.contains('dark') ? 'dark' : 'light'
    );
    
    // Verify theme changed
    expect(newTheme).not.toBe(initialTheme);
    
    // Reload page
    await page.reload();
    
    // Verify theme persisted
    const persistedTheme = await page.evaluate(() => 
      document.documentElement.classList.contains('dark') ? 'dark' : 'light'
    );
    expect(persistedTheme).toBe(newTheme);
  });

  test('should have theme toggle visible on all pages', async ({ page }) => {
    const pages = ['/static/login', '/static/signup'];
    
    for (const path of pages) {
      await page.goto(path);
      await expect(page.getByRole('button').filter({ hasText: 'Toggle theme' })).toBeVisible();
    }
  });
});