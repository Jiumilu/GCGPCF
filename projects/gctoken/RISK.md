---
doc_id: GPCF-DOC-GCTOKEN-RISK-20261025
title: GCToken 风险
project: GCToken
related_projects: [GCToken, GPCF]
domain: governance
status: draft
version: v1.0
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
| MVP 未实现 | 高 | Token MVP（T-A1~A6）尚未落地，只有 S0 验证原型 | 按 64 号文素材实施；验收七条判据 |
| 真实 provider 未联调 | 高 | 计量/成本/降级未经真实调用验证 | 真实 key 联调后复测；不提前声明生产可用 |
| 运维未定 | 中 | 监控/告警/容量/备份未设计 | P2 阶段补运维方案 |
| 依赖上游 | 中 | LiteLLM 升级/停更（MIT） | 锁版本 + 薄自研层隔离 |
| 成本失控 | 中 | 多 provider 费用无预算约束 | 四档 Key 预算 + 计量对账 |

## 非声明

- 不声明风险已关闭；不声明项目状态提升。
