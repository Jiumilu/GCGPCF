import { defineConfig, devices } from '@playwright/test'

const STUDIO = '/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio'

export default defineConfig({
  testDir: `${STUDIO}/tests/e2e`,
  timeout: 120_000,
  expect: { timeout: 10_000 },
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
  projects: [{ name: 'studio-specs', use: { ...devices['Desktop Chrome'], channel: 'chrome' } }],
  webServer: {
    command: `cd "${STUDIO}" && HERMES_WEB_UI_BACKEND_PORT=8678 HERMES_WEB_UI_FRONTEND_PORT=8679 npx vite --host 127.0.0.1 --port 8679 --strictPort`,
    url: 'http://127.0.0.1:8679',
    reuseExistingServer: true,
    timeout: 120_000,
  },
})
