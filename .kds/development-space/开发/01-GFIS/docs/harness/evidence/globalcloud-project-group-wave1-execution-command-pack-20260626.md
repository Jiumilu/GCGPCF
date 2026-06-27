---
doc_id: GPCF-DOC-PROJECT-GROUP-WAVE1-EXECUTION-COMMAND-PACK-20260626
title: GlobalCloud 项目群 Wave 1 真实执行命令包 2026-06-26
project: GFIS
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD]
domain: docs
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-wave1-execution-command-pack-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-27
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Wave 1 真实执行命令包 2026-06-26

## 1. 定位

本文承接当前状态基线刷新和下一批可执行任务包，将 Wave 1 的主链路任务转成执行前命令包。本文只定义任务、命令、证据、门禁、回滚和人工确认边界，不执行源码修复、不读取生产数据、不触发外部联调、不 stage、不 commit、不 push、不发布、不升级状态。

当前 Wave 1 命令包仍受 `docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md` 约束：在 `KDS/AAAS/XWAIL/GPCF/GFIS/SOP` 六仓 review 边界未完成人工确认前，Wave 1 不得进入任何执行回执。

当前 Wave 1 命令包与以下两份证据保持一致：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

## 2. 控制结论

```text
project_group_wave1_execution_command_pack_20260626 = controlled
wave = 1
command_pack_count = 5
authorization_required_count = 5
live_project_group_git_gate = blocked
project_group_current_state_baseline_refresh_20260626 = controlled
development_queue_ready = true
review_boundary_repo_count = 6
noise_cleanup_repo_count = 1
review_boundary_repos_current = GlobalCloud AAAS, GlobalCoud GPCF, GlobalCloud XWAIL, GlobalCloud GFIS, GlobalCloud KDS, GlobalCloud SOP
noise_cleanup_repo_current = WAS世界资产体系(.DS_Store)
action_executed_count = 0
accepted = false
integrated = false
production_ready = false
customer_accepted = false
stage_allowed = false
commit_allowed = false
push_allowed = false
```

## 3. Wave 1 命令包矩阵

