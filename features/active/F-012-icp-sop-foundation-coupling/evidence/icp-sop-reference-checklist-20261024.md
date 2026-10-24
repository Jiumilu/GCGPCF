---
doc_id: GPCF-DOC-F012-ICP-SOP-CHECKLIST-20261024
title: ICP→SOP 版本化引用清单（M1）
project: GPCF
related_projects: [ICP, SOP]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-012-icp-sop-foundation-coupling/evidence/icp-sop-reference-checklist-20261024.md
source_path: features/active/F-012-icp-sop-foundation-coupling/evidence/icp-sop-reference-checklist-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# ICP→SOP 版本化引用清单（M1）

> 依据 F-019 已验 API（5/5 GET 200）与 SOP 矩阵消费点。M1 交付物，待 SOP 属主评审。

## 1. ICP 引用端点

| 端点 | 内容 | 关键字段 |
|---|---|---|
| `GET /api/v1/industry-model` | 24 节点 | `nodes[].id/name/level` |
| `GET /api/v1/resource-pools` | 11 池 | `pools[].id/kind/projectionOnly` |
| `GET /api/v1/scenarios` | 3 场景 | `scenarios[].id/status` |
| `GET /api/v1/constitution-governance` | 5 角色 | `roles[].id/domainOwner/canonicalCustodian` |
| `GET /health` | 版本/健康 | `version/status` |

## 2. 版本化要求

- 每个响应必须带 `icp_model_version`（建议新增）；SOP 记录消费版本。
- SOP 启动时校验版本存在；缺失/不兼容 → 拒绝并给恢复提示。

## 3. SOP 消费点

| SOP 对象 | 消费 ICP |
|---|---|
| 矩阵节点 | 24 节点 id/name |
| 资源池 | 11 池 id/kind |
| 场景 | 3 场景 id/status |
| 角色/权限 | 5 角色 id + owner |
| 版本审计 | `icp_model_version` |

## 4. 禁止

- 复制 ICP 数据到 SOP 作为事实源；
- 在 SOP 内改 ICP 基线；
- 以 fixture 代替真实版本字段。

## 5. 验收（M1/M2）

- 清单评审通过；
- SOP 版本不兼容时拒绝并可恢复；
- 字段映射可回放（请求/响应样本）。

## 非声明

- 不声明已实现；不声明 F-012 可关闭。
