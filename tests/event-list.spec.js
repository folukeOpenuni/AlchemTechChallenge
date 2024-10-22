import { test, expect } from '@playwright/test';

test.describe('Event List Page', () => {
  test('should load the event list and display it correctly', async ({ page }) => {
    // Navigate to the React app
    await page.goto('https://bookish-goldfish-5gjj476449jcpv95-3000.app.github.dev');
    await page.waitForLoadState('networkidle');  // Ensure all resources are loaded

    //await page.pause();  // Pause execution and open browser for debugging

    // Ensure the Event List header is displayed (Increase timeout to wait for JavaScript rendering)
    await expect(page.locator('h1')).toHaveText('Event List', { timeout: 30000 });

    // Wait for the table rows to load (ensure data is fetched from the API)
    const tableRows = page.locator('tbody tr');
    await expect(tableRows).toHaveCount(1, { timeout: 10000 });

    // Check the first row in the table
    const firstRow = tableRows.first();
    await expect(firstRow.locator('td:nth-child(1)')).not.toHaveText('');  // Check that ID is not empty
  });
});
