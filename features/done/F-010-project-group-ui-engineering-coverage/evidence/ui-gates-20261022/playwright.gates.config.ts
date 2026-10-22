import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: '.',
  timeout: 60_000,
  expect: { timeout: 8_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL: 'http://127.0.0.1:8679',
    channel: 'chrome',
    headless: true,
    viewport: { width: 1500, height: 834 },
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chrome', use: { ...devices['Desktop Chrome'], channel: 'chrome' } }],
  webServer: {
    command: 'cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio" && HERMES_WEB_UI_BACKEND_PORT=8678 HERMES_WEB_UI_FRONTEND_PORT=8679 npx vite --host 127.0.0.1 --port 8679 --strictPort',
    url: 'http://127.0.0.1:8679',
    reuseExistingServer: true,
    timeout: 120_000,
  },
})
