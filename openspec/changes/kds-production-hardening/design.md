---
doc_id: GPCF-DOC-FFFA25C3EF
title: design
project: KDS
related_projects: [PVAOS, WAME, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/kds-production-hardening/design.md
source_path: openspec/changes/kds-production-hardening/design.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

## Architecture Overview（架构总览）

KDS v3.1 将 v3.0 平铺的 `services/` 目录重构为 6 个领域层：

```
server/
  core/         — 配置、数据库连接池、认证、错误、日志
  knowledge/    — 搜索、渲染、图谱、嵌入、向量索引
  governance/   — 权限、租户、脱敏、数据质量、修复任务、证据、审计
  operations/   — 报告、批量操作、通知、趋势
  agent/        — 智能体任务、补丁复核、冲突检测、工作区
  platform/     — 项目注册表、连接器
  routes/       — 10 个路由文件（运营、前台、管理端及智能体/审计/数据质量/运维/权限/平台管理）
```

## Key Design Decisions（关键设计决策）

### 1. 统一配置（单一事实源）
所有配置按 env vars > .env > defaults 的优先级合并。子目录不保留重复的 `config.py`。敏感值（session_secret、csrf_secret）若未提供，则用 `os.urandom(32)` 自动生成。

### 2. 会话 + CSRF 认证
- 使用 `itsdangerous.URLSafeTimedSerializer` 签发会话 Cookie
- CSRF 令牌经 HMAC-SHA256 与会话绑定
- Cookie 属性：HttpOnly、SameSite=Lax、Secure（生产环境）
- 接口密钥：SHA-256 哈希，分域（逗号分隔），含过期时间／最后使用时间／吊销标记

### 3. 权限决策引擎（固定不可变顺序）
六步固定顺序：显式拒绝 → 已过期 → 例外放行 → 租户放行 → 角色放行 → 敏感级放行。每次决策返回结构化输出（原因、命中规则、租户、角色、敏感级）。租户与敏感级过滤下沉至 SQL WHERE 子句，防止内存态检索后过滤。

### 4. 七维数据质量评分
加权平均：权威性 20%、时效性 20%、完整性 15%、元数据 15%、链接健康 10%、重复度 10%、安全性 10%。每个维度返回（得分、问题列表），便于行动化反馈。

### 5. 智能体四层防御
第 1 层：工作区隔离（`.harness/runs/<id>/workspaces/`）
第 2 层：补丁白名单（文件扩展名 + 路径规则）
第 3 层：静态风险扫描（SQL DROP、os.system、import os、权限变更）
第 4 层：人工复核（风险等级 ≥ 中 必须复核）

### 6. 审计架构
PostgreSQL `audit_events` 表 = 主事实源（可查询）。JSONL 文件 = 仅追加归档。写入先落数据库、后写 JSONL；查询只走数据库。每个事件携带 request_id、session_id、ip_hash、user_agent_hash、路由、方法、状态码、延迟毫秒数。

### 7. 接口版本化
所有路由挂载 `/api/v1/` 前缀。通过重定向层向后兼容 v3.0 路径。统一响应格式：`{ok, data, error, meta}`，含 request_id 与版本。

## Data Model Changes（数据模型变更）

新增表：schema_migrations、api_keys、evidence_ledger、notifications、projects（v3.1 模式迁移 `001_v3.1_schema.sql`）。

既有表新增列：所有核心表增加 created_at、updated_at、created_by、updated_by、deleted_at、version。content_chunks 表增加嵌入版本字段（embedding_model、embedding_dimension、chunking_strategy、chunk_hash、content_hash）。

## Frontend Architecture（前端架构）

管理端拆分为外壳（`index.html` + `app.js` + `app.css`），含 7 个页面模块（仪表盘、数据质量、权限、审计、智能体、运维、平台）与 4 个可复用组件（轻提示、弹窗、表格、过滤器）。公共模板（`server/templates/index.html`）展示统计与混合搜索界面，并显示得分解说。
