---
doc_id: GPCF-DOC-8352F39CCF
title: "Harness Governance Status Audit: gbrain-multitenant-deploy-v1"
project: WAES
related_projects: [PVAOS, WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/status-audit.md
source_path: .harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/status-audit.md
sync_direction: bidirectional
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# Harness Governance Status Audit: gbrain-multitenant-deploy-v1

## Status: accepted → complete

人工确认 + ECS Caddy 部署完成。

## 部署架构

```
用户浏览器
    │
    ▼
gbrain.csydsc.com (ECS Caddy :443)
gbrain-admin.csydsc.com
    │
    ▼
ECS :19828 ──SSH隧道──→ Mac mini :19828 (GCBrain Portal)
                              │
                              ├── /api/* (前台)
                              ├── /admin/* (后台, Basic Auth)
                              └── pgvector :5432
```

## 访问地址

| 服务 | 地址 | 认证 |
|------|------|------|
| 知识门户 | `https://gbrain.csydsc.com` | 可选 API Key 登录 |
| 管理控制台 | `https://gbrain-admin.csydsc.com` | Basic Auth |

## 待持久化（Caddyfile 需手动写入）

```
sudo tee -a /etc/caddy/Caddyfile < /tmp/new_caddy_entries.txt
```

路由已在 Caddy 内存中生效，仅重启会丢失。

## Evidence 最终审计

| ID | Result |
|----|--------|
| E1-E8 | All pass |
| E9 (Caddy) | Routes live, verified 200 |

## 判定: complete

GCBrain 三阶段全部交付:
- Phase 1: 知识门户 ✅
- Phase 2: 管理控制台 ✅
- Phase 3: 多租户权限 + 生产部署 ✅
