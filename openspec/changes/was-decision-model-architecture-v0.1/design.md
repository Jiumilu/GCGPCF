---
doc_id: GPCF-DOC-CANDIDATE-WAS-DECISION-MODEL-ARCH-DESIGN
title: WAS 决策模型体系架构设计（候选）
project: WAS
related_projects: [GPCF, XWAIL, WAME, Ontology, AaaS]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/design.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/design.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 设计：WAS 决策模型体系架构（候选）

## 1. 纵向能力链

```text
业务事实与观测 → WAS（资产/维度/流/生命周期）
→ Ontology（术语/关系/约束）
→ XWAIL（机器契约/Profile/Schema/Validator）
→ Decision Runtime（模型选择/候选/评估）
→ WAME（登记/授权/发布/门禁/审计/回滚）
→ 业务系统执行 → Evidence/Outcome/Feedback → Loop/Harness
```

## 2. 横向决策平面

决策贯穿识别→规划→设计→构建→部署→运营→优化→退役；不替代各阶段责任主体，不设流水线末端单点裁判。

## 3. 语义模型

- 14 对象：DecisionQuestion/Case/Context/Objective/Alternative/Criterion/Constraint/Model/Assessment/Record/Authorization/Execution/Outcome/Feedback；
- 15 关系（subject→predicate→object）；
- 7 状态族独立（模型治理/评估可信/裁定/授权/执行/结果/项目群）；
- 三世界：记录载体 real，预测/推荐 evolution，核验 trusted。

## 4. 契约策略

- `DecisionProfile` 作为可选扩展包，不修改 Core 必填字段；
- Candidate envelope 已含对象 `$defs`；四层 Validator：schema / ontology-aware / policy / evidence；
- 正例 1、负例 15；`validate_all` 18 PASS（本地候选）。

## 5. WAME no-write 运行时

预检（模型状态/适用性/证据/数据边界/授权前置）→ 适配器（注入 transport；缺失 fail-closed）→ Assessment（五失败态 fail-closed）→ AuthorizationRecord（人工确认；概率不可授权）→ 执行门禁（默认 disabled；no-write sink）→ append-only 审计；暂停→恢复演练；版本回退选版。

## 6. 兼容与迁移

`migration_required / additive_profile_first / current candidate`；旧对象有效；禁止静默补写；回滚保留 0.2.0 引用。

## 7. 非声明

设计为候选；不构成 XWAIL 发布、WAME 生产运行时或 Go 判定。
