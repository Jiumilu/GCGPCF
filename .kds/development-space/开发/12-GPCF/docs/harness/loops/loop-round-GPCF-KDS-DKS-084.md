---
doc_id: GPCF-DOC-D0B29C3DE0
title: LOOP Round GPCF-KDS-DKS-084 - GC-Knowledge Fabric RAG Citation Strength L0-L5
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-084.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-084.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-084 - GC-Knowledge Fabric RAG Citation Strength L0-L5

## 1. 本轮目标

根据 GC-Knowledge Fabric 完整评审问题清单中“RAG 准入规则方向正确，但缺少引用强度分层”的 P0/P1 缺口，建立 RAG 引用强度 L0-L5 规则，防止 `safe` 被误读为业务决策、正式写回、收益确认或责任归因授权。

本轮只做引用强度契约、Shared Type 和 no-write validator，不执行真实 RAG 检索，不写 KDS、WAES、GFIS/GPC 或外部 API。

## 2. 本轮输入资料

- `okf/rag-admission-policy.yaml`
- `packages/shared/src/knowledge/rag-admission.ts`
- `packages/shared/src/knowledge/object.ts`
- `docs/gc-knowledge-fabric/waes-gate-io-policy.md`
- GC-Knowledge Fabric 综合实施方案完整评审与问题清单：问题 5 RAG 引用强度分层建议

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/rag-citation-strength-policy.md`
- `okf/rag-citation-strength-policy.yaml`
- `packages/shared/src/knowledge/rag-citation-strength.ts`
- `fixtures/rag/citation-strength-policy-smoke.json`
- `scripts/rag/validate_rag_citation_strength_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 引用强度必须覆盖 `L0` 至 `L5`。
- `blocked` 必须映射到 `L0`。
- `sensitive_metadata_only` 与 `repair_required` 只能映射到 `L1/L2`。
- `limited` 必须映射到 `L3`。
- `safe` 默认映射到 `L4`。
- `L5` 必须要求 `safe`、T0/T1、人工或委员会确认、证据存在。
- `L5` 不得自动触发业务写回、收益确认或委员会裁决替代。
- no-write 断言必须证明 KDS fact、WAES gate result、业务系统、收益分配和外部 API 写入均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| RAG 引用强度 smoke | pass | `rag_citation_strength_policy_smoke=pass levels=6 mappings=5 blocked=L0 limited=L3 safe=L4 l5_conditions=T0,T1+confirmed+evidence l5_no_auto_writeback=covered sensitive_metadata_boundary=covered writes_kds_fact=0 writes_waes_gate_result=0 writes_business_system=0 writes_revenue_distribution=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=12 okf_files=19 type_files=21 api_files=15 validator_files=19 fixture_files=19 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 状态机、对象关系、WAES IO 回归 | pass | `status_machine_policy_smoke=pass`；`object_relationship_policy_smoke=pass`；`waes_gate_io_policy_smoke=pass` |
| WAES 既有回归 | pass | `waes_endpoint_no_write_smoke=pass`；`waes_minimum_gates=pass` |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=18 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-084 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮 L0-L5 只是引用强度契约，不代表任何对象已进入真实 RAG 索引或生产检索。
- `L5` 是业务辅助决策引用，不是自动业务决策、正式写回、收益确认或责任归因。
- 敏感资料仍必须经过 metadata-only、脱敏、ACL 和 external share gate。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-085`：建立 GFIS Writeback Sandbox 契约与 no-write/sandbox/approved-write 边界 smoke。
- `GPCF-KDS-DKS-086`：建立四池台账 P0 压缩规则 validator，区分登记、候选、确认和禁止自动结算。
- `GPCF-KDS-DKS-087`：建立 Committee DecisionRecord 输入输出契约与争议冻结门禁 smoke。
