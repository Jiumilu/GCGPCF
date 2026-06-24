---
doc_id: GPCF-DOC-A7161F4187
title: Loop Round GPCF Headroom LCX Metadata Replay Check 001
project: GPCF
related_projects: [GPC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-METADATA-REPLAY-CHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Metadata Replay Check 001

## 输入

- 上轮已建立 sanitized measurement dry-run skeleton。
- 本轮只允许 check-only metadata replay。

## 动作

- 运行 `python3 tools/kds-sync/run_headroom_lcx_metadata_replay_check.py --check-only`。
- 校验字段映射、项目标记、gate marker 和 evidence schema。
- 不读取原文、不计算真实生产节省、不启动 production proxy。

## 输出

- `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.json`
- `docs/harness/evidence/headroom-lcx-metadata-replay-check-20260622.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_metadata_replay_check.py`
- `python3 tools/kds-sync/validate_headroom_lcx_sanitized_measurement_dry_run.py`

## 反馈

- metadata replay 校验已建立。
- 当前仍不得进入生产 token 测量。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

建立 marker/retrieval miss 对比门禁；仍不得读取原文或启动生产代理。
