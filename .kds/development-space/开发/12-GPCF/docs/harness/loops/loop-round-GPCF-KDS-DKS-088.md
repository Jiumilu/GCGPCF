---
doc_id: GPCF-DOC-89C823A706
title: LOOP Round GPCF-KDS-DKS-088 - GC-Knowledge Fabric 敏感元数据存储契约
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-088.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-088.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# LOOP Round GPCF-KDS-DKS-088 - GC-Knowledge Fabric 敏感元数据存储契约

## 1. 本轮目标

建立敏感资料 metadata-only 入库契约与受控原件指针 validator，覆盖合同敏感条款、金融凭证、POD 原件、质量争议、客户/供应商身份、凭证与密钥、未发布政策解释、商业报价与佣金等高风险资料。

本轮只做本地契约、类型、fixture 和 no-write validator，不写真实 KDS，不写业务系统，不暴露原文，不同步受控原件，不把 metadata-only 内容升级为 RAG 强引用。

## 2. 本轮输入资料

- `okf/redaction-policy.yaml`
- `okf/rag-admission-policy.yaml`
- `packages/shared/src/knowledge/evidence.ts`
- `packages/shared/src/knowledge/source.ts`
- `docs/gc-knowledge-fabric/rag-citation-strength-policy.md`
- `docs/gc-knowledge-fabric/waes-gate-io-policy.md`
- GC-Knowledge Fabric 综合实施方案：敏感资料 metadata-only、受控原件、哈希、摘要、权限、证据链位置与可引用范围要求

## 3. 本轮新增工程文件

- `docs/gc-knowledge-fabric/sensitive-metadata-storage-policy.md`
- `okf/sensitive-metadata-storage-policy.yaml`
- `packages/shared/src/knowledge/sensitive-metadata-storage.ts`
- `fixtures/waes/sensitive-metadata-storage-policy-smoke.json`
- `scripts/waes/validate_sensitive_metadata_storage_policy_smoke.py`

## 4. 本轮修改工程文件

- `docs/gc-knowledge-fabric/README.md`
- `packages/shared/src/knowledge/index.ts`
- `fixtures/coverage/okf-types-api-validator-coverage.json`
- `scripts/coverage/validate_okf_types_api_validator_coverage.py`

## 5. 本轮验收口径

- 敏感资料分类必须覆盖 8 类 P0 敏感内容。
- 存储模式必须覆盖 metadata_only、redacted_copy、controlled_original、blocked。
- metadata-only 元数据字段必须覆盖编号、类型、标题、摘要、哈希、来源、证据、权限、受控原件指针、RAG 边界、WAES gate、保留策略、脱敏状态和审计引用。
- metadata-only 不允许写入 raw content。
- controlled original 不允许把原文写入 KDS，只能保存受控空间指针、哈希和权限边界。
- 默认 RAG 准入必须是 `sensitive_metadata_only`，不得自动转为 safe。
- 凭证、Token、密钥类内容不得进入文档、evidence 或外部 API。
- 本轮 validator 必须证明 business write、external API write、secret write、raw content write 均为 0。

## 6. 本轮验证结果

| 检查项 | 结果 | 证据摘要 |
|---|---|---|
| Sensitive metadata storage policy smoke | pass | `sensitive_metadata_storage_policy_smoke=pass sensitive_classes=8 storage_modes=4 metadata_fields=14 metadata_only_raw_content=false controlled_original_raw_content_in_kds=false default_rag=sensitive_metadata_only writes_raw_content_to_kds=0 writes_secret_to_docs=0 writes_secret_to_evidence=0 writes_external_api=0` |
| 覆盖矩阵 | pass | `okf_types_api_validator_coverage=pass coverage_items=16 okf_files=23 type_files=25 api_files=15 validator_files=23 fixture_files=23 missing_files=0 no_write=covered business_writes=0 external_api_writes=0` |
| TypeScript 类型检查 | pass | `tsc -p packages/shared/tsconfig.json --noEmit` 与 `tsc -p packages/api/tsconfig.json --noEmit` 均无报错 |
| 前序专项回归 | pass | 状态机、对象关系、WAES IO、RAG 强度、GFIS 写回沙箱、四池 P0 台账、委员会 DecisionRecord smoke 全部 pass |
| 既有 API route no-write smoke | pass | Brain/PKC、Governance、GFIS、KWE、WAES、KDS v2 endpoint smoke 全部 pass，真实写入计数均为 0 |
| 既有 dry-run validators | pass | LOOP Dashboard、Brain/PKC entry contract、GFIS document acceptance E2E、GFIS assistant no-write、Governance ledger、KDS search、WAES minimum gates、KWE minimum workflow 全部 pass |
| OKF parse | pass | `okf_parse=pass yaml_files=22 json_files=1` |
| 文档治理门禁 | pass | `document_pollution=pass`；`kds_token=pass fingerprint=bfd9553d`；`loop_document_gate.py` 输出 `gate=pass`、`missing_metadata=0`、`missing_readme_dirs=0` |
| LOOP 文档门禁残留项 | known gap | `status_counts.missing=1`、`project_counts.missing=1` 为既有仓库元数据缺口，本轮未扩大该缺口 |
| 差异检查 | pass | `git diff --check -- <DKS-088 touched files>` 无输出 |
| 敏感/误升级关键词扫描 | pass | 未命中生产就绪、验收集成状态、真实同步、Token 或密钥类误升级关键词 |

## 7. 风险与边界

- 本轮只定义 metadata-only 与受控原件指针契约，不代表任何真实敏感原件已经入库或同步。
- metadata-only 只能提供编号、摘要、哈希、权限、证据链位置和引用边界，不提供原文。
- 受控原件仍留在受控空间，KDS 不保存合同敏感条款、金融凭证、POD 原件、质量争议原文或密钥。
- 当前仓库已有大量非本轮脏变更，本轮不回滚、不整理无关文件。

## 8. 下一轮建议

- `GPCF-KDS-DKS-089`：建立 MMC AgentUsedKnowledge 调用证据契约与越权读取拦截 smoke。
- `GPCF-KDS-DKS-090`：建立 LOOP record schema 与 next-action closure gate。
- `GPCF-KDS-DKS-091`：建立 Harness evidence 引用完整性 validator。
