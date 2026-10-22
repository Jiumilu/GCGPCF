---
doc_id: GPCF-DOC-D2B0AFA74D
title: F-014 权威接收台账 owner、scope 重定与留存策略（老卢裁定记录）
project: KDS
related_projects: [GPC, WAME, KDS, MMC, GPCF, Studio, Project]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/f014-ledger-owner-and-retention-20261022.md
source_path: docs/reports/f014-ledger-owner-and-retention-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-014 权威接收台账 owner、scope 重定与留存策略（老卢裁定记录）

- 裁定时间：2026-10-22 22:44（问答，决策模型辅助）
- 回执：`AUTH-PG-F014-LEDGER-OWNER-20261022`

## 1. 三项裁定

| # | 议题 | 决策模型 | 裁定 |
|---|---|---|---|
| 1 | 权威接收台账 owner | PMC 46.1% / GPCF 29.6% / KDS 14.9% / 新建 9.4% | **Project（PMC / Plane 项目主账）**，人工确认后写入，禁止自动写入 |
| 2 | scope 重定 | `gate` escalate 0.418（要求人决） | **按退役事实重定**：Studio review 条款随 Studio 退役失效，接收方改为 PMC；保留 KDS canonical 与 MMC 委派两段 |
| 3 | 会议数据留存 | 24 个月归档 53.8% / 永久 16.9% / 12 个月 16.9% / 24 月后匿名 12.4% | **24 个月后归档**（不删除，转 `_archive/` 并写 MANIFEST） |

## 2. 变更落点（`features/active/F-014-*/feature.yaml`）

- `goal`：Studio review → PMC/Plane 权威接收台账；
- `scope.in`：Studio OpenSpec 条款标注退役失效（仅历史引用）；新增 PMC 接收边界；
- `acceptance`：删除两条 Studio 门禁要求，改为 PMC 接收边界 + GPCF 门禁；
- 新增 `authoritative_receiving_ledger`（owner=Project）与 `retention_policy`；
- `blockers` 收敛为 2 条（真实会议数据未授权、KDS/MMC 运行配置边界未授权），`governance_blocked` 保持 true。

## 3. 仍然阻塞的（需另行授权）

1. **真实会议数据试点**：需 `gate(production)` 级授权 + 数据范围（哪些会议、哪些字段、脱敏规则）；
2. **KDS/MMC 运行配置边界变更**：属主执行（KDS 属主 / MMC 属主），GPCF 只出清单。

## 4. 非声明

本文件只记录裁定与台账变更，不构成真实数据接入、生产写入或状态提升；`C_real` 不因此变化。
