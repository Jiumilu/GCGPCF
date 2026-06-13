---
doc_id: GPCF-L4-MCL-README
title: Minimum Closed Loop Harness
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/minimum-closed-loop/README.md
source_path: docs/harness/minimum-closed-loop/README.md
sync_direction: bidirectional
last_reviewed: 2026-06-13
supersedes: []
superseded_by: []
---

# Minimum Closed Loop Harness

本目录收录 GlobalCloud 项目群最小闭环 L4 阶段的总控材料。

范围：

- 项目群最小闭环控制面。
- 12 项目职责、输入、输出、验证和 evidence 映射。
- 平台订单、样品确认、转量产、工厂订单、签收、异常对象契约。
- 项目级 evidence 与项目群 evidence 的双层索引。

硬约束：

- 样品确认是平台订单与工厂订单之间的独立阶段。
- 未完成客户签样、豁免或转量产门禁，不得进入工厂订单。
- 纯文档说明不得计为真实项目仓实质开发轮。
- 不自动标记 accepted 或 integrated。

文档清单：

| 文档 | 用途 |
|---|---|
| `control-plane.md` | L4-001 项目群最小闭环控制面 |
| `project-role-verification-matrix.md` | 12 项目职责、输入、输出、验证和 evidence |
| `object-contracts.md` | 核心对象与事件契约 |
| `evidence-index.md` | L4 项目群 evidence 总入口 |

