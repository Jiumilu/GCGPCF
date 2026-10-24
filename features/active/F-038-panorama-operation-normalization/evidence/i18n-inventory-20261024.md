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
