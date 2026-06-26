---
doc_id: GPCF-LOOP-IMPLEMENTATION-UI-LOOP-INTEGRATION-001
title: Loop Round GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001
project: GPCF
related_projects: [GPC, WAES, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001

## 输入

- 用户确认：根目录 `GlobalCloud 项目群实施方案.md` 才是唯一主体实施方案
- `GlobalCloud 项目群实施方案.md`
- `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`
- `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`
- `09-status/globalcloud-project-implementation-control-register.md`
- `02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md`
- `tools/kds-sync/validate_project_group_implementation_plan.py`
- `tools/kds-sync/validate_loop_engineering_master_plan.py`

## run

1. 纠正项目群主体实施方案路径认定，将根目录 `GlobalCloud 项目群实施方案.md` 确立为唯一主体实施方案。
2. 将原 `01-architecture/GlobalCloud项目群实施方案.md` 从主体位置迁出，转为兼容镜像，避免历史继承链立即断裂。
3. 把界面工程专项实施链路纳入主体实施方案，明确其受控入口、工具链、状态边界和 LOOP 留证字段。
4. 把 UI/界面工程接入写入项目群实施方案控制台账和 LOOP 工程体系整体实施规范。
5. 更新当前主校验器和证据模板，使新的主体路径与 UI/LOOP 接入口径进入机检。

## stop

| 字段 | 值 |
|---|---|
| stop_type | evidence_candidate_ready |
| stop_reason | 项目群主体实施方案路径已纠正，界面工程专项已纳入主体实施方案与 LOOP 工程体系主规范 |

## verify

本轮执行并通过：

```bash
python3 tools/kds-sync/validate_project_group_implementation_plan.py
python3 tools/kds-sync/validate_loop_engineering_master_plan.py
python3 tools/kds-sync/validate_loop_ui_quality_baseline.py
git diff --check -- 'GlobalCloud 项目群实施方案.md' '01-architecture/GlobalCloud项目群实施方案.md' '09-status/globalcloud-project-implementation-control-register.md' '02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md' 'tools/kds-sync/validate_project_group_implementation_plan.py' 'tools/kds-sync/validate_loop_engineering_master_plan.py' 'templates/real-evidence-record-template.md' 'GlobalCloud GPCF 实施方案.md' 'docs/harness/loops/loop-round-GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001.md'
```

关键验证结论：

1. 主体实施方案已切换到根目录文件。
2. 界面工程专项已进入主体实施方案的 `UI/LOOP 实施链路`。
3. LOOP 工程主规范已把 UI/工作台专项能力、UI round 强制字段和 UI gate 纳入能力治理。

## recover

1. 旧路径保留兼容镜像，后续各项目实施方案可分批把 `master_control` 从旧路径传导到新主体路径。
2. 当前如果某些下游项目实施方案仍引用旧路径，不影响根目录主体文件继续作为唯一控制入口。

## debug

当前仍未关闭的边界：

1. 项目群主体文件路径已切换，但各项目仓的继承声明尚未分批完成传导。
2. 本轮只纳入界面工程专项治理与 LOOP 路由，不新增具体页面的三方案产出。
3. 本轮不提升任何项目到 `accepted`、`integrated` 或 `production_ready`。

## 输出

- `GlobalCloud 项目群实施方案.md`
- `01-architecture/GlobalCloud项目群实施方案.md`
- `09-status/globalcloud-project-implementation-control-register.md`
- `02-governance/loop/LOOP_ENGINEERING_MASTER_IMPLEMENTATION_PLAN.md`
- `tools/kds-sync/validate_project_group_implementation_plan.py`
- `tools/kds-sync/validate_loop_engineering_master_plan.py`
- `templates/real-evidence-record-template.md`
- `GlobalCloud GPCF 实施方案.md`
- `docs/harness/loops/loop-round-GPCF-IMPLEMENTATION-UI-LOOP-INTEGRATION-001.md`

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 9 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | evidence_candidate_ready |

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | pass |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 下一轮建议

- 下一轮 Round ID：`GPCF-IMPLEMENTATION-PLAN-PROPAGATION-UI-001`
- 下一轮目标：分批把各项目实施方案的 `master_control` 继承声明从兼容镜像路径传导到根目录主体路径
- 下一轮仍禁止：不得把主体路径切换写成业务实现完成
