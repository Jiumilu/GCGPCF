import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string
const A_USER = process.env.F010_A_USER as string
const A_PASSWORD = process.env.F010_A_PASSWORD as string
const B_USER = process.env.F010_B_USER as string
const B_PASSWORD = process.env.F010_B_PASSWORD as string

async function login(page: import('@playwright/test').Page, user: string, password: string) {
  await page.goto('/')
  await page.waitForTimeout(1200)
  await page.locator('input').nth(0).fill(user)
  await page.locator('input[type="password"]').first().fill(password)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.getByTestId('account-menu-trigger').waitFor({ timeout: 20000 })
}

async function dump(page: import('@playwright/test').Page, tag: string) {
  const info = await page.evaluate(() => ({
    url: location.href,
    bodyText: document.body.innerText.slice(0, 1200),
    testids: Array.from(document.querySelectorAll('[data-testid]')).slice(0, 80).map((el) => el.getAttribute('data-testid')),
    ariaLabels: Array.from(document.querySelectorAll('[aria-label]')).slice(0, 40).map((el) => el.getAttribute('aria-label')),
    buttons: Array.from(document.querySelectorAll('button')).slice(0, 60).map((el) => (el.textContent || '').trim().slice(0, 40)),
    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 40).map((el) => ({ href: el.getAttribute('href'), label: (el.textContent || '').trim().slice(0, 30) })),
  }))
  console.log(`DUMP_${tag} ` + JSON.stringify(info).slice(0, 5000))
}

test('probe dual-role workbench nav', async ({ browser }) => {
  const ctxA = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageA = await ctxA.newPage()
  await login(pageA, A_USER, A_PASSWORD)
  await pageA.goto('/global-cloud-workbench')
  await pageA.waitForTimeout(2500)
  await pageA.screenshot({ path: `${OUT}/screens/probe-role-admin-workbench.png`, fullPage: false })
  await dump(pageA, 'ADMIN_WORKBENCH')
  await ctxA.close()

  const ctxB = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageB = await ctxB.newPage()
  await login(pageB, B_USER, B_PASSWORD)
  await pageB.goto('/global-cloud-workbench')
  await pageB.waitForTimeout(2500)
  await pageB.screenshot({ path: `${OUT}/screens/probe-role-viewer-workbench.png`, fullPage: false })
  await dump(pageB, 'VIEWER_WORKBENCH')
  await pageB.goto('/global-cloud-workbench/idp')
  await pageB.waitForTimeout(2500)
  await pageB.screenshot({ path: `${OUT}/screens/probe-role-viewer-idp-direct.png`, fullPage: false })
  await dump(pageB, 'VIEWER_IDP_DIRECT')
  await ctxB.close()
})
