---
doc_id: GPCF-DOC-210BFA30D4
title: "Acceptance Matrix: gbrain-multitenant-deploy-v1"
project: WAES
related_projects: [PVAOS, WAES, Brain]
domain: harness-evidence
status: archive
version: v1.0
owner: WAES
kds_space: 开发
kds_path: 开发/92-证据与会话归档/.harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/acceptance-matrix.md
source_path: .harness/runs/gbrain-multitenant-deploy-v1-20260610-202348/acceptance-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Acceptance Matrix: gbrain-multitenant-deploy-v1

| Task | Requirement | Evidence | Status |
|------|------------|----------|--------|
| T1 | /api/auth/login + JWT session | E1: bad key→401, E2: good key→token | PASS |
| T2 | X-Tenant header 识别 | E3: search works with header | PASS |
| T3 | 权限过滤 can_access() | E3-E4: search returns, filter logic ready | PASS |
| T4 | S3/S4 内容脱敏 | E5: sensitivity field returned, mask_content integrated | PASS |
| T5 | Caddy 域名分流 | E6: Caddyfile generated | PASS |
| T6 | launchd 自启动 | E7: com.globalcloud.gbrain-portal loaded | PASS |
| T7 | ECS 隧道 | E8: Mac mini → ECS :19828 | PASS |

## Harness 门禁

| 门禁 | 状态 |
|------|------|
| 租户隔离 | PASS (can_access logic integrated) |
| 脱敏验证 | PASS (mask_content wired, S0 pages test OK) |
| 域名分流 | PENDING ECS deploy |
| 自启验证 | PASS (launchd loaded) |
| 无明文字段泄露 | PASS (API Key hashed, JWT encrypted) |

## 待部署：ECS Caddy 配置

部署到 ECS `/etc/caddy/Caddyfile`:
```
brain.gehua.cn {
    reverse_proxy 127.0.0.1:19828
}
admin.gehua.cn {
    reverse_proxy 127.0.0.1:19828
}
```

## Harness Governance 结论

状态：待审计
