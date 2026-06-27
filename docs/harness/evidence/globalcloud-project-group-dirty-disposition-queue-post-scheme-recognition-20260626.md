---
doc_id: GPCF-DOC-PROJECT-GROUP-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626
title: GlobalCloud 项目群 Dirty 仓逐仓处置队列｜方案识别规则写入后 2026-06-26
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Dirty 仓逐仓处置队列｜方案识别规则写入后 2026-06-26

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626-001` |
| 前置证据 | `globalcloud-project-group-dirty-disposition-queue-20260625.md`、`globalcloud-project-group-live-status-snapshot-20260626.md`、`GlobalCloud 项目群方案体系识别规则.md` |
| 当前结论 | `project_group_dirty_disposition_queue_post_scheme_recognition_20260626 = controlled` |
| 状态候选 | `dirty_disposition_queue_post_scheme_recognition_ready` |
| recheck_date | `2026-06-27` |
| dirty_repo_count | `7` |
| scheme_recognition_dirty_count | `1` |
| review_candidate_count | `6` |
| owner_decision_count | `1` |
| noise_decision_count | `1` |
| kds_sensitive_path_count | `1` |
| review_allowed | `false` |
| stage_allowed | `false` |
| commit_allowed | `false` |
| push_allowed | `false` |
| delete_allowed | `false` |
| current_state_refresh | `project_group_current_state_baseline_refresh_20260626 = controlled` |
| development_queue | `development_queue_ready = true` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文承接 2026-06-26 会话入口识别规则写入后的真实 Git 状态，并按 2026-06-27 live recheck 把 post-scheme 处置队列从“17 仓历史口径”收敛到“7 仓当前事实”。其中 `WAS世界资产体系/.DS_Store` 作为 system noise cleanup 单独沿既有噪声处置路径治理，不并入 Pre-Wave1 的 6 仓 review 边界。旧队列 `GPCF-DIRTY-DISPOSITION-QUEUE-001` 和旧版 17 仓 post-scheme 审查口径仍作为历史证据保留；本文是当前 replay 口径，不覆盖历史事实。

当前 post-scheme dirty 逐仓处置队列还必须与以下两份证据保持一致：

- `docs/harness/evidence/globalcloud-project-group-current-state-baseline-refresh-20260626.md`
- `docs/harness/evidence/globalcloud-project-group-dev-task-queue-20260626.md`

本文只把当前 7 个 dirty 仓从“live 状态变化”推进到“逐仓处置队列”。它不执行删除、清理、stage、commit、push、merge、真实 KDS API 同步、生产部署或客户验收。

## 2. 逐仓处置队列

| 队列 ID | 仓库 | live dirty 类型 | 当前处置类型 | 下一步动作 | 必跑命令 | 证据 | 门禁 | 回滚/降级 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|---|---|
| `DISP-WAS-SYSTEM-NOISE-20260627` | `WAS世界资产体系` | tracked `.DS_Store` system noise | `noise_decision_required / system_artifact_cleanup_candidate` | 沿既有 `AUTH-WAS-DELETE-DS-STORE-20260626` 路径，确认删除 `.DS_Store` 或补充忽略规则；不并入 Pre-Wave1 六仓 review 边界；单仓锚点复用 `4.1 A 项单仓核对卡 / 4.2 A 项确认后状态传导摘要` | `git status --short --untracked-files=all`、`git diff --check` | 本队列、`globalcloud-project-group-live-status-snapshot-20260626.md`、`globalcloud-project-group-authorization-pre-execution-command-pack-20260626.md` | live status snapshot gate、Git clean gate、document pollution gate | 回滚 WAS noise cleanup 记录；未确认前保持 `noise_decision_required` | 是，需要确认 `allow_delete_ds_store` 或 `allow_gitignore_update` | 不声明 WAS clean、不自动删除 `.DS_Store`、不声明项目群 Git 全量 clean |
| `DISP-AAAS-LOOP-GATE-DELEGATE-20260627` | `GlobalCloud AAAS` | delegated loop gate wrapper、未跟踪 `tools/kds-sync/loop_document_gate.py` | `loop_gate_delegate_review_candidate / wrapper_scope_confirmation_required` | 确认 AAAS delegated loop gate wrapper 是否保留为项目群 gate 纳入入口，并校验它只委托到 GPCF canonical gate，不解释为 AaaS 真实业务完成 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/loop_document_gate.py --check-only` | 本队列、`globalcloud-project-group-live-status-snapshot-20260626.md`、`tools/kds-sync/loop_document_gate.py` | live status snapshot gate、Loop document gate、Git clean gate | 回滚 AAAS wrapper review 记录；未确认前保持 `partial/rework` 和 dirty boundary | 是，review/stage/commit/push 或保留 wrapper 前需要确认 | 不声明 AaaS 真实计费、客户订阅、项目群 Git 全量 clean或真实 KDS API 已同步 |
| `DISP-GPCF-SCHEME-RECOGNITION-20260626` | `GlobalCoud GPCF` | 总控方案、识别规则、当前状态刷新证据、validator 与 `.kds` 镜像聚合修改 | `scheme_recognition_review_candidate / governance_evidence_review_candidate / current_baseline_replay_required` | 审查总控文档、识别规则、6 仓当前事实回写和镜像边界；镜像包不得解释为真实 KDS API 同步 | `python3 tools/kds-sync/validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`、`python3 tools/kds-sync/validate_project_group_real_execution_governance_board.py`、`python3 tools/kds-sync/validate_project_group_current_state_baseline_refresh_20260626.py` | 本队列、`GlobalCloud 项目群方案体系识别规则.md`、`globalcloud-project-group-live-status-snapshot-20260626.md`、`globalcloud-project-group-current-state-baseline-refresh-20260626.md` | post-scheme dirty queue gate、governance board gate、current baseline gate、Git clean gate | 回滚本轮新增治理文档/validator/引用；镜像异常时降级 `partial/rework` | 是，治理包和镜像包进入 review/stage/commit/push 前需要确认 | 不声明项目群 Git 全量 clean、真实 KDS API 已同步、可提交或可推送 |
| `DISP-XWAIL-LOOP-GATE-DELEGATE-20260627` | `GlobalCloud XWAIL` | delegated loop gate wrapper、未跟踪 `tools/kds-sync/loop_document_gate.py` | `loop_gate_delegate_review_candidate / wrapper_scope_confirmation_required` | 确认 XWAIL delegated loop gate wrapper 是否保留为项目群 gate 纳入入口，并校验它只委托到 GPCF canonical gate，不解释为 XWAIL 完整工具链闭环 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/loop_document_gate.py --check-only` | 本队列、`globalcloud-project-group-live-status-snapshot-20260626.md`、`tools/kds-sync/loop_document_gate.py` | live status snapshot gate、Loop document gate、Git clean gate | 回滚 XWAIL wrapper review 记录；未确认前保持 `partial/rework` 和 dirty boundary | 是，review/stage/commit/push 或保留 wrapper 前需要确认 | 不声明 XWAIL 完整工具链完成、WAES 发布、AaaS 绑定或项目群 Git 全量 clean |
| `DISP-GFIS-SCHEME-RECOGNITION-20260626` | `GlobalCloud GFIS` | 真实运行层 repair 工作区、source-of-record 阻塞、existing runtime evidence dirty | `repair_boundary_review_candidate / real_source_record_pending` | 审查 GFIS 当前 dirty 工作区与真实 SOR 阻塞边界；不得把 repair review 写成真实业务输入已到位 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_gfis_real_fact_entry_gate.py` | 本队列、`gfis-real-runtime-baseline-20260624.md`、`globalcloud-project-group-live-status-snapshot-20260626.md` | GFIS real-fact entry gate、Git clean gate | 回滚 GFIS review 记录；无真实业务输入时保持 `repair_required` | 是，review/stage/commit/push 或真实业务输入确认前需要确认 | 不声明 GFIS 真实 source-of-record 已取得、不声明真实 SOP E2E 已通过 |
| `DISP-KDS-SCHEME-RECOGNITION-20260626` | `GlobalCloud KDS` | `.env.production.example` sensitive_path、KDS hold review、owner decision 边界 | `sensitive_path_review_required / owner_decision_required / diff_check_currently_pass` | 审查 `.env.production.example` 的 sensitive path 归类路线，并保持 KDS 业务报告/hold review 的 owner 边界；单仓锚点复用 `5.3 KDS 单仓核对卡 / 5.4 KDS 确认后状态传导摘要` | `git status --short --untracked-files=all`、`git diff --check`、`git ls-files --stage -- .env.production.example`、`python3 tools/kds-sync/validate_kds_token.py` | 本队列、`kds-brain-report-hold-review-20260625.md`、`globalcloud-project-group-live-status-snapshot-20260626.md` | KDS sensitive path gate、KDS hold review gate、Git clean gate | 回滚 KDS review 记录；owner 未确认且 sensitive_path 未归类前保持 blocked | 是，需要 KDS owner 与 Git 动作授权分别确认 | 不声明 KDS sensitive_path 已解除、不声明真实 KDS API 已同步 |
| `DISP-SOP-LOOP-GATE-DELEGATE-20260627` | `GlobalCloud SOP` | delegated loop gate wrapper、未跟踪 `tools/kds-sync/loop_document_gate.py` | `loop_gate_delegate_review_candidate / wrapper_scope_confirmation_required` | 确认 SOP delegated loop gate wrapper 是否保留为项目群 gate 纳入入口，并校验它只委托到 GPCF canonical gate，不解释为 SOP 场景方案已确认或入 KDS | `git status --short --untracked-files=all`、`python3 tools/kds-sync/loop_document_gate.py --check-only` | 本队列、`globalcloud-project-group-live-status-snapshot-20260626.md`、`tools/kds-sync/loop_document_gate.py` | live status snapshot gate、Loop document gate、Git clean gate | 回滚 SOP wrapper review 记录；未确认前保持 `partial/rework` 和 dirty boundary | 是，review/stage/commit/push 或保留 wrapper 前需要确认 | 不声明 SOP 场景方案已确认、KDS 事实已入库、客户验收或项目群 Git 全量 clean |

