---
doc_id: GPCF-DOC-D83FE8C1B1
title: Loop Round GPCF Headroom LCX Sanitized Measurement Dry Run 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-SANITIZED-MEASUREMENT-DRY-RUN-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX Sanitized Measurement Dry Run 001

## 输入

- WAES/Harness 已准入 `admitted_for_sanitized_measurement_precheck`。
- 当前只允许脱敏台账元数据 dry-run。

## 动作

- 运行 `python3 tools/kds-sync/run_headroom_lcx_sanitized_measurement_dry_run.py --check-only`。
- 校验脱敏台账结构和安全边界。
- 不计算真实生产 token 节省，不启动 production proxy。

## 输出

- `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.json`
- `docs/harness/evidence/headroom-lcx-sanitized-measurement-dry-run-20260622.md`

## 检查

- `python3 tools/kds-sync/validate_headroom_lcx_sanitized_measurement_dry_run.py`
- `python3 tools/kds-sync/validate_headroom_lcx_authorized_measurement_precheck.py`

## 反馈

- dry-run runner 骨架已建立。
- 当前仍不得进入生产 token 测量。
- `accepted=false`、`integrated=false`、`production_ready=false`。

## 下一轮

建立只读 metadata replay 校验；仍不得读取原文或启动生产代理。
