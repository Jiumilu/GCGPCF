---
doc_id: GPCF-DOC-638FE1B07B
title: O3 侧栏统一 —— 证据（F-034，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-034-wae-p0-shell-and-role-convergence/evidence/o3-sidebar-unification.md
source_path: features/done/F-034-wae-p0-shell-and-role-convergence/evidence/o3-sidebar-unification.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# O3 侧栏统一 —— 证据（F-034，2026-10-22）

> 本轮只读盘点：未修改 WAE / WAME 任何仓。跨仓归并不在本轮范围。

## 结论

**partial（现状可核，归并未完成）**：框架侧已有**唯一侧栏实现**（`packages/app-shell/src/GlobalCloudSidebar.tsx`，导航项由使用方 `items` 注入、可选 `subject` 做 L1 过滤；移动端由 `MobileNav.tsx` 承担）；**项目侧（WAME）三套仍独立存在、未归并**，且 WAME 对 `@globalcloud/app-shell` 的引用为 **0**。

## 1. 框架侧（唯一侧栏）

| 文件 | 行数 | 说明 |
|---|---|---|
| `GlobalCloud WAE/packages/app-shell/src/GlobalCloudSidebar.tsx` | 85 | 由 WAES 母本最小改造：硬编码 4 条导航与路径前缀改为 props；**不传 `items` ⇒ 空导航提示**，不内置任何项目导航；`subject` 显式提供时才 `filterMenu`（L1 呈现层，不构成授权事实） |
| `GlobalCloud WAE/packages/app-shell/src/MobileNav.tsx` | — | 移动端：汉堡 Drawer + 底部 Tab（≤5），显式 `capabilities.mobileNav` 或 `navItems` 才启用 |

导出面（供项目侧注入）：
```text
SidebarItem { label, path, icon, requires? }
GlobalCloudSidebarProps { items?, rootPath?, title?, subtitle?, description?, getCurrentPath?, subject? }
```

测试覆盖现状：框架侧栏无独立单测文件；其行为由 `packages/app-shell/src/shell.dom.test.tsx` 间接覆盖（① 空导航提示、② `slots.sidebar` 注入后框架侧栏退场、④ 移动端导航）。**这是现状，不宣称"侧栏已单测完备"**。

## 2. 项目侧（WAME 三套，只读盘点）

| 文件（WAME 仓） | 行数 | sha256(12) | 使用关系 | 是否消费框架侧栏 |
|---|---|---|---|---|
| `src/app/layout/GlobalCloudSidebar.tsx` | 49 | `fefe5daa856b` | 被 `src/app/layout/GlobalCloudShell.tsx` 引用；后者被 `modules/global-cloud-workbench/GlobalCloudWorkbenchModule.tsx` 引用 | **否**（0 处 import `@globalcloud/app-shell`） |
| `src/app/components/FunctionPanel.tsx` | 1557 | `3737de15bde7` | 被 `src/app/components/MainContent.tsx` 引用 | **否** |
| `src/app/components/Sidebar.tsx` | 114 | `f5cb3ab40873` | 全仓检索**未发现 import 方**（疑似遗留件） | **否** |

核对命令：

```bash
cd "GlobalCloud V0.0.1"

# 行数与指纹
wc -l "GlobalCloud WAME/src/app/layout/GlobalCloudSidebar.tsx" \
      "GlobalCloud WAME/src/app/components/FunctionPanel.tsx" \
      "GlobalCloud WAME/src/app/components/Sidebar.tsx" \
      "GlobalCloud WAE/packages/app-shell/src/GlobalCloudSidebar.tsx"
shasum -a 256 "GlobalCloud WAME/src/app/layout/GlobalCloudSidebar.tsx" \
              "GlobalCloud WAME/src/app/components/FunctionPanel.tsx" \
              "GlobalCloud WAME/src/app/components/Sidebar.tsx"

# 项目侧是否消费框架壳
grep -rn "@globalcloud/app-shell" --include=*.tsx --include=*.ts --include=package.json "GlobalCloud WAME" | grep -v node_modules
# → 无输出（0 处）

# WAME 三套的引用关系
grep -rn "from './GlobalCloudSidebar'" --include=*.tsx "GlobalCloud WAME/src"
# → src/app/layout/GlobalCloudShell.tsx:3: import GlobalCloudSidebar from './GlobalCloudSidebar';
grep -rn "Sidebar" --include=*.tsx --include=*.ts "GlobalCloud WAME/src" | grep -v GlobalCloudSidebar | grep -v SidebarItem
# → 未发现 src/app/components/Sidebar.tsx 的 import 方
```

## 3. 判定口径与限制

- 「框架侧唯一侧栏」成立：WAE 仓内没有第二套侧栏实现（`GlobalCloudSidebar.tsx` 唯一；移动端为 `MobileNav.tsx`，职责不同）。
- 「项目侧三套未归并」为**当前事实**：三套皆为 WAME 本地实现，未接入框架 `items` 注入接口，WAME 对框架壳包 0 引用。
- 本轮**不跨仓修改 WAME**（属主项目执行）；也不做视觉一致性验证。
- `src/app/components/Sidebar.tsx` 判定"疑似遗留"依据是静态 import 检索为 0，**不排除**通过字符串/动态路径加载的隐式引用；如 WAME 属主确认在用，请以属主口径为准。
- 未修改任何文件；未 commit/push。
