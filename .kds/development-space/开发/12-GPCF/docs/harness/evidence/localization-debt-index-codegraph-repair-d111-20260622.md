---
doc_id: GPCF-DOC-LOCALIZATIONDEBTINDEXCODEGRAPHREPAIRD11120260622
title: 索引与 CodeGraph 文档 D111 中文化修复证据
project: GPCF
related_projects: [WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/localization-debt-index-codegraph-repair-d111-20260622.md
source_path: docs/harness/evidence/localization-debt-index-codegraph-repair-d111-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# 索引与 CodeGraph 文档 D111 中文化修复证据

## Evidence ID

`LOCALIZATION-DEBT-INDEX-CODEGRAPH-REPAIR-D111-20260622`

## 结论

D111 对 `docs/harness/evidence/evidence-index.md` 与 `docs/codegraph/codegraph-loop-integration.md` 做 scoped 中文化修复，并在 scoped `document_control` 阶段补齐缺失的 `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md` 受控文件。

修复后：

- 当前全仓中文化门禁命中为 `23`。
- 本轮目标组样本命中从 `4` 收敛到 `3`。
- 本轮清掉了 `codegraph-loop-integration.md` 的单行英文命中，并清理了 `evidence-index.md` 中一组早期索引项；但该聚合索引在更靠后的区段仍持续暴露新的英文行命中，因此 D111 只能记为部分收敛，而不是完全收口。
- 本轮只修复索引标题、索引项文案和 CodeGraph evidence 字段说明，不改动证据结论、验证结果或业务状态。

## 修复范围

- `docs/harness/evidence/evidence-index.md`
- `docs/codegraph/codegraph-loop-integration.md`

## 边界

- `real_kds_api_write=false`
- `business_system_writeback=false`
- `status_upgrade=false`
- `accepted=false`
- `integrated=false`
- `production_ready=false`
- `gfis_real_business_lane=repair_required`

## 后续

本轮之后，sample findings 的剩余重点仍包括 `evidence-index.md` 后段的滚动聚合条目、`docs/harness/evidence/was-real-source-record-monitor-044-20260622.md`、`openspec/changes/kds-production-hardening/*`、`templates/*` 以及 `02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md`。`docs/codegraph/codegraph-loop-integration.md` 已不再出现在当前 sample findings。
