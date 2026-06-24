---
doc_id: GPCF-DOC-82997F4582
title: Loop Round - CodeGraph GFIS 残余 added Locator
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-LOCATOR-008.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round - CodeGraph GFIS 残余 added Locator

## 输入

- 上一轮：`GPCF-CODEGRAPH-DEV-EXECUTION-GFIS-RESIDUAL-DRIFT-007`
- GFIS CodeGraph：`pendingChanges.added=1`
- 约束：只读定位，不删除、不 stage、不 commit、不 push、不 deploy。

## 动作

- 新增只读 locator 脚本。
- 读取 GFIS `codegraph status --json`。
- 读取 GFIS `codegraph files --json`。
- 读取 GFIS Git 未跟踪文件列表。
- 比对未跟踪可扫描文件是否缺失于 CodeGraph 索引。

## 输出

- `tools/kds-sync/locate_gfis_codegraph_residual_added.py`
- `docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.json`
- `docs/harness/evidence/codegraph-dev-execution-gfis-residual-locator-20260622.md`
- `tools/kds-sync/validate_codegraph_dev_execution_gfis_residual_locator.py`

## 检查

必须通过：

```bash
python3 tools/kds-sync/validate_codegraph_dev_execution_gfis_residual_locator.py
```

检查点：

- `untracked_codegraph_scannable_not_indexed_count=0`
- `exact_pending_file_identified=false`
- `codegraph_sync_only_closure=false`
- 未执行 GFIS 文件清理。

## 反馈

下一步若要继续闭合，需要问答式授权：

```text
是否授权执行 GFIS CodeGraph clean reindex audit?
```

推荐答案：

```text
暂不授权 clean reindex，先保留 locator 证据并继续项目群治理收口。
```
