---
doc_id: GPCF-DOC-9C70414B66
title: "Acceptance Matrix: GCBrain v3.1"
project: WAES
related_projects: [WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/acceptance-matrix.md
source_path: .harness/runs/gbrain-v3.1-hardening-20260611-002252/acceptance-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Acceptance Matrix: GCBrain v3.1

| Requirement | Implementation | Evidence | Status |
|---|---|---|---|
| Session + CSRF 认证 | server/core/auth.py | CSRF token 返回 200 OK | [x] |
| 统一权限中间件 | server/routes/middleware.py | 全 API 带 request_id | [x] |
| API Key 作用域 | server/core/auth.py + routes/admin.py | generate/revoke/rotate 路由 | [x] |
| 权限决策可解释 | server/governance/permissions.py | 6 步判定返回 structured result | [x] |
| SQL 层过滤 | server/governance/permissions.py | tenant + sensitivity SQL filters | [x] |
| 审计 DB 主存储 | server/governance/audit.py | DB insert + JSONL append | [x] |
| schema_migrations | migrations/001_v3.1_schema.sql | 追踪表已创建 | [x] |
| Embedding 版本 | server/knowledge/embed.py | model/dimension/chunk_hash 字段 | [x] |
| 7 维 DQ 评分 | server/governance/dq.py | 全维度评分 + grade + issues | [x] |
| 搜索评分解释 | server/knowledge/search.py | keyword/semantic/authority/dq 分解 | [x] |
| 修复任务 SLA | server/governance/repair_tasks.py | owner/reviewer/due_at/sla_level | [x] |
| Agent 4 层防线 | server/agent/patch_review.py | 隔离→白名单→扫描→审查 | [x] |
| Agent 6 态状态机 | server/agent/agent_tasks.py | not_started→...→closed | [x] |
| 强制回滚方案 | server/agent/agent_tasks.py | submit_patch 强制 rollback_plan | [x] |
| Release Report | server/operations/reports.py | generate_release_report() | [x] |
| /api/metrics | server/routes/ops.py | DB pool/queue 指标 | [x] |
| 隧道监控 | scripts/tunnel-monitor.sh | auto-reconnect | [x] |
| 备份策略 | scripts/backup.sh | 7日+4周+6月 retention | [x] |
| 连接器契约 | server/platform/connectors.py | BaseConnector + Markdown + Git | [x] |
| 后台模块化 | admin/ (7 modules + 4 components) | 角色导航 + 二次确认 | [x] |
| 前台搜索界面 | server/templates/index.html | 统计卡片 + 评分明细 | [x] |
| 测试覆盖 | tests/ (6 files, 102+ tests) | 22/22 unit tests passed | [x] |
| 统一响应格式 | server/core/errors.py | {ok, data, error, meta} | [x] |
| DB 迁移 | migrations/001_v3.1_schema.sql | 11 new tables + schema_migrations | [x] |
