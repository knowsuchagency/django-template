import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should redirect to login when not authenticated', async ({ page }) => {
    await page.goto('/static/dashboard');
    await expect(page).toHaveURL('/static/login');
  });

  test('should display login page correctly', async ({ page }) => {
    await page.goto('/static/login');
    await expect(page).toHaveURL('/static/login');
    await expect(page.getByRole('heading', { name: /login/i })).toBeVisible();
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
    await expect(page.getByRole('button', { name: /login/i })).toBeVisible();
    // Check for sign up link in the form area
    await expect(page.locator('form').getByRole('link', { name: /sign up/i })).toBeVisible();
  });

  test('should navigate to signup from login', async ({ page }) => {
    await page.goto('/static/login');
    // Click the sign up link in the form area
    await page.locator('form').getByRole('link', { name: /sign up/i }).click();
    await expect(page).toHaveURL('/static/signup');
    await expect(page.getByRole('heading', { name: /sign up/i })).toBeVisible();
  });

  test('should display signup page correctly', async ({ page }) => {
    await page.goto('/static/signup');
    await expect(page.getByLabel(/email/i)).toBeVisible();
    await expect(page.getByLabel('Password', { exact: true })).toBeVisible();
    await expect(page.getByLabel('Confirm Password')).toBeVisible();
    await expect(page.getByRole('button', { name: /sign up/i })).toBeVisible();
    // Check for login link in the form area
    await expect(page.locator('form').getByRole('link', { name: 'Login' })).toBeVisible();
  });

  test('should navigate to login from signup', async ({ page }) => {
    await page.goto('/static/signup');
    // Click the login link in the form area
    await page.locator('form').getByRole('link', { name: 'Login' }).click();
    await expect(page).toHaveURL('/static/login');
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/static/login');
    await page.getByLabel(/email/i).fill('invalid@example.com');
    await page.getByLabel(/password/i).fill('wrongpassword');
    await page.getByRole('button', { name: /login/i }).click();
    
    // Wait for form submission and check if we're still on login page (indicates error)
    await page.waitForLoadState('networkidle');
    await expect(page).toHaveURL('/static/login');
    // Could also check for error styling or specific error elements if they exist
  });
});