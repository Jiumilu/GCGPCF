---
doc_id: GPCF-DOC-66A701A0F6
title: GPCF-KDS-DKS-003 完整实施提示词 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-003.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-003 完整实施提示词 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

用户要求“给出完整实施的提示词，并建立目标开始执行，在过程中可以进行问答”。前两轮已完成：

1. `GPCF-KDS-DKS-001`：纳入 Loop Engineering 并形成总体实施治理方案。
2. `GPCF-KDS-DKS-002`：形成对象字段与 KDS 11 池映射清单。

本轮补齐可复用的主控实施提示词，作为后续 AI、团队、项目负责人和治理委员会推进本专题的统一入口。

## 2. 动作

本轮执行动作：

1. 建立受控提示词文档：
   `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统完整实施提示词.md`
2. 将用户已确认的治理原则、业务事实、葛化重点、湖北磷材重点、积分收益规则、AI 边界和问答机制整合为主控提示词。
3. 定义每轮输出格式和当前优先队列。
4. 明确不得自动确认业务事实、收益分配、积分结算或 accepted / complete / integrated 状态。

## 3. 输出

本轮产出：

| 产物 | 路径 | 说明 |
|---|---|---|
| 完整实施提示词 | `03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统完整实施提示词.md` | 可复用的主控实施提示词，支撑后续问答、Loop round 和协同智能体执行 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-003.md` | 记录本轮五段式治理微循环 |

## 4. 检查

本轮检查口径：

| 检查项 | 结果 | 说明 |
|---|---|---|
| 用户请求覆盖 | pass | 已补齐完整实施提示词 |
| Loop 纳入 | pass | 提示词要求每轮进入 `GPCF-KDS-DKS-XXX` |
| 问答机制 | pass | 每轮最多提出 5 个高价值问题，并给建议默认方向 |
| 用户掌控 | pass | 用户保留治理急停权，委员会负责具体裁决 |
| AI 越权边界 | pass | 明确 AI 不得写业务主账或确认关键事实 |
| 状态升级 | pass | 不允许自动 accepted / complete / integrated |
| Git 工作区保护 | partial | 当前工作区已有大量既有变更；本轮只新增本专题 DKS-003 相关文件 |

## 5. 反馈

本轮结论：

1. 绿色供应链分布式知识系统已有总体方案、对象字段清单和完整实施提示词。
2. 本专题可以继续按 `GPCF-KDS-DKS` Round 推进。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-004：
建立葛化订单运行母版字段/单据映射专项，优先围绕辽宁远航链路、现代精工 OEM 过渡、质量/发货/POD/金融凭证门禁形成可验收清单。
```

待用户回答：

1. 葛化辽宁远航链路现有材料中，客户确认函、23个样箱测试反馈、POD、质量报告、金融凭证分别在哪里？
2. 现代精工 OEM 过渡资料中，哪些事实可以进入共享知识库，哪些必须限制在 DSR-L2 / DSR-L3？
3. 葛化 GFIS 文档验收助手第一阶段要优先验收哪些文档类型？
4. 湖北磷材拓厂项目第一批材料来源是什么？
5. 知识收益治理委员会首批成员角色是否按主控提示词候选结构建立？
