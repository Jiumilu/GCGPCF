---
doc_id: GPCF-DOC-DEV-TASK-QUEUE-20260626
title: GlobalCloud 项目群开发态任务队列
project: GFIS
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: docs
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群开发态任务队列

## 控制结论

```text
development_queue_ready = true
project_count = 17
trigger_layer_binding_count = 17
dependency_edge_binding_count = 17
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 队列规则

- 每个项目先进入开发态，不进入验收态。
- 每仓第一任务均为 dirty 分类与本地验证，不提交、不推送。
- 若触发测试失败、敏感路径、生产写入、schema migrate、部署或业务事实冲突，立即暂停该仓。
- 本队列保留 2026-06-26 初始开发态任务队列；当前执行判断必须以后续 2026-06-28 live override 为准。当前项目群 Git gate 为 `partial`，dirty 仓为 `GlobalCoud GPCF`、`GlobalCloud GFIS`、`GlobalCloud SOP`，KDS 已从当前 dirty/sensitive 阻塞源移除；执行任何项目任务前仍必须复跑 17 仓 Git gate，以当次输出为准。
- P0-A dirty 分类已生成：`docs/harness/evidence/globalcloud-project-group-dev-p0-dirty-classification-20260626.md`。
- P0-B 项目级最小验证已生成：`docs/harness/evidence/globalcloud-project-group-dev-p0-project-validation-20260626.md`。

## 开发态任务级 Trigger Layer / Dependency Edge 绑定

| 项目 | trigger_layer | dependency_edge | authoritative_entry | 当前开发态入口含义 |
|---|---|---|---|---|
| GlobalCloud AAAS | `pre_wave1_review_bridge` | `XWAIL -> AaaS` | `AUTH-AAAS-LOOP-GATE-DELEGATE-REVIEW-20260627` | 先复核 delegated wrapper replay，再决定是否进入 AaaS 绑定预检；单仓锚点复用 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.1 AAAS delegated wrapper 单仓核对卡 / 5.6.1 AAAS delegated wrapper 确认后状态传导摘要` |
| GlobalCloud Brain | `human_review_boundary` | `KDS -> Brain` | `BRAIN-HUMAN-REVIEW-DECISION-001` | Brain 当前开发态只准备人工审查决策，不进入 accepted/integrated |
| WAS世界资产体系 | `semantic_mapping_boundary` | `WAS -> Ontology -> XWAIL` | `WAS-XWAIL-ONTOLOGY-MAPPING-001` | WAS 当前开发态只允许语义映射候选，不进入事实主存或 WAES 发布 |
| GlobalCloud XiaoC | `environment_block_boundary` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `XIAOC-MODEL-ROUTING-DRYRUN-001` | XiaoC 当前先受环境阻塞，保持 dry-run 候选边界 |
| GlobalCloud WAES | `repair_authorization_boundary` | `WAES -> XWAIL` | `AUTH-WAVE1-WAES-LINT-RUNTIME-20260626` | WAES 当前开发态入口是 repair 授权，不直接进入源码修复或发布 |
| GlobalCloud GPC | `external_runtime_boundary` | `GFIS -> GPC` | `AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626` | GPC 当前开发态只补外部 runtime 证据，不声明完整场景交付 |
| GlobalCloud Studio | `local_release_review_boundary` | `Studio -> GPCF/WAES` | `STUDIO-WORKFLOW-PERMISSIONS-001` | Studio 当前开发态只停留在本地 release/review 边界 |
| GlobalCoud GPCF | `authorization_to_pre_execution_total_bridge` | `GPCF -> all projects` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | GPCF 当前开发态先过 `GPCF/GFIS/SOP` 三仓 review 桥接入口；KDS 不再属于当前 active dirty/sensitive 边界 |
| GlobalCloud XWAIL | `pre_wave1_review_bridge` | `WAES -> XWAIL` | `AUTH-XWAIL-LOOP-GATE-DELEGATE-REVIEW-20260627` | XWAIL 当前开发态先复核 wrapper replay，再决定 contract precheck；单仓锚点复用 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.2 XWAIL delegated wrapper 单仓核对卡 / 5.6.2 XWAIL delegated wrapper 确认后状态传导摘要` |
| GlobalCloud GFIS | `source_record_boundary` | `GFIS/GPC/PVAOS -> SCaaS` | `AUTH-GFIS-SCHEME-REVIEW-20260626` | GFIS 当前开发态先分类 dirty 与 SOR 缺口，不进入真实业务链 |
| GlobalCloud MMC | `local_document_smoke_boundary` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `MMC-GOVERNANCE-TEMPLATE-SMOKE-001` | MMC 当前开发态只允许治理模板 smoke，不进入下游接入 |
| GlobalCloud KDS | `pre_wave1_review_bridge` | `KDS -> Brain` | `KDS-BRAIN-REPORT-HOLD-REVIEW-001` | KDS blocker 已解除并保持 clean；当前只保留资金报告、sync-run 接收/归档、Brain/WAES 消费和真实 KDS API 同步的 owner review 边界，不进入 Brain accepted 判断 |
| GlobalCloud XiaoG | `authorization_pack_boundary` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `XIAOG-LIVE-API-AUTH-PACK-001` | XiaoG 当前开发态只建立 live API 授权包，不触发真实外部动作 |
| GlobalCloud PVAOS | `local_release_review_boundary` | `PVAOS -> SCaaS` | `PVAOS-RELEASE-REVIEW-001` | PVAOS 当前开发态只停留在本地 release review 候选 |
| GlobalCloud SOP | `pre_wave1_review_bridge` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627` | SOP 当前开发态先复核 wrapper replay，再进入 scenario owner review 主动作；单仓锚点复用 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 第 `5.5.3 SOP delegated wrapper 单仓核对卡 / 5.6.3 SOP delegated wrapper 确认后状态传导摘要` |
| GlobalCloud PKC | `local_dev_dryrun_boundary` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `PKC-KDS-BRAIN-WORKFLOW-DRYRUN-001` | PKC 当前开发态只允许本地 dry-run，不写真实个人数据 |
| GlobalCloud XGD | `local_dev_smoke_boundary` | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | `XGD-TICK-BRAIN-SMOKE-001` | XGD 当前开发态只允许 bounded smoke，不触发真实外部动作 |

