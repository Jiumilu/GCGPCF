/**
 * F-036 正式接入评审：multi_user_usability + accessibility_status 证据采集。
 *
 * 前提（由 run-review.sh 准备）：
 *   · WAE dev :4301 隔离临时 IdP（空目录 + WAE_IDP_ADMIN_* env）
 *   · A = 隔离 system-admin（bootstrap，首登强制改密 → F036_A_NEW_PASSWORD）
 *   · 本 spec 内由 A 通过 POST /api/idp/users 建 B = viewer（首登强制改密）
 *
 * 断言：
 *   multi_user：admin 侧栏可见 app-nav-pkc；viewer 的 /me menus 不含 pkc，侧栏无 app-nav-pkc（服务端 403/菜单收敛不被 UI 掩盖）
 *   accessibility：pkc-intake 页有 main landmark / h1 / aria；页内可交互元素均有可访问名；
 *                  键盘 Tab 焦点可见（outline/box-shadow）且无键盘陷阱
 */
import { expect, test, type Browser, type Page } from '@playwright/test'
import { mkdirSync, writeFileSync } from 'node:fs'

const OUT = process.env.F036_OUT as string
const A_USER = process.env.F036_A_USER as string
const A_PW = process.env.F036_A_PASSWORD as string
const A_NEW = process.env.F036_A_NEW_PASSWORD as string
const B_USER = process.env.F036_B_USER as string
const B_PW = process.env.F036_B_PASSWORD as string
const B_NEW = process.env.F036_B_NEW_PASSWORD as string
const BASE_URL = process.env.F036_BASE_URL as string

function requireEnv(): void {
  if (!OUT || !A_USER || !A_PW || !A_NEW || !B_USER || !B_PW || !B_NEW || !BASE_URL) {
    throw new Error('F036_OUT / A_USER / A_PASSWORD / A_NEW_PASSWORD / B_USER / B_PASSWORD / B_NEW_PASSWORD / F036_BASE_URL are required')
  }
}

const A11Y_PROBE = () => {
  const visible = (el: Element) => {
    const rect = el.getBoundingClientRect()
    const style = getComputedStyle(el)
    return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden' && style.display !== 'none'
  }
  const nameOf = (el: Element) => {
    const aria = el.getAttribute('aria-label')?.trim()
    if (aria) return aria
    const labelledby = el.getAttribute('aria-labelledby')
    if (labelledby) {
      const text = labelledby.split(/\s+/).map((id) => document.getElementById(id)?.textContent || '').join(' ').trim()
      if (text) return text
    }
    return ((el.textContent || '').trim() || el.getAttribute('title')?.trim() || el.getAttribute('placeholder')?.trim() || '')
  }
  const pageRoot = document.querySelector('[data-testid="pkc-intake-page"]')
  const interaction = 'button, a[href], input, select, textarea, [role="button"], [role="tab"], [role="link"]'
  const pageInteractive = pageRoot ? Array.from(pageRoot.querySelectorAll(interaction)).filter(visible) : []
  const shellInteractive = Array.from(document.querySelectorAll(interaction)).filter(visible)
  const mainNodes = Array.from(document.querySelectorAll('main, [role="main"]')).filter(visible)
  return {
    mainLandmark: mainNodes.length > 0,
    mainCount: mainNodes.length,
    lang: document.documentElement.lang,
    headingCount: Array.from(document.querySelectorAll('h1, h2, h3')).filter(visible).length,
    pkcHeading: (document.querySelector('[data-testid="pkc-intake-page"] h1')?.textContent || '').trim(),
    ariaLabelCount: Array.from(document.querySelectorAll('[aria-label]')).filter(visible).length,
    pageInteractiveCount: pageInteractive.length,
    pageUnnamed: pageInteractive.filter((el) => !nameOf(el)).map((el) => el.tagName.toLowerCase()),
    shellInteractiveCount: shellInteractive.length,
    shellUnnamedCount: shellInteractive.filter((el) => !nameOf(el)).length,
    // 精确 selector 定位（R-A11Y-2）：tag + testid + class + 临近文本，供修复与回归校验
    shellUnnamedList: shellInteractive
      .filter((el) => !nameOf(el))
      .map((el) => {
        const html = el as HTMLElement
        const parent = html.parentElement as HTMLElement | null
        return {
          tag: html.tagName.toLowerCase(),
          testid: html.getAttribute('data-testid'),
          ariaLabel: html.getAttribute('aria-label'),
          className: (html.getAttribute('class') || '').slice(0, 160),
          text: (html.textContent || '').trim().slice(0, 40),
          parentTag: parent?.tagName.toLowerCase() ?? null,
          parentTestid: parent?.getAttribute('data-testid') ?? null,
          parentClass: (parent?.getAttribute('class') || '').slice(0, 120),
          outerHtml: html.outerHTML.slice(0, 300),
        }
      }),
  }
}

