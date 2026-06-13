---
doc_id: GPCF-DOC-31F21E6BD5
title: GlobalCloud Loop Git Version Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/git-version-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/git-version-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Git Version Gates

## 目标

每轮 Loop 必须有可回放的 Git 版本状态。文档、evidence、代码和远端版本必须能互相对应。

## 每轮必留 Git evidence

| 文件 | 内容 |
|---|---|
| `git-status-{ID}.txt` | 分支、HEAD、upstream、dirty、ahead/behind |
| `git-diff-stat-{ID}.txt` | 本轮变更统计 |
| `git-diff-check-{ID}.txt` | `git diff --check -- .` 结果 |
| `git-commit-{ID}.txt` | commit hash 或不提交原因 |
| `git-push-{ID}.txt` | push 结果或不推送原因 |

## 状态上限

| Git 状态 | Loop 状态上限 |
|---|---|
| dirty 已登记 | `audit_ready` |
| dirty 未登记 | `rework_required` |
| 敏感文件未处理 | `blocked` |
| committed but not pushed | `harness_review` |
| push rejected / 远端冲突 | `blocked` |
| clean + pushed + evidence 完整 | 可申请 `accepted` |

## 敏感文件

以下文件或模式不得自动提交：

- `.env`
- `.env.*`，但 `.env.example` 可提交
- `*TOKEN*`
- `*SECRET*`
- `*.pem`
- `*.key`
- `*.p12`
- `id_rsa*`

## 分支与提交建议

默认分支：

```text
codex/{project-code}-loop-{round-id}
```

提交信息：

```text
loop({project-code}): complete {round-id}
```

若项目已有明确 upstream，优先尊重现有 upstream，不强行改分支。
