---
doc_id: GPCF-DOC-666112D107
title: LOOP Delivery Efficiency Control
project: WAES
related_projects: [AAAS, Brain, WAS, XiaoC, WAES, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_DELIVERY_EFFICIENCY_CONTROL.md
source_path: 02-governance/loop/LOOP_DELIVERY_EFFICIENCY_CONTROL.md
sync_direction: bidirectional
last_reviewed: 2026-07-08
supersedes: []
superseded_by: []
---

# LOOP Delivery Efficiency Control

本文把 Studio 与 Brain 评估中暴露的经验升级为项目群级 LOOP 交付效率控制。它覆盖 `project_group_scope_17_projects`：AAAS、Brain、WAS、XiaoC、WAES、GPC、Studio、GPCF、XWAIL、GFIS、MMC、KDS、XiaoG、PVAOS、SOP、PKC、XGD。

## 1. 最高裁决

```text
high_compliance_low_product_progress is a LOOP failure mode.
Governance progress must not crowd out product progress.
Every Delivery Loop must expose product_delta or explicitly mark product_progress=false.
Single label/copy tweaks must not trigger heavy LOOP unless they block the main user path.
Project-group governance improves speed by reducing drift, not by expanding proof surfaces.
```

## 2. 控制目标

本控制用于防止以下偏差：

- LOOP 每轮都合规，但用户可感知进展很小。
- governance_progress 快于 product_progress，导致工程主进程被证明、文案和测试适配吞没。
- UI、业务流、接口、数据链路或项目任务被拆成过细切片，形成大量低实质轮次。
- 多会话并行开发把治理收据当成产品交付结果。
- 单个项目的经验只留在本地，没有覆盖整个项目群。

## 3. Delivery Efficiency Gate

所有开发态 Delivery Loop 必须显式记录以下字段：

| Field | 要求 | 失败后处理 |
|---|---|---|
| `product_delta` | 本轮带来的产品、业务流、接口、数据处理、用户任务或运行能力增量 | 没有增量时必须标记 `product_progress=false` |
| `user_visible_delta` | 用户、开发者、运营或审查者可复现的可见变化；纯内部治理可写 `none` | 连续 3 轮为 `none` 时必须回到治理复核 |
| `loop_cost_level` | `G0`、`G1` 或 `G2`；不得用 G2 处理普通 G0 小切片 | 成本过高时降级为轻量 Delivery Loop |
| `substantive_round` | 是否满足独立输入、判断、输出、验证、反馈中的至少 4 项 | 不满足不得计入连续运行实质轮次 |
| `task_flow_e2e_status` | 涉及产品流时必须验证任务流，而不是只验证证据存在 | 失败时进入 rework |
| `evidence_overexposure_gate` | 默认产品面不得被 evidence、receipt、preflight、dry-run、boundary、readiness、audit 淹没 | 失败时进入 rework |
| `delivery_efficiency_gate` | 本轮治理成本与产品增量匹配 | 失败时压缩 LOOP 或合并切片 |

## 4. 快速开发规则

开发态默认执行轻量 Delivery Loop：

```text
goal / changed / verified / risk / next
```

每轮还必须给出：

```text
product_delta
user_visible_delta
loop_cost_level
substantive_round
task_flow_e2e_status
evidence_overexposure_gate
delivery_efficiency_gate
```

`single_label_copy_tweak_heavy_loop_blocked`：单个 label、copy、测试选择器或同类微文案调整，不得独立触发完整 G2 治理轮，除非它阻塞主用户路径、授权边界、P0/P1 风险或状态提升。

## 5. 治理瘦身规则

- 每个 Delivery Loop 最多保留 1 个主 evidence，除非触发 P0/P1、真实 API、KDS、deploy、状态提升或跨项目冲突。
- 连续 3 轮只有 governance_progress、没有 product_progress，必须暂停开发态并登记 `high_compliance_low_product_progress`。
- 文档、validator 和测试只能服务交付闭环；不得把新增证明面当成产品完成。
- 多智能体并行开发必须绑定不重叠 scope；最终合并前必须复核 product_delta 与 evidence_overexposure_gate。
- 输出必须继续遵守 `DO NOT send optional commentary`。

## 6. 项目群覆盖规则

本控制默认覆盖全部 17 项目。各项目本地 LOOP 可保留自己的开发目标，但必须接收以下项目群级约束：

- Studio、Brain、GPC、PVAOS、XiaoC、XGD、XiaoG 等产品界面或工作台项目，必须同时遵守 `LOOP_UI_PRODUCT_FIRST_CONTROL.md`。
- GFIS、KDS、WAES、MMC、SOP、PKC、WAS、AAAS、XWAIL 等非 UI 主线，必须用 `product_delta` 表达真实开发、运行、数据、接口、治理或审查能力增量。
- GPCF 只负责项目群 LOOP 防偏、门禁和经验传导，不隐式接管项目本地目标。
- 需要提交、推送、真实外部 API、真实 KDS API、deploy、生产写入或状态提升时，必须重新获得人工授权。

## 7. Validator

本控制由以下脚本检查：

```bash
python3 tools/kds-sync/validate_loop_delivery_efficiency_control.py
```

该 validator 必须接入 `loop_document_gate.py`，并与 `validate_loop_ui_product_first_control.py` 共同约束项目群开发态 LOOP。
