---
doc_id: GPCF-DOC-9630ED7C78
title: proposal
project: KDS
related_projects: [PVAOS, WAME, KDS]
domain: openspec
status: draft
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/openspec/changes/kds-production-hardening/proposal.md
source_path: openspec/changes/kds-production-hardening/proposal.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

## Why（背景与动机）

KDS v3.0 是一个功能完整的知识治理平台原型（12 条路由、20 项服务、56 个接口、42 项测试），但在安全、数据一致性、审计可靠性、智能体安全与运维可恢复性方面缺少生产级加固。缺少这些能力，平台无法安全地服务多租户、无法通过安全审计、也无法作为商业产品交付。v3.1 的目标是补齐从「能力原型」到「生产加固平台」的差距。

## What Changes（变更内容）

### 安全加固（P0）
- 以会话认证＋CSRF 防护替换基础认证（BasicAuth）
- 统一权限中间件覆盖全部接口（前台＋管理端）
- 接口密钥分域（搜索／读取／管理／导出／智能体），哈希存储、支持过期与限流
- 权限决策可解释（每次决策输出：原因、命中规则、租户、角色、敏感级别）

### 数据一致性（P0）
- 以 audit_events 数据库表作为主事实源，JSONL 文件作为仅追加归档
- schema_migrations 迁移状态跟踪表（升／降／校验和／应用时间）
- 嵌入版本管理（模型、维度、分块策略、分块哈希）
- 所有核心表统一标准审计字段

### 搜索与数据质量治理（P1）
- 七维数据质量评分（权威性、时效性、完整性、元数据、链接健康、重复度、安全性）
- 黄金查询集（Golden Query Set）用于搜索质量回归测试
- 搜索得分可解释（分项拆解）
- 修复任务 SLA 跟踪（负责人、复核人、截止时间、SLA 级别）
- 权限过滤下沉至 SQL 查询层（而非检索后内存过滤）

### 智能体安全（P0）
- 四层防御：工作区隔离 → 补丁白名单 → 静态风险扫描 → 人工复核
- 六态智能体任务状态机，强制附带回滚方案
- **破坏性变更**：智能体不得再修改 auth.py、db.py、数据库迁移脚本或部署脚本

### 运维与平台（P1/P2）
- /api/metrics 指标端点、隧道监控与自动重连
- 备份保留策略（7 日 + 4 周 + 6 月 + 恢复演练）
- 连接器契约、项目策略模板、管理端前端模块化

## Capabilities（能力清单）

### 新增能力
- `session-auth`：会话 + CSRF 认证，管理端替换基础认证
- `api-key-scopes`：分域接口密钥，哈希存储、过期与限流
- `unified-permission-middleware`：权限中间件应用于全部接口路由
- `permission-explainability`：结构化权限决策输出
- `audit-db-primary`：数据库作为审计主事实源
- `schema-migrations`：迁移状态跟踪表
- `embedding-versioning`：嵌入模型／维度／分块哈希版本管理
- `dq-seven-dim`：七维数据质量评分（含等级与分项）
- `golden-query-set`：搜索质量回归测试数据集
- `search-score-explanation`：搜索得分分项拆解
- `repair-task-sla`：修复任务的 SLA、负责人与复核人
- `agent-safety-matrix`：智能体四层防御（文件类型／路径／风险白名单）
- `agent-six-state`：六态智能体任务状态机，强制回滚方案
- `release-gate`：自动发布报告
- `api-metrics`：运维指标端点
- `tunnel-monitor`：SSH 隧道健康监控与自动重连
- `connector-contract`：数据源连接器接口契约
- `admin-frontend-modules`：带角色导航的模块化管理面板

### 变更的能力
无 —— v3.0 没有既有 OpenSpec 规格；所有能力均为净新增。

## Impact（影响面）

- **代码**：6 层 30+ 服务模块、10 个路由文件、模块化管理端前端（11 个 JS/CSS/HTML 文件）
- **接口**：所有端点纳入统一权限中间件；新增 /api/v1/admin/* 路由；新增 /api/metrics
- **数据库**：schema_migrations 表、既有表新增列、audit_events 结构调整
- **依赖**：会话／CSRF 需要 python-jose、passlib、itsdangerous
- **部署**：隧道监控新增 launchd 配置，更新备份脚本
- **测试**：从 42 项增至 102+ 项，覆盖权限矩阵、搜索质量、智能体安全与端到端
