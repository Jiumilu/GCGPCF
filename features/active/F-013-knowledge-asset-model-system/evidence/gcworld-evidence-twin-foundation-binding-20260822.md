---
doc_id: GPCF-F013-GCWORLD-BINDING-20260822
title: GCWORLD 证据数字孪生底座与 F-013 绑定证据
project: GPCF
related_projects: [KDS, WAS, XWAIL, WAES, KWE, MMC, GFIS, Brain, Studio]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-013-knowledge-asset-model-system/evidence/gcworld-evidence-twin-foundation-binding-20260822.md
source_path: features/active/F-013-knowledge-asset-model-system/evidence/gcworld-evidence-twin-foundation-binding-20260822.md
sync_direction: bidirectional
last_reviewed: 2026-08-22
supersedes: []
superseded_by: []
---

# GCWORLD 证据数字孪生底座与 F-013 绑定证据

## 绑定结论

OpenSpec 变更 `gcworld-evidence-twin-foundation` 作为 GKE-001 `release_0` 下的 GCWORLD 规划与只读评估工作包，绑定到 F-013 `knowledge-asset-model-system`。本次绑定只建立规划、规格和证据关系，不改变 F-013 的 `active / evaluate / not_complete` 状态，不解除既有阻塞，也不扩大 F-013 的范围上限。

用户于 2026-08-22 指示“下一步”，该人工确认仅授权继续执行当前 GPCF 仓库内的规划、门禁和只读证据工作；不构成 KDS 或 MMC 写入、跨仓代码修改、提交、推送、部署、验收、集成或状态提升授权。

## 受控对象

| 对象 | 值 |
| --- | --- |
| 项目群工程 | GKE-001 |
| 功能包 | F-013 |
| OpenSpec 变更 | `gcworld-evidence-twin-foundation` |
| OpsX 运行实例 | `20260822-235654-gcworld-evidence-twin-foundation` |
| 当前实施范围 | GPCF 本地规划与确定性只读验证 |
| 禁止范围 | KDS/MMC 写入、身份合并、关系回写、业务动作、跨仓代码、提交、推送、部署和状态提升 |

## 输入证据

| 输入 | 摘要值 |
| --- | --- |
| 变更提案 | `1ec6b87abb3c5208be3a326e8fb0530b517ff7de72e53fe51499f2a4735a9bfd` |
| 总体设计 | `6eb8ea884ccf6fbac17ed1ea7b9208915e1de659512afc0b5ffe11e3e3fa60ae` |
| 任务清单 | `be7a2e53163cf578f9a4d275ec0c8dfd676fa91138f6e02eea3a2f4d0225377f` |
| 《GCWORLD总体架构与实施方案_v1.0》 | `791a8d5100f96145ab2a9649a696f283209dd461aa6b208538c8b3ec250c1f83` |

## 当前门禁事实

| 门禁 | 当前结果 | 状态影响 |
| --- | --- | --- |
| OpenSpec 严格校验 | 通过 | 仅证明规格结构有效 |
| GPCF 文档门禁 | 通过；缺失元数据为零，缺失目录说明为零，无中文化债务 | 允许保留本地规划文档 |
| 项目群就绪度 | 17/17 通过；GFIS 状态上限仍为 `repair_required` | 不提升项目群状态 |
| F-013 模型门禁 | 通过；`not_complete`，各类真实写入与部署授权均为否 | 保持未完成 |
| F-013 工作区门禁 | 通过；`status_promotion_allowed=false` | 禁止状态提升 |
| KDS 读取准入 | 校验器执行通过，但实际准入为 `blocked_dirty_worktree`；KDS 有417项变更且本地领先4个提交 | 禁止进入KDS应用与写入 |
| CodeGraph 开发准入 | 通过 | 仅证明开发准入契约存在，本次未改变源码关系 |
| 基础构建 | MMC、KDS语法检查通过；Brain、PKC临时目录构建通过 | 不代表GCWORLD运行时已实现 |
| 本地服务 | MMC健康检查为200；KDS权威开发端口18080为200；8080路径为404 | 只记录本地观测，不执行服务变更 |

## 关系声明

本轮新增的唯一受控关系为：`GKE-001 → F-013 → gcworld-evidence-twin-foundation` 的规划与证据绑定。未修改 CodeGraph 源码节点或依赖边，未改变 KDS、WAS、WAES、XWAIL、MMC、Brain、Studio 或业务系统的权威职责。

## 未解决事项

- F-013 原有全部阻塞继续有效。
- KDS 工作树不满足读取评估应用准入，任务1.2至1.3不能据此自动视为完成。
- KDS只读来源清单、数据分级边界和身份归一人工责任人尚需独立确认。
- 本证据不构成 Harness 验收，不得用于声明已验收、已集成、生产就绪或全量覆盖。
