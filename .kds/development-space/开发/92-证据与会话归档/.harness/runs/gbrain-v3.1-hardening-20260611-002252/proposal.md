---
doc_id: GPCF-DOC-F7F2EF5A5D
title: "OpsX Proposal: GCBrain v3.1 Production Hardening"
project: WAES
related_projects: [WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/proposal.md
source_path: .harness/runs/gbrain-v3.1-hardening-20260611-002252/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# OpsX Proposal: GCBrain v3.1 Production Hardening

**Change ID**: gbrain-v3.1-hardening
**Run ID**: gbrain-v3.1-hardening-20260611-002252
**Status**: proposed
**Author**: Codex Agent (OpsX Full Cycle v2.1)

## 需求来源

《GCBrain 专业版 v3.0 全量开发文档》改进建议方案——将 v3.0 从"能力拼装型平台雏形"升级为"生产级知识治理平台"。

## 变更范围 (Scope)

### Sprint 1: 安全与权限硬化 (P0)
- Session + CSRF 认证替换 BasicAuth
- 统一权限中间件覆盖全部 API
- API Key 作用域 (search/read/admin/export/agent)、哈希存储、过期时间
- 权限决策可解释性
- 权限矩阵测试 30+

### Sprint 2: 数据一致性与审计硬化 (P0)
- audit_events 以 DB 为主事实源，JSONL 为追加归档
- schema_migrations 追踪表
- Embedding 版本管理
- request_id 全链路追踪

### Sprint 3: 搜索质量与 DQ 治理升级 (P1)
- 7 维 DQ 评分 + 等级 + 问题清单
- Golden Query Set 搜索质量回归
- 搜索评分可解释
- 修复任务 SLA (owner/reviewer/due_at/sla_level)

### Sprint 4: Agent 安全与发布门禁 (P0)
- 4 层防线：隔离→白名单→静态扫描→人工审查
- 6 态任务状态机，强制回滚方案
- Release Report 机制

### Sprint 5: 运维与平台化 (P1/P2)
- /api/metrics 端点
- 隧道监控 + 自动重连
- 备份保留策略 (7日+4周+6月)
- 连接器契约、项目策略模板、后台前端模块化

## 非变更范围 (Non-Goals)
- 不新增知识领域模块
- 不修改 Ollama/向量模型配置
- 不新增第三方集成

## 边界与风险

| 风险 | 级别 | 缓解措施 |
|------|------|----------|
| v3.0 DB schema 与新代码不兼容 | High | 增量 migration + 兼容查询 |
| Agent 安全规则过严影响开发效率 | Medium | 分风险等级，low 可自动通过 |
| 前端模块化影响现有用户体验 | Low | 渐进式替换，保持向后兼容 |

## 验收标准

1. 所有前端 API 权限感知
2. 审计事件可追溯至 request_id
3. 搜索结果含评分明细
4. Agent patch 必须有回滚方案
5. 权限矩阵测试覆盖 30+ 场景
6. Release Report 可用
7. DQ 任务有 owner/SLA
8. API 响应统一为 {ok, data, error, meta} 格式
