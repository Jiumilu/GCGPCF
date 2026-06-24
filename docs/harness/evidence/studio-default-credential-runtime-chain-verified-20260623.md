---
doc_id: GPCF-DOC-7C5E1A92D4
title: Studio 默认凭据治理运行链路验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-runtime-chain-verified-20260623.md
source_path: docs/harness/evidence/studio-default-credential-runtime-chain-verified-20260623.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据治理运行链路验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-RUNTIME-CHAIN-VERIFIED-20260623`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-014` 的新增事实：默认凭据治理链路已经获得受控真人工运行验证。

本轮关键事实如下：

1. 测试账号已完成真人工链路验证：`默认凭据登录 -> 跳到账户页 -> 改密/改名 -> 提示自动消失 -> 再进 chat 正常`。
2. 这证明前一轮补上的“治理动作后自动收口”不只是自动化测试成立，也已在真实运行链路上成立。
3. 本轮运行验证事实来自用户完成后的明确确认，不是本轮由智能体直接操作浏览器得出的观察。
4. 即便运行链路已闭合，UI 结论仍不能升格为业务 `complete/accepted/integrated`。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/hermes/settings/AccountSettings.vue
Scope: 默认凭据登录后到账户页整改、整改完成后提示自动收口、再进入 chat 正常的真人工运行链路
Tools used: manual, vitest
Tools unavailable: impeccable_not_invoked, figma_not_verified, mobile_not_verified
Verification: 用户确认测试账号真人工链路通过 + 既有前端账户页/登录提醒回归测试通过 + 后端 requiresCredentialChange 语义测试通过
Status ceiling: ui_evidence_candidate
```

## 运行链路证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 真人工链路 | 默认凭据登录后跳到账户页 | 用户确认已完成 |
| 真人工链路 | 账户页执行改密/改名 | 用户确认已完成 |
| 真人工链路 | 治理提示自动消失 | 用户确认已完成 |
| 真人工链路 | 完成整改后再进 chat 正常 | 用户确认已完成 |
| 前端自动化 | 账户页整改后收口测试通过 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/account-settings-default-credential.test.ts` |
| 前端自动化 | 登录分流与默认凭据提醒回归通过 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/login-view.test.ts` / `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts` |
| 后端自动化 | 改密或改名会清除 `requiresCredentialChange` | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/server/user-auth.test.ts` |

## 验证说明

### 运行链路新增事实

本轮新增的关键证据不是代码或单测，而是用户已完成的受控真人工运行验证：

1. 使用测试账号按默认凭据链路登录。
2. 系统真实跳到账户页进入治理动作。
3. 执行改密/改名后，默认凭据治理提示真实消失。
4. 随后重新进入 `chat` 主界面，功能链路正常。

### 与上一轮证据的关系

上一轮 `GPCF-UI-STUDIO-WORKBENCH-013` 已证明：

1. 前端页面具备整改后重新同步用户状态的收口逻辑。
2. 后端语义上会在改密或改名后撤销 `requiresCredentialChange`。

本轮则补上最后缺口：真实运行链路也已成立，因此 `runtime_not_verified` 不再适用于这条默认凭据治理链路。

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 默认凭据用户被导向账户页完成治理，再返回 chat；入口、治理页、返回主界面链路已闭合 | 后续可补首次登录强制治理的单步引导 |
| G2 Design Tokens | pass | 本轮不新增样式层，只验证既有治理链路在真实运行时成立 | 无 |
| G3 Component Consistency | pass | 登录分流、账户页治理、页内提示收口、返回 chat 使用同一套既有界面框架 | 后续继续沉淀到统一工作台治理模式 |
| G4 Evidence And Governance | pass | 自动化证据与用户确认的真人工链路证据已分开记录，未越权升级项目状态 | 后续可在 Harness 侧继续汇总 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 建议与业务事实混写 | 无 |
| G6 Accessibility | partial | 现仅能证明功能链路成立，尚无更细键盘顺序、读屏、焦点回退证据 | 后续补账户页与 chat 回跳的完整 a11y 证据 |
| G7 Responsive And Text Robustness | partial | 本轮新增的是运行链路事实，不含移动端/平板端复验 | 后续补移动端默认凭据治理链路 |
| G8 Runtime Verification | pass | 用户已完成受控真人工链路：登录、整改、提示消失、回到 chat 正常 | 如需更强证据，可再补截图或录屏归档 |
| G9 Scope Control | pass | 本轮仅新增证据与 loop 记录，不改 Studio 代码 | 无额外扩面 |

## 结论

这条默认凭据治理链路现在具备两层证据：

1. 自动化测试证明逻辑存在且语义正确。
2. 受控真人工运行验证证明真实链路可走通。

因此，本项“默认凭据登录后治理并自动收口”的运行验证缺口已经关闭。但整体 UI 门禁状态仍保持 `ui_partial`，因为可访问性、移动端链路和项目群级统一治理规范仍有未关闭项。

## UI Caveats

- `runtime_confirmed_by_user_report`
- `a11y_manual_only`
- `figma_not_verified`
- `mobile_not_verified`
- `credential_change_not_enforced_server_side`

## 下一步建议

1. 补移动端默认凭据治理链路的真人工验证。
2. 评估后端是否进入“首次登录强制改密/改名”治理阶段。
3. 将这条“默认凭据治理闭环”固化进项目群专业工作台通用登录治理规范。