## 3. 状态传导

| 输入 | 输出 | 限制 |
|---|---|---|
| `project_group_live_status_snapshot_20260626 = controlled` | `dirty_repo_count = 7` | 只说明 live dirty 集合已按 2026-06-27 重新采集，不说明 Git clean |
| `project_group_scheme_recognition_rules = controlled` | `scheme_recognition_dirty_count = 1` | 说明会话入口规则仍是 GPCF 当前治理工作区的一部分，不说明其它 14 仓需要进入 review |
| `project_group_dirty_disposition_queue = controlled` | `post_scheme_queue_supersedes_runtime_count_only` | 旧 7 仓队列作为历史证据保留；新队列更新当前 7 仓 live dirty 处置口径，其中 WAS system noise 单独治理 |
| `project_group_git_clean = blocked` | `kds_sensitive_path_count = 1` | 当前 KDS `git diff --check` 为 pass，但项目群 Git clean 已因 7 仓 dirty 和 `.env.production.example` sensitive_path 收紧为 blocked |
| 任一仓人工确认 | `repo_specific_action_allowed` | 只限该仓、该包、该动作；不能传导到其它仓或其它动作 |

## 4. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 读取 7 个当前 dirty 仓 live Git 状态，将 post-scheme 旧口径重放为当前逐仓处置队列 |
| stop | 停止在 `authorization_boundary`，不执行清理、提交、推送、真实同步、生产动作或状态升级 |
| verify | 通过 `validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`、`validate_project_group_scheme_recognition_rules_20260626.py`、总控板校验、文档门禁和 Git clean 门禁复核 |
| recover | 若队列与 live dirty 不一致，回滚本文和 validator，重新采集当前 7 仓 Git 状态 |
| debug | 当前主要阻塞是 KDS sensitive_path、GFIS 真实 SOR 阻塞、GPCF 治理 review 边界、WAS system noise cleanup，以及 AAAS/XWAIL/SOP delegated wrapper 的保留范围确认，而不是文档识别规则缺失 |

## 5. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明任一项目方案识别规则已经完成提交验收。
- 不声明 KDS `.env.production.example` sensitive_path review 或 cleanup 已执行或已修复。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或客户验收。
- 不声明真实 KDS API 已同步。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
