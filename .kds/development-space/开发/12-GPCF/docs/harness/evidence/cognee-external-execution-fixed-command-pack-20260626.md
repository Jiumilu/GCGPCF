---
doc_id: GPCF-DOC-6E4E6C9A41
title: Cognee 外部执行固定命令包 2026-06-26
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/cognee-external-execution-fixed-command-pack-20260626.md
source_path: docs/harness/evidence/cognee-external-execution-fixed-command-pack-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Cognee 外部执行固定命令包 2026-06-26

## 1. 当前结论

`cognee_external_execution_fixed_command_pack = prepared`

本文冻结 Cognee 外部执行验证前必须先跑的本地命令包。它只定义执行前校验顺序，不代表真实外部执行已经发生。

## 2. 固定命令包

```bash
python3 tools/kds-sync/validate_cognee_p4_live_authorization_signoff.py \
  --require-complete-signoff

python3 loop/context/cognee/scripts/validate-cognee-p4-real-writeback-live.py \
  --input docs/harness/evidence/cognee-p4-real-writeback-live-20260624.json

python3 tools/kds-sync/validate_cognee_external_execution_integration_intake.py \
  --require-complete-intake
```

## 3. 预期门禁结果

| command | expected_result |
|---|---|
| `validate_cognee_p4_live_authorization_signoff.py --require-complete-signoff` | `pass_complete` |
| `validate-cognee-p4-real-writeback-live.py --input ...` | `pass` |
| `validate_cognee_external_execution_integration_intake.py --require-complete-intake` | `pass_complete` |

## 4. 失败即停止规则

| item | rule |
|---|---|
| signoff fail | 不进入外部执行验证 |
| live rehearsal fail | 退回 `GPCF-COGNEE-P4-REAL-WRITEBACK-LIVE-001` 链路修复 |
| intake fail | 退回 `GPCF-DOC-LOOP-COGNEE-EXTERNAL-EXECUTION-INTEGRATION-002` 重收口 |

## 5. 非声明

- 不声明固定命令包已经实际执行
- 不声明 `Cognee 已全量运行`
- 不声明 `production_write=true`
- 不声明 `accepted=true`
- 不声明 `integrated=true`
- 不声明 `production_ready=true`
