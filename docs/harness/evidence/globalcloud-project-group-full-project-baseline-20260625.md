---
doc_id: GPCF-DOC-PROJECT-GROUP-FULL-PROJECT-BASELINE-20260625
title: GlobalCloud 项目群全量项目真实状态基线 2026-06-25
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, XiaoC, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群全量项目真实状态基线 2026-06-25

## 1. 定位

本文补齐 `GPCF-FULL-PROJECT-BASELINE-001`，用于把项目群真实执行治理从核心链路扩展到 17 个项目仓库。

本文不替代项目群主方案、项目群实施方案、各项目唯一总体方案或各项目唯一实施方案。本文只登记当前可证明的真实状态、下一批可执行任务、门禁、回滚边界和禁止声明。

## 2. 采集范围

| 项 | 内容 |
|---|---|
| task_id | `GPCF-FULL-PROJECT-BASELINE-001` |
| baseline_date | 2026-06-25 |
| expected_project_count | 17 |
| checked_project_count | 17 |
| source_gate | `project_group_git_clean_gate.py` |
| source_evidence | `docs/harness/evidence/globalcloud-project-group-git-clean-20260625.md` |
| source_json | `docs/harness/evidence/globalcloud-project-group-git-clean-20260625.json` |
| validator | `tools/kds-sync/validate_project_group_full_project_baseline.py` |
| conclusion | `full_project_baseline = controlled` |

## 3. 全量项目基线矩阵

