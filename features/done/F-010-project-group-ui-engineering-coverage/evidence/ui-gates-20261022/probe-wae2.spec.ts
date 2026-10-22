import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string

test('probe WAE routes', async ({ page }) => {
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 500)))
  for (const [name, path] of [
    ['console', '/wae-console/'],
    ['workbench-was', '/global-cloud-workbench/was-browse'],
    ['workbench-root', '/global-cloud-workbench'],
  ] as const) {
    await page.goto(path)
    await page.waitForTimeout(3500)
    await page.screenshot({ path: `${OUT}/screens/wae-probe-${name}.png`, fullPage: false })
    const summary = await page.evaluate(() => ({
      url: location.href,
      title: document.title,
      bodyText: document.body.innerText.slice(0, 800),
      testids: Array.from(document.querySelectorAll('[data-testid]')).slice(0, 50).map((el) => el.getAttribute('data-testid')),
      navs: Array.from(document.querySelectorAll('nav')).map((el) => el.getAttribute('aria-label')),
    }))
    console.log(`ROUTE_${name} ` + JSON.stringify(summary))
  }
})

test('probe WAE login failure recovery', async ({ page }) => {
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 500)))
  await page.goto('/')
  await page.waitForTimeout(3000)
  await page.screenshot({ path: `${OUT}/screens/wae-login-initial.png`, fullPage: false })
  const accountInput = page.locator('input').first()
  const passwordInput = page.locator('input[type="password"]').first()
  console.log('ACCOUNT_VISIBLE', await accountInput.isVisible(), 'PASSWORD_VISIBLE', await passwordInput.isVisible())
  const submit = page.getByRole('button', { name: /登录/ }).first()
  console.log('SUBMIT_VISIBLE', await submit.isVisible())
  await submit.click()
  await page.waitForTimeout(1500)
  await page.screenshot({ path: `${OUT}/screens/wae-login-empty-submit.png`, fullPage: false })
  const afterText = await page.evaluate(() => document.body.innerText.slice(0, 1200))
  console.log('AFTER_EMPTY_SUBMIT ' + JSON.stringify(afterText))
})
