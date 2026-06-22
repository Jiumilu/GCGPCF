---
doc_id: GPCF-DOC-C7BD30A8E1
title: GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001
project: GPCF
related_projects: [GFIS, GPC, WAES, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001.md
source_path: docs/harness/loops/loop-round-GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001

## 输入

用户明确授权：

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

## 动作

| # | 动作 | 说明 |
|---|---|---|
| 1 | 写入授权文件 | `agent-reach-exa-local-pilot-authorization.json` |
| 2 | 临时安装 mcporter | `npm install --prefix /tmp/agent-reach-mcporter mcporter` |
| 3 | 临时 MCP 注册 | 在 `/tmp/agent-reach-exa-home/config/mcporter.json` 注册 Exa |
| 4 | Agent-Reach doctor | `exa_search=ok` |
| 5 | Exa 工具发现 | `web_search_exa`、`web_fetch_exa` |
| 6 | Exa 小规模搜索 | query 指向 Agent-Reach / AI agent search；首条结果为 Agent-Reach GitHub |
| 7 | 回滚 | 删除临时 prefix 与临时 HOME，并确认 `mcporter` 不在 PATH |

## 输出

| 产物 | 路径 |
|---|---|
| Authorization | `docs/harness/evidence/agent-reach-exa-local-pilot-authorization.json` |
| Evidence JSON | `docs/harness/evidence/agent-reach-exa-local-pilot-20260620.json` |
| Evidence Markdown | `docs/harness/evidence/agent-reach-exa-local-pilot-20260620.md` |
| Validator | `tools/kds-sync/validate_agent_reach_exa_local_pilot.py` |

## 检查

| 检查项 | 当前结果 |
|---|---|
| agent_reach_doctor_exa_status | ok |
| exa_schema_status | ok |
| exa_search_test_success_rate | 1.0 |
| rollback_verified | true |
| global_npm_install_performed | false |
| project_dependency_changed | false |
| cookie_or_login_state | false |
| production_write_count | 0 |
| kds_canonical_write_count | 0 |

## 反馈

本轮完成 Exa local pilot，但状态仍不得升级为生产集成。Exa 只可作为候选搜索能力进入后续质量 benchmark。

## 轮次真实性

| 字段 | 值 |
|---|---|
| declared_rounds | 1 |
| substantive_rounds | 1 |
| generated_items | 4 |
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
