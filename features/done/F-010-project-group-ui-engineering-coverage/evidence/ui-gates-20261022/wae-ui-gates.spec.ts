import { expect, test, type Page } from '@playwright/test'

const OUT = process.env.F010_OUT as string
function outDir(): string {
  if (!OUT) throw new Error('F010_OUT is required')
  return OUT
}

async function screenshot(page: Page, name: string) {
  await page.screenshot({ path: `${outDir()}/screens/${name}.png`, fullPage: false })
}

async function openLoginEntry(page: Page) {
  await page.goto('/')
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  await expect(page.getByTestId('login-space-was')).toBeVisible()
}

test('accessibility_status: WAE 统一身份入口键盘焦点 / aria 语义 / 无焦点陷阱', async ({ page }) => {
  await openLoginEntry(page)

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
    return {
      mainLandmark: Boolean(document.querySelector('main')),
      ariaLabelCount: Array.from(document.querySelectorAll('[aria-label]')).filter(visible).length,
      interactiveCount: interactive.length,
      unnamedCount: unnamed.length,
      unnamed: unnamed.slice(0, 10),
      lang: document.documentElement.lang,
      headings: Array.from(document.querySelectorAll('h1, h2, h3')).slice(0, 10).map((el) => (el.textContent || '').trim().slice(0, 40)),
    }
  })
  console.log('STATIC_A11Y ' + JSON.stringify(staticAudit))
  await screenshot(page, 'wae-a11y-login-first-view')

  const traversal: Array<Record<string, unknown>> = []
  let lastKey = ''
  let same = 0
  let maxSame = 0
  for (let i = 0; i < 16; i++) {
    await page.keyboard.press('Tab')
    const info = await page.evaluate(() => {
      const raw = document.activeElement as HTMLElement | null
      if (!raw || raw === document.body) {
        return { key: 'body', tag: 'body', testid: null, focusVisible: false, outline: '', shadow: '' }
      }
      const style = getComputedStyle(raw)
      return {
        key: `${raw.tagName}:${raw.getAttribute('data-testid') || ''}:${(raw.textContent || '').trim().slice(0, 16)}`,
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
  await screenshot(page, 'wae-a11y-keyboard-focus-state')

  expect(staticAudit.lang).toMatch(/^zh/i)
  expect(staticAudit.ariaLabelCount).toBeGreaterThanOrEqual(3)
  expect(staticAudit.unnamedCount).toBe(0)
  expect(distinct).toBeGreaterThanOrEqual(5)
  expect(maxSame).toBeLessThanOrEqual(1)
  expect(focusVisibleCount).toBeGreaterThanOrEqual(5)
  expect(focusIndicatorCount).toBeGreaterThanOrEqual(5)
})

test('evidence_overexposure_gate: WAE 统一身份入口默认可见文本不暴露机器字段', async ({ page }) => {
  await openLoginEntry(page)

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
  const text = await page.evaluate(() => document.body.innerText)
  const findings = patterns
    .map((pattern) => ({ pattern: pattern.name, match: text.match(pattern.re)?.[0]?.slice(0, 80) }))
    .filter((item) => item.match)
  const environmentLabels = ['环境 开发 · :4300', '版本 v0.1.0', '身份服务 /api/idp']
    .filter((label) => text.includes(label))
  console.log('OVEREXPOSURE_FINDINGS ' + JSON.stringify(findings))
  console.log('ENVIRONMENT_LABELS_OBSERVED ' + JSON.stringify(environmentLabels))
  await screenshot(page, 'wae-overexposure-login-default')

  expect(findings).toEqual([])
})

test('task_flow_partial: 空间切换与登录校验失败恢复（无真实账号，未完成登录）', async ({ page }) => {
  await openLoginEntry(page)

  await page.getByTestId('login-space-was').click()
  await expect(page.getByText(/进入\s*世界资产/).first()).toBeVisible()
  await screenshot(page, 'wae-taskflow-space-switch')

  const submit = page.getByRole('button', { name: /登录/ }).first()
  await submit.click()
  await expect(page.getByText('请填写账号与口令').first()).toBeVisible()
  await screenshot(page, 'wae-taskflow-login-validation-failure')

  await page.getByTestId('login-space-greenchain').click()
  await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  await expect(page.locator('input').first()).toBeVisible()
  await expect(page.locator('input[type="password"]').first()).toBeVisible()
  await screenshot(page, 'wae-taskflow-recovered-usable-form')

  expect(await page.locator('input').first().isEditable()).toBe(true)
})
