---
doc_id: GPCF-DOC-PROJECT-GROUP-DEPENDENCY-EXECUTION-MATRIX-20260625
title: GlobalCloud 项目群依赖执行矩阵 2026-06-25
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-dependency-execution-matrix-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群依赖执行矩阵 2026-06-25

## 1. 定位

本文补齐 `GPCF-DEPENDENCY-MATRIX-001`，把项目群依赖从总控板中的链路概览，进一步落成可执行、可校验、可传导、可回滚的依赖边矩阵。

本文不执行依赖任务，不替代项目实施方案，不授予 stage、commit、push、deploy、release、accepted、integrated 或客户验收权限。

## 2. 控制结论

```text
dependency_execution_matrix = controlled
dependency_edge_count = 12
project_group_git_clean = partial
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 3. 依赖边执行矩阵

| # | dependency_edge | 上游项目 | 下游项目 | 当前状态 | 上游证据 | 下游任务 | 传导门禁 | 阻塞/风险 | 回滚/降级 | 人工确认 | 禁止声明 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `WAES -> XWAIL` | GlobalCloud WAES | GlobalCloud XWAIL | `blocked_by_waes_repair_required` | `docs/harness/WAES/evidence/waes-lint-runtime-repair-authorization-20260625.md` | `XWAIL-WAES-AAAS-CONTRACT-PRECHECK-001` | WAES quality gate、XWAIL validator gate、GPCF dependency matrix gate | WAES lint/runtime 未修复时，XWAIL 只能保持 local dev boundary | 若 WAES gate 失败，XWAIL 不升级 integration_precheck，保持 `ready_for_review / local_dev_boundary` | WAES 源码修复需授权 | 不声明 WAES 发布或 XWAIL 已接入 WAES |
| 2 | `XWAIL -> AaaS` | GlobalCloud XWAIL | GlobalCloud AAAS | `integration_precheck_candidate` | `docs/harness/AaaS/evidence/aaas-waes-binding-precheck-20260625.md` | `AAAS-WAES-BINDING-PRECHECK-001` | XWAIL validator gate、AaaS service runtime gate、contract precheck gate、binding precheck gate | 只能证明最小契约输入和本地 precheck，不证明商业服务绑定 | AaaS precheck 失败时保持 `ready_for_review / local_dev_boundary` | 否，除非真实订阅/计费 | 不声明 AaaS 客户可订阅或真实计费 |
| 3 | `WAES -> AaaS` | GlobalCloud WAES | GlobalCloud AAAS | `integration_precheck_candidate / authorization_boundary` | `docs/harness/AaaS/evidence/aaas-waes-binding-precheck-20260625.md`、`docs/harness/WAES/evidence/waes-real-runtime-baseline-20260624.md` | `AAAS-WAES-BINDING-PRECHECK-001` | contract precheck gate、WAES publication gate、AaaS binding gate、human confirmation gate | WAES 未授权/未发布时，AaaS 不得声明发布绑定 | WAES 未通过时，AaaS 维持 local dev boundary | 是，涉及 WAES 发布或服务上架 | 不声明 WAES 发布、AaaS 上架、客户订阅 |
| 4 | `KDS -> Brain` | GlobalCloud KDS | GlobalCloud Brain | `ready_for_review_to_human_review` | `docs/harness/KDS/evidence/kds-rag-export-repair-20260625.md` | `BRAIN-HUMAN-REVIEW-DECISION-001` | KDS RAG export gate、Brain review handoff gate、human review gate | KDS dirty 中存在业务报告 hold，不能混入 Brain accepted 判定 | 人工未确认时 Brain 保持 `ready_for_review / authorization_boundary` | 是，Brain accepted/integrated 前 | 不声明 Brain accepted、integrated、production_ready |
| 5 | `GFIS -> GPC` | GlobalCloud GFIS | GlobalCloud GPC | `blocked_by_real_sor_missing` | `docs/harness/GFIS/evidence/gfis-real-runtime-baseline-20260624.md` | `GPC-EXTERNAL-RUNTIME-EVIDENCE-001` | GFIS source-record gate、GPC external runtime gate | GFIS 真实 source-of-record 缺失会阻断 GPC 真实业务链路证明 | GFIS 输入缺失时，GPC 只能保持 external_runtime_evidence_required | 是，真实业务 owner/外部联调需确认 | 不声明真实业务闭环或外部联调完成 |
| 6 | `GPC -> PVAOS` | GlobalCloud GPC | GlobalCloud PVAOS | `partial_to_review_candidate` | `docs/harness/PVAOS/evidence/pvaos-release-review-20260625.md` | `PVAOS-RELEASE-REVIEW-001` | GPC runtime evidence gate、PVAOS release local gate、release review gate | PVAOS review candidate 不等于 GPC 外部运行证据齐备 | GPC 外部证据缺失时，PVAOS 不升级生产发布或 SCaaS 完整交付 | 是，远程 CI/PR/merge/发布前 | 不声明生产发布或客户验收 |
| 7 | `PVAOS -> SCaaS` | GlobalCloud PVAOS | SCaaS / GlobalCloud 绿色供应链体系 | `review_candidate` | `docs/harness/PVAOS/evidence/pvaos-release-review-20260625.md` | `PVAOS-RELEASE-REVIEW-001` | PVAOS release gate、release review gate、SCaaS scenario evidence gate | 本地 release review 不证明客户环境或生产发布 | 未授权发布时保持 local release boundary | 是，发布/客户验收前 | 不声明 SCaaS 场景已交付或客户验收 |
| 8 | `GFIS/GPC/PVAOS -> SCaaS` | GFIS/GPC/PVAOS | SCaaS / GlobalCloud 绿色供应链体系 | `partial_verified_external_evidence_required` | GFIS/GPC/PVAOS evidence baseline | `GFIS-REAL-SOR-001`、`GPC-EXTERNAL-RUNTIME-EVIDENCE-001`、`PVAOS-RELEASE-REVIEW-001` | SCaaS scenario gate、source-record gate、external runtime gate、release review gate | 任一主链路证据缺失，都不能声明绿色供应链场景完整交付 | 任何一项失败时 SCaaS 保持 partial/rework | 是，真实客户/场景 owner 验收前 | 不声明 GlobalCloud 绿色供应链体系客户验收 |
| 9 | `WAS -> Ontology -> XWAIL` | WAS世界资产体系 | GlobalCloud XWAIL | `xwail_mapping_candidate` | `docs/harness/evidence/was-xwail-ontology-mapping-20260625.md` | `WAS-XWAIL-ONTOLOGY-MAPPING-001` | WAS semantic gate、Ontology mapping gate、XWAIL validator precheck、XAP check gate、mapping evidence gate | WAS 语义不能替代 KDS 事实主存、GFIS 运行层或 WAES 裁决；映射候选不等于 WAES 发布或 AaaS 绑定 | 映射冲突时保持 semantic candidate 并登记 rework | 是，若改变主术语/总体架构 | 不声明语义映射等于真实业务事实，不声明 WAES 发布或 AaaS 绑定 |
| 10 | `GPCF -> all projects` | GlobalCoud GPCF | 17 项目 | `controlled_git_partial` | `docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md` | `GPCF-AUTHORIZATION-PACKAGE-ROUTING-001` | GPCF board gate、human confirmation gate、Git clean gate、Loop document gate | Git 仍 partial，未授权前不得进入 stage/commit/push | 任一门禁失败则保持 `partial/rework` | 是，review/stage/commit/push/delete 前 | 不声明项目群 Git clean、可提交、可推送 |
| 11 | `Studio -> GPCF/WAES` | GlobalCloud Studio | GPCF/WAES | `workflow_release_boundary_review_required` | `docs/harness/evidence/globalcloud-project-group-full-project-baseline-20260625.md` | `STUDIO-WORKFLOW-PERMISSIONS-001` | Studio workflow boundary gate、GPCF release governance gate | release-write workflow 未补显式权限前，不得作为发布链路依据 | workflow gate 失败时保持 review_required_before_commit | 是，触发 release/GitHub 写入前 | 不声明 release、部署或 GitHub release 写入完成 |
| 12 | `PKC/XGD/XiaoG/XiaoC/MMC/SOP -> KDS/Brain/WAES` | PKC/XGD/XiaoG/XiaoC/MMC/SOP | KDS/Brain/WAES | `baseline_only_task_pack_ready` | `docs/harness/evidence/globalcloud-project-group-next-executable-task-packs-20260625.md` | Wave 3 baseline-only 专项任务包 | task-pack gate、project local harness gate、human confirmation gate where required | baseline-only 不等于真实运行；部分任务需要 live API、设备、scenario owner 或真实数据授权 | 未授权或本地 gate 失败时保持 baseline_controlled | 视任务而定 | 不声明生产可用、真实外部 API、客户验收 |

## 4. 状态传导规则

| 传导场景 | 规则 |
|---|---|
| 上游从 `repair_required` 到 `ready_for_review` | 下游只允许进入 `integration_precheck_candidate`，不得直接进入 `accepted` 或 `integrated` |
| 上游仍为 `partial_verified` | 下游必须保留对应边界，禁止声明完整集成或客户验收 |
| 上游需要人工确认 | 下游状态不得超过 `ready_for_review / authorization_boundary` |
| 依赖边证据冲突 | 上下游均标记 `dependency_review_required`，并回写总控板和核心台账 |
| 任一依赖边涉及生产、权限、部署、真实外部 API | 必须另行人工确认，本文不授予执行权限 |

## 5. 下一步

| 优先级 | 依赖边 | 下一步 |
|---|---|---|
| P0 | `GFIS -> GPC`、`GFIS/GPC/PVAOS -> SCaaS` | 获取真实 source-of-record 与外部运行证据 |
| P0 | `WAES -> XWAIL`、`WAES -> AaaS` | 等待 WAES lint/runtime 修复授权并复跑 WAES 门禁 |
| P1 | `KDS -> Brain` | 等待 Brain 人工审查决策，不自动 accepted |
| P1 | `WAS -> Ontology -> XWAIL` | 建立 WAS/Ontology 到 XWAIL 的映射 evidence |
| P1 | `GPCF -> all projects` | 等待逐包 review/stage/commit/push/delete 授权 |
