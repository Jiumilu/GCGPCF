---
doc_id: GPCF-DOC-098065D309
title: LOOP Round GPCF-KDS-DKS-070 - GC-Knowledge Fabric Brain/PKC入口契约Smoke
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-070.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-070.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-070 - GC-Knowledge Fabric Brain/PKC入口契约Smoke

## 1. 本轮目标

建立 Brain 与 PKC 入口层的最小 API 契约和只读 smoke，验证 Brain Workbench / PKC Console 只能聚合展示 KDS、WAES、KWE、治理台账与 LOOP 信息，不能绕过 WAES/KWE/委员会直接改变事实、写回业务系统、确认收益或覆盖门禁。

本轮只运行本地 fixture 和 dry-run validator，不触达真实 Brain、PKC、KDS、WAES、KWE、GFIS、GPC 或外部 API。

## 2. 本轮输入资料

- `packages/api/src/kds/v2/contracts.ts`
- `packages/api/src/kwe/contracts.ts`
- `packages/api/src/governance/contracts.ts`
- `packages/api/src/gfis/contracts.ts`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-069.md`

## 3. 本轮新增工程文件

- `packages/api/src/brain/contracts.ts`
- `packages/api/src/pkc/contracts.ts`
- `fixtures/brain-pkc/entry-contract-smoke.json`
- `scripts/brain_pkc/validate_brain_pkc_entry_contract_smoke.py`

## 4. 本轮修改工程文件

- `packages/api/src/index.ts`

## 5. 本轮验收口径

- Brain 可展示 Knowledge Command Center、KDS Object Center、WAES Gate Center、KWE Work Queue、治理中心、收益/贡献中心、AI 额度中心和 LOOP Dashboard。
- PKC 可展示我的知识、草稿、待办、Agent 输出、KWE 工单、贡献记录、积分、AI 额度、悬赏和项目知识包。
- Brain / PKC 响应必须声明 `noWrite=true`。
- Brain / PKC 不允许直接执行正式事实确认、WAES 覆盖、GFIS 写回、收益分配、委员会裁决或 KDS 生命周期强改。
- dry-run 写入计数必须全部为 0。

## 6. 本轮验证计划

- `python3 scripts/brain_pkc/validate_brain_pkc_entry_contract_smoke.py`
- `python3 scripts/gfis/validate_gfis_document_acceptance_e2e.py`
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

## 7. 本轮验证结果

| 检查 | 结果 |
|---|---|
| Brain/PKC 入口契约 smoke | `brain_pkc_entry_contract_smoke=pass cases=4 surfaces=brain,pkc covered_views=18 blocked_actions=19 no_write=covered kds_writes=0 waes_writes=0 kwe_writes=0 business_writes=0 external_api_writes=0` |
| Brain/PKC fixture JSON 解析 | `brain_pkc_fixture_json=pass` |
| GFIS 文档验收 E2E dry-run | `gfis_document_acceptance_e2e=pass cases=3 fact_candidates=3 gaps=4 human_or_blocked_cases=3 writeback_candidates_only=1 business_writes=0 kds_fact_writes=0 external_api_writes=0` |
| Governance Ledger dry-run | `governance_ledger_dry_run=pass contributions=2 revenues=3 quotas=3 bounties=2 formal_distribution_eligible=1 confirmed_contributions=1 valid_quotas=2 invalid_quotas=1 settlement_eligible_bounties=1 real_revenue_distributions=0 real_quota_mutations=0 real_bounty_settlements=0` |
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
| 差异检查 | `git diff --check -- docs/harness/loops/loop-round-GPCF-KDS-DKS-070.md fixtures/brain-pkc/entry-contract-smoke.json scripts/brain_pkc/validate_brain_pkc_entry_contract_smoke.py packages/api/src/brain/contracts.ts packages/api/src/pkc/contracts.ts packages/api/src/index.ts` 通过 |
| 敏感词与误升级扫描 | 通过，未发现指定误升级表述或密钥模式 |

`loop_document_gate.py` 仍显示仓库级 `status_counts.missing=1` 和 `project_counts.missing=1`，该项为全仓既有元数据缺口。本轮 smoke 不证明 Brain / PKC 前端已经实现，不创建真实 KDS 对象、WAES GateResult、KWE WorkItem、GFIS 写回或收益分配。

## 8. 风险与边界

- 本轮只证明入口契约边界可机检，不证明 Brain / PKC 前端已经实现。
- 本轮不创建真实 KDS 对象，不写 WAES/KWE/GFIS，不进行收益分配。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 9. 下一轮建议

- `GPCF-KDS-DKS-071`：建立 LOOP dashboard 指标 dry-run。
- `GPCF-KDS-DKS-072`：建立 OKF/Types/API/Validator 覆盖矩阵。
- `GPCF-KDS-DKS-073`：建立 Brain/PKC UI 最小只读页面清单。
