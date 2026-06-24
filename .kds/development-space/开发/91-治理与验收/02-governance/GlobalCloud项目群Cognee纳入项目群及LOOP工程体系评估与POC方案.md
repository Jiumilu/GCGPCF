---
doc_id: GPCF-DOC-3A9B7F4E12
title: GlobalCloud 项目群 Cognee 纳入项目群及 LOOP 工程体系评估与 POC 方案
project: WAES
related_projects: [GPC, PVAOS, WAES, KDS, Brain, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md
source_path: 02-governance/GlobalCloud项目群Cognee纳入项目群及LOOP工程体系评估与POC方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 项目群 Cognee 纳入项目群及 LOOP 工程体系评估与 POC 方案

## 1. 评估结论

`cognee` 适合作为 GlobalCloud 项目群的“辅助长期记忆候选层”，不建议直接替代当前 Headroom LCX 与已建立的 Loop 主链能力。

结论：

- 采用**并行接入**（双栈对照）而非主链替换。
- 试点目标是验证：`记忆召回质量 / 可审计性 / 代价 / 治理合规`。
- 当前阶段保持 `accepted=false`、`integrated=false`、`production_ready=false`、`production_token_measurement=false`。

该结论与项目群当前治理边界一致：先有证据和授权，再谈生产自治。

## 2. 纳入对象与定位

### 2.1 角色定义

`cognee` 在本项目群中的建议定位：

- 长期上下文记忆（跨任务、跨会话）候选
- 语义检索/召回增强（尤其适合方案内回放）
- 失败经验复用候选（待 WAES 批准后写入）

不作为：

- 业务事实源（Source of Record）
- WAES 代替品
- KDS 或 Brain 的正式知识源替代
- 未授权生产写入入口

### 2.2 作用边界

- 接入阶段主路由：仍以现有 Headroom + KDS/Brain 为主。
- cognee 只作为旁路增强：`dual mode`
  - `headroom`：主输出
  - `cognee`：召回候选补充输出（非主裁决）
- 任何写操作需经过 marker 与批准，禁止自动写回业务文档或规则。

## 3. 价值评估

### 3.1 预期收益

1. 跨会话记忆连续性增强：减少“重复上下文重建”成本
2. 多项目经验复用：降低新问题重查的时间
3. 语义检索覆盖补齐：对 Headroom 在长时段上下文中的空白进行补充
4. 作为外部失败库候选：结合 Loop evidence 做失败归因与复盘输入

### 3.2 风险评估（高优先级）

- 语义漂移导致误召回、误导性建议
- 与 WAES 门禁边界不一致导致越权记忆写入
- 与现网 Headroom/Waes 检索链路冲突
- 运营成本与 token 变化不透明

### 3.3 风险缓解

- 召回结果只打 `candidate` 标记，不作为单一依据
- 引入 `marker_gated_recall`：无 marker 不可入主链
- 仅试点写 `non-business` 的脱敏 payload
- 指标化记录，并与现有 evidence schema 对齐

## 4. 兼容性对齐

### 4.1 与 LOOP 边界对齐

- 认定：gpcf-loop 的真实进展仍由 harness evidence、WAES 审核与 production-runtime 等级决定。
- 认定：cognee 的成功不等于业务完成。
- 认定：任何 production API write / external write / deploy / commit / push 仍需明示授权。

### 4.2 与 KDS / Brain / WAES 对齐

- KDS 仍是项目事实与知识源。
- Brain 仍为知识引擎与检索编排。
- WAES 保留最终门禁与策略裁决。
- cognee 不变更 AGENTS、CLAUDE、项目源文档。

## 5. 试点实施方案（2 周）

### 5.1 试点范围

- 项目群：`GPCF` 内局部范围
- 功能：`记忆 recall`（并行对照）与 `remember`（非关键中间态）
- 场景优先级：
  1) Loop 工具输出摘要召回
  2) 项目群状态总结复用
  3) 失败案例检索支持

