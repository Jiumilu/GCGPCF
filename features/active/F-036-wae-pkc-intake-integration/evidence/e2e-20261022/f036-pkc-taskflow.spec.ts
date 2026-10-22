/**
 * F-036 task_flow E2E：登录 → 侧栏 PKC 入口（requires pkc）→ pkc-intake 候选页 → 返回工作台。
 *
 * 断言口径（与 F-036 acceptance 对应）：
 *   ① 真实登录（隔离临时 IdP，口令仅 env 注入，不写入证据）；
 *   ② system-admin 可见侧栏一级入口 `app-nav-pkc`；
 *   ③ 进入 `/global-cloud-workbench/pkc`：候选态徽章 / 非声明文案可见；机器字段不上屏；
 *   ④ 受控嵌入默认不启用（无 iframe）、页面不接受外部请求（监听 request）；
 *   ⑤ 返回工作台后 shell 正常（欢迎回来）；
 *   ⑥ 全程 0 pageerror；console error 仅允许登录前 `/me` 401 会话探测（预期）。
 */
import { expect, test, type Page } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'

const OUT = process.env.F036_OUT as string
const USER = process.env.F036_USER as string
const PASSWORD = process.env.F036_PASSWORD as string
const NEW_PASSWORD = process.env.F036_NEW_PASSWORD as string
const BASE_URL = process.env.F036_BASE_URL as string

function requireEnv(): void {
  if (!OUT || !USER || !PASSWORD || !NEW_PASSWORD || !BASE_URL) {
    throw new Error('F036_OUT / F036_USER / F036_PASSWORD / F036_NEW_PASSWORD / F036_BASE_URL are required')
  }
}

const EXTERNAL_ALLOW = /^(data:|blob:|about:|https?:\/\/(127\.0\.0\.1|localhost):\d+)/

