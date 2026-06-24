---
doc_id: GPCF-DOC-GLOBALCLOUD-PROJECT-GROUP-IMPLEMENTATION-PLAN-20260624
title: GlobalCloud 项目群实施方案
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: architecture
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/01-architecture/GlobalCloud项目群实施方案.md
source_path: 01-architecture/GlobalCloud项目群实施方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群实施方案

## 1. 实施方案定位

本文是 GlobalCloud 项目群唯一总实施主方案，承接 `WAS世界资产体系总体方案` 和 `GlobalCloud 项目群主方案控制台账`，用于控制项目群从方案一致性走向真实进度、真实研发、真实运行、真实集成、真实交付和真实客户验收。

本文不替代任何项目总体方案，不重新定义 WAS、Ontology、XWAIL、WAE、WAES、AaaS 或 SCaaS 的定位。本文只定义如何实施、如何验证、如何交付、如何验收和如何保留证据。

## 2. 与 WAS 项目群总体方案的继承关系

本方案继承：

```text
GPCF:01-architecture/WAS世界资产体系总体方案.md
```

本方案受以下文件控制：

- `09-status/globalcloud-project-master-plan-control-register.md`
- `09-status/globalcloud-project-implementation-control-register.md`
- `09-status/globalcloud-core-chain-real-evidence-register.md`
- `02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md`
- `templates/project-implementation-plan-template.md`
- `templates/real-evidence-record-template.md`
- `02-governance/project-implementation-plan-change-propagation-template.md`

主方案变化影响实施口径时，必须先更新项目群实施方案，再传导到相关项目实施方案。项目实施方案变化影响总体职责、接口、交付或验收口径时，必须回流项目群实施方案或 Change Proposal。

## 3. 实施范围与项目清单

本方案覆盖以下业务和治理项目：

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

`shared/python_utils` 是共享工具目录，不建立项目实施方案，但必须纳入依赖、导入可用性和回滚控制。

## 4. 实施状态机

| 状态 | 含义 | 升级要求 |
|---|---|---|
| `not_started` | 尚未建立实施动作 | 无 |
| `planned` | 已有实施方案或任务计划 | 有受控方案或任务 |
| `in_progress` | 正在实施 | 有真实任务或代码/配置变更 |
| `blocked` | 被依赖、权限、测试、环境或确认阻塞 | 有阻塞证据 |
| `candidate` | 有候选实现或候选交付物 | 有候选证据，不得声明完成 |
| `verified` | 内部验证通过 | 有测试、运行或接口证据 |
| `ready_for_review` | 可进入人工审查 | 证据包完整 |
| `ready_for_uat` | 可进入用户/客户验收 | 有交付包和验收清单 |
| `customer_review` | 用户/客户正在验收 | 有验收记录 |
| `customer_accepted` | 用户/客户确认通过 | 必须有人类确认 |
| `repair_required` | 验证或验收退回 | 有修复项 |
| `closed` | 完整闭环 | 有验收、交付和归档证据 |

Agent、脚本或自动化不得自动声明 `customer_accepted`、`accepted`、`integrated` 或 `production_ready`。

## 5. 真实进度管理

真实进度必须由任务、里程碑、阻塞项、证据和下一步组成。没有任务，不叫进度。

项目实施状态由 `09-status/globalcloud-project-implementation-control-register.md` 统一登记。每个项目实施方案必须列出当前真实状态、当前里程碑、阻塞项、证据索引和下一步动作。

## 6. 真实研发管理

真实研发必须有代码、配置、脚本、测试或工程证据。文档更新不能单独声明研发完成。

每个项目实施方案必须列出：

- 研发任务清单；
- 代码或配置变更位置；
- 测试命令；
- 构建命令；
- 失败记录；
- 回滚路径。

## 7. 真实运行管理

真实运行必须有环境、启动命令、健康检查、日志、依赖服务和最近一次运行证据。页面存在、README 存在或 mock 成功都不能替代真实运行。

