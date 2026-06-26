---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001
title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Precheck 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Real Measurement External Receipt Precheck 001

## run

### 输入

- 外部授权回执模板 evidence
- 预期正式外部回执路径

### 动作

- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_precheck.py`
- 检查正式外部回执实例是否存在且满足模板字段。

### 输出

- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.json`
- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-precheck-20260623.md`

## stop

- stop_type: authorization_boundary
- stop_reason: 正式外部回执实例未回填，真实测量继续阻断。

## verify

### 检查

- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_precheck.py`

## recover

- 删除本轮 precheck evidence 和 validator 即可回退，不影响模板和授权链。
- 禁止恢复为生产执行状态。

## debug

### 反馈

- 本轮确认缺正式外部 receipt，保持 blocked_missing_external_receipt_instance。

### 下一轮

- 需要用户提供正式外部回执实例，或继续生成 receipt completed 填写包。
