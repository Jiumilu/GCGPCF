---
doc_id: GPCF-DOC-5A9F2D1C7E
title: Studio 默认凭据移动端运行链路验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-mobile-runtime-verified-20260623.md
source_path: docs/harness/evidence/studio-default-credential-mobile-runtime-verified-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据移动端运行链路验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-MOBILE-RUNTIME-VERIFIED-20260623`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-015` 的新增事实：默认凭据治理链路已在移动端视口 `390x844` 下获得智能体观察到的真实运行证据。

本轮关键事实如下：

1. 在隔离运行时中，默认凭据 `admin / 123456` 登录后，会真实跳到 `#/hermes/settings?tab=account&reason=default-credentials`。
2. 移动端账户页会显示默认凭据治理提示，且 `390px` 视口下无水平溢出。
3. 执行“修改密码”后，路由中的 `reason=default-credentials` 会被清理，治理提示自动消失。
4. 随后执行“修改用户名”后，账户页状态保持收口，仍无水平溢出。
5. 整改完成后进入 `#/hermes/chat` 正常，且移动端 chat 主界面同样无水平溢出。
6. 运行验证期间暴露出账户页关闭按钮缺少 `common.close` 语言键，本轮已在 Studio 多语言包中补齐该键，消除运行时 i18n 警告。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue
Scope: 默认凭据登录后到账户页治理、移动端执行改密/改名、提示自动收口、再进入 chat 正常的 390x844 运行链路
Tools used: playwright(system-chrome), curl, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 隔离运行时移动端真实链路通过 + 移动端账户页截图 + 移动端 chat 截图 + 前端账户页/登录提醒回归测试已通过
Status ceiling: ui_evidence_candidate
```

## 运行链路证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 运行环境 | 隔离前端 `8669` + 隔离后端 `8667` | 避免污染当前共享 `8647/8649` 运行时 |
| 登录链路 | 默认凭据登录后跳到账户页治理入口 | `#/hermes/settings?tab=account&reason=default-credentials` |
| 移动态账户页 | 治理提示真实出现，且无横向溢出 | `390x844`、`scrollWidth=390`、`overflowX=false` |
| 动作后收口 | 改密后治理提示消失，`reason` 路由参数被清理 | URL 变为 `#/hermes/settings?tab=account` |
| 动作补充 | 改用户名后账户页保持收口状态 | 当前账户显示为 `mobile-owner-20260623` |
| 移动态 chat | 整改完成后进入 chat 正常，且无横向溢出 | `#/hermes/chat`、`scrollWidth=390`、`overflowX=false` |
| 截图 | 账户页移动端截图 | `docs/harness/evidence/assets/studio-default-credential-mobile-account-20260623.png` |
| 截图 | chat 页移动端截图 | `docs/harness/evidence/assets/studio-default-credential-mobile-chat-20260623.png` |
| 代码修改 | 补齐账户页关闭按钮使用的 `common.close` 多语言键 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/i18n/locales/*.ts` |

## 验证说明

### 为什么使用隔离运行时

本轮没有直接复用当前共享 `8647/8649` 运行时，原因有两点：

1. 共享运行时中的测试账号凭据已被改变，不能再用默认凭据直接复验。
2. Studio 后端在 `dev` 模式下固定把数据库写入 `packages/server/data`，不尊重 `HERMES_WEB_UI_HOME`，不能提供真正隔离的默认凭据环境。

因此，本轮采用：

1. Vite 前端：`http://127.0.0.1:8669`
2. production 后端：`http://127.0.0.1:8667`
3. 独立 `HERMES_WEB_UI_HOME=/tmp/gc-studio-mobile-verify-prod-home`

这样得到的是“当前代码基线下可复现的移动端默认凭据治理链路”，且不污染共享账号状态。

### 真实运行结果

智能体实际观察到的顺序如下：

1. `admin / 123456` 登录成功。
2. 登录后跳转到账户页治理入口。
3. 移动端账户页提示卡显示正常，无横向溢出。
4. 修改密码后，治理提示自动消失，URL 中 `reason=default-credentials` 被移除。
5. 修改用户名后，账户页保持已收口状态。
6. 随后进入 `chat` 页面正常，且移动端 `390px` 视口无横向溢出。
7. 账户页关闭按钮不再缺失 `common.close` 语言键，运行时 i18n 警告已被修正。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 移动端已真实完成“登录 -> 账户页治理 -> 收口 -> 回 chat”链路 | 后续可评估首次登录单步强制治理 |
| G2 Design Tokens | pass | 本轮不改视觉实现，只验证现有界面在移动端链路成立 | 无 |
| G3 Component Consistency | pass | 登录页、账户页、提示卡、chat 页在同一框架内连续可用 | 后续继续沉淀项目群统一模式 |
| G4 Evidence And Governance | pass | 智能体观察到的运行证据、自动化测试、隔离环境理由都已分离记录 | 后续可供 Harness 审计引用 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议与业务事实混写 | 无 |
| G6 Accessibility | partial | 已验证移动端功能链路与基本可见性，但未补完整键盘/读屏路径 | 后续补账户页与 chat 回跳的 a11y 证据 |
| G7 Responsive And Text Robustness | pass | `390x844` 账户页与 chat 页均 `overflowX=false` | 后续补更窄视口与更长文本场景 |
| G8 Runtime Verification | pass | 智能体在隔离运行时中真实完成移动端默认凭据治理链路 | 如需更强证据，可补录屏或更多视口 |
| G9 Scope Control | pass | 本轮只新增证据与 loop 记录，不改 Studio 代码 | 无额外扩面 |

## 结论

默认凭据治理链路现在具备三层证据：

1. 自动化测试证明前端收口逻辑与后端语义正确。
2. 用户确认的真人工桌面链路已成立。
3. 智能体观察到的移动端 `390x844` 运行链路也已成立。

因此，默认凭据治理链路的“移动端运行验证”缺口已经关闭。但整体 UI 状态仍保持 `ui_partial`，原因是更细的可访问性证据、更多移动端极限场景，以及项目群级统一规范闭环仍未全部完成。

## UI Caveats

- `runtime_verified_on_isolated_runtime`
- `a11y_manual_only`
- `figma_not_verified`
- `credential_change_not_enforced_server_side`

## 下一步建议

1. 如果继续推进真实性，应补更窄视口和长文本场景下的移动端验证。
2. 如果继续推进治理闭环，应评估后端首次登录强制改密/改名能力。
3. 将“默认凭据治理链路在桌面与移动端均需可闭合”写入项目群工作台登录治理规范。
