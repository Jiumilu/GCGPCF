---
doc_id: GPCF-DOC-80A0BC302D
title: "Mem/PQC CI 排队根因：runner 离线（且不在本机）· 2026-10-24 17:20"
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/ci-queue-root-cause-20261024.md
source_path: docs/reports/ci-queue-root-cause-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# Mem/PQC CI 排队根因：runner 离线（且不在本机）· 2026-10-24 17:20

- 现象：GCMem / GCPQC 的 `test-build` 自 16:23–16:34 起一直 `queued`，其余 5 仓已绿
- 排查结论：**不是配置问题、不是容量问题**，而是这两个仓的 self-hosted runner 处于 **offline**

## 1. 证据

| 仓 | runner 名 | 状态（GitHub API） |
|---|---|---|
| GCSOP | `gc-macmini-GCSOP` | ✅ online（已绿） |
| GCMem | `gc-macmini-GCMem` | ❌ **offline** |
| GCPQC | `gc-macmini-GCPQC` | ❌ **offline** |

本机巡检报告（`runtime/ops/reports/runner-health-latest.md`，17:19）：
**仓数 30 · offline 2 · 隧道失败 0 · runner 进程数 29**，仅 GCMem / GCPQC 离线。

## 2. 尝试修复（未成功，无副作用）

按 `runtime/ops/self-hosted-runner.md` 标准做法执行：
```bash
launchctl kickstart -k gui/501/ai.globalcloud.gc-runner.GCMem
launchctl kickstart -k gui/501/ai.globalcloud.gc-runner.GCPQC
```
结果：`Could not find service ... in domain for user gui: 501`。

进一步核查：
- `launchctl list | grep gc-runner` → **0 条**
- `~/Library/LaunchAgents/` 中无 `gc-runner.*` plist

→ 这 2 个（连同其余 27 个在线 runner）**不在本机运行**，本机只是"看到"它们在线/离线；
因此**无法从本机重启**，需在 runner 实际所在主机（手册提到 MacBook `~/actions-runner-gpcf` 一类部署）执行。

## 3. 需要的动作

| 动作 | 责任人 | 判据 |
|---|---|---|
| 在实际主机启动/重启 GCMem、GCPQC 的 runner 服务 | 运维（老卢） | GitHub API 中两个 runner 变 online；排队 run 自动开始 |
| 若 2 仓不再需要 self-hosted（可改 GitHub 托管 runner） | 属主 | 见手册"public 仓使用 hosted runner"口径 |

## 4. 透明记录

- 本轮排查时手动运行了 `runtime/ops/runner_health.py`（**未加 `--no-email`**），因此额外发送了 1 封巡检邮件（本应由 launchd 定时发送）。后续只读排查会加 `--no-email`。
- 本次尝试未改动任何仓或服务状态。
