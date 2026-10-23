---
doc_id: GPCF-DOC-F023-REMAINING-REFS-20261024
title: F-023 旧流名残余引用清单（2026-10-24）
project: GPCF
related_projects: [WAS, KDS]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
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