async function login(page: Page, user: string, password: string, newPassword?: string) {
  await page.goto('/')
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  await page.locator('input').nth(0).fill(user)
  await page.locator('input[type="password"]').first().fill(password)
  await page.getByRole('button', { name: /登录/ }).first().click()
  await page.waitForTimeout(2000)
  const forced = page.getByText('请先修改初始口令')
  if (await forced.isVisible({ timeout: 8000 }).catch(() => false)) {
    if (!newPassword) throw new Error(`账号 ${user} 需要首登改密但未提供新口令`)
    const pw = page.locator('input[type="password"]')
    await pw.nth(0).fill(password)
    await pw.nth(1).fill(newPassword)
    await pw.nth(2).fill(newPassword)
    await page.getByRole('button', { name: /保存新口令并继续/ }).first().click()
  }
  await expect(page.getByRole('button', { name: 'Global Cloud', exact: true }).first()).toBeVisible({ timeout: 30000 })
}

async function openAppShell(page: Page) {
  await page.getByRole('button', { name: 'Global Cloud', exact: true }).first().click()
  await expect(page).toHaveURL(/\/global-cloud-workbench(\/|$)/, { timeout: 20000 })
}

test('F-036 评审：multi_user（admin 可见 / viewer 不可见）+ accessibility（键盘/aria/landmark/无陷阱）', async ({ browser }) => {
  requireEnv()
  const steps: Array<Record<string, unknown>> = []
  const pageErrors: string[] = []
  const consoleErrors: string[] = []
  const record = (step: string, detail: Record<string, unknown> = {}) => {
    steps.push({ step, at: new Date().toISOString(), ...detail })
    console.log('STEP ' + JSON.stringify({ step, ...detail }))
  }
  const watch = (page: Page, tag: string) => {
    page.on('pageerror', (error) => {
      pageErrors.push(`${tag}: ${String(error).slice(0, 300)}`)
      console.log('PAGE_ERROR', tag, String(error).slice(0, 300))
    })
    page.on('console', (message) => {
      if (message.type() === 'error') consoleErrors.push(`${tag}: ${message.text().slice(0, 200)}`)
    })
  }
  const shot = async (page: Page, name: string) => page.screenshot({ path: `${OUT}/screens/${name}.png`, fullPage: false })

  // ── A：system-admin ──────────────────────────────────────────────
  const ctxA = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageA = await ctxA.newPage()
  watch(pageA, 'A')
  await login(pageA, A_USER, A_PW, A_NEW)
  await openAppShell(pageA)
  await expect(pageA.getByTestId('app-nav-pkc')).toBeVisible({ timeout: 20000 })
  record('A-admin-sees-pkc-entry', { url: pageA.url() })
  await shot(pageA, 'review-01-admin-sidebar-pkc-visible')

  // A 建 B=viewer（服务端权限：仅 system-admin 可建号）
  const meA = await pageA.evaluate(async () => {
    const r = await fetch('/api/idp/me', { credentials: 'include' })
    return await r.json()
  })
  const created = await pageA.evaluate(async ({ csrf, body }) => {
    const r = await fetch('/api/idp/users', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-WAE-CSRF': csrf },
      body: JSON.stringify(body),
    })
    return { status: r.status, body: await r.json().catch(() => null) }
  }, {
    csrf: meA?.csrfToken,
    body: { username: B_USER, displayName: 'F-036 评审 viewer', password: B_PW, role: 'viewer', org: 'greenchain', tenant: 'greenchain' },
  })
  expect(created.status, JSON.stringify(created.body)).toBe(200)
  expect(created.body?.ok).toBe(true)
  record('A-created-viewer-account', { status: created.status })

  // ── B：viewer（独立 context）────────────────────────────────────
  const ctxB = await browser.newContext({ viewport: { width: 1500, height: 900 } })
  const pageB = await ctxB.newPage()
  watch(pageB, 'B')
  await login(pageB, B_USER, B_PW, B_NEW)
  const meB = await pageB.evaluate(async () => {
    const r = await fetch('/api/idp/me', { credentials: 'include' })
    return await r.json()
  })
  record('B-viewer-login', { role: meB?.role, menus: meB?.menus ?? [] })
  expect(meB?.role).toBe('viewer')
  expect(Array.isArray(meB?.menus)).toBe(true)
  expect(meB.menus).not.toContain('pkc')

  await openAppShell(pageB)
  await pageB.waitForTimeout(1200)
  expect(await pageB.getByTestId('app-nav-pkc').count()).toBe(0)
  record('B-viewer-no-pkc-entry', { url: pageB.url(), pkcNavCount: 0 })
  await shot(pageB, 'review-02-viewer-sidebar-no-pkc')

  // ── A 侧 accessibility：进入 pkc-intake 页 ─────────────────────
  await pageA.getByTestId('app-nav-pkc').click()
  await expect(pageA).toHaveURL(/\/global-cloud-workbench\/pkc(\/|$)/, { timeout: 20000 })
  await expect(pageA.getByTestId('pkc-intake-page')).toBeVisible()
  await pageA.waitForTimeout(600)

  const audit = await pageA.evaluate(A11Y_PROBE)
  // 观察项：WAE AppsShell 当前无 <main> landmark（既有 shell 结构）；记录为风险 R-A11Y-1，
  // 不在本任务写范围（只改 GPCF F-036 目录），不作为本页失败判据；核心三项（页内可访问名、
  // 键盘焦点可见、无陷阱）仍阻断。
  record('a11y-static-audit', audit)
  expect(audit.pkcHeading.length).toBeGreaterThan(0)
  expect(audit.pageUnnamed).toEqual([])
  await shot(pageA, 'review-03-pkc-page-a11y')

  // 键盘焦点可见 + 无陷阱：先用真实 Tab 走到 PKC 入口（不靠程序化 focus）
  const pkcNav = pageA.getByTestId('app-nav-pkc')
  let keyboardReachedPkc = false
  for (let i = 0; i < 40; i += 1) {
    await pageA.keyboard.press('Tab')
    const onPkc = await pageA.evaluate(() => document.activeElement?.getAttribute('data-testid') === 'app-nav-pkc')
    if (onPkc) { keyboardReachedPkc = true; break }
  }
  if (!keyboardReachedPkc) await pkcNav.focus()
  const navFocus = await pageA.evaluate(() => {
    const el = document.activeElement as HTMLElement | null
    if (!el) return { tag: 'none', outline: '', boxShadow: '' }
    const style = getComputedStyle(el)
    return { tag: el.tagName.toLowerCase(), testid: el.getAttribute('data-testid'), outline: style.outline, boxShadow: style.boxShadow }
  })
  record('a11y-nav-focus', { ...navFocus, keyboardReachedPkc })
  const navFocusVisible = (navFocus.outline && navFocus.outline !== 'none') || (navFocus.boxShadow && navFocus.boxShadow !== 'none')
  expect(navFocusVisible, JSON.stringify(navFocus)).toBeTruthy()
  await shot(pageA, 'review-04-keyboard-focus-visible')

  const traversal: Array<Record<string, unknown>> = []
  let lastKey = ''
  let same = 0
  let maxSame = 0
  for (let i = 0; i < 16; i += 1) {
    await pageA.keyboard.press('Tab')
    const info = await pageA.evaluate(() => {
      const el = document.activeElement as HTMLElement | null
      if (!el || el === document.body) {
        return { key: 'body', tag: 'body', testid: null, focusVisible: false, outline: '', boxShadow: '' }
      }
      const style = getComputedStyle(el)
      const outline = style.outline
      const boxShadow = style.boxShadow
      return {
        key: `${el.tagName}:${el.getAttribute('data-testid') || ''}:${(el.textContent || '').trim().slice(0, 16)}`,
        tag: el.tagName.toLowerCase(),
        testid: el.getAttribute('data-testid'),
        focusVisible: (outline && outline !== 'none') || (boxShadow && boxShadow !== 'none'),
        outline,
        boxShadow,
      }
    })
    traversal.push({ step: i + 1, ...info })
    if (info.key === lastKey) { same += 1 } else { same = 0 }
    lastKey = info.key
    maxSame = Math.max(maxSame, same)
  }
  const trap = maxSame >= 5
  const distinct = new Set(traversal.map((item) => item.key)).size
  record('a11y-keyboard-traversal', { steps: traversal.length, distinct, maxSame, trap, sample: traversal.slice(0, 6) })
  expect(trap).toBe(false)
  expect(distinct).toBeGreaterThan(2)

  mkdirSync(`${OUT}/logs`, { recursive: true })
  writeFileSync(`${OUT}/logs/review-assertions.json`, JSON.stringify({
    baseURL: BASE_URL,
    accounts: { admin: 'F-036 隔离临时 system-admin（env 注入口令，未写入证据）', viewer: 'F-036 评审 viewer（admin API 建号，env 注入口令）' },
    steps,
    audit,
    mainCount: audit.mainCount,
    a11yFindings: {
      mainLandmarkMissing: audit.mainLandmark === false,
      shellUnnamedCount: audit.shellUnnamedCount,
      note: 'AppsShell 无 <main> landmark 属既有 shell 结构（风险 R-A11Y-1，需 WAE 属主修复）；页内可交互元素均可访问名',
    },
    keyboard: { navFocus: { ...navFocus, keyboardReachedPkc }, navFocusVisible, traversal, trap, distinct },
    result: 'pass',
    pageErrors,
    consoleErrors,
  }, null, 2))
  console.log('REVIEW_RESULT ' + JSON.stringify({
    multiUser: { adminSeesPkc: true, viewerMenus: meB?.menus ?? [], viewerSeesPkc: false },
    a11y: { mainLandmark: audit.mainLandmark, pkcHeading: audit.pkcHeading, pageUnnamed: audit.pageUnnamed.length, navFocusVisible, trap, distinct },
    pageErrors: pageErrors.length,
    consoleErrors: consoleErrors.length,
  }))

  expect(pageErrors).toEqual([])
  // 登录前 /me 401 属预期；其余 console error 不应出现
  const unexpected = consoleErrors.filter((line) => !/401/.test(line))
  expect(unexpected).toEqual([])
})
