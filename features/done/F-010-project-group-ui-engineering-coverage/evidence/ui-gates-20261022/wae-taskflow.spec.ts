import { expect, test, type Page } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'

const OUT = process.env.F010_OUT as string
const USER = process.env.F010_LOGIN_USER as string
const PASSWORD = process.env.F010_LOGIN_PASSWORD as string
const NEW_PASSWORD = process.env.F010_NEW_PASSWORD as string
function requireEnv(): void {
  if (!OUT || !USER || !PASSWORD || !NEW_PASSWORD) throw new Error('F010_OUT / F010_LOGIN_USER / F010_LOGIN_PASSWORD / F010_NEW_PASSWORD are required')
}

async function loginWith(page: Page, password: string) {
  await page.locator('input').nth(0).fill(USER)
  await page.locator('input[type="password"]').first().fill(password)
  await page.getByRole('button', { name: /登录/ }).first().click()
}

test('task_flow_e2e_status: WAE 登录 → 首登改密 → 工作台 → 进入页面 → 返回/退出（含失败恢复）', async ({ page }) => {
  requireEnv()
  const steps: Array<Record<string, unknown>> = []
  const pageErrors: string[] = []
  const consoleErrors: string[] = []
  page.on('pageerror', (error) => {
    pageErrors.push(String(error).slice(0, 400))
    console.log('PAGE_ERROR', String(error).slice(0, 400))
  })
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text().slice(0, 300))
  })
  const record = (step: string, detail: Record<string, unknown> = {}) => {
    steps.push({ step, at: new Date().toISOString(), ...detail })
    console.log('STEP ' + JSON.stringify({ step, ...detail }))
  }
  const shot = async (name: string) => page.screenshot({ path: `${OUT}/screens/${name}.png`, fullPage: false })

  // 1) 登录页
  await page.goto('/')
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  await shot('wae-flow-01-login')
  record('login-page-loaded', { url: page.url() })

  // 2) 失败恢复：空提交（客户端校验，不发送登录请求）
  await page.getByRole('button', { name: /登录/ }).first().click()
  await expect(page.getByText('请填写账号与口令').first()).toBeVisible()
  await shot('wae-flow-02-login-validation-error')
  record('empty-submit-recovery', { message: '请填写账号与口令' })

  // 3) 真实本地测试身份登录（凭据由 env 注入，不写入证据文件）
  await loginWith(page, PASSWORD)
  await page.waitForTimeout(2500)
  const badCredential = page.getByText('用户名或口令不正确')
  if (await badCredential.isVisible().catch(() => false)) {
    // 复跑路径：账号已完成首登改密 → 用新口令重试
    record('login-fallback-to-changed-password', {})
    await loginWith(page, NEW_PASSWORD)
    await page.waitForTimeout(2500)
  }

  // 4) 首次登录强制改密（首次账号）或直接工作台（改密后复跑）
  let forcedChangeApplied = false
  const forcedChange = page.getByText('请先修改初始口令')
  if (await forcedChange.isVisible({ timeout: 8000 }).catch(() => false)) {
    await shot('wae-flow-03-forced-password-change')
    record('forced-password-change-page', {})
    const pw = page.locator('input[type="password"]')
    await pw.nth(0).fill(PASSWORD)
    await pw.nth(1).fill(NEW_PASSWORD)
    await pw.nth(2).fill(NEW_PASSWORD)
    await page.getByRole('button', { name: /保存新口令并继续/ }).first().click()
    await expect(page.getByText(/欢迎回来/).first()).toBeVisible({ timeout: 25000 })
    forcedChangeApplied = true
    record('password-changed', { forced: true })
  } else {
    record('login-without-forced-change', { note: '账号已完成首登改密（复跑路径）' })
  }

  // 5) 登录后工作台
  await expect(page.getByTestId('account-menu-trigger')).toBeVisible({ timeout: 25000 })
  await expect(page.getByText(/欢迎回来/).first()).toBeVisible()
  await shot('wae-flow-04-workbench-home')
  record('workbench-home', { accountVisible: (await page.getByText(USER).count()) > 0 })

  // 6) 进入一个工作区/页面（项目管理器，弹层）
  await page.getByTestId('home-open-project-manager').click()
  await page.waitForTimeout(1500)
  await shot('wae-flow-05-project-manager')
  const dialog = page.getByRole('dialog')
  const dialogVisible = await dialog.isVisible().catch(() => false)
  const managerSnippet = dialogVisible
    ? await dialog.evaluate((el) => (el as HTMLElement).innerText.slice(0, 400))
    : await page.evaluate(() => document.body.innerText.slice(0, 400))
  record('enter-workspace', { dialogVisible, snippet: managerSnippet.slice(0, 160) })

  // 关闭弹层（Escape 优先，按钮兜底）
  if (dialogVisible) {
    await page.keyboard.press('Escape')
    await page.waitForTimeout(600)
    if (await dialog.isVisible().catch(() => false)) {
      const closeButton = dialog.getByRole('button', { name: /✕|关闭|取消|Close/ }).first()
      if (await closeButton.count() > 0) await closeButton.click()
    }
    await expect(dialog).toBeHidden({ timeout: 10000 })
    record('close-workspace-dialog', {})
  }

  // 7) 返回工作台主页
  await page.getByRole('button', { name: /^主页$/ }).first().click()
  await expect(page.getByText(/欢迎回来/).first()).toBeVisible()
  await shot('wae-flow-06-return-home')
  record('return-home', {})

  // 8) 退出登录 → 回到登录页
  await page.getByTestId('account-menu-trigger').click()
  const logout = page.getByText('退出登录', { exact: false }).first()
  await expect(logout).toBeVisible({ timeout: 10000 })
  await logout.click()
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible({ timeout: 20000 })
  await shot('wae-flow-07-logout-return-login')
  record('logout-return-login', { url: page.url() })

  mkdirSync(`${OUT}/logs`, { recursive: true })
  writeFileSync(`${OUT}/logs/taskflow-assertions.json`, JSON.stringify({
    username: USER,
    forcedChangeApplied,
    steps,
    pageErrors,
    consoleErrors,
  }, null, 2))
  console.log('TASKFLOW_RESULT ' + JSON.stringify({
    steps: steps.length,
    pageErrors: pageErrors.length,
    consoleErrors: consoleErrors.length,
    forcedChangeApplied,
  }))

  expect(pageErrors).toEqual([])
  expect(steps.length).toBeGreaterThanOrEqual(8)
})
