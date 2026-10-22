---
doc_id: GPCF-DOC-F036-E2E-20261022
title: F-036 task_flow E2E 证据（WAE PKC 入口，2026-10-22）
project: GPCF
related_projects: [WAE, PKC, GPCF]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/README.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/e2e-20261022/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-036 task_flow E2E 证据（WAE PKC 入口，2026-10-22）

> 性质：真实浏览器（Playwright + system Chrome）task_flow 演练，隔离临时 IdP，无 mock。
> **最终结论（run3，原始 dev、无任何垫片）：pass** —— 10 步全过，`pageErrors=0`，`externalRequests=0`，`consoleErrors=1`（登录前 `/me` 401 会话探测，属预期）。`task_flow_e2e_status = pass`。
> 不声明 PKC 已接入 / accepted / integrated / production_ready；未 commit/push；未改 PKC 仓；未改 WAE 业务代码。

## 0. 结论

- run3 使用**原始 WAE dev**（无垫片）跑通完整 flow：登录（首登强制改密）→ 应用壳 → 侧栏一级入口 `PKC 知识工作台`（requires pkc）→ `pkc-intake` 候选页（候选态/非声明可见、机器字段不上屏、受控嵌入默认无 iframe 且 0 外部请求）→ 返回工作台。
- 前置修复：WAE 工作区已补 `apps/wame/src/app/hooks/useAppContent.ts` 的 `import { CONSOLE_COLORS } from './consolePalette';`（未提交工作区修复，由 WAE 属主完成；`tsc --noEmit` pass）。修复后 spec 中的临时常量垫片已删除，run3 不再依赖垫片。
- 历史轮次保留：run1（修复前原始 dev）fail 复现既有回归；run2（修复前 + 文档化垫片）链路 pass。二者仅作溯源，不代表当前 gate。

## 1. 环境（隔离、可清理）

| 项 | 值 |
|---|---|
| WAE dev | `pnpm --filter @globalcloud/wame exec vite --port 4301 --strictPort`（**4300 有其它会话实例，未终止他人服务**，改用 4301 隔离实例） |
| 隔离临时 IdP | `/tmp/f036-e2e-idp/`（env 覆盖 `WAE_IDP_DIRECTORY / SESSIONS / AUDIT / CONFIRM_TOKENS / TENANT_CONFIG`；`POST /api/idp/bootstrap` 建唯一 `f036-e2e-admin` system-admin，`mustChangePassword=true`） |
| 凭据 | 初始/新口令运行时随机生成，仅存 `/tmp`（600）与进程 env；**不写入任何证据文件**；运行结束整目录删除 |
| Playwright | 复用 F-010 模式：`GlobalCloud WAE/apps/wame/node_modules/.bin/playwright` + 本目录 `playwright.f036.config.ts`（`channel: chrome`，baseURL 由 `F036_BASE_URL` 注入；`testMatch` 只跑 `f036-pkc-taskflow.spec.ts`）；`node_modules` 临时软链运行完即删 |
| 复现 | `bash "…/evidence/e2e-20261022/run-e2e.sh"`（脚本内含全部 env 注入与收尾） |

## 2. 轮次记录（同一 spec，差异仅在环境前置条件）

| 轮次 | 环境前置 | 结果 | 证据位置 |
|---|---|---|---|
| run1 | 修复前原始 dev（WAE HEAD `41ce842` 漏 `CONSOLE_COLORS` import） | **fail**：登录/改密后 ErrorBoundary 白屏；断言失败 `account-menu-trigger` 不可见 | `logs/run1-raw-fail/`、`screens/run1-raw-fail/` |
| run2 | 同上 + spec 内文档化常量垫片（逐字同 `consolePalette.ts`） | PKC 链路 **pass**（10 步；证明 PKC 侧本身无阻塞） | `logs/run2-with-shim/`、`screens/run2-with-shim/`；垫片版 spec 归档 `logs/run2-with-shim/f036-pkc-taskflow.with-shim.spec.ts.txt`（不参与执行） |
| **run3（当前）** | **WAE 补 import 后的原始 dev（无垫片）** | **pass**：10 步全过，`pageErrors=0`、`externalRequests=0`、`consoleErrors=1`（预期 401） | `logs/run3-raw-dev-pass/`、`screens/f036-flow-*.png` |

