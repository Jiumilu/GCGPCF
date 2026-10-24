---
doc_id: GPCF-DOC-F023-COMPAT-WINDOW-20261024
title: F-023 兼容窗口决策（2026-10-24）
project: GPCF
related_projects: [WAS]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# F-023 兼容窗口决策

## 决策

- 兼容窗口在**下一次 WAS minor 版本发布时关闭**（由 WAS 属主发布时执行）。
- 窗口内允许旧流名仅存在于：
  - `okf/schemas/*`（兼容枚举/旧字段）
  - `okf/validators/*`（DEPRECATED_FLOWS 兼容校验）
  - `okf/was/deprecations.yaml`（迁移表/说明）
- **数据文件**（`okf/was/*`、examples、fixtures）继续禁止旧流名。

## 验证

- WAS `okf` 数据文件旧名扫描：0 处（仅 schemas/validators/deprecations 命中）。
- GPCF tools/scripts/tests/fixtures 旧名扫描：0 处。
- scenario matrix validator：flows=9/9 pass。

## 非声明

- 不声明 WAS 新版本已发布；窗口关闭时点由 WAS 属主执行。
