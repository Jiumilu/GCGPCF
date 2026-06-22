---
doc_id: GPCF-DOC-80B184DFCE
title: Agent-Reach Exa授权包 evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoC, XGD, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-exa-auth-pack-20260620.md
source_path: docs/harness/evidence/agent-reach-exa-auth-pack-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Agent-Reach Exa授权包 evidence

## Evidence ID

`AGENT-REACH-EXA-AUTH-PACK-20260620`

## 结论

Exa 授权包已准备，但仍处于 `authorization_required`。

当前没有安装 `mcporter`，没有修改 MCP 配置，没有注册 Exa MCP，没有执行 Exa 搜索，没有配置 Cookie，没有生产写入，没有 KDS canonical 写入，也没有状态升级。

## 当前事实

| 字段 | 值 |
|---|---|
| mcporter_cli_available | false |
| npm_package | `mcporter` |
| npm_visible_version | `0.12.0` |
| exa_mcp_endpoint_candidate | `https://mcp.exa.ai/mcp` |
| installation_performed | false |
| mcp_configuration_changed | false |
| exa_mcp_registered | false |
| exa_search_verified | false |
| status_upgrade_allowed | false |

## 授权要求

执行前必须明确：

- `authorized_mode=agent-reach-exa-local-pilot`
- `authorized_scope`
- `authorized_projects`
- `allow_network_download`
- `allow_npm_package_install`
- `allow_global_npm_install`
- `allow_project_dependency_change=false`
- `allow_mcp_configuration_change`
- `allow_exa_mcp_registration`
- `allow_cookie_or_login_state=false`
- `allow_production_write=false`
- `allow_kds_canonical_write=false`
- `rollback_required=true`
- `rollback_deadline_minutes`
- `acceptance_required=true`

## 受控产物

| 产物 | 路径 |
|---|---|
| 授权包 | `02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md` |
| Evidence JSON | `docs/harness/evidence/agent-reach-exa-auth-pack-20260620.json` |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-AUTH-PACK-001.md` |
| Validator | `tools/kds-sync/validate_agent_reach_exa_auth_pack.py` |

## 非声明

- 本 evidence 不证明 `mcporter` 已安装。
- 本 evidence 不证明 Exa MCP 已配置。
- 本 evidence 不证明 Agent-Reach `exa_search` 已可用。
- 本 evidence 不配置 Cookie 或登录态平台。
- 本 evidence 不写 KDS canonical Markdown。
- 本 evidence 不创建 GFIS source-of-record。
- 本 evidence 不升级 GPCF、GFIS、KDS、Brain、WAES、GPC、PKC、XiaoC 或 XGD 状态。
