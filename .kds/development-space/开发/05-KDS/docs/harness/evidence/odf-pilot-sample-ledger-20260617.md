---
doc_id: GPCF-DOC-0F24C05984
title: ODF 试点样本准入台账
project: KDS
related_projects: [GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/odf-pilot-sample-ledger-20260617.md
source_path: docs/harness/evidence/odf-pilot-sample-ledger-20260617.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# ODF 试点样本准入台账

日期：2026-06-17

## 试点边界

- 不全量导入 ODF。
- 不批量改写现有文档结构。
- 不把 ODF 当作 Git、KDS、OKF 或 Loop evidence 的替代品。
- 不自动升级 `accepted` 或 `integrated`。

## 样本清单

| sample_id | source_path | source_hash | odf_hash | markdown_hash | owner | status |
| --- | --- | --- | --- | --- | --- | --- |
| `ODF-PILOT-20260617-001` | `02-governance/GlobalCloud项目群文档防污染规则.md` | `76add94d9481fbdb993707f0874d8bde8b0f2e13043643027b80711de7c84317` | `2405c97d8a34dca0df812602c90eab26a7869060efbae89fcb67c187c442a72e` | `76add94d9481fbdb993707f0874d8bde8b0f2e13043643027b80711de7c84317` | WAES | `pilot_sample` |
| `ODF-PILOT-20260617-002` | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | `31a84c070bfc15f79146a667d42fced62337b1606f2f7603f5172bc4856c9d2c` | `898d7ade933455868c91e23834e3eb4ecc54ae35cef61f0b71725c0ff9753a3d` | `31a84c070bfc15f79146a667d42fced62337b1606f2f7603f5172bc4856c9d2c` | WAES | `pilot_sample` |
| `ODF-PILOT-20260617-003` | `.okf/index.md` | `c2dace42e1cd8ce5e9693d800d71f8b64cf74d3eaeb42040a1c24a1a1d6f7103` | `63425cb11337dcf3f35e3dfca6a9417e1a2acbf4242dd552603a1941f5583cbd` | `c2dace42e1cd8ce5e9693d800d71f8b64cf74d3eaeb42040a1c24a1a1d6f7103` | GPCF | `pilot_sample` |

## 准入字段完整性

| field | result |
| --- | --- |
| `source_uri` | present |
| `source_hash` | present |
| `odf_hash` | present |
| `markdown_hash` | present |
| `conversion_method` | present |
| `conversion_actor` | present |
| `owner` | present |
| `source_path` | present |
| `kds_path` | present |
| `sensitivity_check` | present |
| `status` | present |
| `rollback_hint` | present |

## 结论

三个样本均为 metadata envelope 试点，不复制正文，不替代原始受控 Markdown。当前允许继续进入 ODF 试点纳管和门禁验证，不允许进入全量推广。
