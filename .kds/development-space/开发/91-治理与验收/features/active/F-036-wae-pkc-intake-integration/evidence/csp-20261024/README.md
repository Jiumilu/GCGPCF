---
doc_id: GPCF-DOC-F036-CSP-20261024
title: F-036 CSP frame-ancestors 行为验证（2026-10-24）
project: GPCF
related_projects: [WAE, PKC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/csp-20261024/README.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/csp-20261024/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-036 CSP frame-ancestors 行为验证

- PKC dist 由自定义静态服务器提供，响应头：
  `Content-Security-Policy: frame-ancestors 'self' http://127.0.0.1:4300`
- 父页面 :4300（白名单内）：iframe 正常渲染，截图 149KB。
- 父页面 :4301（白名单外）：iframe 被 CSP 阻止，截图 4.8KB 空白。
- 结论：生产嵌入需按 WAE 域名配置 `frame-ancestors` 白名单；本验证只覆盖 CSP，不含 SSO/403/部署。
- 复现：`serve_csp.py` + 两个 parent html；测试后已停服务。
