---
doc_id: GPCF-DOC-F032-PQC-PVA-CHECKLIST-20261024
title: PQC↔PVA 外部服务接口清单（M1/M2）
project: GPCF
related_projects: [PQC, PVA]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# PQC↔PVA 外部服务接口清单（M1/M2）

> PQC 询价/测算/订单服务经 PVA PVAAI 对话与应用模块承载；数据在 PQC 执行。

## 1. 接口（建议）

| 能力 | 方法/路径 | 关键字段 |
|---|---|---|
| 询价 | `POST /api/v1/pqc/inquiry` | `items[]/quantity/delivery/currency` |
| 测算 | `POST /api/v1/pqc/estimate` | `inquiry_id/process/params` |
| 下单 | `POST /api/v1/pqc/order` | `estimate_id/contract/terms` |

## 2. 契约字段

- `request_id` 幂等键（PQC 生成/校验）
- `pva_conversation_id`（PVA 承载，不传业务敏感数据）
- `pqc_model_version`（版本冻结）
- 错误码：`PQC-401/403/409/422/429/5xx`（与错误码注册表一致）

## 3. 数据边界

- 业务数据只在 PQC 执行；PVA 只承载对话/应用模块，不复制 PQC 数据。
- PVA 不持久化 PQC 订单/回款。

## 4. 回滚

- 关闭 PVA 入口即回退；PQC 侧接口保留但不可达。

## 5. 验收（M1/M2）

- 设计评审通过；
- 契约版本/字段/错误码冻结；
- 合成数据试点通过，不声明生产。

## 非声明

- 不声明已实现；不声明 F-032 可关闭。
