---
doc_id: GPCF-DOC-B32E9CBB6A
title: CodeGraph GFIS 残余 added Locator 证据
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.md
source_path: docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph GFIS 残余 added Locator 证据

本证据对应 `GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008`。

## 结论

GFIS `pendingChanges.added=1` 未能映射到 Git 未跟踪且 CodeGraph 可扫描但未入索引的文件。

```text
pre_sync_pendingChanges.added=1
post_sync_pendingChanges.added=1
untracked_files_total=226
untracked_codegraph_scannable_files=73
untracked_codegraph_scannable_not_indexed_count=0
exact_pending_file_identified=false
locator_conclusion=pending_added_not_mapped_to_untracked_scannable_file
```

## Sync Probe

locator 再次执行 `codegraph sync`，输出仍包含：

```text
Added: 1
0 nodes
```

但 `codegraph files --json` 中已有 1022 个索引文件，且 73 个可扫描未跟踪文件都已在索引中。

## 解释

当前最合理解释是 CodeGraph 工具状态或非 Git 扫描口径残差，而不是一个明确的未跟踪脚本/配置文件漏入索引。

本轮不执行：

- 删除 GFIS 未跟踪文件。
- stage GFIS 文件。
- commit。
- push。
- deploy。
- clean reindex。

## 授权问答

**Q：下一步如果要继续闭合，需要什么授权？**  
A：需要明确授权是否执行 GFIS CodeGraph clean reindex audit。

**Q：建议授权吗？**  
A：建议暂不授权 clean reindex，先保留 locator 证据并继续项目群治理收口。

**Q：为什么？**  
A：clean reindex 会重建 `.codegraph/` 本地索引，虽不触碰 Git tracked 文件，但会改变本地索引状态；当前已经证明残余 added 不是普通未跟踪可扫描文件缺索引。

## 下一轮

`GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-TOOL-STATE-AUDIT-009`
