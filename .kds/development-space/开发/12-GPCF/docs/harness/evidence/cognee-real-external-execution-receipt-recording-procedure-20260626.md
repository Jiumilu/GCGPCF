---
doc_id: GPCF-DOC-4C30871182
title: Cognee 真实外部执行回执登记流程 2026-06-26
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-real-external-execution-receipt-recording-procedure-20260626.md
source_path: docs/harness/evidence/cognee-real-external-execution-receipt-recording-procedure-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 真实外部执行回执登记流程 2026-06-26

## 1. 当前结论

`cognee_real_external_execution_receipt_recording_procedure = defined_pending_real_receipt`

本文定义真实外部执行回执到来后的登记、复核和 readiness 更新流程。当前只是流程定义，尚未收到真实回执。

## 2. 流程文件

- JSON: `fixtures/cognee/cognee-real-external-execution-receipt-recording-procedure.json`
- validator: `tools/kds-sync/validate_cognee_real_external_execution_receipt_recording_procedure.py`
- source receipt intake: `docs/harness/evidence/cognee-real-external-execution-receipt-intake-20260626.md`
- source readiness rollup: `docs/harness/evidence/cognee-full-run-readiness-rollup-20260626.md`

## 3. 登记步骤

| step | action | required_output |
|---|---|---|
| `RECEIPT-RECORD-001` | `receive_real_external_execution_receipt` | `real_receipt_ref_and_receipt_id` |
| `RECEIPT-RECORD-002` | `reject_completed_example_or_template_receipt` | `non_sample_receipt_boundary_confirmed` |
| `RECEIPT-RECORD-003` | `fill_receipt_intake_fields` | `receipt_intake_updated_with_real_counts` |
| `RECEIPT-RECORD-004` | `run_receipt_intake_validator_require_real_receipt` | `cognee_real_external_execution_receipt_intake=pass_real` |
| `RECEIPT-RECORD-005` | `update_readiness_rollup_gap_001_only` | `gap_001_ready_true_without_full_run_claim` |
| `RECEIPT-RECORD-006` | `rerun_readiness_rollup_validator` | `readiness_rollup_recomputed` |

## 4. 禁止输入

| input | reason |
|---|---|
| `fixtures/cognee/cognee-external-execution-receipt.completed.example.json` | completed example 不是真实执行回执 |
| `docs/harness/evidence/cognee-external-execution-receipt-completed-example-20260626.md` | 样例 evidence 不是真实执行回执 |
| `template_only_receipt` | 模板不能关闭 GAP-001 |
| `operator_note_without_receipt` | 仅有操作备注不能替代回执 |

## 5. 必跑命令

```bash
python3 tools/kds-sync/validate_cognee_real_external_execution_receipt_intake.py \
  --require-real-receipt

python3 tools/kds-sync/validate_cognee_full_run_readiness_rollup.py
```

## 6. 状态边界

| field | value |
|---|---|
| `procedure_status` | `defined_pending_real_receipt` |
| `production_write` | `false` |
| `accepted` | `false` |
| `integrated` | `false` |
| `production_ready` | `false` |
| `full_run_claim` | `false` |

## 7. 非声明

- 不声明真实外部执行回执已经收到
- 不声明 GAP-001 已关闭
- 不声明 readiness 已变为 ready
- 不声明 `Cognee 已全量运行`
