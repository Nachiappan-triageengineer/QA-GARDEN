// @ts-check
const { test, expect } = require('@playwright/test');

/**
 * Demo Playwright Test Suite
 * This suite contains intentional failures to demonstrate the bug triage engine
 */

test.describe('Login Page Tests', () => {

    test('should display correct page title', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - intentional mismatch
        await expect(page).toHaveTitle('Login - MyApp');
    });

    test('should find login button', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - element doesn't exist
        await page.click('#login-button');
    });

    test('should validate email input', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - element doesn't exist
        const emailInput = await page.locator('#email-input');
        await expect(emailInput).toBeVisible();
    });

});

test.describe('Dashboard Tests', () => {

    test('should load user profile', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - element doesn't exist
        await page.waitForSelector('.user-profile', { timeout: 5000 });
    });

    test('should display welcome message', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - text doesn't exist
        await expect(page.locator('h1')).toContainText('Welcome, User!');
    });

});

test.describe('Form Submission Tests', () => {

    test('should submit contact form', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - button doesn't exist
        await page.fill('#contact-name', 'John Doe');
        await page.fill('#contact-email', 'john@example.com');
        await page.click('#submit-contact');
    });

    test('should validate required fields', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - element doesn't exist
        await page.click('#submit-form');
        const errorMessage = await page.locator('.error-message');
        await expect(errorMessage).toBeVisible();
    });

});

test.describe('Navigation Tests', () => {

    test('should navigate to settings page', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - link doesn't exist
        await page.click('a[href="/settings"]');
        await expect(page).toHaveURL(/.*settings/);
    });

    test('should have working breadcrumbs', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - element doesn't exist
        const breadcrumb = await page.locator('.breadcrumb');
        await expect(breadcrumb).toContainText('Home');
    });

});

test.describe('API Integration Tests', () => {

    test('should fetch user data', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This will fail - API endpoint doesn't exist
        const response = await page.request.get('https://demo.playwright.dev/api/user/123');
        expect(response.status()).toBe(200);
    });

    test('should handle 404 errors gracefully', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/nonexistent-page');
        // This might fail depending on the site's 404 handling
        await expect(page.locator('h1')).toContainText('Page Not Found');
    });

});

test.describe('Passing Tests', () => {

    test('should load the demo page successfully', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This should pass
        await expect(page).toHaveTitle(/TodoMVC/);
    });

    test('should have input field for new todos', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This should pass
        const input = await page.locator('.new-todo');
        await expect(input).toBeVisible();
    });

    test('should add a new todo item', async ({ page }) => {
        await page.goto('https://demo.playwright.dev/todomvc');
        // This should pass
        await page.fill('.new-todo', 'Test Todo Item');
        await page.press('.new-todo', 'Enter');
        await expect(page.locator('.todo-list li')).toHaveCount(1);
    });

});
