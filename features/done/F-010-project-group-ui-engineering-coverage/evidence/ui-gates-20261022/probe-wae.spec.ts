import { test } from '@playwright/test'

const OUT = process.env.F010_OUT as string

test('probe WAE ui', async ({ page }) => {
  page.on('pageerror', (error) => console.log('PAGE_ERROR', (error.stack || String(error)).slice(0, 800)))
  await page.goto('/')
  await page.waitForTimeout(5000)
  await page.screenshot({ path: `${OUT}/screens/wae-probe-home.png`, fullPage: false })
  console.log('URL', page.url())
  console.log('TITLE', await page.title())
  const summary = await page.evaluate(() => {
    const text = (el: Element | null) => (el?.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60)
    return {
      bodyText: document.body.innerText.slice(0, 2000),
      buttons: Array.from(document.querySelectorAll('button, [role="button"]')).slice(0, 40).map((el) => text(el)),
      links: Array.from(document.querySelectorAll('a[href]')).slice(0, 40).map((el) => ({ href: el.getAttribute('href'), label: text(el) })),
      testids: Array.from(document.querySelectorAll('[data-testid]')).slice(0, 60).map((el) => el.getAttribute('data-testid')),
      ariaLabels: Array.from(document.querySelectorAll('[aria-label]')).slice(0, 40).map((el) => el.getAttribute('aria-label')),
      localKeys: Object.keys(window.localStorage).slice(0, 20),
    }
  })
  console.log('SUMMARY ' + JSON.stringify(summary, null, 1).slice(0, 6000))
})
