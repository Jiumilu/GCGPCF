---
doc_id: GPCF-DOC-1212817FF5
title: GlobalCloud 模型授权审计计量与分期结算规划
project: GPCF
related_projects: [GPCF, PVAOS, WAES]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud模型授权审计计量与分期结算规划.md
source_path: 03-data-ai-knowledge/GlobalCloud模型授权审计计量与分期结算规划.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud 模型授权审计计量与分期结算规划

日期：2026-06-08
状态：设计基线 v1
用途：统一模型授权、审计、用量统计、计量、配额、分期结算与充值规划。

## 1. 总体原则

1. 先统一治理，再统一计量，最后再做充值与结算。
2. 模型成本统计不等于用户收费。
3. 本地模型也必须纳入计量，但计量方式可以不同于云模型。

## 2. WAES 授权治理

WAES 负责：

1. 场景授权等级
2. 项目允许档位
3. 用户允许模型范围
4. 高敏感模型限制
5. 自定义模型审批
6. 越权拦截记录

## 3. 审计对象

必须统一记录：

1. `ModelUsageRecord`
2. `ModelAuthorizationRecord`
3. `ModelFallbackRecord`
4. `ModelOverreachBlockedRecord`
5. `ModelProposalRecord`
6. `ModelQuotaConsumptionRecord`

## 4. 统一计量字段

至少包含：

1. 用户
2. 项目
3. 组织
4. 模型
5. provider
6. token 输入
7. token 输出
8. 请求次数
9. 工具调用次数
10. 音频时长
11. 图片生成次数
12. 推理耗时
13. 成本估算
14. 是否本地模型

## 5. 统计维度

### V2 必须支持

1. 用户维度
2. 项目维度
3. 组织维度
4. 模型维度
5. provider 维度
6. 时间维度

## 6. 配额与限额

建议支持：

1. 用户日限额
2. 用户月限额
3. 项目预算上限
4. 组织总预算上限
5. 高成本模型单独限制
6. 本地模型资源占用限制

## 7. 分期落地

### V1 统一治理版

做：

1. 模型目录
2. 项目引用
3. 用户偏好
4. 基础授权
5. 基础审计

不做：

1. 充值
2. 账户余额
3. 自动扣费

### V2 统一计量版

做：

1. 用量统计
2. 成本估算
3. 配额与限额
4. 告警
5. 看板

### V3 结算与充值版

做：

1. 账户体系
2. 充值记录
3. 配额包
4. 结算规则
5. 对账报表

## 8. 关键风险

1. 把统计和收费混在一期
2. 本地模型变成计量盲区
3. 用户自定义模型绕过授权
4. 项目缓存自己的模型副本

## 9. 当前建议

当前最适合纳入的交付版本是：

1. **V1：统一治理与统一配置**
2. **V2：统一计量与统计**
3. **V3：充值与结算**

因此，“用量、统计、充值”应现在进入规划，但不建议在第一阶段直接实施。
