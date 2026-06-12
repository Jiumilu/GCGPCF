# GCBrain v3.2 — 智能知识平台 设计方案

**版本**: v3.2  
**代号**: Intelligent Knowledge Platform  
**前置版本**: v3.1 Production Hardening (accepted)  
**设计日期**: 2026-06-11  

---

## 一、现状分析

### v3.1 已完成的能力

| 领域 | 能力 |
|---|---|
| 安全 | Session+CSRF 认证、API Key 作用域、权限决策可解释、SQL 层过滤 |
| 数据 | 审计 DB 主存储、schema_migrations、Embedding 版本管理、request_id 全链路 |
| 治理 | 7 维 DQ 评分、修复任务 SLA、权限矩阵、内容脱敏 |
| 搜索 | 混合搜索 + 评分解释、Golden Query Set、SQL 层权限过滤 |
| Agent | 4 层防线、6 态状态机、强制回滚方案、冲突检测 |
| 运维 | /api/metrics、隧道监控、备份保留策略、Release Report |
| 平台 | 项目注册、连接器契约、策略模板 |
| 前端 | 模块化后台（7 页面 + 4 组件）、前台搜索界面 |
| 测试 | 102+ 单元测试、22/22 验证通过 |

### v3.1 的局限性

v3.1 完成了"生产硬化"，但仍然是**被动知识治理平台**——它能管好已有知识，但缺乏：

1. **主动智能**：搜索只能"找得到"，不能"答得出"。用户需要逐篇阅读，无法直接获得答案
2. **知识推理**：页面之间只有简单链接，无法发现隐含关系、推断新知
3. **数据源局限**：仅支持 Markdown 目录，无法接入数据库、PDF、第三方平台
4. **协作缺失**：知识是静态页面，无法批注、评审、协同编辑
5. **生态封闭**：无插件机制、无 Webhook、无 SDK，第三方无法扩展
6. **部署复杂**：依赖 Mac mini + SSH tunnel，没有标准化部署方案

### 竞品对标

| 能力 | GCBrain v3.1 | Notion AI | Glean | Guru |
|---|---|---|---|---|
| 知识搜索 | ✓ 混合+评分 | ✓ | ✓✓ 企业级 | ✓ |
| RAG 问答 | ✗ | ✓ | ✓✓ | ✗ |
| 知识图谱 | 基础 D3 | ✗ | ✓ | ✗ |
| 多源连接 | ✗ | 有限 | ✓✓ 100+ | ✓ 有限 |
| 权限治理 | ✓✓ 6步引擎 | 基础 | ✓ | ✓ |
| 插件/扩展 | ✗ | ✓ API | ✗ | ✓ |
| 部署灵活 | 仅 Mac | SaaS | SaaS | SaaS |
| DQ 治理 | ✓✓ 7维 | ✗ | ✗ | ✗ |

**结论**: v3.1 在"权限治理"和"DQ 治理"上是独特的强项，但在"智能问答""多源连接""生态扩展"上存在明显短板。

---

## 二、v3.2 设计目标

### 核心定位

将 GCBrain 从"被动知识治理平台"升级为**"主动智能知识平台"**——

> 用户不只是搜索知识，而是直接向知识库提问，获得经过治理验证的答案。

### 三大主题

**主题一：知识智能 (Knowledge Intelligence)**
- RAG 问答引擎：基于知识库的 LLM 问答
- 知识图谱推理：关系发现、路径探索、知识补全
- 智能摘要：自动生成页面摘要、主题聚合
- 搜索增强：Query 改写、多轮对话搜索

**主题二：数据连接 (Data Connectivity)**
- 多源连接器：PDF 解析、数据库查询、REST API、Notion、Confluence
- 增量同步：变更检测、自动索引更新
- 连接器健康：同步状态监控、失败重试

**主题三：协作与生态 (Collaboration & Ecosystem)**
- 知识协作：页面批注、评审流程、变更建议
- 个性化门户：用户自定义仪表盘、收藏、订阅
- 插件系统：扩展点定义、插件注册、生命周期管理
- Webhook：事件驱动的外部集成
- 部署标准化：Docker Compose、环境向导、健康仪表盘

