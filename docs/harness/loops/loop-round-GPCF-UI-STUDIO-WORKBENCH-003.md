---
doc_id: GPCF-LOOP-UI-STUDIO-WORKBENCH-003
title: Loop Round GPCF-UI-STUDIO-WORKBENCH-003
project: GPCF
related_projects: [GPC, WAES, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-003.md
source_path: docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-003.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Loop Round GPCF-UI-STUDIO-WORKBENCH-003

## 输入

- `docs/harness/evidence/studio-kanban-runtime-entry-gate-20260622.md`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-002.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/router/index.ts`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/LoginView.vue`
- 用户授权：允许使用登录页显示的默认凭据完成本地登录验证

## 动作

1. 使用授权的本地默认凭据登录 `Studio`。
2. 记录登录后的默认落点和默认密码提醒弹窗。
3. 再次访问 `/#/hermes/kanban`，确认 `KanbanView` 是否真实进入。
4. 对 `KanbanView` 补齐桌面态、移动态截图及最小键盘焦点验证。
5. 记录一个真实运行发现：`chat -> kanban` 路由切换需 `reload()` 才稳定进入目标页。

## 输出

- `docs/harness/evidence/studio-kanban-runtime-verified-20260622.md`
- `docs/harness/evidence/studio-kanban-runtime-verified-20260622.json`
- `docs/harness/evidence/assets/studio-kanban-desktop-20260622.png`
- `docs/harness/evidence/assets/studio-kanban-mobile-20260622.png`
- `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-003.md`

## 检查

运行态检查要点：

1. 登录成功。
2. `KanbanView` 最终可达。
3. 桌面态与移动态截图已生成。
4. 无水平溢出。
5. 键盘焦点至少能落到 `新建任务` 表单的 `任务标题` 输入框。

## 反馈

本轮已经把 `Studio/KanbanView` 从“登录前入口阻断”推进到“登录后真实运行态可达”。

当前结论如下：

1. `KanbanView` 真实运行页已经进入并完成截图。
2. 当前状态由 `ui_blocked` 重新推进为 `ui_partial`。
3. 仍不能升为 `ui_ready`，因为发现了一个真实路由/渲染偏差：从 `chat` 切到 `kanban` 时需要刷新才能稳定显示目标页。

## 连续运行真实性记录

| 字段 | 值 |
|---|---|
| declared_rounds | 1/1 |
| substantive_rounds | 1/1 |
| generated_items | 5 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |

## 7.1 UI 质量门禁

| 字段 | 值 |
|---|---|
| UI scope | true |
| Surface | operation-workbench |
| Repository/path | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue` |
| Scope | `Studio` Kanban 登录后运行态、桌面/移动端与最小键盘焦点路径验证 |
| Tools used | `manual` / `in-app-browser` |
| Tools unavailable | `impeccable_not_invoked` / `figma_not_verified` |
| Verification | 登录成功 + 运行态页面截图 + 移动端截图 + 最小键盘焦点检查 |
| Status ceiling | `ui_evidence_candidate` |

```text
UI gate status: ui_partial
Surface: operation-workbench
Repository/path: /Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Studio/packages/client/src/views/hermes/KanbanView.vue
Scope: Studio Kanban 登录后运行态、桌面/移动端与最小键盘焦点路径验证
Tools used: manual, in-app-browser
Tools unavailable: impeccable_not_invoked, figma_not_verified
Verification: 登录成功 + 运行态页面截图 + 移动端截图 + 最小键盘焦点检查
Status ceiling: ui_evidence_candidate
```

| Gate | Status | Evidence | Remaining work |
|---|---|---|---|
| G1 Surface Structure | pass | 登录后页面标题为 `看板`，板选择、筛选、状态列与 `新建任务` 都已真实出现 | 补有真实任务数据时的结构截图 |
| G2 Design Tokens | partial | 运行态与 Studio 本地令牌一致，但尚未完成项目群统一令牌映射 | 下一轮形成 WAES 映射清单 |
| G3 Component Consistency | pass | 页头、按钮、筛选器、列、弹窗运行态一致 | 后续与 WAES 母框架逐项对表 |
| G4 Evidence And Governance | partial | 当前空板状态未能覆盖 receipt / audit / source record | 需用真实任务数据补充 |
| G5 AI Fact Separation | partial | 当前工作台页本身未混写 AI 事实，但主应用默认落到 chat，边界仍需治理 | 补工作台内 AI 分区验证 |
| G6 Accessibility | partial | 打开 `新建任务` 后焦点落到 `任务标题` 输入框 | 继续补完整 Tab 顺序与关闭路径 |
| G7 Responsive And Text Robustness | pass | `1280x720` 与 `390x844` 均 `overflowX=false` | 补真实任务卡片长文本验证 |
| G8 Runtime Verification | partial | 登录后真实进入 `KanbanView`；但 `chat -> kanban` 切换需刷新才能稳定生效 | 将该问题纳入下一轮修复 |
| G9 Scope Control | pass | 本轮只做运行验证与证据记录，未改 `Studio` 代码 | 下一轮修复仍保持最小范围 |

UI caveats：

- `a11y_manual_only`
- `figma_not_verified`
- `runtime_verified_with_reload_note`

## 8. 产出文件

| 文件 | 类型 | 说明 |
|---|---|---|
| `docs/harness/evidence/studio-kanban-runtime-verified-20260622.md` | 新增 | 登录后运行态验证证据 |
| `docs/harness/evidence/studio-kanban-runtime-verified-20260622.json` | 新增 | 登录后运行态机器证据 |
| `docs/harness/evidence/assets/studio-kanban-desktop-20260622.png` | 新增 | 桌面态截图 |
| `docs/harness/evidence/assets/studio-kanban-mobile-20260622.png` | 新增 | 移动态截图 |
| `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-003.md` | 新增 | 本轮 Loop 记录 |

## 9. Evidence 清单

| evidence | 路径 | 是否完整 |
|---|---|---|
| Studio Kanban runtime verified markdown evidence | `docs/harness/evidence/studio-kanban-runtime-verified-20260622.md` | yes |
| Studio Kanban runtime verified json evidence | `docs/harness/evidence/studio-kanban-runtime-verified-20260622.json` | yes |
| 桌面态截图 | `docs/harness/evidence/assets/studio-kanban-desktop-20260622.png` | yes |
| 移动态截图 | `docs/harness/evidence/assets/studio-kanban-mobile-20260622.png` | yes |
| 本轮 Loop 记录 | `docs/harness/loops/loop-round-GPCF-UI-STUDIO-WORKBENCH-003.md` | yes |

## 10. 风险与回滚

| 风险 | 等级 | 处置 | 回滚/撤销路径 |
|---|---|---|---|
| 将“刷新后可达”误写成“路由无问题” | P1 | 保持 G8=`partial` 并显式记录 reload 依赖 | 下一轮只针对路由偏差修复 |
| 误把空板状态写成工作台功能完整 | P1 | 保持 G4/G5=`partial` | 需补真实任务数据场景 |
| 因默认账户提示忽略安全边界 | P1 | 只记录提醒事实，不做账户修改 | 安全整改另行处理 |

## 11. 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | completed |
| 门禁结果 | partial |
| 是否需要人工确认 | no |
| 是否可进入下一轮 | yes |
| 连续运行是否必须继续 | no |

## 12. 下一轮建议

- 下一轮 Round ID：`GPCF-UI-STUDIO-WORKBENCH-004`
- 下一轮目标：只针对 `chat -> kanban` 路由/渲染偏差做最小修复与复验
- 下一轮仍禁止：不得把当前状态提升为 `ui_ready`，不得宣称工作台全量验证完成
