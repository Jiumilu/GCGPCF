---
doc_id: GPCF-DOC-C039431381
title: KDS Sync Tools
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: tools
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/tools/kds-sync/README.md
source_path: tools/kds-sync/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# KDS Sync Tools

用途：维护 GlobalCloud GPCF 文档控制体系、目录 README、KDS `开发` 空间本地镜像和同步台账。

运行：

```bash
python3 tools/kds-sync/document_control.py
```

输出：

- `09-status/globalcloud-document-control-register.md`
- `09-status/kds-development-space-sync-register.md`
- `09-status/document-deprecation-register.md`
- `.kds/development-space/开发/`
- `.kds/local-mirror-ledger.jsonl`
- `.kds/sync-ledger.jsonl`

## 门禁"合法红"说明（2026-10-12 核实）

`validate_*.py` 里有一批门禁**在正常状态下也会红**，因为它们断言的是**项目群整体活状态**，
而不是某个文档的内容。以下两类不要当成缺陷去"修"：

### 1. 项目群"干净且已同步"类

`validate_project_group_dev_p0_dirty_classification_20260626`、
`validate_project_group_dev_p0_blocker_reduction_20260626`、
`validate_project_group_dirty_classification_p0a_20260626`、
`validate_project_group_p0c_minimal_validation_20260626` 等，统一调用
`.codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py`，
要求**全部 17 仓**满足：无 ahead / 无 behind / 无缺失 / 无敏感路径漂移。

只要有**任一工作流在途中**（例如某仓有未推送提交、或并行会话正在改文件），这些门禁必然红。
**这不代表记录陈旧**——记录是对的，是活状态不满足。除非该工作流收口，不要为它们改记录或改门禁。

### 2. 快照自引用类

`validate_project_group_live_status_snapshot_20260626` 把"本仓 dirty"同时记进快照与实时状态，
因此**提交后读取必然 stale、不提交才 PASS**。它是 pre-commit 门禁，不是回归。

### 3. 跨仓派发型门禁有副作用

`validate_loop_project_group_gate_readiness` 会**逐仓派发执行各仓的 loop gate**，
被派发的仓其 gate 会重写自家 evidence（典型：只改 `generated_at`，每文件 ±1 行）。
因此跑一次该门禁，就会在 `GlobalCloud GFIS` 等仓制造一轮未提交漂移——
**这是已知的循环性副作用，不是"别人在改文件"**。
