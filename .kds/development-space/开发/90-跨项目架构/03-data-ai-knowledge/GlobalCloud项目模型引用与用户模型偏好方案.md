---
doc_id: GPCF-DOC-09065C5D7F
title: GlobalCloud 项目模型引用与用户模型偏好方案
project: GPCF
related_projects: [GPCF, WAES]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/90-跨项目架构/03-data-ai-knowledge/GlobalCloud项目模型引用与用户模型偏好方案.md
source_path: 03-data-ai-knowledge/GlobalCloud项目模型引用与用户模型偏好方案.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud 项目模型引用与用户模型偏好方案

日期：2026-06-08
状态：设计基线 v1
用途：统一项目如何引用模型，以及用户如何在统一治理边界内选择模型。

## 1. 核心原则

1. 项目不拥有模型真源。
2. 项目只声明引用策略。
3. 用户可以选择，但不能突破治理边界。

## 2. 项目模型引用

每个项目只维护：

1. `ProjectModelBinding`
2. `ScenarioModelBinding`
3. `RoleModelBinding`
4. `FallbackModelBinding`

项目引用至少说明：

1. 场景名称
2. 允许档位
3. 默认档位
4. 是否允许用户覆盖
5. 是否允许本地模型
6. 是否允许自定义模型

## 3. 项目侧禁止事项

1. 不允许项目直接新建模型真源。
2. 不允许项目直接存生产密钥。
3. 不允许项目把模型配置写死在多个地方。
4. 不允许项目直接突破 WAES 的授权等级。

## 4. 用户模型偏好

用户偏好只允许配置：

1. 默认模型偏好
2. 默认供应商偏好
3. 是否优先本地模型
4. 是否允许降级
5. 是否允许实验模型

## 5. 用户侧可选择模型来源

### 5.1 全局白名单模型
优先来源，默认可选。

### 5.2 本地模型
允许选择，但必须来自已登记本地模型目录。

### 5.3 自定义模型
允许提议接入，但不等于立即可用。

## 6. 自定义模型接入流程

1. 用户提交模型建议
2. 进入候选区
3. 做协议兼容检查
4. 做安全检查
5. 做成本检查
6. 做能力标签评估
7. 做灰度试用
8. 决定是否进入白名单

## 7. 本地模型接入流程

1. 登记 endpoint
2. 探测能力
3. 绑定运行时
4. 记录资源等级
5. 绑定权限策略
6. 纳入计量与审计

## 8. 当前建议

V1 阶段只做：

1. 全局白名单选择
2. 本地模型受控选择
3. 自定义模型申请入口

不做：

1. 即时开放任意 endpoint
2. 无审批直连自定义模型
