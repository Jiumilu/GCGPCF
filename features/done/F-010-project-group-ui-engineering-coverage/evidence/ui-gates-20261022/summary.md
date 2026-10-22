---
doc_id: GPCF-DOC-B6A1B60F9D
title: F-010 四项 UI gate 证据补采（2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-010-project-group-ui-engineering-coverage/evidence/ui-gates-20261022/summary.md
source_path: features/done/F-010-project-group-ui-engineering-coverage/evidence/ui-gates-20261022/summary.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-010 四项 UI gate 证据补采（2026-10-22）

- 任务：task-17 / PJ（Lead 指派）—— 为 `multi_user_usability` / `task_flow_e2e_status` / `accessibility_status` / `evidence_overexposure_gate` 补采真实证据。
- 执行时间：2026-10-22 16:36–17:35（+08:00）。
- 执行边界：只改本 Feature 目录；未 commit/push；未改 Studio/WAE 代码；未创建或重置任何凭据；WAE dev server 为验证临时启动并已停止；无状态提升。

## 0. 结论表

| gate | 本轮取值 | 依据摘要 |
|---|---|---|
| `multi_user_usability` | **pass（2026-10-22 追加，task-19，老卢授权双临时角色）** | WAE 隔离临时 IdP 建 2 账号：A=system-admin（16 menus）/ B=viewer（4 menus）；A 可加载用户目录（200，2/2 账号表），B 被拒（403「需要 system-admin 角色」+ 页面「无权限：用户目录仅体系管理员可见」）；双方退出后 `/me` 均 401（会话隔离）。见 §2.6。 |
| `task_flow_e2e_status` | **pass（2026-10-22 追加，task-18）** | WAE 统一入口真实完整任务流：登录页 → 失败恢复（空提交校验错误）→ 登录 → 首登强制改密 → 工作台「欢迎回来」→ 进入项目管理器弹层 → 关闭返回主页 → 账号菜单退出 → 回登录页；Playwright **1 passed**（9 steps / 0 pageerror）。Studio 侧既有 E2E 仍因 HEAD 回归 2 failed（见 §1），不用于 pass。 |
| `accessibility_status` | **pass** | WAE 统一身份入口（真实 UI，无 mock）真机键盘实测：16 次 Tab、10 个不同焦点目标、15/16 `:focus-visible` 且 outline 2px、0 个无名称交互元素、`main` landmark 存在、`lang=zh-CN`。 |
| `evidence_overexposure_gate` | **pass** | WAE 统一身份入口默认可见文本对 9 类机器字段正则 **0 命中**；观测到 3 项工程环境标注（非 doc_id/evidence/json/内部 ID），单列不记为违规。 |

`status_ceiling` 保持 `partial`；Feature 保持 `active`。

## 1. 阻断事实：Studio HEAD 运行时回归（应用空白）

- 现象：Studio 以 `npx vite` 启动后访问 `/#/hermes/jobs`、`/#/hermes/settings` 等任何登录后路由，页面为**空白**（截图 `screens/studio-head-blank-app.png`），`body.innerText` 为空。
- 运行时错误（`logs/studio-probe.log`）：

```text
PAGE_ERROR Error: No match for
 {"name":"gcworld.organizations","params":{}}
    at createRouterError (... vue-router ...)
    at useLink (...)
    at setup (...)
  at <RouterLink to= {name: gcworld.organizations} ... > at <AppSidebar ... >
```

- 根因（A 级，文件级核对）：
  - HEAD `b02d837e`「refactor(studio): GCWorld 组织世界纵切迁出至独立项目 GlobalCloud World」在 `packages/client/src/router/index.ts` 删除 5 行（注销 `gcworld.*` 路由）；
  - `packages/client/src/components/layout/AppSidebar.vue:626` 仍渲染 `:to="{ name: 'gcworld.organizations' }"`；
  - 路由不存在 → `RouterLink` 在 setup 阶段抛错 → `AppSidebar` 所在整棵树崩溃 → 应用空白；
  - `App.vue:39,57` 仍保留 `gcworld.organizations` 判断（不致命，但同属未清理引用）。
- 影响：**Studio 当前任何登录后 UI 与 E2E 均不可用**（非本 Feature 引入）。修复需改 Studio 仓，超出本任务「只改 F-010 目录」边界，未修复。
- 复现命令：`cd "GlobalCloud Studio" && npx playwright test --config <本目录>/playwright.gates.config.ts --grep "probe studio shell render"`（日志已存 `logs/studio-probe.log`）。

## 2. 命令、结果与证据

### 2.1 accessibility_status（pass）

