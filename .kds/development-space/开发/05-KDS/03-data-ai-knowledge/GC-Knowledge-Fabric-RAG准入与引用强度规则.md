---
doc_id: GPCF-DOC-C831F07BC3
title: GC-Knowledge Fabric RAG准入与引用强度规则
project: KDS
related_projects: [WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-RAG准入与引用强度规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-RAG准入与引用强度规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric RAG准入与引用强度规则

## 1. 准入状态

| 状态 | 含义 | 可用范围 |
|---|---|---|
| safe | 可强引用 | 可用于正式问答、指挥舱引用、SOP 依据 |
| limited | 有限引用 | 可用于提示、解释、背景说明，必须显示边界 |
| repair_required | 需补证 | 只能提示存在缺口，不能作为结论依据 |
| blocked | 禁止引用 | 不进入 RAG 召回 |
| sensitive_metadata_only | 仅元数据 | 只可引用编号、状态、摘要、权限和证据位置 |

## 2. 来源等级到准入的默认映射

| 来源等级 | 默认准入 | 条件 |
|---|---|---|
| T0 | safe | 系统正式记录、到账记录、合同、人工确认记录且证据完整 |
| T1 | safe 或 limited | 权威政策、标准网站，需保留版本、时间、适用范围 |
| T2 | limited 或 safe | 合作单位正式资料，需验收资料完整 |
| T3 | repair_required | 会议、电话、飞书、邮件、WIKI 记录，人工确认前不得强引用 |
| T4 | limited 或 repair_required | 网络搜索、行业文章、第三方报告，需注明非权威边界 |
| T5 | blocked | LLM 分析结果，只能作为候选，除非转为 source-backed 并确认 |

## 3. 引用强度

- 强引用：用于正式事实、SOP、业务解释和指挥舱指标，必须满足 `safe`。
- 弱引用：用于背景说明和风险提示，允许 `limited`。
- 缺口引用：用于指出证据缺失、字段缺失或待确认事项，允许 `repair_required`。
- 禁止引用：`blocked` 不进入召回；敏感原文不进入开放 RAG。

## 4. 响应要求

RAG 响应必须能返回 Domain、PoolRefs、ObjectType、TrustLevel、RAG Admission、Lifecycle、SourceRefs、EvidenceRefs、WAES Gate Status 和可共享边界。

## 5. AI 输出边界

AI 生成内容默认视为 T5。只有绑定来源、通过 WAES、进入 KWE 确认并形成 evidence 后，才能提升引用强度。
