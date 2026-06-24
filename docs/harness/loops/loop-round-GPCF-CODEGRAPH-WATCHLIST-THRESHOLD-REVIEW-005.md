---
doc_id: GPCF-DOC-7AAEB2E376
title: Loop Round GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005

## 输入

- 用户输入：`下一步`
- 上轮输出：`GPCF-CODEGRAPH-PROJECT-GROUP-STEADY-STATE-RECHECK-004`
- 受控目标：复核 Brain/KDS/GFIS/Studio/GPCF watchlist 阈值，判断是否触发新的 sync 授权。

## 动作

- 只读检查 Brain、KDS、GFIS、Studio、GPCF 的 `codegraph status --json .`。
- 只读检查目标仓库 `.codegraph/` 是否进入 Git 状态。
- 生成阈值评审 JSON/Markdown 证据。
- 生成可回放 validator。
- 仅在证据落盘后对 GPCF 执行本仓 `codegraph sync .`。

## 输出

- `docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.json`
- `docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.md`
- `tools/kds-sync/validate_codegraph_watchlist_threshold_review_20260622.py`

## 检查

- Brain pending=4，阈值结果为 watch，不触发新 sync 授权。
- KDS pending=1，阈值结果为 watch，不执行 sync。
- GFIS pending=1 且 added=1，保持 policy_exception_watch。
- Studio pending=0，保持 steady。
- GPCF 本轮证据落盘后允许 self-sync，并要求 self-sync 后 pending=0。
- `.codegraph/` 不得进入 Git 状态。

## 反馈

本轮关闭条件不是“项目群长期静止”，而是“阈值评审完成且未触发新的非 GPCF sync 授权”。任何后续 Brain/KDS/GFIS 漂移都必须由下一轮实时检查重新判定。

## 非声明

- 不声明 Brain / KDS / GFIS / Studio 已完成业务修复。
- 不声明 GFIS policy exception 已消失。
- 不声明 accepted / integrated / production_ready。
- 不声明 KDS canonical write 已执行。
- 不声明 Git 已提交或已推送。

## 下一轮

`GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`
