---
doc_id: GPCF-DOC-11CD3E9E36
title: LOOP Round GPCF-KDS-DKS-091 - GC-Knowledge Fabric Harness evidence 引用完整性
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-091.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-091.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-091 - GC-Knowledge Fabric Harness evidence 引用完整性

## 1. 本轮目标

建立 Harness evidence 引用完整性 validator，固化 evidence 与 KDS 对象、来源、WAES gate、LOOP record、委员会/授权决策记录之间的最小引用边界。

本轮只做本地 OKF、文档、shared type、fixture 和 no-write validator，不写真实 Harness evidence，不写 KDS fact，不写 WAES gate result，不写 KWE work item，不写 GFIS/GPC/ERP/MES，不确认收益、积分、额度、悬赏或委员会裁决。

## 2. 本轮输入资料

- `packages/shared/src/knowledge/evidence.ts`
- `packages/shared/src/knowledge/object-relationship.ts`
- `packages/shared/src/knowledge/loop-record-closure.ts`
- `packages/api/src/governance/contracts.ts`
- `packages/api/src/governance/routes.ts`
- `docs/gc-knowledge-fabric/object-relationship-policy.md`
- `docs/gc-knowledge-fabric/sensitive-metadata-storage-policy.md`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-090.md`
- GC-Knowledge Fabric 综合实施方案：Harness 负责 evidence、acceptance、audit、Knowledge CI、AgentUsedKnowledge、Publication Approval、Permission Change Record，且不存普通业务知识正文

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/harness-evidence-integrity-policy.md`
- `okf/harness-evidence-integrity-policy.yaml`
- `packages/shared/src/knowledge/harness-evidence-integrity.ts`
- `fixtures/governance/harness-evidence-integrity-policy-smoke.json`
- `scripts/governance/validate_harness_evidence_integrity_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- Evidence 最小字段必须覆盖 evidence、tenant、kind、title、object/source/gate/loop/decision refs、hash、受控原件指针、summary、createdBy、createdAt 和 metadata。
- 引用分组必须覆盖 objectRefs、sourceRefs、gateRefs、loopRefs、decisionRefs。
- evidence kind 必须与 shared `EvidenceKind` 保持一致。
- 完整性状态只能是 passed、blocked、repair_required。
- passed 只表示引用结构完整，不表示业务完成或验收完成。
- Evidence 不得直接创建正式事实、写业务系统、分配收益、确认积分、划拨额度、结算悬赏、完成委员会裁决、允许外部共享或写外部 API。
- 敏感 metadata-only evidence 不得包含敏感原文。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| Harness evidence integrity policy smoke | pass | `harness_evidence_integrity_policy_smoke=pass evidence_fields=15 reference_groups=5 evidence_kinds=9 integrity_statuses=3 integrity_rules=5 unresolved_refs=0 sensitive_raw_content=false passed_business_completion=false writes_kds_fact=0 writes_business_system=0 writes_revenue_distribution=0 writes_score_confirmation=0 writes_quota_transfer=0 writes_bounty_settlement=0 writes_committee_decision_completion=0 writes_external_share_permission=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=19 okf_files=26 type_files=28 api_files=15 validator_files=26 fixture_files=26 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | LOOP closure、AgentUsedKnowledge、状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0 台账、委员会 DecisionRecord、敏感 metadata storage smoke 全部 pass |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=25 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-091 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮不代表真实 Harness evidence 已写入。
- Evidence 引用完整性 pass 只代表本地结构完整，不能升级为业务完成、验收完成、正式写回、正式收益或积分确认。
- Harness evidence 仍只保存治理证据，不保存普通业务知识正文或敏感原文。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-092`：建立 KDS 对象 ACL 与外部共享视图 smoke。
- `GPCF-KDS-DKS-093`：建立 RAG response citation packet dry-run。
- `GPCF-KDS-DKS-094`：建立 KWE confirmation workpack 引用完整性 validator。
