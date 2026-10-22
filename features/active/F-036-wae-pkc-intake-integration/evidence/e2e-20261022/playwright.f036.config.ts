/**
 * F-036 task_flow E2E —— Playwright 配置（复用 F-010 WAE 配置模式，2026-10-22）。
 * baseURL 由 F036_BASE_URL 注入（本轮隔离实例 :4301；4300 被其它会话占用，不终止他人服务）。
 */
import { defineConfig, devices } from '@playwright/test'

const baseURL = process.env.F036_BASE_URL as string
if (!baseURL) throw new Error('F036_BASE_URL is required')

export default defineConfig({
  testDir: '.',
  // 只跑当前验用 spec；归档的 run2 垫片版本在 logs/run2-with-shim/*.txt（不参与执行）
  testMatch: 'f036-pkc-taskflow.spec.ts',
  timeout: 90_000,
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
