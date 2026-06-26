---
doc_id: GPCF-DOC-PROJECT-GROUP-DIRTY-DISPOSITION-QUEUE-POST-SCHEME-RECOGNITION-20260626
title: GlobalCloud 项目群 Dirty 仓逐仓处置队列｜方案识别规则写入后 2026-06-26
project: KDS
related_projects: [GPC, WAES, KDS, Brain, XiaoC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md
source_path: docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-post-scheme-recognition-20260626.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
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
| dirty_repo_count | `17` |
| scheme_recognition_dirty_count | `17` |
| review_candidate_count | `17` |
| owner_decision_count | `2` |
| noise_decision_count | `1` |
| kds_diffcheck_blocker_count | `0` |
| review_allowed | `false` |
| stage_allowed | `false` |
| commit_allowed | `false` |
| push_allowed | `false` |
| delete_allowed | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文承接 2026-06-26 会话入口识别规则写入后的真实 Git 状态。旧队列 `GPCF-DIRTY-DISPOSITION-QUEUE-001` 仍作为 2026-06-25 的 7 仓历史处置证据保留；本文是新口径，不覆盖旧口径。

本文只把 17 个 dirty 仓从“live 状态变化”推进到“逐仓处置队列”。它不执行删除、清理、stage、commit、push、merge、真实 KDS API 同步、生产部署或客户验收。

## 2. 逐仓处置队列

| 队列 ID | 仓库 | live dirty 类型 | 当前处置类型 | 下一步动作 | 必跑命令 | 证据 | 门禁 | 回滚/降级 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|---|---|
| `DISP-AAAS-SCHEME-RECOGNITION-20260626` | `GlobalCloud AAAS` | `AGENTS.md` 与 AaaS 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则与继承声明是否准确；未确认前保持 dirty review | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`GlobalCloud 项目群方案体系识别规则.md` | scheme recognition rules gate、Loop document gate、Git clean gate | 回滚 AAAS `AGENTS.md` 识别段和项目方案继承声明；若缺失或冲突，降级 `partial/rework` | 是，review/stage/commit/push 前需要确认 | 不声明 AaaS 可提交、已发布、客户可订阅或验收 |
| `DISP-BRAIN-SCHEME-RECOGNITION-20260626` | `GlobalCloud Brain` | `AGENTS.md` 与 Brain 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则与继承声明是否准确；Brain accepted/integrated 仍需另行人工确认 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`brain-review-handoff-20260625.md` | scheme recognition rules gate、Brain review handoff gate、Git clean gate | 回滚 Brain `AGENTS.md` 识别段和项目方案继承声明；若影响 Brain 边界，保持 `authorization_boundary` | 是，review/stage/commit/push 或状态升级前需要确认 | 不声明 Brain accepted、integrated、production_ready 或客户验收 |
| `DISP-WAS-SCHEME-RECOGNITION-20260626` | `WAS世界资产体系` | `AGENTS.md`、WAS 项目级总体/实施方案继承声明、历史 `.DS_Store` | `scheme_recognition_review_candidate / noise_decision_required` | 审查 WAS 作为主项目的继承关系；`.DS_Store` 删除或忽略规则另行确认 | `git status --short --untracked-files=all`、`git diff --check`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`HOLD-WAS-SYSTEM-NOISE-20260625` | scheme recognition rules gate、pollution gate、Git clean gate | 回滚 WAS `AGENTS.md` 识别段和项目方案继承声明；不自动删除 `.DS_Store` | 是，需要 review 确认；删除噪声另需 `allow_delete_ds_store` 或 `allow_gitignore_update` | 不声明 WAS clean、不自动删除 `.DS_Store`、不声明主方案已验收 |
| `DISP-XIAOC-SCHEME-RECOGNITION-20260626` | `GlobalCloud XiaoC` | `AGENTS.md` 与 XiaoC 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则与继承声明；Node engine 阻塞仍按原证据处理 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`xiaoc-model-routing-dryrun-environment-blocked-20260625.md` | scheme recognition rules gate、XiaoC dry-run environment gate、Git clean gate | 回滚 XiaoC `AGENTS.md` 识别段和项目方案继承声明；若 Node 版本仍不匹配，保持 `environment_blocked` | 是，review/stage/commit/push 前需要确认 | 不声明 XiaoC dry-run 通过、不声明生产模型路由可用 |
| `DISP-WAES-SCHEME-RECOGNITION-20260626` | `GlobalCloud WAES` | `AGENTS.md` 与 WAES 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate / existing_repair_boundary` | 审查 WAES 入口识别规则；WAES lint/runtime 修复仍需另行授权 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`waes-lint-runtime-repair-authorization-20260625.md` | scheme recognition rules gate、WAES quality gate、Git clean gate | 回滚 WAES `AGENTS.md` 识别段和项目方案继承声明；lint 修复失败保持 `repair_required` | 是，review/stage/commit/push 或 lint 修复前需要确认 | 不声明 WAES 治理运行闭环完成、不声明 WAES 发布 |
| `DISP-GPC-SCHEME-RECOGNITION-20260626` | `GlobalCloud GPC` | `AGENTS.md`、GPC 项目级总体/实施方案继承声明、既有 evidence/browser repair dirty | `scheme_recognition_review_candidate / existing_review_candidate` | 审查入口识别规则，并保留 GPC 外部证据和运行态边界 | `git status --short --untracked-files=all`、`npm run quality:repo`、`npm run test:e2e`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`gpc-evidence-browser-repair-20260625.md` | scheme recognition rules gate、GPC evidence gate、Git clean gate | 回滚 GPC `AGENTS.md` 识别段和项目方案继承声明；外部证据缺失时保持 `external_runtime_evidence_required` | 是，review/stage/commit/push 前需要确认 | 不声明 GPC 外部联调完成、不声明生产确认完成 |
| `DISP-STUDIO-SCHEME-RECOGNITION-20260626` | `GlobalCloud Studio` | `AGENTS.md`、Studio 项目级总体/实施方案继承声明、既有 evidence-index dirty | `scheme_recognition_review_candidate / existing_review_candidate` | 审查入口识别规则；不得触发 release workflow | `git status --short --untracked-files=all`、`npm run harness:check`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`studio-workflow-permissions-recheck-20260625.md` | scheme recognition rules gate、Studio harness gate、release boundary gate | 回滚 Studio `AGENTS.md` 识别段和项目方案继承声明；release 边界异常保持 `local_release_review_boundary` | 是，review/stage/commit/push 或 release 授权前需要确认 | 不声明 Studio 已发布、不触发 GitHub release 或生产部署 |
| `DISP-GPCF-SCHEME-RECOGNITION-20260626` | `GlobalCoud GPCF` | 总控方案、识别规则、证据、validator、`.kds` 本地镜像聚合修改 | `scheme_recognition_review_candidate / governance_evidence_review_candidate` | 审查项目群总控文档、识别规则、17 仓入口写入和本队列；镜像包不得解释为真实 KDS API 同步 | `python3 tools/kds-sync/validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`、`python3 tools/kds-sync/validate_project_group_real_execution_governance_board.py`、`python3 tools/kds-sync/loop_document_gate.py` | 本队列、`GlobalCloud 项目群方案体系识别规则.md`、`globalcloud-project-group-live-status-snapshot-20260626.md` | post-scheme dirty queue gate、governance board gate、Loop document gate、Git clean gate | 回滚本轮新增治理文档/validator/引用；镜像异常时降级 `partial/rework` | 是，治理包和镜像包进入 review/stage/commit/push 前需要确认 | 不声明项目群 Git 全量 clean、真实 KDS API 已同步、可提交或可推送 |
| `DISP-XWAIL-SCHEME-RECOGNITION-20260626` | `GlobalCloud XWAIL` | `AGENTS.md` 与 XWAIL 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查 XWAIL 主项目对 WAS 主方案和实施方案的继承声明 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`xwail-waes-aaas-contract-precheck-20260625.md` | scheme recognition rules gate、XWAIL contract precheck gate、Git clean gate | 回滚 XWAIL `AGENTS.md` 识别段和项目方案继承声明；契约候选异常保持 `integration_precheck_candidate` | 是，review/stage/commit/push 前需要确认 | 不声明完整 XWAIL 工具链完成、不声明 WAES 发布或 AaaS 绑定完成 |
| `DISP-GFIS-SCHEME-RECOGNITION-20260626` | `GlobalCloud GFIS` | `AGENTS.md` 与 GFIS 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则；真实 source-of-record 仍需业务输入 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`gfis-real-runtime-baseline-20260624.md` | scheme recognition rules gate、GFIS evidence gate、Git clean gate | 回滚 GFIS `AGENTS.md` 识别段和项目方案继承声明；无真实业务输入时保持 `repair_required` | 是，review/stage/commit/push 或真实业务输入确认前需要确认 | 不声明 GFIS 真实 source-of-record 已取得、不声明交付完成 |
| `DISP-MMC-SCHEME-RECOGNITION-20260626` | `GlobalCloud MMC` | `AGENTS.md` 与 MMC 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则和治理模板 smoke 边界 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`mmc-governance-template-smoke-20260625.md` | scheme recognition rules gate、MMC smoke gate、Git clean gate | 回滚 MMC `AGENTS.md` 识别段和项目方案继承声明；模板缺失时保持 `baseline_controlled` | 是，review/stage/commit/push 前需要确认 | 不声明 MMC runtime 已通过、不声明下游项目已接入 |
| `DISP-KDS-SCHEME-RECOGNITION-20260626` | `GlobalCloud KDS` | `AGENTS.md`、KDS 项目级总体/实施方案继承声明、资金报告/sync-run owner review | `scheme_recognition_review_candidate / owner_decision_required / diff_check_currently_pass` | 审查入口识别规则；资金报告与 sync-run 继续 owner review；当前 `git diff --check` 为 pass，但仍不得跳过 review/stage/commit/push 授权 | `git status --short --untracked-files=all`、`git diff --check`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py`、`python3 tools/kds-sync/validate_kds_token.py` | 本队列、`kds-brain-report-hold-review-20260625.md`、`globalcloud-project-group-live-status-snapshot-20260626.md` | scheme recognition rules gate、KDS hold review gate、Git clean gate | 回滚 KDS `AGENTS.md` 识别段和项目方案继承声明；owner 未确认保持 hold | 是，需要 scheme review、business owner、KDS owner 分别确认 | 不声明资金报告已业务确认、不声明项目群 Git 全量 clean、不声明真实 KDS API 已同步 |
| `DISP-XIAOG-SCHEME-RECOGNITION-20260626` | `GlobalCloud XiaoG` | `AGENTS.md` 与 XiaoG 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则；live API/通知/WAES 写入仍保持授权包边界 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`xiaog-live-api-auth-pack-20260625.md` | scheme recognition rules gate、XiaoG authorization pack gate、Git clean gate | 回滚 XiaoG `AGENTS.md` 识别段和项目方案继承声明；未授权不触发 live API 或生产写入 | 是，review/stage/commit/push 或 live API 授权前需要确认 | 不声明 live GFIS/GPC API 已验证、不声明真实通知或 WAES 写入完成 |
| `DISP-PVAOS-SCHEME-RECOGNITION-20260626` | `GlobalCloud PVAOS` | `AGENTS.md`、PVAOS 项目级总体/实施方案继承声明、既有 release gate dirty | `scheme_recognition_review_candidate / existing_review_candidate` | 审查入口识别规则；远程 CI/PR/merge/发布仍需另行授权 | `git status --short --untracked-files=all`、`npm run release:gate:local`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`pvaos-release-review-20260625.md` | scheme recognition rules gate、PVAOS local release gate、Git clean gate | 回滚 PVAOS `AGENTS.md` 识别段和项目方案继承声明；release gate 失败保持 `repair_required` | 是，review/stage/commit/push 或远程发布前需要确认 | 不声明远程 CI、PR、merge、生产发布或客户验收 |
| `DISP-SOP-SCHEME-RECOGNITION-20260626` | `GlobalCloud SOP` | `AGENTS.md`、SOP 项目级总体/实施方案继承声明、场景生成物和 `.DS_Store` 历史 owner review | `scheme_recognition_review_candidate / owner_decision_required` | 审查入口识别规则；武汉城市圈场景生成物继续 owner review；噪声删除另行确认 | `git status --short --untracked-files=all`、`python3 scripts/validate_sop_assets.py`、`python3 scripts/run_smoke_test.py`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`sop-scenario-owner-review-20260625.md` | scheme recognition rules gate、SOP owner review gate、asset smoke gate | 回滚 SOP `AGENTS.md` 识别段和项目方案继承声明；未确认保持 owner review，不删除 `.DS_Store` | 是，需要 scheme review、scenario owner 和噪声清理分别确认 | 不声明场景方案已确认、已交付、KDS 事实入库或客户验收 |
| `DISP-PKC-SCHEME-RECOGNITION-20260626` | `GlobalCloud PKC` | `AGENTS.md` 与 PKC 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则和 KDS/Brain workflow dry-run 边界 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`pkc-kds-brain-workflow-dryrun-20260625.md` | scheme recognition rules gate、PKC workflow gate、Git clean gate | 回滚 PKC `AGENTS.md` 识别段和项目方案继承声明；dry-run 失败保持 `repair_required` | 是，review/stage/commit/push 前需要确认 | 不声明真实 KDS/Brain 集成完成、不声明客户验收 |
| `DISP-XGD-SCHEME-RECOGNITION-20260626` | `GlobalCloud XGD` | `AGENTS.md` 与 XGD 项目级总体/实施方案继承声明 | `scheme_recognition_review_candidate` | 审查入口识别规则和 Tick Brain smoke 边界 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_project_group_scheme_recognition_rules_20260626.py` | 本队列、`xgd-tick-brain-smoke-20260625.md` | scheme recognition rules gate、XGD smoke gate、Git clean gate | 回滚 XGD `AGENTS.md` 识别段和项目方案继承声明；smoke 失败保持 `repair_required` | 是，review/stage/commit/push 前需要确认 | 不声明长程 Agent 生产可用、不声明真实外部动作 |

## 3. 状态传导

| 输入 | 输出 | 限制 |
|---|---|---|
| `project_group_live_status_snapshot_20260626 = controlled` | `dirty_repo_count = 17` | 只说明 live dirty 集合已按 2026-06-26 重新采集，不说明 Git clean |
| `project_group_scheme_recognition_rules = controlled` | `scheme_recognition_dirty_count = 17` | 说明 17 仓会话入口规则和 34 个项目级方案继承声明已进入审查队列，不说明可提交 |
| `project_group_dirty_disposition_queue = controlled` | `post_scheme_queue_supersedes_runtime_count_only` | 旧 7 仓队列作为历史证据保留；新队列只更新当前 live dirty 处置口径 |
| `project_group_git_clean = partial` | `kds_diffcheck_blocker_count = 0` | 当前 KDS `git diff --check` 为 pass；项目群 Git clean 仍因 17 仓 dirty 保持 partial |
| 任一仓人工确认 | `repo_specific_action_allowed` | 只限该仓、该包、该动作；不能传导到其它仓或其它动作 |

## 4. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 读取 17 个 dirty 仓 live Git 状态，将方案识别规则写入后的 dirty 变化转成逐仓处置队列 |
| stop | 停止在 `authorization_boundary`，不执行清理、提交、推送、真实同步、生产动作或状态升级 |
| verify | 通过 `validate_project_group_dirty_disposition_queue_post_scheme_recognition_20260626.py`、`validate_project_group_scheme_recognition_rules_20260626.py`、总控板校验、文档门禁和 Git clean 门禁复核 |
| recover | 若队列与 live dirty 不一致，回滚本文和 validator，重新采集 17 仓 Git 状态 |
| debug | 当前主要阻塞是 review/owner/cleanup 授权边界，而不是文档识别规则缺失 |

## 5. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明任一项目方案识别规则已经完成提交验收。
- 不声明 KDS `wiki/log.md` whitespace cleanup 已执行或已修复。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或客户验收。
- 不声明真实 KDS API 已同步。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
