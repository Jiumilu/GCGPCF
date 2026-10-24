---
doc_id: GPCF-DOC-F038-I18N-INVENTORY-20261024
title: F-038 i18n 存量盘点（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
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
