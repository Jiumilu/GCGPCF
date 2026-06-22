---
doc_id: GPCF-DOC-76D6EBBEAB
title: ODF 受控引入与治理试点方案
project: GPCF
related_projects: [WAES, KDS, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/odf-introduction-governance-plan.md
source_path: 09-status/odf-introduction-governance-plan.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# ODF 受控引入与治理试点方案

日期：2026-06-17

## 目标

建立 ODF 受控引入与治理试点闭环，在不影响当前 KDS Markdown 化、OKF 只读索引、Loop 文档治理、Harness evidence 和其它并行工作的前提下，验证 ODF 是否可以作为导入、交换和结构化承载层纳入 GlobalCloud 文档治理体系。

## ODF 定义

本试点将 ODF 定义为 `Object Document Frame`，即对象化文档框架。ODF 只保存文档对象的元数据、哈希、映射关系、敏感信息检查、状态和回滚提示，不复制受控 Markdown 正文。

ODF 不是：

- Git 源文档。
- KDS 真实知识主存。
- OKF 只读导航层。
- Loop 或 Harness evidence 的替代品。
- 验收状态或业务完成状态。

## 当前阶段

当前状态：`pilot_closed`

禁止状态：

- `full_rollout`
- `accepted`
- `integrated`

## 准入字段

| field | requirement |
| --- | --- |
| `source_uri` | 原始来源 URI 或 Git 路径 |
| `source_hash` | 原始来源 SHA-256 |
| `odf_hash` | ODF envelope SHA-256 |
| `markdown_hash` | 受控 Markdown SHA-256 |
| `conversion_method` | 转换方式，本轮为 `metadata-envelope-only` |
| `conversion_actor` | 转换执行者或工具角色 |
| `owner` | 责任项目或责任人 |
| `source_path` | Git 源路径 |
| `kds_path` | KDS `开发` 空间目标路径 |
| `sensitivity_check` | TOKEN、账号、客户敏感信息和正文复制检查 |
| `status` | 本轮仅允许 `pilot_sample`、`pilot_closed` 或 `rejected` |
| `rollback_hint` | 回滚方式，不得删除原始受控文档 |

## 试点样本

| sample_id | source_path | reason |
| --- | --- | --- |
| `ODF-PILOT-20260617-001` | `02-governance/GlobalCloud项目群文档防污染规则.md` | 低风险治理规则，已受控，适合验证敏感信息和污染边界 |
| `ODF-PILOT-20260617-002` | `02-governance/GlobalCloud项目群KDS开发空间安全规范.md` | KDS 安全规则，适合验证 TOKEN 不复制边界 |
| `ODF-PILOT-20260617-003` | `.okf/index.md` | OKF 只读导航入口，适合验证 ODF 与 OKF 的关系 |

## 证据文件

| evidence | path |
| --- | --- |
| ODF 样本 ledger Markdown | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.md` |
| ODF 样本 ledger JSON | `docs/harness/evidence/odf-pilot-sample-ledger-20260617.json` |
| ODF 样本 envelope | `docs/harness/evidence/odf-samples/*.json` |

## KDS/OKF/Loop 纳管规则

1. ODF envelope 进入 Git，仅作为 evidence 附件。
2. Markdown 源文档仍是事实源。
3. KDS 同步只同步受控文档和 evidence，不把 ODF 视为 KDS 主存替代。
4. OKF 只增加 ODF 试点入口，不复制 ODF 或 Markdown 正文。
5. Loop evidence 必须记录 ODF 样本 ledger 和本轮门禁结果。

## 推广门禁

进入下一阶段前必须满足：

1. 三个试点样本均具备完整准入字段。
2. `source_hash`、`markdown_hash`、`odf_hash` 可复算。
3. 污染检查通过。
4. KDS TOKEN 检查通过。
5. Loop 文档门禁通过。
6. KDS 本地镜像冲突检查通过。
7. KDS 同步计划通过。
8. 若发生真实 KDS 写入，必须保留 API ledger。

## 当前结论

ODF 受控试点已完成第一轮闭环。三个样本完成准入矩阵、hash 复算、OKF 导航、KDS 定向同步和 Loop 门禁验证。

当前允许进入下一阶段准备，但不得直接进入全量推广。下一阶段必须先扩大样本范围并继续使用定向 KDS 同步，避免影响其它并行工作线。

最终判定见 `docs/harness/evidence/odf-pilot-closure-report-20260617.md`。
