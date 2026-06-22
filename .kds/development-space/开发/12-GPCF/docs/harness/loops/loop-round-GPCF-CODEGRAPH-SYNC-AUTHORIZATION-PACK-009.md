---
doc_id: GPCF-DOC-277A170C82
title: GPCF CodeGraph Sync Authorization Pack 009
project: GPCF
related_projects: [GFIS, GPC, WAES, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Sync Authorization Pack 009

## 输入

- 用户要求：建立下一阶段目标并执行。
- 上一轮输出：`GPCF-CODEGRAPH-SYNC-AUTHORIZATION-PACK-009`。
- 阈值来源：`docs/harness/evidence/codegraph-drift-alert-thresholds-20260621.json`。

## 动作

- 复核 Brain、Studio、GFIS、GPCF CodeGraph pending 状态。
- 生成 Brain/Studio sync-only 授权包。
- 明确授权口令、允许命令、禁止动作、回滚方案。
- 执行 `codegraph query`、`codegraph node`、`codegraph affected` 和 `rg` 对照。
- 生成 authorization pack evidence 与 validator。

## 输出

- `docs/harness/evidence/codegraph-sync-authorization-pack-20260621.json`
- `docs/harness/evidence/codegraph-sync-authorization-pack-20260621.md`
- `tools/kds-sync/validate_codegraph_sync_authorization_pack.py`

## 检查

- `python3 tools/kds-sync/validate_codegraph_sync_authorization_pack.py`
- `python3 tools/kds-sync/validate_codegraph_drift_alert_thresholds.py`
- `python3 tools/kds-sync/check_document_pollution.py`
- `python3 tools/kds-sync/validate_kds_token.py`
- `python3 tools/kds-sync/loop_document_gate.py --check-only`
- `git diff --check`

## 反馈

Brain 与 Studio sync-only 授权包已建立，当前状态为 `sync_authorization_pack_ready`。本轮未执行 Brain/Studio `codegraph sync`，未进入业务开发，未提交、未推送、未部署。下一轮只有在用户明确授权后才进入 `GPCF-CODEGRAPH-SYNC-ONLY-CLOSURE-010`。
