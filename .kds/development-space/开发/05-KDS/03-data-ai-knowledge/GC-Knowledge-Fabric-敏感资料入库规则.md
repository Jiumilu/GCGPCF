---
doc_id: GPCF-DOC-A0469C3170
title: GC-Knowledge Fabric 敏感资料入库规则
project: KDS
related_projects: [WAES, KDS]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GC-Knowledge-Fabric-敏感资料入库规则.md
source_path: 03-data-ai-knowledge/GC-Knowledge-Fabric-敏感资料入库规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 敏感资料入库规则

## 1. 定位

敏感资料不直接进入开放知识库。KDS 只登记编号、状态、摘要、哈希、权限、证据链位置、受控原件位置和可引用范围。

## 2. 敏感资料范围

- 合同敏感条款。
- 金融凭证、到账凭证、开票资料。
- POD 原件、签收敏感信息。
- 质量争议、责任归因、处罚材料。
- 客户、供应商、个人身份和联系方式。
- 门禁、账号、密钥、TOKEN、内部权限配置。
- 未公开政策解释、商业报价和渠道佣金。

## 3. 入库模式

| 模式 | 用途 |
|---|---|
| metadata_only | 只登记元数据、摘要、状态、权限和证据位置 |
| redacted_copy | 脱敏副本可进入有限引用 |
| controlled_original | 原件保留在受控空间，只登记引用 |
| blocked | 禁止入库或禁止召回 |

## 4. 最小登记字段

- 对象编号。
- 来源编号。
- 证据编号。
- 哈希或受控原件位置。
- 权限范围。
- 可引用范围。
- WAES Sensitive Data Gate 结果。
- 脱敏责任人或确认人。

## 5. RAG 边界

敏感资料默认 `sensitive_metadata_only`。除非形成脱敏副本并通过 WAES，否则不得进入开放 RAG 原文召回。

## 6. 写回边界

敏感资料可以支撑候选写回，但正式写回必须由业务负责人确认，并保留 Harness evidence。
