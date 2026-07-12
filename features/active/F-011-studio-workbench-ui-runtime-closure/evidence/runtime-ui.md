---
doc_id: GPCF-DOC-F011-STUDIO-WORKBENCH-RUNTIME-UI-20260712
title: Studio 工作台运行态 UI 证据
project: GPCF
related_projects: [Studio, WAES, GPCF]
domain: ui-delivery
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-011-studio-workbench-ui-runtime-closure/evidence/runtime-ui.md
source_path: features/active/F-011-studio-workbench-ui-runtime-closure/evidence/runtime-ui.md
sync_direction: bidirectional
last_reviewed: 2026-07-12
supersedes: []
superseded_by: []
---

# Studio 工作台运行态 UI 证据

日期：2026-07-12

## 变更对象

- Studio 页面：`/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/SettingsView.vue`
- Feature：`F-011`

## 本轮实装结果

- 对设置页中的“智能运营工作台入口”进行了真实界面增强。
- 保留原有跳转语义、整改态隔离逻辑和既有测试前提。
- 新增工作台眉标、能力摘要、按钮视觉强化、焦点态和移动端按钮铺满策略。

## 本地验证

### 单元测试

```text
npm test -- tests/client/settings-view-default-credential.test.ts tests/client/router-default-credential-guard.test.ts
2 files passed, 10 tests passed
```

### 浏览器运行态

```text
npx playwright test tests/e2e/studio-shell-visual.spec.ts --project=chromium
```

- 已真实生成：
  - `artifacts/studio-settings-runtime/settings-desktop.png`
  - `artifacts/studio-settings-runtime/settings-desktop.json`
- Playwright 用例在后续切换到 `/#/hermes/chat?mvp=project` 时失败，失败点为既有断言 `main.app-main display=contents`，不在本轮设置页改造范围内。
- 设置页桌面视口截图和结构指标已先行落盘，可回放本轮页面改造结果。

## 运行态结构指标

- URL：`http://127.0.0.1:8679/#/hermes/settings`
- shell columns：`global-nav|smart-session|center-workspace|kds-workspace`
- grid columns：`64px 288px 743px 405px`
