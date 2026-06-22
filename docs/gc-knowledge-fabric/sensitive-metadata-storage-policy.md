---
doc_id: GPCF-DOC-71DA0641E8
title: GC-Knowledge Fabric 敏感资料 Metadata-only 存储契约
project: KDS
related_projects: [WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/sensitive-metadata-storage-policy.md
source_path: docs/gc-knowledge-fabric/sensitive-metadata-storage-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric 敏感资料 Metadata-only 存储契约

## 1. 定位

本文件定义合同敏感条款、金融凭证、POD 原件、质量争议、客户/供应商身份、凭证或 Token、未发布政策解释、商业报价或佣金等敏感资料在 KDS 中的 metadata-only 存储契约。

敏感资料原文必须留在受控空间。KDS 只记录编号、摘要、哈希或受控原件指针、ACL、引用范围、证据链和 WAES Sensitive Data Gate 结果。

## 2. Metadata-only 最小字段

每条敏感 metadata record 至少包含：

- `objectId`
- `tenantId`
- `sensitiveClass`
- `storageMode`
- `sourceRef`
- `evidenceRef`
- `hashOrOriginalPointer`
- `controlledOriginalRef`
- `aclRef`
- `citationScope`
- `ragAdmission`
- `sensitiveDataGateResult`
- `summary`
- `rawContentStored`

## 3. 受控原件指针

受控原件指针必须满足：

- 不包含真实密钥、Token、银行卡、账户口令或完整敏感原文。
- 只指向授权受控空间。
- 有 hash 或不可逆摘要。
- 有 ACL 与 citation scope。
- 有 evidence ref 与 gate result。

## 4. 硬边界

1. `metadata_only` 不允许存原文。
2. `controlled_original` 只允许记录受控空间指针，不允许把原文写入 KDS 文档、fixture、evidence 或日志。
3. `credential_or_token` 默认必须 blocked 或 metadata-only。
4. 敏感资料默认 RAG admission 为 `sensitive_metadata_only`。
5. 敏感资料对外共享必须通过 redaction gate、external share gate 和 ACL gate。
6. Hash、摘要、编号、权限、证据链位置和受控原件位置可以入库；原件保留在受控空间。

## 5. P0/P1 验收条件

- OKF 中有敏感 metadata-only storage policy。
- Shared Types 中有敏感类别、存储模式、metadata record 和 no-raw-content 断言。
- Validator 能检查最小字段、敏感类别、存储模式、原文禁止、默认 RAG 准入和 no-write/no-secret 断言。
