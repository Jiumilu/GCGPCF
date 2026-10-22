import { expect, test, type Page } from '@playwright/test'
import {
  authenticate,
  mockChatSocket,
  mockHermesApi,
  TEST_ACCESS_KEY,
  TEST_ADMIN_ACCESS_KEY,
} from '../../../../../../GlobalCloud Studio/tests/e2e/fixtures'

const OUT = process.env.F010_OUT as string
function outDir(): string {
  if (!OUT) throw new Error('F010_OUT is required')
  return OUT
}

async function screenshot(page: Page, name: string) {
  await page.screenshot({ path: `${outDir()}/screens/${name}.png`, fullPage: false })
}

async function expectCoreShell(page: Page) {
  await expect(page.getByTestId('app-layout')).toHaveAttribute('data-layout', 'global-nav-smart-session-center-kds')
  await expect(page.getByTestId('app-layout')).toHaveAttribute('data-shell-columns', 'global-nav|smart-session|center-workspace|kds-workspace')
  await expect(page.getByTestId('global-nav-rail')).toHaveAttribute('data-shell-column', 'global-nav')
  await expect(page.getByTestId('smart-session-rail')).toHaveAttribute('data-shell-column', 'smart-session')
}

/** 核心任务：登录后进入任务页 → 切模型页 → 进入设置页，并始终保持四列壳。 */
async function completeCoreTask(page: Page) {
  await page.goto('/#/hermes/jobs')
  await expectCoreShell(page)
  await expect(page.getByTestId('global-nav-tasks')).toHaveClass(/active/)
  await expect(page.getByRole('heading', { name: /^(Scheduled Jobs|定时任务)$/ })).toBeVisible()

  await page.getByTestId('global-nav-models').click()
  await expect(page).toHaveURL(/#\/hermes\/models$/)
  await expect(page.getByTestId('global-nav-models')).toHaveClass(/active/)

  await page.getByTestId('global-nav-settings').click()
  await expect(page).toHaveURL(/#\/hermes\/settings$/)
  await expect(page.getByRole('heading', { name: /^(Settings|设置)$/ })).toBeVisible()
  await expectCoreShell(page)
  await expect(page.getByTestId('settings-workbench-entry')).toBeVisible()
}

test('multi_user_usability: super_admin 完成核心任务', async ({ page }) => {
  await authenticate(page, TEST_ACCESS_KEY, 'research')
  const api = await mockHermesApi(page)
  await mockChatSocket(page)

  await completeCoreTask(page)
  await screenshot(page, 'multi-user-super-admin-core-task')

  expect(api.unexpectedRequests).toEqual([])
})

test('multi_user_usability: admin 角色完成同一核心任务', async ({ page }) => {
  await authenticate(page, TEST_ADMIN_ACCESS_KEY, 'research')
  const api = await mockHermesApi(page, { userRole: 'admin' })
  await mockChatSocket(page)

  await completeCoreTask(page)
  await screenshot(page, 'multi-user-admin-core-task')

  expect(api.unexpectedRequests).toEqual([])
})

test('accessibility_status: 语义 landmark / 可访问名 / 键盘焦点可见 / 无焦点陷阱', async ({ page }) => {
  await authenticate(page, TEST_ACCESS_KEY, 'research')
  await mockHermesApi(page)
  await mockChatSocket(page)

  await page.goto('/#/hermes/settings')
  await expect(page.getByTestId('settings-workbench-entry')).toBeVisible()

  const staticAudit = await page.evaluate(() => {
    const visible = (el: Element) => {
      const rect = el.getBoundingClientRect()
      const style = getComputedStyle(el)
      return rect.width > 0 && rect.height > 0 && style.visibility !== 'hidden'
    }
    const nameOf = (el: Element) => {
      const aria = el.getAttribute('aria-label')?.trim()
      if (aria) return aria
      const labelledby = el.getAttribute('aria-labelledby')
      if (labelledby) {
        const text = labelledby.split(/\s+/)
          .map((id) => document.getElementById(id)?.textContent || '')
          .join(' ')
          .trim()
        if (text) return text
      }
      const text = (el.textContent || '').trim()
      if (text) return text
      const title = el.getAttribute('title')?.trim()
      if (title) return title
      const placeholder = el.getAttribute('placeholder')?.trim()
      if (placeholder) return placeholder
      return ''
    }
    const interactive = Array.from(document.querySelectorAll(
      'button, a[href], input, select, textarea, [role="button"], [role="tab"], [role="link"]',
    )).filter(visible)
    const unnamed = interactive
      .filter((el) => !nameOf(el))
      .map((el) => `${el.tagName.toLowerCase()}${el.getAttribute('data-testid') ? `[data-testid=${el.getAttribute('data-testid')}]` : ''}`)
    const ariaLabelCount = Array.from(document.querySelectorAll('[aria-label]')).filter(visible).length
    return {
      mainLandmark: Boolean(document.querySelector('main')),
      navCount: Array.from(document.querySelectorAll('nav')).filter(visible).length,
      ariaLabelCount,
      interactiveCount: interactive.length,
      unnamedCount: unnamed.length,
      unnamed: unnamed.slice(0, 10),
      lang: document.documentElement.lang,
    }
  })
  console.log('STATIC_A11Y ' + JSON.stringify(staticAudit))
  await screenshot(page, 'a11y-settings-first-view')

  const traversal: Array<Record<string, unknown>> = []
  let lastKey = ''
  let same = 0
  let maxSame = 0
  for (let i = 0; i < 18; i++) {
    await page.keyboard.press('Tab')
    const info = await page.evaluate(() => {
      const raw = document.activeElement as HTMLElement | null
      if (!raw || raw === document.body) {
        return { key: 'body', tag: 'body', testid: null, name: '', focusVisible: false, outline: '', shadow: '' }
      }
      const style = getComputedStyle(raw)
      const key = `${raw.tagName}:${raw.getAttribute('data-testid') || ''}:${(raw.textContent || '').trim().slice(0, 16)}`
      return {
        key,
        tag: raw.tagName.toLowerCase(),
        testid: raw.getAttribute('data-testid'),
        name: (raw.getAttribute('aria-label') || raw.textContent || '').trim().slice(0, 40),
        focusVisible: raw.matches(':focus-visible'),
        outline: `${style.outlineStyle} ${style.outlineWidth}`,
        shadow: style.boxShadow,
      }
    })
    traversal.push(info)
    if (info.key === lastKey) {
      same += 1
      maxSame = Math.max(maxSame, same)
    } else {
      same = 0
    }
    lastKey = String(info.key)
  }
  const distinct = new Set(traversal.map((item) => item.key)).size
  const focusVisibleCount = traversal.filter((item) => item.focusVisible === true).length
  const focusIndicatorCount = traversal.filter((item) => item.focusVisible === true
    && (String(item.outline) !== 'none 0px' || String(item.shadow) !== 'none')).length
  console.log('TAB_TRAVERSAL ' + JSON.stringify({ total: traversal.length, distinct, maxSame, focusVisibleCount, focusIndicatorCount }))
  console.log('TAB_TRAVERSAL_DETAIL ' + JSON.stringify(traversal))
  await screenshot(page, 'a11y-keyboard-focus-state')

  expect(staticAudit.mainLandmark).toBe(true)
  expect(staticAudit.ariaLabelCount).toBeGreaterThanOrEqual(3)
  expect(staticAudit.unnamedCount).toBe(0)
  expect(distinct).toBeGreaterThanOrEqual(5)
  expect(maxSame).toBeLessThanOrEqual(1)
  expect(focusVisibleCount).toBeGreaterThanOrEqual(5)
  expect(focusIndicatorCount).toBeGreaterThanOrEqual(5)
})

test('evidence_overexposure_gate: 默认界面可见文本不暴露机器字段', async ({ page }) => {
  await authenticate(page, TEST_ACCESS_KEY, 'research')
  await mockHermesApi(page)
  await mockChatSocket(page)

  const patterns: Array<{ name: string; re: RegExp }> = [
    { name: 'doc_id_field', re: /doc_id\s*[:=]/i },
    { name: 'evidence_field', re: /evidence\s*[:=]/i },
    { name: 'external_source', re: /external_source/i },
    { name: 'feature_id', re: /feature_id/i },
    { name: 'work_item_id', re: /work_item_id/i },
    { name: 'gpcf_doc_id', re: /GPCF-DOC-[0-9A-F]/i },
    { name: 'uuid', re: /\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b/i },
    { name: 'json_blob', re: /\{\s*"[a-z_]+"\s*:/i },
    { name: 'sha256', re: /\b[0-9a-f]{64}\b/i },
  ]
  const routes = ['/#/hermes/jobs', '/#/hermes/models', '/#/hermes/settings']
  const findings: Array<{ route: string; pattern: string; sample: string }> = []
  for (const route of routes) {
    await page.goto(route)
    await expect(page.getByTestId('app-layout')).toBeVisible()
    const text = await page.evaluate(() => document.body.innerText)
    for (const pattern of patterns) {
      const match = text.match(pattern.re)
      if (match) findings.push({ route, pattern: pattern.name, sample: match[0].slice(0, 80) })
    }
    await screenshot(page, `overexposure-${route.split('/').slice(-1)[0]}`)
  }
  console.log('OVEREXPOSURE_FINDINGS ' + JSON.stringify(findings))
  expect(findings).toEqual([])
})

test('task_flow_e2e_status: 项目会话任务流 + 不可用会话失败恢复', async ({ page }) => {
  await authenticate(page, TEST_ACCESS_KEY, 'research')
  await mockHermesApi(page)
  await mockChatSocket(page)

  await page.goto('/#/hermes/chat')
  await expectCoreShell(page)
  const typeList = page.getByTestId('session-create-type-list')
  if (await typeList.count() === 0) {
    await page.getByTestId('session-rail-create').click()
  }
  await expect(typeList).toBeVisible()
  await page.getByTestId('session-create-type-project').click()
  await expect(page).toHaveURL(/#\/hermes\/session\//)
  await expect(page.getByTestId('workspace-status-signal-type')).toHaveAttribute('title', '当前会话类型: 项目会话')
  await screenshot(page, 'task-flow-project-session-created')

  await page.goto('/#/hermes/session/unavailable-project-session?profile=research&sessionType=project')
  await expect(page.getByTestId('session-route-unavailable')).toBeVisible()
  await expect(page.getByTestId('session-route-unavailable')).toContainText('暂时无法打开此会话')
  await expect(page.getByTestId('session-route-unavailable-target')).toContainText('unavailable-project-session')
  await expect(page.getByTestId('chat-panel')).toHaveCount(0)
  await screenshot(page, 'task-flow-failure-unavailable-session')

  await page.getByTestId('session-route-return-list').click()
  await expect(page).toHaveURL(/#\/hermes\/chat$/)
  await expect(page.getByTestId('smart-session-rail')).toBeVisible()
  await screenshot(page, 'task-flow-recovered-session-list')
})
