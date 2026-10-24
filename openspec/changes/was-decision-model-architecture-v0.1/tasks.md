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
- [x] DecisionProfile 候选 Schema（WP-B，2026-10-24）
- [x] 对象独立 Schema 7 + 兼容矩阵（WP-B 加固）
- [x] 正例/负例（WP-B：1 正例 + 15 负例；v0.3：1 正例 + **16 负例**）
- [x] Schema/Ontology-aware/Policy/Evidence Validator（v0.3：`validate_decision_v03.py`，8 类结构规则含 `R-CONFIRMATION`）
- [x] `validate_all` 56 PASS（本地，含决策校验器）
- [x] **v0.3.0 契约冻结**（11 对象 + common + manifest；content_hash `1640dcd0…`；独立复核通过 A .868；冻结确认 A .616；2026-10-24）
- [x] 映射矩阵/迁移测试集（Gen1 v0.2→v0.3；对账 mapped 107 / derived 72 / unmapped 0；迁移 bundle VALID）
- [x] 独立复核/冻结签署（复核人=老卢，本人兼任，双角色已声明；仍在 GPCF 治理侧留下评审待办）
- [x] XWAIL 本地发布（`feat/xwail-decision-schemas-v03` @ `3c934d5`；13 文件哈希复现；43 PASS；bundle VALID；**未 push/未合并**）
- [ ] GPCF 门禁清障（37 外部 hard failures，非本 CP 可修）
- [ ] CP 评审/批准/合并（需 GPCF owner + 门禁清障）

## Phase C WAME no-write 运行时
- [x] 模型登记/版本状态机
- [x] 上下文预检
- [x] 适配器协议（注入 transport；fail-closed）
- [x] Assessment/授权回执/执行门禁/审计
- [x] 暂停→恢复/版本回退选版/Scorecard 骨架
- [x] WAME 决策运行时 v0.3 适配性复核（只读：9/9 映射对象缺必填；枚举 5/9 不一致；世界层/contentHash 全缺）
- [x] WAME v0.3 适配规格（candidate：mapper/枚举收敛/回执映射/BLOCKED 清单/Q-W3 输入扩展草案/Q-W6…W8 开放问题）
- [ ] 真实外部 transport（需数据边界/凭据授权）
- [ ] 服务化接线/双钥匙恢复/事故流程
- [ ] WAME 跨仓实施（Q-W3/Q-W7 输入扩展+mapper；需 WAME owner 授权）

## Phase D/E 与 v0.3.1（2026-10-25 更新）
- [x] 候选场景硬门槛评分表（docs/decision/pilot-candidate-scenarios-v0.1.md）
- [x] 回放/影子对照模板（pilot-c-evidence-templates / runbooks）
- [x] 零生产写回证据模板（pilot-evidence-templates-v0.1.md）
- [x] 许可证/商业权利证据包模板（serviceization-license-evidence-v0.1.md）
- [x] ServicePackage/SLA/责任矩阵模板（service-package-template-v0.1.md）
- [x] 法律审查清单模板（serviceization-legal-review-checklist-v0.1.md）
- [x] v0.3.1 契约冻结（content_hash c243f6aa…；复核通过 A .740；冻结确认 A .927）
- [x] XWAIL v0.3.1 发布（d9647e7；PR #4 已合并 main bfd7595）
- [x] WAME v0.3.1 capability mapper（1975b96；main 合并 1b227b2）

## Phase D 隔离试点准备
- [ ] 候选场景硬门槛评分表
- [ ] 回放/影子对照模板
- [ ] 零生产写回证据模板

## Phase E 受控服务化前置
- [ ] 许可证/商业权利证据包
- [ ] ServicePackage/SLA/责任矩阵
- [ ] 法律审查与专项人工确认

## 非声明
任务勾选为本地候选证据（含 WAS 冻结/发布与只读复核进展），**不构成验收、合并或状态提升**；外部 hard failures 不由本 CP 修复；v0.3 FROZEN/发布 ≠ 生产可用。
