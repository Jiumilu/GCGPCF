---
doc_id: GPCF-DOC-5649B07956
title: GPCF CodeGraph Project Group Graphized Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/loop-codegraph-project-group-graphized-20260621.md
source_path: docs/harness/evidence/loop-codegraph-project-group-graphized-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF CodeGraph Project Group Graphized Evidence

## 结论

本轮状态为 `project_group_codegraph_graphized_with_controlled_gfis_residual_and_active_watchlist`。

项目群当前 14 个本机 Git 仓均已纳入 CodeGraph 本地图谱，且 `.codegraph/` 均保持 Git 保护。GlobalCloud Studio 与 WAS世界资产体系均已纳入项目群图谱范围。

当前 14 个项目中，11 仓 `codegraph status` 为 up-to-date，Brain 与 Studio 为活动 drift watchlist，GFIS 为受控 residual。

本轮执行了受控 `codegraph sync`，范围仅限本地 `.codegraph/` 索引：

- GlobalCloud Brain
- GlobalCloud KDS
- GlobalCloud Studio
- GlobalCloud GFIS
- GlobalCoud GPCF

本轮未修改项目业务代码，未提交，未推送，未部署，未升级 accepted / integrated / production_ready。

## 14 仓图谱状态

| 项目 | Files | Nodes | Edges | 状态 |
| --- | ---: | ---: | ---: | --- |
| GlobalCloud Brain | 152 | 2447 | 5758 | pending_sync_watchlist |
| GlobalCloud GFIS | 1022 | 13152 | 38142 | controlled_residual |
| GlobalCloud GPC | 70 | 705 | 1995 | up_to_date |
| GlobalCloud KDS | 518 | 3499 | 7115 | up_to_date |
| GlobalCloud MMC | 84 | 522 | 1083 | up_to_date |
| GlobalCloud PKC | 110 | 1034 | 2685 | up_to_date |
| GlobalCloud PVAOS | 604 | 8899 | 28838 | up_to_date |
| GlobalCloud Studio | 797 | 14457 | 46854 | pending_sync_watchlist |
| GlobalCloud WAES | 281 | 3511 | 11298 | up_to_date |
| GlobalCloud XGD | 181 | 3645 | 9914 | up_to_date |
| GlobalCloud XiaoC | 1176 | 15520 | 64515 | up_to_date |
| GlobalCloud XiaoG | 752 | 13943 | 45987 | up_to_date |
| GlobalCoud GPCF | 819 | 9343 | 21668 | up_to_date_after_final_sync |
| WAS世界资产体系 | 30 | 70 | 209 | up_to_date |

## Brain 活动漂移

Brain 曾执行多次 `codegraph sync`，可短暂达到 up-to-date，但随后再次出现 `Modified: 7 files`。本轮复核时仍有 Brain 相关长进程在运行：

- `gbrain embed --all`
- `gbrain embed --all --batch-size 20`
- Vite dev server on `127.0.0.1:5175`

本轮未修改 Brain 业务代码，不进入项目内部开发，也未停止活动进程；仅执行 `.codegraph` 同步。最终复核 Brain 当前状态为 `pending_sync_watchlist`，`codegraph status --json` 显示 `modified=32`。

## Studio 活动漂移

Studio 曾在本轮执行受控 `.codegraph` 同步复核，但最终复核时再次出现 `Added: 2 files; Modified: 2 files`。本轮不进入 Studio 业务开发，也不作为业务完成声明。

当前 Studio 活动漂移文件：

- `packages/client/src/components/studio/SessionContextBar.vue`
- `packages/client/src/views/hermes/ChatView.vue`
- `tests/client/chat-view-tab-title.test.ts`
- `tests/client/session-context-bar.test.ts`

## GFIS 受控 residual

GFIS 已执行 `codegraph sync`，同步结果为 `Added: 1 - 0 nodes`。同步后 `codegraph status` 仍提示 `Added: 1 files`，但该项已由 `large_generated_validator_exception_candidate` 策略解释，并且 `.codegraph/` 未进入 Git 状态。

因此，GFIS 当前 residual 是受控图谱残留，不作为项目群图谱化失败处理，也不等于 GFIS 业务完成、运行层完成或验收完成。

## 完成边界

本轮完成的是项目群 CodeGraph 本地图谱化：

- 14 仓全部存在 `.codegraph/`
- 14 仓全部可执行 `codegraph status`
- 14 仓 `.codegraph/` 均被 Git 保护
- 11 仓 `codegraph status` 为 up-to-date
- 2 仓 Brain 与 Studio 为活动 pending sync watchlist
- 1 仓 GFIS 为受控 residual

本轮不证明：

- 项目业务功能完成
- GFIS 真实业务 SOP E2E 完成
- accepted / integrated / production_ready
- 生产写入、真实外部 API 写入或部署完成

## Loop 下一轮输入

`GPCF-CODEGRAPH-ACTIVE-DRIFT-MONITOR-001`

目标：持续监控 Brain 与 Studio 活动 CodeGraph drift，保持 14 仓覆盖与 GFIS 受控 residual 策略，不进入项目业务开发。
