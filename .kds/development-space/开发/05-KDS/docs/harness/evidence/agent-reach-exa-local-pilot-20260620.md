---
doc_id: GPCF-DOC-CADCE617E6
title: Agent-Reach Exa local pilot evidence
project: KDS
related_projects: [GFIS, GPC, WAES, KDS, Brain, PKC, XiaoC, XGD, GPCF]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/agent-reach-exa-local-pilot-20260620.md
source_path: docs/harness/evidence/agent-reach-exa-local-pilot-20260620.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Agent-Reach Exa local pilot evidence

## 结论

`GPCF-AGENT-REACH-EXA-LOCAL-PILOT-001` 结论为 `pass`，但只证明 Exa local pilot 在临时隔离范围内可用。

本轮使用 `/tmp/agent-reach-mcporter` 临时 npm prefix 和 `/tmp/agent-reach-exa-home` 临时 HOME。未执行全局 npm 安装，未修改项目依赖，未配置 Cookie，未写生产系统，未写 KDS canonical。执行后已删除临时 prefix 与临时 HOME，`mcporter` 没有留在 PATH。

## 授权

授权文件：

```text
docs/harness/evidence/agent-reach-exa-local-pilot-authorization.json
```

授权字段与本轮执行一致：

| 字段 | 值 |
|---|---|
| authorized_mode | agent-reach-exa-local-pilot |
| authorized_scope | local_tmp_or_user_tooling |
| allow_global_npm_install | false |
| allow_project_dependency_change | false |
| allow_cookie_or_login_state | false |
| allow_production_write | false |
| allow_kds_canonical_write | false |
| rollback_required | true |

## 验证结果

| 检查项 | 结果 |
|---|---|
| installation_performed | true |
| global_npm_install_performed | false |
| project_dependency_changed | false |
| mcp_configuration_changed | true |
| mcp_configuration_scope | temporary_home_only |
| exa_mcp_registered | true |
| agent_reach_doctor_exa_status | ok |
| agent_reach_doctor_exa_backend | Exa via mcporter |
| exa_schema_status | ok |
| exa_tools | web_search_exa, web_fetch_exa |
| exa_search_test_success_rate | 1.0 |
| exa_search_first_result_url | https://github.com/Panniantong/Agent-Reach |
| rollback_verified | true |

## 回滚结果

| 项 | 结果 |
|---|---|
| `/tmp/agent-reach-mcporter` | removed |
| `/tmp/agent-reach-exa-home` | removed |
| mcporter_still_available_after_rollback | false |

## 非声明

- 本 evidence 不证明 Agent-Reach 已生产集成。
- 本 evidence 不配置 Cookie 或登录态平台。
- 本 evidence 不写 KDS canonical Markdown。
- 本 evidence 不创建 GFIS source-of-record。
- 本 evidence 不授权生产写入。
- 本 evidence 不升级 GPCF、GFIS、KDS、Brain、WAES、GPC、PKC、XiaoC 或 XGD 状态。

## 下一步

下一轮可二选一：

| 路线 | 动作 | 边界 |
|---|---|---|
| 保守路线 | 保持 `candidate_search_only`，把 Exa 作为候选搜索能力 | 不进入 L3 |
| 扩展路线 | 新增固定查询集，验证 5 到 10 个 GlobalCloud 主题的搜索质量 | 仍不写 KDS canonical，不做状态升级 |
