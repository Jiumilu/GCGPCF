import { expect, test, type Page } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'

const OUT = process.env.F010_OUT as string
const A_USER = process.env.F010_A_USER as string
const A_PASSWORD = process.env.F010_A_PASSWORD as string
const B_USER = process.env.F010_B_USER as string
const B_PASSWORD = process.env.F010_B_PASSWORD as string

function requireEnv(): void {
  if (!OUT || !A_USER || !A_PASSWORD || !B_USER || !B_PASSWORD) {
    throw new Error('F010_OUT / F010_A_USER / F010_A_PASSWORD / F010_B_USER / F010_B_PASSWORD are required')
  }
}

async function login(page: Page, user: string, password: string) {
  await page.goto('/')
  await page.waitForTimeout(1500)
  await page.locator('input').nth(0).fill(user)
  await page.locator('input[type="password"]').first().fill(password)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.waitForTimeout(2500)
}

async function me(page: Page) {
  return page.evaluate(async () => {
    const response = await fetch('/api/idp/me', { credentials: 'include' })
    const body = await response.json().catch(() => null)
    return { status: response.status, role: body?.role, menus: body?.menus ?? [], csrfToken: body?.csrfToken ?? null }
  })
}

async function usersApiStatus(page: Page) {
  return page.evaluate(async () => {
    const response = await fetch('/api/idp/users', { credentials: 'include' })
    const body = await response.json().catch(() => null)
    return { status: response.status, error: body?.error || body?.code || null }
  })
}

async function logoutViaSession(page: Page) {
  return page.evaluate(async () => {
    const meResponse = await fetch('/api/idp/me', { credentials: 'include' })
    const meBody = await meResponse.json().catch(() => null)
    const csrf = meBody?.csrfToken || ''
    const response = await fetch('/api/idp/logout', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-WAE-CSRF': csrf },
    })
    return response.status
  })
}

async function openUsersTab(page: Page) {
  await page.goto('/global-cloud-workbench/service/idp-console')
  await page.waitForTimeout(2200)
  await page.getByText('用户与目录', { exact: false }).first().click()
  await page.waitForTimeout(1800)
}

test('multi_user_usability: 双角色（system-admin / viewer）可见性差异、越权拒绝、会话隔离', async ({ browser }) => {
  requireEnv()
  const steps: Array<Record<string, unknown>> = []
  const pageErrors: string[] = []
  const consoleErrors: string[] = []
  const record = (step: string, detail: Record<string, unknown> = {}) => {
    steps.push({ step, at: new Date().toISOString(), ...detail })
    console.log('STEP ' + JSON.stringify({ step, ...detail }))
  }
  const watch = (page: Page, tag: string) => {
    page.on('pageerror', (error) => {
      pageErrors.push(`${tag}: ${String(error).slice(0, 300)}`)
      console.log('PAGE_ERROR', tag, String(error).slice(0, 300))
    })
    page.on('console', (message) => {
      if (message.type() === 'error') consoleErrors.push(`${tag}: ${message.text().slice(0, 200)}`)
    })
  }
  const shot = async (page: Page, name: string) => page.screenshot({ path: `${OUT}/screens/${name}.png`, fullPage: false })

  // 账号 A：system-admin
  const ctxA = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageA = await ctxA.newPage()
  watch(pageA, 'A')
  await login(pageA, A_USER, A_PASSWORD)
  const meA = await me(pageA)
  record('A-login', { role: meA.role, menus: meA.menus.length })
  expect(meA.role).toBe('system-admin')
  expect(meA.menus).toContain('idp-console')

  await openUsersTab(pageA)
  await expect(pageA.getByText('目录账号', { exact: false }).first()).toBeVisible()
  await expect(pageA.getByText('2 / 2').first()).toBeVisible()
  await expect(pageA.getByText(A_USER, { exact: false }).first()).toBeVisible()
  await expect(pageA.getByText(B_USER, { exact: false }).first()).toBeVisible()
  const apiA = await usersApiStatus(pageA)
  await shot(pageA, 'multi-user-A-system-admin-idp-users')
  record('A-admin-capability', {
    usersApiStatus: apiA.status,
    seesBothAccounts: true,
    roleTextVisible: (await pageA.getByText('system-admin', { exact: false }).count()) > 0,
  })
  expect(apiA.status).toBe(200)

  const logoutA = await logoutViaSession(pageA)
  await pageA.goto('/')
  await expect(pageA.getByTestId('login-space-greenchain')).toBeVisible({ timeout: 20000 })
  await shot(pageA, 'multi-user-A-after-logout-login')
  const meA2 = await me(pageA)
  record('A-logout', { logoutStatus: logoutA, meAfterLogout: meA2.status })
  expect(meA2.status).toBe(401)

  // 账号 B：viewer（独立 context，不继承 A 会话）
  const ctxB = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageB = await ctxB.newPage()
  watch(pageB, 'B')
  await login(pageB, B_USER, B_PASSWORD)
  const meB = await me(pageB)
  record('B-login', { role: meB.role, menus: meB.menus.length })
  expect(meB.role).toBe('viewer')
  expect(meB.menus).not.toContain('idp-console')

  await openUsersTab(pageB)
  await expect(pageB.getByText('无权限：用户目录仅体系管理员可见', { exact: false }).first()).toBeVisible()
  await expect(pageB.getByText('当前身份为「viewer」', { exact: false }).first()).toBeVisible()
  const apiB = await usersApiStatus(pageB)
  await shot(pageB, 'multi-user-B-viewer-idp-denied')
  record('B-denied', {
    usersApiStatus: apiB.status,
    apiError: apiB.error,
    deniedTextVisible: true,
  })
  expect(apiB.status).toBe(403)
  expect(apiB.error || '').toContain('system-admin')

  const logoutB = await logoutViaSession(pageB)
  await pageB.goto('/')
  await expect(pageB.getByTestId('login-space-greenchain')).toBeVisible({ timeout: 20000 })
  await shot(pageB, 'multi-user-B-after-logout-login')
  const meB2 = await me(pageB)
  record('B-logout', { logoutStatus: logoutB, meAfterLogout: meB2.status })
  expect(meB2.status).toBe(401)

  await ctxA.close()
  await ctxB.close()

  mkdirSync(`${OUT}/logs`, { recursive: true })
  writeFileSync(`${OUT}/logs/multi-user-assertions.json`, JSON.stringify({
    accounts: { admin: A_USER, viewer: B_USER },
    roles: { A: meA.role, B: meB.role },
    menus: { A: meA.menus, B: meB.menus },
    usersApi: { A: apiA.status, B: apiB.status, BError: apiB.error },
    sessionIsolation: { AAfterLogout: meA2.status, BAfterLogout: meB2.status },
    steps,
    pageErrors,
    consoleErrors,
  }, null, 2))
  console.log('MULTI_USER_RESULT ' + JSON.stringify({
    steps: steps.length,
    pageErrors: pageErrors.length,
    consoleErrors: consoleErrors.length,
    roles: { A: meA.role, B: meB.role },
    usersApi: { A: apiA.status, B: apiB.status },
  }))
  expect(pageErrors).toEqual([])
})
