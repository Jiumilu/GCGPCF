---
doc_id: GPCF-DOC-B487995496
title: Loop CodeGraph Project Group Coverage Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.md
source_path: docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop CodeGraph Project Group Coverage Evidence

## Evidence ID

`LOOP-CODEGRAPH-PROJECT-GROUP-COVERAGE-20260620`

## 结论

项目群当前本机 14 个 Git 仓库已经完成 CodeGraph 本地代码图谱生成，`WAS世界资产体系` 已作为第 14 项纳入项目群、代码图谱和 Loop 工程登记。

## 当前事实

| 字段 | 值 |
|---|---|
| codegraph_cli_available | true |
| codegraph_version | `1.0.1` |
| telemetry | disabled |
| project_group_repo_count | 14 |
| studio_included | true |
| was_included | true |
| mcp_configuration_changed | false |
| codegraph_index_created | true |
| production_write | false |
| external_api_write | false |
| status_upgrade_allowed | false |

## 受控产物

| 产物 | 路径 |
|---|---|
| 覆盖登记 | `02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md` |
| Evidence JSON | `docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.json` |
| 本轮 Loop 记录 | `docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-001.md` |
| Validator | `tools/kds-sync/validate_loop_codegraph_project_group_coverage.py` |

## Studio 纳入证据

| 字段 | 值 |
|---|---|
| path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` |
| files | 778 |
| nodes | 14,202 |
| edges | 46,489 |
| db_size | 43.00 MB |
| loop_context_detected | true |
| loop_admission_status | `loop_ready_partial` |
| loop_admission_validator | `scripts/validate_studio_loop_admission.py` |
| quality_readiness_status | `test_build_harness_pass` |
| quality_readiness_validator | `scripts/validate_studio_quality_readiness.py` |
| test_evidence | `docs/harness/evidence/studio-test-run-20260620.json` |
| quality_gate_repair_evidence | `docs/harness/evidence/studio-quality-gate-repair-20260620.json` |
| harness_foundation_evidence | `docs/harness/evidence/studio-harness-foundation-20260620.json` |
| workflow_release_boundary_evidence | `docs/harness/evidence/studio-workflow-release-boundary-20260620.json` |
| npm_test_executed | true |
| npm_test_status | `pass` |
| npm_build_executed | true |
| npm_build_status | `pass` |
| harness_check_executed | true |
| harness_check_status | `pass` |
| workflow_release_boundary_status | `review_required_before_commit` |

## WAS 纳入证据

| 字段 | 值 |
|---|---|
| path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/WAS世界资产体系` |
| remote | `https://github.com/Jiumilu/GCWAS.git` |
| role | `semantic_foundation_project` |
| files | 30 |
| nodes | 70 |
| edges | 209 |
| db_size | 0.27 MB |
| loop_context_detected | true |
| was_validator_status | `pass` |
| accepted | false |
| integrated | false |
| production_ready | false |

## 非声明

- 本 evidence 不证明 GFIS runtime SOP E2E 已通过。
- 本 evidence 不创建 source-of-record、运行层主键、review queue、runtime intake、WAES review、verified artifact、UAT 签收、客户满意、`accepted` 或 `integrated`。
- 本 evidence 不授权生产写入、真实外部 API 写入、数据库迁移、权限变更、部署、提交、推送或合并。
