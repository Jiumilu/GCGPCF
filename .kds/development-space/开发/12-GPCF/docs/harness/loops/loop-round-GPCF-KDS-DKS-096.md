---
doc_id: GPCF-DOC-C860998BF2
title: LOOP Round GPCF-KDS-DKS-096 - GC-Knowledge Fabric 收益贡献归因包
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-096.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-096.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-096 - GC-Knowledge Fabric 收益贡献归因包

## 1. 本轮目标

建立 Revenue/Contribution attribution packet dry-run，将收益记录、贡献记录、evidence、WAES gate、委员会/冻结触发原因组织成可审查候选归因包。

本轮只做本地 OKF、文档、shared type、fixture 和 validator，不确认积分，不分配收益，不转移 AI 额度，不结算悬赏，不写 GFIS/GPC/ERP/MES，不写 KDS 正式事实，不调用外部 API。

## 2. 本轮输入资料

- `packages/shared/src/knowledge/contribution.ts`
- `packages/shared/src/knowledge/revenue.ts`
- `packages/shared/src/knowledge/four-pool-ledger-p0.ts`
- `docs/gc-knowledge-fabric/four-pool-ledger-p0-policy.md`
- `docs/gc-knowledge-fabric/committee-decision-policy.md`
- `fixtures/governance/ledger-dry-run.json`
- `scripts/governance/validate_governance_ledger_dry_run.py`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-095.md`
- GC-Knowledge Fabric 综合实施方案：有收入才进正式产值、开票仅财务统计、潜在收益不得自动转正式、委员会裁决与冻结、AI 只生成候选、收益/积分必须区分候选与确认状态

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/revenue-contribution-attribution-packet-policy.md`
- `okf/revenue-contribution-attribution-packet-policy.yaml`
- `packages/shared/src/knowledge/revenue-contribution-attribution-packet.ts`
- `fixtures/governance/revenue-contribution-attribution-packet-dry-run.json`
- `scripts/governance/validate_revenue_contribution_attribution_packet.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 归因包必须是候选审查材料，不是收益分配结果。
- 正式收益候选必须满足 `formal_revenue + cash_received + evidence + WAES gate + 已确认贡献`。
- 开票收入只能作为财务统计，不得进入收益分配候选。
- 潜在收益不得自动转正式收益。
- 渠道机会只能作为渠道贡献候选或参考，不得直接分配。
- 跨单位争议、潜在转正式、重大违规必须触发委员会或冻结建议。
- 所有 no-write 计数必须为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| Revenue/Contribution attribution packet | pass | `revenue_contribution_attribution_packet=pass packets=5 formal_distribution_candidates=1 invoiced_statistical_only=1 potential_not_promoted=1 channel_reference_only=1 committee_required=2 freeze_recommended=1 score_confirmations=0 revenue_distributions=0 quota_transfers=0 bounty_settlements=0 business_writes=0 external_api_writes=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=24 okf_files=31 type_files=33 api_files=15 validator_files=31 fixture_files=31 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| OKF parse | pass | `okf_parse=pass yaml_files=30 json_files=1` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | DKS-095 GFIS checklist、DKS-094 KWE workpack、DKS-093 RAG citation packet、KDS ACL、Harness evidence、LOOP closure、AgentUsedKnowledge、状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0、委员会 DecisionRecord、敏感 metadata storage、Brain/PKC/Governance/GFIS/KWE/WAES/KDS endpoint no-write、LOOP Dashboard、Brain/PKC entry、GFIS acceptance E2E、GFIS assistant、Governance ledger、KDS search、WAES gates、KWE workflow 全部 pass |
| 文档治理门禁 | pass | `document_pollution=pass`、`kds_token=pass fingerprint=bfd9553d`、`loop_document_gate gate=pass repo_md=1270 kds_md=1232 missing_metadata=0 missing_readme_dirs=0`；既有 `status_counts.missing=1`、`project_counts.missing=1` 为仓库台账残留，本轮未新增 |
| 差异检查 | pass | `git diff --check -- <DKS-096 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 对本轮触达文件扫描 P0 文档误述、正式写回/收益确认误述、生产就绪/验收集成误升级、真实同步误述、TOKEN/密钥模式，均无命中 |

## 7. 风险与边界

- 本轮不代表收益分配、积分确认、额度转移、悬赏结算或委员会裁决完成。
- `distribution_candidate` 仍只是可审查候选材料，不能直接触发真实分配。
- 开票、潜在、渠道、知识价值只可作为统计、机会、贡献或参考记录。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-097`：建立 KWE promotion request no-write dry-run。
- `GPCF-KDS-DKS-098`：建立 GFIS writeback candidate batch diff validator。
- `GPCF-KDS-DKS-099`：建立 Brain/PKC revenue attribution read model contract。
