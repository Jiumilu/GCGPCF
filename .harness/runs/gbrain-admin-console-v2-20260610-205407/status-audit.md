# Harness Governance: gbrain-admin-console-v2 → accepted

## 事后门禁修正

V2 开发中多次重启 uvicorn，验证时走 `ssh macmini curl 127.0.0.1`（直连），
未检查 `localhost:19828` 隧道。导致浏览器无法访问。

**新增硬门禁：**
- `local_tunnel_alive`: 每次重启后验证 `curl localhost:19828/api/stats` 返回 200

## 当前验证 ✅

| 检查 | 结果 |
|------|------|
| Mac mini 服务 | PID 89291, 33 routes |
| 本地隧道 | localhost:19828 返回 200 |
| 前台 | 23.9KB 加载 |
| 后台 | 27.1KB 加载 |
| 搜索 | 2 results |
| 仪表盘 | 7,844 pages |

## Evidence Audit ✅

全部门禁通过，前后台均已恢复可访问。
