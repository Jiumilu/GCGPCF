---
doc_id: GPCF-DOC-PROJECT-GROUP-DIRTY-DISPOSITION-QUEUE-20260625
title: GlobalCloud 项目群 Dirty 仓逐仓处置队列 2026-06-25
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-dirty-disposition-queue-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Dirty 仓逐仓处置队列 2026-06-25

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-DIRTY-DISPOSITION-QUEUE-001` |
| 前置证据 | `globalcloud-project-group-git-clean-20260625.md`、`globalcloud-project-group-dirty-classification-20260625.md`、`globalcloud-project-group-review-packages-20260625.md`、`globalcloud-project-group-authorization-routing-20260625.md` |
| 当前结论 | `project_group_dirty_disposition_queue = controlled` |
| 状态候选 | `dirty_disposition_queue_ready` |
| dirty_repo_count | `7` |
| review_candidate_count | `4` |
| owner_decision_count | `2` |
| noise_decision_count | `1` |
| review_allowed | `false` |
| stage_allowed | `false` |
| commit_allowed | `false` |
| push_allowed | `false` |
| delete_allowed | `false` |
| accepted | `false` |
| integrated | `false` |
| production_ready | `false` |
| customer_accepted | `false` |

本文只把 7 个 dirty 仓从“发现/分组”推进到“逐仓处置队列”。它不执行删除、清理、stage、commit、push、merge、真实 KDS API 同步、生产部署或客户验收。

## 2. 逐仓处置队列

| 队列 ID | 仓库 | live dirty 类型 | 当前处置类型 | 下一步动作 | 必跑命令 | 证据 | 门禁 | 回滚/降级 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|---|---|
| `DISP-WAS-SYSTEM-NOISE-20260625` | `WAS世界资产体系` | `.DS_Store` untracked | `noise_decision_required` | 确认删除 `.DS_Store` 或补充忽略规则；未确认前保持 hold | `git status --short --untracked-files=all`、`git diff --check` | `HOLD-WAS-SYSTEM-NOISE-20260625`、本队列 | Git clean gate、pollution gate | 不删除；若误删业务文件立即恢复并降级 `partial/rework` | 是，需要确认 `allow_delete_ds_store` 或 `allow_gitignore_update` | 不声明 WAS clean、不自动删除 `.DS_Store` |
| `DISP-GPC-EVIDENCE-BROWSER-20260625` | `GlobalCloud GPC` | README、外部证据登记、E2E 断言修改 | `review_candidate` | 进入 GPC evidence/browser review；未补外部联调前保持 partial | `npm run quality:repo`、`npm run test:e2e`、`python3 tools/kds-sync/validate_gpc_evidence_browser_repair.py` | `gpc-evidence-browser-repair-20260625.md`、`PKG-GPC-EVIDENCE-BROWSER-20260625` | GPC evidence gate、Git diff check、authorization route | 回滚 README、`docs/26-*`、E2E 断言；外部证据缺失则保持 partial | 是，需要确认 review/stage/commit/push | 不声明外部联调完成、生产确认完成或客户验收 |
| `DISP-STUDIO-EVIDENCE-INDEX-20260625` | `GlobalCloud Studio` | `docs/harness/evidence/evidence-index.md` 修改 | `review_candidate` | 进入 Studio evidence-index review；不触发 release workflow | `npm run harness:check`、`validate_studio_workflow_release_boundary.py`、`validate_studio_workflow_permissions_hardening.py`、`validate_studio_workflow_permissions_recheck.py` | `studio-workflow-permissions-recheck-20260625.md` | Studio harness gate、release boundary gate、authorization route | 回滚 evidence-index 3 行和 GPCF recheck evidence；失败保持 `local_release_review_boundary` | 是，需要确认 review/stage/commit/push | 不声明 Studio 已发布、GitHub release 已写入或生产部署完成 |
| `DISP-GPCF-GOVERNANCE-EVIDENCE-20260625` | `GlobalCoud GPCF` | 总控文档、证据、validator、`.kds` 本地镜像聚合修改 | `review_candidate_with_mirror_boundary` | 拆成治理包与 KDS 本地镜像包审查；镜像包不得解释为真实 KDS API 同步 | `python3 tools/kds-sync/validate_project_group_real_execution_governance_board.py`、`python3 tools/kds-sync/loop_document_gate.py`、`python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --allow-non-pass-exit-zero` | `PKG-GPCF-GOVERNANCE-EVIDENCE-20260625`、`PKG-GPCF-KDS-MIRROR-20260625`、本队列 | governance board gate、document gate、Git clean gate | 回滚本轮新增治理文档/validator；镜像异常时降级 `partial/rework` | 是，需要确认治理包和镜像包是否进入 review/stage/commit/push | 不声明项目群 Git 全量 clean、真实 KDS API 已同步、可提交或可推送 |
| `DISP-KDS-FUNDING-SYNC-RUNS-20260625` | `GlobalCloud KDS` | 资金追踪报告修改，sync-run 目录未跟踪 | `owner_decision_required` | 业务 owner 确认资金报告口径；KDS owner 确认 sync-run 是否归档/纳入/删除 | `git status --short --untracked-files=all`、`python3 tools/kds-sync/validate_kds_brain_report_hold_review.py`、`python3 tools/kds-sync/validate_kds_token.py` | `kds-brain-report-hold-review-20260625.md`、`HOLD-KDS-FUNDING-REPORT-20260625` | KDS hold review gate、KDS token gate、authorization route | 未确认保持 hold；若口径错误，回滚资金报告或另建 correction 包 | 是，需要 business owner 与 KDS owner 确认 | 不声明资金报告已业务确认、真实 KDS API 已同步、Brain 已正式摄取 |
| `DISP-PVAOS-RELEASE-GATE-20260625` | `GlobalCloud PVAOS` | `package.json`、`package-lock.json`、`vitest.config.ts` 修改 | `review_candidate` | 进入 PVAOS release gate review；远程 CI/PR/merge/发布另行授权 | `npm run release:gate:local`、`python3 tools/kds-sync/validate_pvaos_release_gate_repair.py`、`python3 tools/kds-sync/validate_pvaos_release_review.py` | `pvaos-release-gate-repair-20260625.md`、`pvaos-release-review-20260625.md`、`PKG-PVAOS-RELEASE-GATE-20260625` | PVAOS local release gate、review gate、authorization route | 回滚 `vitest.config.ts`、`package.json`、`package-lock.json`；失败保持 repair/review 边界 | 是，需要确认 review/stage/commit/push | 不声明远程 CI、PR、merge、生产发布或客户验收 |
| `DISP-SOP-WUHAN-SCENARIO-20260625` | `GlobalCloud SOP` | 索引、场景文档、PDF/MD 输出和 `.DS_Store` | `owner_decision_required` | 方案 owner 确认场景文档是否保留/返工/归档/入 KDS/对外；噪声删除另行确认 | `python3 scripts/validate_sop_assets.py`、`python3 scripts/run_smoke_test.py`、`python3 tools/kds-sync/validate_sop_scenario_owner_review.py` | `sop-scenario-owner-review-20260625.md`、`HOLD-SOP-WUHAN-SCENARIO-20260625` | SOP owner review gate、asset smoke gate、authorization route | 未确认保持 owner review；若不保留，回滚生成物或另建 archive/delete 包 | 是，需要 scenario owner 确认 | 不声明场景方案已确认、已交付、KDS 事实入库或客户验收 |

## 3. 状态传导

| 输入 | 输出 | 限制 |
|---|---|---|
| `project_group_git_clean = partial` | `dirty_disposition_queue_ready` | 只说明 7 个 dirty 仓已有逐仓处置路径，不说明 Git clean |
| `project_group_review_packages = controlled` | `review_candidate_count = 4` | 只可进入 review 候选，不授权 stage/commit/push |
| `owner_review_required` | `owner_decision_count = 2` | KDS 与 SOP 必须 owner 决策后才能改变事实状态 |
| `noise_decision_required` | `noise_decision_count = 1` | WAS `.DS_Store` 删除或忽略规则必须人工确认 |
| 任一包人工确认 | `package_specific_action_allowed` | 只限该包、该仓、该动作；不能传导到其他包 |

## 4. LOOP 运行控制闭环

| 方向 | 本轮定义 |
|---|---|
| run | 读取 7 个 dirty 仓 live Git 状态，形成逐仓处置队列 |
| stop | 停止在 `authorization_boundary`，不执行清理、提交、推送、真实同步或状态升级 |
| verify | 通过 `validate_project_group_dirty_disposition_queue.py`、总控板校验、文档门禁和 Git clean 门禁复核 |
| recover | 若队列与 live dirty 不一致，回滚本文和 validator，重新采集 Git 状态 |
| debug | 当前主要阻塞不是技术不可执行，而是人工确认边界：review 包、owner decision 和 noise decision 尚未逐项确认 |

## 5. 禁止升级

- 不声明项目群 Git 全量 clean。
- 不声明任一 dirty 仓可 stage、commit 或 push。
- 不声明 KDS 资金报告已业务确认。
- 不声明 SOP 场景方案已确认、已交付或客户验收。
- 不声明 GPC 外部联调、PVAOS 远程 CI、Studio release 或生产部署完成。
- 不声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