| # | 项目 | 当前真实状态 | 方案状态 | Git 状态 | 下一批任务 | 门禁/命令 | 回滚边界 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|
| 1 | GlobalCloud AAAS | `ready_for_review / local_dev_boundary` | `implementation_plan_exists` | `clean` | 将 AaaS ServicePackage/Metering/SLA/EvidenceRequirement 接入 WAES 注册、授权和发布边界 | `validate_aaas_service_runtime.py`、`validate_project_group_full_project_baseline.py` | 回滚最小 runtime 样例与验证脚本；失败时降回 `candidate` | 不声明真实计费、客户订阅、商业交付或 WAES 发布完成 |
| 2 | GlobalCloud Brain | `ready_for_review / authorization_boundary / ready_for_human_review` | `implementation_plan_exists` | `clean` | 等待人工 review 决策；如获授权，进入 accepted 前复核 KDS RAG 输入和本地 action 边界 | `validate_brain_review_handoff.py`、Brain harness validators | 停止本地 dev server；未确认时保持 `ready_for_review / authorization_boundary` | 不声明 accepted、integrated、production_ready 或客户验收 |
| 3 | WAS世界资产体系 | `semantic_foundation_candidate / not_accepted` | `main_plan_missing_in_scan` | `dirty / system_noise_only` | 将 WAS 术语、Profile 和 Ontology 映射继续作为 XWAIL 输入，不替代事实主存 | `project_group_git_clean_gate.py`、WAS validators | 不自动删除 `.DS_Store`；不自动升级 WAS 状态 | 不声明 KDS 事实主存、GFIS 运行层或 WAES 裁决完成 |
| 4 | GlobalCloud XiaoC | `baseline_controlled / no_current_execution_task` | `implementation_plan_exists` | `clean` | 进入下一轮时建立模型路由、AI 能力生产或 UI/Wrangler dry-run 任务包 | 项目本地 harness、后续专项 validator | 若专项门禁失败，保持 baseline；不改生产配置 | 不声明真实部署、真实模型路由生产可用或客户验收 |
| 5 | GlobalCloud WAES | `repair_required / authorization_required` | `implementation_plan_exists` | `clean` | 修复 lint/runtime 并恢复 `npm run check`，再接入 XWAIL/AaaS 注册发布门禁 | `npm run lint`、`npm run check`、`validate_waes_lint_runtime_repair_authorization.py` | 回滚 lint/runtime 修复文件；失败保持 `repair_required` | 不声明 WAES 治理运行闭环、发布、权限变更或验收 |
| 6 | GlobalCloud GPC | `partial_verified / browser_repaired / external_runtime_evidence_required` | `implementation_plan_exists` | `dirty / review_package_ready` | 补生产确认、外部联调和 GCFIS runtime surface 可达证据 | `npm run quality:100`、`npm run quality:ops`、`validate_gpc_evidence_browser_repair.py` | 回滚 README 索引、E2E 断言和边界文案；外部证据缺失时保持 partial | 不声明外部联调、真实交付或客户验收 |
| 7 | GlobalCloud Studio | `release_boundary_recheck_passed / local_release_review_boundary` | `implementation_plan_exists` | `dirty / evidence_index_repaired` | Studio harness、workflow release boundary、permissions hardening、test 和 build 已复核通过；本轮只补 Studio evidence-index 3 行 | `npm run harness:check`、`validate_studio_workflow_release_boundary.py`、`validate_studio_workflow_permissions_hardening.py`、`npm run test`、`npm run build`、`validate_studio_workflow_permissions_recheck.py` | 回滚 Studio evidence-index 3 行和 GPCF recheck evidence；不触发 release workflow | 不声明发布、GitHub release 写入、生产部署或客户验收 |
| 8 | GlobalCoud GPCF | `controlled / git_clean_partial / human_confirmation_request_prepared` | `implementation_plan_exists` | `dirty / governance_package_ready` | 维护总控板、核心台账、全量基线和人工确认请求；等待逐包授权 | `validate_project_group_full_project_baseline.py`、`loop_document_gate.py` | 回滚本轮治理文档和 validator；失败最高 `partial/rework` | 不声明项目群 Git 全量 clean、可提交、可推送或已验收 |
| 9 | GlobalCloud XWAIL | `ready_for_review / local_dev_boundary` | `implementation_plan_exists` | `clean` | 将最小 Validator/XAP 继续接入 WAES 和 AaaS 绑定门禁 | `validate_xwail_min_validator_runtime.py`、XWAIL scripts | 回滚最小 schema/profile/XAP 样例与脚本；失败降回 `candidate` | 不声明完整工具链、WAES 发布或 AaaS 绑定完成 |
| 10 | GlobalCloud GFIS | `partial_verified / repair_required` | `implementation_plan_exists` | `clean` | 获取真实 source-of-record 或等效正式确认，进入 pending_business_verification | `validate_gfis_was_source_record_submission_precheck.py`、GFIS quality gates | 不写入 runtime；不合格输入登记 rejected reason | 不声明真实 SOP E2E、生产写入、客户验收或 accepted |
| 11 | GlobalCloud MMC | `baseline_controlled / no_current_execution_task` | `implementation_plan_exists` | `clean` | 进入下一轮时建立治理模板复用 smoke 或下游 contract dry-run | MMC harness validators、后续专项 validator | 专项失败保持 baseline；不影响主链路状态 | 不声明下游项目已集成或客户验收 |
| 12 | GlobalCloud KDS | `owner_review_required / kds_report_hold_controlled` | `implementation_plan_exists` | `dirty / hold_business_report / sync_runs_untracked` | KDS RAG 修复已验证；资金追踪报告和 2026-06-25 sync-run 产物已建立 owner review 包，等待确认是否纳入、归档、返工或删除 | `validate_kds_rag_export_repair.py`、`validate_kds_brain_report_hold_review.py`、KDS evidence gates | 不自动纳入资金报告，不自动接收 sync-run 目录，不执行真实 KDS API 同步；未确认保持 hold | 不声明真实 KDS API 已同步、生产索引、真实交付、Brain/WAES 已消费或客户验收 |
| 13 | GlobalCloud XiaoG | `task_pack_ready / authorization_pack_ready` | `implementation_plan_exists` | `clean` | 已建立 live API、PKC 通知、WAES 审计写入和设备验证专项授权包；未获授权不触发真实动作 | `npm run harness:check`、`validate_xiaog_l4_readonly_audit_mock.py`、`validate_xiaog_live_api_auth_pack.py` | 回滚 XiaoG auth pack evidence、总控板和状态矩阵文本；未获授权不触发 live API/设备写入 | 不声明设备 OTA、真实外部 API、production_ready 或客户验收 |
| 14 | GlobalCloud PVAOS | `ready_for_review / local_release_gate_boundary` | `implementation_plan_exists` | `dirty / review_package_ready` | 等待 review；后续补远程 CI、PR、merge 或真实发布授权 | `npm run release:gate:local`、`validate_pvaos_release_gate_repair.py` | 回滚 `vitest.config.ts`、`package.json`、`package-lock.json` | 不声明远程 CI、PR、merge、生产发布或客户验收 |
| 15 | GlobalCloud SOP | `owner_review_required / scenario_candidate_controlled` | `implementation_plan_exists` | `dirty / owner_review_required` | 已建立武汉城市圈绿色供应链场景生成物 owner review 包；等待确认是否保留、返工、归档、删除噪声、入 KDS 或对外交付 | `validate_sop_assets.py`、`run_smoke_test.py`、`validate_sop_scenario_owner_review.py` | 回滚 SOP owner review evidence、总控板和状态矩阵文本；不自动纳入、不自动删除 output `.DS_Store` | 不声明场景方案已确认、已交付或客户验收 |
| 16 | GlobalCloud PKC | `baseline_controlled / no_current_execution_task` | `implementation_plan_exists` | `clean` | 进入下一轮时建立 PKC workflow dry-run 或 KDS/Brain 依赖验证 | PKC harness validators、后续专项 validator | 专项失败保持 baseline；不写入真实个人数据 | 不声明端到端用户闭环或客户验收 |
| 17 | GlobalCloud XGD | `baseline_controlled / no_current_execution_task` | `implementation_plan_exists` | `clean` | 进入下一轮时建立 bounded TICK loop dry-run 或 Brain UI/ACUI smoke | XGD harness validators、后续专项 validator | 专项失败保持 baseline；不扩大权限 | 不声明长程 Agent 生产可用或客户验收 |

