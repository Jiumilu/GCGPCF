---
doc_id: GPCF-DOC-A4D6B9E217
title: globalcloud-project-group-git-clean
project: GPCF
related_projects: [GPCF, KDS]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-project-group-git-clean/README.md
source_path: .codex/skills/globalcloud-project-group-git-clean/README.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# globalcloud-project-group-git-clean

目录：`.codex/skills/globalcloud-project-group-git-clean`

用途：保存项目群 17 个 Git 仓库全量 clean 门禁技能、只读检查脚本和 Loop 接入说明。

KDS 空间：`开发`

关联项目：GPCF

受控规则：

- 本目录新增 Markdown 文档必须重新运行 `python3 tools/kds-sync/document_control.py`。
- 当前有效文档使用 `controlled` 或 `operational_controlled`；草案使用 `draft`；历史证据使用 `archive`。
- 本技能只做 Git 状态审计，不自动提交、推送、stash、reset、clean 或删除文件。

## 文档清单

| doc_id | title | source_path | project | status |
| --- | --- | --- | --- | --- |
| GPCF-DOC-A4D6B9E217 | globalcloud-project-group-git-clean | .codex/skills/globalcloud-project-group-git-clean/README.md | GPCF | operational_controlled |
| GPCF-DOC-7F9C2E9A61 | GlobalCloud Project Group Git Clean | .codex/skills/globalcloud-project-group-git-clean/SKILL.md | GPCF | operational_controlled |
