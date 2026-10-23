---
doc_id: GPCF-DOC-GPCF-COMMIT-BATCH-PLAN-20261023
title: GPCF 未提交改动分批提交计划（2026-10-23）
project: GPCF
related_projects: [GPCF, WAE, WAME, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/gpcf-commit-batch-plan-20261023.md
source_path: docs/harness/evidence/gpcf-commit-batch-plan-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# GPCF 未提交改动分批提交计划（2026-10-23）

> 只读盘点；不 commit/push。目的：避免 `git add -A` 混入并发改动。

## 1. 规模

| 范围 | 条数 |
|---|---:|
| 全部 dirty | 1118+ |
| `.kds` 镜像 | 536 |
| 非 `.kds` | 612 |
| 可脏区外（gc_standard R14） | 47 |

## 2. 建议批次（显式路径）

### 批次 A：治理校验器 + CI（本会话新增）
- `tools/kds-sync/validate_vu_ledger.py`
- `tools/kds-sync/validate_asset_reuse.py`
- `tools/kds-sync/validate_contract_version_drift.py`
- `tools/kds-sync/validate_event_package_ref.py`
- `tools/kds-sync/validate_xap_error_code_registry.py`
- `tools/kds-sync/measure_asset_reuse.py`
- `tools/kds-sync/loop_document_gate.py`（动态基线修复）
- `tools/kds-sync/validate_project_group_single_authorization_ledger.py`、`validate_evidence_rule_version.py`
- `.github/workflows/governance.yml`
- `scripts/gpcf_check_evidence.py`、`scripts/gpcf_feature_lib.py`（如属本会话）
- `tests/test_gpcf_feature_move_metadata.py`

### 批次 B：台账与快照
- `runtime/vu-ledger.yaml`、`runtime/asset-registry/registry.yaml`、`runtime/asset-registry/usage-report.yaml`
- `runtime/contract-matrix.yaml`、`runtime/xap-error-code-registry.yaml`、`runtime/contract-version-hashes.yaml`
- `runtime/plan-20261022/*`（章程/复盘/指标/阻塞裁定/报告）
- `docs/harness/evidence/project_group_live_status_current.{json,md}`

### 批次 C：文档/证据/状态
- `docs/harness/evidence/*`（本会话新增）
- `09-status/globalcloud-cross-project-contract-matrix-v1.0.md`、`globalcloud-project-group-completion-baseline-v1.0.md`
- `projects/{wae,pkc,wame}/STATUS.md`
- `features/active/F-035-*`、`features/active/F-036-*`、`features/done/F-034-*` 证据
- `README.md`

### 批次 D：fixtures/schema
- `fixtures/events/package-ref.{positive,negative}.json`
- `okf/event-envelope-package-ref.schema.json`

### 批次 E：并发/非本会话（不接管）
- `$CODEX_HOME/**`、`.kunsdd/**`、`.okf/**`、`.standards/**`、`00-index/**`、`01-architecture/README.md` 等

## 3. 操作纪律

1. 禁止 `git add -A` / `git add .`；按批次显式路径。
2. 提交前 `git diff --cached --stat` 复核，确认只含本批次。
3. 任一提交/推送需老卢授权；默认不 commit/push。
4. `.kds` 镜像由 `document_control.py` 统一同步，不手工逐个 add。

## 4. 非声明

- 不声明任何改动已提交；不声明状态提升。
