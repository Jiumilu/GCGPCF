---
doc_id: GPCF-DOC-A2F5EC5E20
title: GCBrain 专业版 v3.0 全量开发文档
project: KDS
related_projects: [PVAOS, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/GCBrain-Development-Manual.md
source_path: docs/GCBrain-Development-Manual.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GCBrain 专业版 v3.0 全量开发文档

> **⚠️ 归属说明：** 本文档原为 GlobalCloud Brain 的设计，现已归属为 **KDS（Knowledge Data Source，唯一数据源）**。Brain 当前定位为基于 KDS 的全局知识中心（聚合/检索/图谱），不再承担数据存储职责。本文档中描述的架构、数据模型与索引机制为 KDS 的部署与运行参考。

## 一、系统架构

```
浏览器 (前台/后台)
    │
    ▼
FastAPI (server.main:app, port 19828)
    │
    ├── Middleware: BasicAuthMiddleware
    │       └── 保护 /admin /admin/
    │
    ├── routes/ (12 路由模块, 56 端点)
    │   ├── frontend.py     # 前台: /api/search, /api/render, /api/tree...
    │   ├── admin.py        # 后台: /admin/dashboard, /admin/keys...
    │   ├── admin_agent.py  # Agent: /admin/agent/tasks...
    │   ├── admin_audit.py  # 审计: /admin/audit/v3...
    │   ├── admin_dq.py     # DQ: /admin/dq/distribution...
    │   ├── admin_operations.py  # 运营: /admin/operations/batch...
    │   ├── admin_permissions.py # 权限: /admin/permissions/test
    │   ├── admin_platform.py    # 平台: /admin/platform/stats
    │   ├── search.py      # 搜索: /api/search/v2
    │   ├── graph.py       # 图谱: /api/graph
    │   └── ops.py         # 运维: /api/health, /api/ready, /api/version
    │
    ├── services/ (20 服务模块)
    │   ├── db.py          # 连接池 + fetch_all/fetch_one/execute
    │   ├── permissions.py # 六步权限决策引擎
    │   ├── tenants.py     # 租户/角色管理
    │   ├── masking.py     # 内容脱敏
    │   ├── search.py      # keyword/semantic/hybrid 搜索
    │   ├── highlight.py   # 高亮提取
    │   ├── dq.py          # DQ 四维评分
    │   ├── repair_tasks.py # 修复任务状态机
    │   ├── audit.py       # 审计日志 (15 事件类型)
    │   ├── evidence.py    # Evidence Ledger
    │   ├── health.py      # 健康检查
    │   ├── agent_tasks.py # Agent 任务管理
    │   ├── patch_review.py # Patch 安全审查
    │   ├── conflict_detection.py # 冲突检测
    │   ├── operations.py  # 批量操作/DQ趋势
    │   ├── reports.py     # 报告生成
    │   ├── project_registry.py # 项目注册表
    │   ├── embed.py       # 嵌入管理
    │   ├── vector_index.py # TurboVec sidecar
    │   └── config.py      # 环境配置
    │
    └── templates/
        └── index.html     # 前台 (14KB)
    admin/
        └── index.html     # 后台 (24KB)
```

## 二、目录结构

```
gbrain-portal/
├── server/
│   ├── main.py, config.py, auth.py
│   ├── routes/    (12 modules, 56 endpoints)
│   ├── services/  (20 modules)
│   └── templates/index.html
├── admin/index.html
├── agent/
│   ├── agent-contract.md
│   ├── agent-result.schema.yaml
│   ├── create-agent-workspace.sh
│   └── detect-conflicts.sh
├── scripts/
│   ├── backup.sh, restore-check.sh, migrate.sh
├── tests/        (9 test files, 42 tests)
├── migrations/
├── pyproject.toml
└── requirements.txt
```

## 三、API 全量参考

### 前台 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 前台首页 |
| GET | `/api/search?q=&space=&authority=&limit=` | 关键词搜索 |
| GET | `/api/search/v2?q=&tenant=&role=&mode=` | 权限感知混合搜索 |
| GET | `/api/render?slug=` | 页面渲染 (Markdown→HTML) |
| GET | `/api/tree?space=` | 知识空间文件树 |
| GET | `/api/stats` | 统计: pages/chunks/embedded |
| GET | `/api/backlinks?slug=` | 反向链接 |
| GET | `/api/graph?slug=&depth=` | 知识图谱 (D3) |

### 后台 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/dashboard/v2` | 仪表盘数据 |
| GET | `/admin/tenants` | 租户列表 |
| GET | `/admin/keys/masked` | Key 列表 (掩码) |
| POST | `/admin/keys/generate/v2` | 生成 Key |
| DELETE | `/admin/keys/{id}` | 吊销 Key |
| POST | `/admin/keys/{id}/rotate` | 轮换 Key |

### DQ API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/dq/distribution` | DQ 分布 (空间×权威) |
| GET | `/admin/dq/analyze` | 全量 DQ 分析 |
| GET | `/admin/dq/tasks` | 修复任务列表 |
| POST | `/admin/dq/tasks` | 创建修复任务 |
| POST | `/admin/dq/tasks/{id}/status` | 更新任务状态 |

### Agent API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/agent/tasks` | Agent 任务列表 |
| POST | `/admin/agent/tasks` | 创建 Agent 任务 |
| POST | `/admin/agent/tasks/{id}/start` | 启动任务 (→in_progress) |
| POST | `/admin/agent/tasks/{id}/submit` | 提交 Patch (→ready) |
| POST | `/admin/agent/tasks/{id}/accept` | 验收 (→accepted) |
| POST | `/admin/agent/tasks/{id}/reject` | 退回 (→in_progress) |
| POST | `/admin/agent/review-patch` | Patch 安全审查 |

### 运营 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/operations/low-dq` | 低 DQ 页面列表 |
| GET | `/admin/operations/stale` | 过期内容列表 |
| GET | `/admin/operations/dq-trend` | DQ 趋势 |
| GET | `/admin/operations/report/dq` | DQ 报告 JSON |
| GET | `/admin/operations/report/dq/csv` | DQ 报告 CSV |
| POST | `/admin/operations/batch/archive` | 批量归档 |
| POST | `/admin/operations/batch/authority` | 批量设权威级 |
| POST | `/admin/operations/batch/deprecate` | 批量废弃 |
| POST | `/admin/operations/batch/repair-tasks` | 批量创建修复任务 |

### 审计 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/audit/v3?event_type=&tenant=&q=&page=&fmt=` | 审计查询 |
| GET | `/admin/audit/types` | 事件类型列表 |
| POST | `/admin/audit/log` | 手动记录审计 |

### 权限 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/permissions/tenants` | 租户列表 |
| GET | `/admin/permissions/roles` | 角色列表 |
| GET | `/admin/permissions/test?tenant=&role=&sensitivity=` | 权限模拟 |

### 平台 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/platform/stats` | 平台统计 |
| GET | `/admin/platform/projects` | 项目列表 |
| POST | `/admin/platform/projects` | 添加项目 |
| GET | `/admin/platform/projects/{id}` | 项目详情 |

### 运维 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 进程存活检查 |
| GET | `/api/ready` | 就绪检查: DB/Ollama/Brain |
| GET | `/api/version` | 版本: v3.0, gbrain, commit |

## 四、服务层详解

### 权限引擎 (`services/permissions.py`)

```
判定顺序 (固化):
  explicit_deny → expired → exception_allow
  → tenant_allow → role_allow → sensitivity_allow

核心类:
  PermissionContext(tenant_id, user_id, role, max_sensitivity, is_expired, ...)
  PermissionResult(allowed, reason, detail)

核心函数:
  decide(ctx, page) → PermissionResult
  can_read_page(ctx, page_fm) → (bool, reason)
  filter_search_results(ctx, items) → filtered_items
```

### 搜索服务 (`services/search.py`)

```
搜索模式:
  keyword:  tsquery 全文检索
  semantic: gbrain query (pgvector)
  hybrid:   keyword + semantic → merge → permission filter

链路:
  query → keyword(tsquery) + semantic(pgvector)
  → dedup → permission filter → snippet → response
```

### DQ 服务 (`services/dq.py`)

```
评分维度:
  authority_score    (A0=100, D=10)
  freshness_score    (30天内=100, >180天=10)
  completeness_score (必填字段覆盖率)
  metadata_score     (rag_include/dq_score/last_verified_at/evidence)

修复状态机:
  open → assigned → fixing → ready_for_review → accepted → closed
  (complete 必须人工确认)
```

### Agent 服务 (`services/agent_tasks.py`)

```
任务状态机:
  not_started → in_progress → ready_for_human_acceptance → accepted → complete
                                   ↑ Agent 最高到此          ↑ 仅人工

Patch 安全审查 (patch_review.py):
  禁止: DROP/DELETE SQL, os.system, rm -rf
  允许: frontmatter 修改, markdown 正文修改
```

### 审计服务 (`services/audit.py`)

```
15 事件类型:
  page_view, page_search, permission_denied, permission_allowed,
  api_key_created, api_key_revoked, embedding_started, embedding_completed,
  dq_repair_created, dq_repair_accepted, admin_login, export_started,
  agent_task_created, agent_task_accepted, agent_task_rejected

存储: ~/.gbrain/audit/audit-events.jsonl
查询: tenant/event_type/actor 过滤 + 分页
```

## 五、数据库

### 主库: PostgreSQL + pgvector

```
核心表:
  pages            # 页面 (7,844)
  content_chunks   # 分块 (36,525)
  links            # 链接 (1,369)
  tenants          # 租户
  tenant_memberships # 租户成员
  page_acl         # 页面 ACL
  dq_scores        # DQ 评分
  repair_tasks     # 修复任务
  audit_events     # 审计事件
  embedding_jobs   # 嵌入任务
```

## 六、部署架构

```
Mac mini (192.168.31.60)
├── uvicorn :19828       (launchd 守护)
├── pgvector :5432       (Docker)
├── Ollama :11434        (Docker)
└── SSH tunnel → ECS :19828

ECS (121.40.144.57)
├── Caddy (SSL 终结)
│   ├── gbrain.csydsc.com → :19828
│   └── gbrain-admin.csydsc.com → :19828
└── 隧道: Mac mini → ECS

主 Mac
└── SSH tunnel: localhost:19828 → Mac mini:19828
```

### 启动命令

```bash
cd ~/gbrain-portal
ADMIN_USER=admin ADMIN_PASS=gcbrain2026 \
  python3 -m uvicorn server.main:app --host 0.0.0.0 --port 19828
```

### 健康检查

```bash
curl /api/health   # {"status":"ok"}
curl /api/ready    # {"status":"ok","checks":{"database":"ok",...}}
curl /api/version  # {"version":"3.0","gbrain":"0.42.33.0","commit":"6672df6"}
```

### 运维脚本

```bash
bash scripts/backup.sh         # PostgreSQL dump
bash scripts/restore-check.sh  # 备份验证
bash scripts/migrate.sh        # 迁移状态检查
```

## 七、测试

### 运行

```bash
pytest                    # 全部 42 tests
pytest tests/test_permissions.py  # 权限 (8 tests)
pytest tests/test_search.py      # 搜索 (4 tests)
pytest tests/test_agent.py       # Agent (7 tests)
pytest tests/test_operations.py  # 运营 (4 tests)
pytest tests/test_platform.py    # 平台 (4 tests)
ruff check server/               # Lint
```

### 测试覆盖

| 模块 | 测试数 | 覆盖场景 |
|------|--------|---------|
| API | 5 | health/stats/search/auth/dashboard |
| Permissions | 8 | S0/all deny/expired/exception/tenant/role/sensitivity |
| Search | 4 | keyword/highlight/permission_filter/no_ctx |
| DQ | 4 | authority/freshness/compute/repair |
| Audit | 4 | log/query/invalid/event_types |
| Agent | 7 | create/start/submit/accept/reject/review/conflict |
| Operations | 4 | low_dq/stale/trend/report |
| Platform | 4 | list/get/stats/add |
| Health | 2 | check_db/readiness |

## 八、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.x | 2026-06 | 单文件原型 (1854行) |
| v2.0 | 2026-06-10 | 模块化重构 (10模块, 5 tests) |
| v2.1 | 2026-06-10 | 治理内核 (17模块, 27 tests) |
| v2.2 | 2026-06-10 | Agent 辅助治理 (7模块, 7 tests) |
| v2.3 | 2026-06-10 | 运营控制台 (4模块, 4 tests) |
| v3.0 | 2026-06-10 | 平台化 (2模块, 4 tests) |

**当前: v3.0, 20 服务模块, 12 路由模块, 56 API 端点, 42 测试, ~3900 行 Python**