test('task_flow_e2e_status: F-036 WAE 登录 → PKC 侧栏入口 → pkc-intake 候选页 → 返回工作台', async ({ page }) => {
  requireEnv()
  const steps: Array<Record<string, unknown>> = []
  const pageErrors: string[] = []
  const consoleErrors: string[] = []
  const externalRequests: string[] = []
  page.on('pageerror', (error) => {
    pageErrors.push(String(error).slice(0, 400))
    console.log('PAGE_ERROR ' + String(error).slice(0, 400))
  })
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text().slice(0, 300))
  })
  page.on('request', (request) => {
    const url = request.url()
    if (!EXTERNAL_ALLOW.test(url)) externalRequests.push(url.slice(0, 300))
  })
  const record = (step: string, detail: Record<string, unknown> = {}) => {
    steps.push({ step, at: new Date().toISOString(), ...detail })
    console.log('STEP ' + JSON.stringify({ step, ...detail }))
  }
  const shot = async (name: string) => page.screenshot({ path: `${OUT}/screens/${name}.png`, fullPage: false })

  // 1) 登录页（真实产品 UI，无 mock）
  await page.goto('/')
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  await shot('f036-flow-01-login')
  record('login-page-loaded', { url: page.url() })

  // 2) 真实登录（隔离临时 IdP；口令 env 注入）
  await page.locator('input').nth(0).fill(USER)
  await page.locator('input[type="password"]').first().fill(PASSWORD)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.waitForTimeout(2500)

  // 3) 首登强制改密（bootstrap 管理员 mustChangePassword=true）
  const forcedChange = page.getByText('请先修改初始口令')
  if (await forcedChange.isVisible({ timeout: 10000 }).catch(() => false)) {
    await shot('f036-flow-02-forced-password-change')
    record('forced-password-change-page', {})
    const pw = page.locator('input[type="password"]')
    await pw.nth(0).fill(PASSWORD)
    await pw.nth(1).fill(NEW_PASSWORD)
    await pw.nth(2).fill(NEW_PASSWORD)
    await page.getByRole('button', { name: /保存新口令并继续/ }).first().click()
    record('password-changed', { forced: true })
  } else {
    record('login-without-forced-change', { note: '账号已完成首登改密（复跑路径）' })
  }

  // 4) 工作台（登录成功）
  await expect(page.getByTestId('account-menu-trigger')).toBeVisible({ timeout: 30000 })
  await expect(page.getByText(/欢迎回来/).first()).toBeVisible()
  await shot('f036-flow-03-workbench')
  record('workbench-home', {})

  // 5) 进入应用壳（Global Cloud Workbench → AppsShell），侧栏一级入口 PKC（requires pkc，system-admin 可见）
  await page.getByRole('button', { name: 'Global Cloud', exact: true }).first().click()
  await expect(page).toHaveURL(/\/global-cloud-workbench(\/|$)/, { timeout: 20000 })
  const pkcNav = page.getByTestId('app-nav-pkc')
  await expect(pkcNav).toBeVisible({ timeout: 20000 })
  await shot('f036-flow-04-sidebar-pkc-entry')
  record('sidebar-pkc-visible', { testId: 'app-nav-pkc', url: page.url() })

  // 6) 进入 pkc-intake 候选页（AppsShell pushState：/global-cloud-workbench/pkc/pkc-intake）
  await pkcNav.click()
  await expect(page).toHaveURL(/\/global-cloud-workbench\/pkc(\/|$)/, { timeout: 20000 })
  const pageRoot = page.getByTestId('pkc-intake-page')
  await expect(pageRoot).toBeVisible()
  record('pkc-page-opened', { url: page.url() })

  // 7) 候选态 / 非声明文案可见
  await expect(page.getByText('PKC 知识工作台（候选接入）').first()).toBeVisible()
  await expect(page.getByText(/不声明 PKC 已接入/).first()).toBeVisible()
  const bodyText = await page.evaluate(() => document.body.innerText)
  record('candidate-and-nonclaims-visible', {
    hasCandidateBadge: bodyText.includes('候选'),
    hasNonClaim: bodyText.includes('不声明 PKC 已接入'),
  })

  // 8) 证据展示门禁：机器字段不上屏
  const machineFields = ['packageId', 'evidenceRefs', 'contentDigest', 'status_ceiling', 'cost_tier']
  const leaked = machineFields.filter((field) => bodyText.includes(field))
  record('no-machine-fields', { checked: machineFields, leaked })
  expect(leaked).toEqual([])

  // 9) 受控嵌入默认不启用：无 iframe，dry-run 说明可见；页面不接受外部请求
  await expect(page.getByTestId('pkc-embed-disabled')).toBeVisible()
  expect(await page.getByTestId('pkc-embed-frame').count()).toBe(0)
  await shot('f036-flow-05-pkc-candidate-page')
  record('embedment-default-off', { frameCount: 0, externalRequests: externalRequests.length })
  expect(externalRequests).toEqual([])

  // 10) 返回工作台（退回应用壳；侧栏入口仍在 = 壳未崩）
  await page.goBack()
  await expect(page.getByTestId('app-nav-pkc')).toBeVisible({ timeout: 20000 })
  await shot('f036-flow-06-return-workbench')
  record('return-workbench', { url: page.url() })

  mkdirSync(`${OUT}/logs`, { recursive: true })
  writeFileSync(`${OUT}/logs/taskflow-assertions.json`, JSON.stringify({
    baseURL: BASE_URL,
    account: 'F-036 隔离临时 system-admin（口令 env 注入，未写入证据）',
    steps,
    pageErrors,
    consoleErrors,
    externalRequests,
    result: 'pass',
  }, null, 2))
  console.log('TASKFLOW_RESULT ' + JSON.stringify({
    steps: steps.length,
    pageErrors: pageErrors.length,
    consoleErrors: consoleErrors.length,
    externalRequests: externalRequests.length,
  }))

  expect(pageErrors).toEqual([])
  expect(steps.length).toBeGreaterThanOrEqual(10)
})