| pack_id | 项目 | 目标 | 可执行命令 | 预期证据 | 门禁 | 回滚边界 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|
| `WAVE1-WAES-LINT-RUNTIME-001` | WAES | 修复 lint/runtime 并恢复综合检查 | `npm run lint`、`npm run check`、`npm run typecheck`、`npm run test`、`npm run build`、`npm run check:wasm`、`python3 tools/kds-sync/validate_waes_lint_runtime_repair_authorization.py` | `docs/harness/WAES/evidence/waes-lint-runtime-repair-*.md`、命令输出摘要、修复 diff 摘要 | WAES quality gate、WAES authorization gate、GPCF register gate、Loop document gate、Git diff check | 仅回滚本次 WAES lint/runtime 修复；任一命令失败则保持 `repair_required` | 是，源码修复、提交、推送、发布前均需确认 | 不声明 WAES 治理运行闭环、发布、权限变更、accepted 或客户验收 |
| `WAVE1-GFIS-REAL-SOR-001` | GFIS | 获取或登记真实 source-of-record 输入 | `python3 tools/kds-sync/validate_gfis_was_source_record_submission_precheck.py`、GFIS source-record intake 扫描、人工核验记录检查 | `docs/harness/GFIS/evidence/gfis-real-source-record-intake-*.md`、真实订单或平台订单回执索引、人工核验结论 | GFIS source-record gate、business owner gate、WAES review gate、GPCF register gate | 不写入 GFIS runtime；输入不合格时登记 rejected reason 并保持 `repair_required` | 是，需要业务 owner、订单 owner 或等效正式回执 | 不声明真实 SOP E2E、生产写入、SCaaS 闭环、accepted 或客户验收 |
| `WAVE1-GPC-EXTERNAL-RUNTIME-001` | GPC | 补生产确认、外部联调和 runtime surface 证据 | `npm run quality:100`、`npm run quality:ops`、`npm run test:e2e`、`python3 tools/kds-sync/validate_gpc_evidence_browser_repair.py` | `docs/harness/GPC/evidence/gpc-external-runtime-evidence-*.md`、生产确认记录、外部联调记录、runtime surface 可达性摘要 | GPC external runtime gate、browser/e2e gate、GFIS source-record dependency gate、Loop document gate | 不伪造生产确认；外部证据缺失时保持 `external_runtime_evidence_required` | 是，生产/外部联调需要 owner 或环境确认 | 不声明外部联调完成、真实交付、SCaaS 完整交付或客户验收 |
| `WAVE1-BRAIN-HUMAN-REVIEW-001` | Brain | 准备 Brain 人工审查决策，不自动 accepted | `python3 tools/kds-sync/validate_brain_review_handoff.py`、Brain 本地 harness validators、KDS RAG 输入复核 | `docs/harness/Brain/evidence/brain-human-review-decision-*.md`、审查意见、accepted/rework 决策记录 | Brain review handoff gate、KDS RAG input gate、human review gate | 未确认时保持 `ready_for_review / authorization_boundary`；审查不通过则进入 rework | 是，accepted、integrated、production_ready 前必须确认 | 不声明 Brain accepted、integrated、production_ready 或客户验收 |
| `WAVE1-GPCF-POST-SCHEME-REVIEW-001` | GPCF/all projects | 将当前 6 仓 dirty review 转成逐仓授权执行入口，并优先锁定 KDS sensitive_path、GFIS repair 边界和 AAAS/XWAIL/SOP delegated wrapper 边界 | `python3 tools/kds-sync/validate_project_group_pre_wave1_review_authorization_request_20260627.py`、`python3 tools/kds-sync/validate_project_group_post_scheme_recognition_review_authorization_request_20260626.py`、`python3 tools/kds-sync/validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`、`python3 tools/kds-sync/validate_project_group_current_state_baseline_refresh_20260626.py`、`python3 tools/kds-sync/validate_project_group_dev_task_queue_20260626.py`、`python3 tools/kds-sync/loop_document_gate.py` | `docs/harness/evidence/globalcloud-project-group-pre-wave1-review-authorization-request-20260627.md`、`docs/harness/evidence/globalcloud-project-group-post-scheme-recognition-review-authorization-request-20260626.md`、逐仓 review 授权回执 | pre-wave1 review authorization gate、post-scheme review authorization gate、dirty queue gate、current baseline refresh gate、dev task queue gate、Git clean gate、Loop document gate | 不自动 review、stage、commit、push、delete、cleanup；任一仓缺确认则保持 `review_allowed=false` 且 Wave 1 不得进入执行回执 | 是，任何 review/stage/commit/push/delete 前必须逐仓确认 | 不声明项目群 Git 全量 clean、可提交、可推送、Wave 1 已授权、accepted、integrated 或客户验收 |

## 4. 执行顺序

| 顺序 | 动作 | 控制 |
|---|---|---|
| 1 | 先复跑 `pre-wave1` 桥接 validator | 确认 6 仓 review 边界仍全部 `pending_confirmation`，且 Wave 1 仍被前置桥接入口锁定 |
| 2 | 复跑当前状态基线刷新验证器 | 确认 17 项目状态和 Git live 边界仍受控 |
| 2.1 | 复跑开发态任务队列验证器 | 确认 17 项目开发态入口仍与 Wave 1 pack 前置顺序一致 |
| 3 | 用户按 pack_id 明确授权 | 未授权 pack 的所有动作保持 `false` |
| 4 | 登记授权回执 | 写入授权回执总账，不扩大授权范围 |
| 5 | 执行对应 pack 命令 | 只运行被授权 pack 的命令，不跨项目联动执行 |
| 6 | 写入执行证据 | 证据必须包含命令、结果、失败项、边界和回滚说明 |
| 7 | 复跑门禁 | 总控板、目标覆盖审计、Loop 文档门禁、Git clean 门禁 |

## 5. 依赖传导

| 依赖链 | Wave 1 影响 |
|---|---|
| `WAES -> XWAIL -> AaaS` | WAES 未修复前，XWAIL/AaaS 只能保持 `integration_precheck_candidate` |
| `GFIS/GPC/PVAOS -> SCaaS` | GFIS SOR 和 GPC 外部运行证据未完成前，SCaaS 不得声明真实运营闭环 |
| `KDS -> Brain` | Brain 只能进入人工审查，不得自动 accepted/integrated |
| `GPCF -> all projects` | 当前 6 仓 dirty 与 KDS sensitive_path 未逐仓确认、`pre-wave1` 未解除前，不得声明项目群 Git clean、可提交或 Wave 1 已授权 |

## 6. 禁止声明

```text
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

本文建立 Wave 1 真实执行命令包，不代表任何任务已执行，不代表任何授权已发生。
