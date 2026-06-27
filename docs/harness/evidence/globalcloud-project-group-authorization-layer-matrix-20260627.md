---
doc_id: GPCF-DOC-AUTHORIZATION-LAYER-MATRIX-20260627
title: GlobalCloud 项目群开发过程授权层级矩阵 2026-06-27
project: GFIS
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: docs
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md
source_path: docs/harness/evidence/globalcloud-project-group-authorization-layer-matrix-20260627.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群开发过程授权层级矩阵 2026-06-27

## 授权边界

- 输入：用户要求“按建议执行”，承接授权堵点评估结论。
- 目标：将开发过程授权拆成 `DEV-AUTH`、`REVIEW-AUTH`、`RUNTIME-AUTH`、`ACCEPTANCE-AUTH` 四层，并把当前第一优先 `REVIEW-AUTH` 入口落到 Pre-Wave1 六仓 review 边界桥接包。
- 允许动作：生成授权层级矩阵、生成 Loop round、生成只读 validator、更新开发态任务队列、运行只读门禁。
- 禁止动作：自动 review、stage、commit、push、merge、deploy、release、删除文件、生产写入、schema migrate、真实外部 API 写入、真实 KDS API 双向同步、标记 accepted/integrated/production_ready/customer_accepted。
- 判定边界：本文只把授权入口结构化，不代表用户已授予任何 review/stage/commit/push/runtime/acceptance 权限。

当前授权层级矩阵与以下两份证据保持一致：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

## 当前门禁快照

