---
doc_id: GPCF-DOC-6B5483766B
title: GFIS 质量与安全门禁候选
project: GFIS
related_projects: [GFIS, GPC, WAES, GPCF]
domain: evidence
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/08-evidence-samples/GFIS/gfis-quality-gate-candidates.md
source_path: 08-evidence-samples/GFIS/gfis-quality-gate-candidates.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GFIS 质量与安全门禁候选

Round ID：`GPCF-GF-LR-001`

## 门禁清单

| 门禁 | 触发点 | GFIS 事实 | WAES 判定 | 默认动作 |
|---|---|---|---|---|
| 未检验不得入库 | 原料到厂、成品完工 | 检验记录、结果、检验人 | 是否允许入库 | 阻断入库 |
| 未确认不得量产 | 首件完成 | 首件确认数据 | 是否允许批量生产 | 阻断工单放量 |
| 未放行不得发货 | 出库前 | 成品检验、隔离状态 | 是否允许出库 | 阻断出库 |
| 未隔离不得返工 | 不合格发现 | 不合格批次、隔离库位 | 返工路径是否合规 | 阻断返工 |
| 未闭环不得销项 | 异常处理 | 异常单、责任人、处理结果 | 是否允许关闭 | 阻断关闭 |
| 安全异常不得开机 | 设备点检异常 | 点检记录、故障等级 | 是否允许生产 | 阻断开机 |
| 批次不清不得追溯完成 | 追溯缺失 | 批次、码值、工单关系 | 是否接受证据 | 阻断追溯完成 |

## 门禁状态

| 状态 | 含义 | 可执行动作 |
|---|---|---|
| draft | 候选门禁，未现场确认 | 仅用于设计 |
| active | 已确认可执行 | 可进入 GFIS 开发任务 |
| waes_required | 需要 WAES 审批或放行规则 | 不得由 GFIS 单独判定 |

## 首轮结论

GFIS 只负责记录事实、发起阻断和提供证据；最终放行、豁免、越权控制应由 WAES 形成治理判定。
