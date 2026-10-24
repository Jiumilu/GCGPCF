---
doc_id: GPCF-DOC-F034-SIDEBAR-INVENTORY-20261024
title: 项目侧侧栏实现盘点（2026-10-24）
project: GPCF
related_projects: [WAE, Studio, PKC, Brain, PVAOS]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# 项目侧侧栏实现盘点

| 仓 | 侧栏实现 | 是否消费 app-registry 契约 |
|---|---|---|
| WAE | `apps/wame/src/app/components/sidebarPlugin.ts` + `PluginSidebarItems.tsx`；apps 壳统一导航 | 是（sidebarContract） |
| WAME | 已由 F-035 收敛，消费 app-registry | 是 |
| Studio | `packages/client/src/components/layout/PageSidebarNav.vue`（自有） | 否 |
| PKC | `src/app/components/ui/sidebar.tsx`（shadcn 原语） | 否 |
| Brain | `src/app/components/ui/sidebar.tsx`（shadcn 原语） | 否 |
| PVAOS | 未检出独立 Sidebar 组件 | — |

## 结论

- WAE/WAME 侧已统一为侧栏插件 + 契约；**项目侧（Studio/PKC/Brain）仍是各自实现**，未消费 `sidebarContract`。
- O3 的剩余工作属 Studio/PKC/Brain 属主：接入 app-registry 契约或登记受控例外。
- 不建议 GPCF 跨仓改写其 UI。

## 非声明

- 不声明侧栏已统一；不声明 F-034 可关闭。
