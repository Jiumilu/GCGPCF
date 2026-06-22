---
doc_id: GPCF-DOC-0E289454CD
title: LOOP Round GPCF-KDS-DKS-072 - GC-Knowledge Fabric OKF/Types/API/Validator覆盖矩阵
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-072.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-072.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-072 - GC-Knowledge Fabric OKF/Types/API/Validator覆盖矩阵

## 1. 本轮目标

建立 GC-Knowledge Fabric P0-P1 工程交付物的覆盖矩阵，把 OKF 契约、Shared Types、API Contracts、dry-run validators 和 fixtures 的对应关系显式化，并用本地 validator 检查声明覆盖与真实文件存在性一致。

本轮只运行本地 fixture 和 dry-run validator，不触达真实 KDS、WAES、KWE、GFIS、GPC、Brain、PKC、治理台账或外部 API。

## 2. 本轮输入资料

- `okf/*`
- `packages/shared/src/knowledge/*`
- `packages/api/src/*`
- `scripts/*`
- `fixtures/*`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-071.md`

## 3. 本轮新增工程文件

- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 4. 本轮验收口径

- 覆盖矩阵必须覆盖知识对象核心、KDS 十一池、候选事实/SOP/写回、WAES/RAG、KWE、积分/收益/额度/悬赏、Brain/PKC/LOOP Dashboard、governance/loop/evidence。
- 所有声明文件必须真实存在。
- OKF 15 个契约文件必须至少被覆盖一次。
- Shared knowledge 类型文件必须至少被覆盖一次，`index.ts` 作为聚合导出不计入对象覆盖要求。
- API contracts / SQL 文件必须至少被覆盖一次，`index.ts` 作为聚合导出不计入模块覆盖要求。
- 覆盖矩阵 validator 只读，必须声明 `noWrite=true`。
- dry-run 写入计数必须全部为 0。

## 5. 本轮验证计划

- `python3 scripts/coverage/validate_okf_types_api_validator_coverage.py`
- `python3 scripts/loop_dashboard/validate_knowledge_closure_metrics.py`
- `python3 scripts/brain_pkc/validate_brain_pkc_entry_contract_smoke.py`
- `python3 scripts/gfis/validate_gfis_document_acceptance_e2e.py`
- `python3 scripts/governance/validate_governance_ledger_dry_run.py`
- `python3 scripts/kds/validate_kds_search_dry_run.py`
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
| 覆盖矩阵 validator | `okf_types_api_validator_coverage=pass coverage_items=8 okf_files=15 type_files=17 api_files=8 validator_files=9 fixture_files=9 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| 覆盖矩阵 fixture JSON 解析 | `coverage_matrix_fixture_json=pass` |
| LOOP Dashboard 指标 dry-run | `knowledge_closure_metrics=pass objects=5 closure_score=53 rag_safe_rate=0.2 blocked_knowledge_rate=0.2 repair_required_gap_count=1 waes_interception_count=2 human_confirmation_completion_rate=0.5 committee_closure_rate=0.5 revenue_candidate_to_formal_rate=0.5 bounty_closure_rate=0.333333 ai_candidate_adoption_rate=0.4 external_share_violation_count=1 sensitive_metadata_only_rate=0.4 no_write=covered kds_writes=0 waes_writes=0 kwe_writes=0 business_writes=0 external_api_writes=0` |
| Brain/PKC 入口契约 smoke | `brain_pkc_entry_contract_smoke=pass cases=4 surfaces=brain,pkc covered_views=18 blocked_actions=19 no_write=covered kds_writes=0 waes_writes=0 kwe_writes=0 business_writes=0 external_api_writes=0` |
| GFIS 文档验收 E2E dry-run | `gfis_document_acceptance_e2e=pass cases=3 fact_candidates=3 gaps=4 human_or_blocked_cases=3 writeback_candidates_only=1 business_writes=0 kds_fact_writes=0 external_api_writes=0` |
| Governance Ledger dry-run | `governance_ledger_dry_run=pass contributions=2 revenues=3 quotas=3 bounties=2 formal_distribution_eligible=1 confirmed_contributions=1 valid_quotas=2 invalid_quotas=1 settlement_eligible_bounties=1 real_revenue_distributions=0 real_quota_mutations=0 real_bounty_settlements=0` |
| KDS Search dry-run | `kds_search_dry_run=pass objects=5 results=1 tenant_filter=covered acl_filter=covered domain_filter=covered pool_filter=covered project_filter=covered rag_filter=covered keyword_filter=covered result_fields=covered real_kds_reads=0 vector_reads=0 graph_reads=0` |
| WAES dry-run validator | `waes_minimum_gates=pass cases=6 passed_cases=6 evaluated_gates=16 source_gate=covered evidence_gate=covered rag_gate=covered writeback_gate=covered revenue_gate=covered contribution_gate=covered sensitive_data_gate=covered real_writes=0 external_api_writes=0` |
| KWE dry-run validator | `kwe_minimum_workflow=pass workflows=4 promotable_candidates=1 blocked_or_pending_candidates=3 ai_direct_fact_writes=0 kds_fact_writes=0 gfis_writes=0` |
| Shared Types 编译检查 | `tsc -p packages/shared/tsconfig.json --noEmit` 通过 |
| API Contract 编译检查 | `tsc -p packages/api/tsconfig.json --noEmit` 通过 |
| OKF YAML / JSON 解析复查 | `okf_contract_parse=pass files=15` |
| 文档污染检查 | `document_pollution=pass` |
| KDS Token 安全检查 | `kds_token=pass fingerprint=bfd9553d` |
| LOOP 文档门禁 | `gate=pass` |
| 差异检查 | `git diff --check -- docs/harness/loops/loop-round-GPCF-KDS-DKS-072.md fixtures/coverage/okf-types-api-validator-coverage.json scripts/coverage/validate_okf_types_api_validator_coverage.py` 通过 |
| 敏感词与误升级扫描 | 通过，未发现指定误升级表述或密钥模式 |

`loop_document_gate.py` 仍显示仓库级 `status_counts.missing=1` 和 `project_counts.missing=1`，该项为全仓既有元数据缺口。本轮覆盖矩阵不证明真实业务系统上线，不创建真实 KDS 对象、WAES GateResult、KWE WorkItem、GFIS 写回、收益分配或外部共享放行。

## 7. 风险与边界

- 覆盖矩阵只证明 P0-P1 工程交付物之间存在可审计映射，不证明业务系统已上线。
- 覆盖矩阵不替代真实 API、真实 KDS 写入、真实 GFIS 写回或人工/委员会确认。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-073`：建立 Brain/PKC UI 最小只读页面清单。
- `GPCF-KDS-DKS-074`：建立 KDS v2 endpoint skeleton 与 no-write route smoke。
- `GPCF-KDS-DKS-075`：建立 SQL schema 覆盖与迁移风险 dry-run。
