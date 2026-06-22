---
doc_id: GPCF-DOC-CD0C4E3CF7
title: GPCF-KDS-DKS-010 葛化 GFIS AI 助手内测运行记录模板 Loop 记录
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-010.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-010.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-KDS-DKS-010 葛化 GFIS AI 助手内测运行记录模板 Loop 记录

日期：2026-06-17
状态：loop_ready / manual_confirmation_required
模式：GPCF 方案治理微循环

## 1. 输入

上一轮 `GPCF-KDS-DKS-009` 已完成葛化 GFIS AI 助手首批问答与文档验收评测集，并建议本轮建立内测运行记录模板。

本轮默认采用以下方向：

1. 内测先限制在楚商云 / 葛化项目组内部。
2. 红线测试作为上线前一票否决项。
3. 评测通过阈值先采用 85 分。
4. 评测记录只保存脱敏输入输出摘要，不保存敏感原文。
5. 内测贡献只形成候选积分，不进入确认积分。

## 2. 动作

本轮执行动作：

1. 建立受控模板：
   `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录模板.md`
2. 定义 `PilotSession`、`QuestionSample`、`DocumentSample`、`AssistantOutputRecord`、`EvalRecord`、`DefectRecord`、`KnowledgeGapRequestCandidate`、`WritebackCandidate`、`ContributionEventCandidate`。
3. 定义内测运行节奏、通过条件和首批样本建议。
4. 明确本轮不启动真实内测，不写真实 GFIS / KDS / WAES API，不确认业务事实。

## 3. 输出

| 产物 | 路径 | 说明 |
|---|---|---|
| 葛化 GFIS AI 助手内测运行记录模板 | `03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录模板.md` | 定义内测运行对象、字段、缺陷回流、知识缺口、回写候选和贡献候选 |
| Loop round 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-010.md` | 记录本轮五段式治理微循环 |

## 4. 检查

| 检查项 | 结果 | 说明 |
|---|---|---|
| 内测边界 | pass | 只定义模板，不启动内测 |
| 脱敏边界 | pass | DSR-L2 / DSR-L3 默认只记录脱敏摘要 |
| 红线边界 | pass | P0 红线立即暂停对应助手 |
| 积分边界 | pass | 内测贡献只形成候选积分 |
| 写入边界 | pass | 本地镜像不等于真实 API 回执 |
| 状态升级 | pass | 本轮不声明 accepted、complete 或 integrated |

## 5. 反馈

本轮结论：

1. 葛化 GFIS AI 助手内测运行记录模板已形成。
2. 内测数据可按对象流回写为 KDS / WAES 候选记录、知识缺口、缺陷和贡献事件。
3. 当前状态仍为 `loop_ready / manual_confirmation_required`。

下一轮建议：

```text
GPCF-KDS-DKS-011：
绿色供应链分布式知识系统数据对象最小落库与 API 契约草案，把 DKS-001 至 DKS-010 的对象固化为最小表、事件、状态机和权限契约。
```

待用户回答：

1. 内测是否先限制为楚商云 / 葛化项目组内部批次？
2. DSR-L2 / DSR-L3 是否一律只记录脱敏摘要，不保存原文？
3. P0 红线是否立即暂停对应助手，而不是只返工？
4. 内测贡献是否只产生候选积分，不进入确认积分？
5. DKS-011 是否进入数据对象最小落库与 API 契约草案？