每个项目实施方案必须列出运行环境、启动命令、健康检查方式、日志位置、依赖服务和运行失败处理。

## 8. 真实集成管理

真实集成必须按调用方、被调用方、接口类型、数据对象、权限方式、契约版本、测试命令、最近验证时间和失败处理登记。

集成状态分级：

```text
declared -> contracted -> mocked -> tested -> verified -> accepted
```

`accepted` 必须有业务方或用户确认，不能由自动化脚本直接生成。

## 9. 真实交付管理

真实交付必须具备交付说明、部署说明、运行说明、配置说明、账号权限说明、测试报告、已知问题、回滚说明、培训材料和验收清单。

项目实施方案不得把代码合并、构建通过或文档完成直接声明为客户交付完成。

## 10. 客户验收管理

客户验收必须记录验收对象、验收场景、验收步骤、验收数据、验收人、验收结果、问题清单、修复记录和签收证据。

没有客户或授权人确认，不得声明 `customer_accepted`。

## 11. 项目间实施依赖矩阵

| 链路 | 主要项目 | 实施控制 |
|---|---|---|
| 模型契约链路 | WAS、Ontology、XWAIL、WAES | 模型、Profile、Validator、发布状态 |
| 服务运营链路 | XWAIL、WAES、AaaS、PVAOS | ServicePackage、计量、SLA、订阅状态 |
| 业务事实链路 | GFIS、GPC、PVAOS、KDS | 事实源、证据源、审计和回滚 |
| 知识智能链路 | KDS、Brain、XiaoC、PKC、XGD、XiaoG | 知识、提示、智能体输出和候选边界 |
| 工程治理链路 | GPCF、MMC、SOP、Studio | Harness、LOOP、SOP、模板、配置和证据 |

## 12. 版本、里程碑与发布节奏

| 对象 | 当前基线 |
|---|---|
| 项目群方案基线 | `GC-WAS-PG-BASELINE-0.1.0` |
| 项目群实施方案 | `v1.0` |
| 实施登记状态 | `implementation_plan_governance = phase_3_all_project_plans_controlled` |

实施方案版本不得高于其继承的项目总体方案版本控制边界。项目实施方案发生结构性变化时，必须更新实施控制台账。

## 13. 证据标准

| 证据类型 | 最低要求 |
|---|---|
| 进度证据 | 任务、里程碑、状态、阻塞、下一步 |
| 研发证据 | 代码/配置/脚本变更、测试、构建、回滚 |
| 运行证据 | 启动命令、健康检查、日志、依赖 |
| 集成证据 | 契约、接口测试、权限、数据对象 |
| 交付证据 | 交付包、部署说明、测试报告、已知问题 |
| 验收证据 | 验收场景、验收人、验收结果、签收或退回 |

核心链路真实证据由 `09-status/globalcloud-core-chain-real-evidence-register.md` 控制，单条证据记录使用 `templates/real-evidence-record-template.md`。历史 evidence、mock、dry-run 或专项样例不能自动升级为当前真实运行证据，必须经台账登记和验证脚本确认。

## 14. LOOP 接入

```yaml
loop_enabled: true
loop_owner: GPCF
required_gates:
  - document_gate
  - implementation_plan_gate
  - real_progress_gate
  - real_development_gate
  - runtime_gate
  - integration_gate
  - delivery_gate
  - customer_acceptance_gate
  - evidence_gate
```

每轮真实实施推进必须覆盖 `run -> stop -> verify -> recover -> debug`。

## 14.1 WAS/LOOP 实施链路

WAS/LOOP 实施链路是本实施方案体系的默认主链之一，用于把 WAS 顶层语义、Ontology 语义知识层、XWAIL 机器契约、WAES 审查门禁、KDS 证据引用、Brain 候选解释和 GPCF LOOP 运行控制闭环合并到同一实施路径。

受控入口：

