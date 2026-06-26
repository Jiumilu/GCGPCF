---
doc_id: GPCF-DOC-GLOBALCLOUD-GPCF-MASTER-PLAN-20260624
title: GlobalCloud GPCF 总体方案
project: GFIS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/GlobalCloud GPCF 总体方案.md
source_path: GlobalCloud GPCF 总体方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

## 项目群主方案继承声明

本项目总体方案继承《GlobalCloud 项目群总体方案》。
本项目实施方案继承《GlobalCloud 项目群实施方案》。
若本项目方案与项目群主方案冲突，以项目群主方案为准，并触发回传与协同修订。

# GlobalCloud GPCF 总体方案

## 1. 项目定位

GlobalCloud GPCF 是 GlobalCloud WAS 项目群的治理、控制、门禁、文档、LOOP 和证据编排项目。GPCF 负责维护项目群唯一总体控制性文档、项目主方案台账、文档门禁、KDS 开发空间镜像、专项验证脚本、LOOP 运行控制闭环和跨项目状态报告。

本项目不等同于 WAS 世界资产体系本身。WAS 定义资产体系，Ontology 定义语义，XWAIL 定义契约，WAE 提供世界资产运行引擎，WAES 提供基于 WAE 的业务实现和治理入口，AaaS 提供服务化运营。GPCF 负责让这些项目间的名称、职责、版本、接口、交付、测试和证据保持受控一致。

## 2. 与项目群主方案的继承关系

本方案继承 `GPCF:01-architecture/WAS世界资产体系总体方案.md`，并作为 `GlobalCoud GPCF` 仓内唯一当前有效项目总体方案。

`01-architecture/WAS世界资产体系总体方案.md` 是项目群唯一总体控制性文档；本文件是 GPCF 作为治理项目的项目级总体方案。主方案变化必须经本项目影响评估后传导到所有相关项目方案。本方案变化必须先回流主方案或 Change Proposal，再传导到受影响项目。未经用户确认的结构性变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 3. 项目群版本基线

| 对象 | 当前基线 |
|---|---|
| 项目群基线 | `GC-WAS-PG-BASELINE-0.1.0` |
| GPCF 总体方案 | `v1.0` |
| 上游控制 | `01-architecture/WAS世界资产体系总体方案.md` |
| 语义来源 | WAS / Ontology |
| 契约来源 | XWAIL |
| 治理入口 | WAES |
| 服务化出口 | AaaS / SCaaS |

## 4. 本项目权威职责

1. 维护项目群唯一总体控制性文档和项目群总体方案治理路线图。
2. 维护全项目主方案控制台账，确保每个业务项目只有一个当前有效总体方案。
3. 维护术语、版本、架构、职责、接口、测试、交付、LOOP 和证据的一致性验证脚本。
4. 执行文档门禁、污染检查、KDS TOKEN 检查和 LOOP 文档门禁。
5. 维护 KDS 开发空间本地镜像和文档控制元数据。
6. 编排 LOOP 运行控制闭环，记录 `run -> stop -> verify -> recover -> debug` 的治理证据。
7. 管理主方案到项目方案、项目方案到主方案、项目方案之间经主方案传导的变更机制。

## 5. 本项目不承担的职责

1. 不替代 WAS 定义顶层资产理论、三层资产、八维、八流和生命周期。
2. 不替代 Ontology 定义语义本体、词表、概念关系和推理规则。
3. 不替代 XWAIL 定义模型契约、Schema、Profile、状态机和 Validator。
4. 不替代 WAE 的世界资产运行引擎职责。
5. 不替代 WAES 的注册、授权、发布、治理和业务 Explorer 职责。
6. 不替代 AaaS 服务包、计量、SLA、商业运营和客户交付。
7. 不替代 GFIS、GPC、PVAOS、KDS、Brain、Studio、MMC、PKC、SOP、XGD、XiaoC、XiaoG 的项目级业务实现。

## 6. 核心交付物

| 交付物 | 说明 | 状态 |
|---|---|---|
| GPCF 总体方案 | 本文件 | controlled |
| 项目群唯一总体控制性文档 | `01-architecture/WAS世界资产体系总体方案.md` | controlled |
| 项目群主方案控制台账 | `09-status/globalcloud-project-master-plan-control-register.md` | controlled |
| 项目群总体方案治理路线图 | `02-governance/GlobalCloud项目群总体方案治理专项目标与路线图.md` | controlled |
| 项目总体方案模板 | `templates/project-master-plan-template.md` | controlled |
| 变更传导模板 | `02-governance/project-master-plan-change-propagation-template.md` | controlled |
| 专项验证脚本 | `tools/kds-sync/validate_project_*.py` 与 WAS/XWAIL/AaaS 对齐脚本 | controlled |
| 文档门禁证据 | document_control、污染检查、KDS TOKEN、LOOP 文档门禁输出 | evidence_required |

