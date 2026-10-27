---
doc_id: GPCF-DOC-PJ25-PMC-PLANE-VERIFICATION-20261022
title: PJ-25 PMC Plane UI/幂等验证（只读优先）2026-10-22
project: GPCF
related_projects: [GPCF, Project]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pj25-pmc-plane-verification-20261022.md
source_path: docs/harness/evidence/pj25-pmc-plane-verification-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PJ-25 PMC Plane UI/幂等验证（只读优先）2026-10-22

- 执行时间：2026-10-22 07:23–07:26（+08:00）
- 执行人：status-writer-a（证验执行智能体）
- 执行边界：只读探针 + 只读 MCP；**未启动/未停止任何服务**；未写任何 Plane 实例；未创建/输出任何凭据明文；未改仓库文件；未 commit/push。
- 结论先行：**生产 Plane UI/API 只读可达；F-028 隔离实例已停机；本地无可用 Plane UI；重复同步幂等（created=0）本轮无法重跑，仍为 B 级文档证据。**

## 1. 现状（引用既有记录）

| 来源 | 事实 |
|---|---|
| `projects/project/STATUS.md` | F-028 已关闭、`overall_status=partial`；本机 Plane API 同步队列 28 个 Feature（27 创建、1 更新）；重复同步 F-028 更新同一工作项、GPCF 源文件哈希不变；**Plane 用户界面未验证**；本机验证实例已停机，临时容器卷与凭据已清理 |
| `features/done/F-028-plane-gpcf-feature-evidence-integration/evidence/harness-handoff.json` | `plane_instance=isolated_local_api_127.0.0.1:18081_verified_then_stopped; ephemeral_volumes_and_credentials_removed; user_interface_not_verified`；授权=本机开发环境与本机凭据（2026-10-18）；共享/生产写入未确认 |
| `.../evidence/live-plane-api.json` | `environment=isolated local Plane API at 127.0.0.1:18081`；`first_sync=F-028: created`、`second_sync=F-028: updated`；`gpcf_source_unchanged=true`；`project_id=efbc9f78-55ad-46c9-8bf2-c659c1305679` |
| `.../evidence/live-plane-full-sync.json` | 28 Feature / 12 项目；`created=27`、`updated=1`；`plane_projection_ids_match_gpcf=true` |
| `.../journal.md`「本机 Plane API 实证」 | 隔离实例端口 `127.0.0.1:18081`；验证后仅停止 `gcp-plane-dev` 容器并移除临时卷、本地环境文件与 API 密钥文件；未留可复跑命令 |

## 2. 探针命令与结果（全部只读）

### 2.1 本机候选端口逐一定性（不能凭端口号认定 PMC）

| 目标 | 命令 | 结果 | 定性 |
|---|---|---|---|
| `127.0.0.1:8000` | `curl -sS -D- http://127.0.0.1:8000/` | HTTP 200；`server: uvicorn`；body `{"ok":true,"data":{"service":"mmc-control-plane","phase":"phase2","version":"0.1.0",...}}` | **MMC 控制面，不是 Plane** |
| `127.0.0.1:3000` | `curl -sS -D- http://127.0.0.1:3000/` + `lsof -p <pid>` | HTTP 200；`X-Powered-By: Next.js`；`<title>绿色环保包装综合业务平台</title>`；进程 cwd=`GlobalCloud PQC/frontend` | **PQC 前端，不是 Plane** |
| `127.0.0.1:3001` | `curl -sS http://127.0.0.1:3001/` + `lsof -p <pid>` | HTTP 404；`X-Powered-By: Express`；进程 cwd=`GlobalCloud XiaoC/packages/mcp-server` | **XiaoC MCP server，不是 Plane admin** |
| `127.0.0.1:18081`（F-028 实例端口） | `curl --max-time 4 http://127.0.0.1:18081/`；`lsof -nP -iTCP:18081 -sTCP:LISTEN` | `curl: (7) Failed to connect`，http_code=000；无监听 | **F-028 隔离实例已停机（与 STATUS 一致）** |
| `127.0.0.1:18000` / `:3004` | `lsof -nP -iTCP:18000 / :3004 -sTCP:LISTEN` | 均无监听 | Plane 本地 web/space 端口未运行 |
| `https://pmc.csydsc.com/` | `curl -sS -D- https://pmc.csydsc.com/` | HTTP 200（1.35s）；`server: Caddy`；`<title>GlobalCloud PMC（项目管理中心）</title>` | **Plane Web UI（共享/生产实例）** |
| `https://pmc.csydsc.com/api/instances/` | 只读 GET | HTTP 200；返回 Plane 实例配置 JSON（`is_workspace_creation_disabled`、`admin_base_url`、`app_base_url`、`is_feishu_enabled` 等） | **Plane API 可用（共享/生产实例）** |
| `[::1]:8000` | `curl -g -6 http://[::1]:8000/api/instances/` | connection reset | 8000 为双绑：IPv4 命中 MMC 控制面，IPv6 不可用 |
| 本机 PMC docker 栈 | `docker ps -a --filter name=globalcloudproject`；`docker logs --tail 15 globalcloudproject-api-1`；容器内 `GET http://172.22.0.5:8000/api/instances/` | api 容器 `Up 53 minutes`，日志持续 `Waiting for database migrations to complete...`；容器内 `/`、`/api/instances/`、`/api/health/` 均 404；worker/beat/minio 均 `Exited (137)`；无 web 容器；compose 配置=`GlobalCloud PMC/docker-compose-local.yml` | **本地 Plane 后端未就绪且无 UI；非本任务启动** |

### 2.2 生产实例只读身份与 API 可用性（MCP 只读）

