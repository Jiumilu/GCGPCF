---
doc_id: GPCF-DOC-BATCH2-EXTERNAL-REQUEST-PACK-20261022
title: 批次 2 外部输入催办包（2026-10-22）
project: GPCF
related_projects: [GPCF, GFIS, GPC, SOP]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/batch2-external-request-pack-20261022.md
source_path: docs/harness/evidence/batch2-external-request-pack-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 批次 2 外部输入催办包（2026-10-22）

> 依据：`docs/harness/evidence/batch2-prerequisites-20261022.md`（GFIS 0/5，GPC not_ready）。
> 性质：催办清单与请求模板；不包含凭据请求；不声明任何数据已到。

## 1. GFIS：5 类真实单据（业务方 → GFIS）

| # | 单据 | 最小字段/格式 | 验收判据 | 责任方 | 状态 |
|---:|---|---|---|---|---|
| 1 | 订单 | 订单号、客户、金额、签章/平台回执 | 可核对来源；非报价单 | 辽宁远航/现代精工 | 待交 |
| 2 | 规格 | 物料/型号/技术参数清单 | 与订单可关联 | 业务方 | 待交 |
| 3 | 交付 | 交付单/DeliveryNote/POD | 签收或物流回执 | 业务方 | 待交 |
| 4 | 责任方 | 项目负责人/供应商联系人确认 | `owner_confirmation` 字段 | 业务方 | 待交 |
| 5 | 回款 | 银行流水/对账/发票（脱敏） | 金额与订单可勾稽 | 业务方/财务 | 待交 |

补充要求：
- 客户确认：`customer_confirmation` 显式签署/邮件确认（当前字段不存在）。
- 脱敏：不提交客户原件到仓库；走 GFIS source validation 受控目录。
- 到齐后：GFIS `source validation` → `real_source_records>0` → 再申请批次 2 联调。

## 2. GPC：PG-11 运行宿主与外部 runtime

| # | 事项 | 要求 | 责任方 | 状态 |
|---:|---|---|---|---|
| 1 | PG-11 落点 | 明确 GPC 在 PG-11 的宿主/容器/进程 | GPC 属主 | 待定 |
| 2 | 外部地址 | 域名/端口/证书（或明确仅内网） | GPC 属主 | 待定 |
| 3 | 访问控制 | 认证方式、来源白名单、最小权限 | GPC 属主 + 安全 | 待定 |
| 4 | external runtime check | 可回放的联调检查脚本与证据 | GPC 属主 | 待产出 |
| 5 | 8080 归属 | 当前本机 `127.0.0.1:8080` 被 PID 798 占用，归属待核 | GPC 属主 | 待核 |

## 3. 请求模板

### 3.1 给业务方（GFIS）

```text
主题：批次 2 真实业务验证材料请求（5 类）
请提供：订单、规格、交付、责任方确认、回款 5 类材料（脱敏），并出具客户确认。
用途：GFIS source validation → 批次 2 联调；不用于生产写入。
回执：材料清单 + 确认人 + 日期。
```

### 3.2 给 GPC 属主

```text
主题：PG-11 GPC 外部 runtime 就绪确认
请明确：PG-11 落点、外部地址/端口/证书、访问控制、external runtime check 脚本、8080 归属。
用途：批次 2 GPC 外部联调；不涉及生产发布。
回执：就绪结论 + 证据路径。
```

## 4. 跟踪与升级

| 项 | 卡点 | 升级条件 |
|---|---|---|
| GFIS 5 类 | 业务方未交 | 超过 3 个工作日 → 升级老卢 |
| GPC PG-11 | 属主未定 | 超过 3 个工作日 → 升级老卢 |

## 5. 非声明

- 不声明任何单据已到、客户已确认、宿主已就绪；
- 不请求、不创建、不读取任何凭据；
- 不声明任何项目状态提升。
