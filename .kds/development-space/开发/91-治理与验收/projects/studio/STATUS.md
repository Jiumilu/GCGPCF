---
doc_id: GPCF-DOC-D67FFAE452
title: Studio 状态
project: Studio
related_projects: [Studio]
domain: governance
status: controlled
version: v1.0
owner: Studio
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/studio/STATUS.md
source_path: projects/studio/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-17
supersedes: []
superseded_by: []
---

# Studio 状态

本文件只记录 Studio 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## GCWorld 组织世界纵切迁出（2026-10-17）

GCWorld（原 GCWORLD）组织世界只读纵切已于 2026-10-17 **迁移至独立项目 GlobalCloud World**（`../GlobalCloud World`，角色 external，Feature F-021 纳管）。

| 项 | 内容 |
|---|---|
| 迁移依据 | 用户 2026-10-16 裁定「GCWorld 是一个单独的项目，不依赖 Studio」；World 授权记录见 `GlobalCloud World/docs/授权与范围变更记录_20261016.md` |
| Studio 侧改动 | 移除客户端路由 `/gcworld/organizations`；移除服务端 `app.use(createGcworldRoutes().routes())` 及其 import；Playwright 忽略 `**/gcworld-*.spec.ts` |
| Studio 侧保留 | `packages/client/src/views/gcworld/`、`features/gcworld/`、`packages/server/src/routes/gcworld.ts`、`services/gcworld-*.ts`、`data/gcworld-*.json`、`tests/{client,server}/gcworld-*`（**已非路由装配的一部分**，作为历史实现保留待处置） |
| Studio 侧不迁不改 | `docs/harness/` 全部历史证据（71 个 gcworld codegraph JSON + loop 回执 + `admin-trial-runtime-20260905.md`）——它们记录「当时在 Studio 发生」的事实 |
| 验证 | Studio gcworld 单元/组件测试 31/31 仍通过；`routes/index.ts` 可打包（无未解析 import）；无残留 gcworld 引用 |
| F-015 归属 | 仍为 Studio 名下（`features/active/F-015-.../feature.yaml:3 project: studio`），状态 `blocked`（stage-1 主动冻结，恢复条件＝真实接入就绪），**本项变更不改其归属** |

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/studio-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project studio`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`
