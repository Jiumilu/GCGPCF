---
doc_id: GPCF-DOC-62B1AFEC53
title: GPCF Project Group Phase Goals
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PHASE-GOALS-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PHASE-GOALS-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF Project Group Phase Goals

## 输入

本轮目标是建立 GlobalCloud V0.0.1 项目群阶段性工作目标，作为 CodeGraph 项目群集成收口后的 Loop 下一轮控制输入。

本文件只定义项目群治理目标、证据门禁和下一轮输入，不进入任何项目内部业务开发任务。

## 动作

- 固化 14 仓项目群阶段目标。
- 明确 GFIS 真实源记录准备、运行治理路径、ready_for_review 项目群硬化和接受准备包的分阶段边界。
- 生成下一轮受控输入，保持不进入内部业务开发、不升级 accepted/integrated/production_ready。

## 输出

- 本 Loop round 文件作为阶段目标控制记录。
- 下一轮输入 `GPCF-PROJECT-GROUP-GFIS-REAL-SOURCE-RECORD-READINESS-001`。

## 当前事实基线

| 维度 | 当前事实 | 阶段含义 |
| --- | --- | --- |
| 项目群范围 | GFIS、GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、GPCF、Studio、WAS，共 14 仓 | 后续项目群目标必须覆盖 14 仓，不再沿用 12 仓口径 |
| CodeGraph | 14 仓已纳入项目群代码图谱；13 仓 up-to-date；GFIS 为 controlled_residual | CodeGraph 阶段从部署集成转为持续监控 |
| 状态矩阵 | 12 个项目 ready_for_review；GFIS、GPCF 为 repair_required | 项目群瓶颈集中在 GFIS 真实业务链路与 GPCF 收口状态 |
| GFIS | 真实业务链路仍为 repair_required，真实提交文件、有效源记录、可进入下一门禁数量仍未闭合 | 下一阶段优先处理真实源记录准备，而不是扩展功能 |
| Studio | 已纳入项目群、CodeGraph 与 Loop 体系；发布工作流权限仍需显式审查 | Studio 不进入发布动作，只补齐 release boundary 证据 |
| WAS | 已纳入项目群、CodeGraph 与 Loop 体系；定位为语义基础工程候选 | WAS 不替代 KDS/GFIS/WAES，只作为语义契约与 crosswalk 基线 |
| 接受状态 | 当前不得宣称 accepted、integrated、production_ready | 所有阶段目标都必须以 evidence gate 为准 |

## 阶段目标总览

| 阶段 | 名称 | 范围 | 目标 | 完成定义 |
| --- | --- | --- | --- | --- |
| Phase A | 项目群治理基线稳定 | 14 仓、GPCF、CodeGraph、Loop | 固化 14 仓覆盖、CodeGraph 监控、文档门禁、GPCF validator 与 Loop 下一轮输入 | CodeGraph monitor 可回放；文档污染、KDS token、Loop document gate 通过；不进入项目内部开发 |
| Phase B | GFIS 真实源记录准备 | GFIS、GPCF，关联 GPC/KDS/WAES/WAS | 获取或登记真实客户订单、平台回执或等价正式输入，并完成字段级 readiness 包 | `submitted_files_found >= 1`、`valid_source_records >= 1`、`accepted_for_next_gate >= 1`；禁止伪造样例冒充真实业务 |
| Phase C | GFIS 运行治理路径准备 | GFIS、WAES、GPCF | 在真实源记录通过后，进入 runtime primary key、review queue、runtime intake、WAES review、verified artifact 准备 | `runtime_primary_key_ready >= 1`、`review_queue >= 1`、`runtime_intake >= 1`、`waes_review >= 1`、`verified >= 1`；生产写入需另行授权 |
| Phase D | ready_for_review 项目群硬化 | GPC、PVAOS、WAES、KDS、Brain、PKC、XiaoC、XGD、XiaoG、MMC、Studio、WAS | 不做业务功能开发，只补齐治理证据、角色边界、dry-run 证据和发布边界审查 | 每个项目具备当前 loop-state、evidence-index、validator 或等价状态证据；项目角色无陈旧歧义 |
| Phase E | 接受准备包 | 项目群整体 | 在 GFIS 真实链路闭合且用户明确授权后，整理 acceptance package、回滚计划、监控计划与人工签署材料 | 有 WAES 判定证据、UAT/signoff、rollback/monitor plan 和用户显式授权；不得自动升级状态 |

## 项目群分工边界

| 项目 | 阶段职责 | 当前控制点 |
| --- | --- | --- |
| GFIS | Phase B/C 主瓶颈 | 真实源记录与运行治理链路未闭合 |
| GPCF | Loop 编排、证据门禁、项目群状态收口 | 不替代项目内部实现，不擅自升级接受状态 |
| GPC | 合同、订单、平台输入边界协同 | 提供正式输入或字段映射证据 |
| WAES | 审查与验收治理 | 只基于证据判定，不替代执行层 |
| KDS | source of record 与文档受控 | 保护 canonical Markdown 与 token 安全 |
| WAS | 语义契约与 crosswalk 基线 | 不替代 KDS/GFIS/WAES 层职责 |
| Studio | 项目群新纳入工程与 release boundary 审查 | 不执行发布，只审查权限与证据 |
| Brain、PKC、XiaoC、XGD、XiaoG、MMC、PVAOS | ready_for_review 项目群硬化 | 补证据、补边界、补 dry-run，不进入内部开发 |

## 禁止事项

- 不进入任何项目内部业务开发任务。
- 不宣称 accepted、integrated、production_ready。
- 不执行真实外部 API、生产写入、部署、发布、schema migration。
- 不写入或暴露 token，不破坏 KDS canonical Markdown。
- 不自动 commit、push、merge 或创建 PR。
- 不用 mock/demo/治理材料冒充真实业务闭环。

## 下一轮输入

```text
loop_id: GPCF-PROJECT-GROUP-GFIS-REAL-SOURCE-RECORD-READINESS-001
objective: 将项目群阶段目标转化为 GFIS 真实源记录 readiness 包；若真实输入不存在，则生成 hold register，不进入项目内部开发。
scope:
  include:
    - GFIS 真实客户订单或平台回执输入登记
    - GFIS native 12 字段与 WAS 12 字段 crosswalk readiness
    - 预检、负例门禁、状态证据
    - CodeGraph 项目群持续监控引用
  exclude:
    - 业务代码实现
    - 生产 API 写入
    - 发布、部署、schema migration
    - accepted/integrated/production_ready 状态升级
allowed_actions:
  - read_only_scan
  - controlled_document_update
  - validator_run
  - evidence_index_update
stop_condition:
  - 缺少真实客户订单、平台回执或等价正式输入
  - 任何动作需要生产写入、发布权限或用户显式验收
```

## 检查

```bash
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
git diff --check -- docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-PHASE-GOALS-001.md
```

## 连续运行真实性记录

| 字段 | 值 |
| --- | --- |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 1 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |
