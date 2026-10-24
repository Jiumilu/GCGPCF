---
doc_id: GPCF-DOC-F023-REMAINING-REFS-20261024
title: F-023 旧流名残余引用清单（2026-10-24）
project: GPCF
related_projects: [WAS, KDS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-023-was-flow-naming-migration/evidence/remaining-references-20261024.md
source_path: features/active/F-023-was-flow-naming-migration/evidence/remaining-references-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-023 旧流名残余引用清单

扫描范围：GPCF `tools/`、`scripts/`、`tests/`、`fixtures/`（不含 .kds）。
结果：**11 文件 / 28 处**仍含八流旧名。

## 1. 按文件

| 文件 | 命中 |
|---|---:|
| `tools/kds-sync/validate_was_scenario_profile_matrix.py` | 8 |
| `fixtures/was/scenario-profile-matrix-positive.json` | 8 |
| `tools/kds-sync/validate_was_loop_context_coverage.py` | 3 |
| `tools/kds-sync/validate_gfis_was_source_record_admission_gate.py` | 2 |
| `tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py` | 1 |
| `tools/kds-sync/validate_was_real_source_record_candidate_precheck.py` | 1 |
| `fixtures/was/p4-real-source-record-candidate-negative-wrong-dimension.json` | 1 |
| `fixtures/was/p4-real-source-record-candidate-positive.json` | 1 |
| `fixtures/was/p4-real-source-record-candidate-negative-missing-runtime-site-context.json` | 1 |
| `fixtures/was/p4-real-source-record-candidate-negative-llm-only.json` | 1 |
| `fixtures/was/p4-real-source-record-candidate-negative-missing-source.json` | 1 |

## 2. 建议批次

1. **一致性批次**：`validate_was_scenario_profile_matrix.py` + `scenario-profile-matrix-positive.json` 同步切 V1.2 八流名（含新增 Value/Credit/Scenario 口径）。
2. **admission/precheck 批次**：3 个 `validate_*` 中 `commerce_flow` 改为 `ServiceFlow`，并保留 `{"ServiceFlow","commerce_flow"}` 兼容断言范围。
3. **fixtures 批次**：5 个 p4 candidate fixture 的 `flowType` 改 `ServiceFlow`/`FinancialFlow`；同步检查负例语义仍成立。
4. 每批跑对应 validator + `validate_was_scenario_profile_matrix`，再更新本清单。

## 3. 非声明

- 本轮只盘点，未改任何文件；兼容窗口仍需另定关闭时点。

## 2026-10-24 批次可行性复核

- **批 2（admission/precheck）**：`validate_gfis_was_source_record_admission_gate.py` 依赖 WAS 仓
  `okf/examples/gfis-runtime-sop-e2e-was-profile.yaml` 的 `flowType`；
  证据 JSON 的 `target_stage.flow_type` 也需同步。属跨项目（WAS）改动，GPCF 侧无法单独完成。
- **批 1（scenario matrix）**：需同步 GPCF evidence JSON/MD + loop round + WAS schema 口径，跨项目。
- **批 3（fixtures）**：GPCF 内可改，但需与 WAS profile/validator 同批，避免断链。
- 结论：F-023 残余迁移需 WAS 属主共同排期；本轮不改文件。

## 2026-10-24 批 3 部分完成

- 5 个 `p4-real-source-record-candidate-*.json` 已迁移：
  - `commerce_flow` → `ServiceFlow`（4 个）
  - `capital_flow` → `FinancialFlow`（1 个 wrong-dimension 负例）
- `validate_was_real_source_record_candidate_precheck.py` 接受集合改为 `{ServiceFlow, commerce_flow}`。
- 该 validator 复跑 pass（positive 1 / negative 4）。
- 剩余：2 文件 / 16 处（scenario matrix validator 8 + positive fixture 8）；loop context 已迁 ServiceFlow。
- 注意：admission/submission 两个 validator 当前因旧路径 `WAS世界资产体系` 不存在而 fail（既有问题，与本次改动无关）。

## 2026-10-24 批 2 兼容层收紧

- admission/submission/precheck 三个 validator 的 flow 断言已收紧为 `ServiceFlow`；
- 三个 validator 均 pass；旧流名仅余 scenario matrix（需批 1 决策）与 loop context 历史断言。

## 2026-10-24 loop context 迁移

- 13 个 covered loop 文档的 `loop_was_context.related_flows` 由 `commerce_flow` 改为 `ServiceFlow`；
- `validate_was_loop_context_coverage.py` 期望与输出同步；validator pass。
