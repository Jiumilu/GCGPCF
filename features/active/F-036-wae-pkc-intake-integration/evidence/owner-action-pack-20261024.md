---
doc_id: GPCF-DOC-F036-OWNER-PACK-20261024
title: F-036 WAE/PKC 属主动作包
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/owner-action-pack-20261024.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/owner-action-pack-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-036 属主动作包

## 已完成（GPCF/WAE/PKC）

- WAE 生产构建验证（embed URL + allow-same-origin）；
- 登录态受控嵌入（隔离 IdP）Playwright；
- CSP allow/block；
- 401/403 超时降级 + postMessage 双端：
  - WAE 708d02e 监听；
  - PKC 90dbbf3a/6daf867e 上报 + no-referrer 兜底；
  - PKC e74c12ce ready；
- 证据 manifest 83 文件 hash。

## 需属主动作

| 项目 | 动作 |
|---|---|
| WAE | 生产部署（目标环境/域名/回滚） |
| PKC | 正式 SSO 接入（非隔离 IdP） |
| WAE/PKC | 属主签字（UI/安全/运行） |
| 老卢 | 生产授权、发布窗口 |

## 部署前检查

1. `VITE_PKC_EMBED_URL` 指向生产 PKC；
2. PKC `frame-ancestors` 放行 WAE 生产域名；
3. SSO 登录态可跨域/iframe 使用；
4. 401/403 显示可读提示（已验证代码路径）；
5. 回滚：移除 WAE 入口或关闭 embed URL。

## 签完后 GPCF 动作

1. 更新 F-036 blockers 与 resolved；
2. `python3 scripts/gpcf_check_evidence.py --check-only F-036`；
3. 关闭需授权；不声明 production_ready。

## 非声明

- 不声明部署/SSO 已完成；不声明 F-036 可关闭。
