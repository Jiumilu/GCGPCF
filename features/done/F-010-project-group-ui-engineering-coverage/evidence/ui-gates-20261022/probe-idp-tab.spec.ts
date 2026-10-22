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

test('probe idp users tab content', async ({ browser }) => {
  for (const [tag, user, password] of [['ADMIN', A_USER, A_PASSWORD], ['VIEWER', B_USER, B_PASSWORD]] as const) {
    const ctx = await browser.newContext({ viewport: { width: 1500, height: 900 } })
    const page = await ctx.newPage()
    await login(page, user, password)
    await page.goto('/global-cloud-workbench/service/idp-console')
    await page.waitForTimeout(2000)
    const tab = page.getByText('用户与目录', { exact: false }).first()
    if (await tab.count() > 0) {
      await tab.click()
      await page.waitForTimeout(1500)
    }
    const content = await page.evaluate(() => document.body.innerText.slice(0, 2500))
    console.log(`TAB_${tag} ` + JSON.stringify(content))
    await page.screenshot({ path: `${OUT}/screens/probe-idp-users-${tag.toLowerCase()}.png`, fullPage: false })
    await ctx.close()
  }
})
