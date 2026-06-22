---
doc_id: GPCF-DOC-F5839F8424
title: LOOP Round GPCF-KDS-DKS-068 - GC-Knowledge Fabric Governance Ledger Dry-run
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-068.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-068.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-068 - GC-Knowledge Fabric Governance Ledger Dry-run

## 1. 本轮目标

建立 Contribution、Revenue、Quota、Bounty 四类治理台账 dry-run，验证“有收入才进正式收益”“自购 AI 额度不进统一收益池”“候选贡献不能直接确认”“悬赏结算必须绑定缺口和验收状态”等 P0 底线可以被本地 fixture 机检。

本轮只运行本地 fixture 和 dry-run validator，不触达真实 KDS、GFIS、GPC、WAES、财务系统或外部 API。

## 2. 本轮输入资料

- `packages/shared/src/knowledge/contribution.ts`
- `packages/shared/src/knowledge/revenue.ts`
- `packages/shared/src/knowledge/quota.ts`
- `packages/shared/src/knowledge/bounty.ts`
- `packages/api/src/governance/contracts.ts`
- `okf/contribution-policy.yaml`
- `okf/revenue-policy.yaml`
- `okf/quota-policy.yaml`
- `okf/bounty-policy.yaml`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-067.md`

## 3. 本轮新增或修订工程文件

- 修订 `packages/api/src/governance/contracts.ts`
- 新增 `fixtures/governance/ledger-dry-run.json`
- 新增 `scripts/governance/validate_governance_ledger_dry_run.py`

## 4. 本轮台账口径

- 正式收益必须是 `formal_revenue` + `cash_received` + evidence。
- 开票收入只能进入财务统计，不得直接分配。
- 潜在收益、渠道机会、知识潜在价值不得自动进入正式收益分配。
- 候选贡献必须等待人工或委员会确认。
- 自购额度必须 `revenuePoolEligible=false`。
- 悬赏结算必须绑定 GapRecord，并完成验收或部分验收。

## 5. 本轮验证计划

- `python3 scripts/governance/validate_governance_ledger_dry_run.py`
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
| Governance Ledger dry-run | `governance_ledger_dry_run=pass contributions=2 revenues=3 quotas=3 bounties=2 formal_distribution_eligible=1 confirmed_contributions=1 valid_quotas=2 invalid_quotas=1 settlement_eligible_bounties=1 real_revenue_distributions=0 real_quota_mutations=0 real_bounty_settlements=0` |
| Fixture JSON 解析 | `governance_ledger_fixture_json=pass` |
| KDS Search dry-run | `kds_search_dry_run=pass objects=5 results=1 tenant_filter=covered acl_filter=covered domain_filter=covered pool_filter=covered project_filter=covered rag_filter=covered keyword_filter=covered result_fields=covered real_kds_reads=0 vector_reads=0 graph_reads=0` |
| GFIS Assistant no-write smoke | `gfis_assistant_no_write_smoke=pass runs=4 knowledge=covered usage=covered document_acceptance=covered writeback_candidate=covered business_writes=0 external_api_writes=0 kds_writes=0` |
| WAES dry-run validator | `waes_minimum_gates=pass cases=6 passed_cases=6 evaluated_gates=16 source_gate=covered evidence_gate=covered rag_gate=covered writeback_gate=covered revenue_gate=covered contribution_gate=covered sensitive_data_gate=covered real_writes=0 external_api_writes=0` |
| KWE dry-run validator | `kwe_minimum_workflow=pass workflows=4 promotable_candidates=1 blocked_or_pending_candidates=3 ai_direct_fact_writes=0 kds_fact_writes=0 gfis_writes=0` |
| Shared Types 编译检查 | `tsc -p packages/shared/tsconfig.json --noEmit` 通过 |
| API Contract 编译检查 | `tsc -p packages/api/tsconfig.json --noEmit` 通过 |
| OKF YAML / JSON 解析复查 | `okf_contract_parse=pass files=15` |
| 文档污染检查 | `document_pollution=pass` |
| KDS Token 安全检查 | `kds_token=pass fingerprint=bfd9553d` |
| LOOP 文档门禁 | `gate=pass` |
| 差异检查 | `git diff --check -- docs/harness/loops/loop-round-GPCF-KDS-DKS-068.md fixtures/governance/ledger-dry-run.json scripts/governance/validate_governance_ledger_dry_run.py packages/api/src/governance/contracts.ts` 通过 |
| 敏感词与误升级扫描 | 通过，未发现 P0 8 份、正式写回已完成、收益已确认、production_ready、accepted/integrated、真实 KDS API 已同步或密钥模式 |

`loop_document_gate.py` 仍显示仓库级 `status_counts.missing=1` 和 `project_counts.missing=1`，该项为全仓既有元数据缺口。本轮 ledger dry-run 不产生真实收益分配、不变更真实额度、不结算真实悬赏、不写真实 KDS/GFIS/GPC。

## 7. 风险与边界

- Ledger dry-run 只验证台账规则，不证明真实收入、真实积分、真实额度或真实悬赏已经确认。
- 本轮不创建真实收益分配、不扣减额度、不结算悬赏、不写真实 KDS。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-069`：建立 GFIS 文档验收助手候选事实 end-to-end dry-run。
- `GPCF-KDS-DKS-070`：建立 Brain / PKC 入口 contract smoke。
- `GPCF-KDS-DKS-071`：建立 LOOP dashboard 指标 dry-run。
