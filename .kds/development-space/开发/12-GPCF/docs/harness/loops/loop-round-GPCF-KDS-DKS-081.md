---
doc_id: GPCF-DOC-36DBE4BB63
title: LOOP Round GPCF-KDS-DKS-081 - GC-Knowledge Fabric 统一状态机策略
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-081.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-081.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-081 - GC-Knowledge Fabric 统一状态机策略

## 1. 本轮目标

根据 GC-Knowledge Fabric 完整评审问题清单中“状态机还不够硬”的 P0 缺口，建立统一状态机与状态提升规则的受控文档、OKF policy、Shared Type 和本地 no-write validator。

本轮只固化状态语义、提升 actor、hard boundaries 与 no-write 断言，不把任何对象提升为正式事实，不触发 GFIS/GPC/ERP/MES 写回，不确认收益、积分、额度、悬赏或委员会裁决。

## 2. 本轮输入资料

- `okf/flow-policy.yaml`
- `okf/ontology.yaml`
- `okf/knowledge-object.schema.json`
- `packages/shared/src/knowledge/object.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- GC-Knowledge Fabric 综合实施方案完整评审与问题清单：问题 1 状态机硬化建议

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/status-machine-policy.md`
- `okf/status-machine-policy.yaml`
- `packages/shared/src/knowledge/status-machine.ts`
- `fixtures/status-machine/status-machine-policy-smoke.json`
- `scripts/status_machine/validate_status_machine_policy_smoke.py`

## 4. 本轮修改工程文件

- `packages/shared/src/knowledge/object.ts`
- `packages/shared/src/knowledge/index.ts`
- `okf/ontology.yaml`
- `okf/knowledge-object.schema.json`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 生命周期状态必须覆盖 `draft`、`candidate`、`reviewing`、`repair_required`、`evidence_ready`、`verified`、`accepted`、`published`、`frozen`、`superseded`、`archived`。
- schema、ontology、Shared Type 与 OKF status machine policy 的状态集合必须一致。
- AI 只能进入 `draft`、`candidate`、`repair_required`，不能提升为 `verified`、`accepted`、`published`。
- LOOP 不能提升为 `verified`、`accepted`、`published`。
- 正式写回和收益确认必须要求 `accepted`。
- `frozen`、`superseded`、`archived` 不得进入强引用、正式写回或收益确认。
- 本轮 validator 必须证明 no-write：KDS fact、业务系统、收益分配和外部 API 写入均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| 状态机 policy smoke | pass | `status_machine_policy_smoke=pass states=11 promotion_rules=10 terminal_states=superseded,archived ai_boundary=covered loop_boundary=covered formal_writeback_requires_accepted=true revenue_confirmation_requires_accepted=true template_is_not_fact=true writes_kds_fact=0 writes_business_system=0 writes_revenue_distribution=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=9 okf_files=16 type_files=18 api_files=15 validator_files=16 fixture_files=16 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=15 json_files=1` |
| 文档治理门禁 | pass | 首次运行因新增 `docs/gc-knowledge-fabric/` 目录缺 README 出现 `missing_readme_dirs=1`，已补 `docs/gc-knowledge-fabric/README.md` 后重跑通过：`document_pollution=pass`、`kds_token=pass fingerprint=bfd9553d`、`loop_document_gate.py` 输出 `gate=pass`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-081 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮状态机只是契约与本地 validator，不代表任何真实对象状态已提升。
- `accepted` 仍必须由授权人或委员会确认，不能由 AI、LOOP、Brain、PKC、dashboard 或 validator 自动完成。
- `formal_writeback_requires_accepted=true` 只是门禁规则，不代表 GFIS/GPC 写回已发生。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-082`：建立核心对象关系图与最小字段契约，覆盖 Source/Evidence/KnowledgeObject/FactCandidate/WAESGateResult/KWE/Decision/Writeback/Contribution/Revenue/Harness/LOOP 的关系链。
- `GPCF-KDS-DKS-083`：建立 WAES Gate 输入输出契约与 hard-stop reason code validator。
- `GPCF-KDS-DKS-084`：建立 GFIS Writeback Sandbox 契约与 no-write/sandbox/approved-write 边界 smoke。
