---
doc_id: GPCF-L4-MCL-PROJECT-MATRIX
title: L4 Project Role Verification Matrix
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/minimum-closed-loop/project-role-verification-matrix.md
source_path: docs/harness/minimum-closed-loop/project-role-verification-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-13
supersedes: []
superseded_by: []
---

# L4 Project Role Verification Matrix

| 项目 | 职责 | 输入 | 输出 | 验证方式 | 项目级 evidence | 项目群 evidence |
|---|---|---|---|---|---|---|
| GFIS | 配方研发、样品打样、样品检测、工厂订单、工单、质量、库存、批次、发货事实 | ProductionRelease、样品规格、工厂执行规则 | SampleWorkOrder、FactoryOrder、WorkOrder、QualityInspection、Shipment | L4-008 只读样本/API dry-run；L3 validator baseline | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GFIS/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| GPC | 平台订单、样品申请、客户签样、转量产门禁、签收/POD、外部异常 | PVAOS 组织/伙伴、GFIS 样品/工厂回执、WAES 状态门 | PlatformOrder、SampleRequest、SampleApproval、ProductionRelease、POD、ExternalException | L4-007 contract/dry-run；`npm run check:js` baseline | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud GPC/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| PVAOS | 租户、组织、伙伴、项目空间、用户权限、门户入口 | 项目初始化需求、组织/伙伴资料 | Tenant、Organization、Partner、ProjectSpace、PermissionBoundary | L4-006 organization/permission baseline dry-run | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PVAOS/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| WAES | 治理规则、状态门禁、证据确证、审计、风险阻断 | 全项目事件、样品签样、转量产、异常和审计请求 | GateDecision、EvidenceRecord、AuditEvent、RiskBlock | L4-009 evidence gate dry-run；Vitest baseline | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAES/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| KDS | 知识主存、SOP、样品资料、签样资料、案例沉淀、引用回指 | 样品规格、签样资料、SOP、evidence refs | KnowledgeEntry、EvidenceBacklink、CaseRecord | L4-003 index/backlink dry-run；KDS token safety gate | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| Brain | 知识检索、SOP 呈现、案例匹配、复盘视图 | KDS KnowledgeEntry、CaseRecord、SOP | RetrievalResult、ReviewView、CaseMatch | L4-004 SOP/case/sample retrieval smoke | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| PKC | 个人任务、通知、审批待办、状态同步 | SampleApproval task、GateDecision、Exception notice | PersonalTask、Notification、TodoState | L4-005 task/notification mock | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud PKC/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| MMC | 治理模板、配置基线、策略边界、字段标准 | L4 object contracts、WAES rules、GPC/GFIS field boundaries | PolicyTemplate、FieldStandard、SampleGatePolicy | L4-002 config/policy validator | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| XiaoC | 蚁后，任务拆解、模型路由、Agent 调度、结果汇总 | 最小闭环业务链、object contracts | TaskBreakdown、ModelRoute、AgentDispatchPlan | L4-010 model routing dry-run | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoC/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| XGD | 大象，重分析、复杂判断、瓶颈推演、风险建议 | SampleApproval、ProductionRelease、capacity/risk facts | RiskAnalysis、BottleneckProjection、RootCauseHypothesis | L4-011 analysis sample | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| XiaoG | 蚂蚁，只读查询、跨系统 API dry-run、WAES 审计写入 mock | SampleRequest id、WorkOrder id、WAES audit target | ReadOnlyQueryResult、AuditWriteMock | L4-012 readonly/API dry-run and audit mock | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/docs/harness` | `docs/harness/minimum-closed-loop/evidence-index.md` |
| GPCF | 项目群治理总控、Loop 编排、文档控制、KDS 映射、evidence 收口 | 12 项目 evidence、validator output、Git gate | L4 score matrix、blocker list、evidence index、next round plan | L4-001 validator and document governance gates | `docs/harness/minimum-closed-loop` | `docs/harness/evidence/l4_minimum_loop_assessment.json` |

## Coverage Rules

- 每个项目必须有职责、输入、输出、验证方式和 evidence。
- 低成熟项目可以用契约、mock、dry-run 或占位验证参与，但不得缺席。
- 项目级 evidence 证明项目参与闭环；项目群 evidence 证明 GPCF 已收口。