- 被测：`GlobalCloud WAE` 统一身份入口（真实产品 UI，无 mock），`http://localhost:4300/`。
- 启动：`cd "GlobalCloud WAE" && pnpm dev`（Vite `:4300`，验证后已停止）。
- 命令：`cd "GlobalCloud Studio" && F010_OUT=<本目录> npx playwright test --config <本目录>/playwright.wae.config.ts --grep "accessibility_status: WAE"` → **1 passed**。
- 真机数据（`logs/run-wae-gates.log`）：

```text
STATIC_A11Y {"mainLandmark":true,"ariaLabelCount":4,"interactiveCount":12,"unnamedCount":0,"unnamed":[],"lang":"zh-CN"}
TAB_TRAVERSAL {"total":16,"distinct":10,"maxSame":1,"focusVisibleCount":15,"focusIndicatorCount":15}
```

- 判据映射：Tab 焦点可见（15/16 且 outline solid 2px）✔；aria/语义（4 个 aria-label、`main` landmark、三级标题、`zh-CN`）✔；无键盘陷阱（16 次 Tab 覆盖 10 个不同目标、最大连续重复 1、循环回绕正常）✔。
- 证据：`screens/wae-a11y-login-first-view.png`、`screens/wae-a11y-keyboard-focus-state.png`、`logs/run-wae-gates.log`。

### 2.2 evidence_overexposure_gate（pass）

- 被测：同上默认首屏可见文本。
- 机器字段正则 9 类：`doc_id:`、`evidence:`、`external_source`、`feature_id`、`work_item_id`、`GPCF-DOC-*`、UUID、JSON 对象片段、64 位 sha256。
- 结果（`logs/run-wae-gates.log`）：

```text
OVEREXPOSURE_FINDINGS []
ENVIRONMENT_LABELS_OBSERVED ["环境 开发 · :4300","版本 v0.1.0","身份服务 /api/idp"]
```

- 判据映射：默认界面未暴露 doc_id/evidence/json/内部 ID ✔；观测到的 3 项为**工程环境标注**（环境名、版本号、身份服务路径），不属于上述机器字段，单列记录、不记为违规，也不据此证明其它项目页面。
- 证据：`screens/wae-overexposure-login-default.png`；既有 Studio 设置页截图复核（`artifacts/studio-runtime-reference/`）无机器字段，可作辅助。

### 2.3 task_flow_e2e_status（初轮 fail，最终结果见 §2.5：已由 WAE 完整任务流取证 pass）

- 命令：`cd "GlobalCloud Studio" && npx playwright test --config <本目录>/playwright.studio-specs.config.ts --grep "renders authenticated shell and navigates between key product routes|recovers the session rail after a temporary session-service outage"` → **2 failed**。
- 失败点：两条 spec 都在应用壳渲染前失败（`app-layout` / `session-rail-shell-mode` 不存在），与 §1 回归同因；`logs/run-studio-existing-e2e.log` 为原始输出。
- WAE 侧补充：`task_flow_partial` 用例通过（空提交 → 「请填写账号与口令」客户端校验失败 → 切换空间/回填后表单仍可交互），但**无真实账号未完成登录**，不构成端到端任务流，故不用于 pass。
- 证据：`logs/run-studio-existing-e2e.log`、`screens/wae-taskflow-space-switch.png`、`screens/wae-taskflow-login-validation-failure.png`、`screens/wae-taskflow-recovered-usable-form.png`。

### 2.4 multi_user_usability（pending，无证据）

- 已尝试的两条路径均不可用且未越权：
  1. Studio：应用空白（§1），无法完成任何核心任务；其既有 E2E 2 failed（含失败恢复用例）。
  2. WAE 本地 IdP：`runtime/idp/users.json` 有 5 个账号（角色覆盖 system-admin / operator / viewer / auditor / studio），但**口令不在本任务可见范围**；创建/重置凭据属凭据创建类高危险操作（GPCF AGENTS 需人工授权），未执行。
- 未采用 Playwright 路由注入的合成会话去「证明」两类用户完成核心任务——那只能证明 UI 结构可渲染，不构成多用户可用性验收，故保持 pending。
- 解锁所需（可执行）：任一被测 UI 的**已授权测试账号**（≥2 个角色），或人工授权一次本地 IdP 凭据初始化（仅本机、验证后清理）。

### 2.5 task_flow_e2e_status（task-18 追加：pass）

