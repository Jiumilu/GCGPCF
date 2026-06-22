---
doc_id: GPCF-DOC-6744A9045B
title: GPCF-KDS-DKS-004 葛化订单运行母版字段与单据映射 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-004.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-004.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-004 葛化订单运行母版字段与单据映射 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

上一轮 `GPCF-KDS-DKS-003` 已形成完整实施提示词，并建议下一轮进入葛化订单运行母版字段/单据映射专项。

本轮输入文档包括：

1. `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统实施治理方案.md`
2. `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统对象字段与11池映射清单.md`
3. `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统完整实施提示词.md`
4. `08-evidence-samples/GFIS/modern-jinggong-training-analysis.md`
5. `08-evidence-samples/GFIS/docs/17-gcfis-functional-specification.md`
6. `08-evidence-samples/GFIS/docs/07-p0-sop-to-erpnext-doctype-mapping.md`
7. `08-evidence-samples/GFIS/docs/20-gcfis-core-flow-closure-matrix.md`
8. `08-evidence-samples/GFIS/docs/21-gcfis-risk-ledger-and-uat-plan.md`

Loop 编排脚本显示当前 KDS token 和文档门禁可用，但全仓 Git/运营门禁仍受既有 GFIS repair_required 与无关 diff-check 问题限制。本轮仅做受控文档推进。

## 2. 动作

本轮执行动作：

1. 建立受控专项清单：
   `03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md`
2. 将预运营阶段拆成 DemandSourceRecord、AISuggestion、PreOperationOrder、OEMProductionEvidencePackage、QualityEvidenceGate、ShipmentAndPODGate、FinanceEvidenceGate 和 OperatingOrderConversionDecision。
3. 将 P0 SOP 映射到 GFIS/GCFIS 标准单据、自定义对象、GPC/PVAOS 客户协同引用、WAES/KDS 门禁。
4. 建立辽宁远航链路证据缺口清单。
5. 明确本轮不触发业务主账写入、不确认真实证据、不升级验收状态。

## 3. 输出

本轮产出：

| 产物 | 路径 | 说明 |
|---|---|---|
| 葛化订单运行母版字段与单据映射专项清单 | `03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md` | 定义预运营期订单主链路、字段/单据映射、P0 SOP 对应关系、辽宁远航证据缺口和 DKS-005 建议 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-004.md` | 记录本轮五段式治理微循环 |

## 4. 检查

本轮检查口径：

| 检查项 | 结果 | 说明 |
|---|---|---|
| 业务事实边界 | pass | 本轮只新增文档映射，不写 GFIS/GPC/PVAOS 主账 |
| AI 越权边界 | pass | AI 建议只作为候选，不确认订单、质量、POD、金融或收益事实 |
| GFIS 主体边界 | pass | GFIS 运行层是工厂事实主体；Demo 不作为 SOP 验收主体 |
| OEM 责任边界 | pass | 现代精工 OEM 必须与葛化目标工厂区分事实责任 |
| GPC/POD 边界 | pass | POD / 客户签收主责需与 GPC 协同边界对齐 |
| 金融边界 | pass | 金融凭证包保持建议和 `L4_blocked`，不确认资金事实 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |
| 全仓门禁 | partial | Loop 编排脚本显示全仓 Git/运营门禁仍有既有 blocked/rework 信号，本轮不处理无关债务 |

## 5. 反馈

本轮结论：

1. 葛化订单运行母版已有字段/单据映射专项清单。
2. 辽宁远航链路已形成 8 项证据缺口。
3. 现代精工 OEM 过渡资料已被纳入责任划分和证据包候选。
4. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-005：
辽宁远航链路证据缺口请求包与知识悬赏草案，围绕客户确认函、23个样箱测试反馈、现代精工 OEM 生产事实、质量报告、POD、金融凭证和转量产批准建立 KGR/KGB/KGS/BTS 字段模板。
```

待用户回答：

1. 辽宁远航需求最早来源是电话、会议、邮件、聊天记录还是第三方介绍？
2. 23 个样箱是否已有编号、测试反馈、签收记录或客户意见汇总？
3. 现代精工 OEM 过渡资料中哪些可共享，哪些必须限制在 `DSR-L2 / DSR-L3`？
4. POD 和金融凭证由谁保管，是否可先建立脱敏索引？
5. 辽宁远航是否已有转量产口头或书面批准？
