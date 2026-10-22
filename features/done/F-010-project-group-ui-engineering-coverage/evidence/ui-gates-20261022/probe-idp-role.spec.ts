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

async function inspectIdp(page: Page, tag: string) {
  for (const path of ['/global-cloud-workbench/service/idp-console', '/global-cloud-workbench/idp']) {
    await page.goto(path)
    await page.waitForTimeout(2500)
    const info = await page.evaluate(async () => {
      const response = await fetch('/api/idp/users', { credentials: 'include' })
      const body = await response.json().catch(() => null)
      const content = document.querySelector('[data-testid="app-content"]') || document.body
      return {
        url: location.href,
        apiStatus: response.status,
        apiError: body?.error || body?.code || null,
        bodyText: (content as HTMLElement).innerText.slice(0, 900),
      }
    })
    console.log(`IDP_${tag}_${path.replaceAll('/', '_')} ` + JSON.stringify(info).slice(0, 3000))
    await page.screenshot({ path: `${OUT}/screens/probe-idp-${tag.toLowerCase().replace(/[^a-z]/g, '')}-${path.split('/').pop()}.png`, fullPage: false })
  }
}

test('probe idp console access by role', async ({ browser }) => {
  const ctxA = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageA = await ctxA.newPage()
  await login(pageA, A_USER, A_PASSWORD)
  await inspectIdp(pageA, 'ADMIN')
  await ctxA.close()

  const ctxB = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageB = await ctxB.newPage()
  await login(pageB, B_USER, B_PASSWORD)
  await inspectIdp(pageB, 'VIEWER')
  await ctxB.close()
})
