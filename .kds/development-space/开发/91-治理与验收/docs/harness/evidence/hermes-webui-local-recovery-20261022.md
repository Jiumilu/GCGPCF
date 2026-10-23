---
doc_id: GPCF-DOC-HERMES-WEBUI-LOCAL-RECOVERY-20261022
title: Hermes Web UI 本机恢复验证（2026-10-22）
project: GPCF
related_projects: [GPCF, Hermes]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/hermes-webui-local-recovery-20261022.md
source_path: docs/harness/evidence/hermes-webui-local-recovery-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# Hermes Web UI 本机恢复验证（2026-10-22）

> 授权：老卢 2026-10-22 06:49 问答批准「只启动本机 8648，健康检查通过后停下」。
> 范围：仅本机 127.0.0.1:8648；不改 Caddy/隧道、不动对外路由、不碰凭据；验证后停止进程。

## 1. 执行结果

| 项 | 结果 |
|---|---|
| 启动命令 | `hermes dashboard --port 8648 --host 127.0.0.1 --skip-build --no-open` |
| 启动日志 | `HERMES_DASHBOARD_READY port=8648` / `Hermes Web UI → http://127.0.0.1:8648` |
| 健康检查 | `GET http://127.0.0.1:8648/` → **HTTP 200** |
| 绑定 | 127.0.0.1（仅本机；无对外监听） |
| 停止 | 进程已停止；8648 端口关闭 |
| 对外路由 | **未修改**；公开 `hermes.csydsc.com` 仍为 502 |

## 2. 结论

- **本机 Web UI 可以恢复**：在当前 Hermes 安装下，`hermes dashboard` 可在 8648 正常启动并返回 200。
- 恢复动作只验证了本机；**对外 502 的根因（Caddy/SSH 隧道）未验证、未修改**。
- 访问控制未验证：本次绑定 loopback，未测试认证/OAuth 配置。

## 3. 回滚

- 已执行：`kill <dashboard pid>`；端口关闭。
- 若后续正式常驻，回滚为停止 dashboard 进程并恢复原 launchd 状态；不删除日志。

## 4. 非声明

- 不声明对外 Web UI 已恢复或可访问；
- 不声明访问控制/认证已验证；
- 不声明 F-029 试点准入通过或状态提升。
