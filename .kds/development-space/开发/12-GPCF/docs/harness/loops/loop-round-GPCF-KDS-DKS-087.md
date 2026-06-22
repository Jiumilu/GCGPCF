---
doc_id: GPCF-DOC-A9DAF1F48B
title: LOOP Round GPCF-KDS-DKS-087 - GC-Knowledge Fabric 委员会 DecisionRecord IO 与冻结边界
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-087.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-087.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-087 - GC-Knowledge Fabric 委员会 DecisionRecord IO 与冻结边界

## 1. 本轮目标

建立委员会 DecisionRecord 输入输出契约与争议冻结门禁，覆盖积分确认争议、收益分配争议、重大违规、悬赏结算争议、潜在产值转正式产值、跨单位贡献争议、第三方池子分配、项目内部争议、重大 RAG 强引用争议和收益池规则争议。

本轮只做本地契约、类型和 no-write validator，不写业务系统，不分配收益，不确认积分，不划拨额度，不结算悬赏，不替代 WAES gate。

## 2. 本轮输入资料

- `okf/committee-policy.yaml`
- `packages/shared/src/knowledge/decision.ts`
- `packages/shared/src/knowledge/dispute.ts`
- `packages/api/src/kwe/contracts.ts`
- `docs/gc-knowledge-fabric/four-pool-ledger-p0-policy.md`
- GC-Knowledge Fabric 综合实施方案：委员会机制与争议冻结要求

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/committee-decision-policy.md`
- `okf/committee-decision-policy.yaml`
- `packages/shared/src/knowledge/committee-decision.ts`
- `fixtures/governance/committee-decision-policy-smoke.json`
- `scripts/governance/validate_committee_decision_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 决策触发事项必须覆盖 10 类委员会事项。
- 输入字段必须覆盖 decision、tenant、issue、type、trigger、object refs、evidence、participants、voting、requester、freeze review。
- 输出字段必须覆盖 result、reason、actions、freeze scope、visibility、Harness evidence、effective state 和 no-write flags。
- 冻结范围必须覆盖 object、RAG admission、贡献积分、收益分配、额度划拨、悬赏结算、外部共享。
- 决策域必须是 governance。
- 委员会不得替代 WAES gate，不得直接写业务系统，不得直接分配收益或确认积分。
- 必须要求 Harness evidence，并限制外部账号只看授权视图。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| Committee Decision policy smoke | pass | `committee_decision_policy_smoke=pass triggers=10 input_fields=11 output_fields=12 freeze_scopes=7 decision_domain=governance waes_not_replaced=covered harness_evidence_required=true writes_business_system=0 writes_revenue_distribution=0 writes_score_confirmation=0 writes_quota_transfer=0 writes_bounty_settlement=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=15 okf_files=22 type_files=24 api_files=15 validator_files=22 fixture_files=22 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | 状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0 台账 smoke 全部 pass |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=21 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-087 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮委员会契约不代表任何真实委员会已经召开或形成决议。
- DecisionRecord 只能作为 governance evidence 和后续动作依据，不能直接写业务系统、收益台账、积分台账、额度台账或悬赏结算。
- 冻结范围只是治理门禁建议，实际冻结仍需 WAES/KWE/Harness 受控流程。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-088`：建立 sensitive metadata-only storage contract 与受控原件指针 validator。
- `GPCF-KDS-DKS-089`：建立 MMC AgentUsedKnowledge 调用证据契约与越权读取拦截 smoke。
- `GPCF-KDS-DKS-090`：建立 LOOP record schema 与 next-action closure gate。
