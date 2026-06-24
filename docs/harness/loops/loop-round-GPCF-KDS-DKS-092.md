---
doc_id: GPCF-DOC-C8DCDC7886
title: LOOP Round GPCF-KDS-DKS-092 - GC-Knowledge Fabric KDS ACL 外部共享视图
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-092.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-092.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-092 - GC-Knowledge Fabric KDS ACL 外部共享视图

## 1. 本轮目标

建立 KDS 对象 ACL 与外部共享视图 smoke，固化外部账号、合作单位、供应链节点、Brain/PKC 和 Agent 在读取 KDS 对象时的 tenant、domain、pool、ACL、脱敏、metadata-only、publication approval 与 WAES external_share_gate 边界。

本轮只做本地 OKF、文档、shared type、fixture 和 no-write validator，不写真实 ACL store，不创建真实外部账号，不发布真实外部共享视图，不写 KDS 对象，不写业务系统，不确认收益、积分、额度、悬赏或委员会裁决。

## 2. 本轮输入资料

- `packages/shared/src/knowledge/object.ts`
- `packages/shared/src/knowledge/source.ts`
- `packages/shared/src/knowledge/pool.ts`
- `okf/domain-policy.yaml`
- `okf/redaction-policy.yaml`
- `okf/waes-gate-policy.yaml`
- `fixtures/kds/search-dry-run.json`
- `scripts/kds/validate_kds_search_dry_run.py`
- `docs/harness/loops/loop-round-GPCF-KDS-DKS-091.md`
- GC-Knowledge Fabric 综合实施方案：外部伙伴只看授权视图、合作单位默认只能看自己的贡献/积分/额度/争议/悬赏/授权项目视图、supply_chain 跨供应商读取必须被 ACL 与 WAES 门禁限制

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/kds-acl-external-share-policy.md`
- `okf/kds-acl-external-share-policy.yaml`
- `packages/shared/src/knowledge/kds-acl-external-share.ts`
- `fixtures/kds/acl-external-share-policy-smoke.json`
- `scripts/kds/validate_kds_acl_external_share_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- ACL subject 必须覆盖 user、team、project、org、external_account、agent。
- ACL action 必须覆盖 metadata、redacted summary、full content、limited/safe RAG、candidate、promotion request、external share request。
- ACL 最小字段必须覆盖 subject、object、domain、visibility、actions、pool、project、supplyChainNode、expiry 和创建信息。
- 外部共享视图必须覆盖 visible/redacted fields、metadataOnly、RAG admission、WAES gate、publication approval、evidence 和 expiry。
- external_account 默认只能读取 metadata 与 redacted summary。
- metadata-only 敏感对象不得暴露 raw content。
- blocked RAG 与 T5 AI-only 内容不得作为正式外部共享事实。
- ACL pass 不等于 RAG 强引用、业务写回、收益或积分确认。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| KDS ACL external-share policy smoke | pass | `kds_acl_external_share_policy_smoke=pass subject_types=6 actions=8 acl_fields=15 external_view_fields=12 required_gates=7 metadata_only=true visible_raw_content=false blocked_objects=1 writes_acl_store=0 writes_external_share_permission=0 writes_publication_approval=0 writes_kds_object=0 writes_business_system=0 writes_revenue_or_score_confirmation=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=20 okf_files=27 type_files=29 api_files=15 validator_files=27 fixture_files=27 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | Harness evidence、LOOP closure、AgentUsedKnowledge、状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0 台账、委员会 DecisionRecord、敏感 metadata storage smoke 全部 pass |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=26 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-092 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮不代表真实 ACL、外部账号、外部共享门户或 KDS 权限已经写入。
- ACL external-share smoke 只验证本地契约，不证明任何真实外部访问已经放行。
- 外部共享仍必须经过 WAES external_share_gate、脱敏、publication approval 和 evidence。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-093`：建立 RAG response citation packet dry-run。
- `GPCF-KDS-DKS-094`：建立 KWE confirmation workpack 引用完整性 validator。
- `GPCF-KDS-DKS-095`：建立 GFIS document acceptance checklist schema 与 batch fixture。
