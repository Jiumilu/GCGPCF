---
doc_id: GPCF-DOC-A412B97247
title: GPCF-AGENT-REACH-EXA-AUTH-PACK-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-AUTH-PACK-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-AUTH-PACK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-EXA-AUTH-PACK-001

## 输入

上一轮 `GPCF-AGENT-REACH-L2-ZERO-CONFIG-REPAIR-001` 已证明公开网页、GitHub API、RSS 零配置渠道 4/4 pass，但 `exa_search` 仍需要 `mcporter + Exa MCP` 授权。

## 动作

| # | 动作 | 说明 |
|---|---|---|
| 1 | 只读检查 mcporter | 当前 `mcporter_cli_available=false` |
| 2 | 只读检查 npm 包 | `mcporter` 可见版本 `0.12.0` |
| 3 | 新增 Exa 授权包 | 固化授权字段、执行候选、回滚方案、验收指标 |
| 4 | 新增 Exa evidence | 记录当前仍为 `authorization_required` |
| 5 | 新增 validator | 防止把授权包误报为已安装或可用 |

## 输出

| 产物 | 路径 |
|---|---|
| 授权包 | `02-governance/loop/LOOP_AGENT_REACH_EXA_AUTH_PACK.md` |
| Evidence Markdown | `docs/harness/evidence/agent-reach-exa-auth-pack-20260620.md` |
| Evidence JSON | `docs/harness/evidence/agent-reach-exa-auth-pack-20260620.json` |
| Validator | `tools/kds-sync/validate_agent_reach_exa_auth_pack.py` |

## 检查

| 检查项 | 当前结果 |
|---|---|
| mcporter_cli_available | false |
| npm_visible_version | `0.12.0` |
| installation_performed | false |
| mcp_configuration_changed | false |
| exa_mcp_registered | false |
| exa_search_verified | false |
| status_upgrade_allowed | false |

## 反馈

下一轮只有在用户明确授权字段后，才能执行 Exa local pilot：

```text
authorized_mode=agent-reach-exa-local-pilot
authorized_scope=local_tmp_or_user_tooling
allow_network_download=true
allow_npm_package_install=true
allow_global_npm_install=false
allow_project_dependency_change=false
allow_mcp_configuration_change=true
allow_exa_mcp_registration=true
allow_cookie_or_login_state=false
allow_production_write=false
allow_kds_canonical_write=false
rollback_required=true
acceptance_required=true
```

## 轮次真实性

| 字段 | 值 |
|---|---|
| declared_rounds | 1 |
| substantive_rounds | 1 |
| generated_items | 4 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_required |

## 非声明

- 本轮不安装 `mcporter`。
- 本轮不修改 MCP 配置。
- 本轮不注册 Exa MCP。
- 本轮不执行 Exa 搜索。
- 本轮不配置 Cookie 或登录态平台。
- 本轮不证明 Agent-Reach `exa_search` 已可用。
- 本轮不证明 GFIS runtime SOP E2E 已通过。
- 本轮不授权生产写入、真实外部 API 写入、KDS canonical 写入、数据库迁移、权限变更、部署、提交、推送或合并。
