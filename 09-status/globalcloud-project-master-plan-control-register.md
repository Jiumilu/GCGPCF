---
doc_id: GPCF-DOC-WAS-PROJECT-MASTER-PLAN-REGISTER-20260624
title: GlobalCloud 项目群主方案控制台账
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-project-master-plan-control-register.md
source_path: 09-status/globalcloud-project-master-plan-control-register.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群主方案控制台账

日期：2026-06-24

## 1. 台账定位

本文是 `WAS世界资产体系总体方案` 的项目群主方案落地台账，用于登记项目群内每个项目的唯一当前有效总体方案、候选方案、缺口、冲突、继承状态和下一步动作。

本文不替代任何项目总体方案，也不把候选方案声明为已完成方案。本文只做控制、盘点、传导和门禁输入。

## 2. 控制原则

1. 项目群唯一总控方案是 `01-architecture/WAS世界资产体系总体方案.md`。
2. 每个项目只能有一个当前有效总体方案。
3. 项目总体方案必须继承主方案的结构、术语、版本基线、传导机制、测试交付和 LOOP 门禁。
4. 历史总体方案、实施方案、专项方案、README 和 AGENTS 不能自动等同于项目总体方案。
5. 主方案变化必须先更新本台账的受影响项目，再传导到对应项目总体方案。
6. 项目方案变化必须先回流到主方案或 Change Proposal，再更新本台账，再传导到关联项目。
7. 未经过用户确认的结构性变化，只能登记为 `candidate` 或 `repair_required`。

## 3. 状态定义

| status | 含义 |
|---|---|
| `authoritative` | 已明确为当前唯一有效总体方案 |
| `candidate` | 可作为主方案底稿，但尚未完成继承和确认 |
| `missing` | 尚未发现可用总体方案 |
| `conflict` | 存在多个候选或历史命名冲突 |
| `rename_required` | 内容可能可用，但名称或项目身份不符合主方案规范 |
| `inheritance_required` | 需要补齐主方案继承结构 |
| `not_project` | 不是业务项目，不要求项目总体方案 |

## 4. 项目主方案盘点

