---
doc_id: GPCF-DOC-F036-EMBED-READINESS-20261022
title: F-036 真实受控嵌入就绪核查（2026-10-22）
project: WAE
related_projects: [WAE, PKC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/embed-readiness-20261022.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/embed-readiness-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-036 真实受控嵌入就绪核查（2026-10-22）

> 性质：就绪核查，不联调、不发起 PKC 运行时请求、不改配置。

## 1. 机制现状（已实现）

| 项 | 事实 |
|---|---|
| 入口 | `apps/wame/src/app/apps/PkcIntakePage.tsx` |
| 开关 | `VITE_PKC_EMBED_URL`（空则保持预演，不请求） |
| 触发 | 配置后仍需人工点击「启用受控嵌入」才渲染 iframe |
| 隔离 | `sandbox="allow-scripts allow-same-origin allow-forms"` + `referrerPolicy="no-referrer"` |
| 回滚 | 移除 `placement.city.yaml` 的 pkc app/entry → `pnpm gen:apps`；或清空 env |

## 2. 就绪缺口

| # | 缺口 | 责任方 | 阻塞等级 |
|---:|---|---|---|
| 1 | `VITE_PKC_EMBED_URL` 未配置（WAE `.env` 无该键） | WAE 属主 | 高 |
| 2 | PKC dev 端口 5174（`vite.config.ts`）；未确认 iframe 允许被嵌入 | PKC 属主 | 高 |
| 3 | 未发现 PKC `X-Frame-Options`/CSP `frame-ancestors` 配置 | PKC 属主 | 中 |
| 4 | PKC SSO/403 与 WAE 身份未对齐 | PKC 属主 | 高 |
| 5 | 无真实嵌入的回滚演练记录 | GPCF/WAE | 中 |

## 3. 联调前置步骤（待授权后执行）

1. PKC 启动 `pnpm dev`（:5174），确认页面可访问。
2. WAE 启动 `pnpm dev`（:4300），设置 `VITE_PKC_EMBED_URL=http://127.0.0.1:5174/`（仅本地）。
3. 登录 WAE → PKC 知识工作台 → 点击「启用受控嵌入」；监听网络，确认仅此时发起请求。
4. 验证 iframe 内 PKC 页面身份/403 与 WAE 一致；记录截图与请求日志。
5. 回滚：清空 env + 移除 pkc 注册 → 重跑 `gen:apps`，确认入口消失。

## 4. 风险

- `allow-scripts allow-same-origin` 组合在跨源场景下等价于放宽沙箱；需 PKC 侧 CSP/来源白名单配合。
- 真实嵌入后 PKC 的 401/403 可能被 iframe 吞掉，需错误边界与可读提示。
- 未完成 SSO 对齐前，iframe 内容不得作为治理证据。

## 5. 结论

**代码路径就绪，运行时配置与 PKC 侧嵌入条件未就绪**。在完成 §2 缺口 1–4 前，不得声明「PKC 已接入」；`task_flow` 仍以候选页为证据。

## 6. 非声明

- 不声明真实嵌入已联调；不声明 PKC 已接入；不声明任何项目状态提升。

## 7. 运行时探测（2026-10-23 04:55）

- PKC `pnpm dev --host 127.0.0.1`（:5174）启动成功；`curl -I /` → **HTTP 200**。
- 响应头**无** `X-Frame-Options`、**无** `Content-Security-Policy: frame-ancestors` → 开发态可被 iframe 嵌入，但**无嵌入防护**。
- 仅开发服务器探测；未验证生产/构建产物、SSO/403、CSP；验证后已停止 :5174。
- 结论不变：代码路径就绪，运行时配置与 PKC 侧安全/身份条件未就绪；不得声明 PKC 已接入。

## 8. 嵌入安全头建议（2026-10-23 05:15）

探测显示 PKC dev 无 `X-Frame-Options` / `frame-ancestors`。若要真实嵌入，建议：

1. `Content-Security-Policy: frame-ancestors 'self' http://127.0.0.1:4300`（生产替换为 WAE 域名）。
2. 或 `X-Frame-Options: ALLOW-FROM <WAE>`（兼容旧浏览器；现代优先 CSP）。
3. iframe 侧保持 `sandbox="allow-scripts allow-same-origin allow-forms"`，但需评估 `allow-same-origin` + `allow-scripts` 组合风险；跨源时考虑去掉 `allow-same-origin`。
4. `Referrer-Policy: no-referrer` 已在 WAE 侧设置；PKC 侧补 `X-Content-Type-Options: nosniff`。
5. SSO/403：iframe 内 401/403 需可读提示，不得静默失败；未对齐前不得作为治理证据。

以上为建议，未改 PKC 配置。
