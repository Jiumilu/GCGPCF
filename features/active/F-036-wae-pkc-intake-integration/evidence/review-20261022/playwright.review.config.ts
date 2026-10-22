/**
 * F-036 正式接入评审准备 —— Playwright 配置（multi_user + accessibility，2026-10-22）。
 * 复用 F-010 WAE 模式：隔离临时 IdP + system Chrome；baseURL 由 F036_BASE_URL 注入。
 */
import { defineConfig, devices } from '@playwright/test'

const baseURL = process.env.F036_BASE_URL as string
if (!baseURL) throw new Error('F036_BASE_URL is required')

export default defineConfig({
  testDir: '.',
  testMatch: 'review.spec.ts',
  timeout: 120_000,
  expect: { timeout: 12_000 },
  fullyParallel: false,
  workers: 1,
  reporter: [['list']],
  use: {
    baseURL,
    channel: 'chrome',
    headless: true,
    viewport: { width: 1500, height: 900 },
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [{ name: 'chrome', use: { ...devices['Desktop Chrome'], channel: 'chrome' } }],
})
