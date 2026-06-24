---
doc_id: GPCF-DOC-F57E6B4E33
title: Loop Round GPCF-CODEGRAPH-PROJECT-GROUP-001
project: GPCF
related_projects: [GFIS, GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-001.md
source_path: docs/harness/loops/loop-round-GPCF-CODEGRAPH-PROJECT-GROUP-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-CODEGRAPH-PROJECT-GROUP-001

## 输入

- 用户要求完成整个项目群代码图谱生成。
- 用户明确要求新增项目 `GlobalCloud Studio` 纳入项目群、代码图谱与 Loop 工程体系。

## 动作

- 安装并验证 `@colbymchenry/codegraph@1.0.1` CLI。
- 关闭 CodeGraph telemetry。
- 发现 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1` 下 13 个 Git 仓库。
- 对 13 个仓库执行 `codegraph init` / 必要时 `codegraph sync`。
- 将 `.codegraph/` 写入各仓 `.git/info/exclude`，避免索引缓存进入 Git。
- 在 GPCF 总控侧新增项目群覆盖登记、evidence、validator，并把 Studio 纳入状态矩阵与 Loop 控制板。

## 输出

- `02-governance/loop/LOOP_CODEGRAPH_PROJECT_GROUP_COVERAGE.md`
- `docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.json`
- `docs/harness/evidence/loop-codegraph-project-group-coverage-20260620.md`
- `tools/kds-sync/validate_loop_codegraph_project_group_coverage.py`

## 检查

- `project_group_repo_count=13`
- `studio_included=true`
- 每个仓库 `.codegraph/` 存在。
- 每个仓库 `git status --short -- .codegraph` 为 0 项。
- CodeGraph 统计可读，且 Studio 统计为 `files=764 nodes=14141 edges=46339`。

## 反馈

本轮只完成本地代码图谱与治理登记。GFIS 仍保持真实业务 evidence repair 边界；Studio 作为新项目纳入图谱和 Loop 工程，不代表交付完成、验收完成、accepted、integrated 或 production_ready。
