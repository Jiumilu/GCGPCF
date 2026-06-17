---
doc_id: GPCF-DOC-B1085FD000
title: KDS API 同步流水覆盖事件记录
project: GPCF
related_projects: [GPCF, WAES, KDS]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/kds-api-sync-ledger-incident-20260617.md
source_path: 09-status/kds-api-sync-ledger-incident-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS API 同步流水覆盖事件记录

日期：2026-06-17

## 事件

在 KDS Markdown 化与 OKF 兼容层全面实施闭环执行过程中，`document_control.py` 将 `.kds/sync-ledger.jsonl` 重写为本地镜像流水，覆盖了此前由 `kds_sync_apply.py` 追加的真实 KDS API 写入流水。

## 影响

- 真实 KDS 远端写入已经执行并通过只读探测与同步计划收敛验证。
- 早段每条 API 写入的 JSONL 流水无法从本地文件完整恢复。
- 不得伪造 `http_200` API ledger 条目补齐缺口。

## 已修复

- `document_control.py` 改为写入 `.kds/local-mirror-ledger.jsonl`。
- `kds_sync_apply.py` 继续写入 `.kds/sync-ledger.jsonl`。
- `loop_document_gate.py` 区分本地镜像流水和真实 API 同步流水。
- `.kds/sync-ledger.jsonl` 已保留一条 `api_sync_ledger_overwrite_incident` 记录，后续真实写入继续追加 `http_200` 记录。

## 当前可用证据

| evidence | result |
| --- | --- |
| `kds_readonly_probe.py` | pass |
| `kds_sync_plan.py --require-clean-plan` | pass |
| final sync plan | `create=0`, `update=0`, `conflicts=0`, `missing_local=0`, `self_refresh=2` |
| remote documents | `712` |
| `.kds/sync-ledger.jsonl` | 1 条 incident + 修复后的真实 API 写入流水 |
| `.kds/local-mirror-ledger.jsonl` | 本地镜像流水 |

## 后续规则

- 不得再将本地镜像流水写入 `.kds/sync-ledger.jsonl`。
- 真实 KDS 写入只能由 `kds_sync_apply.py` 追加 API ledger。
- 若需要审计早段写入，只能引用命令输出、KDS 远端只读状态和最终同步计划，不得补造逐条 API ledger。
