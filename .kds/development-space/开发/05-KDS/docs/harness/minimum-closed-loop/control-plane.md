---
doc_id: GPCF-DOC-9886BDB110
title: L4 Control Plane
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/minimum-closed-loop/control-plane.md
source_path: docs/harness/minimum-closed-loop/control-plane.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# L4 Control Plane

## 主链路

- 项目初始化 -> 组织/伙伴接入 -> 平台订单
- 样品打样/样箱打样 -> 客户签样确认 -> 转量产门禁 -> 工厂订单
- 样品确认独立阶段
- 禁止绕过门禁
- 12 项目不缺席

## GFIS 运行层约束

- GFIS 当前承载现代精工 OEM 代加工生产，葛化自建工厂投产后继续使用同一 GFIS 运行时系统。
- GFIS Demo 只能作为展示、培训和前端回归，不得替代运行层事实。
- 未取得真实 customer requirement/platform order source-of-record、dispatch confirmation、WAES confirmation、KDS write receipt 和 runtime primary key 前，完整 SOP E2E 必须保持 `repair_required`。
