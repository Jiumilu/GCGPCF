---
doc_id: GPCF-DOC-DE330E086C
title: GPCF-L4-002 MMC Production Resource Policy Evidence Intake
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-L4-002.md
source_path: docs/harness/loops/loop-round-GPCF-L4-002.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-L4-002 MMC Production Resource Policy Evidence Intake

## Round Output

| 字段 | 值 |
|---|---|
| Round ID | GPCF-L4-002 |
| 对应项目轮次 | MMC-L4-002 |
| 涉及项目 | MMC, GFIS, GPC, WAES, KDS, GPCF |
| 本轮业务节点 | 设备、产线、工序能力、生产资源与样品转量产资源门禁 |
| 真实项目仓路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC` |
| KDS retrieval | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/evidence/kds-retrieval-MMC-L4-002.json` |
| substantive_round | true for MMC real repository policy/test/validator implementation |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## KDS Retrieval Summary

| 字段 | 值 |
|---|---|
| retrieval_mode | local_mirror |
| source_documents | `GPCF-DOC-E3822328DF`, `GPCF-DOC-7B5E3B05D7`, `GPCF-DOC-E2FDF91E39`, `GPCF-DOC-1A3581D521`, `GPCF-DOC-3F160ABA27` |
| retrieved_objects | Equipment, CapacitySnapshot, ResourceCapabilityCheck, ProductionRelease |
| retrieved_statuses | sample confirmation gate, resource capability gate |
| resource_fields | `factory_id`, `line_id`, `equipment_id`, `process_capability_code`, `capacity_snapshot_id` |
| unresolved_questions | 既有 L4 方案写 MMC 为治理/配置基线；最新目标写 MMC 为设备/产线/工序能力/生产资源。本轮按最新目标执行，但不把 MMC 写成 GFIS 主账。 |

## Changes In Real Project Repository

| 类型 | 路径 |
|---|---|
| KDS 检索 evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/evidence/kds-retrieval-MMC-L4-002.json` |
| 运行时策略配置 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/runtime/policies/minimum_closed_loop_policy.json` |
| 运行时测试 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/runtime/tests/test_minimum_closed_loop_policy.py` |
| 项目级 validator | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/scripts/validate_mmc_l4_sample_policy.py` |
| 项目级 evidence 文档 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/minimum-closed-loop/sample-confirmation-policy.md` |

## Verification

| Command | Result |
|---|---|
| `python3 scripts/validate_mmc_l4_sample_policy.py` | pass |
| `python3 scripts/validate_mmc_loop_harness.py` | pass |
| `python3 scripts/validate_mmc_l3_admission.py` | pass |
| `python3 scripts/validate_mmc_self_evolution.py` | pass |
| `python3 scripts/validate_mmc_commit_readiness.py` | pass |
| `MMC_TEST_MODE=true python3 -m pytest runtime/tests -q` | 36 passed |
| `bash runtime/scripts/contract_test.sh` | schema checks passed |
| `git diff --check -- .` | pass |

## Evidence

| 类型 | 路径 |
|---|---|
| 项目级 evidence | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/evidence/kds-retrieval-MMC-L4-002.json` |
| 项目群 evidence | `docs/harness/minimum-closed-loop/evidence-index.md` |

## Risk And Rollback

- 风险：MMC 只定义生产资源能力策略字段和 validator，不代表 GFIS 设备、产线、工单或生产执行事实已写入。
- 风险：既有受控 L4 方案与最新目标中的 MMC 职责描述存在差异，已登记为 unresolved question。
- 回滚：撤回 MMC 本轮新增的 KDS retrieval、policy、test、validator、round record 与项目级 evidence 文档。
- 禁止动作：accepted/integrated、生产写入、真实外部 API 写入、权限变更、部署、数据库迁移、TOKEN 输出、Git push。

## Next Input

`KDS-L4-003`：在 KDS 真实仓建立样品规格、签样资料、SOP 和 evidence 回指索引。每轮必须先执行 KDS 关联数据检索。