- `02-governance/GlobalCloud项目群WAS-Ontology全量实施方案与执行提示词.md`
- `docs/harness/loops/loop-round-GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100.md`
- `docs/harness/evidence/was-real-source-record-monitor-100-20260623.md`
- `tools/kds-sync/validate_was_real_source_record_monitor_100.py`
- `tools/kds-sync/validate_was_status_matrix_control_board_refresh.py`

WAS/LOOP 实施链路的最低推进规则：

| 阶段 | 目标 | 退出门禁 |
|---|---|---|
| 方案控制 | 确认 WAS 总体方案、项目群实施方案和专项全量实施方案一致 | `validate_project_group_implementation_plan.py` pass |
| Source Record 准备 | 定义并监控真实 P4 candidate 输入 | 无真实输入时 `hold_required=1` |
| 语义与契约 replay | 复跑 profile mapping、crosswalk、negative fixtures 和 WAS validator | 不提升真实业务计数 |
| WAES 审查前置 | 只有真实 source-record 和授权齐备后才允许进入 review/runtime | 缺输入时 `review_queue=0`、`runtime_intake=0`、`waes_review=0` |
| 证据与下一轮 | 形成 Loop round、Harness evidence、validator output 和下一轮输入 | 必须包含 `run -> stop -> verify -> recover -> debug` |

当前 WAS/LOOP 状态固定为：`latest_monitor_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-100`，`next_monitor_round=GPCF-ONTOLOGY-WAS-REAL-SOURCE-RECORD-MONITOR-101`，`real_source_records=0`，`valid_source_records=0`，`runtime_primary_key_ready=0`，`review_queue=0`，`runtime_intake=0`，`waes_review=0`，`verified=0`，`accepted=false`，`integrated=false`，`production_ready=false`。

WAS/LOOP 实施链路不得把文档、模板、测试数据、mock、KDS 候选、用户口述、报价材料、合同审阅稿或治理 validator 写成真实 source-of-record、业务事实、客户验收或生产完成。

## 15. 变更传导机制

```text
Implementation Change Proposal
  -> Scope Review
  -> Affected Project Implementation Matrix
  -> Master Implementation Plan Decision
  -> Project Implementation Plan Patch List
  -> User Confirmation
  -> Document Control / KDS Mirror
  -> Gate Validation
  -> Evidence / Status Report
```

未经用户确认的结构性实施变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 16. 第一阶段实施边界

第一阶段只建立项目群实施方案管控体系：

- 项目群实施主方案；
- 项目实施方案模板；
- 项目实施方案控制台账；
- 实施方案变更传导模板；
- 第一批实施方案治理验证脚本。

第一阶段不声明任何项目真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

第二阶段建立核心链路项目唯一实施方案：

- GPCF；
- WAS世界资产体系；
- GlobalCloud XWAIL；
- GlobalCloud AaaS / AAAS；
- GlobalCloud WAES；
- GlobalCloud GFIS；
- GlobalCloud GPC；
- GlobalCloud PVAOS；
- GlobalCloud KDS；
- GlobalCloud Brain。

第二阶段不声明上述项目真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

第三阶段建立全部剩余支撑与智能体项目唯一实施方案：

- GlobalCloud Studio；
- GlobalCloud MMC；
- GlobalCloud PKC；
- GlobalCloud SOP；
- GlobalCloud XGD；
- GlobalCloud XiaoC；
- GlobalCloud XiaoG。

第三阶段完成后，可以声明所有登记业务项目均已有唯一当前有效实施方案，但仍不得声明真实研发完成、真实运行完成、真实集成完成、真实交付完成或客户验收完成。

## 17. 非声明边界

本文不声明：

- 不声明任何业务项目已经真实研发完成；
- 不声明任何业务项目已经真实运行完成；
- 不声明任何跨项目接口已经真实集成完成；
- 不声明任何项目已经客户交付完成；
- 不声明任何项目已经客户验收通过；
- 不声明 accepted、integrated 或 production_ready。
