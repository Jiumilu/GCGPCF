import { test, type Page } from '@playwright/test'

const OUT = process.env.F010_OUT as string
const A_USER = process.env.F010_A_USER as string
const A_PASSWORD = process.env.F010_A_PASSWORD as string
const B_USER = process.env.F010_B_USER as string
const B_PASSWORD = process.env.F010_B_PASSWORD as string

async function login(page: Page, user: string, password: string) {
  await page.goto('/')
  await page.waitForTimeout(1200)
  await page.locator('input').nth(0).fill(user)
  await page.locator('input[type="password"]').first().fill(password)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.getByTestId('account-menu-trigger').waitFor({ timeout: 20000 })
}

async function inspect(page: Page, tag: string) {
  const me = await page.evaluate(async () => {
    const response = await fetch('/api/idp/me', { credentials: 'include' })
    const body = await response.json().catch(() => null)
    return { status: response.status, role: body?.role, menus: body?.menus, ok: body?.ok }
  })
  console.log(`ME_${tag} ` + JSON.stringify(me))
  const rail = await page.evaluate(() => Array.from(document.querySelectorAll('[data-testid^="app-nav-"]')).map((el) => ({
    testid: el.getAttribute('data-testid'),
    label: (el.textContent || '').trim().slice(0, 40),
  })))
  console.log(`RAIL_${tag} ` + JSON.stringify(rail))
  const bodyText = await page.evaluate(() => document.body.innerText.slice(0, 500))
  console.log(`BODY_${tag} ` + JSON.stringify(bodyText))
}

test('probe role session details', async ({ browser }) => {
  const ctxA = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageA = await ctxA.newPage()
  await login(pageA, A_USER, A_PASSWORD)
  await pageA.goto('/global-cloud-workbench')
  await pageA.waitForTimeout(2000)
  await inspect(pageA, 'ADMIN')
  await pageA.screenshot({ path: `${OUT}/screens/probe-inspect-admin.png`, fullPage: false })
  await ctxA.close()

  const ctxB = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageB = await ctxB.newPage()
  await login(pageB, B_USER, B_PASSWORD)
  await pageB.goto('/global-cloud-workbench')
  await pageB.waitForTimeout(2000)
  await inspect(pageB, 'VIEWER')
  await pageB.screenshot({ path: `${OUT}/screens/probe-inspect-viewer.png`, fullPage: false })
  await ctxB.close()
})