- 环境：WAE dev `:4300`；**隔离临时 IdP 目录** `/tmp/f010-e2e-idp`（env 覆盖 `WAE_IDP_DIRECTORY` / `WAE_IDP_SESSIONS` / `WAE_IDP_AUDIT` / `WAE_IDP_TENANT_CONFIG`；首启 `POST /api/idp/bootstrap` 创建唯一临时账号；口令仅 env 注入、未写入证据；验证后停止服务并删除临时目录）。
- 命令：`cd "GlobalCloud WAE" && pnpm dev`（:4300）→ `cd "GlobalCloud Studio" && F010_OUT=<本目录> F010_LOGIN_USER=… F010_LOGIN_PASSWORD=… F010_NEW_PASSWORD=… npx playwright test --config <本目录>/playwright.wae.config.ts --grep "task_flow_e2e_status: WAE"` → **1 passed**（9 steps，0 pageerror，1 console error＝登录前 `/me` 401 会话探测，属预期）。
- 流程（`logs/taskflow-assertions.json` + `logs/run-wae-taskflow.log`）：
  1. 登录页加载（`screens/wae-flow-01-login.png`）；
  2. 失败恢复：空提交 →「请填写账号与口令」（客户端校验，未发送登录请求）（`wae-flow-02-login-validation-error.png`）；
  3. 真实本地测试身份登录 → 首登强制改密页（`wae-flow-03-forced-password-change.png`）；
  4. 改密成功（forced=true）→ 进入工作台「欢迎回来」（`wae-flow-04-workbench-home.png`）；
  5. 进入工作区：项目管理器弹层（4 个真实项目/收藏/归档/回收站，`wae-flow-05-project-manager.png`）；
  6. 关闭弹层 → 返回工作台主页（`wae-flow-06-return-home.png`）；
  7. 账户菜单 → 退出登录 → 回到统一身份登录页（`wae-flow-07-logout-return-login.png`）。
- 判据映射：端到端任务流（登录→改密→工作台→进入页面→返回→退出）✔；失败恢复（空提交错误提示且可继续操作）✔。
- 边界：身份为**本机隔离临时账号**（非真实用户、非共享/生产实例）；覆盖对象为 WAE 统一入口，不代表 28 项目逐页覆盖；Studio 侧 E2E 仍受 §1 回归阻断。另观察：项目管理器弹层关闭按钮的可访问名为 `✕`（语义偏弱），记录为 a11y 观察项，不改变本轮 a11y gate（范围仍为登录首屏）。

### 2.6 multi_user_usability（task-19 追加：pass，老卢授权双临时角色）

- 授权与做法：老卢 2026-10-22 授权「隔离临时 IdP + 2 个不同角色临时账号，验证后删除」。`/tmp/f010-multi-idp`（env 覆盖 `WAE_IDP_DIRECTORY/SESSIONS/AUDIT/TENANT_CONFIG`）→ `POST /api/idp/bootstrap` 建 A（system-admin）→ A 会话建 B（role=viewer）→ 两账号首登改密；口令仅 env 注入、不写入证据，验证后删除临时目录。
- 命令：`cd "GlobalCloud WAE" && pnpm dev`（:4300）→ `cd "GlobalCloud Studio" && F010_OUT=<本目录> F010_A_USER=… F010_A_PASSWORD=… F010_B_USER=… F010_B_PASSWORD=… npx playwright test --config <本目录>/playwright.wae.config.ts --grep "multi_user_usability: 双角色"` → **1 passed**（6 steps / 0 pageerror）。
- 结果（`logs/multi-user-assertions.json`）：
  - A=system-admin：`/me` 16 menus（含 idp-console）；身份与权限 → 用户与目录显示 `目录账号 2 / 2`（f010-admin、f010-viewer）；`GET /api/idp/users` **200**；
  - B=viewer：`/me` 4 menus（overview/feedback-center/scene/pqc-sop）；同一页面显示「无权限：用户目录仅体系管理员可见 / 当前身份为「viewer」」；`GET /api/idp/users` **403**「需要 system-admin 角色」；
  - 会话隔离：A 登出后 `/me`=401 且回登录页；B 独立 context 登录、其 `/me`=viewer（不继承 A 权限）；B 登出后 `/me`=401。
  - 截图：`screens/multi-user-A-system-admin-idp-users.png`、`screens/multi-user-B-viewer-idp-denied.png`、`screens/multi-user-A-after-logout-login.png`、`screens/multi-user-B-after-logout-login.png`。
