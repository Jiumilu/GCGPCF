---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001
title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Negative Fixtures 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-NEGATIVE-FIXTURES-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Real Measurement External Receipt Negative Fixtures 001

## run

### 输入

- completed receipt 填写包

### 动作

- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py`
- 生成 completed receipt 负向 fixtures。
- 不生成正式 completed receipt 实例。

### 输出

- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.json`
- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-negative-fixtures-20260623.md`
- `fixtures/headroom/headroom-lcx-real-measurement-external-receipt-negative-fixtures.json`

## stop

- stop_type: authorization_boundary
- stop_reason: 负向 fixtures 只验证拒绝规则，不代表正式回执已经记录。

## verify

### 检查

- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_negative_fixtures.py`

## recover

- 删除本轮 negative fixtures、evidence 和 validator 即可回退。

## debug

### 反馈

- 本轮预期 11 个负向样本全部 rejected，accepted=0。

### 下一轮

- 等待人工填写正式 completed receipt，或建立正式 receipt intake validator。
