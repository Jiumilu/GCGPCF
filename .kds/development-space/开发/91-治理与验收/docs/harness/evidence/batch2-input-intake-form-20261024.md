---
doc_id: GPCF-DOC-BATCH2-INTAKE-FORM-20261024
title: 批次 2 外部输入登记表（2026-10-24）
project: GPCF
related_projects: [GFIS, GPC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/batch2-input-intake-form-20261024.md
source_path: docs/harness/evidence/batch2-input-intake-form-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# 批次 2 外部输入登记表

> 用途：GFIS/GPC 属主按表登记真实输入；GPCF 只验收「真实文件 + 责任方确认」，不接受合成/演示数据。

## A. GFIS 5 类单据

| # | 类别 | 文件路径 | 来源系统/对方 | 日期 | 责任方确认（人/时间） | sha256 |
|---:|---|---|---|---|---|---|
| 1 | 订单 |  |  |  |  |  |
| 2 | 规格 |  |  |  |  |  |
| 3 | 交付要求 |  |  |  |  |  |
| 4 | 责任方确认 |  |  |  |  |  |
| 5 | 回款记录 |  |  |  |  |  |

客户确认：`customer_confirmation`（文件/邮件/回执）：
`owner_confirmation`：

## B. GPC PG-11

| # | 事项 | 值/路径 | 责任人 | 时间 |
|---:|---|---|---|---|
| 1 | PG-11 落点文档 |  |  |  |
| 2 | 外部地址/端口/证书 |  |  |  |
| 3 | 访问控制 |  |  |  |
| 4 | external runtime check 输出 |  |  |  |
| 5 | 8080 归属 |  |  |  |

## 验收口径

- 真实业务单据（非 fixture/mock/演示）；
- 有责任方确认与日期；
- 文件 hash 可复核；
- 任一项缺失 → 批次 2 不启动，状态不提升。

## 非声明

- 本表为登记模板；空白表示未到，不声明已具备输入。