### 非目标 (Non-Goals)
- 不做实时协同编辑（那是 Notion/Google Docs 的领域）
- 不做通用 LLM Chat（只做基于知识库的 RAG）
- 不做工作流引擎（那是 OA/BPM 的领域）
- 不替换 Ollama（保持本地嵌入模型）

---

## 三、核心能力拆解

### 3.1 RAG 问答引擎

```
用户提问
  ↓
Query 理解（改写/扩展/意图识别）
  ↓
混合检索（keyword + semantic + graph）
  ↓
上下文组装（chunk 排序 + 去重 + 截断）
  ↓
LLM 生成（带引用 + 置信度）
  ↓
答案验证（事实核查 + DQ 加权）
  ↓
返回：答案 + 引用来源 + 置信度 + 相关页面
```

**关键设计**：
- 答案必须附带引用来源（页面 slug + chunk 位置）
- 置信度基于：检索相关度 × 来源 DQ × 来源权威等级
- 支持追问（多轮对话上下文）
- 答案可追溯：每次问答生成 audit event
- 流式输出（SSE）：逐 token 返回，改善体验

**API 设计**：
```
POST /api/v2/ask
{
  "question": "什么是碳核算？",
  "tenant_id": "gehua",
  "conversation_id": "conv_123",  // 可选，多轮对话
  "stream": true                   // 是否 SSE 流式
}
→ SSE: {type: "token", data: "碳"} {type: "token", data: "核"} ... {type: "done", sources: [...]}
```

### 3.2 知识图谱推理

**当前 v3.1**: 基础 D3 可视化，仅展示直接链接关系

**v3.2 增强**：
1. **关系类型识别**：从 frontmatter 和正文提取 `related_to`、`derived_from`、`conflicts_with`、`supersedes` 等语义关系
2. **路径发现**：两个页面之间的最短/最相关路径
3. **知识补全**：推荐可能相关但未链接的页面
4. **子图查询**：以某主题为中心的关联知识簇
5. **时序分析**：知识演化路径（版本更替、权威变化）

**API 设计**：
```
GET /api/v2/graph/path?from=page-a&to=page-b  → 最短关系路径
GET /api/v2/graph/cluster?slug=page-a&depth=3  → 知识簇（增强版）
GET /api/v2/graph/suggest?slug=page-a           → 推荐关联页面
```

### 3.3 多源连接器

在 v3.1 的 `connectors.py` 契约基础上，实现实际连接器：

| 连接器 | 数据源 | 同步模式 | 优先级 |
|---|---|---|---|
| Markdown（已有） | 本地目录 | 文件监听 | — |
| Git | Git 仓库 | Webhook / 定时 | P0 |
| PDF | PDF 文件 | 手动 / 目录扫描 | P0 |
| Database | PostgreSQL / MySQL | 定时查询 | P1 |
| REST API | 外部 API | 定时拉取 | P1 |
| Notion | Notion 页面 | API 轮询 | P1 |
| Confluence | Confluence 空间 | API 轮询 | P2 |

**连接器管理器**：
- 统一生命周期：注册 → 配置 → 测试连接 → 启动同步 → 监控
- 同步状态：`idle` / `syncing` / `error` / `disabled`
- 增量同步：基于 `updated_at` 或 `etag`/`hash` 的变更检测
- 失败重试：指数退避，最多 3 次

### 3.4 知识协作

| 能力 | 说明 |
|---|---|
| 页面批注 | 对知识页面段落添加评论，支持 @提及 |
| 变更建议 | 类似 PR 的变更提案 → 评审 → 合并流程 |
| 评审流程 | owner + reviewer 双重确认 |
| 订阅通知 | 关注页面/空间/主题，变更时通知 |
| 使用统计 | 页面访问量、搜索热词、DQ 趋势个人视图 |

### 3.5 插件系统

```
插件注册 → 声明扩展点 → 加载 → 生命周期管理
```

