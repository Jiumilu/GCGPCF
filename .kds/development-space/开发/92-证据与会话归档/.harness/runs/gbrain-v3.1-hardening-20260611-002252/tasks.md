---
doc_id: GPCF-DOC-65DA9DDC44
title: "Task Breakdown: GCBrain v3.1 Production Hardening"
project: WAES
related_projects: [PVAOS, WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-v3.1-hardening-20260611-002252/tasks.md
source_path: .harness/runs/gbrain-v3.1-hardening-20260611-002252/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Task Breakdown: GCBrain v3.1 Production Hardening

**Run ID**: gbrain-v3.1-hardening-20260611-002252

## Sprint 1: Security & Permission Hardening

| ID | Task | Status | Agent |
|---|---|---|---|
| T1.1 | 统一配置模块 (server/core/config.py) | done | — |
| T1.2 | Session + CSRF 认证 (server/core/auth.py) | done | — |
| T1.3 | API Key 作用域与哈希存储 | done | — |
| T1.4 | 6 步权限决策引擎 (server/governance/permissions.py) | done | — |
| T1.5 | SQL 层租户/敏感度过滤 | done | — |
| T1.6 | 请求上下文中间件 (server/routes/middleware.py) | done | — |
| T1.7 | Admin 登录/登出路由 (server/routes/admin.py) | done | — |
| T1.8 | API Key CRUD 路由 | done | — |
| T1.9 | 权限矩阵测试 (test_permissions.py, 22 tests) | done | — |
| T1.10 | 统一响应格式 {ok, data, error, meta} | done | — |

## Sprint 2: Data Consistency & Audit

| ID | Task | Status | Agent |
|---|---|---|---|
| T2.1 | schema_migrations 追踪表 | done | — |
| T2.2 | audit_events DB 主存储 + request_id/session_id | done | — |
| T2.3 | JSONL 追加归档 | done | — |
| T2.4 | Embedding 版本字段 (model/dimension/chunk_hash) | done | — |
| T2.5 | Evidence Ledger 表与服务 | done | — |
| T2.6 | 审计查询 API | done | — |
| T2.7 | 审计测试 (test_audit.py, 6 tests) | done | — |

## Sprint 3: Search & DQ Governance

| ID | Task | Status | Agent |
|---|---|---|---|
| T3.1 | 7 维 DQ 评分引擎 (server/governance/dq.py) | done | — |
| T3.2 | DQ 等级与问题清单 | done | — |
| T3.3 | 修复任务 SLA (owner/reviewer/due_at/sla_level) | done | — |
| T3.4 | 混合搜索评分解释 (keyword/semantic/authority/dq) | done | — |
| T3.5 | Golden Query Set 定义 | done | — |
| T3.6 | 内容脱敏 (server/governance/masking.py) | done | — |
| T3.7 | DQ 测试 (test_dq.py, 16 tests) | done | — |
| T3.8 | 搜索测试 (test_search.py, 16 tests) | done | — |

## Sprint 4: Agent Safety & Release Gates

| ID | Task | Status | Agent |
|---|---|---|---|
| T4.1 | 6 态 Agent 任务机 (server/agent/agent_tasks.py) | done | — |
| T4.2 | 4 层 Patch 审查 (server/agent/patch_review.py) | done | — |
| T4.3 | 冲突检测 (server/agent/conflict_detection.py) | done | — |
| T4.4 | Workspace 隔离 (server/agent/workspace.py) | done | — |
| T4.5 | Agent 契约 (agent/agent-contract.md) | done | — |
| T4.6 | Release Report 生成 | done | — |
| T4.7 | Agent 测试 (test_agent.py, 20 tests) | done | — |

## Sprint 5: Operations & Platform

| ID | Task | Status | Agent |
|---|---|---|---|
| T5.1 | /api/metrics 端点 | done | — |
| T5.2 | Readiness 分级 (ok/degraded/down) | done | — |
| T5.3 | 隧道监控脚本 | done | — |
| T5.4 | 备份脚本 (7日+4周+6月) | done | — |
| T5.5 | Restore Check 脚本 | done | — |
| T5.6 | 项目管理 (server/platform/project_registry.py) | done | — |
| T5.7 | 连接器契约 (server/platform/connectors.py) | done | — |
| T5.8 | 批量操作 API | done | — |
| T5.9 | 通知服务 | done | — |

## Frontend

| ID | Task | Status | Agent |
|---|---|---|---|
| F1 | 前台搜索模板 (server/templates/index.html) | done | — |
| F2 | Admin 壳 (admin/index.html + app.js + app.css) | done | — |
| F3 | Dashboard 模块 | done | — |
| F4 | DQ 模块 | done | — |
| F5 | Permissions 模块 | done | — |
| F6 | Audit 模块 | done | — |
| F7 | Agent 模块 | done | — |
| F8 | Operations 模块 | done | — |
| F9 | Platform 模块 | done | — |
| F10 | 可复用组件 (toast/modal/table/filters) | done | — |

## Summary

- Total tasks: 44
- Done: 44
- Remaining: 0
- Tests: 102+ (6 test files)
- Backend: ~4,767 lines Python
- Frontend: ~868 lines JS/CSS/HTML
