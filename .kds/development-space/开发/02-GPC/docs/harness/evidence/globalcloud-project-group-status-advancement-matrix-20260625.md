---
doc_id: GPCF-DOC-PROJECT-GROUP-STATUS-ADVANCEMENT-MATRIX-20260625
title: GlobalCloud 项目群状态推进判定矩阵 2026-06-25
project: GPC
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: docs
status: controlled
version: v1.0
owner: GPC
kds_space: 开发
kds_path: 开发/02-GPC/docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群状态推进判定矩阵 2026-06-25

## 1. 定位

本文补齐 `GPCF-STATUS-ADVANCEMENT-001`，用于把项目群状态从 `candidate`、`partial_verified`、`repair_required`、`baseline_controlled` 推进到 `ready_for_review` 的判定条件显式化。

本文只定义状态推进条件和降级规则，不执行项目任务，不升级 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

当前状态推进矩阵与以下两份证据保持一致：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

## 2. 控制结论

```text
status_advancement_matrix = controlled
project_status_rule_count = 17
ready_for_review_requires_gate = true
accepted_requires_human_confirmation = true
integrated_requires_human_confirmation = true
customer_accepted_requires_human_confirmation = true
live_project_group_git_gate = blocked
project_group_current_state_baseline_refresh_20260626 = controlled
development_queue_ready = true
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 3. 项目状态推进矩阵

| # | 项目 | 当前状态 | 目标状态 | 推进任务 | 必须证据 | 必须门禁 | 阻塞条件 | 降级/回滚 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GlobalCloud AAAS | `ready_for_review / local_dev_boundary / integration_precheck_candidate / wrapper_review_required` | `integration_precheck_candidate` | `AAAS-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001`、`GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`AAAS-WAES-BINDING-PRECHECK-001` | `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.1 AAAS delegated wrapper 单仓核对卡` / `5.6.1 AAAS delegated wrapper 确认后状态传导摘要`、`aaas-waes-binding-precheck-20260625.md`、AaaS runtime evidence | pre-wave1 review authorization gate、AaaS wrapper review gate、AaaS service runtime gate、WAES binding precheck gate、contract precheck gate | delegated wrapper replay 未确认、WAES 未发布/未授权、真实计费/订阅缺失 | 失败保持 local dev boundary / wrapper_review_required | 真实订阅/计费/生产 SLA 前需要 | 不声明真实计费、客户订阅、商业交付 |
| 2 | GlobalCloud Brain | `ready_for_human_review / authorization_boundary` | `accepted_candidate_or_rework` | `BRAIN-HUMAN-REVIEW-DECISION-001` | `brain-human-review-decision-*.md`、Brain handoff evidence | Brain review handoff gate、human review gate | 未获得人工确认、KDS 输入冲突 | 未确认保持 authorization_boundary | 是，accepted/integrated 前必须 | 不声明 accepted、integrated、production_ready |
| 3 | WAS世界资产体系 | `semantic_foundation_candidate / not_accepted / xwail_mapping_candidate` | `xwail_mapping_candidate` | `WAS-XWAIL-ONTOLOGY-MAPPING-001` | `was-xwail-ontology-mapping-20260625.md` | WAS semantic gate、Ontology mapping gate、XWAIL validator precheck、XAP check gate、mapping evidence gate | 主术语变更未确认、语义和事实边界混淆 | 冲突时保持 semantic candidate | 主术语/总体架构变更需要 | 不声明真实业务事实、KDS 事实主存、WAES 发布、AaaS 绑定 |
| 4 | GlobalCloud XiaoC | `baseline_controlled / environment_blocked` | `task_pack_ready` | `XIAOC-MODEL-ROUTING-DRYRUN-001` | `xiaoc-model-routing-dryrun-environment-blocked-20260625.md` | XiaoC dry-run environment gate、`validate_xiaoc_model_routing_dryrun_environment_blocked.py`、GPCF task-pack gate、Loop document gate | Node engine 要求 `^22.0.0`，当前 `v26.0.0`；真实模型调用、Wrangler/部署未授权 | 切换 Node 22 后复跑；失败保持 environment_blocked 或降级 repair_required | 真实模型、Wrangler、Docker 或部署前需要 | 不声明 XiaoC dry-run 通过，不声明真实部署，不声明生产模型路由可用，不声明 accepted/integrated/customer accepted |
| 5 | GlobalCloud WAES | `repair_required / authorization_required` | `ready_for_review_candidate` | `WAES-LINT-RUNTIME-001` | `waes-lint-runtime-repair-*.md` | WAES quality gate、GPCF register gate | lint/runtime 未修复、源码修复未授权 | 失败保持 repair_required | 是，源码修复需授权 | 不声明治理运行闭环、发布、权限变更 |
| 6 | GlobalCloud GPC | `partial_verified / external_runtime_evidence_required` | `ready_for_review_candidate` | `GPC-EXTERNAL-RUNTIME-EVIDENCE-001` | `gpc-external-runtime-evidence-*.md` | GPC external runtime gate、browser/e2e gate | 生产确认、外部联调、GCFIS runtime 缺失 | 失败保持 external_runtime_evidence_required | 外部联调/生产确认需要 | 不声明外部联调、真实交付、客户验收 |
| 7 | GlobalCloud Studio | `release_boundary_recheck_passed / local_release_review_boundary` | `release_authorization_review_required` | `STUDIO-WORKFLOW-PERMISSIONS-001` | `studio-workflow-permissions-recheck-20260625.md`、Studio evidence-index 3 行修正、test/build/harness evidence | Studio workflow boundary gate、GPCF release governance gate、`validate_studio_workflow_permissions_recheck.py` | release/GitHub 写入、部署、提交和推送未授权 | 失败保持 review_required_before_commit 或降级 repair_required | 触发 release/GitHub 写入/部署/提交/推送前需要 | 不声明 release、部署、GitHub release 写入 |
| 8 | GlobalCoud GPCF | `controlled / git_clean_blocked / live_git_blocked_by_sensitive_path_review / authorization_routing_ready / dirty_disposition_queue_ready / live_status_snapshot_controlled / loop_gate_readiness_pass / first_execution_authorization_request_prepared / execution_authorization_receipt_template_ready / execution_authorization_receipt_ledger_ready / authorization_pre_execution_command_pack_ready / authorization_pre_execution_environment_ready / ready_for_review_advancement_queue_ready / pre_wave1_review_authorization_ready / next_stage_authorization_decision_board_prepared / next_stage_authorization_receipt_example_pack_ready / next_stage_authorization_receipt_recording_procedure_ready / next_stage_authorization_human_fill_request_ready / next_stage_authorization_chain_consistency_audit_ready / next_stage_authorization_package_ready / next_stage_authorization_chain_loop_round_ready` | `ready_for_review_advancement_queue_ready` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-HUMAN-FILL-REQUEST-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-CONSISTENCY-AUDIT-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-PACKAGE-20260627-001`、`GPCF-NEXT-STAGE-AUTHORIZATION-CHAIN-LOOP-ROUND-20260627-001`、`GPCF-AUTHORIZATION-PACKAGE-ROUTING-001`、`GPCF-DIRTY-DISPOSITION-QUEUE-001`、`GPCF-LIVE-STATUS-SNAPSHOT-20260626-001`、`GPCF-LOOP-GATE-READINESS-PASS-20260626-001`、`GPCF-FIRST-EXECUTION-AUTHORIZATION-REQUEST-20260626-001`、`GPCF-EXECUTION-AUTHORIZATION-RECEIPT-TEMPLATE-20260626-001`、`GPCF-EXECUTION-AUTHORIZATION-RECEIPT-LEDGER-20260626-001`、`GPCF-AUTHORIZATION-PRE-EXECUTION-COMMAND-PACK-20260626-001`、`GPCF-AUTHORIZATION-PRE-EXECUTION-ENVIRONMENT-READINESS-20260626-001`、`GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001` | `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md`、`globalcloud-project-group-next-stage-authorization-decision-board-20260626.md`、`globalcloud-project-group-next-stage-authorization-receipt-example-pack-20260627.md`、`globalcloud-project-group-next-stage-authorization-receipt-recording-procedure-20260627.md`、`globalcloud-project-group-next-stage-authorization-human-fill-request-20260627.md`、`globalcloud-project-group-next-stage-authorization-chain-consistency-audit-20260627.md`、`globalcloud-project-group-next-stage-authorization-package-20260627.md`、`loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md`、`globalcloud-project-group-authorization-routing-20260625.md`、`globalcloud-project-group-dirty-disposition-queue-20260625.md`、`globalcloud-project-group-live-status-snapshot-20260626.md`、`globalcloud-project-group-loop-gate-readiness-pass-20260626.md`、`globalcloud-project-group-first-execution-authorization-request-20260626.md`、`globalcloud-project-group-execution-authorization-receipt-template-20260626.md`、`globalcloud-project-group-execution-authorization-receipt-ledger-20260626.md`、`project_group_execution_authorization_receipt_ledger_20260626 = controlled`、`globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md`、`project_group_authorization_pre_execution_command_pack_20260626 = controlled`、`globalcloud-project-group-authorization-pre-execution-environment-readiness-20260626.md`、`project_group_authorization_pre_execution_environment_readiness_20260626 = controlled`、`globalcloud-project-group-ready-for-review-advancement-queue-20260626.md`、`project_group_ready_for_review_advancement_queue_20260626 = controlled` | pre-wave1 review authorization gate、next-stage human fill request gate、next-stage chain consistency audit gate、next-stage authorization package gate、next-stage chain loop-round gate、authorization routing gate、dirty disposition queue gate、live status snapshot gate、loop gate readiness pass gate、first execution authorization request gate、execution authorization receipt template gate、execution authorization receipt ledger gate、`validate_project_group_execution_authorization_receipt_ledger_20260626.py`、authorization pre-execution command pack gate、`validate_project_group_authorization_pre_execution_command_pack_20260626.py`、authorization pre-execution environment readiness gate、`validate_project_group_authorization_pre_execution_environment_readiness_20260626.py`、ready-for-review advancement queue gate、`validate_project_group_ready_for_review_advancement_queue_20260626.py`、Git clean gate、Loop document gate | 当前 live Git gate 已因 `GlobalCloud KDS/.env.production.example` sensitive_path 和当前 7 仓总 dirty 事实收紧为 blocked；其中 `WAS世界资产体系/.DS_Store` 沿 noise cleanup 路径单独治理，其余 `KDS/AAAS/XWAIL/GPCF/GFIS/SOP` 6 仓为当前 review 边界；`pre-wave1` 未确认、next-stage human fill request 仍未转成真实回执、next-stage package 与 loop-round 只证明链路已归档、owner decision 未完成、noise cleanup 未授权、命令包未获授权运行、状态升级未获人工确认 | readiness 再次失败时降回 partial/rework；KDS sensitive_path 未归类前保持 live blocked；`pre-wave1` 未确认前保持 Wave 1 blocked；队列缺项目/任务/门禁/阻塞边界时降回 partial/rework；未确认保持 queue_ready | 是，实际回执、运行命令包、review/stage/commit/push/delete/owner decision、accepted/integrated/customer accepted 前 | 不声明可提交、可推送、Git 全量 clean、任何授权已发生、任何命令包已执行、任何项目已自动升级到 ready_for_review、Wave 1 已授权、已验收 |
| 9 | GlobalCloud XWAIL | `ready_for_review / local_dev_boundary / integration_precheck_candidate / wrapper_review_required` | `integration_precheck_candidate` | `XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001`、`GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001` | `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.2 XWAIL delegated wrapper 单仓核对卡` / `5.6.2 XWAIL delegated wrapper 确认后状态传导摘要`、`xwail-waes-aaas-contract-precheck-20260625.md` | pre-wave1 review authorization gate、XWAIL wrapper review gate、XWAIL validator gate、contract precheck gate | WAES 未修复/未发布、AaaS 未绑定、delegated wrapper replay 未确认 | 失败保持 local dev boundary / wrapper_review_required | 否，除非改变核心契约 | 不声明完整工具链、WAES 发布、AaaS 绑定 |
| 10 | GlobalCloud GFIS | `partial_verified / repair_required` | `pending_business_verification_candidate` | `GFIS-REAL-SOR-001` | `gfis-real-source-record-intake-*.md` | GFIS source-record gate、WAES review gate | 缺真实 source-of-record 或 owner 确认 | 失败保持 repair_required | 是，需要业务 owner 或正式回执 | 不声明真实 SOP E2E、生产写入、客户验收 |
| 11 | GlobalCloud MMC | `task_pack_ready / local_document_smoke_boundary` | `task_pack_ready` | `MMC-GOVERNANCE-TEMPLATE-SMOKE-001` | `mmc-governance-template-smoke-20260625.md` | MMC smoke gate、`validate_mmc_governance_template_smoke.py`、GPCF task-pack gate、Loop document gate | runtime pytest、contract test、控制面运行证据和下游接入未验证 | runtime 或继承关系失败时降回 baseline_controlled | 改治理模板基线、执行服务重启或下游写入前需要 | 不声明 MMC runtime 已通过，不声明下游项目已接入 MMC 模板，不声明 accepted/integrated/customer accepted |
| 12 | GlobalCloud KDS | `owner_review_required / kds_report_hold_controlled / git_sensitive_review_boundary` | `owner_decision_required_or_ready_for_review` | `AUTH-KDS-SCHEME-REVIEW-20260626`、`GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`KDS-BRAIN-REPORT-HOLD-REVIEW-001` | `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要`、`kds-brain-report-hold-review-20260625.md`、资金追踪报告、2026-06-25 sync-run evidence | pre-wave1 review authorization gate、KDS evidence gate、KDS TOKEN gate、owner review gate、`validate_kds_brain_report_hold_review.py`、Loop document gate | 资金追踪报告未确认、sync-run 接收/归档未确认、真实 API 同步未授权，且 `.env.production.example` sensitive_path 仍待归类 | 未确认保持 owner_review_required；owner 不通过则保持 hold_business_report；sensitive_path 未归类前不得进入 Git 动作 | 是，业务报告纳入、sync-run 接收/归档、KDS API 同步、Brain/WAES 消费前需要 | 不声明真实 KDS API 同步、生产索引、Brain/WAES 已消费 |
| 13 | GlobalCloud XiaoG | `task_pack_ready / authorization_pack_ready` | `live_api_human_authorization_required` | `XIAOG-LIVE-API-AUTH-PACK-001` | `xiaog-live-api-auth-pack-20260625.md`、XiaoG L4 readonly/audit/notification mock evidence | XiaoG authorization pack gate、`validate_xiaog_live_api_auth_pack.py`、Loop document gate | live API、设备验证、真实通知、WAES 写入、Docker、部署和 TOKEN 访问未授权 | 未授权保持 authorization_pack_ready；validator 失败降级 baseline_controlled | 是，live API/设备验证/真实外部写入需要 | 不声明设备 OTA、真实外部 API、真实通知、WAES 写入 |
| 14 | GlobalCloud PVAOS | `ready_for_review / local_release_gate_boundary / review_candidate` | `review_candidate` | `PVAOS-RELEASE-REVIEW-001` | `pvaos-release-review-20260625.md` | PVAOS local release gate、review package gate、release review gate | 远程 CI/PR/merge/发布未授权 | 未授权保持 local release boundary | 是，远程 CI/PR/merge/发布前 | 不声明远程 CI、PR、merge、生产发布 |
| 15 | GlobalCloud SOP | `owner_review_required / scenario_candidate_controlled / wrapper_review_required` | `owner_decision_required` | `AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627`、`GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`、`SOP-SCENARIO-OWNER-REVIEW-001` | `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.3 SOP delegated wrapper 单仓核对卡` / `5.6.3 SOP delegated wrapper 确认后状态传导摘要`、`sop-scenario-owner-review-20260625.md`、SOP asset/smoke evidence、武汉城市圈场景 draft/candidate | pre-wave1 review authorization gate、SOP wrapper review gate、SOP owner review gate、`validate_sop_scenario_owner_review.py`、dirty classification gate、Loop document gate | scenario owner 未确认；KDS 事实入库、对外发布、删除噪声未授权；delegated wrapper replay 未确认 | 未确认保持 owner_review_required / wrapper_review_required；owner 不通过则降回 hold_scenario_output | 是，需要 scenario owner 确认 | 不声明场景方案已确认、已交付、KDS 事实入库 |
| 16 | GlobalCloud PKC | `task_pack_ready / local_dev_dryrun_boundary` | `task_pack_ready` | `PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001` | `pkc-kds-brain-workflow-dryrun-20260625.md` | PKC workflow gate、`validate_pkc_kds_brain_workflow_dryrun.py`、KDS/Brain dependency gate、Loop document gate | 真实 KDS/Brain 集成、真实个人数据、外部 API 写入未授权或未验证 | 命令失败保持 baseline_controlled 或降级 repair_required | 涉及真实个人数据、外部 API 或生产写入前需要 | 不声明端到端用户闭环，不声明真实 KDS/Brain 集成，不声明 accepted/integrated/customer accepted |
| 17 | GlobalCloud XGD | `task_pack_ready / local_dev_smoke_boundary` | `task_pack_ready` | `XGD-TICK-BRAIN-SMOKE-001` | `xgd-tick-brain-smoke-20260625.md` | XGD harness gate、`validate_xgd_tick_brain_smoke.py`、Brain UI smoke gate、Loop document gate | 长程 Agent 真实外部动作、生产运行、真实 KDS/Brain/XiaoC/WAES 集成未授权或未验证 | 命令失败保持 baseline_controlled 或降级 repair_required | 外部动作、生产运行或真实写入前需要 | 不声明长程 Agent 生产可用，不声明真实外部动作，不声明 accepted/integrated/customer accepted |

