---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-SCHEME-RECOGNITION-RULES-20260626
title: GlobalCloud 项目群方案体系识别规则
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud 项目群方案体系识别规则.md
source_path: 02-governance/GlobalCloud 项目群方案体系识别规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群方案体系识别规则

## 1. 目的

本文建立会话入口级识别规则，确保项目群内所有 Codex/Agent 会话都能识别两个总控体系，而不是只依赖某一个主方案文件。

## 2. 两个必须识别的总控体系

| 总控体系 | 规范主文件名 | 当前权威路径 | 定位 |
|---|---|---|---|
| GlobalCloud 项目群总体方案体系 | `GlobalCloud 项目群总体方案.md` | `GPCF:01-architecture/GlobalCloud 项目群总体方案.md` | 项目群最高层总体控制性方案，负责项目群架构、术语、版本、兼容矩阵、方案传导、项目边界与协同控制 |
| GlobalCloud 项目群实施方案体系 | `GlobalCloud 项目群实施方案.md` | `GPCF:GlobalCloud 项目群实施方案.md` | 项目群唯一实施控制性方案，负责真实进度、真实研发、真实运行、真实集成、真实交付、客户验收、任务包、命令、证据、门禁、回滚和 LOOP 闭环 |

## 3. 会话入口规则

所有项目 `AGENTS.md` 必须包含 `GlobalCloud 项目群总控体系识别规则`，并显式声明：

- 存在 GlobalCloud 项目群总体方案体系；
- 存在 GlobalCloud 项目群实施方案体系；
- 所有项目级总体方案必须继承项目群总体方案；
- 所有项目级实施方案必须继承项目群实施方案；
- 项目级方案变化必须回传项目群主方案，并按影响范围传导到关联项目；
- 未经人工确认，不得声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

## 4. 项目方案继承规则

每个项目唯一总体方案和唯一实施方案必须包含 `项目群主方案继承声明`：

```text
本项目总体方案继承《GlobalCloud 项目群总体方案》。
本项目实施方案继承《GlobalCloud 项目群实施方案》。
若本项目方案与项目群主方案冲突，以项目群主方案为准，并触发回传与协同修订。
```

## 5. 覆盖项目

| 项目 | AGENTS.md | 唯一总体方案 | 唯一实施方案 |
|---|---|---|---|
| AAAS | `GlobalCloud AAAS/AGENTS.md` | `GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md` | `GlobalCloud AAAS/docs/GlobalCloud AaaS 实施方案.md` |
| Brain | `GlobalCloud Brain/AGENTS.md` | `GlobalCloud Brain/GlobalCloud Brain 总体方案.md` | `GlobalCloud Brain/GlobalCloud Brain 实施方案.md` |
| GFIS | `GlobalCloud GFIS/AGENTS.md` | `GlobalCloud GFIS/GlobalCloud GFIS 总体方案.md` | `GlobalCloud GFIS/GlobalCloud GFIS 实施方案.md` |
| GPC | `GlobalCloud GPC/AGENTS.md` | `GlobalCloud GPC/GlobalCloud GPC 总体方案.md` | `GlobalCloud GPC/GlobalCloud GPC 实施方案.md` |
| KDS | `GlobalCloud KDS/AGENTS.md` | `GlobalCloud KDS/GlobalCloud KDS 总体方案.md` | `GlobalCloud KDS/GlobalCloud KDS 实施方案.md` |
| MMC | `GlobalCloud MMC/AGENTS.md` | `GlobalCloud MMC/GlobalCloud MMC 总体方案.md` | `GlobalCloud MMC/GlobalCloud MMC 实施方案.md` |
| PKC | `GlobalCloud PKC/AGENTS.md` | `GlobalCloud PKC/GlobalCloud PKC 总体方案.md` | `GlobalCloud PKC/GlobalCloud PKC 实施方案.md` |
| PVAOS | `GlobalCloud PVAOS/AGENTS.md` | `GlobalCloud PVAOS/GlobalCloud PVAOS 总体方案.md` | `GlobalCloud PVAOS/GlobalCloud PVAOS 实施方案.md` |
| SOP | `GlobalCloud SOP/AGENTS.md` | `GlobalCloud SOP/GlobalCloud SOP 总体方案.md` | `GlobalCloud SOP/GlobalCloud SOP 实施方案.md` |
| Studio | `GlobalCloud Studio/AGENTS.md` | `GlobalCloud Studio/GlobalCloud Studio 总体方案.md` | `GlobalCloud Studio/GlobalCloud Studio 实施方案.md` |
| WAES | `GlobalCloud WAES/AGENTS.md` | `GlobalCloud WAES/GlobalCloud WAES 总体方案.md` | `GlobalCloud WAES/GlobalCloud WAES 实施方案.md` |
| XGD | `GlobalCloud XGD/AGENTS.md` | `GlobalCloud XGD/GlobalCloud XGD 总体方案.md` | `GlobalCloud XGD/GlobalCloud XGD 实施方案.md` |
| XWAIL | `GlobalCloud XWAIL/AGENTS.md` | `GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md` | `GlobalCloud XWAIL/GlobalCloud XWAIL 实施方案.md` |
| XiaoC | `GlobalCloud XiaoC/AGENTS.md` | `GlobalCloud XiaoC/GlobalCloud XiaoC 总体方案.md` | `GlobalCloud XiaoC/GlobalCloud XiaoC 实施方案.md` |
| XiaoG | `GlobalCloud XiaoG/AGENTS.md` | `GlobalCloud XiaoG/GlobalCloud XiaoG 总体方案.md` | `GlobalCloud XiaoG/GlobalCloud XiaoG 实施方案.md` |
| GPCF | `GlobalCoud GPCF/AGENTS.md` | `GlobalCoud GPCF/GlobalCloud GPCF 总体方案.md` | `GlobalCoud GPCF/GlobalCloud GPCF 实施方案.md` |
| WAS | `WAS世界资产体系/AGENTS.md` | `WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md` | `WAS世界资产体系/docs/GlobalCloud WAS 实施方案.md` |

附加镜像入口：

| 镜像 | AGENTS.md | 说明 |
|---|---|---|
| KDS GPC 开发空间镜像 | `GlobalCloud KDS/concepts/开发/02-GPC/AGENTS.md` | KDS 内部开发空间镜像入口，不作为独立项目计数，但必须识别项目群两个总控体系 |

## 6. 变更传导机制

| 变更 | 必须动作 |
|---|---|
| 项目群总体方案变化 | 更新本文、影响项目的 `AGENTS.md`、项目总体方案和项目实施方案 |
| 项目群实施方案变化 | 更新本文、项目实施方案、任务包、证据门禁、状态推进矩阵和 LOOP 证据 |
| 项目总体方案变化 | 回传 GPCF，判断是否需要修订项目群总体方案、术语表、架构边界或兼容矩阵 |
| 项目实施方案变化 | 回传 GPCF，判断是否需要修订项目群实施方案、真实执行治理总控板、任务包和依赖矩阵 |

## 7. 当前结论

```text
project_group_scheme_recognition_rules = controlled
agents_recognition_scope = 17 projects
project_plan_inheritance_scope = 34 files
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

本文只建立识别规则和继承关系，不声明项目群真实运行、真实集成、真实交付或客户验收完成。
