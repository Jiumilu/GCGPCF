---
doc_id: GPCF-DOC-8DCFDAD068
title: 阿里云 ECS 当前访问机制与配置变更控制
project: WAES
related_projects: [GFIS, WAES, KDS, XGD, GPCF]
domain: governance
status: controlled
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/ops/ecs-access-control-and-network-boundary.md
source_path: 02-governance/ops/ecs-access-control-and-network-boundary.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# 阿里云 ECS 当前访问机制与配置变更控制

## 控制结论

本文档记录 GlobalCloud 当前阿里云 ECS 入口、反向隧道、Caddy 路由、裸 IP 兜底入口、RustDesk 基线和自动化变更边界。该文档是 Loop、Hermes、Codex 和项目群自动化的运行边界，不代表本轮执行了任何 ECS、阿里云、Caddy、隧道或生产配置变更。

## 配置变更控制

| 主体 | 权限边界 |
|---|---|
| Hermes | 只允许 read-only 诊断、日志读取和建议输出；不得在任何时候、通过任何方式修改 ECS、阿里云控制台/CLI、安全组、防火墙、Caddy/Nginx、SSH 隧道、systemd/launchd、Docker/Compose、容器服务或运行时配置 |
| Codex 当前会话 | 只有在用户明确授权且满足回滚、审计、风险门禁时，才可作为变更执行入口；默认只做文档、分析、验证和建议 |
| 其他系统、服务、cron、Agent、外部自动化 | 不得直接执行配置变更；必须先提交到 Codex 当前会话或人工变更流程 |
| 人工 root / 云账号持有人 | 可执行需要 sudo、root、承载账号或控制台权限的动作；执行后应回写受控 evidence |

禁止把任何密钥、Token、RustDesk Key、云账号凭据写入 Git、文档、evidence、日志或 KDS 镜像。

## 网络边界

| 区域 | 说明 | 暴露策略 |
|---|---|---|
| Internet | 公网用户、外部 API 调用方 | 只访问阿里云 ECS 的 80/443 |
| Aliyun ECS `121.40.144.57` | 公网入口、TLS、反向代理 | 不保存核心数据 |
| Tunnel | ECS 到 MacPro 的反向连接 | 只绑定 ECS 本地回环地址 |
| MacPro Docker | 核心服务和数据服务 | 内部 bridge 网络 |
| LAN | 局域网设备 | 只访问 local-gateway |

公网 80/443 在到达 Caddy 前可能经过阿里云 Beaver/WAF/备案入口策略。出现 `Server: Beaver`、`403`、TLS 握手失败、`SSL_ERROR_SYSCALL` 时，应优先判断是否被阿里云入口层拦截，而不是只看 ECS 内部 Caddy 和隧道状态。

## 2026-06-06 已确认基线

- FunASR/TTS 的局域网后端、ECS `127.0.0.1:31095/31096` 隧道和 ECS 内部 Caddy 路由均正常。
- 公网 `funasr.csydsc.com`、`tts.csydsc.com` 的 80/443 被阿里云前置入口层拦截。
- 当前本机 aliyun CLI 账号不是 ECS 承载账号；WAF、网站接入、云防火墙、备案接入、DDoS、安全中心等入口层策略需要使用承载账号 `1096301569235682` 处理。
- ECS root 下已完成 `/etc/caddy/Caddyfile` 最小持久化修正并重载 Caddy：`health.csydsc.com` 固定为 `respond "ok" 200`，`xiaog.csydsc.com` 固定为 `127.0.0.1:28645`。
- FunASR/TTS 的 ECS 内部 Caddy 路由正常；公网异常仍按阿里云前置入口层处理。

## 裸 IP HTTP 兜底入口

| 公网入口 | ECS 目标 | 用途 | 验证 |
|---|---|---|---|
| `http://121.40.144.57/funasr/*` | `127.0.0.1:31095` | FunASR | `/funasr/v1/models` 返回 200 |
| `http://121.40.144.57/tts/*` | `127.0.0.1:31096` | EdgeTTS/TTS | `/tts/health` 返回 200；`/tts/tts` 返回 `audio/wav` |

主 Mac 应用当前应使用裸 IP 路径入口：

| 配置项 | 当前值 |
|---|---|
| `FunASR_BASE_URL` | `http://121.40.144.57/funasr` |
| `FunASR_TRANSCRIBE_URL` | `http://121.40.144.57/funasr/v1/audio/transcriptions` |
| `TTS_BASE_URL` | `http://121.40.144.57/tts` |
| `TTS_SYNTH_URL` | `http://121.40.144.57/tts/tts` |
| `TTS_HEALTH_URL` | `http://121.40.144.57/tts/health` |

在承载账号处理 Beaver/WAF/备案入口层之前，不应将 `https://funasr.csydsc.com` 和 `https://tts.csydsc.com` 作为运行配置。

## 当前 ECS 运行时路由基线