## 3. run3 步骤与断言（最终 gate 依据）

| # | 步骤 | 断言 | 结果 |
|---|---|---|---|
| 1 | 打开 `/` | 登录门可见（真实产品 UI，无 mock） | ✓ |
| 2 | 真实登录（隔离 IdP） | 首登强制改密 → 保存新口令 | ✓ |
| 3 | 进入 WAE 工作台 | `account-menu-trigger` + 「欢迎回来」可见 | ✓ |
| 4 | 进入应用壳 | URL `/global-cloud-workbench`；`app-nav-pkc`（requires pkc，system-admin）可见 | ✓ |
| 5 | 点击 PKC 入口 | URL `/global-cloud-workbench/pkc/pkc-intake`；`pkc-intake-page` 可见 | ✓ |
| 6 | 候选态 / 非声明 | 「PKC 知识工作台（候选接入）」+「不声明 PKC 已接入」可见 | ✓ |
| 7 | 机器字段不上屏 | 页面文本不含 `packageId / evidenceRefs / contentDigest / status_ceiling / cost_tier` | ✓（leaked=[]） |
| 8 | 受控嵌入默认关闭 | 无 `pkc-embed-frame`；`pkc-embed-disabled` 可见 | ✓（frameCount=0） |
| 9 | 不接受外部请求 | `page.on('request')` 全程外部请求 **0**（仅 127.0.0.1:4301 同源） | ✓ |
| 10 | 返回工作台 | 退回应用壳，`app-nav-pkc` 仍在（壳未崩） | ✓ |

- 汇总：`steps=10, pageErrors=0, consoleErrors=1（预期 /me 401）, externalRequests=0`；`PLAYWRIGHT_EXIT=0`。
- 截图：`screens/f036-flow-01…06*.png`（登录页 / 改密页 / 工作台 / 侧栏 PKC 入口 / PKC 候选页 / 返回工作台）。
- 断言 JSON：`logs/run3-raw-dev-pass/taskflow-assertions.json`；运行日志：`logs/run3-raw-dev-pass/playwright-run.log`、`dev-server.log`、`run-meta.json`。

## 4. Gate 结论与依赖

- `task_flow_e2e_status = **pass**`（run3 原始 dev 真实通过，无垫片）。
- 依赖：WAE 工作区修复 `useAppContent.ts` 的 `CONSOLE_COLORS` import（未提交；`tsc --noEmit` pass）。若该修复被回退，本 gate 会回退为 fail（run1 可复现）。
- 仍存的非 E2E 阻塞：PKC 仓令牌（P4）/状态语义（P5）与真实运行时嵌入/正式接入评审（见 `evidence/summary.md` §5）。

## 5. 清理确认（本任务收尾）

| 项 | 状态 |
|---|---|
| WAE dev（4301） | 已停止；`lsof :4301` = 0 listeners（4300 他人实例未动，仍 1 listener） |
| 临时 IdP `/tmp/f036-e2e-idp` | 已删除 |
| Playwright `node_modules` 软链 | 已删除 |
| WAE `test-results/`（本次运行产物） | 已删除 |
| 证据凭据 | 无实际口令值；无凭据泄漏（`F036a!/F036b!` 仅为脚本随机口令模板与说明文字） |

## 6. 非声明

- 不声明 PKC 已接入 / 已集成 / accepted / integrated / production_ready / 客户验收。
- E2E 通过仅表示"WAE 侧 PKC 候选入口的 task_flow 可走通"；PKC 业务运行态、令牌/状态语义、授权/MMC 仍未接入与验收。
- 未 commit / push；未关闭 Feature；未改 PKC 仓 / WAE 业务代码。
