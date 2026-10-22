import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string
const USER = process.env.F010_LOGIN_USER as string
const PASSWORD = process.env.F010_LOGIN_PASSWORD as string

test('probe WAE login success path', async ({ page }) => {
  page.on('console', (message) => console.log('PAGE_CONSOLE', message.type(), message.text().slice(0, 300)))
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 600)))
  await page.goto('/')
  await page.waitForTimeout(2000)

  const inputs = page.locator('input')
  console.log('INPUT_COUNT', await inputs.count())
  await inputs.nth(0).fill(USER)
  await page.locator('input[type="password"]').first().fill(PASSWORD)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.waitForTimeout(3500)
  await page.screenshot({ path: `${OUT}/screens/probe-wae-after-login.png`, fullPage: false })

  const summary = await page.evaluate(() => ({
    url: location.href,
    title: document.title,
    bodyText: document.body.innerText.slice(0, 2500),
    testids: Array.from(document.querySelectorAll('[data-testid]')).slice(0, 60).map((el) => el.getAttribute('data-testid')),
    ariaLabels: Array.from(document.querySelectorAll('[aria-label]')).slice(0, 40).map((el) => el.getAttribute('aria-label')),
    navs: Array.from(document.querySelectorAll('nav')).map((el) => el.getAttribute('aria-label')),
    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 20).map((el) => ({ href: el.getAttribute('href'), label: (el.textContent || '').trim().slice(0, 30) })),
    cookieHasSession: document.cookie.includes('wae_sid'),
  }))
  console.log('AFTER_LOGIN ' + JSON.stringify(summary, null, 1).slice(0, 8000))
})
