---
doc_id: GPCF-DOC-AGENT-REACH-CONTROLLED-ADAPTER-20260622
title: Agent-Reach 受控 Adapter Skeleton
project: GFIS
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GFIS
kds_space: 开发
kds_path: 开发/01-GFIS/third_party/agent-reach/CONTROLLED_ADAPTER.md
source_path: third_party/agent-reach/CONTROLLED_ADAPTER.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach 受控 Adapter Skeleton

本文件定义 `GPCF-AGENT-REACH-P2-CONTROLLED-ADAPTER-SKELETON-001` 的最小受控 adapter 边界。当前 skeleton 只做 dry-run、fixture 解析、命令白名单和阻断登记，不调用真实搜索。

## 输入边界

| 输入 | 状态 |
| --- | --- |
| 上游版本 | `agent-reach==1.5.0` |
| P1 安装结论 | `isolated_install_ready` |
| 本轮 fixture | `fixtures/agent-reach/controlled-adapter-dry-run.json` |
| 当前准入 | `limited_candidate_only` |

## 命令策略

| 类型 | 命令 | 处理 |
| --- | --- | --- |
| diagnostic | `agent-reach --help` | allow_dry_run |
| diagnostic | `agent-reach --version` | allow_dry_run |
| health_probe | `agent-reach doctor --json` | allow_with_probe_record |
| configuration | `agent-reach configure --from-browser chrome` | block |
| installer | `agent-reach install --channels opencli` | block |
| update | `agent-reach check-update` | block |
| watch | `agent-reach watch` | block |
| transcribe | `agent-reach transcribe <url-or-file>` | block |
| live_search | 任一真实搜索或读取动作 | block |

## 候选结果结构

每条候选结果必须包含：

- `candidate_id`
- `channel`
- `title`
- `source_url`
- `snippet`
- `evidence_tier`
- `admission_status`

当前只接受 `evidence_tier=fixture_only` 和 `admission_status=candidate_only`。

## 阻断规则

| 阻断 | 说明 |
| --- | --- |
| `credential_required_channel` | 需要 token、cookie、browser profile 或第三方账号时阻断 |
| `production_write` | 任何生产写入阻断 |
| `kds_canonical_write` | KDS canonical 写入阻断 |
| `gfis_source_of_record_write` | GFIS source-of-record 写入阻断 |
| `global_mcp_config_write` | 全局 MCP 配置写入阻断 |
| `live_external_search_without_authorization` | 未授权真实搜索阻断 |

## 非声明

- 不声明真实搜索已调用。
- 不声明搜索质量已验收。
- 不声明 KDS canonical、GFIS source-of-record、生产配置或全局 MCP 配置已写入。
- 不声明 accepted、integrated 或 production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P3-QUALITY-REPLAY-HARNESS-001`：建立离线 replay harness、固定查询集、评分字段和质量回归门禁，仍不调用真实搜索。
