---
doc_id: GPCF-DOC-F012-ICP-SOP-CHECKLIST-20261024
title: ICP→SOP 版本化引用清单（M1）
project: GPCF
related_projects: [ICP, SOP]
domain: governance
status: draft
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-012-icp-sop-foundation-coupling/evidence/icp-sop-reference-checklist-20261024.md
source_path: features/active/F-012-icp-sop-foundation-coupling/evidence/icp-sop-reference-checklist-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-27
supersedes: []
superseded_by: []
---

# ICP→SOP 版本化引用清单（M1）

> 依据 F-019 已验 API（5/5 GET 200）与 SOP 矩阵消费点。M1 交付物，待 SOP 属主评审。
>
> **v1.1（2026-10-27）字段名更正**：v1.0 的字段名与 ICP 实际响应不符，由 ICP 属主实测核对后更正（见 `docs/governance/loop-治理收敛范围与判据.md` 的判据纪律：接口事实必须来自实测，不得从文档推定）。v1.0 的字段名若不修，SOP 侧照抄会拿到不存在的字段。

## 1. ICP 引用端点

| 端点 | 内容 | 关键字段（ICP 属主实测） |
|---|---|---|
| `GET /api/v1/industry-model` | 24 节点 | `nodes[].code / label / group / position / meaning` |
| `GET /api/v1/resource-pools` | 11 池 | `pools[].code / name / layer / aliases` |
| `GET /api/v1/scenarios` | 3 场景 | `scenarios[].scenarioId / scenarioName` |
| `GET /api/v1/constitution-governance` | 5 角色 | `roles[].role / project / allowedActions / forbiddenActions` |
| `GET /health` | 健康 | `status`（**无 `version`**）；版本在 `industry-model.version` |

字段名以本表为准，逐条对照实测响应；v1.0 的错值只在文末「附：更正对照（勿照抄）」留痕。

待核一项：v1.0 在 resource-pools 行写过的 `projectionOnly` **不在 ICP 属主实测表内**，本页不再把它当接口事实；如需使用，须 ICP 属主再核一次。

## 2. 版本化要求

- 版本字段**不新增**：`industry-model.version` 已存在，直接消费它。v1.0 曾建议新增一个版本字段，**该建议作废**——那会引入一次不必要的跨仓 schema 改动。
- SOP 记录消费到的 `industry-model.version`。
- SOP 启动时校验该版本存在；缺失/不兼容 → 拒绝并给恢复提示。

## 3. SOP 消费点

| SOP 对象 | 消费 ICP |
|---|---|
| 矩阵节点 | 24 节点 `code / label / group / position / meaning` |
| 资源池 | 11 池 `code / name / layer / aliases` |
| 场景 | 3 场景 `scenarioId / scenarioName` |
| 角色/权限 | 5 角色 `role / project / allowedActions / forbiddenActions` |
| 版本审计 | `industry-model.version` |

## 4. 禁止

- 复制 ICP 数据到 SOP 作为事实源；
- 在 SOP 内改 ICP 基线；
- 以 fixture 代替真实版本字段；
- 从文档推定字段名而不实测（本次五处错字的成因）。

## 5. 验收（M1/M2）

- 清单评审通过；
- SOP 版本不兼容时拒绝并可恢复；
- 字段映射可回放（请求/响应样本）；
- 五个端点的字段名逐条对照实测响应，无推定。

## 附：v1.0 → v1.1 更正对照（**勿照抄左列**，仅作更正留痕）

> **本表不参与判据**：字段正确性判据只对「附录之前」的正文生效。理由：若把整份文件都纳入判据，判红会命中这张留痕表，构成判据自匹配（判据内容躺在被判据文件里）。

| v1.0（错，勿用） | v1.1（ICP 属主实测） |
|---|---|
| `nodes[].id / name / level` | `code / label / group / position / meaning` |
| `pools[].id / kind` | `code / name / layer / aliases` |
| `scenarios[].id / status` | `scenarioId / scenarioName` |
| `roles[].id` | `role / project / allowedActions / forbiddenActions` |
| `/health` 带 `version` | `/health` 无 `version`，版本在 `industry-model.version` |
| 建议新增 `icp_model_version` | 不需要新增，用 `industry-model.version` |

## 非声明

- 不声明已实现；不声明 F-012 可关闭。
