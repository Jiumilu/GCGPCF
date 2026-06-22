---
doc_id: GPCF-DOC-BA68A130D5
title: GlobalCloud 绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图
project: KDS
related_projects: [GPC, PVAOS, WAES, KDS, Brain, XiaoC, XGD, Studio]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图.md
source_path: 03-data-ai-knowledge/GlobalCloud绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 绿色供应链体系企业级知识库主存层与LLM Wiki-Brain升级图

日期：2026-06-07
状态：专项架构图 v1
口径：只展开 KDS（企业级知识主存层）、`LLM Wiki`、`Brain`（知识引擎+服务层）、`WAES` 之间的分层与升级路径。

## 1. 知识底座升级图

```mermaid
flowchart TB
  subgraph SRC["知识来源"]
    DOC1["宪法 / 制度 / 体系设计"]
    DOC2["SOP / 项目方案 / 纪要 / 合同 / 验收 / 复盘"]
    DOC3["政策 / 合规 / 标准 / 监管资料"]
  end

  subgraph KMS["企业级知识主存层"]
    KDOC["KnowledgeDocument"]
    KVER["KnowledgeVersion"]
    KREL["KnowledgeRelease"]
    KPOL["KnowledgeAccessPolicy"]
    KAUDIT["KnowledgeAuditLog"]
  end

  subgraph MIG["编制与引擎层"]
    WIKI["LLM Wiki
规范编制 / 内容组织 / 历史沉淀"]
    GBRAIN["Brain
索引 / 向量 / 图谱 / RAG / 回指"]
    BRAIN["Brain
知识服务 / SOP / 案例 / 复盘"]
  end

  subgraph WAES["WAES 知识治理"]
    KIN["知识准入
canonical-only / source_refs / 分类校验"]
    KPUB["知识发布验证
版本 / 生效 / 退役 / 审计"]
    KAI["AI可见范围
项目隔离 / 密级 / Agent授权"]
    KSTOP["失效拦截
退役文档 / 失效引用 / 越权访问"]
  end

  subgraph AI["AI 消费层"]
    XIAOC["XiaoC"]
    HERMES["Hermes / XGD"]
  end

  DOC1 --> KDOC
  DOC2 --> KDOC
  DOC3 --> KDOC

  KDOC --> KVER --> KREL
  KPOL --> KDOC
  KAUDIT --> WAES

  KREL --> WIKI
  KREL --> GBRAIN
  WIKI --> BRAIN
  GBRAIN --> BRAIN

  KIN --> KREL
  KPUB --> KREL
  KAI --> BRAIN
  KSTOP --> WIKI
  KSTOP --> GBRAIN
  KSTOP --> BRAIN

  BRAIN --> XIAOC --> HERMES

  HERMES -. 禁止直接改正式知识版本 .-> KDOC
  GBRAIN -. 禁止直接改正式知识版本 .-> KDOC
  WIKI -. 测试期不作为唯一企业真源 .-> KDOC
```

## 2. 升级重点

### 2.1 企业级知识主存层必须补齐

1. 文档编号
2. 版本链
3. 发布审批
4. 权限与密级
5. 保留与归档
6. 审计日志

### 2.2 LLM Wiki 升级重点

1. 统一元数据
2. 版本绑定
3. 标准引用锚点
4. 发布态区分
5. 与主存层单向同步

### 2.3 Brain 升级重点

1. ingest 来源绑定
2. 切片回指
3. 项目与密级隔离
4. 失效知识清退
5. 查询与引用审计

## 3. 结论

测试结束后，`LLM Wiki` 与 `Brain` 可以在知识引擎层做唯一性选择；
企业级知识真源仍应稳定保留在知识主存层。
