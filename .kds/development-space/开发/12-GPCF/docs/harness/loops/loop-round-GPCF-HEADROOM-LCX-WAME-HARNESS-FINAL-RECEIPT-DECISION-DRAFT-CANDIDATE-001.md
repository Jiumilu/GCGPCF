---
doc_id: GPCF-DOC-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001
title: Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Draft Candidate 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-WAES-HARNESS-FINAL-RECEIPT-DECISION-DRAFT-CANDIDATE-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX WAES Harness Final Receipt Decision Draft Candidate 001

## run

### 输入

- final receipt decision request
- final receipt decision human fill request

### 动作

- `python3 tools/kds-sync/build_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py`
- 生成建议回填草稿，但不生成正式 response。

### 输出

- `docs/harness/evidence/headroom-lcx-waes-harness-final-receipt-decision-draft-candidate-20260623.json`
- `fixtures/headroom/headroom-lcx-waes-harness-final-receipt-decision.response.draft.candidate.json`

## stop

- stop_type: authorization_boundary
- stop_reason: draft candidate 仅供参考，仍需 WAES/Harness 独立签署正式 response。

## verify

### 检查

- `python3 tools/kds-sync/validate_headroom_lcx_waes_harness_final_receipt_decision_draft_candidate.py`

## recover

- 删除本轮 draft candidate evidence 与 fixture 即可回退。

## debug

### 反馈

- 草稿已生成，但仍不是 formal decision。

### 下一轮

- 需要 WAES/Harness 独立回填正式 response.json。
