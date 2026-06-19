---
doc_id: GPCF-DOC-C4980D88C1
title: KDS Phase 10 Self-refresh Stabilization Workpack
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/kds-phase10-self-refresh-stabilization-workpack-20260619.md
source_path: docs/harness/evidence/kds-phase10-self-refresh-stabilization-workpack-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS Phase 10 Self-refresh Stabilization Workpack

日期：2026-06-19

## 目的

本工作包用于降低 Phase 9 后续运行中的短暂门禁冲突，尤其是自刷新报告、生成型 README 和 KDS 本地镜像之间的 hash 追逐。

## 已确认的自刷新面

| source_path | disposition | rule |
|---|---|---|
| `09-status/kds-development-space-sync-plan.md` | hold_self_refresh | sync plan 生成结果，不作为普通业务文档追逐 |
| `09-status/kds-readonly-probe-report.md` | hold_self_refresh | readonly probe 结果，不作为普通业务文档追逐 |
| `09-status/globalcloud-document-health-report.md` | controlled_self_refresh | Loop gate 输出；允许 directed sync，但不得循环追逐 |
| generated `README.md` surfaces | hold_until_self_refresh_stable | 先稳定批次，再小批量同步 |

## 本轮已加固项

| item | result |
|---|---|
| `loop_document_gate.py` health report doc_id | fixed to `GPCF-DOC-C436DDB0F6` |
| health report local mirror | written together with source report |
| KDS conflict guard after self-refresh | pass |
| sync plan after self-refresh | pass |

## 可重复运行顺序

```bash
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/kds_conflict_guard.py
python3 tools/kds-sync/kds_sync_plan.py --require-clean-plan
python3 tools/kds-sync/classify_kds_sync_backlog.py --print-summary
```

若 `loop_document_gate.py` 被运行并改写 `09-status/globalcloud-document-health-report.md`，必须先确认：

```bash
python3 tools/kds-sync/kds_conflict_guard.py
python3 tools/kds-sync/kds_sync_plan.py --require-clean-plan
```

仅当 health report 出现在 plan 的 update 队列，且其它门禁通过时，才可使用：

```bash
python3 tools/kds-sync/kds_sync_apply.py --confirm-development-space --source-path 09-status/globalcloud-document-health-report.md
```

## 禁止事项

- 不用 health report 的 hash 漂移触发全局 KDS 写入。
- 不把 README 生成面作为业务完成或验收完成依据。
- 不将 self-refresh 报告的 KDS 同步写成全局 backlog 清零。
- 不升级 `accepted` 或 `integrated`。
