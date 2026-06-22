---
doc_id: GPCF-DOC-9B51263381
title: GC-Knowledge Fabric WAES Gate 输入输出契约与 Hard-stop 规则
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/waes-gate-io-policy.md
source_path: docs/gc-knowledge-fabric/waes-gate-io-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric WAES Gate 输入输出契约与 Hard-stop 规则

## 1. 定位

本文件定义 WAES Gate 的最小输入输出契约、reason code、allowed operations 和 hard-stop 规则，用于防止 RAG、写回、收益、贡献、外部共享、冻结等门禁只停留在“名称清单”层面。

本文件只定义 no-write gate check 契约，不落库 WAES gate result，不写 GFIS/GPC/ERP/MES，不确认收益、积分、额度、悬赏或委员会裁决。

## 2. Gate 输入契约

每次 WAES gate check 至少必须提供：

| 字段 | 说明 |
|---|---|
| `gateId` | 本次 gate check 编号 |
| `tenantId` | 租户隔离 |
| `gateType` | WAES gate 类型 |
| `targetObjectType` | 目标对象类型 |
| `targetObjectId` | 目标对象编号 |
| `policyRefs` | 适用 OKF/WAES policy |
| `sourceRefs` | 来源引用 |
| `evidenceRefs` | 证据引用 |
| `aclRefs` | 权限与可见性引用 |
| `riskSignals` | 风险信号 |
| `requestedBy` | 发起者 |
| `dryRun` | P0/P1 阶段必须为 true |

## 3. Gate 输出契约

每次 WAES gate check 至少必须输出：

| 字段 | 说明 |
|---|---|
| `gateId` | 与输入一致 |
| `result` | `passed` / `blocked` / `repair_required` / `human_required` / `committee_required` / `redaction_required` / `freeze_required` / `metadata_only` |
| `reasonCodes` | 可解释原因码 |
| `requiredActions` | 后续动作 |
| `nextState` | 建议的 KDS/KWE 下一状态 |
| `allowedOperations` | 允许操作 |
| `reviewerRequirement` | 是否需要人工或委员会 |
| `harnessEvidenceRequired` | 是否必须留存 Harness evidence |
| `writesGateResult` | P0/P1 dry-run 必须为 false |
| `writesBusinessSystem` | 必须为 false |
| `writesRevenueDistribution` | 必须为 false |
| `writesExternalApi` | 必须为 false |

## 4. Hard-stop 规则

| Gate | hard-stop 条件 | 默认结果 |
|---|---|---|
| RAG Gate | T5、无来源、无证据、敏感原文、ACL 不明 | `blocked` 或 `metadata_only` |
| Writeback Gate | 无业务负责人、无 evidence、无确认包、目标字段责任不清 | `blocked` 或 `human_required` |
| Revenue Gate | 未到账、无开票/合同/机会依据、贡献归因争议 | `blocked` 或 `committee_required` |
| Contribution Gate | 无采纳证据、重复贡献、责任边界不清 | `repair_required` 或 `committee_required` |
| External Share Gate | ACL 不明、合同/金融/POD/质量争议原文、未脱敏 | `blocked` 或 `redaction_required` |
| Freeze Gate | 重大争议、恶意污染、未授权访问、收益分配争议 | `freeze_required` |

## 5. Reason Code 最小集合

| Reason Code | 含义 |
|---|---|
| `missing_source` | 缺来源 |
| `missing_evidence` | 缺证据 |
| `t5_ai_only` | 仅 AI/LLM 候选 |
| `acl_unknown` | 权限不明 |
| `sensitive_raw_content` | 敏感原文暴露风险 |
| `owner_confirmation_missing` | 业务负责人确认缺失 |
| `committee_required_by_policy` | 规则要求委员会 |
| `revenue_basis_missing` | 收益依据缺失 |
| `duplicate_or_conflicting_contribution` | 重复或冲突贡献 |
| `major_violation_risk` | 重大违规风险 |

## 6. P0/P1 验收条件

- OKF 中有独立 WAES Gate IO policy。
- Shared Types 中有 Gate input、Gate output、reason code、allowed operation 和 hard-stop rule 类型。
- Validator 能检查输入输出字段、6 类 hard-stop gate、10 个 reason code 和 no-write 断言。
- 所有验证只使用本地文件和 fixture，不触达真实 WAES/KDS/GFIS/GPC 或外部 API。
