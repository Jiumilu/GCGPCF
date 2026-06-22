---
doc_id: GPCF-DOC-A584BC19A5
title: KDS Phase 10 Backlog 分诊报告
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/kds-phase10-backlog-triage-20260619.md
source_path: docs/harness/evidence/kds-phase10-backlog-triage-20260619.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# KDS Phase 10 Backlog 分诊报告

generated_at: 2026-06-19T03:24:36.532001+00:00

## 范围

本报告对当前 KDS sync-plan backlog 进行分组，用于受控执行。它不是 KDS 写入操作，也不授权全局 blind sync。

## Sync Plan 快照

| metric | value |
| --- | --- |
| status | ready |
| remote_documents | 742 |
| create | 225 |
| update | 160 |
| skip | 98 |
| self_refresh | 2 |
| conflicts | 0 |
| missing_local | 0 |

## 按 Action 分类

| action | count |
| --- | --- |
| create | 225 |
| update | 160 |
| self_refresh | 2 |

## 按 Bucket 分类

| bucket | count |
| --- | --- |
| other_backlog | 39 |
| kds_knowledge_backlog | 39 |
| agent_team_backlog | 14 |
| loop_evidence_backlog | 228 |
| status_register_backlog | 9 |
| harness_evidence_backlog | 20 |
| closure_related_governance | 4 |
| architecture_backlog | 7 |
| generated_readme_surface | 22 |
| evidence_sample_backlog | 2 |
| self_refresh_control_surface | 3 |

## 按 Disposition 分类

| disposition | count |
| --- | --- |
| requires_manual_triage | 39 |
| requires_human_review | 39 |
| requires_owner_review | 14 |
| requires_batch_review | 228 |
| directed_sync_candidate | 13 |
| requires_evidence_batch_review | 22 |
| requires_architecture_batch_review | 7 |
| hold_until_self_refresh_stable | 22 |
| hold_self_refresh | 3 |

## No-Blind-Write 队列策略

- `directed_sync_candidate`：只能在 gates 通过后，通过明确的 `--source-path` 同步。
- `hold_self_refresh` 和 `hold_until_self_refresh_stable`：不要用重复写入追赶，必须先稳定生成过程。
- `requires_*_review`：在任何 KDS 写入前，先分成小批次并进行人工或 owner review。
- `requires_manual_triage`：分类完成前不写入。

## 样例队列项

| action | bucket | disposition | source_path |
| --- | --- | --- | --- |
| create | other_backlog | requires_manual_triage | .codex/skills/globalcloud-document-governance/SKILL.md |
| create | other_backlog | requires_manual_triage | .codex/skills/globalcloud-loop-orchestrator/SKILL.md |
| create | other_backlog | requires_manual_triage | .codex/skills/ui-ux-pro-max/SKILL.md |
| create | other_backlog | requires_manual_triage | 02-governance/loop/LOOP_GOVERNANCE_ROUND_REVIEW_PLAN.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率计算样表与字段字典.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud底座可用知识闭环率评分脚本dry-run规格.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选结构与发布门禁.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选评审实例包与人工填报示例.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页候选运行评审空白台账与发布前问题清单.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材Brain知识页评审样例到SOP候选写回规则.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材SOP候选写回规则到缺口悬赏与人工确认任务包.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材拓厂评估与知识源评测集.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材真实资料接收任务包与人工评测演练.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批空白执行台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材缺口悬赏与人工确认任务包首批虚拟填报演练.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材评测运行记录首批空白台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud湖北磷材首批知识对象运行空白台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud知识缺口悬赏与真实资料回收跟踪台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud积分收益额度悬赏争议联动规则.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud统一模型配置体系方案.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud绿色供应链体系全局初始化SOP方案.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud绿色供应链体系对象目录.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud绿色供应链分布式知识系统当前实施分析与下一阶段推进.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化DKS052填报包dry-run验收与人工确认队列视图.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手三件套首批dry-run评测运行记录.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测运行记录首批空白台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手内测问答与资料回收包联动规则.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化GFISAI助手首批问答与文档验收评测集.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化湖北磷材提交前审核清单与人工确认工作台.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化湖北磷材真实脱敏资料接收任务包与首批人工审核演练.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化湖北磷材试点样本表与MMC参数基线落地包.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化湖北磷材首批填报实例包与提交门禁.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化订单运行母版字段与单据映射专项清单.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化辽宁远航与金融凭证缺口专项台账.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化辽宁远航补证请求包与金融凭证脱敏索引空白填报包.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud葛化首批资料包入库验收与GFISAI助手试运行任务书.md |
| create | kds_knowledge_backlog | requires_human_review | 03-data-ai-knowledge/GlobalCloud首批资料回收包字段验收与候选SOP写回建议.md |
| create | agent_team_backlog | requires_owner_review | 05-agent-team/GlobalCloud智能体团队Loop Engineering全面改进方案.md |
| create | agent_team_backlog | requires_owner_review | 05-agent-team/GlobalCloud智能体团队侧边聊天10条主线-团队责任分配总表.md |
| create | agent_team_backlog | requires_owner_review | 05-agent-team/GlobalCloud智能体团队总体规划与行动计划.md |

## 边界

- No global blind KDS sync.
- No accepted/integrated status upgrade.
- No production system, database, or external business API writes.
- OKF remains a read-only navigation layer.
- KDS sync evidence must come from `.kds/sync-ledger.jsonl` with `result=http_200`.
