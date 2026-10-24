---
doc_id: GPCF-DOC-F034-OWNER-PACK-20261024
title: F-034 属主动作包
project: GPCF
related_projects: [WAE, PKC, Brain, PVA, Studio]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# F-034 属主动作包

## 已由 GPCF/老卢完成

- PKC `--gc-*` 别名层例外 approved；
- PVA（PVAOS）路径映射 + 1 处差异例外 approved。

## 需属主动作

| 项目 | 动作 | 证据 |
|---|---|---|
| Brain | 裁定 25 处差异 + 5 独有令牌（对齐或受控例外） | `brain-token-diff-20261024.md` |
| Studio | `PageSidebarNav.vue` 接入 app-registry `sidebarContract` 或登记例外 | `project-side-sidebar-inventory-20261024.md` |
| PKC | `ui/sidebar.tsx` 接入契约或登记例外；M3 7 项 | 同上 |
| Brain | 侧栏契约或例外 | 同上 |
| WAE/PKC | 运行时 task_flow / evidence_overexposure 证据 | F-034 evidence |

## 签完后 GPCF 动作

1. 更新 O2/O3/M3 blockers 与 resolved 证据；
2. `python3 scripts/gpcf_check_evidence.py --check-only F-034`；
3. 关闭需授权；
4. 不声明 status done。

## 风险

- 令牌差异可能是刻意主题，禁止直接批量替换；
- 侧栏合并涉及各项目 UI，需各自测试与截图。
