---
doc_id: GPCF-DOC-F038-I18N-INVENTORY-20261024
title: F-038 i18n 存量盘点（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-038-panorama-operation-normalization/evidence/i18n-inventory-20261024.md
source_path: features/active/F-038-panorama-operation-normalization/evidence/i18n-inventory-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# F-038 i18n 存量盘点

## 统计（PanoramaDeep.vue，1904 行）

| 指标 | 值 |
|---|---:|
| 含中文行 | **270** |
| 其中模板/HTML 行 | 88 |
| 引号内中文字面量 | 81 |
| 去重后字面量 | **75** |

## 迁移建议

1. **阶段 1**：75 个引号字面量 → `T('pano.<key>', fallback)`（与现有一致）；
2. **阶段 2**：模板静态中文（~88 行含标签）→ 插值 `T()`；
3. **阶段 3**：title/aria 等可访问性文案同步；
4. 每阶段跑 `pnpm vitest run plugins/map-3d/tests` + `tsc --noEmit` + 截图核对。

## 说明

- 未改代码；本盘点只给迁移范围。
- 600 行说法为含脚本注释/模板混合估算；实际 CJK 行为 270。

## 2026-10-24 阶段 1 进展

- `PanoramaDeep.vue`：25 处用户可见字面量改为 `T('pano.*', fallback)`（图层/场景/模式/操作/提示）。
- 验证：map-3d tests 793 passed；tsc --noEmit 0。
- SpaceAI Platform 本地提交 `92c6843`（main，未 push）。
- 剩余：模板静态中文（~88 行）、其余脚本字面量、title/aria。

## 阶段 1 批次 2（2026-10-24）

- 追加迁移：告警分类、NLU 行/说明、实时流注记、飞行高度/停留选项。
- SpaceAI 本地提交 `2c292ce`（main，未 push）。
- 验证：793 tests / tsc 0。

## 阶段 1 批次 3（模板标签，2026-10-24）

- 按钮/选项/placeholder/图例/确认框标签改用 `T()`；
- SpaceAI 本地提交 `86d742d`（main，未 push）；
- 验证：793 tests / tsc 0。

## 阶段 1 批次 4（长文案，2026-10-24）

- 相机/工具提示、NLU placeholder、品牌/大屏、派单/回投确认文案改 T()；
- SpaceAI 本地提交 `06be37a`（main，未 push）；
- 验证：793 tests / tsc 0。

## 阶段 1 批次 5（大屏/最新流，2026-10-24）

- 大屏 ticker、对象/重点/活跃事件/设备、最新事件文案改 T()。
- SpaceAI 本地提交（main，未 push）；793 tests / tsc 0。

## 阶段 1 批次 6（配置/派单/回投，2026-10-24）

- 巡演、配置标题/尺寸/默认、派单表头/目标/类型/接收方/选项/按钮、回投表头/按钮、团队上下文文案改 T()。
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 7（脚本用户文案，2026-10-24）

- 团队任务提示、NLU 未识别说明、卡片标题后缀、星期文案改 T()。
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。
- 模板用户可见文案已基本迁完；剩余为注释/数据键/少量 aria。

## 阶段 1 批次 8（PanoramaCtrl，2026-10-24）

- 工厂/低空/空间检索、快照保存/空态、数据说明、检索空态/覆盖、底图标签改 `ctx.T()`；
- 测试 mock 补 `T`（fallback）以符合 `CtrlCtx` 契约；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 9（PanoramaCtrl 弹层/工具条，2026-10-24）

- 关闭/搜索 placeholder/精度/图层提示/收藏空态/场景过滤/小应用/实时流/语音/CWME 控制台与按钮改 `ctx.T()`；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 10（PanoramaBubbles，2026-10-24）

- 气泡标题按钮/行标签/摄像机/当前画面/AI 输入/派单选项/备注/提交/图片 alt 改 T()；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 11（PanoramaCardColumn，2026-10-24）

- 摘要标签/按钮、历史、组折叠、翻转/配置标题、指数/评分说明、风险/事件/力量/处置/值守/研判标签改 T()；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 12（PanoramaFlyPanel，2026-10-24）

- 飞翔标题/路径/特效、地图打点/名称/智能添加、收藏/巡检/演练航线、采集中心、AI 解析、高度/停留、执行/循环/预览/保存/分享/导入/轨迹/清空、环绕/运镜改 T()；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。

## 阶段 1 批次 13（PanoramaCwmePanel，2026-10-24）

- 面板标题/折叠/停靠/退出、批注/清除/导出 PNG/MD/独立版、回放口径、场景切换、加载/超时/缓存/重试、热力/时点/空态改 T()；
- 793 tests / tsc 0；SpaceAI main 本地提交（未 push）。
