---
doc_id: GPCF-DOC-24E6A9A471
title: CodeGraph Sync 授权包证据
project: KDS
related_projects: [KDS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-sync-authorization-pack-20260621.md
source_path: docs/harness/evidence/codegraph-sync-authorization-pack-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Sync 授权包证据

本轮执行 `GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009`，目标是把 Brain 的 zero-pending monitor-only 状态与 Studio 的 `action_required` 漂移转成可审计的 sync-only 授权边界。本轮只生成授权包，不执行 Brain/Studio `codegraph sync`。

当前状态：`sync_authorization_pack_ready`。

边界说明：本轮 not execute Brain/Studio sync-only closure。

## 授权请求

需要用户明确回复以下口令后，才允许下一轮执行 Studio CodeGraph sync-only closure：

`授权执行 Brain/Studio CodeGraph sync-only closure`

## 候选仓

| repo | pending | threshold_result | 授权后允许命令 |
|---|---|---|---|
| GlobalCloud Brain | added=0 / modified=0 / removed=0 | green | `monitor_only; no sync required` |
| GlobalCloud Studio | added=0 / modified=18 / removed=0 | action_required | `codegraph sync && codegraph status --json . && git status --short -- .codegraph` |

## 禁止动作

- 不改 Brain/Studio 业务文件。
- 不执行 `git add`、`git commit`、`git push`。
- 不部署。
- 不写生产或外部 API。
- 不升级 accepted / integrated / production_ready。

## 授权后执行协议

1. 在 Brain 和 Studio 分别运行 `codegraph status --json .`。
2. 在 Brain 和 Studio 分别运行 `git status --short -- .codegraph`，若有输出立即停止。
3. 仅对 Studio 运行 `codegraph sync`。
4. 重跑 `codegraph status --json .`，要求 Brain 维持 `pendingChanges=0`，Studio 的 `pendingChanges` 全部为 0。
5. 重跑 `git status --short -- .codegraph`，要求无输出。
6. 只在 GPCF 记录 evidence，不触碰业务开发任务。

## 回滚

`.codegraph` 已 Git 隔离，因此 sync-only 不需要 Git rollback。若 sync 失败，只记录失败 evidence，不修改业务文件；若 `.codegraph` 出现在 Git status，立即停止并等待用户复核。

## Impact Gate 采样

| 命令 | 当前结果 |
|---|---|
| `codegraph query codegraph_drift_alert_thresholds --json` | 4 results，top result 是 `validate_codegraph_drift_alert_thresholds.py` |
| `codegraph node tools/kds-sync/validate_codegraph_drift_alert_thresholds.py` | 160 lines / 12 symbols / 0 dependents |
| `codegraph affected tools/kds-sync/validate_codegraph_drift_alert_thresholds.py --json` | 0 affected tests / 0 traversed dependents |
| `rg` 文本扫描 | 13 files / 29 lines |

## 下一轮

`GPCF-CODEGRAPH-SYNC-ONLY-CLOSURE-010`