| 门禁 | 当前结果 | 授权含义 |
|---|---|---|
| 17 仓 Git gate | `blocked`；10/17 clean；dirty_repos=`GlobalCloud AAAS`,`WAS世界资产体系`,`GlobalCoud GPCF`,`GlobalCloud XWAIL`,`GlobalCloud GFIS`,`GlobalCloud KDS`,`GlobalCloud SOP`；`GlobalCloud KDS` 命中 sensitive_path=`.env.production.example`；17/17 diff-check pass | 本地开发可继续，但 review/stage/commit/push 必须先解除 KDS sensitive_path 硬阻塞，并完成 AAAS/XWAIL/SOP delegated wrapper review replay；当前这 6 仓 review 边界已进一步收口为 `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`。`WAS世界资产体系/.DS_Store` 仍按 noise cleanup 单独治理，不并入 Pre-Wave1 六仓 review 边界；基线见 `globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md` 和 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` |
| GPCF worktree review packages | `pass`；review_package_count=7 | 已具备 REVIEW-AUTH 的逐包确认入口 |
| SOP/PKC generated/output/dist isolation | `pass`；候选数 0 | 不再作为当前 REVIEW-AUTH 堵点 |
| KDS token / pollution / conflict / Loop document gate | 最近均 pass | 文档/KDS 本地治理不是当前授权主堵点 |
| operational gates | `blocked`，dependency/customer/quality 仍有 rework/blocker | 阻塞 RUNTIME-AUTH 与 ACCEPTANCE-AUTH，不阻塞 DEV-AUTH |

## 四层授权包

| 授权包 | 状态 | 允许范围 | 当前入口 | 默认动作状态 | 禁止传导 |
|---|---|---|---|---|---|
| `DEV-AUTH-20260627` | `active_for_local_dev` | 本地开发、mock、dry-run、fixture、validator、文档 evidence、本地测试、只读 Git/文档门禁 | 项目群开发态 P0 队列 | `local_dev_allowed=true` | 不传导到 stage/commit/push/runtime/accepted |
| `REVIEW-AUTH-20260627` | `prepared_pending_confirmation` | 人工 review、逐包确认、提交候选判断，以及 next-stage receipt 字段确认入口 | `REVIEW-AUTH-GPCF-WORKTREE-20260627`、`GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-DECISION-BOARD-20260626-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001` | `review_allowed=false stage_allowed=false commit_allowed=false push_allowed=false delete_allowed=false` | 单包确认不得传导到其它包或 Git push；Pre-Wave1 未确认前不得进入 Wave 1 执行回执；next-stage human fill request、authorization package 和 loop-round 不得直接写成真实授权 |
| `RUNTIME-AUTH-20260627` | `blocked_pending_business_input` | GFIS/KDS/WAES 真实运行层写入、schema、runtime API、真实 KDS API | GFIS true source-of-record、runtime primary key、review queue、runtime intake、WAES review | `runtime_write_allowed=false schema_migrate_allowed=false real_api_write_allowed=false` | 不得由 DEV/REVIEW 授权自动传导 |
| `ACCEPTANCE-AUTH-20260627` | `blocked_pending_human_acceptance` | accepted、integrated、production_ready、customer_accepted、客户/UAT/WAES/Harness 裁决 | WAES/Harness/owner/customer confirmation | `accepted_allowed=false integrated_allowed=false production_ready_allowed=false customer_accepted_allowed=false` | 不得由测试通过、review 完成或 runtime precheck 自动传导 |

## REVIEW-AUTH 入口

| review_auth_id | 范围 | 进入条件 | 当前状态 | 执行前必须复核 | 允许动作 |
|---|---|---|---|---|---|
| `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | 当前 6 仓 review 边界：`KDS/AAAS/XWAIL/GPCF/GFIS/SOP` | `validate_project_group_pre_wave1_review_authorization_request_20260627.py` pass；post-scheme request/ledger/command pack 均 pass；Loop document gate pass | `pre_wave1_review_authorization_ready / pending_confirmation` | `validate_project_group_pre_wave1_review_authorization_request_20260627.py`、post-scheme 3 个 validator、Loop document gate、Git clean gate | 仅允许 6 仓 review 边界的人审授权和结论登记；不允许进入任何 Wave 1 pack 的执行回执 |
| `GPCF-NEXT-STAGE-AUTHORIZATION-DECISION-BOARD-20260626-001` | 当前 7 项 next-stage 决策项：`1` 项 `WAS .DS_Store` noise cleanup + `6` 项 Pre-Wave1 review 边界对应的 receipt 录入链 | `validate_project_group_next_stage_authorization_decision_board_20260626.py` pass；receipt example pack / recording procedure / human fill request / chain consistency audit 均 pass；Loop document gate pass | `authorization_decision_board_prepared / pending_confirmation` | `validate_project_group_next_stage_authorization_decision_board_20260626.py`、`validate_project_group_next_stage_authorization_receipt_example_pack_20260627.py`、`validate_project_group_next_stage_authorization_receipt_recording_procedure_20260627.py`、`validate_project_group_next_stage_authorization_human_fill_request_20260627.py`、`validate_project_group_next_stage_authorization_chain_consistency_audit_20260627.py`、Loop document gate、Git clean gate | 仅允许 next-stage 人工确认、receipt 字段准备和结论登记；不允许直接写入真实授权、不允许进入 Wave 1 执行回执 |
| `GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001` | 当前 7 项 next-stage auth_id 的聚合授权包：固定 `1/6` 总账分流、route_layer、receipt_source 和默认禁止边界 | `validate_project_group_next_stage_authorization_package_20260627.py` pass；decision board / example pack / recording procedure / human fill request / chain consistency audit 均 pass；Loop document gate pass | `next_stage_authorization_package_ready / pending_confirmation` | `validate_project_group_next_stage_authorization_package_20260627.py`、`validate_project_group_next_stage_authorization_chain_consistency_audit_20260627.py`、`validate_project_group_authorization_routing.py`、Loop document gate、Git clean gate | 仅允许聚合授权包的人工复核和结论登记；不允许直接写入真实授权、不允许绕过目标总账、不允许进入 Wave 1 执行回执 |
| `GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001` | 当前 next-stage 授权链的 loop-round 归档：固定从人工确认入口到目标总账的节点顺序与默认边界 | `validate_project_group_next_stage_authorization_chain_loop_round_20260627.py` pass；authorization package / chain consistency audit 均 pass；Loop document gate pass | `next_stage_authorization_chain_loop_round_ready / pending_confirmation` | `validate_project_group_next_stage_authorization_chain_loop_round_20260627.py`、`validate_project_group_next_stage_authorization_package_20260627.py`、`validate_project_group_next_stage_authorization_chain_consistency_audit_20260627.py`、Loop document gate、Git clean gate | 仅允许 loop-round 归档的人审确认；不允许生成真实授权回执、不允许进入 Wave 1 执行回执 |

