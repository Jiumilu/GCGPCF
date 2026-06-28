---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-SCHEME-RECOGNITION-RULES-20260626
title: GlobalCloud 项目群方案体系识别规则
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud 项目群方案体系识别规则.md
source_path: 02-governance/GlobalCloud 项目群方案体系识别规则.md
sync_direction: bidirectional
last_reviewed: 2026-06-28
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群方案体系识别规则

```text
project_group_scheme_recognition_rules = controlled
agents_recognition_scope = 17 projects
project_plan_inheritance_scope = 34 files
```

## 1. 双总控体系

GlobalCloud 项目群存在两个必须识别的总控体系：

| 总控体系 | 主文件 | 控制范围 |
|---|---|---|
| GlobalCloud 项目群总体方案体系 | `GPCF:01-architecture/GlobalCloud 项目群总体方案.md` | 架构、术语、版本、兼容矩阵、方案传导、项目边界和协同控制 |
| GlobalCloud 项目群实施方案体系 | `GPCF:GlobalCloud 项目群实施方案.md` | 真实进度、真实研发、真实运行、真实集成、真实交付、客户验收、任务包、命令、证据、门禁、回滚和 LOOP 闭环 |

所有项目级总体方案必须继承项目群总体方案。所有项目级实施方案必须继承项目群实施方案。项目级方案变化必须回传项目群主方案，并按影响范围传导到关联项目。

## 2. 当前纳入边界

武汉城市圈绿色供应链运营 SOP 已作为场景运营 SOP 链路纳入项目群总体方案和项目群实施方案。该纳入只建立 `controlled_internal_pilot` 边界，用于 SOP、KDS、GFIS、GPC、GPCF 和 WAES 的受控协同，不等于正式 SOP 发布、真实 KDS API 写入、GFIS 真实 SOP E2E、生产运行完成、客户验收或 1+8 全覆盖达成。

## 3. 禁止声明

未经人工确认和真实证据门禁，不得声明：

```text
accepted=false
integrated=false
production_ready=false
customer_accepted=false
```
