---
doc_id: GPCF-DOC-6417D8DF39
title: GFIS WAS Source Record Negative Fixtures Evidence
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.md
source_path: docs/harness/evidence/gfis-was-source-record-negative-fixtures-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GFIS WAS Source Record Negative Fixtures Evidence

## Evidence ID

`GFIS-WAS-SOURCE-RECORD-NEGATIVE-FIXTURES-20260621`

## 结论

GPCF 已为 GFIS-WAS source-record 提交前扫描器补齐负例回放门禁。6 个负例全部在 GPCF evidence 内部回放，不写入 GFIS 接收目录；所有负例均被拒收，`accepted_fixture_count=0`。

## 负例覆盖

| 负例 | 拒收原因 |
|---|---|
| missing-was-fields | 缺 `objectFamily`、`assetDimension`、`kdsBacklink` 等 WAS/Ontology 字段 |
| wrong-dimension-and-flow | `assetDimension` 和 `flowType` 不匹配 WAS S01 |
| auto-promoted-valid-source-record | 跳过 `pending_business_verification` |
| kds-backlink-mismatch | GFIS backlink 与 WAS `kdsBacklink` 不一致 |
| invalid-hash | `source_record_hash` 不是 sha256-hex-64 |
| forbidden-source-kind | 使用 `gfis_demo` 等禁止来源 |

## 当前结果

| 字段 | 值 |
|---|---|
| negative_fixture_count | `6` |
| rejected_fixture_count | `6` |
| accepted_fixture_count | `0` |
| gfis_directory_writes | `0` |
| real_source_records | `0` |
| valid_source_records | `0` |
| runtime_primary_key_ready | `0` |
| review_queue | `0` |
| runtime_intake | `0` |
| waes_review | `0` |
| verified | `0` |

## 非声明

- 本 evidence 不向 GFIS 接收目录写入 fixture。
- 本 evidence 不创建真实 source-of-record。
- 本 evidence 不创建 runtime primary key、review queue、runtime intake、WAES review 或 verified artifact。
- 本 evidence 不证明 GFIS 真实业务 SOP E2E 完成。
- 本 evidence 不升级 accepted、integrated 或 production_ready。

## 下一步

收到真实客户订单原件或平台订单回执后，先运行提交前扫描器和负例门禁；只有真实候选通过 GFIS 原生字段、WAS/Ontology 字段、hash、backlink、来源类型和 lifecycle 检查，才允许进入 GFIS 后续人工核验与 runtime primary key 门禁。
