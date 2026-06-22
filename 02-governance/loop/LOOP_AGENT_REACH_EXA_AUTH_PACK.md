---
doc_id: GPCF-DOC-A882F89F6C
title: Loop Agent-Reach Exa授权包
project: WAES
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoC, XGD, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md
source_path: 02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Agent-Reach Exa授权包

## 1. 结论

本授权包用于 `GPCF-AGENT-REACH-EXA-AUTH-PACK-001`，目标是把 Agent-Reach 的 `exa_search` 从 `authorization_required` 推进到可执行试点前检查。

本轮只起草授权字段、安装范围、回滚步骤、验收指标和硬停止条件；不安装 `mcporter`，不修改 MCP 配置，不调用 Exa，不写 KDS canonical，不写生产系统，不升级任何项目状态。

## 2. 当前只读事实

| 字段 | 当前值 |
|---|---|
| mcporter_cli_available | false |
| npm_package | `mcporter` |
| npm_visible_version | `0.12.0` |
| exa_mcp_endpoint_candidate | `https://mcp.exa.ai/mcp` |
| installation_performed | false |
| mcp_configuration_changed | false |
| exa_search_verified | false |
| production_write | false |
| kds_canonical_write | false |
| status_upgrade_allowed | false |

## 3. 授权字段

真正执行前，用户必须明确给出以下字段。字段缺一不可。

```text
authorized_mode=agent-reach-exa-local-pilot
authorized_scope=local_tmp_or_user_tooling
authorized_projects=GPCF,KDS,Brain,PKC,XiaoC,XGD,WAES
allow_network_download=true/false
allow_npm_package_install=true/false
allow_global_npm_install=true/false
allow_project_dependency_change=false
allow_mcp_configuration_change=true/false
allow_exa_mcp_registration=true/false
allow_cookie_or_login_state=false
allow_production_write=false
allow_kds_canonical_write=false
rollback_required=true
rollback_deadline_minutes=30
acceptance_required=true
```

## 4. 执行方案候选

| 方案 | 命令候选 | 默认建议 | 原因 |
|---|---|---|---|
| A：临时 npm prefix | `npm install --prefix /tmp/agent-reach-mcporter mcporter` | 推荐 | 不污染项目依赖和全局 npm |
| B：用户级工具安装 | `npm install -g mcporter` | 需明确授权 | 会修改全局 npm 工具 |
| C：已有 mcporter 复用 | `mcporter config list` | 仅当已安装 | 本机当前不可用 |

推荐优先方案 A。只有当 A 无法满足 MCP 发现或 Agent-Reach doctor 时，才申请 B。

## 5. MCP 配置候选

如果用户授权 MCP 配置变更，候选命令为：

```bash
mcporter config add exa https://mcp.exa.ai/mcp
mcporter config list
agent-reach doctor --json
```

执行前必须记录原始配置：

```bash
mcporter config list > /tmp/agent-reach-exa-before.json
```

执行后必须记录新配置：

```bash
mcporter config list > /tmp/agent-reach-exa-after.json
```

## 6. 回滚方案

| 变更 | 回滚命令候选 | 验收 |
|---|---|---|
| 临时 npm prefix | `rm -rf /tmp/agent-reach-mcporter` | 目录不存在 |
| 全局 npm 安装 | `npm uninstall -g mcporter` | `command -v mcporter` 不存在或恢复到原路径 |
| Exa MCP 注册 | `mcporter config remove exa` 或恢复 before 配置 | `mcporter config list` 不含 exa |
| 临时 evidence | 保留，不删除 | evidence 记录已回滚 |

若 `mcporter config remove exa` 不可用，必须人工查看 `mcporter config list` 输出和工具文档，不得猜测配置文件路径后直接删除。

## 7. 验收指标

| 指标 | 目标 |
|---|---:|
| `mcporter_cli_available` | true |
| `exa_mcp_registered` | true |
| `agent_reach_exa_search_status` | ok |
| `exa_search_test_success_rate` | >= 0.8 |
| `source_provenance_rate` | 1.0 |
| `credential_leakage_count` | 0 |
| `cookie_or_login_state_count` | 0 |
| `production_write_count` | 0 |
| `kds_canonical_write_count` | 0 |
| `rollback_verified` | true |

## 8. 硬停止条件

以下任一条件触发时必须停止：

- 安装命令要求修改项目依赖。
- 工具要求 Cookie、登录态、Token 或账号授权。
- Exa MCP 返回需要密钥、付费账号或不可确认的授权条款。
- MCP 配置无法导出 before/after。
- 回滚命令不可确认。
- 任何命令尝试生产写入、真实外部平台写入或 KDS canonical 写入。
- 出现敏感信息输出。

## 9. 非声明

本文档不声明：

- `mcporter` 已安装。
- Exa MCP 已配置。
- Agent-Reach `exa_search` 已可用。
- Agent-Reach 已生产集成。
- KDS canonical Markdown 已写入。
- GFIS source-of-record 已创建。
- GPCF、GFIS、KDS、Brain、WAES、GPC、PKC、XiaoC 或 XGD 状态可升级。

## 10. 下一步

若用户明确授权，可进入 `GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001`。

若未授权，本任务停止于：

```text
status=authorization_required
stop_type=authorization_boundary
```
