---
doc_id: GPCF-DOC-BBB53AE37E
title: Instructions
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/logs/run1-raw-fail/error-context.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/logs/run1-raw-fail/error-context.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: f036-pkc-taskflow.spec.ts >> task_flow_e2e_status: F-036 WAE 登录 → PKC 侧栏入口 → pkc-intake 候选页 → 返回工作台
- Location: ../GlobalCloud GPCF/features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/f036-pkc-taskflow.spec.ts:29:5

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByTestId('account-menu-trigger')
Expected: visible
Timeout: 30000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" getByTestId('account-menu-trigger') with timeout 30000ms
  - waiting for getByTestId('account-menu-trigger')
    - waiting for "http://127.0.0.1:4301/" navigation to finish...
    - navigated to "http://127.0.0.1:4301/"

```

```yaml
- img
- heading "页面出现错误" [level=4]
- text: 关键
- paragraph: CONSOLE_COLORS is not defined
- heading "解决建议:" [level=4]
- list:
  - listitem: • 这是一个临时性错误
  - listitem: • 重试通常可以解决问题
  - listitem: • 如果问题持续，请联系技术支持
- button "重试 (0/3)":
  - img
  - text: 重试 (0/3)
- button "返回主页":
  - img
  - text: 返回主页
- button "刷新页面":
  - img
  - text: 刷新页面
- paragraph: "错误ID: error_1792670630376_vhoyfetkh"
- group:
  - img
  - text: 调试信息
