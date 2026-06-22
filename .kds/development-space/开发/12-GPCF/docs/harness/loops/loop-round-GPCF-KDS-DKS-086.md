---
doc_id: GPCF-DOC-C74468101A
title: LOOP Round GPCF-KDS-DKS-086 - GC-Knowledge Fabric Four-pool P0 Ledger Boundary
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-086.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-086.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-086 - GC-Knowledge Fabric Four-pool P0 Ledger Boundary

## 1. 本轮目标

根据 GC-Knowledge Fabric 完整评审问题清单中“四池机制 P0 应压缩”的建议，建立知识积分池、收益池、AI 额度池、知识悬赏池的 P0 台账边界：只允许登记、候选、审查、冻结和证据引用，不允许自动确认、自动分配、自动划拨或自动结算。

本轮只做本地契约、类型和 no-write validator，不确认积分，不分配收益，不划拨额度，不结算悬赏。

## 2. 本轮输入资料

- `okf/contribution-policy.yaml`
- `okf/revenue-policy.yaml`
- `okf/quota-policy.yaml`
- `okf/bounty-policy.yaml`
- `packages/shared/src/knowledge/contribution.ts`
- `packages/shared/src/knowledge/revenue.ts`
- `packages/shared/src/knowledge/quota.ts`
- `packages/shared/src/knowledge/bounty.ts`
- GC-Knowledge Fabric 综合实施方案完整评审与问题清单：问题 7 四池机制 P0 压缩建议

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/four-pool-ledger-p0-policy.md`
- `okf/four-pool-ledger-p0-policy.yaml`
- `packages/shared/src/knowledge/four-pool-ledger-p0.ts`
- `fixtures/governance/four-pool-ledger-p0-policy-smoke.json`
- `scripts/governance/validate_four_pool_ledger_p0_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 必须覆盖知识积分池、收益池、AI 额度池、知识悬赏池四池。
- 知识积分池只允许登记贡献、候选分、确认状态、证据引用和冻结，不允许自动确认/扣减/兑换。
- 收益池只允许登记收入口径、候选分配、审查状态、证据引用和冻结，不允许自动分配、潜在转正式、无到账分配。
- AI 额度池只允许登记额度类型、owner、amount、usedAmount、收益池资格，不允许自购额度入统一池或自动划拨。
- 悬赏池只允许登记缺口、提交、验收状态、争议期、候选奖励，不允许自动结算、跳过争议期或 AI 直接验收。
- no-write 断言必须证明积分确认、收益分配、额度划拨、悬赏结算和外部 API 写入均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| 四池 P0 台账 smoke | pass | `four_pool_ledger_p0_policy_smoke=pass pools=4 formal_revenue_requires_cash=true potential_no_auto_promote=covered self_purchased_quota_excluded=covered bounty_dispute_window_required=covered writes_score_confirmation=0 writes_revenue_distribution=0 writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=14 okf_files=21 type_files=23 api_files=15 validator_files=21 fixture_files=21 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 状态机、对象关系、WAES IO、RAG 强度、GFIS 沙箱回归 | pass | `status_machine_policy_smoke=pass`；`object_relationship_policy_smoke=pass`；`waes_gate_io_policy_smoke=pass`；`rag_citation_strength_policy_smoke=pass`；`gfis_writeback_sandbox_policy_smoke=pass` |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=20 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-086 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮四池台账规则不代表任何积分、收益、额度或悬赏已经确认、分配、划拨或结算。
- 正式收益仍以到账为准；开票、潜在收益、渠道机会和知识潜在价值不能自动进入正式分配。
- 自购 AI 额度不得进入统一收益池。
- AI 初审只作为建议，不能替代悬赏验收或争议期。

## 8. 下一轮建议

- `GPCF-KDS-DKS-087`：建立 Committee DecisionRecord 输入输出契约与争议冻结门禁 smoke。
- `GPCF-KDS-DKS-088`：建立 sensitive metadata-only storage contract 与受控原件指针 validator。
- `GPCF-KDS-DKS-089`：建立 MMC AgentUsedKnowledge 调用证据契约与越权读取拦截 smoke。