| 域名 | ECS 目标 | 状态 |
|---|---|---|
| `health.csydsc.com` | Caddy `respond "ok"` | 已部署 |
| `hermes.csydsc.com` | `127.0.0.1:31201` | 已部署 |
| `funasr.csydsc.com` | `127.0.0.1:31095` | 已部署，公网入口层可能拦截 |
| `tts.csydsc.com` | `127.0.0.1:31096` | 已部署，公网入口层可能拦截 |
| `ollama.csydsc.com` | `127.0.0.1:31434` | 已部署 |
| `xiaog.csydsc.com` | `127.0.0.1:28645` | 已部署 |
| `qdrant.csydsc.com` | 503 / 不进公网入口 | 按设计不暴露；本地 Qdrant 未配置鉴权 |
| `ha.csydsc.com` | 未接入后端 | ECS 内部应返回 502 |
| `web.csydsc.com` | 未接入后端 | ECS 内部应返回 502 |

当前 Caddy 运行时配置通过 Admin API 加载，不完全等于 `/etc/caddy/Caddyfile`。规范化模板位于 ECS 的 `/home/tunnel/caddy/Caddyfile.normalized`。

## 巡检分类约定

| 场景 | 分类 |
|---|---|
| `web.csydsc.com` 与 `ha.csydsc.com` 在 ECS 内部返回非 502 | DRIFT；优先排查本地 `com.csydsc.reverse-tunnel.core` 是否重新带回 `30888` 或 `31123` 映射 |
| 公网侧出现 `Server: Beaver`、`SSL_ERROR_SYSCALL` 或入口层 403 | 阿里云前置入口层拦截；不直接归因于 ECS Caddy 路由故障 |
| `health`、`hermes`、`funasr`、`tts`、`ollama`、`xiaog` 与基线不符 | 优先按 ECS Caddy 或隧道问题处理 |

## 当前 SSH 反向隧道

| ECS localhost | 本地或局域网目标 | 服务 |
|---|---|---|
| `127.0.0.1:31095` | `192.168.31.60:10095` | FunASR |
| `127.0.0.1:31096` | `192.168.31.60:10096` | TTS |
| `127.0.0.1:31201` | `127.0.0.1:9000` | Hermes Dashboard |
| `127.0.0.1:31434` | `127.0.0.1:11434` | Ollama |
| `127.0.0.1:28645` | `127.0.0.1:8645` | 小G缓存代理 |

反向隧道应使用 `ExitOnForwardFailure=yes`。`tunnel` 用户没有免密 sudo，涉及 root 或服务重启的动作必须走人工 root 或明确授权的 Codex 当前会话流程。

## MacPro 与局域网访问

| 服务 | MacPro 监听 | ECS 监听 | 公网 |
|---|---|---|---|
| local-gateway HTTP | `0.0.0.0:8080` | tunnel `127.0.0.1:30888` | 443 via ECS |
| API | container internal `8080` | 不直接暴露 | 通过网关 |
| Web | container internal `3000` | 不直接暴露 | 通过网关 |
| PostgreSQL | `127.0.0.1:15432` | 不暴露 | 不暴露 |
| Redis | `127.0.0.1:16379` | 不暴露 | 不暴露 |
| Grafana | `127.0.0.1:13000` | 可选管理隧道 | 默认不暴露 |

局域网设备访问 `http://192.168.31.60:8080`。MacPro 防火墙建议只允许可信局域网网段访问 8080。

## RustDesk 基线

RustDesk 当前采用 ECS 本地 hbbs/hbbr、Caddy 和 socat 组合，不再通过 Mac Mini SSH 反向隧道，也不依赖旧的 `42116/42117` TCP forwarder。

| 入口 | 后端 |
|---|---|
| `rustdesk.csydsc.com` | ECS Caddy -> `127.0.0.1:31118` hbbs WSS |
| `csydsc.com/ws/*` | ECS Caddy -> `127.0.0.1:31119` hbbr WSS |

| ECS 入口 | 作用 |
|---|---|
| `21116/tcp` | hbbs TCP 入口，转发到 `31116` |
| `21116/udp` | hbbs UDP 入口，转发到 `31116` |
| `21117/tcp` | hbbr TCP 入口，转发到 `31117` |
| `21118/tcp` | hbbs WSS 入口，转发到 `31118` |
| `21119/tcp` | hbbr WSS 入口，转发到 `31119` |

当前客户端配置应使用：

| 设备 | ID Server | Relay | Key |
|---|---|---|---|
| 主 Mac | `csydsc.com` | `csydsc.com` | 仅从安全存储读取，不写入仓库文档 |
| Mac mini | `csydsc.com` | `csydsc.com` | 仅从安全存储读取，不写入仓库文档 |
| 手机 Web | `rustdesk.csydsc.com` | 留空 | 仅从安全存储读取，不写入仓库文档 |

历史 `42116/42117` 方案已弃用，只保留作迁移记录，不应再作为当前健康检查或客户端配置入口。

## Loop 与 Hermes 执行约束

- Loop 在 L3/L4/L5 模式下不得自动修改本文档列出的 ECS、Caddy、隧道、Docker、云控制台或安全策略。
- Hermes 不得作为 ECS 配置变更执行者；Hermes 的输出只能作为诊断 evidence 或建议输入。
- 任何真实生产入口层变更、服务重启、配置热更新、持久化、迁移、删除、权限变更、云账号操作，都必须停在人工确认或 Codex 当前会话显式授权边界。
- 运行巡检可以记录 `read-only` 命令结果，但不得把巡检通过写成生产可用、业务验收或 accepted/integrated。
