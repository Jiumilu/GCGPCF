---
doc_id: GPCF-DOC-4D7E1FF80C
title: GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-EXA-FIXED-BENCHMARK-001

## 输入

上一轮 `GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001` 已证明 Exa local pilot 可用并已回滚。本轮目标是验证固定查询集质量，不写 KDS canonical，不升级状态。

## 动作

| # | 动作 | 说明 |
|---|---|---|
| 1 | 临时安装 mcporter | `/tmp/agent-reach-mcporter` |
| 2 | 临时 MCP 注册 | `/tmp/agent-reach-exa-home` |
| 3 | 固定查询集 | 5 个公开查询，每个最多 3 个结果 |
| 4 | 记录指标 | 成功率、延迟、URL provenance、RAG Admission |
| 5 | 回滚 | 删除临时 prefix 和临时 HOME |

## 输出

| 产物 | 路径 |
|---|---|
| Evidence JSON | `docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.json` |
| Evidence Markdown | `docs/harness/evidence/agent-reach-exa-fixed-benchmark-20260620.md` |
| Validator | `tools/kds-sync/validate_agent_reach_exa_fixed_benchmark.py` |

## 检查

| 检查项 | 当前结果 |
|---|---|
| query_count | 5 |
| success_count | 5 |
| exa_search_test_success_rate | 1.0 |
| source_provenance_rate | 1.0 |
| rollback_verified | true |
| kds_canonical_write_count | 0 |
| status_upgrade_allowed | false |

## 反馈

Exa 可进入候选搜索能力 review，但不得直接生产集成。所有结果保持 `limited` 引用强度。

## 轮次真实性

| 字段 | 值 |
|---|---|
| declared_rounds | 1 |
| substantive_rounds | 1 |
| generated_items | 3 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 非声明

- 本轮不证明 Agent-Reach 已生产集成。
- 本轮不配置 Cookie 或登录态平台。
- 本轮不写 KDS canonical。
- 本轮不创建 GFIS source-of-record。
- 本轮不授权生产写入。
- 本轮不升级任何项目状态。
