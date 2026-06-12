# Design Review: GCBrain v3.1 Production Hardening

**Run ID**: gbrain-v3.1-hardening-20260611-002252

## 架构决策

### 1. 服务层重构
v3.0 的 `services/` 平铺 20 个模块 → v3.1 按领域分层 6 层：

```
server/
├── core/         # config, db, auth, errors, logging
├── knowledge/    # search, render, embed, graph, vector_index
├── governance/   # permissions, tenants, masking, dq, repair_tasks, evidence, audit
├── operations/   # reports, batch_actions, notifications, trends
├── agent/        # agent_tasks, patch_review, conflict_detection, workspace
└── platform/     # project_registry, connectors
```

### 2. 认证升级路径
```
BasicAuth → Session + CSRF → API Key Scopes → Rate Limiting
```

### 3. 权限过滤器前置
```
query → tenant SQL filter → candidate retrieval → permission check → masking → ranking → response
```
不再先召回全量再内存过滤。

### 4. Agent 四层防线
```
Workspace Isolation → Patch Allowlist → Static Risk Scan → Human Review
```

### 5. 审计双写
```
audit_event → insert DB (primary) → append JSONL (archive)
```

## 风险矩阵

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| DB schema 不兼容 | High | Medium | 增量 ALTER TABLE + try/except |
| Session 认证影响现有 BasicAuth | Medium | Low | 双轨过渡，/admin 先上 |
| Agent 规则过严 | Medium | Low | 分 risk_level 分级 |
| 搜索评分解释性能开销 | Low | Medium | 评分计算内存完成，不增加 DB 查询 |

## 变更边界

- **允许修改**: gbrain-portal/ 下所有文件
- **只读引用**: 现有 DB schema (pages/content_chunks/links 等)
- **禁止修改**: 其他项目仓库、生产配置
- **必须人工确认**: DB migration 执行、git push

## 兼容性

- API 路径: /api/v1/* 新前缀，旧 /api/* 保持兼容
- 响应格式: 统一 {ok, data, error, meta}
- DB: 增量添加列和表，不删除 v3.0 结构
