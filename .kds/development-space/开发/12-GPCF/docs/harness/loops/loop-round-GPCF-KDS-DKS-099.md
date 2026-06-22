---
doc_id: GPCF-DOC-0193F30472
title: LOOP Round GPCF-KDS-DKS-099 - GC-Knowledge Fabric Brain PKC 收益归因读模型
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-099.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-099.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-099 - GC-Knowledge Fabric Brain PKC 收益归因读模型

## 1. 本轮目标

建立 Brain/PKC revenue attribution read model dry-run，让 Brain 收益/贡献中心和 PKC 个人/团队入口可以只读展示归因包、收益候选、贡献候选、WAES/KWE/委员会/冻结状态和可见性边界。

本轮只做本地 OKF、文档、shared type、fixture 和 validator，不确认积分，不分配收益，不提升潜在收益，不改 KDS lifecycle，不写 WAES/KWE，不写业务系统，不调用外部 API。

## 2. 本轮输入资料

- `packages/api/src/brain/contracts.ts`
- `packages/api/src/pkc/contracts.ts`
- `packages/api/src/brain/routes.ts`
- `packages/api/src/pkc/routes.ts`
- `fixtures/brain-pkc/endpoint-no-write-smoke.json`
- `fixtures/brain-pkc/entry-contract-smoke.json`
- `docs/gc-knowledge-fabric/revenue-contribution-attribution-packet-policy.md`
- `packages/shared/src/knowledge/revenue-contribution-attribution-packet.ts`
- `fixtures/governance/revenue-contribution-attribution-packet-dry-run.json`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-098.md`
- GC-Knowledge Fabric 综合实施方案：Brain 多角色工作台、PKC 个人/团队入口、收益/贡献中心、委员会与冻结、合作单位默认只能看到自己的贡献/积分/额度/争议状态

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/brain-pkc-revenue-attribution-read-model-policy.md`
- `okf/brain-pkc-revenue-attribution-read-model-policy.yaml`
- `packages/shared/src/knowledge/brain-pkc-revenue-attribution-read-model.ts`
- `fixtures/brain-pkc/revenue-attribution-read-model-dry-run.json`
- `scripts/brain_pkc/validate_revenue_attribution_read_model.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- Read model 只能展示引用、聚合、授权明细或 masked 跨单位信息。
- Brain governance aggregate 不得暴露贡献明细。
- Brain committee review 必须 committee authorized。
- PKC 默认只能 own_only 或 project_authorized。
- masked cross-unit 视图不得暴露其他单位 contribution id。
- 所有视图必须阻断 score confirmation、revenue distribution、potential promotion、WAES override、committee completion、business write、KDS lifecycle mutation 和 external API。
- 所有 no-write 计数必须为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| Brain/PKC revenue attribution read model | pass | `brain_pkc_revenue_attribution_read_model=pass views=4 brain_views=2 pkc_views=2 masked_views=2 committee_authorized_views=1 own_only_views=1 blocked_actions=32 cross_unit_leaks=0 writes_kds_lifecycle=0 writes_waes_gate_result=0 writes_kwe_work_item=0 writes_score_confirmation=0 writes_revenue_distribution=0 writes_business_system=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=27 okf_files=34 type_files=36 api_files=15 validator_files=34 fixture_files=34 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| OKF parse | pass | `okf_parse=pass yaml_files=33 json_files=1` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | DKS-098 GFIS batch diff、DKS-097 KWE promotion request、DKS-096 收益/贡献归因包、DKS-095 GFIS checklist、DKS-094 KWE workpack、DKS-093 RAG citation packet、KDS ACL、Harness evidence、LOOP closure、AgentUsedKnowledge、状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0、委员会 DecisionRecord、敏感 metadata storage、Brain/PKC/Governance/GFIS/KWE/WAES/KDS endpoint no-write、LOOP Dashboard、Brain/PKC entry、GFIS acceptance E2E、GFIS assistant、Governance ledger、KDS search、WAES gates、KWE workflow 全部 pass |
| 文档治理门禁 | pass | `document_pollution=pass`、`kds_token=pass fingerprint=bfd9553d`、`loop_document_gate gate=pass repo_md=1290 kds_md=1299 missing_metadata=0 missing_readme_dirs=0`；既有 `status_counts.missing=1`、`project_counts.missing=1` 为仓库台账残留，本轮未新增 |
| 差异检查 | pass | `git diff --check -- <DKS-099 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 对本轮触达文件扫描 P0 数量误述、业务写回/收益确认/收益分配/积分确认误述、状态误升级、生产就绪/验收集成误升级、真实同步误述、TOKEN/密钥模式，均无命中 |

## 7. 风险与边界

- 本轮不代表 Brain/PKC 真实 UI 或服务已完成。
- Read model pass 只证明只读视图结构、ACL/掩码和 no-write 边界可机检。
- 委员会、收益分配、贡献积分确认、潜在收益转正式收益仍必须走后续 WAES/KWE/人工/委员会/Harness evidence 链路。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-100`：建立 KDS object lifecycle transition read model and audit packet。
- `GPCF-KDS-DKS-101`：建立 GFIS writeback approval preflight no-write checklist。
- `GPCF-KDS-DKS-102`：建立 Committee review queue read model。
