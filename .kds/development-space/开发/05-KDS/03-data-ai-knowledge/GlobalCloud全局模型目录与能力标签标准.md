---
doc_id: GPCF-DOC-A3B30485E9
title: GlobalCloud 全局模型目录与能力标签标准
project: KDS
related_projects: [KDS, WAES, Studio]
domain: data-ai-knowledge
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/03-data-ai-knowledge/GlobalCloud全局模型目录与能力标签标准.md
source_path: 03-data-ai-knowledge/GlobalCloud全局模型目录与能力标签标准.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GlobalCloud 全局模型目录与能力标签标准

日期：2026-06-08
状态：设计基线 v1
用途：统一定义模型目录、能力标签、档位、参数基线和模型元数据结构。

## 1. 目标

为所有项目建立统一的模型描述语言，避免只记录“模型名”而无法治理。

## 2. 模型目录核心对象

每个模型至少要有以下字段：

1. `modelId`
2. `displayName`
3. `providerId`
4. `providerType`
5. `endpointType`
6. `modelTier`
7. `lifecycleStatus`
8. `isLocalModel`
9. `isCustomModel`
10. `isWhitelisted`

## 3. 能力标签

每个模型至少打以下标签：

1. `text_generation`
2. `tool_calling`
3. `multimodal_input`
4. `multimodal_output`
5. `embedding`
6. `asr`
7. `tts`
8. `reasoning_level`
9. `latency_level`
10. `cost_level`
11. `sensitivity_level`
12. `supports_streaming`
13. `supports_json_mode`
14. `supports_function_schema`
15. `supports_local_runtime`

## 4. 档位标准

### L0_DISABLED
禁用模型，不可被任何项目调用。

### L1_QUERY
低成本查询、轻任务、摘要、基础分类。

### L2_GENERAL
通用业务助手、普通 Agent 对话、基础知识问答。

### L3_REASONING
高质量推理、复杂方案、分析、复盘草案。

### L4_GOVERNANCE
治理分析、审计辅助、规则复核、证据摘要。

### L5_LOCAL_EXPERIMENT
本地模型、实验模型、灰度模型。

## 5. 参数基线

每个模型必须有统一参数基线：

1. `temperature_default`
2. `max_tokens_default`
3. `timeout_default`
4. `context_window`
5. `retry_policy`
6. `rate_limit_policy`
7. `fallback_model_ids`

## 6. 本地模型额外字段

本地模型必须额外记录：

1. `runtimeType`（Ollama / LM Studio / vLLM / custom）
2. `hostType`
3. `hostAddress`
4. `healthCheckPath`
5. `owner`
6. `resourceClass`
7. `gpuRequired`
8. `sensitiveDataAllowed`

## 7. 自定义模型额外字段

自定义模型必须额外记录：

1. `proposalSource`
2. `proposalOwner`
3. `approvalStatus`
4. `compatibilityStatus`
5. `securityReviewStatus`
6. `costReviewStatus`
7. `goLiveStatus`

## 8. 生命周期状态

统一状态：

1. `draft`
2. `candidate`
3. `approved`
4. `active`
5. `restricted`
6. `deprecated`
7. `retired`

## 9. 当前约束

1. 目录是全局真源，不允许项目复制后私改。
2. 档位比模型名更稳定，项目应优先绑定档位。
3. 标签必须支持 WAES 授权与审计。
