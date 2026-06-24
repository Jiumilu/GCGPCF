---
doc_id: GPCF-DOC-GPC-REAL-RUNTIME-BASELINE-20260624
title: GPC 真实运行基线证据 2026-06-24
project: GPC
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md
source_path: docs/harness/GPC/evidence/gpc-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GPC 真实运行基线证据 2026-06-24

## 1. 证据定位

本文记录 GPC 在 `GlobalCloud 项目群实施方案` 下的首轮真实运行、绿色供应链场景、L3/L4 合同、接口验证、测试结果和阻塞状态。

本文不声明 GPC 真实交付完成，不声明外部绿色供应链与金融联调完成，不声明客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 执行日期 | 2026-06-24 |
| 执行仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC` |
| 当前分支 | `main` |
| 工作区状态 | dirty，存在未跟踪总体/实施方案文档和 `tools/` 目录 |
| 仓库类型 | Node + Python + Playwright + Frappe/ERPNext 绿色供应链场景仓库 |
| 证据采集方式 | 本地命令执行 |

## 3. 已执行命令与结果

| 命令 | 结果 | 说明 |
|---|---|---|
| `npm run check:js` | pass | `app.js`、中文品牌脚本、设计系统脚本均通过 `node --check` |
| `npm run quality:repo` | fail | smoke、artifact、API、核心流、外部契约 smoke、中文完整性通过；失败于 README 缺索引 |
| `python3 scripts/validate_gpc_l3_harness.py` | pass | L3 harness 门禁通过 |
| `python3 scripts/validate_gpc_l4_platform_contract.py` | pass | L4 平台订单合同门禁通过 |
| `npm run quality:100` | fail | evidence policy 通过；生产环境确认和外部联调证据失败 |
| `npm run test:e2e` | fail | 20 个 Playwright 用例因本机缺 Chromium headless shell 失败 |
| `npm run quality:ops` | pass | operational preflight、ops drill、runtime API integration 均通过 |

## 4. 已通过的关键证据

### 4.1 绿色供应链核心链路

`npm run quality:repo` 已通过的关键片段：

```text
smoke check passed
factories=3 orders=5 suggestions=4 finance_packages=2

gcfis API contract validation passed
implemented_apis=6 commits=3

gcfis core flow validation passed
core_flows=5
closed_loop=ORD-2404->F-GEHUA->WO/QI/Stock/DN->POD-2404->FIN-002

gcfis external contract smoke passed
apis=5 write_apis=3 read_apis=2 auth=bearer idempotency=covered forbidden_writes=blocked fund_fact_auto_confirmed=false
```

### 4.2 GPC L3/L4 门禁

```text
gpc l3 harness validation passed
round=GPC-LR-001 substantive_rounds=1/15 substance_gate=pass

gpc l4 platform contract validation passed
round=GPC-L4-007 orders=1 sample_requests=1 sample_approvals=1 production_releases=1 pod_records=1
```

### 4.3 GPC 运行态与 API

`npm run quality:ops` 输出：

```text
PASS: GCFIS desk reachable: http://127.0.0.1:8080/desk
PASS: runtime GCFIS language asset reachable
gcfis operational preflight passed
site=frontend compose_project=gcfis apps=frappe,erpnext,gcfis_custom

gcfis ops drill passed
services=9 backup_files_before=4 backup_files_after=8 backup_integrity=json,gzip,tar restore_drill=temp-site doctor=workers-online logs=bench,frappe,scheduler rollback_head=b47d25c

gcfis runtime API integration validation passed
runtime_apis=7 auth=session read_only=3 write_paths=3 health=ok localized_errors=1 dispatch_created=1 confirmation_status=已接受 finance_package_created=1 finance_gate=L4_blocked fund_fact_auto_confirmed=false
```

结论：GPC 本地运行态、运维 drill 和运行态 API integration 本轮通过真实命令验证。

## 5. 失败点

### 5.1 仓库综合门禁失败点

`npm run quality:repo` 失败于：

```text
FAIL: README.md missing docs/18-gcfis-quality-execution-closure.md
```

### 5.2 外部 100 分证据缺口

`npm run quality:100` 失败于：

- `production_environment_confirmation.json` 未确认生产环境、域名、数据库、备份策略、监控和生产证据引用；
- `external_integration_joint_test.json` 未确认绿色供应链与金融联调的授权、幂等、错误处理、审计、资金事实门禁和外部联调证据。

### 5.3 浏览器测试环境缺口

`npm run test:e2e` 失败于：

```text
Executable doesn't exist at /Users/lujunxiang/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell
Please run the following command to download new browsers:
npx playwright install
```

## 6. 结论边界

本轮可以登记：

```text
gpc_runtime_evidence = partial_verified
gpc_interface_evidence = partial_verified
gpc_l3_l4_evidence = verified
gpc_repair_required = readme_external_evidence_browser
```

本轮不得登记：

- 不登记 GPC 真实交付完成；
- 不登记 GPC 外部绿色供应链与金融联调完成；
- 不登记 GPC 客户验收通过；
- 不登记 GPC production_ready；
- 不登记资金事实自动确认为真。

## 7. 下一步

GPC 下一轮修复优先级：

1. 修复 README 缺失 `docs/18-gcfis-quality-execution-closure.md` 索引，重跑 `npm run quality:repo`。
2. 安装或修复 Playwright Chromium，重跑 `npm run test:e2e`。
3. 由授权责任人补充生产环境确认和外部联调证据，重跑 `npm run quality:100`。
