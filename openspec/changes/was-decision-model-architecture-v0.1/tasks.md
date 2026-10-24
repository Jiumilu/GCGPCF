---
doc_id: GPCF-DOC-CANDIDATE-WAS-DECISION-MODEL-ARCH-TASKS
title: WAS 决策模型体系架构实施任务（候选）
project: WAS
related_projects: [GPCF, XWAIL, WAME, Ontology]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/tasks.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/tasks.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 实施任务（候选；勾选仅表示本地证据，不代表验收/合并）

## Phase A 治理与兼容
- [x] 术语候选清单（14 对象/15 关系/7 状态族）
- [x] 跨项目影响矩阵（9 类对象）
- [x] 迁移说明（migration_required/additive_profile_first）
- [x] Ontology 准入包草案（candidate_draft_not_filed）
- [ ] Ontology 正式准入（需 GPCF admission_ref + 人工确认）
- [x] GPCF CP 骨架 → 完整 CP（本次）

## Phase B 契约与 Validator
- [x] DecisionProfile 候选 Schema（对象 `$defs`）
- [x] 正例 1 + 负例 15
- [x] Schema/Ontology-aware/Policy/Evidence Validator
- [x] `validate_all` 18 PASS（本地）
- [ ] 独立复核/兼容矩阵签署

## Phase C WAME no-write 运行时
- [x] 模型登记/版本状态机
- [x] 上下文预检
- [x] 适配器协议（注入 transport；fail-closed）
- [x] Assessment/授权回执/执行门禁/审计
- [x] 暂停→恢复/版本回退选版/Scorecard 骨架
- [ ] 真实外部 transport（需数据边界/凭据授权）
- [ ] 服务化接线/双钥匙恢复/事故流程

## Phase D 隔离试点准备
- [ ] 候选场景硬门槛评分表
- [ ] 回放/影子对照模板
- [ ] 零生产写回证据模板

## Phase E 受控服务化前置
- [ ] 许可证/商业权利证据包
- [ ] ServicePackage/SLA/责任矩阵
- [ ] 法律审查与专项人工确认

## 非声明
任务未派发实现；勾选为本地候选证据，不构成验收或状态提升。