前置证据补充：

- `docs/harness/evidence/globalcloud-project-group-next-stage-authorization-decision-board-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md`
| `REVIEW-AUTH-GPCF-WORKTREE-20260627` | GPCF 7 个 review 包：RP1 KDS mirror、RP2 mirror ledger、RP3 status registers、RP4 docs indexes、RP5 Agent-Reach evidence、RP6 Agent-Reach tooling/fixture、RP7 project-group P0 evidence | `validate_project_group_gpcf_worktree_review_packages_20260627.py` pass；Loop document gate pass；17 仓 Git gate 解除 `GlobalCloud KDS` sensitive_path 硬阻塞，并完成 AAAS/XWAIL/SOP delegated wrapper replay（见 `globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md`）后方可进入实际 review | `blocked_by_git_gate_and_pending_user_confirmation` | Git gate、diff-check、KDS conflict guard、Loop document gate、对应专项 validator | 仅允许人工阅读和确认 review 结论；不允许 stage/commit/push/delete |

## 授权口令模板

### REVIEW-AUTH 最小口令

```text
授权 REVIEW-AUTH-GPCF-WORKTREE-20260627：只允许对 GPCF 7 个 review 包进行人工 review 和结论登记；不允许 stage、commit、push、delete、deploy、生产写入、schema migrate、真实 API 写入或状态提升。
```

### REVIEW + STAGE 另行口令

```text
授权 REVIEW-AUTH-GPCF-WORKTREE-20260627 的 <包ID> 进入 stage 候选：仅限 <文件清单>；执行前复跑 Git gate、diff-check、KDS conflict、Loop document gate；不允许 commit/push/delete/生产写入或状态提升。
```

### PRE-WAVE1 最小口令

```text
授权 GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627 的 6 仓 review 边界：只允许人工 review 和结论登记；不允许 stage、commit、push、delete、cleanup、deploy、真实 KDS API 同步、真实外部 API 写入或状态提升。
```

### RUNTIME-AUTH 另行口令

```text
授权 RUNTIME-AUTH-20260627 的 <对象/接口/目录>：仅限 <具体动作>；必须包含真实 source-of-record、回滚方案、审计证据、时间窗和负责人；不自动传导 accepted/integrated/production_ready。
```

### ACCEPTANCE-AUTH 另行口令

```text
授权 ACCEPTANCE-AUTH-20260627 的 <项目/状态>：基于 <证据包> 由 <owner/WAES/Harness/customer> 人工确认；只提升指定状态，不传导生产写入或其它项目。
```

## 状态声明

- authorization_layer_matrix = prepared
- authorization_layer_count = 4
- project_group_current_state_baseline_refresh_20260626 = controlled
- development_queue_ready = true
- git_gate_current = blocked
- dirty_repos_current = GlobalCloud AAAS, WAS世界资产体系, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP
- sensitive_repos_current = GlobalCloud KDS(.env.production.example)
- dev_auth_status = active_for_local_dev
- review_auth_status = prepared_pending_confirmation
- pre_wave1_review_authorization_status = prepared_pending_confirmation
- next_stage_authorization_package_status = prepared_pending_confirmation
- next_stage_authorization_chain_loop_round_status = prepared_pending_confirmation
- runtime_auth_status = blocked_pending_business_input
- acceptance_auth_status = blocked_pending_human_acceptance
- review_auth_first_entry = GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001
- review_auth_second_entry = GPCF-NEXT-STAGE-AUTHORIZATION-DECISION-BOARD-20260626-001
- review_auth_third_entry = GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001
- review_auth_fourth_entry = GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001
- review_allowed = false
- stage_allowed = false
- commit_allowed = false
- push_allowed = false
- delete_allowed = false
- runtime_write_allowed = false
- schema_migrate_allowed = false
- real_api_write_allowed = false
- accepted_allowed = false
- integrated_allowed = false
- production_ready_allowed = false
- customer_accepted_allowed = false
- accepted = false
- integrated = false
- production_ready = false
- customer_accepted = false
