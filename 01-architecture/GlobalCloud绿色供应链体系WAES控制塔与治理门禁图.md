# GlobalCloud 绿色供应链体系 WAES 控制塔与治理门禁图

日期：2026-06-07  
状态：专项架构图 v1  
口径：只展开 `WAES` 的控制塔、治理门禁、证据、状态、知识治理和 AI 授权边界。

## 1. WAES 控制塔与治理门禁图

```mermaid
flowchart TB
  subgraph SRC["事实与知识来源"]
    PVAOS["PVAOS
组织 / 项目 / 伙伴 / 门户"]
    GPC["GPC-Native
平台订单 / 运输 / POD / 外部异常"]
    GFIS["GFIS
工单 / 质量 / 库存 / 批次 / 发货事实"]
    EDGE["Edge
采集 / 缓存 / 补传 / 回执"]
    KMS["知识主存层
文档 / 版本 / 发布 / 权限"]
    KE["知识引擎层
LLM Wiki / GBrain / Brain"]
    AI["XiaoC / Hermes / XGD
Prompt / Agent / 运行结果"]
  end

  subgraph WAES["WAES 控制塔"]
    PROJ["项目与模板中心
项目发起 / 模板启用 / 配置编排"]
    RULE["规则与指标中心
规则 / 指标口径 / 状态门"]
    EVD["证据中心
EvidenceRecord / Verification / 引用审计"]
    STAT["状态中心
StatusTransition / StatusAudit / 阶段验收"]
    CONN["连接器治理中心
上线 / 下线 / 降级 / 恢复 / 发布验证"]
    KGOV["知识治理中心
知识准入 / 发布验证 / AI可见范围 / 失效拦截"]
    AIGOV["AI 授权中心
AgentToolGrant / 越权拦截 / 建议评价"]
    OBS["监控风险中心
Metric / Trace / Risk / Alert / Exception"]
  end

  subgraph HUMAN["人工治理与确认"]
    GOVAPP["GovernanceApproval
规则 / 指标 / 授权 / 状态升级"]
    HCONF["HumanConfirmation
治理确认 / 验收确认 / 知识发布确认"]
  end

  PVAOS --> PROJ
  GPC --> EVD
  GFIS --> EVD
  EDGE --> EVD
  KMS --> KGOV
  KE --> KGOV
  AI --> AIGOV

  GPC --> OBS
  GFIS --> OBS
  EDGE --> OBS
  KE --> OBS

  PROJ --> RULE
  RULE --> STAT
  EVD --> STAT
  CONN --> STAT
  KGOV --> STAT
  AIGOV --> STAT
  OBS --> STAT

  GOVAPP --> RULE
  GOVAPP --> CONN
  GOVAPP --> AIGOV
  GOVAPP --> STAT
  HCONF --> EVD
  HCONF --> KGOV
  HCONF --> STAT

  WAES -. 不审批工单 / 质量放行 / 库存调整 / 发货 / POD签收 .-> GPC
  WAES -. 不审批工单 / 质量放行 / 库存调整 / 发货 / POD签收 .-> GFIS
```

## 2. 门禁清单

1. 项目模板启用门  
2. 规则生效门  
3. 指标口径生效门  
4. 证据确证门  
5. 状态升级门  
6. SOP 发布与版本门  
7. 连接器上线/下线治理门  
8. 知识准入与知识发布门  
9. AI 授权与工具权限门  
10. 阶段验收结论门  

## 3. 边界说明

`WAES` 负责治理、证据、状态、知识准入、AI 授权和控制塔，不负责具体事务审批。  
工单、质量、库存、发货、签收、维修验收等事务动作，仍必须在 `GFIS` 或 `GPC-Native` 内部闭环。
