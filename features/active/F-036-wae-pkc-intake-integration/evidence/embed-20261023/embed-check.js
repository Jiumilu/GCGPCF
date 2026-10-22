// 复现：PKC dev :5174 + WAE dev :4300（apps/wame/.env.local 配置 bypass/embed URL）
// 用法：npm i playwright-core && node embed-check.js
const { chromium } = require('playwright-core');

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  const external = [];
  page.on('request', (r) => {
    const u = r.url();
    if (!u.startsWith('http://127.0.0.1:4300') && !u.startsWith('http://127.0.0.1:5174') && !u.startsWith('data:')) external.push(u);
  });
  await page.goto('http://127.0.0.1:4300/global-cloud-workbench/pkc/pkc-intake', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(4000);

  const frameBefore = await page.locator('[data-testid="pkc-embed-frame"]').count();
  const btn = page.locator('[data-testid="pkc-embed-enable"]');
  const btnCount = await btn.count();
  let clicked = false;
  if (btnCount) { await btn.click(); clicked = true; await page.waitForTimeout(4000); }

  const frameAfter = await page.locator('[data-testid="pkc-embed-frame"]').count();
  const src = frameAfter ? await page.locator('[data-testid="pkc-embed-frame"]').getAttribute('src') : null;
  const pkc = page.frames().find((f) => f.url().startsWith('http://127.0.0.1:5174'));
  let frameText = '';
  if (pkc) { try { frameText = (await pkc.locator('body').innerText()).slice(0, 200); } catch (e) { frameText = `read failed: ${e.message}`; } }

  await page.screenshot({ path: 'after-embed-pkc-home.png', fullPage: true });
  console.log(JSON.stringify({ frameBefore, btnCount, clicked, frameAfter, src, frameText, externalRequests: external }, null, 2));
  await browser.close();
})().catch((e) => { console.error(e.message); process.exit(1); });
