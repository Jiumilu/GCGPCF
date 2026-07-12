---
doc_id: GPCF-DOC-ICP-RISK-20260712
title: ICP 风险
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/icp/RISK.md
source_path: projects/icp/RISK.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

# ICP 风险

ICP 的主要风险是候选推理能力被误用为事实主账或治理批准。项目群纳入阶段只确认登记、边界和可回放证据，不确认生产接入、真实写入或验收完成。

| 风险 | 控制 |
|---|---|
| 资源投影被误作事实主账 | 只读接口、sourceRefs、projectionOnly 和 noWriteAssertion |
| 与 WAES 控制塔重叠 | ICP 只做产业计算候选，WAES 保留治理批准和状态门禁 |
| 与 GPC/GFIS 执行重叠 | 不提供订单、生产、库存、运输或设备写入接口 |
| fixture 通过被误作真实集成 | 状态保持 candidate/partial，真实连接器单独立项 |
| 第18项目导致历史计数漂移 | 不回写17项目历史证据，后续单独建立 ICP trigger/dependency |
