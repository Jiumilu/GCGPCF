---
doc_id: GPCF-DOC-F87EFE5DF7
title: AgentUsedKnowledge 调用证据与越权读取规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, MMC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/agent-used-knowledge-policy.md
source_path: docs/gc-knowledge-fabric/agent-used-knowledge-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# AgentUsedKnowledge 调用证据与越权读取规则

## 1. 定位

AgentUsedKnowledge 是 MMC 对 AI、Agent、Connector 和 MCP 能力调用的治理证据契约。

它记录：

- 谁发起调用。
- 调用了什么能力。
- 读取了哪些 KDS 对象、来源和 evidence。
- 使用了什么检索 scope、domain、pool 和 ACL。
- 生成了哪些候选输出。
- 是否触发 WAES 门禁。
- 是否存在越权读取、低可信强引用、敏感原文暴露或绕过 KWE promotion。

本契约只记录调用证据和门禁判断，不授予 Agent 事实确认权、业务写回权、收益分配权、积分确认权或委员会裁决权。

## 2. 标准链路

```text
Agent / Connector 请求
→ MMC 记录 invocation
→ KDS 检索候选知识
→ ACL / Domain / Pool / RAG admission 过滤
→ WAES 识别 overread / low-trust / sensitive / cross-supplier 风险
→ AgentUsedKnowledge evidence candidate
→ KWE 或 Harness 接收证据
→ 人工 / 委员会 / WAES 后续确认
```

## 3. 最小记录字段

每条调用证据至少包含：

- invocationId
- tenantId
- agentId
- userId
- capabilityId
- capabilityType
- purpose
- requestedScope
- allowedScope
- timestamp
- inputObjectRefs
- retrievedObjectRefs
- sourceRefs
- evidenceRefs
- waesGateRefs
- outputCandidateRefs
- overreadSignals
- outcome
- writesAccepted
- writesPublic
- writesBusinessSystem
- writesExternalApi

## 4. 越权读取风险信号

WAES / MMC 至少识别以下风险：

- cross_tenant_access
- cross_supplier_access
- acl_missing
- domain_scope_mismatch
- rag_blocked_used
- t5_used_as_final_fact
- sensitive_raw_content_requested
- unverified_strong_conclusion
- promotion_bypass_attempt
- external_share_without_gate

## 5. 硬边界

Agent 不能：

- 直接写 `accepted`。
- 直接写 `public`。
- 直接改 governance evidence。
- 跨供应商读取 supply_chain 未授权对象。
- 使用 unverified / T5 内容生成正式结论。
- 绕过 KWE 完成 promotion。
- 直接写 GFIS/GPC/ERP/MES。
- 直接确认收益、积分、额度或悬赏结算。

允许的输出只能是：

- candidate_fact
- candidate_sop
- candidate_writeback
- candidate_gap
- candidate_risk
- candidate_summary
- metadata_only_answer
- blocked_with_reason

## 6. Evidence 要求

高风险调用必须生成 Harness evidence candidate，并保留：

- invocation 摘要。
- 读取对象清单。
- RAG admission 快照。
- WAES gate 结果。
- overread 信号。
- 被阻断或降级的原因。

敏感资料只记录 metadata-only，不记录原文、密钥、Token、合同敏感条款、POD 原件或金融凭证原文。

## 7. 本地验证边界

本规则当前只通过本地 OKF、shared type、fixture 和 validator 验证。

不得把本规则写成：

- 真实 MMC 网关已经上线。
- 真实 Agent 调用已经接入。
- 真实 KDS 接口同步已经完成。
- 真实 GFIS/GPC 写回已完成。
- Agent 已获得正式裁决权或事实确认权。
