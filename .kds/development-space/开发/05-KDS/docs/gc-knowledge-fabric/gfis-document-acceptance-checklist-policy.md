---
doc_id: GPCF-DOC-AFAB25CFB3
title: GC-Knowledge Fabric GFIS Document Acceptance Checklist 批量验收规则
project: KDS
related_projects: [GFIS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/gfis-document-acceptance-checklist-policy.md
source_path: docs/gc-knowledge-fabric/gfis-document-acceptance-checklist-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric GFIS Document Acceptance Checklist 批量验收规则

## 1. 定位

GFIS Document Acceptance Checklist 是 GFIS 文档验收助手的资料包级检查契约，用于把建设资料、订单资料、质量资料、发货/POD、金融凭证和 OEM 过渡资料批量转为候选事实、缺口、WAES 门禁建议和 KWE 确认包输入。

它不写 GFIS 主账，不写 KDS 正式 fact，不落库 WAES gate result，不创建真实 KWE work item，不确认收益、积分、额度、悬赏或委员会裁决。

## 2. Checklist 必检项

每个资料包至少检查：

| 项 | 要求 |
|---|---|
| `source_registered` | 有 SourceRecord 或受控来源编号 |
| `evidence_bound` | 有 evidence ref、hash 或受控原件指针 |
| `pool_refs_present` | 至少挂接一个 KDS 十一池 |
| `domain_scope_present` | 有 domain、project 或 supply-chain scope |
| `trust_level_assigned` | 有 T0-T5 来源等级 |
| `rag_admission_assessed` | 有 RAG 准入建议 |
| `sensitive_handling_assessed` | 敏感资料有 metadata-only 或受控原件处理 |
| `waes_gate_suggested` | 有 WAES gate 建议 |
| `kwe_workpack_suggested` | 需要人工/委员会时有 KWE confirmation workpack 建议 |
| `writeback_candidate_only` | 只允许生成写回候选，不允许正式写回 |

## 3. 资料包类型

| 类型 | 典型场景 | 默认关注 |
|---|---|---|
| `construction_package` | 葛化建设资料 | 产能池、装备池、数据池 |
| `order_package` | 预运营/正式订单资料 | 订单池、产能池、资金池、运力池 |
| `quality_package` | 质量验收资料 | 数据池、场景池、订单池 |
| `delivery_pod_package` | 发货/POD 资料 | 运力池、订单池、资金池 |
| `finance_package` | 到账、开票、合同敏感字段 | 资金池、数据池，默认 metadata-only |
| `oem_transition_package` | 现代精工 OEM 过渡资料 | 产能池、质量/交付责任边界 |

## 4. 批量结果

资料包验收结果只能为：

- `candidate_ready`：可生成候选事实或候选写回。
- `repair_required`：来源、证据、字段、敏感处理或池挂接缺失。
- `human_required`：需要业务负责人确认。
- `committee_required`：涉及收益、责任归因、重大争议或跨单位贡献争议。
- `metadata_only`：敏感资料仅允许元数据入库。
- `blocked`：T5 AI-only、无来源/证据、违规敏感原文或 WAES hard stop。

## 5. 硬边界

1. Checklist pass 不等于文档正式验收完成。
2. Batch pass 不等于 GFIS 写回完成。
3. Finance、POD、合同敏感条款、质量争议默认不得暴露 raw content。
4. T5 AI-only 只能生成缺口或候选，不能直接进入强引用或正式写回。
5. 存在缺口时必须生成 GapRecord 建议或 KWE workpack 建议。
6. Committee required 的资料包不得由 human-only 路径放行。

## 6. DKS-095 dry-run 验收

本轮 dry-run 必须证明：

- 至少覆盖订单、金融、质量/POD、OEM 过渡四类资料包。
- 每个资料包都有 checklist items、结果、缺口、门禁建议和 no-write 断言。
- 敏感资料不暴露 raw content。
- 所有正式写回、正式 fact、收益/积分确认、外部 API 写入计数为 0。