- 判据映射：两类用户完成核心任务（登录→工作台→身份控制台）✔；角色可见性/权限差异（16 vs 4 menus；用户目录可见 vs 无权限）✔；至少一项越权被拒（页面无权限提示 + API 403）✔；会话隔离（独立 context、双方 logout 后 `/me`=401）✔。
- **发现的 UI 缺陷**（不改变 gate 判定，单独登记）：AppsShell 导航层角色收敛未生效——`apps/wame/src/app/apps/generated.ts` 的 app/entry 无 `requires` 字段，`AppsShell.canSee()` 恒真，viewer 仍看到「服务控制台」下 GCAs/MMC/GPCF/ICP/AaaS/身份与权限入口；实际权限由页面/接口判据正确拒绝（不构成越权成功）。建议另立 UI 缺陷任务补 `requires` 生成。

## 3. 证据文件清单

| 文件 | 内容 |
|---|---|
| `ui-gates.spec.ts` + `playwright.gates.config.ts` | Studio 四项 gate 脚本（本轮因 §1 全部失败，保留为回归复现件） |
| `probe.spec.ts` | Studio 渲染诊断脚本（定位 §1 根因） |
| `probe-wae.spec.ts` / `probe-wae2.spec.ts` / `playwright.wae.config.ts` | WAE UI 探测脚本与配置 |
| `wae-ui-gates.spec.ts` | WAE 登录入口 a11y/证据暴露/失败恢复用例（本轮 pass 的来源） |
| `playwright.studio-specs.config.ts` | 复用 Studio 既有 E2E spec 的配置（channel=chrome） |
| `logs/run-wae-gates.log` | a11y/overexposure/失败恢复原始输出 |
| `logs/run-studio-existing-e2e.log` | Studio 既有 E2E 2 failed 原始输出 |
| `logs/studio-probe.log` | Studio 空白页运行时错误堆栈（根因证据） |
| `logs/run-ui-gates.log` | Studio 自定义四项 gate 脚本失败原始输出 |
| `wae-taskflow.spec.ts` | WAE 完整任务流用例（登录→改密→工作台→进入页面→返回→退出 + 失败恢复） |
| `wae-multi-user.spec.ts` | 双角色用例（system-admin / viewer，可见性差异 + 越权 403 + 会话隔离） |
| `logs/run-wae-multi-user.log` / `logs/multi-user-assertions.json` | 双角色原始输出与断言 JSON（6 steps / 0 pageerror / usersApi A=200 B=403） |
| `logs/run-wae-taskflow.log` / `logs/taskflow-assertions.json` | WAE 任务流原始输出与逐步断言 JSON（9 steps / 0 pageerror） |
| `screens/*.png` | 13 张截图（Studio 空白页、WAE 登录首屏、键盘焦点、失败恢复、证据暴露扫描） |


### 运行前置（可复现说明）

- 本目录脚本依赖 Studio 仓的 `@playwright/test`：运行前在**本目录**创建软链 `node_modules -> "GlobalCloud Studio/node_modules"`（本轮临时创建，验证结束已删除，不进入证据）；
- 运行方式：`cd "GlobalCloud Studio" && F010_OUT=<本目录> npx playwright test --config <本目录>/playwright.<gates|wae|studio-specs>.config.ts`；
- WAE 用例需先 `cd "GlobalCloud WAE" && pnpm dev`（:4300），验证后停止；
- 本轮实际使用 system Chrome（`channel: 'chrome'`），因 Studio Playwright 1.61.1 所需 chromium-1228 未缓存。

## 4. 限制与未做

- 未修复 Studio 回归（需改 Studio 仓，超出本任务边界）；建议另立 Studio 修复任务：删除/改写 `AppSidebar.vue:626` 的 `gcworld.organizations` 链接与 `App.vue` 残留判断，然后复跑既有 E2E。
- 未修复 WAE AppsShell 导航层角色收敛缺陷（`generated.ts` 无 `requires`）；页面/接口权限判据正常，建议另立 UI 缺陷任务。
- 未创建/重置任何账号或凭据；未读取或输出凭据明文。
- 未启动/停止未知服务；WAE `pnpm dev` 为临时验证服务，已停止（端口 4300 已释放）。
- 覆盖范围仍有限：仅 WAE 统一身份入口（默认首屏）+ 既有 Studio 设置页截图，**不代表 18/28 个项目逐页覆盖**；a11y/证据暴露 pass 也不代表多用户与任务流通过。
- 未使用 mock 会话提升任何 gate；task_flow 使用本机隔离临时账号（env 注入、验证后删除），非真实用户验收。
- Studio HEAD 回归仍在；task_flow 改由 WAE 统一入口取证，不代表 Studio 可用。

## 5. 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明多用户可用性通过、任务流 E2E 通过、四大 gate 全通过；
- 不声明 Studio 可用（其 HEAD 当前登录后 UI 空白，属已知回归）；
- 不声明任何项目 UI 已纳入统一框架验收；本文件不替代项目实施方案与 Feature 证据。
