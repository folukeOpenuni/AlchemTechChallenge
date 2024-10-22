// playwright.config.js
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    headless: true,  // Run all tests in headless mode
    baseURL: 'https://bookish-goldfish-5gjj476449jcpv95-3000.app.github.dev',
    timeout: 30000,  // Set a default timeout for the tests
  },
});