```

# Test source

```ts
  1   | /**
  2   |  * F-036 task_flow E2E：登录 → 侧栏 PKC 入口（requires pkc）→ pkc-intake 候选页 → 返回工作台。
  3   |  *
  4   |  * 断言口径（与 F-036 acceptance 对应）：
  5   |  *   ① 真实登录（隔离临时 IdP，口令仅 env 注入，不写入证据）；
  6   |  *   ② system-admin 可见侧栏一级入口 `app-nav-pkc`；
  7   |  *   ③ 进入 `/global-cloud-workbench/pkc`：候选态徽章 / 非声明文案可见；机器字段不上屏；
  8   |  *   ④ 受控嵌入默认不启用（无 iframe）、页面不接受外部请求（监听 request）；
  9   |  *   ⑤ 返回工作台后 shell 正常（欢迎回来）；
  10  |  *   ⑥ 全程 0 pageerror；console error 仅允许登录前 `/me` 401 会话探测（预期）。
  11  |  */
  12  | import { expect, test, type Page } from '@playwright/test'
  13  | import { mkdirSync, writeFileSync } from 'node:fs'
  14  | 
  15  | const OUT = process.env.F036_OUT as string
  16  | const USER = process.env.F036_USER as string
  17  | const PASSWORD = process.env.F036_PASSWORD as string
  18  | const NEW_PASSWORD = process.env.F036_NEW_PASSWORD as string
  19  | const BASE_URL = process.env.F036_BASE_URL as string
  20  | 
  21  | function requireEnv(): void {
  22  |   if (!OUT || !USER || !PASSWORD || !NEW_PASSWORD || !BASE_URL) {
  23  |     throw new Error('F036_OUT / F036_USER / F036_PASSWORD / F036_NEW_PASSWORD / F036_BASE_URL are required')
  24  |   }
  25  | }
  26  | 
  27  | const EXTERNAL_ALLOW = /^(data:|blob:|about:|https?:\/\/(127\.0\.0\.1|localhost):\d+)/
  28  | 
  29  | test('task_flow_e2e_status: F-036 WAE 登录 → PKC 侧栏入口 → pkc-intake 候选页 → 返回工作台', async ({ page }) => {
  30  |   requireEnv()
  31  |   const steps: Array<Record<string, unknown>> = []
  32  |   const pageErrors: string[] = []
  33  |   const consoleErrors: string[] = []
  34  |   const externalRequests: string[] = []
  35  |   page.on('pageerror', (error) => {
  36  |     pageErrors.push(String(error).slice(0, 400))
  37  |     console.log('PAGE_ERROR ' + String(error).slice(0, 400))
  38  |   })
  39  |   page.on('console', (message) => {
  40  |     if (message.type() === 'error') consoleErrors.push(message.text().slice(0, 300))
  41  |   })
  42  |   page.on('request', (request) => {
  43  |     const url = request.url()
  44  |     if (!EXTERNAL_ALLOW.test(url)) externalRequests.push(url.slice(0, 300))
  45  |   })
  46  |   const record = (step: string, detail: Record<string, unknown> = {}) => {
  47  |     steps.push({ step, at: new Date().toISOString(), ...detail })
  48  |     console.log('STEP ' + JSON.stringify({ step, ...detail }))
  49  |   }
  50  |   const shot = async (name: string) => page.screenshot({ path: `${OUT}/screens/${name}.png`, fullPage: false })
  51  | 
  52  |   // 1) 登录页（真实产品 UI，无 mock）
  53  |   await page.goto('/')
  54  |   await expect(page.getByTestId('login-space-greenchain')).toBeVisible()
  55  |   await shot('f036-flow-01-login')
  56  |   record('login-page-loaded', { url: page.url() })
  57  | 
  58  |   // 2) 真实登录（隔离临时 IdP；口令 env 注入）
  59  |   await page.locator('input').nth(0).fill(USER)
  60  |   await page.locator('input[type="password"]').first().fill(PASSWORD)
  61  |   await page.getByRole('button', { name: /登录/ }).first().click()
  62  |   await page.waitForTimeout(2500)
  63  | 
  64  |   // 3) 首登强制改密（bootstrap 管理员 mustChangePassword=true）
  65  |   const forcedChange = page.getByText('请先修改初始口令')
  66  |   if (await forcedChange.isVisible({ timeout: 10000 }).catch(() => false)) {
  67  |     await shot('f036-flow-02-forced-password-change')
  68  |     record('forced-password-change-page', {})
  69  |     const pw = page.locator('input[type="password"]')
  70  |     await pw.nth(0).fill(PASSWORD)
  71  |     await pw.nth(1).fill(NEW_PASSWORD)
  72  |     await pw.nth(2).fill(NEW_PASSWORD)
  73  |     await page.getByRole('button', { name: /保存新口令并继续/ }).first().click()
  74  |     record('password-changed', { forced: true })
  75  |   } else {
  76  |     record('login-without-forced-change', { note: '账号已完成首登改密（复跑路径）' })
  77  |   }
  78  | 
  79  |   // 4) 工作台（登录成功）
> 80  |   await expect(page.getByTestId('account-menu-trigger')).toBeVisible({ timeout: 30000 })
      |                                                          ^ Error: expect(locator).toBeVisible() failed
  81  |   await expect(page.getByText(/欢迎回来/).first()).toBeVisible()
  82  |   await shot('f036-flow-03-workbench')
  83  |   record('workbench-home', {})
  84  | 
  85  |   // 5) 侧栏一级入口 PKC（requires pkc，system-admin 可见）
  86  |   const pkcNav = page.getByTestId('app-nav-pkc')
  87  |   await expect(pkcNav).toBeVisible({ timeout: 15000 })
  88  |   await shot('f036-flow-04-sidebar-pkc-entry')
  89  |   record('sidebar-pkc-visible', { testId: 'app-nav-pkc' })
  90  | 
  91  |   // 6) 进入 pkc-intake 候选页
  92  |   await pkcNav.click()
  93  |   await expect(page).toHaveURL(/\/global-cloud-workbench\/pkc/, { timeout: 20000 })
  94  |   const pageRoot = page.getByTestId('pkc-intake-page')
  95  |   await expect(pageRoot).toBeVisible()
  96  |   await record('pkc-page-opened', { url: page.url() })
  97  | 
  98  |   // 7) 候选态 / 非声明文案可见
  99  |   await expect(page.getByText('PKC 知识工作台（候选接入）').first()).toBeVisible()
  100 |   await expect(page.getByText(/不声明 PKC 已接入/).first()).toBeVisible()
  101 |   const bodyText = await page.evaluate(() => document.body.innerText)
  102 |   record('candidate-and-nonclaims-visible', {
  103 |     hasCandidateBadge: bodyText.includes('候选'),
  104 |     hasNonClaim: bodyText.includes('不声明 PKC 已接入'),
  105 |   })
  106 | 
  107 |   // 8) 证据展示门禁：机器字段不上屏
  108 |   const machineFields = ['packageId', 'evidenceRefs', 'contentDigest', 'status_ceiling', 'cost_tier']
  109 |   const leaked = machineFields.filter((field) => bodyText.includes(field))
  110 |   record('no-machine-fields', { checked: machineFields, leaked })
  111 |   expect(leaked).toEqual([])
  112 | 
  113 |   // 9) 受控嵌入默认不启用：无 iframe，dry-run 说明可见；页面不接受外部请求
  114 |   await expect(page.getByTestId('pkc-embed-disabled')).toBeVisible()
  115 |   expect(await page.getByTestId('pkc-embed-frame').count()).toBe(0)
  116 |   await shot('f036-flow-05-pkc-candidate-page')
  117 |   record('embedment-default-off', { frameCount: 0, externalRequests: externalRequests.length })
  118 |   expect(externalRequests).toEqual([])
  119 | 
  120 |   // 10) 返回工作台
  121 |   await page.getByTestId('app-nav-feedback').click()
  122 |   await expect(page.getByText(/欢迎回来/).first()).toBeVisible({ timeout: 20000 })
  123 |   await shot('f036-flow-06-return-workbench')
  124 |   record('return-workbench', { url: page.url() })
  125 | 
  126 |   mkdirSync(`${OUT}/logs`, { recursive: true })
  127 |   writeFileSync(`${OUT}/logs/taskflow-assertions.json`, JSON.stringify({
  128 |     baseURL: BASE_URL,
  129 |     account: 'F-036 隔离临时 system-admin（口令 env 注入，未写入证据）',
  130 |     steps,
  131 |     pageErrors,
  132 |     consoleErrors,
  133 |     externalRequests,
  134 |     result: 'pass',
  135 |   }, null, 2))
  136 |   console.log('TASKFLOW_RESULT ' + JSON.stringify({
  137 |     steps: steps.length,
  138 |     pageErrors: pageErrors.length,
  139 |     consoleErrors: consoleErrors.length,
  140 |     externalRequests: externalRequests.length,
  141 |   }))
  142 | 
  143 |   expect(pageErrors).toEqual([])
  144 |   expect(steps.length).toBeGreaterThanOrEqual(10)
  145 | })
  146 | 
```
