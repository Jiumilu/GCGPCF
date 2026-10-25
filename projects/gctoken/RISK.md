---
doc_id: GPCF-DOC-GCTOKEN-RISK-20261025
title: GCToken 风险
project: GCToken
related_projects: [GCToken, GPCF, WAME]
domain: governance
status: draft
version: v0.1
owner: GCToken
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gctoken/RISK.md
source_path: projects/gctoken/RISK.md
sync_direction: bidirectional
last_reviewed: 2026-10-25
supersedes: []
superseded_by: []
---

# GCToken 风险

| 风险 | 等级 | 说明 | 缓解 |
|---|---|---|---|
| 项目群门禁未通过 | 高 | 当前文档门禁为 rework_required | 保持 partial，不合并为完成态 |
| 产品能力未实现 | 高 | 尚无真实模型调用、路由和计量证据 | 后续按 Feature 做最小真实切片 |
| 凭据与数据出境 | 高 | 多供应商接入可能扩大密钥和数据边界 | 使用既有密钥机制与 L0-L2 出境门禁 |
| 计量一致性 | 中 | 供应商、本地与缓存口径可能不一致 | 定义统一账单事件并做对账验证 |
| 分支保护待复核 | 中 | 新仓 main 暂未证明保护规则已生效 | 合并准入前配置 PR + 1 审核 + 必需检查 |

## 非声明

- 不声明风险已关闭；不声明项目状态提升。
