---
doc_id: GPCF-DOC-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001
title: Loop Round GPCF Headroom LCX Real Measurement External Receipt Completion Package 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-REAL-MEASUREMENT-EXTERNAL-RECEIPT-COMPLETION-PACKAGE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Real Measurement External Receipt Completion Package 001

## run

### 输入

- 外部授权回执模板
- 外部回执实例预检 evidence

### 动作

- `python3 tools/kds-sync/build_headroom_lcx_real_measurement_external_receipt_completion_package.py`
- 生成 completed receipt 填写模板和负向校验规则。
- 不生成正式 completed receipt 实例。

### 输出

- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.json`
- `docs/harness/evidence/headroom-lcx-real-measurement-external-receipt-completion-package-20260623.md`
- `fixtures/headroom/headroom-lcx-real-measurement-external-authorization-receipt.completed.template.json`

## stop

- stop_type: authorization_boundary
- stop_reason: 需要人工按模板填写正式 completed receipt，当前不得自动生成。

## verify

### 检查

- `python3 tools/kds-sync/validate_headroom_lcx_real_measurement_external_receipt_completion_package.py`

## recover

- 删除本轮 completion package 和 template 即可回退。
- 禁止恢复为生产执行状态。

## debug

### 反馈

- 本轮只产生填写包，正式 receipt 仍未记录。

### 下一轮

- 等待人工提供 completed receipt，或继续生成 completed receipt 负向 fixtures。
