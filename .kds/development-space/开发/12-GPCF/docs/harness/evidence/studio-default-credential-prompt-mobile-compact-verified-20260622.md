---
doc_id: GPCF-DOC-6C81F0E2A4
title: Studio 默认凭据提醒移动端紧凑化验证证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-default-credential-prompt-mobile-compact-verified-20260622.md
source_path: docs/harness/evidence/studio-default-credential-prompt-mobile-compact-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Studio 默认凭据提醒移动端紧凑化验证证据

## 证据摘要

Evidence ID: `STUDIO-DEFAULT-CREDENTIAL-PROMPT-MOBILE-COMPACT-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-011` 的真实结果：在第 010 轮已完成“非阻断化”的基础上，默认凭据提醒在移动端进一步压缩占位，主导航与工作台入口露出更多可视空间。

本轮关键事实如下：

1. 本轮没有再调整提醒逻辑，只对移动端样式做紧凑化处理。
2. 移动端浮层从“近乎整行铺满”改为右下角窄宽度浮层。
3. 真实 `Safari` 390px 视口复验中，浮层尺寸为 `312x169`，右边距 `8px`，底边距 `8px`。
4. 汉堡菜单展开后，侧栏仍可见，说明压缩后没有破坏主导航可达性。
5. 本轮不声明默认凭据风险已关闭，只声明移动端 UI 占位进一步优化。

## Required Summary

```text
UI gate status: ui_partial
Surface: ai-chat
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue
Scope: 仅压缩默认凭据提醒在移动端的占位，不改变提醒语义与动作
Tools used: manual, vitest, safaridriver
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 组件单测通过 + 真实 Safari 移动端尺寸与侧栏可见性复验
Status ceiling: ui_evidence_candidate
```

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 代码修改 | 仅调整移动端 `DefaultCredentialPrompt` 的宽度、边距、内边距、标题/正文/按钮占位 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/auth/DefaultCredentialPrompt.vue` |
| 组件测试 | 提醒逻辑与交互测试继续通过 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/tests/client/default-credential-prompt.test.ts` |
| 测试命令 | `npm test -- tests/client/default-credential-prompt.test.ts` | 结果：`1 passed / 3 tests passed` |
| 运行态截图 | 移动端紧凑版提醒与侧栏同屏 | `docs/harness/evidence/assets/studio-default-credential-prompt-mobile-compact-20260622.png` |
| 运行态观测 | 提醒尺寸 `312x169`，右边距 `8px`，底边距 `8px` | `Safari WebDriver` 实测 |

## 运行态复验

真实 `Safari` 390px 视口复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 使用默认凭据 `admin / 123456` 登录
3. 默认凭据提醒以紧凑浮层形式显示在右下角
4. 点击左上角汉堡菜单后，侧栏正常展开
5. 同屏可见侧栏主体与默认凭据提醒，未再出现上一版那种大面积底部覆盖

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 浮层仍在右下角，不影响移动端主导航入口结构 | 后续可继续统一系统告警浮层层级 |
| G2 Design Tokens | pass | 沿用既有令牌，仅压缩布局密度 | 无 |
| G3 Component Consistency | partial | 组件继续沿用统一按钮与深色浮层语义 | 后续纳入更广的系统提醒组件规范 |
| G4 Evidence And Governance | pass | 明确仅是移动端占位优化，不冒充凭据治理关闭 | 后续治理默认凭据问题本体 |
| G5 AI Fact Separation | not_applicable | 本轮不涉及 AI 语义分离 | 无 |
| G6 Accessibility | partial | 可见性与关闭动作保持不变，但未新增读屏/焦点证据 | 后续补更细可访问性验证 |
| G7 Responsive And Text Robustness | pass | 浮层实测缩至 `312x169`，侧栏可见性更好 | 后续可继续探索更窄屏与更长文案 |
| G8 Runtime Verification | pass | 单测通过，真实 Safari 移动端截图与尺寸记录存在 | 运行态证据成立 |
| G9 Scope Control | pass | 本轮只改移动端样式，不动逻辑 | 无额外扩面 |

## 结论

本轮最小目标已经真实达成：

1. 默认凭据提醒在移动端更紧凑。
2. 主导航与工作台入口露出更多可见区域。
3. 提醒语义、关闭动作、跳转动作都未被破坏。

本轮状态保持 `ui_partial`，原因是默认凭据问题本身仍未关闭，且该提醒仍属于过渡性治理手段。

## UI Caveats

- `a11y_manual_only`
- `figma_not_verified`
- `default_credential_risk_still_exists`
- `mobile_prompt_compacted_but_not_eliminated`

## 下一步建议

1. 如果继续优化，可把移动端正文压缩为更短的一级提示 + 二级说明入口。
2. 更优解应转向首次登录改密流程，而不是长期浮层提醒。
3. 将“移动端浮层默认窄宽度 + 右下角锚定”写入系统级提醒组件规范。
