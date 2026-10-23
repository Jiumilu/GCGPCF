---
doc_id: GPCF-DOC-RUNTIME-HOST-RUNBOOK-20261022
title: 项目群运行宿主 Runbook v1.0
project: GPCF
related_projects: [GPCF, Hermes, GCMEM, StartLux, SpaceAI, MMC, PMC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/runbooks/runtime-host-v1.0.md
source_path: docs/runbooks/runtime-host-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群运行宿主 Runbook v1.0

> 任务：PG-11（运行宿主与可观测）。性质：只读盘点 + 恢复路径说明；不启动、不停止、不修改任何服务。
> 非声明：不声明任何服务生产可用、不声明对外恢复、不声明安全边界已验证。

## 1. 当前实测（2026-10-22 06:45，`runtime_health_check.py`）

| 端点 | 归属 | 状态 | 证据 |
|---|---|---|---|
| `127.0.0.1:8642/health` | Hermes API | **UP** | HTTP 200；launchd `ai.hermes.gateway` |
| `127.0.0.1:8648/` | Hermes Web UI | **DOWN** | 端口未监听；公开 `hermes.csydsc.com` 502 |
| `127.0.0.1:19090/stats` | GCMEM API | **UP** | launchd `ai.globalcloud.gcmem-api` |
| `127.0.0.1:18090/health` | StartLux 本地 | **UP** | 决策模型本地端点 |
| `127.0.0.1:39010/healthz` | SpaceAI BFF | **UP** | status ok |
| `127.0.0.1:5273/` | SpaceAI 前端 | **UP** | Vite |
| `127.0.0.1:3000/` | PQC 前端 | **UP** | Next.js「绿色环保包装综合业务平台」（PJ-25 实测） |
| `127.0.0.1:3001/` | XiaoC MCP server | **UP（404）** | Express（PJ-25 实测） |
| `127.0.0.1:8000/` | MMC 控制面 | **UP** | uvicorn `mmc-control-plane`（非 Plane） |
| `127.0.0.1:8080/` | Python api_server | **UP（路径 404）** | 归属待核；`/api/mmc/v1/health` 不存在 |

结论：**核心 required 端点（Hermes API、GCMEM）在线；Hermes Web UI 8648 与对外 502 是当前唯一明确断点。**

## 2. Hermes Web UI 断点

- 已知事实（F-029 证据）：本机 8648 无监听；公开域名 502；8642 API 是独立服务；Caddy → SSH 隧道 → 8648 的链路未核验。
- **恢复前置**：
  1. 核实访问控制（谁能访问、是否需要认证/白名单）；
  2. 核实远端 Caddy 与 SSH 隧道配置；
  3. 本机 8648 起服务并健康检查；
  4. 再决定是否对外恢复（对外动作需单独授权）。
- 恢复命令（**未执行，需授权**）：以 Hermes 官方入口启动 Web UI，监听 127.0.0.1:8648；先本机验证，再评估隧道/对外。

## 3. 只读诊断命令

```bash
lsof -nP -iTCP:8642 -sTCP:LISTEN
lsof -nP -iTCP:8648 -sTCP:LISTEN
launchctl list | grep -iE "hermes|gcmem"
python3 tools/kds-sync/runtime_health_check.py --json
```

## 4. 恢复与回滚

| 动作 | 回滚 |
|---|---|
| 启动 Hermes Web UI（本机 8648） | 停止该进程；恢复原 launchd 状态；不删除日志 |
| 恢复对外路由 | 撤 Caddy 路由/隧道；恢复原 502 状态 |
| 启动 PMC 本地实例 | 停止实例；不写共享/生产实例 |

## 5. 缺口

- 无常驻统一运行宿主；证据仍停留在本机进程。
- `3000` / `8000` / `8080` 归属未核，不得当作 PMC/MMC 运行证据。
- 告警通道与值守替补仍未指定（F-029 blocker）。

## 6. 非声明

- 不声明 Hermes Web UI 已恢复、对外可用或访问控制已验证；
- 不声明任何项目生产就绪或客户验收；
- 不声明 3000/8000/8080 的服务归属。

## 7. 2026-10-22 本机恢复验证（已执行）

- 授权：老卢问答批准「只启动本机 8648，健康检查通过后停下」。
- 命令：`hermes dashboard --port 8648 --host 127.0.0.1 --skip-build --no-open`。
- 结果：`HERMES_DASHBOARD_READY port=8648`；`GET /` → HTTP 200；仅 loopback 监听；验证后已停止进程，8648 端口关闭。
- 未做：Caddy/SSH 隧道检查与修改、对外路由恢复、认证/访问控制验证。
- 证据：`docs/harness/evidence/hermes-webui-local-recovery-20261022.md`。
