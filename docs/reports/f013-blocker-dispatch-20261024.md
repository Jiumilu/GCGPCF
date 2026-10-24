---
doc_id: GPCF-DOC-B32788D46B
title: "F-013 剩余阻塞项派单表（2026-10-24 19:05）"
project: KDS
related_projects: [GPC, WAME, KDS, Brain, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/f013-blocker-dispatch-20261024.md
source_path: docs/reports/f013-blocker-dispatch-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-013 剩余阻塞项派单表（2026-10-24 19:05）

- 背景：F-013（知识资产模型系统）是当前**唯一 blocked Feature**。原有 15 条 blocker，本轮 KDS 脏树收敛后剩 **14 条**。
- 用途：按归属项目派单；每项给出「解除判据」与「当前状态（技术/治理）」。
- 数据来源：`features/active/F-013-*/feature.yaml`、`features/active/F-013-*/evidence/*`、`docs/harness/evidence/active-feature-blockers-20261024.md`。

## 1. 已解除（留档）

| # | blocker | 解除依据 |
|---|---|---|
| 0 | `kds_p1_apply_blocked_by_dirty_worktree` | KDS 脏树 4266 → **1**（仅实时日志）；完整快照分支 `wip/kds-restructure-snapshot-full-20261024`（5ce9f69）；见 `collab-completion-20261024.md §9` |

## 2. 仍成立（14 条，按归属分组）

### 2.1 GPCF 自身（1 条）

| # | blocker | 解除判据 | 状态 |
|---|---|---|---|
| 1 | `gpcf_a10r27_current_truth_4file_delta_pending_independent_review_and_separate_commit_push_disposition` | 对 A10R27 的 4 文件 delta 做独立复核并单独提交/推送处置 | 待办（GPCF） |

### 2.2 KDS（4 条）

| # | blocker | 解除判据 | 状态 |
|---|---|---|---|
| 2 | `kds_green_supply_chain_role_view_local_commit_pending_separate_human_authorization` | 绿色供应链角色视图本地提交需单独人工授权 | 待人工 |
| 6 | `kds_release0_runtime_activation_independently_verified_local_gbrain_missing_knowledge_intake_audit_relation` | release0 运行激活已独立验证，但本地 GBrain 缺知识摄取审计关系 | 技术部分达成 |
| 7 | `kds_local_gbrain_schema_inventory_and_separate_migration_fixture_authorization_required` | 本地 GBrain schema 盘点 + 迁移 fixture 需单独授权 | 待人工 |
| 9 | `kds_stage_b_read_admission_technical_verified_governance_blocked` | Stage B 只读准入**技术已验证**，卡治理 | 治理待决 |

### 2.3 Brain（2 条）

| # | blocker | 解除判据 | 状态 |
|---|---|---|---|
| 3 | `brain_browser_r2_postpush_revalidated_chat_send_not_executed_mobile_ui_rework_required` | 浏览器 R2 推送后复验；chat 发送未执行；移动端 UI 需返工 | 待 Brain 属主 |
| 4 | `brain_authenticated_readonly_e2e_deferred_pending_a10_control` | 带认证的只读 E2E 被推迟，待 A10 控制项 | 待 A10 |

### 2.4 Studio（4 条）

| # | blocker | 解除判据 | 状态 |
|---|---|---|---|
| 5 | `studio_release0_external_daily_sync_post_sync_governance_disposition_pending` | release0 外部日同步后的治理处置待定 | 待 Studio 属主 |
| 8 | `studio_gehua_authoritative_project_session_target_fixture_lifecycle_not_executed` | 葛化权威项目会话目标 fixture 生命周期未执行 | 待 Studio 属主 |
| 10 | `studio_intake_phase1_authorized_phase2_blocked_by_mmc_prepare_retry_policy_review` | Phase1 已授权；Phase2 被 MMC prepare/retry 策略评审阻塞 | 待 MMC 评审 |
| 11 | `studio_a6_external_daily_sync_commit_push_requires_governance_disposition` | A6 外部日同步的提交/推送需治理处置 | 待治理 |

### 2.5 MMC（2 条）+ 1 条跨仓

| # | blocker | 解除判据 | 状态 |
|---|---|---|---|
| 12 | `unexpected_external_kds_local_mirror_write_requires_review` | 外部对 KDS 本地镜像的写入需复核 | 待复核 |
| 13 | `mmc_a9_bounded_read_subset_technical_verified_global_policy_not_narrowed` | A9 有界只读子集**技术已验证**，全局策略未收窄 | 治理待决 |
| 14 | `mmc_delegation_and_human_confirmation_pending` | 委派与人工确认流程待定 | 待人工 |

## 3. 派单汇总

| 归属 | 条数 | 建议动作 |
|---|---:|---|
| GPCF | 1 | 我可自行完成（A10R27 四文件 delta 独立复核 + 单独提交） |
| KDS | 4 | 属主：2 条需专项授权、1 条治理裁定、1 条补审计关系 |
| Brain | 2 | 属主：移动端 UI 返工 + A10 控制放开 |
| Studio | 4 | 属主：治理处置 + fixture 生命周期 + A11/MMC 策略 |
| MMC | 2 | 治理：收窄全局策略 + 委派人工确认 |
| 跨仓复核 | 1 | GPCF/属主共同复核 KDS 镜像写入 |

## 4. 结论

F-013 现在不是"一个技术问题"，而是**跨 5 个项目的 14 项治理/授权事项**的聚合。
若要解除 F-013，最小路径是：GPCF 先清掉自己那 1 条（我可做），其余按上表派单。
不建议把 F-013 当作单一 Feature 追赶——它更像一个治理积压台账，可考虑在 P19 组合决策里重新界定其范围。