### 5.2 架构（并行）

```text
Agent Runtime
 ├─ 主链：Headroom/现有 LCX Retrieval -> WAES -> 业务输出
 ├─ 并行链：Cognee Recall -> 证据标注 -> 候选补充
 └─ 两链统一输出到 Loop evidence，记录 source_tag 与 confidence
```

### 5.3 阶段计划

#### 阶段 P0：基础接入（2-3 天）

- 建立 `cognee` 隔离实例（tenant/project 分区）
- 完成 auth 与基础安全开关（auth、CORS、最小权限 DB）
- 禁用高风险查询路径

交付：

- `02-governance` 下 POC 接入说明与操作清单
- `loop/context/cognee/` 目录的最小配置样例（只读）

#### 阶段 P1：并行召回对照（3-5 天）

- 将已有 2-3 个高频任务的检索链加入并行候选
- 同时写入两类证据：`headroom_recall`、`cognee_recall`

交付：

- `docs/harness/evidence/cognee-poc-recall-comparison-*.json`
- 每次调度记录 `recall_hit / recall_miss / source_tag`

#### 阶段 P2：受控写入闭环（3-5 天）

- 开启 `remember preview`，仅允许非敏中间态入库
- 引入 `marker` 与 `owner_approval` 双门禁
- 形成回滚策略：超过阈值自动停写

交付：

- `loop/context/cognee/pilot_ddl.md`
- 试点审计日志与回滚记录

## 6. 指标与验收门禁

### 6.1 核心指标

- `recall_hit_rate`
- `recall_precision`
- `token_before`
- `token_after`
- `marker_coverage_rate`
- `unauthorized_write_block_rate`
- `manual_review_false_positive`

### 6.2 POC 通过条件（Go/No-Go）

通过条件：

- `recall_precision >= 0.85`
- `marker_coverage_rate >= 0.95`
- `unauthorized_write_block_rate == 1.0`
- 无高优先级安全/合规告警

未通过条件：

- 误召回导致错误决策
- 出现越权 write 或审计缺失
- 与主链一致性下降（关键路径 answer_equivalence 下降）

### 6.3 停机与回退

- 触发条件：`marker` 缺失、越权写入、误召回告警超过阈值、性能回退
- 回退动作：立即停用 `cognee` 并发输出；保留主链与 evidence 完整性

## 7. 成本与数据治理

| 字段 | 说明 |
|---|---|
| `cognee_input_tokens` | 单次 recall 请求输入 token |
| `cognee_output_tokens` | recall/response token |
| `cognee_recall_latency_ms` | p95 延迟 |
| `cognee_marker_hit_rate` | marker 通过率 |
| `cognee_store_ops` | remember 操作计数 |
| `cognee_cross_tenant_hit_count` | 越租户误召回计数 |
| `cognee_authorization_block_count` | 未授权阻断计数 |

说明：`cognee` 运营成本与 token 成本需与现有项目群成本模型并行记录，单独列为 `C_COGNEE` 分项，不与现有 Headroom 成本账本混淆。

## 8. 现阶段授权边界与限制

- 已确认不做的事（No-Go 项）：
  - 不替换 Headroom 主干
  - 不接管 source-of-truth 写入
  - 不处理真实客户敏感对象/合约原文
  - 不开启生产代理自动写入

- 要求保留的事（MUST）：
  - WAES marker 全量打点
  - Harness evidence 全量回放
  - 任何写入需 owner+WAES 双授权
  - 停止条件可回退并可复盘

## 9. 变更建议（下一个动作）

建议优先做清单：

1. 在 `02-governance` 下建立 1 页“COGNEE 接入白名单清单”
2. 先补齐 `LOOP_EXECUTION_RULES`/WAES marker 与现有日志 schema 的字段映射
3. 完成 P0 配置并给出是否进入 P1 的 `Go/No-Go` 审批材料