## P0 全仓任务

| 优先级 | 项目 | 当前门禁 | 开发态任务 | 验证命令 |
|---|---|---|---|---|
| P0 | GlobalCloud AAAS | dirty=1 untracked=1 diff=pass / wrapper_review_required | 先进入 delegated wrapper replay review，确认 `tools/kds-sync/loop_document_gate.py` 是否保留为项目群 canonical gate 的只读委托入口 | `git status --short --untracked-files=all && git diff --check -- .` |
| P0 | GlobalCloud Brain | dirty=3 diff=pass | 分类 Brain L4 retrieval 变更，复跑前端构建 | `npm run build -- --mode development` |
| P0 | WAS世界资产体系 | dirty=4 untracked=1 diff=pass | 分类 WAS 语义契约变更，确认 untracked 是否为受控 evidence | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud XiaoC | dirty=3 diff=pass | 分类 XiaoC 模型路由/编排变更，复跑本地 harness | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud WAES | dirty=3 diff=pass | 分类 WAES integration-release 变更，保持只做治理/审计候选 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud GPC | dirty=6 diff=pass | 分类 GPC 平台开发变更，补最小验证入口 | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud Studio | dirty=12 untracked=4 diff=pass | 分类 release review readiness 变更，保持发布动作 blocked | `npm run harness:check` |
| P0 | GlobalCoud GPCF | live dirty=current / diff=pass / git_gate_partial | 继续拆分治理/evidence/KDS mirror 大工作区，并先通过 `GPCF/GFIS/SOP` 三仓 review 授权入口 | `python3 tools/kds-sync/loop_document_gate.py --check-only` |
| P0 | GlobalCloud XWAIL | dirty=1 untracked=1 diff=pass / wrapper_review_required | 先进入 delegated wrapper replay review，再进入 WAES/AAAS contract precheck 候选链 | `git status --short --untracked-files=all && git diff --check -- .` |
| P0 | GlobalCloud GFIS | dirty=54 diff=pass / repair_required | 分类 GFIS 当前 dirty 与真实 source-of-record 缺口边界，保持 repair review 候选 | `git status --short --untracked-files=all && git diff --check -- .` |
| P0 | GlobalCloud MMC | dirty=3 diff=pass | 分类 MMC governance template smoke 变更，复跑 runtime tests | `MMC_TEST_MODE=true python3 -m pytest runtime/tests/ -q` |
| P0 | GlobalCloud KDS | clean / diff=pass / sensitive_path=resolved_not_in_git_status | 保留 KDS hold review 与 API contract dry-run 边界；不作为当前 dirty/sensitive 阻塞源 | `python3 tools/kds-sync/validate_project_group_dev_first_goal_and_kds_blocker_20260628.py` |
| P0 | GlobalCloud XiaoG | dirty=3 diff=pass | 分类 XiaoG live API auth pack，保持 live API blocked | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud PVAOS | dirty=6 diff=pass | 分类 PVAOS release gate/review 变更，保持 release blocked | `git status --short --branch && git diff --check -- .` |
| P0 | GlobalCloud SOP | dirty=1 untracked=1 diff=pass / wrapper_review_required | 先进入 delegated wrapper replay review，再进入 scenario owner review 主动作 | `git status --short --untracked-files=all && git diff --check -- .` |
| P0 | GlobalCloud PKC | dirty=8 untracked=2 diff=pass | 分类 PKC task notification 变更，复跑前端构建 | `npm run build -- --mode development` |
| P0 | GlobalCloud XGD | dirty=3 diff=pass | 分类 XGD TICK/Brain smoke 变更，保持桌面/live 调用 blocked | `git status --short --branch && git diff --check -- .` |

