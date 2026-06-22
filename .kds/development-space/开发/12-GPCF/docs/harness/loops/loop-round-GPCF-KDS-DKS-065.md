---
doc_id: GPCF-DOC-85B9E25E62
title: LOOP Round GPCF-KDS-DKS-065 - GC-Knowledge Fabric KWE最小流程Dry-run
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-065.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-065.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-065 - GC-Knowledge Fabric KWE最小流程Dry-run

## 1. 本轮目标

建立 KWE 最小流程 dry-run，验证 AI 候选事实不能直接形成正式事实，必须经过 WAES、KWE 工单、人工确认和 evidence 绑定后，才能进入待入账的受控状态。

本轮只运行本地 fixture 和 dry-run validator，不触达真实 KDS、GFIS、GPC、ERP、MES、WAES API 或生产数据库。

## 2. 本轮输入资料

- `okf/flow-policy.yaml`
- `okf/waes-gate-policy.yaml`
- `packages/shared/src/knowledge/fact-candidate.ts`
- `packages/api/src/kwe/contracts.ts`
- `scripts/waes/validate_waes_minimum_gates.py`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-064.md`

## 3. 本轮新增工程文件

- `fixtures/kwe/minimum-workflow.json`
- `scripts/kwe/validate_kwe_minimum_workflow.py`

## 4. 本轮流程口径

- AI 只能创建 `FactCandidate`。
- WAES 未通过或证据缺失时，KWE 必须保持 `repair_required` 或 `human_required`。
- 人工确认必须绑定 evidence。
- dry-run 只生成候选状态摘要，不创建真实 KDS Fact，不写 GFIS。

## 5. 本轮验证计划

- `python3 scripts/kwe/validate_kwe_minimum_workflow.py`
- `python3 scripts/waes/validate_waes_minimum_gates.py`
- `tsc -p packages/shared/tsconfig.json --noEmit`
- `tsc -p packages/api/tsconfig.json --noEmit`
- 文档污染检查。
- KDS Token 安全检查。
- LOOP 文档门禁。
- 差异检查与误升级关键词扫描。

## 6. 本轮验证结果

| 检查 | 结果 |
|---|---|
| KWE dry-run validator | `kwe_minimum_workflow=pass workflows=4 promotable_candidates=1 blocked_or_pending_candidates=3 ai_direct_fact_writes=0 kds_fact_writes=0 gfis_writes=0` |
| WAES dry-run validator | `waes_minimum_gates=pass cases=6 passed_cases=6 evaluated_gates=16 source_gate=covered evidence_gate=covered rag_gate=covered writeback_gate=covered revenue_gate=covered contribution_gate=covered sensitive_data_gate=covered real_writes=0 external_api_writes=0` |
| Fixture JSON 解析 | `kwe_fixture_json=pass` |
| Shared Types 编译检查 | `tsc -p packages/shared/tsconfig.json --noEmit` 通过 |
| API Contract 编译检查 | `tsc -p packages/api/tsconfig.json --noEmit` 通过 |
| OKF YAML / JSON 解析复查 | `okf_contract_parse=pass files=15` |
| 文档污染检查 | `document_pollution=pass` |
| KDS Token 安全检查 | `kds_token=pass fingerprint=bfd9553d` |
| LOOP 文档门禁 | `gate=pass` |
| 差异检查 | `git diff --check -- docs/harness/loops/loop-round-GPCF-KDS-DKS-065.md fixtures/kwe/minimum-workflow.json scripts/kwe/validate_kwe_minimum_workflow.py` 通过 |
| 敏感词与误升级扫描 | 通过，未发现 P0 8 份、正式写回已完成、收益已确认、production_ready、accepted/integrated、真实 KDS API 已同步或密钥模式 |

`loop_document_gate.py` 仍显示仓库级 `status_counts.missing=1` 和 `project_counts.missing=1`，该项为全仓既有元数据缺口。本轮新增的 KWE dry-run fixture 与脚本不触达真实外部系统，不生成真实 KWE WorkItem，不创建真实 KDS Fact，不写 GFIS/GPC。

## 7. 风险与边界

- KWE dry-run 只验证流程状态机，不证明真实业务事实已经确认。
- 本轮不创建真实 WorkItem、不创建真实 Fact、不写回 GFIS/GPC。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-066`：建立 GFIS Assistant no-write contract smoke。
- `GPCF-KDS-DKS-067`：建立 KDS v2 search/filter dry-run。
- `GPCF-KDS-DKS-068`：建立 Governance Ledger dry-run。