## 4. 全局升级规则

| 目标状态 | 必须满足 |
|---|---|
| `task_pack_ready` | 有任务包、命令、预期证据、门禁、回滚边界和禁止声明 |
| `integration_precheck_candidate` | 上游依赖边未阻塞，且下游 precheck evidence 通过 |
| `ready_for_review_candidate` | 项目关键命令和 GPCF register gate 均通过，且禁止声明保留 |
| `ready_for_review` | 项目 evidence、依赖矩阵、核心台账、Loop 文档门禁均通过 |
| `accepted` | 必须由用户明确确认 |
| `integrated` | 必须由用户明确确认，且依赖边均无阻塞 |
| `customer_accepted` | 必须有客户验收人、验收场景、验收结果和签收/退回证据 |

`GPCF-READY-FOR-REVIEW-ADVANCEMENT-QUEUE-20260626-001` 只建立 17 项目推进队列和优先级，当前结论为 `project_group_ready_for_review_advancement_queue_20260626 = controlled`，状态候选为 `ready_for_review_advancement_queue_ready`，证据文件为 `globalcloud-project-group-ready-for-review-advancement-queue-20260626.md`，校验器为 `validate_project_group_ready_for_review_advancement_queue_20260626.py`，且必须保持 `auto_ready_for_review_upgrade=false`。

在当前状态刷新或开发态入口变化前，不得把任一项目从 `candidate`、`partial_verified`、`repair_required` 直接解释为可自动进入 `ready_for_review`。

## 5. 禁止升级条件

- 只有方案、README、mock、fixture、synthetic/dev-only 数据；
- 只有本地截图或单一构建通过；
- 依赖边仍为 `blocked`、`repair_required` 或 `authorization_boundary`；
- Git 门禁存在敏感路径、behind、diff check 失败或未确认 dirty 变更；
- 需要真实业务 owner、scenario owner、客户、外部系统或生产环境确认但未获得确认；
- 需要 stage、commit、push、deploy、release、merge、生产写入或权限变更但未授权。