## 下一轮执行顺序

1. P0-A：已完成逐仓 dirty 分类证据与 validator。
2. P0-B：已完成 GPC、Studio、MMC、KDS、PKC 项目级最小验证。
3. P0-C：SOP/PKC generated/output/dist 提交前隔离判断已纳入受控，但 2026-06-28 live recheck 显示 `GlobalCloud SOP/output/.DS_Store` 为新增候选，当前状态应按 `recheck_required` 继续重放，见 `docs/harness/evidence/globalcloud-project-group-generated-output-dist-isolation-20260627.md`。
4. P0-D：已完成 GPCF 大工作区 review 包拆分；当前拆为 KDS 本地镜像、mirror ledger、status registers、docs indexes、Agent-Reach evidence、Agent-Reach tooling/fixture、project-group P0 evidence 七包，见 `docs/harness/evidence/globalcloud-project-group-gpcf-worktree-review-packages-20260627.md`。
5. P0-E：已建立四层授权矩阵；当前 `REVIEW-AUTH` 的第一入口已切到 `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001`。`REVIEW-AUTH-GPCF-WORKTREE-20260627` 仍保留为后续 GPCF review 包入口，但位于 `GPCF/GFIS/SOP` 三仓 review 边界之后。
6. P0-F：已将 `GlobalCloud AAAS`、`GlobalCloud XWAIL`、`GlobalCloud SOP` 的 delegated `loop_document_gate.py` 收口为统一 baseline 和 replay 边界，见 `docs/harness/evidence/globalcloud-project-group-external-loop-gate-delegate-baseline-20260627.md`；下一步只允许在人工确认后进入对应 wrapper review replay，不允许 stage/commit/push/delete/runtime/acceptance。
7. P0-G：已建立 `docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md`；2026-06-28 live override 后，当前 active review 边界收口为 `GPCF/GFIS/SOP` 三仓，KDS/AAAS/XWAIL 已从当前 dirty/sensitive 阻塞源移除；任何 Wave 1 pack、GPCF worktree review、Git 动作仍不得绕过当前三仓边界。
8. P0-H：已建立 `docs/harness/evidence/globalcloud-project-group-next-stage-authorization-package-20260627.md`；2026-06-28 live override 后，当前 next-stage 授权包只允许围绕 `GPCF/GFIS/SOP` 三仓 review 边界做人工确认，不允许真实回执落账。
9. P0-I：已建立 `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-NEXT-STAGE-AUTHORIZATION-CHAIN-001.md`，将 next-stage 人工确认链固化为 loop-round；当前只证明链路已归档，不允许进入 Wave 1 执行回执或任何真实授权。

## 2026-06-28 Live Override 补充

| 项目 | 当前 live 状态 | 当前 replay 入口 | 验证命令 |
|---|---|---|---|
| GlobalCloud AAAS | `clean / diff_check=pass` | historical delegated wrapper replay only | 当前不属于 active dirty review 边界；如需回放，仍以 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 的历史锚点为准 |
| GlobalCloud XWAIL | `clean / diff_check=pass` | historical delegated wrapper replay only | 当前不属于 active dirty review 边界；如需回放，仍以 `globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 的历史锚点为准 |
| GlobalCloud SOP | `dirty=2 / diff_check=pass / owner_review_required` | `AUTH-SOP-LOOP-GATE-DELEGATE-REVIEW-20260627` | `git status --short --untracked-files=all`、`python3 tools/kds-sync/loop_document_gate.py --check-only`、`python3 tools/kds-sync/validate_sop_scenario_owner_review.py` |
| GlobalCloud GFIS | `dirty=91 / diff_check=pass / repair_required` | `GFIS-RUNTIME-SOP-E2E-MIN-001` | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_gfis_real_fact_entry_gate.py`、`python3 tools/kds-sync/validate_loop_v11_gfis_authorization_boundary.py` |
| GlobalCloud KDS | `clean / diff_check=pass / sensitive_path=resolved_not_in_git_status` | `KDS-BRAIN-REPORT-HOLD-REVIEW-001` | `python3 tools/kds-sync/validate_project_group_dev_first_goal_and_kds_blocker_20260628.py`、`python3 tools/kds-sync/validate_kds_token.py` |
| GlobalCoud GPCF | `dirty=current / git_gate_partial / authorization_routing_ready` | `GPCF-PRE-WAVE1-REVIEW-AUTHORIZATION-REQUEST-20260627-001` | `python3 tools/kds-sync/validate_project_group_current_state_baseline_refresh_20260626.py`、`python3 tools/kds-sync/validate_project_group_real_execution_governance_board.py`、`python3 tools/kds-sync/loop_document_gate.py --check-only` |

## 状态声明

- development_queue_ready = true
- accepted = false
- integrated = false
- production_ready = false
