import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string
const USER = process.env.F010_LOGIN_USER as string
const PASSWORD = process.env.F010_LOGIN_PASSWORD as string
const NEW_PASSWORD = process.env.F010_NEW_PASSWORD as string

test('probe project manager dialog controls', async ({ page }) => {
  await page.goto('/')
  await page.waitForTimeout(1200)
  // 已改密账号：直接用新口令
  await page.locator('input').nth(0).fill(USER)
  await page.locator('input[type="password"]').first().fill(NEW_PASSWORD)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.getByTestId('account-menu-trigger').waitFor({ timeout: 20000 })
  await page.getByTestId('home-open-project-manager').click()
  await page.getByRole('dialog').waitFor({ timeout: 10000 })
  const controls = await page.getByRole('dialog').evaluate((dialog) => ({
    buttons: Array.from(dialog.querySelectorAll('button')).map((el) => ({
      text: (el.textContent || '').trim().slice(0, 30),
      aria: el.getAttribute('aria-label'),
      title: el.getAttribute('title'),
      testid: el.getAttribute('data-testid'),
      cls: (el.getAttribute('class') || '').slice(0, 60),
    })),
    closeCandidates: Array.from(dialog.querySelectorAll('[aria-label*="关闭"], [title*="关闭"], button')).slice(0, 20).map((el) => (el.getAttribute('aria-label') || el.getAttribute('title') || (el.textContent || '').trim()).slice(0, 30)),
  }))
  console.log('DIALOG_CONTROLS ' + JSON.stringify(controls, null, 1))
  await page.screenshot({ path: `${OUT}/screens/probe-wae-dialog.png`, fullPage: false })
})