**扩展点定义**：
1. `search.filter` — 搜索结果过滤/重排
2. `render.pre` / `render.post` — 页面渲染前后处理
3. `dq.dimension` — 自定义 DQ 维度
4. `connector` — 自定义连接器
5. `auth.provider` — 自定义认证提供者
6. `audit.handler` — 审计事件处理器

**插件结构**：
```
plugins/my-plugin/
├── plugin.json       # 元数据 + 扩展点声明
├── __init__.py       # 入口
└── requirements.txt  # 依赖
```

### 3.6 部署标准化

| 组件 | 方案 |
|---|---|
| 应用 | Docker 镜像，多架构 (amd64/arm64) |
| 数据库 | PostgreSQL + pgvector Docker |
| 嵌入 | Ollama Docker 或远程 API |
| 编排 | Docker Compose 一键启动 |
| 反向代理 | Caddy 自动 HTTPS |
| 初始化向导 | Web UI：创建 admin → 配置 DB → 选择模型 → 创建 tenant → 导入知识 |

---

## 四、架构演进

```
server/
├── core/              # 基础设施 (v3.1)
│   └── plugins.py     # NEW: 插件管理器
├── knowledge/         # 知识核心
│   ├── search.py      # 增强: query 改写、多轮搜索
│   ├── ask.py         # NEW: RAG 问答引擎
│   ├── summarize.py   # NEW: 智能摘要
│   └── graph.py       # 增强: 路径发现、知识补全
├── governance/        # 治理 (v3.1 稳定)
├── operations/        # 运营
│   ├── stats.py       # NEW: 使用统计
│   └── subscriptions.py # NEW: 订阅管理
├── agent/             # Agent (v3.1 稳定)
├── platform/
│   ├── connectors/    # NEW: 连接器管理器
│   │   ├── manager.py
│   │   ├── pdf_connector.py
│   │   ├── database_connector.py
│   │   └── notion_connector.py
│   ├── plugins.py     # NEW: 插件系统
│   └── webhooks.py    # NEW: Webhook 管理
├── collaboration/     # NEW: 协作层
│   ├── comments.py    # 批注
│   ├── proposals.py   # 变更建议
│   └── reviews.py     # 评审
└── routes/
    ├── ask.py         # NEW: 问答路由
    ├── comments.py    # NEW: 协作路由
    └── webhooks.py    # NEW: Webhook 路由
```

---

## 五、数据库扩展

### 新表

```sql
-- 对话历史
conversations (id, user_id, tenant_id, title, created_at)

-- 问答记录
qa_records (id, conversation_id, question, answer, sources JSONB, 
            confidence FLOAT, tokens_used INT, model VARCHAR, created_at)

-- 批注
comments (id, page_id, user_id, content, selection_range JSONB, 
          parent_id INT, resolved BOOL, created_at)

-- 变更建议
change_proposals (id, page_id, proposer, title, description, 
                  patch TEXT, status, reviewer, created_at)

-- 订阅
subscriptions (id, user_id, resource_type, resource_id, events JSONB, created_at)

-- 插件注册
plugins (id, name, version, extension_points JSONB, enabled BOOL, 
         config JSONB, created_at)

-- Webhook 注册
webhooks (id, url, events JSONB, secret VARCHAR, enabled BOOL, 
          last_triggered_at, created_at)

-- 连接器实例
connector_instances (id, connector_type, config JSONB, project_id, 
                     sync_status, last_sync_at, created_at)

-- 使用统计
usage_stats (id, date DATE, metric VARCHAR, value FLOAT, 
             dimension VARCHAR, dimension_value VARCHAR)
```

---

## 六、API 扩展

