---
doc_id: GPCF-DOC-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-20260622
title: Loop Round GPCF Headroom LCX L3.5 Multi Window Stability 001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-L35-MULTI-WINDOW-STABILITY-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Loop Round GPCF Headroom LCX L3.5 Multi Window Stability 001

## 输入

用户要求进入下一轮。上一轮已完成 L3.5 受控脱敏试点窗口。

## 动作

- run: 基于 L3.5 单窗口证据生成 5 个脱敏 replay 窗口。
- stop: 停止边界固定为 authorization_boundary，不进入 L4/L5/生产。
- verify: 检查 5 个窗口的 15 项目覆盖、45 条记录、hash 稳定性和生产禁用门禁。
- recover: 若窗口漂移，回退到单窗口证据并阻断扩大试点。
- debug: 当前剩余阻塞仍是无真实生产 token 实测、无业务答案等价证明、无 L4/L5 授权。

## 输出

- `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.json`
- `docs/harness/evidence/headroom-lcx-l35-multi-window-stability-20260622.md`

## 检查

```bash
python3 tools/kds-sync/run_headroom_lcx_l35_multi_window_stability.py
python3 tools/kds-sync/validate_headroom_lcx_l35_multi_window_stability.py
```

## 反馈

本轮是批量生成的多窗口稳定性检查，按连续运行真实性门禁计为 1 个实质轮次，不作为 L4/L5/生产准入。

## 下一轮

生成 L4 真实测量授权申请包，或继续扩展 L3.5 的业务答案等价脱敏样例。
