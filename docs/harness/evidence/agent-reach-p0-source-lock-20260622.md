---
doc_id: GPCF-DOC-AGENT-REACH-P0-SOURCE-LOCK-20260622
title: Agent-Reach P0 Source Lock 2026-06-22
project: KDS
related_projects: [GFIS, GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-p0-source-lock-20260622.md
source_path: docs/harness/evidence/agent-reach-p0-source-lock-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach P0 Source Lock 2026-06-22

本轮执行 `GPCF-AGENT-REACH-P0-SOURCE-LOCK-001`，结论为 `source_lock_ready`。

## Source Lock

| item | value |
| --- | --- |
| repository | `https://github.com/Panniantong/Agent-Reach.git` |
| verified_head | `22d7f03a59401b5740b380c3ad43e3ff7a9dc373` |
| latest_commit_time | `2026-06-16T20:45:57+08:00` |
| package | `agent-reach` |
| version | `1.5.0` |
| python_requirement | `>=3.10` |
| license | `MIT` |
| source_file_count | `89` |

## 审查包

| artifact | purpose |
| --- | --- |
| `third_party/agent-reach/README.md` | 审查包说明 |
| `third_party/agent-reach/SOURCE.md` | 上游源和入口锁定 |
| `third_party/agent-reach/VERSION.lock` | 机器可读版本锁 |
| `third_party/agent-reach/OSS_REVIEW.md` | license 与依赖初评 |
| `third_party/agent-reach/SECURITY_REVIEW.md` | 凭据、写入面和安装风险初评 |
| `third_party/agent-reach/MODIFICATIONS.md` | 未修改上游源码登记 |

## 安全边界

| control | value |
| --- | --- |
| source_archive_copied | `false` |
| upstream_source_modified | `false` |
| package_installed | `false` |
| live_external_search_invoked | `false` |
| agent_reach_runtime_invoked | `false` |
| credential_written | `false` |
| kds_canonical_write_allowed | `false` |
| gfis_source_of_record_write_allowed | `false` |
| production_config_write_allowed | `false` |
| global_mcp_config_write_allowed | `false` |
| production_integration_allowed | `false` |

## 非声明

- 不声明 Agent-Reach 已安装。
- 不声明任一通道在本机可用。
- 不声明 live external search 已调用。
- 不声明 KDS canonical Markdown 已写入。
- 不声明 GFIS source-of-record 已创建。
- 不声明 accepted / integrated / production_ready。

## 下一轮

进入 `GPCF-AGENT-REACH-P1-ISOLATED-INSTALL-001`：使用临时 HOME、临时 Python venv 和临时 npm prefix 执行 dry-run / isolated install / doctor / uninstall dry-run / rollback 验证。