### 新增 API

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/api/v2/ask` | RAG 问答（支持 SSE 流式） |
| GET | `/api/v2/ask/history` | 问答历史 |
| GET | `/api/v2/graph/path` | 知识图谱路径 |
| GET | `/api/v2/graph/cluster` | 知识簇（增强） |
| GET | `/api/v2/graph/suggest` | 推荐关联 |
| POST | `/api/v2/summarize` | 智能摘要 |
| GET | `/api/v2/comments` | 页面批注列表 |
| POST | `/api/v2/comments` | 添加批注 |
| POST | `/api/v2/proposals` | 创建变更建议 |
| POST | `/api/v2/proposals/{id}/review` | 评审变更 |
| GET | `/api/v2/subscriptions` | 我的订阅 |
| POST | `/api/v2/subscriptions` | 创建订阅 |
| POST | `/api/v2/connectors/{type}/sync` | 触发连接器同步 |
| GET | `/api/v2/connectors/status` | 连接器状态 |
| GET | `/api/v2/stats/usage` | 使用统计 |
| POST | `/api/v2/webhooks` | 注册 Webhook |
| GET | `/api/v2/plugins` | 插件列表 |
| POST | `/api/v2/plugins/install` | 安装插件 |

---

## 七、前端扩展

### 前台增强

- **问答界面**：搜索框升级为问答框，支持流式回答展示，答案附带引用来源卡片
- **知识图谱页**：交互式 D3 力导向图 + 路径高亮 + 节点展开
- **个性化首页**：最近访问、我的收藏、推荐阅读

### 后台新增模块

- **问答监控**：问答量、热门问题、未命中问题、模型用量
- **连接器管理**：连接器列表、同步状态、触发同步、错误日志
- **协作面板**：待审批注、变更建议队列、评审日历
- **插件市场**：已安装插件、可用插件、启用/禁用
- **Webhook 管理**：注册列表、触发历史、重试日志
- **统计仪表盘**：搜索趋势、页面访问排名、用户活跃度

---

## 八、实施路线

### Sprint 1: 智能问答 (P0)
- RAG 问答引擎（ask.py）
- Query 理解与改写
- 上下文组装与引用溯源
- SSE 流式输出
- 问答历史与审计
- 前台问答界面
- 后台问答监控

### Sprint 2: 知识图谱 + 摘要 (P1)
- 关系类型识别
- 路径发现与知识补全
- 智能摘要生成
- 交互式图谱前端

### Sprint 3: 多源连接器 (P0)
- 连接器管理器
- PDF 解析连接器
- Git 仓库连接器
- 连接器状态监控前端

### Sprint 4: 协作系统 (P1)
- 页面批注（comments）
- 变更建议流程（proposals）
- 订阅与通知增强
- 协作前端模块

### Sprint 5: 插件 + Webhook (P1)
- 插件系统框架
- 6 个扩展点实现
- Webhook 注册与触发
- 插件/Webhook 管理前端

### Sprint 6: 部署标准化 (P1)
- Docker Compose 编排
- 初始化向导 Web UI
- 部署文档
- 使用统计仪表盘

---

## 九、风险与缓解

| 风险 | 级别 | 缓解措施 |
|---|---|---|
| LLM 幻觉导致错误答案 | High | 强制引用来源 + 置信度 + DQ 加权 |
| PDF 解析质量差 | Medium | 多引擎备选 (PyMuPDF + unstructured) |
| 插件系统安全风险 | High | 沙箱隔离 + 权限声明 + 签名验证 |
| 多源同步性能 | Medium | 增量同步 + 连接池隔离 |
| 部署复杂度增加 | Low | Docker Compose 封装 + 向导简化 |

---

## 十、成功指标

| 指标 | 目标 |
|---|---|
| 问答准确率 (top-3) | > 85% |
| 问答平均响应时间 | < 3s (非流式) |
| 连接器类型 | 5+ (Markdown, Git, PDF, DB, REST API) |
| 插件扩展点 | 6 个 |
| 部署时间（新环境） | < 30 分钟 |
| 测试覆盖 | 200+ tests |
| 前端页面 | 前台 4 页 + 后台 13 模块 |

---

## 十一、与 v3.1 的差异总结

| 维度 | v3.1 | v3.2 |
|---|---|---|
| 定位 | 生产硬化 | 智能平台 |
| 搜索 | 关键词+语义 | +RAG 问答 |
| 知识图谱 | 基础可视化 | 推理+补全 |
| 数据源 | Markdown | +PDF+DB+API+Notion |
| 协作 | 无 | 批注+评审+订阅 |
| 扩展性 | 无 | 插件+Webhook |
| 部署 | 手动脚本 | Docker Compose |
| API 版本 | /api/v1 | +/api/v2 |
