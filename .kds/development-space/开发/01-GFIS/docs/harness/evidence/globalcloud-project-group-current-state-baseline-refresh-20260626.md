---
doc_id: GPCF-DOC-PROJECT-GROUP-CURRENT-STATE-BASELINE-REFRESH-20260626
title: GlobalCloud Project Group Current State Baseline Refresh
project: GFIS
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: docs
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud Project Group Current State Baseline Refresh

## Control Facts

```text
project_group_current_state_baseline_refresh_20260626 = controlled
project_count = 17
recheck_date = 2026-06-28
git_gate = partial
dirty_repo_count = 3
review_boundary_repo_count = 3
noise_cleanup_repo_count = 0
pass_repo_count = 14
ahead_repos = 0
behind_repos = 0
sensitive_repos = 0
dirty_repos_current = GlobalCoud GPCF, GlobalCloud Brain, GlobalCloud SOP
review_boundary_repos_current = GlobalCoud GPCF, GlobalCloud Brain, GlobalCloud SOP
noise_cleanup_repo_current = none
sensitive_repos_current = none
diff_check = pass
development_queue_ready = true
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
auto_ready_for_review_upgrade = false
authorization_granted = false
action_executed = false
stage_allowed = false
commit_allowed = false
push_allowed = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## Live Repo Classes

```text
dirty>0 / untracked>=0 / diff_check=pass / governance_worktree_volatile
dirty>0 / untracked=0 / diff_check=pass / review_boundary_current
clean / diff_check=pass / sensitive_path=resolved_not_in_git_status
```

KDS blocker 已解除。`GlobalCloud KDS` 当前为 clean / ahead=0 / behind=0 / diff_check=pass，不再属于当前 dirty/sensitive 阻塞源；真实 KDS API sync、live API、deploy、schema migrate 和状态提升仍未授权。

## Project Scope

17 项目覆盖：GlobalCloud AAAS、GlobalCloud Brain、WAS世界资产体系、GlobalCloud XiaoC、GlobalCloud WAES、GlobalCloud GPC、GlobalCloud Studio、GlobalCoud GPCF、GlobalCloud XWAIL、GlobalCloud GFIS、GlobalCloud MMC、GlobalCloud KDS、GlobalCloud XiaoG、GlobalCloud PVAOS、GlobalCloud SOP、GlobalCloud PKC、GlobalCloud XGD。

## Task Anchors

- AAAS-WAES-BINDING-PRECHECK-001
- XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001
- SOP-SCENARIO-OWNER-REVIEW-001
- WAS-XWAIL-ONTOLOGY-MAPPING-001
- KDS-BRAIN-REPORT-HOLD-REVIEW-001
- WAES-LINT-RUNTIME-001
- GFIS-REAL-SOR-001
- GPC-EXTERNAL-RUNTIME-EVIDENCE-001
- BRAIN-HUMAN-REVIEW-DECISION-001
- GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001
- globalcloud-project-group-dev-task-queue-20260626.md

历史 delegated wrapper 锚点保留：

- 5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要
- 5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要
- 5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要

## GFIS Boundary

GFIS 真实业务 lane 仍保持 `repair_required`。当前真实计数：

```text
real_source_records=0
valid_source_records=0
formal_confirmation_files=0
runtime_primary_key_ready=0
review_queue=0
runtime_intake=0
waes_review=0
verified=0
```

未取得真实 source-of-record 或等效正式确认前，不得以治理文档、测试数据、mock、demo、validator 存在替代真实业务闭环。
