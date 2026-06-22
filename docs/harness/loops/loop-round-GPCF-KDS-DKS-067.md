---
doc_id: GPCF-DOC-29DFAA93C4
title: LOOP Round GPCF-KDS-DKS-067 - GC-Knowledge Fabric KDS v2 Search Dry-run
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-067.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-067.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-067 - GC-Knowledge Fabric KDS v2 Search Dry-run

## 1. 本轮目标

建立 KDS v2 search/filter dry-run，验证认证、租户隔离、ACL、scope、domain、pool、project、RAG admission、关键词匹配、可信等级排序和结果字段完整性可以被本地 fixture 机检。

本轮只运行本地 fixture 和 dry-run validator，不触达真实 KDS API、向量库、图数据库、GFIS、WAES 或外部 API。

## 2. 本轮输入资料

- `packages/api/src/kds/v2/contracts.ts`
- `packages/shared/src/knowledge/object.ts`
- `okf/rag-admission-policy.yaml`
- `03-data-ai-knowledge/GC-Knowledge-Fabric-RAG准入与引用强度规则.md`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-066.md`

## 3. 本轮新增工程文件

- `fixtures/kds/search-dry-run.json`
- `scripts/kds/validate_kds_search_dry_run.py`

## 4. 本轮搜索口径

- 先认证和租户隔离，再 ACL 和 scope 过滤。
- Domain、Pool、Project、RAG admission 过滤必须早于关键词结果返回。
- `blocked` 内容不得进入 RAG 结果。
- 结果必须展示 Domain、PoolRefs、ObjectType、TrustLevel、RAG Admission、Lifecycle、Visibility、SourceRefs、EvidenceRefs、WAES Gate Status、CanShare、CanPromote、CanUseForRAG、CanWriteback。

## 5. 本轮验证计划

- `python3 scripts/kds/validate_kds_search_dry_run.py`
- `python3 scripts/gfis/validate_gfis_assistant_no_write_smoke.py`
- `python3 scripts/waes/validate_waes_minimum_gates.py`
- `python3 scripts/kwe/validate_kwe_minimum_workflow.py`
- `tsc -p packages/shared/tsconfig.json --noEmit`
- `tsc -p packages/api/tsconfig.json --noEmit`
- 文档污染检查。
- KDS Token 安全检查。
- LOOP 文档门禁。
- 差异检查与误升级关键词扫描。

## 6. 本轮验证结果

| 检查 | 结果 |
|---|---|
| KDS Search dry-run | `kds_search_dry_run=pass objects=5 results=1 tenant_filter=covered acl_filter=covered domain_filter=covered pool_filter=covered project_filter=covered rag_filter=covered keyword_filter=covered result_fields=covered real_kds_reads=0 vector_reads=0 graph_reads=0` |
| Fixture JSON 解析 | `kds_search_fixture_json=pass` |
| GFIS Assistant no-write smoke | `gfis_assistant_no_write_smoke=pass runs=4 knowledge=covered usage=covered document_acceptance=covered writeback_candidate=covered business_writes=0 external_api_writes=0 kds_writes=0` |
| WAES dry-run validator | `waes_minimum_gates=pass cases=6 passed_cases=6 evaluated_gates=16 source_gate=covered evidence_gate=covered rag_gate=covered writeback_gate=covered revenue_gate=covered contribution_gate=covered sensitive_data_gate=covered real_writes=0 external_api_writes=0` |
| KWE dry-run validator | `kwe_minimum_workflow=pass workflows=4 promotable_candidates=1 blocked_or_pending_candidates=3 ai_direct_fact_writes=0 kds_fact_writes=0 gfis_writes=0` |
| Shared Types 编译检查 | `tsc -p packages/shared/tsconfig.json --noEmit` 通过 |
| API Contract 编译检查 | `tsc -p packages/api/tsconfig.json --noEmit` 通过 |
| OKF YAML / JSON 解析复查 | `okf_contract_parse=pass files=15` |
| 文档污染检查 | `document_pollution=pass` |
| KDS Token 安全检查 | `kds_token=pass fingerprint=bfd9553d` |
| LOOP 文档门禁 | `gate=pass` |
| 差异检查 | `git diff --check -- docs/harness/loops/loop-round-GPCF-KDS-DKS-067.md fixtures/kds/search-dry-run.json scripts/kds/validate_kds_search_dry_run.py` 通过 |
| 敏感词与误升级扫描 | 通过，未发现 P0 8 份、正式写回已完成、收益已确认、production_ready、accepted/integrated、真实 KDS API 已同步或密钥模式 |

`loop_document_gate.py` 仍显示仓库级 `status_counts.missing=1` 和 `project_counts.missing=1`，该项为全仓既有元数据缺口。本轮 search dry-run 不读取真实 KDS、不访问向量索引、不访问图数据库、不生成真实 RAG 引用。

## 7. 风险与边界

- Search dry-run 只验证过滤与结果字段契约，不证明真实索引、向量召回或图检索已经上线。
- 本轮不读取真实 KDS，不写真实 KDS，不生成真实 RAG 引用。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-068`：建立 Governance Ledger dry-run。
- `GPCF-KDS-DKS-069`：建立 GFIS 文档验收助手候选事实 end-to-end dry-run。
- `GPCF-KDS-DKS-070`：建立 Brain / PKC 入口 contract smoke。
