---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-20260622
title: Loop Round GPCF Headroom LCX L3.5 Controlled Sanitized Pilot Window 001
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-CONTROLLED-SANITIZED-PILOT-WINDOW-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX L3.5 Controlled Sanitized Pilot Window 001

## 输入

用户回复“批准”，批准进入 L3.5 受控脱敏试点窗口。

## 动作

- run: 生成 L3.5 controlled sanitized pilot window，并对 15 项目域 45 条脱敏 fixture 做 replay smoke 记录。
- stop: 停止边界固定为 L3.5，不进入 L4/L5/生产，不启动 production proxy。
- verify: 复用 readiness package、negative gate、project-group replay stability，并运行本轮 validator。
- recover: 若 L3.5 失败，回退到 readiness package 和 project-group replay stability，不影响任何生产路径。
- debug: 当前剩余阻塞是无真实生产 token 实测、无运行时业务答案等价证明、无生产准入。

## 输出

- `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.json`
- `docs/harness/evidence/headroom-lcx-l35-controlled-sanitized-pilot-window-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_l35_controlled_sanitized_pilot_window.py
python3 tools/kds-sync/validate_headroom_lcx_l35_controlled_sanitized_pilot_window.py
```

## 反馈

L3.5 窗口只允许本机脱敏 fixture replay 和 evidence 生成。所有生产、KDS API、外部 API、状态升级能力仍关闭。

## 下一轮

扩展 L3.5 pilot 为多轮稳定性窗口，或生成 L4 真实测量授权申请包。
