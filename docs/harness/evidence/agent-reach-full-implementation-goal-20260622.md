---
doc_id: GPCF-DOC-AGENT-REACH-FULL-GOAL-20260622
title: Agent-Reach Full Implementation Goal 2026-06-22
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-full-implementation-goal-20260622.md
source_path: docs/harness/evidence/agent-reach-full-implementation-goal-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Full Implementation Goal 2026-06-22

本轮执行 `GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001`，结论为 `full_implementation_prompt_ready`。

## 输入

| 项 | 值 |
| --- | --- |
| 原始目标 | 在项目群及 Loop 中实现 Agent-Reach 全量能力 |
| 上游仓库 | `https://github.com/Panniantong/Agent-Reach.git` |
| 已核验 HEAD | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| package version | `1.5.0` |
| 当前准入 | `limited_candidate_only` |

## 输出

| 产物 | 路径 |
| --- | --- |
| 全量实施方案与提示词 | `02-governance/GlobalCloud项目群Agent-Reach全量实施方案与执行提示词.md` |
| 结构化 evidence | `docs/harness/evidence/agent-reach-full-implementation-goal-20260622.json` |
| Loop round | `docs/harness/loops/loop-round-GPCF-AGENT-REACH-FULL-IMPLEMENTATION-GOAL-001.md` |
| validator | `tools/kds-sync/validate_agent_reach_full_implementation_goal.py` |

## 阶段目标

| phase | goal |
| --- | --- |
| P0 Source Lock | 上游源、license、安全和依赖锁定 |
| P1 Isolated Install | 临时 HOME / venv / npm prefix 安装与回滚 |
| P2 Channel Doctor | `agent-reach doctor --json` 通道健康矩阵 |
| P3 Fixed Query Benchmark | 固定查询搜索质量与效率基线 |
| P4 Candidate Ingestion | metadata-only 候选摄取 |
| P5 Project Group Routing | 14 项目/域 allow/deny matrix |
| P6 Authorized Read-Only Live | L3.5 授权真实只读验证 |
| P7 Human Review | WAES/KDS/owner 审查闭环 |
| P8 Controlled Production Admission | 单独生产准入包 |

## 非声明

- 不声明 Agent-Reach 已全量完成。
- 不声明 Agent-Reach 已生产集成。
- 不声明 live external search 已重新调用。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P0-SOURCE-LOCK-001`：锁定上游源、license、安全边界和依赖入口，并生成 `third_party/agent-reach/` 审查包。
