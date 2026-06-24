---
doc_id: GPCF-DOC-9B8C2D4F61
title: LOOP 能力注册表
project: WAES
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio, WAS]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_CAPABILITY_REGISTRY.md
source_path: 02-governance/loop/LOOP_CAPABILITY_REGISTRY.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# LOOP 能力注册表

本文件是 GlobalCloud LOOP 能力注册表，覆盖技能池、工具池、方法池的状态模型、风险分级、注册字段、核心能力族与子能力矩阵、能力族升级规则、快速准入、default_enabled、降级、停用、废弃、替代和 rework_required 边界。

## 注册字段

每项能力必须登记 capability_id、type、status、risk_level、version_scope、owner、allowed_contexts、forbidden_contexts、evidence_required、validator_or_gate、rollback_or_disable、last_reviewed。

## 状态模型

状态包括 fast_admitted、candidate、pilot、controlled、default_enabled、downgraded、disabled、deprecated、superseded。`pilot` 以上状态变化必须有 evidence，能力族必须绑定 validator 或 evidence。

## 核心技能

| capability_id | status | type | validator_or_gate |
| --- | --- | --- | --- |
| `skill.globalcloud-loop-orchestrator` | `controlled` | `skill` | `loop_document_gate.py` |
| `skill.globalcloud-document-governance` | `controlled` | `skill` | `document_control.py` |
| `skill.globalcloud-ui-quality-gate` | `pilot` | `skill` | `tool.validate_loop_ui_quality_baseline.py` |
| `skill.opsx-full-cycle` | `pilot` | `skill` | evidence required |
| `skill.globalcloud-harness-governance` | `controlled` | `skill` | Harness evidence |
| `skill.software-project-assessment` | `controlled` | `skill` | assessment evidence |
| `skill.globalcloud-collaborative-dev` | `controlled` | `skill` | `LOOP_MULTI_AGENT_EXECUTION_POLICY.md` |
| `skill.gstack` | `pilot` | `skill` | review / QA / security evidence |

## 核心工具

`loop_document_gate.py`、`check_document_pollution.py`、`validate_kds_token.py`、`check_chinese_localization_gate.py`、`validate_loop_engineering_master_plan.py`、`validate_loop_capability_registry.py`、`validate_loop_baseline_sync_readiness.py`、`validate_loop_engineering_five_direction_implementation.py`、`validate_loop_round_efficiency_audit.py`、`validate_continuous_round_substance.py`、`validate_l3_continuation_guard.py`、`git status`、`git diff`、`git diff --check`、`document_control.py`。

## 核心方法

六段式、任务包、evidence、no-write、test_data_lane、candidate_lane、real_business_lane、owner、WAES、Harness、三层评分、分层裁决、受控工程修改、按任务授权、CodeGraph、外部搜索/检索、RAG/语义索引、多智能体并行开发、Codex 内置 sub-agent、gstack 专家审计、OMX 候选 worker runtime、Agents SDK + Codex MCP 候选编排平台、Agent-Reach、Ontology、Headroom、WAS / Ontology-WAS、OKF/ODF、LCX、WAES-KDS RAG writeback、只读索引、依赖分析、调用图分析、公开资料核验、受控文档召回、分离文件分析、Superpowers LOOP execution discipline、method.superpowers.loop_execution_discipline。

## 候选方法能力

| capability_id | type | status | risk_level | owner | allowed_contexts | forbidden_contexts | validator_or_gate | rollback_or_disable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `method.superpowers.loop_execution_discipline` | `method/skill wrapper` | `candidate` | `medium` | `SOP + GPCF` | `planning,tdd,debugging,verification,review,independent_subtasks` | `auto_commit,auto_push,production_write,cross_repo_write,status_promotion,release,deployment` | `validate_superpowers_loop_admission.py + validate_loop_project_group_gate_readiness.py` | `disabled / repair_required` |

## 能力族

| capability_id | type | status | risk_level | evidence_required |
| --- | --- | --- | --- | --- |
| `family.codegraph` | core method family | controlled/pilot | medium/high by sub-capability | `validate_codegraph_*`; CodeGraph drift/watchlist evidence |
| `family.agent_reach` | method/tool family | candidate/pilot | medium/high by sub-capability | `validate_agent_reach_*`; Agent-Reach benchmark/review evidence |
| `family.ontology` | semantic governance method | controlled/pilot | medium/high by sub-capability | `validate_ontology_*`; Ontology contract evidence |
| `family.was_ontology_was` | semantic governance method | controlled/pilot | medium/high by sub-capability | `validate_was_*`; `validate_ontology_was_*`; source-record intake evidence |
| `family.headroom` | cost/runtime measurement method | candidate/pilot | medium/high by sub-capability | `validate_headroom_*`; Headroom dry-run/proxy/runtime evidence |
| `family.okf_odf` | governance method family | controlled with restrictions | medium/high by sub-capability | `validate_okf_*`; ODF gate evidence |
| `family.lcx` | governance method family | candidate/pilot | medium/high by sub-capability | `validate_headroom_lcx_*`; LCX authorization evidence |
| `family.waes_kds_rag_writeback` | gate/writeback method | candidate/pilot | medium/high by sub-capability | `validate_was_waes_kds_rag_writeback_gate_pack.py`; RAG index evidence; writeback evidence |
| `family.multi_agent_execution` | execution method family | controlled/pilot/candidate by sub-capability | medium/high by sub-capability | `LOOP_MULTI_AGENT_EXECUTION_POLICY.md`; agent output evidence; LOOP gates |

## 能力族升级规则

只读分析、索引、评估、候选生成可以进入 `controlled`。写回、同步、外部 API、跨仓执行、成本测量、自动修复必须保持 `pilot` 或 `candidate`，且必须有显式任务授权。

写入、自动化、跨仓和外部 API 子能力不得因能力登记获得生产权限。真实 KDS API 写入、WAES 写回、GFIS 运行层写入、生产 token、生产成本测量、外部 API 写入必须另行授权。

多智能体执行默认由 Codex 内置 `multi_agent_v1` 与 `globalcloud-collaborative-dev` 承担，状态为 `controlled`。`gstack` 仅作为专家审计组，状态为 `pilot`。OMX 与 OpenAI Agents SDK + Codex MCP 仅作为 `candidate`，未完成隔离 smoke、hook/adapter 审计、evidence adapter 和 validator 前，不得进入 L4/L5 或替代 LOOP 主控。

## 治理入口

`LOOP_CAPABILITY_REGISTRY.md` 管理技能、工具和方法的快速准入、风险分级、`pilot` 以上状态变化必须有 evidence、downgraded、disabled、deprecated、superseded，并由 `validate_loop_capability_registry.py` 与 `loop_document_gate.py` 检查。