## 7. 与其他项目的接口关系

| 项目 | 接口关系 | 证据/契约 |
|---|---|---|
| WAS世界资产体系 | 主方案语义、资产体系和治理边界 | WAS 总体方案 |
| Ontology | 术语、概念关系和语义映射规则 | 术语与映射检查 |
| GlobalCloud XWAIL | 模型契约、Profile、状态机、证据约束 | XWAIL 总体方案与 Validator |
| GlobalCloud AaaS | 服务包、计量、SLA 和商业运营边界 | AaaS 总体方案 |
| WAES | 注册、授权、发布、治理和 Explorer 入口 | WAES 总体方案 |
| GFIS/GPC/PVAOS | 业务事实、绿色供应链场景和运营门户 | 项目总体方案与证据 |
| KDS/Brain/Studio | 知识事实源、知识治理和建模工作台 | 项目总体方案与证据 |
| MMC/SOP | Harness Engineering、SOP、会话和规则治理 | 项目总体方案与脚本 |
| PKC/XGD/XiaoC/XiaoG | 知识/提示/智能体/本地工作台能力 | 项目总体方案与运行证据 |
| shared/python_utils | 共享 Python 工具目录，不作为业务项目 | 导入可用性与依赖治理 |

## 8. 技术架构现状和目标架构

当前 GPCF 是以 Markdown 受控文档、KDS 本地镜像、Python 校验脚本、LOOP 文档门禁和 Harness evidence 为核心的治理仓。仓内存在较多历史文档、镜像文件和专项脚本，短期尊重现实情况，不做大规模迁移或清理。

目标架构：

```text
WAS Master Plan
  -> Project Master Plan Register
  -> Project Master Plans
  -> Validators / Document Gate / KDS Gate / LOOP Gate
  -> Evidence / Status Report / Change Propagation
```

中长期应把 GPCF 的治理脚本、文档门禁、KDS 镜像、LOOP 运行控制、Harness evidence 和项目状态矩阵收敛为统一控制平面，并与 WAES、MMC、SOP 和 KDS 形成可审计接口。

## 9. 测试、交付和运行命令

```bash
python3 -m py_compile tools/kds-sync/validate_was_master_plan_control.py tools/kds-sync/validate_project_master_plan_register.py tools/kds-sync/validate_project_master_plan_uniqueness.py tools/kds-sync/validate_project_plan_inheritance.py tools/kds-sync/validate_project_terms_consistency.py tools/kds-sync/validate_project_version_compatibility.py tools/kds-sync/validate_project_group_delivery_readiness.py
python3 tools/kds-sync/validate_was_master_plan_control.py
python3 tools/kds-sync/validate_project_group_master_plan_governance.py
python3 tools/kds-sync/validate_project_master_plan_register.py
python3 tools/kds-sync/validate_project_master_plan_uniqueness.py
python3 tools/kds-sync/validate_project_plan_inheritance.py
python3 tools/kds-sync/validate_project_terms_consistency.py
python3 tools/kds-sync/validate_project_version_compatibility.py
python3 tools/kds-sync/validate_project_group_delivery_readiness.py
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

命令未执行或失败时，不得声明项目群总体方案治理完成、accepted、integrated 或 production_ready。

## 10. LOOP 接入

```yaml
loop_enabled: true
loop_owner: GPCF
required_gates:
  - document_gate
  - version_gate
  - architecture_gate
  - contract_gate
  - project_master_plan_gate
  - kds_gate
  - loop_document_gate
  - evidence_gate
```

GPCF 自身必须参与 LOOP，不是免审计例外。每轮非只读治理工作必须覆盖 `run -> stop -> verify -> recover -> debug`。

## 11. 风险、依赖、回滚和非声明边界

风险：项目群总控方案与 GPCF 项目方案混用；文档通过被误认为业务实现完成；旧命名、旧架构口径或未确认方案重新回流；脚本覆盖范围窄于治理声明。

依赖：所有项目总体方案、KDS 本地镜像、文档控制台账、专项验证脚本、LOOP 文档门禁、用户确认和变更传导记录。

回滚：未经用户确认的结构性变化必须退回 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`；未通过文档门禁和专项验证的治理状态不得升级。

本方案不声明业务实现完成、不声明客户交付完成、不声明所有项目运行可用、不声明 accepted、integrated 或 production_ready。
