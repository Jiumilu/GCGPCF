---
doc_id: GPCF-DOC-85586D68F8
title: GC-Knowledge Fabric RAG 引用强度 L0-L5 规则
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/gc-knowledge-fabric/rag-citation-strength-policy.md
source_path: docs/gc-knowledge-fabric/rag-citation-strength-policy.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric RAG 引用强度 L0-L5 规则

## 1. 定位

本文件在 RAG 准入状态之上增加引用强度，避免 `safe` 被误解为“可直接形成业务决策、写回、收益确认或责任归因”。

本文件只定义 Brain、PKC、GFIS Assistant、指挥舱和审计检索的引用边界，不执行真实 RAG 检索，不写 KDS、WAES、GFIS/GPC 或外部 API。

## 2. 引用强度

| 强度 | 含义 | 允许场景 |
|---|---|---|
| `L0` | 不可引用 | 不召回、不展示、不作为回答依据 |
| `L1` | 仅检索召回 | 内部缺口发现、风险提示，不展示原文 |
| `L2` | 可展示摘要 | 元数据、摘要、受控原件指针，不展示敏感原文 |
| `L3` | 弱引用 | 助手可回答，但必须标注不确定性、来源边界和证据缺口 |
| `L4` | 强引用 | 可用于 Brain/PKC/GFIS Assistant 回答和 SOP 辅助依据 |
| `L5` | 业务辅助决策引用 | 仅限 T0/T1 且已确认对象；仍不能替代人工/委员会确认和业务写回门禁 |

## 3. RAG 状态映射

| RAG 准入状态 | 默认引用强度 |
|---|---|
| `blocked` | `L0` |
| `sensitive_metadata_only` | `L1` 或 `L2` |
| `repair_required` | `L1` 或 `L2` |
| `limited` | `L3` |
| `safe` | `L4` |
| `safe` + T0/T1 + 已确认 | `L5` |

## 4. 硬边界

1. `L0` 不得进入回答、摘要、写回建议、收益建议或指挥舱强引用。
2. `L1` 只能用于缺口发现、内部检索召回和风险提示。
3. `L2` 只能展示摘要、元数据和受控原件指针。
4. `L3` 必须显示来源边界和不确定性，不能作为业务结论。
5. `L4` 可强引用，但不能自动写回业务系统。
6. `L5` 可作为业务辅助决策引用，但仍需 WAES、KWE、人工或委员会确认才能进入正式写回、收益确认或责任归因。
7. 敏感资料即使满足 `safe`，也必须先通过 redaction、external share 和 ACL gate。

## 5. P0/P1 验收条件

- OKF 中有独立 RAG citation strength policy。
- Shared Types 中有 L0-L5、场景能力和 hard boundary 类型。
- Validator 能检查 RAG 状态到引用强度的映射、L5 不等于自动决策、敏感资料 metadata-only 边界和 no-write 断言。
