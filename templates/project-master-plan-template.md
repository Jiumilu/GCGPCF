---
doc_id: PROJECT-DOC-MASTER-PLAN-TEMPLATE
title: {{PROJECT_DISPLAY_NAME}} 总体方案
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, GPCF, Studio]
domain: templates
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/templates/project-master-plan-template.md
source_path: templates/project-master-plan-template.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# {{PROJECT_DISPLAY_NAME}} 总体方案

## 1. 项目定位

说明本项目在 GlobalCloud WAS 项目群中的定位。

必须回答：

- 本项目是什么；
- 本项目服务哪些对象；
- 本项目在 WAS / Ontology / XWAIL / WAE / WAES / AaaS / SCaaS 链路中的位置；
- 本项目与业务事实源、治理入口、服务化运营之间的关系。

## 2. 与项目群主方案的继承关系

本方案继承：

```text
GPCF:01-architecture/WAS世界资产体系总体方案.md
```

必须声明：

- 本方案是本项目唯一当前有效总体方案；
- 主方案变化如何传导到本方案；
- 本方案变化如何回流到主方案或 Change Proposal；
- 未经用户确认的结构性变化只能登记为 `draft`、`candidate`、`partial`、`pending` 或 `repair_required`。

## 3. 项目群版本基线

| 对象 | 当前基线 |
|---|---|
| 项目群基线 | `GC-WAS-PG-BASELINE-0.1.0` |
| 本项目总体方案 | `v1.0` |
| 上游控制 | GPCF |
| 语义来源 | WAS / Ontology |
| 契约来源 | XWAIL |
| 治理入口 | WAES |

## 4. 本项目权威职责

列出本项目负责且可被其他项目依赖的职责。

## 5. 本项目不承担的职责

列出本项目不得越界承担的职责，避免与 WAS、XWAIL、WAES、AaaS、GFIS、GPC、PVAOS、KDS、Brain、Studio 等项目冲突。

## 6. 核心交付物

| 交付物 | 说明 | 状态 |
|---|---|---|
| 总体方案 | 本文件 | controlled |
| 运行/接口/证据交付物 | 待项目填写 | pending |

## 7. 与其他项目的接口关系

| 项目 | 接口关系 | 证据/契约 |
|---|---|---|
| GPCF | 主方案控制、台账、文档门禁、LOOP 门禁 | 主方案与台账 |
| WAS | 资产体系和治理边界 | WAS 主方案 |
| Ontology | 术语、概念关系和语义映射 | Ontology 映射 |
| XWAIL | 模型契约、Profile、状态机、证据约束 | XWAIL 契约 |
| WAES | 注册、授权、发布、治理入口 | WAES 门禁 |
| AaaS | 服务包、计量、SLA、商业运营 | ServicePackage |

## 8. 技术架构现状和目标架构

必须分别说明：

- 当前技术架构；
- 当前保留原因；
- 中长期目标架构；
- 迁移/收敛路线；
- 与项目群技术架构基线的偏差。

## 9. 测试、交付和运行命令

必须列出真实可执行命令。命令不存在时只能标记为 `implementation_pending`，不得声明测试或交付完成。

```bash
# TODO: 填写项目真实测试命令
```

## 10. LOOP 接入

```yaml
loop_enabled: true
loop_owner: GPCF
required_gates:
  - document_gate
  - version_gate
  - architecture_gate
  - contract_gate
  - test_gate
  - delivery_gate
  - evidence_gate
```

## 11. 风险、依赖、回滚和非声明边界

必须声明：

- 主要风险；
- 跨项目依赖；
- 回滚路径；
- 不声明生产可用；
- 不声明客户交付完成；
- 不声明 accepted、integrated 或 production_ready。