| project | repo_path | 当前有效总体方案 | 候选/相关文档 | status | 主要问题 | 下一步 |
|---|---|---|---|---|---|---|
| 项目群总控 | `GlobalCoud GPCF` | `01-architecture/WAS世界资产体系总体方案.md` | `AGENTS.md`, `README.md` | `authoritative` | 项目群唯一总体控制性文档 | 持续维护主方案、台账、术语、版本、传导和门禁 |
| GlobalCloud GPCF | `GlobalCoud GPCF` | `GlobalCloud GPCF 总体方案.md` | `01-architecture/WAS世界资产体系总体方案.md`, `AGENTS.md`, `README.md` | `authoritative` | 已建立 GPCF 作为治理项目的独立总体方案 | 后续补齐 GPCF 运行控制、文档治理和 LOOP evidence |
| WAS世界资产体系 | `WAS世界资产体系` | `docs/GlobalCloud WAS 总体方案.md` | `docs/GlobalCloud-WAS总体方案V1.2-GPCF统一重构版.md` | `authoritative` | 已建立仓内唯一当前有效总体方案，旧 V1.2 文档作为来源底稿 | 后续补充语义变更回流记录和验证证据 |
| GlobalCloud XWAIL | `GlobalCloud XWAIL` | `GlobalCloud XWAIL 总体方案.md` | `XWAIL实施方案.md` | `authoritative` | 已建立总体方案，实施方案降级为工程实施底稿 | 后续补齐 Schema/Validator/XAP 实现证据 |
| GlobalCloud AAAS / AaaS | `GlobalCloud AAAS` | `docs/GlobalCloud AaaS 总体方案.md` | `docs/AaaS总体方案_GPCF对齐版.md` | `authoritative` | 已统一显示名为 GlobalCloud AaaS，AAAS 保留为仓库名 | 后续补齐 ServicePackage/Metering/SLA 验证证据 |
| GlobalCloud WAES | `GlobalCloud WAES` | `GlobalCloud WAES 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐运行治理和发布证据 |
| GlobalCloud GFIS | `GlobalCloud GFIS` | `GlobalCloud GFIS 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐运行事实和集成证据 |
| GlobalCloud GPC | `GlobalCloud GPC` | `GlobalCloud GPC 总体方案.md` | `GPC-绿色供应链公共服务平台-总体方案.md`, 旧实施规划文件 | `authoritative` | 已建立当前唯一总体方案，旧业务架构文档作为输入来源 | 后续补齐 GFIS/PVAOS/WAES/AaaS 集成证据 |
| GlobalCloud PVAOS | `GlobalCloud PVAOS` | `GlobalCloud PVAOS 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐门户/运行平面集成证据 |
| GlobalCloud KDS | `GlobalCloud KDS` | `GlobalCloud KDS 总体方案.md` | `README.md`, `AGENTS.md`, `concepts/*` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐知识索引和证据准入验证 |
| GlobalCloud Brain | `GlobalCloud Brain` | `GlobalCloud Brain 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐知识治理和 AI 边界证据 |
| GlobalCloud Studio | `GlobalCloud Studio` | `GlobalCloud Studio 总体方案.md` | `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐建模配置和 Harness 证据 |
| GlobalCloud MMC | `GlobalCloud MMC` | `GlobalCloud MMC 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐 Harness 控制台运行和验收证据 |
| GlobalCloud PKC | `GlobalCloud PKC` | `GlobalCloud PKC 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐 KDS/Brain/XiaoC/WAES 集成证据 |
| GlobalCloud SOP | `GlobalCloud SOP` | `GlobalCloud SOP 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已补齐 AGENTS 并建立当前唯一总体方案 | 后续补齐 SOP 规则晋升和会话证据 |
| GlobalCloud XGD | `GlobalCloud XGD` | `GlobalCloud XGD 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐智能体运行、记忆和证据治理 |
| GlobalCloud XiaoC | `GlobalCloud XiaoC` | `GlobalCloud XiaoC 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐提示资产注册和 MCP 服务治理证据 |
| GlobalCloud XiaoG | `GlobalCloud XiaoG` | `GlobalCloud XiaoG 总体方案.md` | `README.md`, `AGENTS.md` | `authoritative` | 已建立当前唯一总体方案 | 后续补齐本地智能体运行和 Harness 证据 |
| shared/python_utils | `shared` | 不适用 | `shared/python_utils/` | `not_project` | 共享工具目录，不是业务项目 | 保留为共享库，受导入可用性和依赖治理控制 |

## 5. 当前结论

当前项目群已具备项目群主方案，第一批和第二批项目总体方案已建立，且 `GlobalCoud GPCF` 已从项目群总控方案中拆分出独立 `GlobalCloud GPCF 总体方案`。因此当前主方案对齐状态可判定为：

```text
project_master_plan_alignment = controlled
reason = all registered business projects have one authoritative project master plan
```

可以声明“项目群主方案控制机制已建立，全部登记业务项目均已具备唯一当前有效项目总体方案，并进入持续验证队列”。该结论不等于业务实现完成、客户交付完成或 production_ready。

## 6. 传导确认清单

每次主方案或项目方案发生结构性变化时，本台账必须记录：

| 检查项 | 要求 |
|---|---|
| 变化来源 | `master_plan` / `project_plan` / `change_proposal` |
| 影响项目 | 必须列出具体项目，不得只写“全项目” |
| 影响章节 | 必须列出定位、职责、接口、术语、版本、架构、测试、交付、LOOP 中受影响项 |
| 用户确认 | 必须记录是否已确认，未确认不得发布 |
| 传导状态 | `pending` / `patched` / `validated` / `blocked` |
| 验证证据 | 必须关联验证脚本、文档门禁和 KDS 镜像状态 |

## 7. 后续实施顺序

1. 建立并验证 `validate_project_master_plan_register.py`。
2. 已为已有候选文档的项目完成重命名或继承补齐：WAS、XWAIL、AaaS、GPC。
3. 已完成第一批项目总体方案：WAES、GFIS、PVAOS、KDS、Brain、Studio。
4. 已建立第二批项目总体方案：MMC、PKC、SOP、XGD、XiaoC、XiaoG。
5. 已建立 `GlobalCloud GPCF 总体方案.md`，明确 GPCF 作为治理项目的独立职责。
6. 更新 AGENTS 控制声明，要求每个项目只能引用本台账登记的当前有效总体方案。
7. 持续运行文档门禁、污染检查、KDS TOKEN 检查和 LOOP 文档门禁。
