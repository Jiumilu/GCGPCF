---
doc_id: GPCF-DOC-B1187FF6E1
title: 任务清单 — KDS v3.1 生产加固
project: KDS
related_projects: [PVAOS, WAES, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/kds-production-hardening/tasks.md
source_path: openspec/changes/kds-production-hardening/tasks.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# 任务清单 — KDS v3.1 生产加固

## Sprint 1：安全与权限加固

- [x] 创建统一配置模块（`server/core/config.py`）—— 作为单一事实来源，避免重复
- [x] 使用 `itsdangerous` 实现会话认证（`server/core/auth.py`）
- [x] 实现 CSRF token 生成与校验
- [x] 实现带作用域的 API key，并使用 `SHA-256` 哈希存储
- [x] 创建统一权限上下文构建器（`identify_user -> build_permission_context`）
- [x] 构建 6 步权限判定引擎，并提供结构化可解释性（`server/governance/permissions.py`）
- [x] 将租户与敏感级别过滤下推到 SQL 层
- [x] 创建带 `request_id` 跟踪的请求上下文中间件
- [x] 实现带 cookie 管理的管理端登录 / 登出路由
- [x] 构建 API key 的 CRUD 路由（生成 / 撤销 / 轮换）
- [x] 创建权限矩阵测试（22 个测试）

## Sprint 2：数据一致性与审计加固

- [x] 在迁移 SQL 中创建 `schema_migrations` 跟踪表
- [x] 为所有核心表增加标准审计字段（`created_at/updated_at/created_by/updated_by/deleted_at/version`）
- [x] 将 `audit_events` 表重构为 DB 主记录表，包含 `request_id/session_id/ip_hash/ua_hash/route/method/status_code/latency_ms`
- [x] 实现以 DB 为主、`JSONL` 为归档的审计写入流程
- [x] 增加向量嵌入版本字段（`embedding_model/embedding_dimension/chunking_strategy/chunk_hash`）
- [x] 创建 evidence ledger 表与服务
- [x] 构建支持 `event_type/tenant/actor/request_id/q` 过滤的审计查询 API
- [x] 创建审计测试（6 个测试）

## Sprint 3：搜索质量与 DQ 治理升级

- [x] 构建 7 维 DQ 评分引擎（`server/governance/dq.py`）
- [x] 实现按维度打分并输出问题列表
- [x] 实现 DQ 等级计算（`A/B/C/D/F`）
- [x] 构建修复任务 SLA 跟踪（`owner/reviewer/due_at/sla_level`）
- [x] 实现带评分解释的混合搜索（`keyword_score/semantic_score/authority_boost/dq_penalty`）
- [x] 定义用于回归测试的 Golden Query Set
- [x] 按敏感级别构建内容脱敏能力
- [x] 创建 DQ 分析与分布 API
- [x] 构建修复任务生命周期 API
- [x] 创建 DQ 测试（16 个测试）

## Sprint 4：智能体安全与发布门禁

- [x] 构建 6 状态智能体任务机（`server/agent/agent_tasks.py`）
- [x] 实现 4 层补丁审查（隔离 -> allowlist -> 静态扫描 -> 人工复核）
- [x] 定义文件类型与路径风险映射
- [x] 实现静态风险扫描（SQL、shell、import、权限模式）
- [x] 要求中高风险补丁必须提供回滚方案
- [x] 构建冲突检测（`file/api/behavior/evidence/policy`）
- [x] 创建智能体工作区隔离
- [x] 构建智能体任务生命周期 API
- [x] 构建补丁审查 API
- [x] 编写智能体契约（`agent/agent-contract.md`）
- [x] 创建智能体安全测试（20 个测试）
- [x] 实现发布报告生成

## Sprint 5：运维与平台增强

- [x] 构建带 DB 连接池 / 队列指标的 `/api/metrics` 端点
- [x] 构建带 `ok/degraded/down` 状态的 readiness probe
- [x] 构建支持自动重连的 SSH 隧道监控脚本
- [x] 构建带保留策略的备份脚本（7 份日备、4 份周备、6 份月备）
- [x] 构建恢复检查脚本
- [x] 创建带策略模板的项目注册表
- [x] 定义连接器契约（`BaseConnector`、`MarkdownConnector`、`GitConnector`）
- [x] 构建批量操作 API（`archive/authority/deprecate/repair`）
- [x] 构建通知服务
- [x] 构建 DQ 趋势与陈旧内容检测
- [x] 生成 DQ 报告（`JSON + CSV`）

## 前端

- [x] 创建带统计和评分展示的公共搜索模板
- [x] 构建模块化管理端壳层（`index.html + app.js + app.css`）
- [x] 构建仪表盘模块（风险 / 工作 / 健康概览）
- [x] 构建 DQ 模块（分布、分析、修复任务）
- [x] 构建权限模块（租户列表、角色管理、权限测试器）
- [x] 构建审计模块（带过滤的事件日志）
- [x] 构建智能体模块（任务列表、补丁审查、安全检查器）
- [x] 构建运维模块（低 DQ、陈旧内容、批量操作、报告）
- [x] 构建平台模块（项目、连接器）
- [x] 构建可复用组件（toast、modal、table、filters）

## 文档与交付

- [x] 编写 `SECURITY.md`
- [x] 编写包含完整端点目录的 `API_REFERENCE.md`
- [x] 创建完整 schema migration（`migrations/001_v3.1_schema.sql`）
- [x] 编写 OpenSpec proposal、design 和 specs
- [x] 创建 `pyproject.toml` 与 `requirements.txt`

## 测试

- [x] `test_permissions.py` — 22 个测试（完整 6 步矩阵）
- [x] `test_dq.py` — 16 个测试（7 维评分）
- [x] `test_agent.py` — 20 个测试（安全审查 + 状态机）
- [x] `test_search.py` — 16 个测试（过滤、脱敏、golden queries）
- [x] `test_audit.py` — 6 个测试（事件类型、查询）
- [x] `test_api.py` — 22 个测试（响应格式、认证、配置、作用域）
