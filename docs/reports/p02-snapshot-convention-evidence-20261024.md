---
doc_id: GPCF-DOC-CDEC3636A1
title: "P02 快照重建口径：运维实证（2026-10-24 16:05）"
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p02-snapshot-convention-evidence-20261024.md
source_path: docs/reports/p02-snapshot-convention-evidence-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P02 快照重建口径：运维实证（2026-10-24 16:05）

- 目标依据：P02「门禁可复现 + 保持快照重建口径」（老卢 2026-10-22 20:20 裁定：其他仓有提交即重建并提交快照，不 push、不碰其他文件）
- 本次核查对象：launchd `ai.globalcloud.gpcf-snapshot` → `~/bin/rebuild_live_status_snapshot.sh`（每 1800s）

## 1. 运行态核查

| 项 | 实测 |
|---|---|
| launchd 任务 | `ai.globalcloud.gpcf-snapshot` **已加载**（`launchctl list` 有记录，exit 0） |
| 最近执行 | 15:10:33 skipped / 15:41:13 committed / 16:03:12 committed |
| 快照新鲜度 | `generated_at = 2026-10-24T15:54:14+08:00`，`freshness_ok=true` |
| 重建日志 | `~/logs/gpcf-snapshot/rebuild.log` |

## 2. 发现的问题与修复

日志中存在 2 次 `commit skipped (hook)`（14:39、15:10）——提交被 pre-commit 钩子/并发索引锁打断，
原脚本**一次性尝试、失败后静默放弃**，导致该周期内快照未入库但无人知晓。

**修复**（`~/bin/rebuild_live_status_snapshot.sh`，用户级运维脚本，非仓内代码）：
1. 提交改为**最多 3 次重试**（每次间隔 10s，避开并发会话的 `.git/index.lock`）；
2. 失败时把最后一次 hook 错误尾部写入日志（不再静默）；
3. 日志记录实际尝试次数，便于巡检定位。

**修复后实测**：`2026-10-24 16:04:27 committed snapshot (attempt 1)` ✅

## 3. 回滚

```bash
cp /tmp/rebuild_backup.sh ~/bin/rebuild_live_status_snapshot.sh   # 若需回到单次尝试版本
launchctl kickstart -k gui/$(id -u)/ai.globalcloud.gpcf-snapshot   # 重载任务（可选）
```

## 4. 边界

- 快照只记录观测事实（HEAD/dirty/ahead），不改变任何项目状态；
- 本次修复不触碰仓内代码，不影响门禁口径。
