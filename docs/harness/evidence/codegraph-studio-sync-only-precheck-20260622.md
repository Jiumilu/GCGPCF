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
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# CodeGraph Studio sync-only precheck 证据

本证据对应 `GPCF-CODEGRAPH-STUDIO-SYNC-ONLY-PRECHECK-015`。

## 结论

用户已授权 Studio 作为 watchlist 第一候选执行 CodeGraph sync-only precheck。本轮只对 `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio` 执行 `codegraph sync`，不进入业务开发，不发布、不部署、不执行 workflow release write，不提交、不推送。

结果为 `studio_codegraph_sync_only_pass_with_residual_watch`：

- sync 前：`pendingChanges={added:2, modified:9, removed:0}`
- sync 命令：`codegraph sync`
- sync 结果：`Synced 12 changed files`，`Added: 2`，`Modified: 10`，`237 nodes`
- 最终验证中 Studio 在同一 Git dirty 范围内再次出现 2 个 modified pending，已按授权内 sync-only 边界补充执行一次 `codegraph sync`，结果为 `Synced 2 changed files`、`Modified: 2`、`22 nodes`
- 最终观测：`pendingChanges={added:0, modified:7, removed:0}`，属于残留 watch；允许上限为 added=0、modified<=9、removed=0，不能超过授权前 modified=9 的范围
- `reindexRecommended=false`
- `worktreeMismatch=null`
- `.codegraph/` 未进入 Git 状态

## Studio dirty 保留

CodeGraph sync-only 已执行，但 Studio 仍存在小幅 modified residual watch；Studio 工作树仍有 12 项既有业务/治理 dirty。本轮不处理这些文件，不声明业务完成。

| 类型 | 数量 |
| --- | ---: |
| modified | 11 |
| deleted | 0 |
| untracked | 1 |
| total | 12 |

文件清单：

- `docs/harness/loops/loop-round-GPCF-STUDIO-LR-017.md`
- `packages/client/src/components/layout/PageSidebarNav.vue`
- `packages/client/src/components/studio/SessionObjectPanel.vue`
- `packages/server/src/routes/governance/session-bindings.ts`
- `packages/server/src/services/core/kds-audit.ts`
- `packages/server/src/services/governance/kds-governance-context.ts`
- `packages/server/src/services/governance/session-binding-context.ts`
- `tests/client/page-sidebar-nav.test.ts`
- `tests/client/session-object-panel.test.ts`
- `tests/server/kds-governance-context.test.ts`
- `tests/server/session-binding-context.test.ts`
- `tests/server/session-bindings-route.test.ts`

## 五方向

### run

按授权只对 Studio 执行 CodeGraph status refresh 与 `codegraph sync`，并采集 post-sync status。

### stop

`stop_type=sync_only_pass_with_residual_watch`。Studio CodeGraph sync-only 已执行，但仍保留小幅 modified residual watch；业务 dirty 仍保留，不能升级 accepted、integrated 或 production_ready。

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
