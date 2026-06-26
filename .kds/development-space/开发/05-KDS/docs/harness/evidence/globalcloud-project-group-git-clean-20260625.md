---
doc_id: GPCF-DOC-PROJECT-GROUP-GIT-CLEAN-20260625
title: GlobalCloud 项目群 17 仓 Git Clean 门禁证据 2026-06-25
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/globalcloud-project-group-git-clean-20260625.md
source_path: docs/harness/evidence/globalcloud-project-group-git-clean-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 17 仓 Git Clean 门禁证据 2026-06-25

## 1. 任务信息

| 项 | 内容 |
|---|---|
| task_id | `GPCF-GIT-CLEAN-001` |
| 执行日期 | 2026-06-25 |
| 执行目录 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF` |
| 检查范围 | GlobalCloud 项目群 17 个 Git 仓库 |
| 原始 JSON | `docs/harness/evidence/globalcloud-project-group-git-clean-20260625.json` |
| 执行命令 | `python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --allow-non-pass-exit-zero` |
| 门禁结论 | `project_group_git_clean = partial` |

## 2. 总体结果

```text
gate = partial
expected_repo_count = 17
checked_repo_count = 17
pass = 11
partial_or_blocked = 6
missing_repos = []
ahead_repos = []
behind_repos = []
sensitive_repos = []
```

该结果说明：

- 17 个项目仓均存在，且均为 Git 仓库。
- 未发现 ahead upstream。
- 未发现 behind upstream。
- 未发现敏感路径。
- 所有仓库 `git diff --check -- .` 均通过。
- 当前不能声明项目群 Git 全量 clean，因为 6 个仓库存在 dirty 或 untracked 变更。

## 3. Dirty 仓库

| 仓库 | 分支 | upstream | dirty_count | untracked_count | ahead | behind | diff_check | issues |
|---|---|---|---:|---:|---:|---:|---|---|
| `WAS世界资产体系` | `main` | `origin/main` | 1 | 1 | 0 | 0 | `pass` | `dirty` |
| `GlobalCloud GPC` | `main` | `origin/main` | 3 | 0 | 0 | 0 | `pass` | `dirty` |
| `GlobalCoud GPCF` | `codex/kds-token-sync-gpcf` | `origin/codex/kds-token-sync-gpcf` | 57 | 14 | 0 | 0 | `pass` | `dirty` |
| `GlobalCloud KDS` | `codex/kds-token-api-kds` | `origin/codex/kds-token-api-kds` | 1 | 0 | 0 | 0 | `pass` | `dirty` |
| `GlobalCloud PVAOS` | `pvaos/D4-release-readiness-governance` | `origin/pvaos/D4-release-readiness-governance` | 3 | 0 | 0 | 0 | `pass` | `dirty` |
| `GlobalCloud SOP` | `main` | `origin/main` | 3 | 2 | 0 | 0 | `pass` | `dirty` |

## 4. 控制结论

```text
project_group_git_clean = partial
project_group_git_clean_pass = false
project_group_git_sensitive_paths = false
project_group_git_behind = false
project_group_git_diff_check = pass
```

当前可以声明：

- 项目群 17 仓存在性已核验。
- 当前无缺失仓库、无 behind、无敏感路径、无 diff check 失败。
- 版本控制门禁已纳入真实执行治理。

当前不得声明：

- 不声明项目群 Git 全量 clean。
- 不声明项目群可提交。
- 不声明项目群可推送。
- 不声明项目群可验收。
- 不声明项目群 ready_for_review。
- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。

```text
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 5. 下一步

| 优先级 | 下一步 | 说明 |
|---|---|---|
| P0 | 对 6 个 dirty 仓库逐仓分类 | 区分本轮变更、用户已有变更、生成镜像变更、待提交变更 |
| P0 | 建立项目群变更分组 | GPC 修复、GPCF evidence/validator、PVAOS gate、KDS 修复、SOP/WAS 待审 |
| P1 | 对每个 dirty 仓库形成提交前证据包 | 需确认范围、敏感路径、diff check、门禁命令 |
| P1 | 人工确认后再提交或推送 | 当前未提交、未推送、未发布 |
