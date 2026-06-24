---
doc_id: GPCF-DOC-GFIS-REAL-RUNTIME-BASELINE-20260624
title: GFIS 真实运行基线证据 2026-06-24
project: GFIS
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md
source_path: docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GFIS 真实运行基线证据 2026-06-24

## 1. 证据定位

本文记录 GFIS 在 `GlobalCloud 项目群实施方案` 下的首轮真实运行、接口验证、测试结果和阻塞状态。

本文不声明 GFIS 真实交付完成，不声明外部联调完成，不声明客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 执行日期 | 2026-06-24 |
| 执行仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` |
| 当前分支 | `main` |
| 工作区状态 | dirty，存在大量既有 SOP/E2E evidence 修改和未跟踪总体/实施方案文档 |
| 仓库类型 | Node + Python + Playwright + Frappe/ERPNext 自定义应用 |
| 证据采集方式 | 本地命令执行 |

## 3. 已执行命令与结果

| 命令 | 结果 | 说明 |
|---|---|---|
| `npm run check:js` | pass | `app.js`、中文品牌脚本、设计系统脚本均通过 `node --check` |
| `npm run quality:100` | fail | evidence policy 通过；外部 100 分证据失败 |
| `npm run quality:repo` | fail | 大量仓库、接口、业务流、SOP、UAT 预检通过；最后在中文品牌可见语言审计失败 |
| `npm run test:e2e` | fail | 26 个 Playwright 用例全部因本机缺 Chromium headless shell 失败 |
| `npm run test:coverage` | fail | 因本机缺 Chromium headless shell 失败 |
| `npm run quality:ops` | fail | operational preflight 通过并确认运行态 GCFIS 可达；ops drill 备份文件数未增加 |

## 4. 已通过的关键证据

### 4.1 运行态预检

`npm run quality:ops` 的 operational preflight 输出包括：

```text
PASS: docker CLI found
PASS: docker daemon is available
PASS: docker compose is available
PASS: GCFIS desk reachable: http://localhost:8080/desk
PASS: runtime GCFIS language asset reachable
gcfis operational preflight passed
site=frontend compose_project=gcfis apps=frappe,erpnext,gcfis_custom
```

结论：GFIS 本地运行态和 GCFIS desk 可达性已得到本轮真实命令证明。

### 4.2 接口与业务流校验

`npm run quality:repo` 已通过的关键段落包括：

```text
gcfis API contract validation passed
implemented_apis=6 commits=3

gcfis core flow validation passed
core_flows=5
closed_loop=ORD-2404->F-GEHUA->WO/QI/Stock/DN->POD-2404->FIN-002

gcfis external contract smoke passed
apis=5 write_apis=3 read_apis=2 auth=bearer idempotency=covered forbidden_writes=blocked fund_fact_auto_confirmed=false

gfis work-order API contract validation passed
created_docs=19 commits=19

gfis WAES gate event validation passed
cases=3 gate_results=allowed,blocked,waived
```

结论：GFIS 的接口契约、核心业务流、外部契约 smoke、工单 API 契约和 WAES gate event 存在本轮真实验证通过证据。

### 4.3 业务事实与 UAT 边界

`npm run quality:repo` 同时给出以下边界：

```text
gfis field sample ingest validation passed
batches=1 real_samples_submitted=False stop_conditions=6

gfis migration execution confirmation validation passed
register_items=12 human_confirmations=10 ready_to_execute=False

gfis UAT and field sample signoff dispatch validation passed
sample_requests=7 uat_requests=7 cross_project_dispatches=4 ready_to_execute=False
```

结论：GFIS 有样例、签收和迁移预检结构，但真实现场样本、执行确认和 UAT 推进仍未达到可执行/验收完成状态。

## 5. 失败点

### 5.1 外部 100 分证据缺口

`npm run quality:100` 失败于：

- `production_environment_confirmation.json` 未确认生产环境、域名、数据库、备份策略、监控和生产证据引用；
- `external_integration_joint_test.json` 未确认绿色供应链与金融联调的授权、幂等、错误处理、审计、资金事实门禁和外部联调证据。

### 5.2 仓库综合门禁失败点

`npm run quality:repo` 最后失败于：

```text
FAIL: install seed labels not covered by frontend map:
{
  'GCFIS SOP Runtime Sample Candidate': 'SOP运行层样品候选',
  'GCFIS SOP Runtime Evidence Candidate': 'SOP运行层证据候选',
  'GCFIS SOP Runtime Handoff Candidate': 'SOP运行层交接候选'
}
```

### 5.3 浏览器测试环境缺口

`npm run test:e2e` 与 `npm run test:coverage` 均失败于：

```text
Executable doesn't exist at /Users/lujunxiang/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell
Please run the following command to download new browsers:
npx playwright install
```

### 5.4 运维 drill 缺口

`npm run quality:ops` 的 ops drill 失败于：

```text
FAIL: backup file count did not increase: before=12 after=4
```

## 6. 结论边界

本轮可以登记：

```text
gfis_runtime_evidence = partial_verified
gfis_interface_evidence = partial_verified
gfis_repair_required = external_evidence_branding_browser_ops_drill
```

本轮不得登记：

- 不登记 GFIS 真实交付完成；
- 不登记 GFIS 外部绿色供应链与金融联调完成；
- 不登记 GFIS 客户验收通过；
- 不登记 GFIS production_ready；
- 不登记 GFIS 现场样本真实提交完成。

## 7. 下一步

GFIS 下一轮修复优先级：

1. 补齐 3 个 install seed label 到前端中文映射，重跑 `npm run quality:repo`。
2. 安装或修复 Playwright Chromium，重跑 `npm run test:e2e` 和 `npm run test:coverage`。
3. 排查 ops drill 备份文件数异常，重跑 `npm run quality:ops`。
4. 由授权责任人补充生产环境确认和外部联调证据，重跑 `npm run quality:100`。
