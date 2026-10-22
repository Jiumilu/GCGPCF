import { test } from '@playwright/test'
import {
  authenticate,
  mockChatSocket,
  mockHermesApi,
  TEST_ACCESS_KEY,
} from '../../../../../../GlobalCloud Studio/tests/e2e/fixtures'

test('probe studio shell render', async ({ page }) => {
  page.on('console', (message) => console.log('PAGE_CONSOLE', message.type(), message.text().slice(0, 400)))
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 2000)))
  page.on('requestfailed', (request) => console.log('REQ_FAILED', request.method(), request.url().slice(0, 200), request.failure()?.errorText))

  await authenticate(page, TEST_ACCESS_KEY, 'research')
  await mockHermesApi(page)
  await mockChatSocket(page)
  await page.goto('/#/hermes/jobs')
  await page.waitForTimeout(4000)
  console.log('URL', page.url())
  console.log('TITLE', await page.title())
  console.log('BODY_TEXT', (await page.evaluate(() => document.body.innerText)).slice(0, 600))
  console.log('BODY_HTML', (await page.evaluate(() => document.body.innerHTML)).slice(0, 1200))
})
