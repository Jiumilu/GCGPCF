---
doc_id: GPCF-DOC-7D6C9E5C21
title: Studio Chat 工作台键盘与移动端复验证据
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/evidence/studio-chat-workbench-keyboard-mobile-verified-20260622.md
source_path: docs/harness/evidence/studio-chat-workbench-keyboard-mobile-verified-20260622.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Studio Chat 工作台键盘与移动端复验证据

## 证据摘要

Evidence ID: `STUDIO-CHAT-WORKBENCH-KEYBOARD-MOBILE-VERIFIED-20260622`

本证据用于记录 `GPCF-UI-STUDIO-WORKBENCH-009` 的真实结果：此前对移动端“入口缺失”的初判已被撤回，`chat` 主界面的工作台入口在桌面端可通过键盘访问，在移动端通过汉堡菜单可见且可达。

本轮关键事实如下：

1. 桌面端 `Safari` 运行态中，`任务`、`看板`、`频道` 三个入口都能获得可见焦点框，并可通过 `Enter` 完成跳转。
2. 移动端 390px 视口下，`chat` 主内容区默认不直接展示该侧栏，这是页面壳层设计，不等于入口缺失。
3. 点击移动端汉堡按钮后，侧栏真实展开，并出现 `新建对话 / 搜索 / 历史 / 任务 / 看板 / 频道`。
4. 从移动端侧栏点击 `看板` 后，真实进入 `#/hermes/kanban?board=default`。
5. 运行态仍会出现“默认账户与密码”提醒弹窗，该弹窗属于独立交互干扰项，不应混写成工作台入口缺陷。

## Required Summary

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/components/layout/PageSidebarNav.vue
Scope: 复验 chat 主界面工作台入口的桌面键盘可达性与移动端菜单可达性
Tools used: manual, safaridriver
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 真实 Safari 桌面键盘焦点 + 真实 Safari 移动端汉堡菜单展开与跳转
Status ceiling: ui_evidence_candidate
```

## 运行态复验

### 路径 1：桌面端键盘访问

真实 `Safari` 运行态复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 通过键盘聚焦 `任务`、`看板`、`频道`
3. 三个入口都显示默认浏览器焦点框，样式为 `5px auto rgb(0, 103, 244)`
4. 按 `Enter` 后分别进入：
   - `#/hermes/jobs`
   - `#/hermes/kanban`
   - `#/hermes/channels`

### 路径 2：移动端菜单访问

真实 `Safari` 390px 视口复验结果：

1. 打开 `http://127.0.0.1:8649/#/hermes/chat`
2. 移动端默认只显示主内容区，不直接展开侧栏
3. 点击左上角汉堡按钮后，侧栏展开
4. 展开后的侧栏真实出现 `新建对话 / 搜索 / 历史 / 任务 / 看板 / 频道`
5. 点击 `看板` 后进入 `http://127.0.0.1:8649/#/hermes/kanban?board=default`

## 实现证据

| Type | Evidence | Path / Observation |
|---|---|---|
| 运行态截图 | 桌面端 `chat` 主界面键盘焦点进入工作台入口 | `docs/harness/evidence/assets/studio-chat-workbench-keyboard-focus-20260622.png` |
| 运行态截图 | 移动端汉堡菜单展开后出现工作台入口 | `docs/harness/evidence/assets/studio-chat-workbench-mobile-menu-20260622.png` |
| 运行态截图 | 移动端从菜单进入 `Kanban` | `docs/harness/evidence/assets/studio-kanban-from-mobile-menu-20260622.png` |
| 运行态观测 | 桌面端 `任务 / 看板 / 频道` 焦点框可见且 `Enter` 可跳转 | `Safari WebDriver` 实测 |
| 运行态观测 | 移动端汉堡菜单展开后可见 `任务 / 看板 / 频道` | `Safari WebDriver` 实测 |
| 运行态观测 | 移动端 `看板` 跳转结果为 `#/hermes/kanban?board=default` | `Safari WebDriver` 实测 |

## Gate Table

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 桌面端与移动端都能到达工作台入口 | 后续继续扩外围工作台入口一致性 |
| G2 Design Tokens | partial | 本轮不涉及令牌与样式系统重构 | 继续做项目群级令牌治理 |
| G3 Component Consistency | pass | 同一入口集在桌面键盘与移动菜单都成立 | 后续补更多页面类一致性 |
| G4 Evidence And Governance | partial | 本轮仅补 UI 入口层证据 | 继续补业务闭环证据 |
| G5 AI Fact Separation | pass | 已撤回错误初判，保留真实移动端路径定义 | 继续保持事实与推断分离 |
| G6 Accessibility | pass | 桌面端焦点可见，键盘 `Enter` 可用 | 后续可补 `Tab` 顺序与读屏证据 |
| G7 Responsive And Text Robustness | pass | 移动端入口通过菜单暴露，未见横向溢出 | 后续补更窄视口与长文本场景 |
| G8 Runtime Verification | pass | 全部结论来自真实 `Safari` 运行态 | 运行态证据成立 |
| G9 Scope Control | pass | 本轮未改 Studio 代码，只做复验与证据固定 | 无额外扩面 |

## 结论

本轮最重要的结论不是“新增了什么”，而是“纠正了什么”：

1. `chat` 主界面工作台入口在桌面端具备真实键盘可达性。
2. 移动端并不存在“入口缺失”，真实模式是“通过汉堡菜单暴露入口”。
3. 先前移动端缺口判断应撤回，避免把壳层交互模式误记为 UI 缺陷。

整体 UI 门禁状态仍保持 `ui_partial`，因为项目群级统一规范、更多页面类与组件类审计、以及默认凭据提醒弹窗干扰治理尚未关闭。

## UI Caveats

- `default_credential_prompt_can_occlude_surface_controls`
- `figma_not_verified`
- `project_group_ui_gate_still_partial`

## 下一步建议

1. 把“默认凭据提醒弹窗会遮挡主界面操作”单独立项，不再并入工作台入口问题。
2. 继续对 `Jobs / Kanban / Channels` 做更细的移动端交互与页面类审计。
3. 进入项目群规范层，将“桌面直接入口 + 移动菜单入口”固化为专业工作台类导航基线。
