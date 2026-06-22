---
doc_id: GPCF-DOC-DD8F57A179
title: LOOP Round GPCF-KDS-DKS-089 - GC-Knowledge Fabric AgentUsedKnowledge Evidence Contract
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-089.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-089.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-089 - GC-Knowledge Fabric AgentUsedKnowledge Evidence Contract

## 1. 本轮目标

建立 MMC AgentUsedKnowledge 调用证据契约与越权读取拦截 smoke，覆盖 Agent / Connector / MCP 在读取 KDS 知识、生成候选输出、触发 WAES 门禁、记录 Harness evidence candidate 时的最小字段和硬边界。

本轮只做本地 OKF、文档、shared type、fixture 和 no-write validator，不调用真实模型，不读取真实 KDS API，不写 Harness evidence，不写 GFIS/GPC/ERP/MES，不确认事实、收益、积分、额度或悬赏。

## 2. 本轮输入资料

- `packages/shared/src/knowledge/evidence.ts`
- `packages/shared/src/knowledge/object.ts`
- `packages/shared/src/knowledge/waes-gate.ts`
- `okf/waes-gate-policy.yaml`
- `okf/rag-admission-policy.yaml`
- `okf/sensitive-metadata-storage-policy.yaml`
- `docs/gc-knowledge-fabric/waes-gate-io-policy.md`
- `docs/gc-knowledge-fabric/sensitive-metadata-storage-policy.md`
- GC-Knowledge Fabric 综合实施方案：MMC 能力网关、AgentUsedKnowledge evidence、Agent 不能直接写 accepted/public/governance evidence、不能跨供应商越权读取、不能绕过 KWE promotion

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/agent-used-knowledge-policy.md`
- `okf/agent-used-knowledge-policy.yaml`
- `packages/shared/src/knowledge/agent-used-knowledge.ts`
- `fixtures/mmc/agent-used-knowledge-policy-smoke.json`
- `scripts/mmc/validate_agent_used_knowledge_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- capability type 至少覆盖 RAG query、候选事实、候选 SOP、写回建议、文档验收和治理审阅。
- invocation 最小字段必须覆盖调用人、Agent、能力、目的、请求 scope、允许 scope、对象、来源、evidence、WAES gate、候选输出、越权信号、结果和 no-write flags。
- overread risk signal 必须覆盖跨租户、跨供应商、ACL 缺失、domain/scope 不匹配、blocked RAG、T5 正式结论、敏感原文请求、未确认强结论、promotion 绕过和未过 gate 外部共享。
- Agent 不能直接写 accepted、public、governance evidence、业务系统、收益或积分确认。
- 高风险调用必须要求 Harness evidence candidate。
- 本轮 validator 必须证明 accepted/public/governance evidence/business system/revenue-score/external API 写入均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| AgentUsedKnowledge policy smoke | pass | `agent_used_knowledge_policy_smoke=pass capability_types=6 invocation_fields=22 overread_signals=10 allowed_outcomes=8 required_gates=7 harness_evidence_required=true writes_accepted=0 writes_public=0 writes_governance_evidence=0 writes_business_system=0 writes_revenue_or_score_confirmation=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=17 okf_files=24 type_files=26 api_files=15 validator_files=24 fixture_files=24 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | 状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0 台账、委员会 DecisionRecord、敏感 metadata storage smoke 全部 pass |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=23 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-089 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮不代表真实 MMC 网关、Agent 调用链或 Connector 审计链已经上线。
- AgentUsedKnowledge 只能证明调用证据契约可机检，不能证明真实模型调用、真实知识读取或真实外部系统写入。
- Agent 输出仍只能进入 candidate，不得形成正式事实、正式写回、收益分配、积分确认、RAG 强引用或委员会裁决。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-090`：建立 LOOP record schema 与 next-action closure gate。
- `GPCF-KDS-DKS-091`：建立 Harness evidence 引用完整性 validator。
- `GPCF-KDS-DKS-092`：建立 KDS 对象 ACL 与外部共享视图 smoke。
