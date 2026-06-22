---
doc_id: GPCF-DOC-FB9A023039
title: CodeGraph Watchlist Threshold Review 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.md
source_path: docs/harness/evidence/codegraph-watchlist-threshold-review-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph Watchlist Threshold Review 2026-06-22

本轮执行 `GPCF-CODEGRAPH-WATCHLIST-THRESHOLD-REVIEW-005`，结论为 `watchlist_threshold_review_no_new_sync_authorization`。

本轮只做 watchlist 阈值评审，不执行 Brain / KDS / GFIS / Studio sync，不进入任何项目业务开发，不提交、不推送、不部署，不升级 accepted / integrated / production_ready。

## 阈值规则

| 类型 | 规则 |
| --- | --- |
| normal repo watch | `1 <= pending_total <= 5` 且 `added == 0` 且 `removed == 0` |
| normal repo action_required | `pending_total >= 6` 或 `added >= 1` 或 `removed >= 1` |
| GFIS policy exception watch | GFIS 维持既有 residual policy exception：`pending_total == 1` 且 `added == 1` |
| GPCF self sync | GPCF 本轮治理证据落盘后可执行本仓 CodeGraph self-sync |
| non-GPCF sync | 必须有新的显式授权，本轮没有新授权 |

## 本轮观测

| repo | pending | threshold_result | decision |
| --- | ---: | --- | --- |
| GlobalCloud Brain | added=0 / modified=4 / removed=0 | watch | no_new_sync_authorization |
| GlobalCloud KDS | added=0 / modified=1 / removed=0 | watch | no_sync |
| GlobalCloud GFIS | added=1 / modified=0 / removed=0 | policy_exception_watch | no_sync |
| GlobalCloud Studio | added=0 / modified=0 / removed=0 | steady | no_action |
| GlobalCoud GPCF | added=5 / modified=4 / removed=0 | self_sync_required_after_evidence | gpcf_self_sync_after_evidence_only |

## 边界声明

- Brain 当前为 active drift watch，但未达到本轮 action_required 阈值；不得声明 Brain 已长期稳定。
- KDS 当前为 modified=1 的 watch 项；不得执行 KDS canonical write 或 KDS CodeGraph sync。
- GFIS 仍是 policy_exception_watch；不得把 GFIS residual 解释为已修复。
- Studio 当前为 steady；不得因 Studio steady 推导 Brain/KDS/GFIS 已完成。
- GPCF 只允许在本轮证据落盘后执行本仓 `codegraph sync .`，用于清零本轮治理证据造成的本仓 pending。

## 验证口径

本轮 validator 必须重新读取实时 `codegraph status --json .`，并检查 `.codegraph/` 未进入 Git 状态。若 Brain/KDS 的 pending 超过阈值、GFIS policy exception 改变、或 GPCF self-sync 后未清零，则本轮不得关闭。

## 下一轮

进入 `GPCF-CODEGRAPH-WATCHLIST-MONITOR-006`：继续监控 Brain/KDS/GFIS/Studio watchlist，并保持非 GPCF sync 需要显式授权。另有独立阻塞项 `GPCF-LOOP-DOCUMENT-LOCALIZATION-DEBT-TRIAGE`，用于处理 `loop_document_gate.py` 的历史中文本地化债务。