| 调用 | 结果 |
|---|---|
| `pmc_health` | `ok:true`；`site_reachable:true`；`api_key_valid:true`（`users/me 200`）；`readonly_endpoint:true`（OAuth2 Bearer 可用） |
| `pmc_whoami` | `mode=readonly-oauth2`；`environment=prod`；`scope=pmc.work_items.read`；`projects=[a9fd689a-2ce2-4487-ad79-bc5909a05cd0]` |
| `pmc_readonly_work_items(limit=3)` | `ok:true`；`totalCount=280`；返回 GC-329 / GC-331 / GC-333（DSH 会话投影）及 `nextCursor` |

> 注：`pmc_whoami` 的 OAuth2 只读 scope 指向项目 `a9fd689a-…`，与 F-028 证据中的 `project_id=efbc9f78-…` 不同；不能据此证明 F-028 的 28 项投影存在于生产实例。

### 2.3 未启动新本地实例的理由（说明为何未做）

- PMC 仓 `README.md` 的本地开发路径为 `pnpm install && ./setup.sh && pnpm dev`，Web 默认 3000、管理界面 3001；本机 3000 已被 PQC 前端占用、3001 已被 XiaoC MCP 占用，且 `setup.sh` 会写入仓内配置，超出本任务「不改任何仓库文件」约束。
- F-028 journal 仅记录结果（隔离实例 18081 验证后停机），未留可复跑命令；本任务不自行重建未登记实例。
- 现存 `globalcloudproject-*` 栈启动时间早于本任务、启动者未登记，不接管、不写入。

## 3. 能否验证（本轮判定）

| 验证项 | 判定 | 依据 |
|---|---|---|
| Plane **UI 可用性**（本地） | **不能** | 本地无 Plane web：compose-local 无 web 服务；18000/3004 无监听；3000 为 PQC 前端 |
| Plane **UI 可达性**（生产只读） | **能（仅只读可达）** | HTTP 200 + Plane 标题；但为共享/生产实例，不写、不创建凭据、无 F-028 投影归因 |
| Plane **API 可用性** | **部分能** | 生产 `/api/instances/` 200 + MCP 只读通道 ok；本地 API 全路径 404（迁移未完成） |
| **重复同步幂等（created=0）** | **不能（本轮无可复现 A 级证据）** | 无可写实例：F-028 实例已停机且卷/凭据清理；本地栈未就绪；生产写入未授权 |
| F-028 投影与 GPCF 一致 | **沿用 F-028 文档证据（B 级）** | `live-plane-full-sync.json`：`created=27/updated=1`、投影 ID 一致；本轮未重跑 |

### 3.1 幂等结论

- 现有可引用证据：F-028 单条二次同步为 `updated`（同一 `work_item_id`）；全量首次同步 `created=27/updated=1`。
- **没有**「重复一次全量同步 → `created=0`」的运行记录；本轮也无法补采。
- 因此幂等仍为 **B 级文档声明**，不升级为已验证。

## 4. 阻塞（可执行口径）

1. F-028 隔离实例 `127.0.0.1:18081` 已停机，临时卷与凭据已清理 → 不可复跑。
2. 本地 `globalcloudproject-*` 栈不可用：api 卡在 `Waiting for database migrations to complete...`、worker/beat/minio 退出、无 web 容器；启动者未登记。
3. 端口冲突：3000=PQC 前端、3001=XiaoC MCP、8000=MMC 控制面；PMC README 的本地开发默认端口不可用，且 `setup.sh` 会写仓内配置。
4. 生产实例 `pmc.csydsc.com` 为共享/生产：写入、凭据创建/使用扩大均未授权；OAuth2 只读 scope 项目 ≠ F-028 项目，无法定位 F-028 投影。
5. 要得到 `created=0` 需：①人工授权启动隔离本地 Plane 实例（含迁移与 admin 初始化）；②人工授权创建本机开发凭据；③用 `../GlobalCloud PMC/globalcloud/gpcf_sync.py` 连续跑两次全量同步并回读 `created=0`；④验证后停止并清理临时卷/凭据。①与②属高危险操作，需人工授权。

## 5. 非声明

- 不声明 F-028 / PJ-25 的 Plane UI 已验证、重复同步幂等已验证；
- 不声明任何项目 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
- 不声明生产/共享实例发生过任何写入；
- 不声明本轮启动或停止了任何服务；未读取或输出任何凭据明文；
- 本文件仅为派生证据记录，不替代 F-028 原始证据、人工审查与生产变更授权。

## 附录 A：本轮实际执行的只读命令

- `curl -sS -D- --max-time 6 http://127.0.0.1:{8000,3000,3001,18081}/`
- `curl -sS --max-time 6 https://pmc.csydsc.com/`、`curl -sS https://pmc.csydsc.com/api/instances/`
- `curl -sS -g -6 --max-time 5 http://[::1]:8000/api/instances/`
- `lsof -nP -iTCP:{3000,8000,18081,18000,3001,3004} -sTCP:LISTEN`；`ps -p <pid> -o pid,ppid,command`；`lsof -p <pid> | grep cwd`
- `docker ps -a --filter "name=globalcloudproject"`；`docker inspect globalcloudproject-api-1`；`docker logs --tail 15 globalcloudproject-api-1`
- MCP 只读：`pmc_health`、`pmc_whoami`、`pmc_readonly_work_items(limit=3)`

## 附录 B：本轮未做

- 未 commit/push；未修改 `projects/project/STATUS.md`、F-028 evidence 与 `docs/harness/evidence/README.md` 等任何既有文件；
- 未启动/停止容器或 dev server；未向任何 Plane 实例写入；未创建或读取凭据明文；
- 未重跑 `globalcloud/gpcf_sync.py`；未复跑 E2E/浏览器自动化。