## 4. 状态分组

| 分组 | 项目 | 控制结论 |
|---|---|---|
| `ready_for_review_or_owner_review` | GlobalCloud AAAS、GlobalCloud Brain、GlobalCloud XWAIL、GlobalCloud PVAOS、GlobalCloud KDS | 已有本地证据或审查包；KDS 资金报告仍需 owner review；所有项目仍需人工确认才能 accepted/integrated |
| `partial_or_repair` | GlobalCloud WAES、GlobalCloud GPC、GlobalCloud GFIS | 下一步优先真实修复或外部证据补齐 |
| `governance_controlled` | GlobalCoud GPCF、WAS世界资产体系 | 作为总控和语义源控制项目群，不替代事实主存与运行层 |
| `baseline_or_task_pack_controlled` | GlobalCloud XiaoC、GlobalCloud Studio、GlobalCloud MMC、GlobalCloud XiaoG、GlobalCloud SOP、GlobalCloud PKC、GlobalCloud XGD | 已纳入基线；Studio、MMC、PKC、XGD 已建立专项任务证据，XiaoG 已建立授权包证据，SOP 已建立 owner review 证据，XiaoC 已登记环境阻塞 |

## 5. 当前必须保留的边界

```text
full_project_baseline = controlled
project_group_git_clean = partial
accepted = false
integrated = false
production_ready = false
customer_accepted = false
review_allowed = false
stage_allowed = false
commit_allowed = false
push_allowed = false
```

当前不能声明：

- 不能声明项目群 17 仓 Git 全量 clean；
- 不能声明项目群可提交、可推送、可发布；
- 不能声明任何项目 accepted、integrated、production_ready 或 customer_accepted；
- 不能用 baseline_only 替代真实研发、真实运行、真实集成或真实交付；
- 不能把 WAS 语义基线、KDS 候选知识、mock、fixture、synthetic/dev-only 数据写成真实业务事实。

## 6. 下一步

| 优先级 | 下一步 | 说明 |
|---|---|---|
| P0 | `GFIS-REAL-SOR-001` | 真实 source-of-record 是 GFIS/GPC/PVAOS -> SCaaS 的主阻塞 |
| P0 | `WAES-LINT-RUNTIME-001` | WAES 是 XWAIL/AaaS 注册、授权、发布和裁决入口 |
| P1 | `GPC-EXTERNAL-RUNTIME-EVIDENCE-001` | GPC 需补生产确认、外部联调和 GCFIS runtime surface |
| P1 | `GPCF-HUMAN-CONFIRMATION-REQUEST-001` | review/stage/commit/push/delete 需要逐包人工确认 |
| P2 | `BASELINE-ONLY-PROJECT-TASK-PACKS` | Studio、MMC、PKC、XGD 已形成专项边界证据，XiaoG 已形成授权包证据，SOP 已形成 owner review 证据，XiaoC 已形成环境阻塞证据 |
