import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string
const USER = process.env.F010_LOGIN_USER as string
const PASSWORD = process.env.F010_LOGIN_PASSWORD as string
const NEW_PASSWORD = process.env.F010_NEW_PASSWORD as string

test('probe WAE change password path', async ({ page }) => {
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 500)))
  await page.goto('/')
  await page.waitForTimeout(1500)
  await page.locator('input').nth(0).fill(USER)
  await page.locator('input[type="password"]').first().fill(PASSWORD)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.getByText('请先修改初始口令').waitFor({ timeout: 15000 })

  const pw = page.locator('input[type="password"]')
  console.log('PW_INPUT_COUNT', await pw.count())
  await pw.nth(0).fill(PASSWORD)
  await pw.nth(1).fill(NEW_PASSWORD)
  await pw.nth(2).fill(NEW_PASSWORD)
  await page.screenshot({ path: `${OUT}/screens/probe-wae-change-password-filled.png`, fullPage: false })
  await page.getByRole('button', { name: /保存新口令并继续/ }).first().click()
  await page.waitForTimeout(4000)
  await page.screenshot({ path: `${OUT}/screens/probe-wae-after-change-password.png`, fullPage: false })
  const summary = await page.evaluate(() => ({
    url: location.href,
    title: document.title,
    bodyText: document.body.innerText.slice(0, 3000),
    testids: Array.from(document.querySelectorAll('[data-testid]')).slice(0, 80).map((el) => el.getAttribute('data-testid')),
    ariaLabels: Array.from(document.querySelectorAll('[aria-label]')).slice(0, 40).map((el) => el.getAttribute('aria-label')),
    buttons: Array.from(document.querySelectorAll('button')).slice(0, 40).map((el) => (el.textContent || '').trim().slice(0, 40)),
    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 30).map((el) => ({ href: el.getAttribute('href'), label: (el.textContent || '').trim().slice(0, 30) })),
    navs: Array.from(document.querySelectorAll('nav')).map((el) => el.getAttribute('aria-label')),
  }))
  console.log('AFTER_PASSWORD_CHANGE ' + JSON.stringify(summary, null, 1).slice(0, 9000))
})
