---
doc_id: GPCF-DOC-69CFFD4C82
title: GlobalCloud 统一模型配置体系方案
project: KDS
related_projects: [KDS, GFIS, GPC, PVAOS, WAES, Brain, XiaoC, XGD]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud统一模型配置体系方案.md
source_path: 03-data-ai-knowledge/GlobalCloud统一模型配置体系方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 统一模型配置体系方案

日期：2026-06-08
状态：设计基线 v1
用途：为 GlobalCloud 绿色供应链体系建立统一的模型配置真源、引用方式、用户偏好边界和治理主线。

## 1. 目标

建立一套跨 `WAES / PVAOS / GPC / GFIS / Brain / XiaoC / Hermes / XGD` 统一适用的模型配置体系，解决以下问题：

1. 不同项目各自维护模型配置，导致配置分叉。
2. 模型供应商、模型名称、参数、权限、成本口径不一致。
3. 用户自定义模型、本地模型、云模型缺少统一纳管。
4. 模型切换、回退、审计、计量无法统一。

## 2. 总体原则

1. **全局只有一个模型配置真源。**
2. **项目只能引用模型，不再自定义模型真相。**
3. **用户可以选择，但只能在统一治理边界内选择。**
4. **本地模型、自定义模型、云模型必须统一纳管。**
5. **WAES 负责授权、审计、准入和策略，不负责业务事实。**
6. **XiaoC 负责模型编排与接入适配，不负责定义治理真源。**

## 3. 分层结构

统一模型配置体系分为五层：

### 3.1 全局模型目录层

定义系统里有哪些模型可被识别和治理。

### 3.2 全局模型策略层

定义哪些项目、角色、场景可以使用哪些模型档位。

### 3.3 项目模型引用层

定义每个项目、每类能力调用哪个模型档位，不定义底层模型真相。

### 3.4 用户模型偏好层

允许用户在白名单内切换模型、供应商、本地模型或自定义模型。

### 3.5 审计与计量层

记录使用、授权、成本、样本、驳回、越权、降级和统计数据。

## 4. 主责分工

### 4.1 WAES

负责：

1. 模型准入规则
2. 模型授权等级
3. 项目允许档位
4. 敏感场景限制
5. 审计与证据
6. 成本策略上限
7. 自定义模型接入审批

不负责：

1. 每个业务页面的模型参数实现
2. 业务事实生成
3. 用户本地模型运行本体

### 4.2 XiaoC

负责：

1. 模型接入适配层
2. Provider 协议抽象
3. 模型能力探测
4. 模型参数模板
5. Prompt 与模型组合编排

不负责：

1. 政策真源定义
2. 跨项目授权最终判定

### 4.3 Brain

负责：

1. 知识域对模型的知识消费输入约束
2. 知识检索上下文与引用回指

不负责：

1. 模型目录真源
2. 模型计量中心

### 4.4 Hermes / XGD

负责：

1. 会话侧模型调用入口
2. 用户交互层模型偏好呈现
3. 工具调用与运行侧回执

不负责：

1. 绕过 WAES 直接切生产模型
2. 直接写业务主账

## 5. 统一配置真源

建议建立唯一真源对象：

1. `ModelProvider`
2. `ModelCatalogEntry`
3. `ModelCapabilityProfile`
4. `ModelPolicy`
5. `ProjectModelBinding`
6. `UserModelPreference`
7. `CustomModelRegistration`
8. `ModelUsageRecord`
9. `ModelQuotaPolicy`
10. `ModelFallbackPolicy`

其中：

- 真源配置归 `WAES + XiaoC` 联合治理
- 运行引用归各项目消费
- 审计与计量归 WAES 汇总

## 6. 模型分类

统一按来源分类：

1. 平台云模型
2. 私有云模型
3. OpenAI Compatible 模型
4. 本地模型
5. 实验模型

统一按用途分类：

1. 文本生成
2. 工具调用
3. 多模态
4. Embedding
5. ASR
6. TTS
7. 治理分析
8. 知识检索辅助

## 7. 统一档位

建议统一档位：

1. `L0_DISABLED`
2. `L1_QUERY`
3. `L2_GENERAL`
4. `L3_REASONING`
5. `L4_GOVERNANCE`
6. `L5_LOCAL_EXPERIMENT`

所有项目优先绑定档位，不直接绑定具体模型名。

## 8. 关键约束

1. 不允许每个项目各自保存一套模型真源配置副本。
2. 不允许项目直接写死生产密钥。
3. 不允许用户自定义模型绕过授权策略。
4. 不允许本地模型成为治理盲区。
5. 不允许模型配置变更没有审计。

## 9. 当前建议状态

当前建议把这套体系作为 **AI 与数据层中的统一模型治理子域** 落地。

当前可以进入下一步：

1. 建立全局模型目录与能力标签标准
2. 建立项目模型引用与用户偏好模型
3. 建立模型授权、审计、计量与分期结算规划

当前不应直接进入：

1. 全量充值系统实现
2. 全量扣费系统实现
3. 各项目独立模型中心建设
