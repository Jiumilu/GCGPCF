---
doc_id: GPCF-DOC-EXTERNAL-AUTHORIZATION-LIST-20261022
title: 项目群外部授权清单 v1.0（2026-10-22）
project: GPCF
related_projects: [GPCF, GFIS, GPC, PMC, Hermes, KDS]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-external-authorization-list-v1.0.md
source_path: 09-status/globalcloud-external-authorization-list-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群外部授权清单 v1.0（2026-10-22）

> 性质：把当前仍需老卢授权/外部条件的动作收敛为**一张清单**；每项含目标、范围、风险、前置、回滚、建议批次。
> 非声明：本清单不表示任何授权已发生；`authorization_granted` 以问答回执为准。

## 1. 总表

| # | 授权项 | 类别 | 当前状态 | 前置条件 | 风险 | 建议批次 |
|---:|---|---|---|---|---|---|
| 1 | GFIS 真实 source-of-record 接入（`AUTH-WAVE1-GFIS-REAL-SOR-20260626`） | C 真实数据 | pending | 5 类真实单据（订单/规格/交付/责任方/回款）到齐 | 中 | 批次 2 |
| 2 | GPC 外部 runtime 联调（`AUTH-WAVE1-GPC-EXTERNAL-RUNTIME-20260626`） | C 外部联调 | pending | 运行宿主就绪（PG-11）、外部接口可达 | 中 | 批次 2 |
| 3 | PMC 幂等复跑（F-028 full sync created=0） | 高危险 | 未授权 | 隔离 Plane 实例 + 本机开发凭据 + 验证后清理 | 高 | 批次 3 |
| 4 | 远端 CI / push（GPCF/KDS workflow + 三闸生效） | Git/发布 | 未授权 | workflow 本地验证通过、push 授权 | 中高 | 批次 1 |
| 5 | Hermes 对外 Web UI 恢复（`hermes.csydsc.com` 502） | 对外暴露 | 未授权 | Caddy/SSH 隧道核验 + 访问控制确认 | 高 | 批次 3 |

已完成、无需再授权：KDS whitespace cleanup（no-op）、WAS `.DS_Store` 删除、Studio 作废/替代、WAE 方案落仓、PG-12 契约落仓。

## 2. 逐项说明

### 2.1 GFIS 真实 SOR 接入
- 目标：取得并验证 5 类真实单据，进入 S4 真实业务验证线。
- 范围：脱敏接收、source validation、runtime intake、review queue；**不上生产、不写客户原件**。
- 风险：中；错误数据可能污染验证链。
- 回滚：删除/隔离测试数据；恢复配置；保留回执。
- 就绪条件：PG-05 请求包已被业务方接受，owner 指定。

### 2.2 GPC 外部 runtime 联调
- 目标：补 GPC production/external/runtime 证据。
- 范围：外部只读联调、GCFIS runtime surface 可达性、证据采集。
- 风险：中；外部接口不可控。
- 回滚：撤销联调配置；保留失败记录。
- 就绪条件：PG-11 运行宿主可用；外部地址与权限确认。

### 2.3 PMC 幂等复跑
- 目标：连续两次全量同步回读 `created=0`，把幂等从 B 级升到 A 级。
- 范围：隔离本地 Plane 实例 + 迁移 + admin 初始化 + 开发凭据 + 两次全量同步 + 清理。
- 风险：高（凭据创建/使用、临时实例、删除清理）。
- 回滚：销毁临时实例与凭据；不触碰共享/生产实例。
- 就绪条件：授权 + 隔离实例方案确认。

### 2.4 远端 CI / push
- 目标：GPCF/KDS 的 3 个门禁在 PR 上自动运行，关闭规则版本生效。
- 范围：workflow 文件、push、PR 验证；不改业务代码。
- 风险：中高；push 即进入共享历史。
- 回滚：revert commit / 禁用 workflow；保留本地文件。
- 就绪条件：workflow 本地验证通过、push 授权。

### 2.5 Hermes 对外 Web UI 恢复
- 目标：`hermes.csydsc.com` 从 502 恢复；本机 8648 已验证可启动（HTTP 200）。
- 范围：Caddy/SSH 隧道核验、访问控制确认、对外路由恢复。
- 风险：高（对外暴露、认证边界）。
- 回滚：撤 Caddy 路由/隧道，恢复 502；保留本机验证证据。
- 就绪条件：访问控制确认 + 对外恢复授权。

## 3. 建议批次

| 批次 | 内容 | 理由 |
|---|---|---|
| 批次 1 | 远端 CI/push | 本地已具备，风险可控，收益直接 |
| 批次 2 | GFIS SOR + GPC runtime | 依赖外部输入/宿主，条件成熟再批 |
| 批次 3 | PMC 幂等 + Hermes 对外 | 高危险，需单独隔离方案与回滚演练 |

## 4. 问答模板（逐项）

```text
是否授权 <授权项>？
范围：<scope>
风险：<risk>
回滚：<rollback>
选项：批准 / 部分批准 / 暂缓
```

## 5. 非声明

- 不声明任何授权已发生；
- 不声明任何项目状态提升或对外恢复完成；
- 不声明凭据已创建或生产实例被写入。
