---
doc_id: GPCF-DOC-69BAD1B287
title: GPCF-L4-GFIS-REPAIR-001 GFIS Runtime SOP E2E Precheck
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoG, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-001.md
source_path: docs/harness/loops/loop-round-GPCF-L4-GFIS-REPAIR-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-L4-GFIS-REPAIR-001 GFIS Runtime SOP E2E Precheck

## Trigger

`GPCF-L4-CORR-001` 已确认 GFIS Demo 被错误计为运行层证据，且 GFIS `test-results/.last-run.json` 为 failed。本轮进入真实 GFIS 项目仓，按运行层主体建立一个最小 SOP E2E 预检闭环。

## Scope

| 项 | 说明 |
|---|---|
| 真实项目仓 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS` |
| 正确主体 | GFIS 运行层 |
| 禁止主体 | GFIS Demo 不能作为 SOP/E2E/UAT/验收主体 |
| 本轮目标 | 建立运行层对象链、fixture、evidence map 和 validator，防止再次用 Demo 替代运行层 |
| 非目标 | 不执行 `bench migrate`、schema sync、数据库迁移、生产写 API、真实外部 API、权限变更、部署或 accepted/integrated 升级 |

## Deliverables

| 类型 | 路径 | 结论 |
|---|---|---|
| GFIS runtime SOP README | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/README.md` | 已新增 |
| GFIS runtime SOP plan | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/gfis-runtime-sop-e2e-plan.md` | 已新增 |
| GFIS runtime evidence map | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/gfis-runtime-evidence-map.md` | 已新增 |
| GFIS runtime fixture | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness/sop-e2e/fixtures/gfis-runtime-sop-e2e.fixture.json` | 已新增 |
| GFIS runtime validator | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/scripts/validate_gfis_runtime_sop_e2e.py` | 已新增 |

## Runtime Chain

```text
GPC PlatformOrder
-> GFIS FactoryOrder
-> GFIS WorkOrder
-> GFIS ProductionExecution
-> GFIS QualityInspection
-> GFIS InventoryBatch
-> GFIS DeliveryNote
-> GPC/POD ProofOfDelivery
-> WAES EvidenceRecord
-> KDS KnowledgeBacklink
-> Brain/PKC/XiaoG read/query/remind/track
```

## Verification

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_runtime_sop_e2e.py` | pass |
| `npm run check:js` | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_core_flows.py` | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gcfis_p0_extensions.py` | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_work_order_api_contract.py` | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_waes_gate_events.py` | pass |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/validate_gfis_outbound_pod_finance_boundary.py` | pass |
| `git diff --check -- .` in GFIS repo | pass |

## Truthfulness Boundary

| 项 | 真实结论 |
|---|---|
| GFIS 主体错位 | 已通过新增运行层 SOP E2E precheck 包纠偏 |
| Demo 替代运行层 | 已被 validator 禁止 |
| 完整 SOP E2E | 仍未判定通过；GFIS `test-results/.last-run.json` 仍是 failed |
| 生产写入 | 未执行 |
| 外部真实 API | 未执行 |
| 数据库迁移/schema sync | 未执行 |
| accepted/integrated | 未升级 |

## Round Accounting

| 字段 | 值 |
|---|---|
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | partial |
| stop_type | authorization_boundary |
| stop_evidence | 本轮只完成 GFIS 运行层 SOP E2E 预检闭环；完整运行态 E2E、真实样本、UAT 和验收升级仍需后续授权 |

## Next Input

下一轮应在保护 GFIS dirty 工作区的前提下，继续把预检 fixture 连接到真实运行层 API 或受控 dry-run runner，并将 Demo Playwright failed 与运行层 SOP E2E 分开治理。
