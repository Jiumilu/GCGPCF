---
doc_id: GPCF-DOC-89DF4CBBFA
title: Git 风险分类报告
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/git-risk-classification-20260617.md
source_path: docs/harness/evidence/git-risk-classification-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Git 风险分类报告

- generated_at: `2026-06-17T00:44:27.522007+00:00`
- scope: GPCF + GFIS
- policy: 只分类、不删除、不 reset、不 checkout
- next: 按分类形成提交候选，再从 KDS 候选提取 5 类真实凭证责任方回执任务

## 汇总

| 仓库 | 分支 | total | modified | untracked | deleted/missing | high risk |
|---|---|---:|---:|---:|---:|---:|
| GPCF | `## codex/kds-token-sync-gpcf...origin/codex/kds-token-sync-gpcf [ahead 4]` | 476 | 41 | 435 | 0 | 2 |
| GFIS | `## main...origin/main` | 486 | 21 | 465 | 0 | 3 |

## 分类计数

### GPCF

| 分类 | 数量 | 处置建议 |
|---|---:|---|
| `gpcf_governance_and_control_sync` | 28 | 优先作为总控同步提交候选复核 |
| `kds_local_mirror_and_ledger` | 234 | 确认是否属于 KDS 开发空间镜像与审计流水 |
| `legacy_or_prior_loop_round_artifacts` | 211 | 按历史轮次证据归档或提交，不能计为新实质轮次 |
| `project_documentation` | 1 | 复核是否属于主体定位或治理文档更新 |
| `sensitive_config_review` | 1 | 必须人工复核，默认不得提交 |
| `unclassified_requires_manual_review` | 1 | 人工判定归属后再提交 |

前 20 项样例：

- ` M` `.kds/development-space/开发/01-GFIS/08-evidence-samples/GFIS/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/01-GFIS/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/04-WAES/08-evidence-samples/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/05-KDS/docs/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/05-KDS/docs/harness/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/05-KDS/docs/harness/minimum-closed-loop/evidence-index.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/05-KDS/docs/harness/minimum-closed-loop/l4-closure-score-matrix.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/12-GPCF/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/12-GPCF/docs/harness/evidence/evidence-index.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/12-GPCF/docs/harness/loop-state.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/12-GPCF/docs/harness/loops/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/02-governance/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/02-governance/loop/LOOP_CONTROL_BOARD.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/02-governance/loop/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-control-register.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/09-status/gpcf-project-status-matrix.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/91-治理与验收/09-status/kds-development-space-sync-register.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/development-space/开发/README.md` -> `kds_local_mirror_and_ledger`
- ` M` `.kds/sync-ledger.jsonl` -> `kds_local_mirror_and_ledger`

### GFIS

| 分类 | 数量 | 处置建议 |
|---|---:|---|
| `gfis_demo_regression` | 3 | 只作为 pass_demo_only 展示层回归候选 |
| `gfis_runtime_repair` | 265 | 优先作为 runtime repair 提交候选复核 |
| `legacy_or_prior_loop_round_artifacts` | 203 | 按历史轮次证据归档或提交，不能计为新实质轮次 |
| `project_documentation` | 12 | 复核是否属于主体定位或治理文档更新 |
| `unclassified_requires_manual_review` | 3 | 人工判定归属后再提交 |

前 20 项样例：

- ` M` `AGENTS.md` -> `project_documentation`
- ` M` `PROJECT_HARNESS_MANIFEST.md` -> `project_documentation`
- ` M` `README.md` -> `project_documentation`
- ` M` `docs/03-mvp-implementation-plan.md` -> `project_documentation`
- ` M` `docs/05-construction-proof-workplan.md` -> `project_documentation`
- ` M` `docs/06-erpnext-local-validation-path.md` -> `project_documentation`
- ` M` `docs/07-p0-sop-to-erpnext-doctype-mapping.md` -> `project_documentation`
- ` M` `docs/09-demo-to-erpnext-traceability.md` -> `project_documentation`
- ` M` `docs/17-gcfis-functional-specification.md` -> `project_documentation`
- ` M` `docs/20-gcfis-core-flow-closure-matrix.md` -> `project_documentation`
- ` M` `docs/21-gcfis-risk-ledger-and-uat-plan.md` -> `project_documentation`
- ` M` `docs/harness/evidence/evidence-index.md` -> `gfis_runtime_repair`
- ` M` `docs/harness/loop-state.md` -> `gfis_runtime_repair`
- ` M` `docs/harness/loops/README.md` -> `gfis_runtime_repair`
- ` M` `docs/harness/metrics.md` -> `project_documentation`
- ` M` `gcfis_custom/gcfis_custom/api.py` -> `gfis_runtime_repair`
- ` M` `gcfis_custom/gcfis_custom/install/doctypes.py` -> `unclassified_requires_manual_review`
- ` M` `gcfis_demo/validation/runtime_api_dry_run_result.json` -> `gfis_demo_regression`
- ` M` `scripts/validate_gfis_work_order_api_contract.py` -> `gfis_runtime_repair`
- ` M` `tests/e2e/gcfis-core-flow.spec.js` -> `gfis_demo_regression`
