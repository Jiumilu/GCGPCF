---
doc_id: GPCF-DOC-PROJECT-GROUP-MASTER-PLAN-GOVERNANCE-20260624
title: GlobalCloud 项目群总体方案治理专项目标与路线图
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md
source_path: 02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群总体方案治理专项目标与路线图

## 1. 专项目标

本专项以 `01-architecture/WAS世界资产体系总体方案.md` 为项目群唯一总体控制性文档，以 `09-status/globalcloud-project-master-plan-control-register.md` 为项目级方案治理台账，建立 GlobalCloud 项目群所有项目的总体方案治理体系。

最终目标：

```text
每个业务项目只有一个当前有效总体方案。
每个项目总体方案继承项目群主方案的结构、术语、职责、架构、版本、接口、交付物、测试、LOOP、证据和变更传导机制。
主方案变化可以传导到受影响项目方案。
项目方案变化可以回流主方案，再传导到相关项目方案。
```

## 2. 当前控制基线

| 控制对象 | 当前状态 | 证据 |
|---|---|---|
| 项目群唯一主方案 | 已建立 | `01-architecture/WAS世界资产体系总体方案.md` |
| 项目主方案控制台账 | 已建立 | `09-status/globalcloud-project-master-plan-control-register.md` |
| WAS 项目总体方案 | 已建立 | `WAS世界资产体系/docs/GlobalCloud WAS 总体方案.md` |
| XWAIL 项目总体方案 | 已建立 | `GlobalCloud XWAIL/GlobalCloud XWAIL 总体方案.md` |
| AaaS 项目总体方案 | 已建立 | `GlobalCloud AAAS/docs/GlobalCloud AaaS 总体方案.md` |
| GPC 项目总体方案 | 已建立 | `GlobalCloud GPC/GlobalCloud GPC 总体方案.md` |
| 其余业务项目总体方案 | 已建立 | 台账状态为 `authoritative` |
| GPCF 项目总体方案 | 已建立 | `GlobalCloud GPCF 总体方案.md` |
| shared/python_utils | 非业务项目 | 台账状态为 `not_project` |

当前专项状态：

```text
project_group_master_plan_governance = controlled
reason = all registered business projects have one authoritative project master plan
```

## 3. 覆盖范围

业务和治理项目：

1. WAS世界资产体系
2. GlobalCloud XWAIL
3. GlobalCloud AaaS / AAAS
4. GlobalCloud WAES
5. GlobalCloud GFIS
6. GlobalCloud GPC
7. GlobalCloud PVAOS
8. GlobalCloud KDS
9. GlobalCloud Brain
10. GlobalCloud Studio
11. GlobalCloud MMC
12. GlobalCloud PKC
13. GlobalCloud SOP
14. GlobalCloud XGD
15. GlobalCloud XiaoC
16. GlobalCloud XiaoG
17. GlobalCoud GPCF

共享目录：

- `shared/python_utils` 仅作为共享工具目录，不作为业务项目，不要求项目总体方案。

## 4. 项目总体方案统一结构

所有项目总体方案必须包含：

1. 项目定位
2. 与 WAS 项目群主方案的继承关系
3. 项目群版本基线
4. 本项目权威职责
5. 本项目不承担的职责
6. 核心交付物
7. 与其他项目的接口关系
8. 技术架构现状和目标架构
9. 测试、交付和运行命令
10. LOOP 接入
11. 风险、依赖、回滚和非声明边界

缺少任一结构项的项目方案不得登记为 `authoritative`。

## 5. 传导机制

主方案到项目方案：

```text
主方案变更
  -> Affected Project Matrix
  -> 用户确认
  -> 项目总体方案补丁
  -> 专项验证脚本
  -> 文档治理门禁
  -> 台账状态更新
```

项目方案到主方案：

```text
项目方案变更
  -> Change Proposal
  -> GPCF 影响评估
  -> 主方案或台账补丁
  -> 用户确认
  -> 关联项目传导
  -> 专项验证脚本
  -> 文档治理门禁
```

项目方案之间不得私下点对点改变项目群口径，必须经主方案或 GPCF Change Proposal 传导。

## 6. 用户确认边界

以下变化必须有用户确认：

| 变化类型 | 是否需要确认 |
|---|---|
| 新增或确认项目唯一总体方案 | 是 |
| 修改项目职责边界 | 是 |
| 修改项目间接口关系 | 是 |
| 修改统一术语或正式名称 | 是 |
| 修改版本基线或兼容矩阵 | 是 |
| 将方案状态提升为 `authoritative` | 是 |
| 将项目状态声明为完成、可交付或 production_ready | 是 |

未经用户确认的结构性变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 7. 实施路线图

### P0：总控与台账基线

状态：已启动。

交付物：

- `WAS世界资产体系总体方案.md`
- `globalcloud-project-master-plan-control-register.md`
- `validate_was_master_plan_control.py`
- `validate_project_master_plan_register.py`

### P1：第一批项目总体方案补齐

范围：

- GlobalCloud WAES
- GlobalCloud GFIS
- GlobalCloud PVAOS
- GlobalCloud KDS
- GlobalCloud Brain
- GlobalCloud Studio

前置条件：

- 用户确认允许批量新增第一批项目总体方案。

### P2：第二批项目总体方案补齐

范围：

- GlobalCloud MMC
- GlobalCloud PKC
- GlobalCloud SOP
- GlobalCloud XGD
- GlobalCloud XiaoC
- GlobalCloud XiaoG
- GlobalCoud GPCF

前置条件：

- P1 验证通过。
- 对 GPCF 是否建立独立项目总体方案形成确认。
- 为 GlobalCloud SOP 建立 AGENTS 控制文件。

### P3：专项验证脚本补齐

状态：已建立首批脚本，后续随项目总体方案补齐继续扩展覆盖范围。
状态：已扩展为全项目严格检查，覆盖所有登记业务项目和 GPCF 独立项目总体方案。

已建立：

- `validate_project_master_plan_uniqueness.py`
- `validate_project_plan_inheritance.py`
- `validate_project_terms_consistency.py`
- `validate_project_version_compatibility.py`
- `validate_project_group_delivery_readiness.py`

当前边界：

- 对所有登记业务项目的 `authoritative` 项目总体方案执行严格检查。
- `shared/python_utils` 只作为共享工具目录，不作为业务项目，不要求项目总体方案。
- 脚本通过只证明文档治理和方案一致性，不证明业务实现或客户交付完成。

### P4：最终治理状态报告

输出：

- 全项目总体方案治理状态报告。
- 未完成项、风险、依赖、回滚和下一轮计划。

## 8. 验证命令

专项当前最低验证命令：

```bash
python3 tools/kds-sync/validate_project_group_master_plan_governance.py
python3 tools/kds-sync/validate_project_master_plan_register.py
python3 tools/kds-sync/validate_was_master_plan_control.py
python3 tools/kds-sync/validate_was_xwail_aaas_plan_alignment.py
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

## 9. 非声明边界

本专项当前不得声明：

- 不声明所有项目职责和接口已完全无冲突。
- 不声明项目群业务实现完成。
- 不声明客户交付完成。
- 不声明 accepted、integrated 或 production_ready。

只有所有项目总体方案、专项验证脚本、文档治理门禁和最终治理状态报告均通过后，才可申请专项文档治理层面的完成确认。该完成确认不得外推为业务实现完成、客户交付完成或 production_ready。
