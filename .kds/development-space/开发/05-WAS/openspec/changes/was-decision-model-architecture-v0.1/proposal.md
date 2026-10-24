---
doc_id: GPCF-DOC-CANDIDATE-WAS-DECISION-MODEL-ARCH-PROPOSAL
title: WAS 决策模型体系架构与实施方案 v0.1 评审与候选契约准入
project: WAS
related_projects: [GPCF, XWAIL, WAME, Ontology, AaaS, SCaaS]
domain: openspec
status: draft
version: v0.1
owner: WAS
kds_space: 开发
kds_path: 开发/05-WAS/openspec/changes/was-decision-model-architecture-v0.1/proposal.md
source_path: openspec/changes/was-decision-model-architecture-v0.1/proposal.md
sync_direction: local_only
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# Change Proposal：WAS 决策模型体系架构与实施方案 v0.1

> 状态：draft（评审登记）；**不实现、不冻结、不做状态提升**。

## 1. 摘要

将“决策”纳入 WAS 一等语义域：WAS 定义决策体系与治理原则，Ontology 定义术语，XWAIL 定义机器契约，WAME负责模型登记/授权/门禁/审计，AaaS/SCaaS 服务化，Loop/Harness 形成证据闭环。首阶段采用 **additive_profile_first**，不修改 XWAIL Core 必填字段。

## 2. 背景与问题

- 现有 WAS Core/P0 契约未表达完整决策对象、状态族与授权分离；
- 模型建议易被误读为事实/授权/执行；
- 缺乏跨对象回放、证据闭环、许可证与商业权利门禁；
- 各项目虽有决策实践，但无统一契约与可验证边界。

## 3. 本变更范围

- 决策术语候选（14 对象/15 关系/7 状态族）与三世界映射；
- 可选 `DecisionProfile` 扩展包与决策对象候选 Schema/正负例/四类 Validator；
- WAME no-write 运行时（登记、预检、适配器、授权回执、审计、暂停恢复）；
- 隔离试点准备；
- 兼容、迁移与回滚说明。

## 4. 非目标

- 不新增资产维度或 Flow；
- 不把模型概率/置信度当作授权、事实或收益保证；
- 不接生产/客户真实数据；
- 不声明 accepted/integrated/production_ready/customer_accepted；
- 不替代 GPCF/WAME/KDS 权威职责。

## 5. 影响

| 对象 | 影响 | 方式 |
|---|---|---|
| WAS | 增加决策平面章节与治理原则 | 增量文档 |
| Ontology | 新增 `decision_terms` 候选组 | candidate-first，版本 bump 需单独批准 |
| XWAIL | 可选 `DecisionProfile` + 对象 Schema | additive_profile_first |
| WAME | 新增决策域运行时能力 | 独立分支 no-write |
| AaaS/SCaaS | 服务包增加许可/风险/责任字段 | 后续阶段 |
| 业务系统 | 只读引用决策/授权/执行记录 | 不写主账 |

## 6. 已有证据

- WAS WP-A：`feat/was-decision-wp-a`（`f337c61`）术语候选/影响矩阵/迁移说明/CP 草案；
- Ontology 准入包：`feat/was-decision-ontology-admission`（`d1ee7b4`）；
- WP-B 契约：`feat/was-decision-wp-b`（`46c6a38`），validate_all **18 PASS**、15 负例；
- WP-C 运行时：WAME `feat/wame-decision-runtime-wp-c`（`4f64781`），7 files/58 tests PASS。

## 7. 风险与回滚

- 风险：概念扩张、状态混写、模型越权、商业许可、数据边界；
- 控制：Profile-first、状态族分离、Validator 负例、WAME 门禁、许可证据门禁；
- 回滚：撤回本 CP 与 Profile；保留 Core 与历史记录；无数据迁移。

## 8. 验收门槛

- 本 CP `openspec validate` 通过；
- WP-A 术语/影响/迁移评审；
- WP-B 契约复核；
- WP-C no-write 验证；
- 人工确认范围/非目标。

## 9. 非声明

不构成契约发布、运行时上线、生产可用或状态提升。
