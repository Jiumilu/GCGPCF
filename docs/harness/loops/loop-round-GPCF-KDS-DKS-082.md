---
doc_id: GPCF-DOC-5135C5EDA5
title: LOOP Round GPCF-KDS-DKS-082 - GC-Knowledge Fabric 核心对象关系策略
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-082.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-082.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-082 - GC-Knowledge Fabric 核心对象关系策略

## 1. 本轮目标

根据 GC-Knowledge Fabric 完整评审问题清单中“对象模型有清单，但缺少对象之间关系图”的 P0/P1 缺口，建立核心对象关系与最小字段契约，固定 Source、Evidence、KnowledgeObject、候选对象、WAES、KWE、Confirmation/Decision、Writeback、Contribution、Revenue、Harness 和 LOOP 的最小关系链。

本轮只做关系契约和本地 no-write validator，不创建正式事实，不执行真实业务写回，不结算收益、积分、额度或悬赏。

## 2. 本轮输入资料

- `docs/gc-knowledge-fabric/status-machine-policy.md`
- `okf/status-machine-policy.yaml`
- `packages/shared/src/knowledge/object.ts`
- `packages/shared/src/knowledge/evidence.ts`
- `packages/shared/src/knowledge/source.ts`
- GC-Knowledge Fabric 综合实施方案完整评审与问题清单：问题 2 核心对象关系图建议

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/object-relationship-policy.md`
- `okf/object-relationship-policy.yaml`
- `packages/shared/src/knowledge/object-relationship.ts`
- `fixtures/object-relationship/object-relationship-policy-smoke.json`
- `scripts/object_relationship/validate_object_relationship_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 最小关系链必须覆盖 SourceRecord -> EvidenceRecord -> KnowledgeObject -> Candidate/Gap -> WAESGateResult -> KWEWorkItem -> Confirmation/Decision -> Writeback/Contribution/Revenue -> HarnessEvidenceRecord -> LOOPRecord。
- 每条关系必须有 `relation_type`、端点类型和 `required_refs`。
- 最小字段必须覆盖 id、tenant、from/to endpoint、required refs、pool refs、createdBy、createdAt 和 noWrite。
- 必须锁定 hard boundaries：正式事实需要来源、evidence_ready 需要 evidence、候选需要 WAES gate、写回候选需要确认、AI 不能创建正式写回关系、LOOP 不能提升业务状态。
- no-write 断言必须证明 KDS fact、业务系统、收益分配和外部 API 写入均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| 对象关系 policy smoke | pass | `object_relationship_policy_smoke=pass relations=10 minimum_fields=12 source_evidence_chain=covered candidate_gate_workflow_chain=covered decision_contribution_revenue_chain=covered harness_loop_chain=covered writes_kds_fact=0 writes_business_system=0 writes_revenue_distribution=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=10 okf_files=17 type_files=19 api_files=15 validator_files=17 fixture_files=17 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 状态机回归 | pass | `status_machine_policy_smoke=pass states=11 promotion_rules=10 ... writes_external_api=0` |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=16 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-082 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮关系链只是契约，不代表真实 Source、Evidence、Fact、Writeback、Revenue 或 LOOP 对象已经产生。
- HarnessEvidenceRecord 仍只保存治理证据，不存普通业务正文。
- LOOPRecord 只能记录闭环 evidence 和 next actions，不能自动升级业务状态。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-083`：建立 WAES Gate 输入输出契约与 hard-stop reason code validator。
- `GPCF-KDS-DKS-084`：建立 RAG 引用强度 L0-L5 契约与 Brain/PKC/GFIS Assistant 引用边界 smoke。
- `GPCF-KDS-DKS-085`：建立 GFIS Writeback Sandbox 契约与 no-write/sandbox/approved-write 边界 smoke。
