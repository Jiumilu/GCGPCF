---
doc_id: GPCF-DOC-5CF2361DE8
title: CodeGraph Studio sync-only precheck 证据
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.md
source_path: docs/harness/evidence/codegraph-studio-sync-only-precheck-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# CodeGraph Studio sync-only precheck 证据

本证据对应 `GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`。

## 结论

用户已授权 Studio 作为 watchlist 第一候选执行 CodeGraph sync-only precheck。本轮只对 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` 执行 `codegraph sync`，不进入业务开发，不发布、不部署、不执行 workflow release write，不提交、不推送。

结果为 `studio_codegraph_sync_only_pass_with_residual_watch`：

- sync 前：`pendingChanges={added:3, modified:4, removed:0}`
- sync 命令：`codegraph sync`
- sync 结果：`Synced 41 changed files`，`Added: 6`，`Modified: 35`，`660 nodes`
- 最终观测：`pendingChanges={added:0, modified:0, removed:0}`，CodeGraph 已收敛；工作树仍保留 8 项既有 dirty，属于 Git residual watch
- `reindexRecommended=false`
- `worktreeMismatch=null`
- `.codegraph/` 未进入 Git 状态

## Studio dirty 保留

CodeGraph sync-only 已执行，但 Studio 工作树仍保留 8 项既有业务/治理 dirty。本轮不处理这些文件，不声明业务完成。

| 类型 | 数量 |
| --- | ---: |
| modified | 8 |
| deleted | 0 |
| untracked | 0 |
| total | 8 |

文件清单：

- `packages/client/src/components/hermes/settings/AccountSettings.vue`
- `packages/client/src/router/index.ts`
- `packages/client/src/views/hermes/SettingsView.vue`
- `packages/server/src/middleware/user-auth.ts`
- `tests/client/account-settings-default-credential.test.ts`
- `tests/client/router-default-credential-guard.test.ts`
- `tests/client/settings-view-default-credential.test.ts`
- `tests/server/user-auth.test.ts`

## 五方向

### run

按授权只对 Studio 执行 CodeGraph status refresh 与 `codegraph sync`，并采集 post-sync status。

### stop

`stop_type=sync_only_pass_with_residual_watch`。Studio CodeGraph sync-only 已执行，CodeGraph pending 已收敛为 0，但工作树仍保留 8 项既有 dirty；不能升级 accepted、integrated 或 production_ready。

### verify

回放：

```bash
python3 tools/kds-sync/validate_codegraph_studio_sync_only_precheck.py
python3 tools/kds-sync/check_chinese_localization_gate.py --json
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
```

### recover

如后续 Studio 继续发生 dirty 漂移，恢复到 `watchlist monitor_only` 或重新请求 Studio 专项授权。

### debug

Studio 索引闭合不等于业务开发闭合；下一轮应转回 Brain/GFIS/KDS 授权边界或项目群 watchlist monitor。

## 非声明

- 不声明 Studio 业务实现完成。
- 不声明 accepted、integrated 或 production_ready。
- 不声明 release、deployment、workflow release write。
- 不声明 commit 或 push。
- 不声明 Brain、GFIS、KDS sync-only closure 完成。
- 不声明 CodeGraph 可替代 WAES、Harness 或人工验收裁决。

## 下一轮

`GPCF-CODEGRAPH-WATCHLIST-POST-STUDIO-MONITOR-016`
