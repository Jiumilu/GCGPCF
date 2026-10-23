---
doc_id: GPCF-DOC-AE6A14367C
title: F-013 · KDS 脏工作树收敛请求（交 KDS 属主）
project: KDS
related_projects: [GPC, WAME, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/f013-kds-dirty-worktree-request-20261022.md
source_path: docs/reports/f013-kds-dirty-worktree-request-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-013 · KDS 脏工作树收敛请求（交 KDS 属主）

- 日期：2026-10-22｜提出方：GPCF｜受理方：KDS 属主
- F-013 现状：`close_candidate=false`，唯一原因为治理阻塞
- GPCF 侧已做：补 `verification.tests/build` + 豁免范围理由（P05），复跑已无证据类理由

## 1. 阻塞事实（feature.yaml blockers 原文要点）

1. `kds_p1_apply_blocked_by_dirty_worktree`——KDS 工作树脏项阻止 P1 应用；
2. `gpcf_a10r27_current_truth_4file_delta_pending_independent_review_and_separate_commit_push_disposition`——4 文件 delta 待独立复核与单独提交处置。

## 2. 请求 KDS 属主完成的三件事

| # | 动作 | 判据 |
|---|---|---|
| 1 | 收敛 KDS 工作树：把脏项分为"本轮要提交/登记延后/清理"三类 | `git -C "GlobalCloud KDS" status --porcelain -uall` 条数落在登记清单内 |
| 2 | 对 4 文件 delta 做独立复核并单独提交（或登记为受控例外） | 独立 commit hash 或例外登记（approved_by + 到期日） |
| 3 | 回填 F-013 证据（summary 更新，注明脏树收敛结论） | `python3 scripts/gpcf_check_evidence.py F-013 --check-only` 仅剩可解释项 |

## 3. GPCF 不代做的事

- 不代写 KDS 仓、不代跑 KDS 清理、不代替属主提交；
- 不对 KDS 的业务内容做裁定。

## 4. 完成后

属主回复后，GPCF 解除 F-013 阻塞（走 `resolved_blockers` + 回执），并复跑证据检查。
