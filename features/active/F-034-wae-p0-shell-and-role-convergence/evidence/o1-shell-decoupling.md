---
doc_id: GPCF-DOC-AD66B8830A
title: O1 外壳解耦 —— 证据（F-034，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-034-wae-p0-shell-and-role-convergence/evidence/o1-shell-decoupling.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/o1-shell-decoupling.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# O1 外壳解耦 —— 证据（F-034，2026-10-22）

> 本轮为只读检查：未修改 WAE 仓代码。命令均在 `GlobalCloud WAE` 仓根执行。

## 结论

**pass（有代码 + 有测试 + 有可回放命令输出）**：框架壳把「项目专属机件」下沉为能力开关（`capabilities`，除安全网 `errorBoundary` 外**默认全关**），项目内容一律经由 `slots` 注入；框架自带导航默认空，不串 WAME 文案。

## 1. 代码路径

| 文件 | 职责 |
|---|---|
| `packages/app-shell/src/shellCapabilities.ts` | 能力键清单（`SHELL_CAPABILITY_KEYS` 7 键）、默认开启集合（`DEFAULT_ON_CAPABILITY_KEYS = ['errorBoundary']`，唯一安全网例外）、`resolveCapabilities()`、`resolveShellSlots()`、`describeShellComposition()` |
| `packages/app-shell/src/GlobalCloudShell.tsx` | 壳本体：只组装「顶栏 + 侧栏（或 slots.sidebar）+ 内容区」；`titleBar` 仅 `capabilities.titleBar` 显式开启时渲染；`errorBoundary` 默认开包裹内容区 |
| `packages/app-shell/src/GlobalCloudSidebar.tsx` | 框架侧侧栏：`items` 默认空（不内置项目导航），`subject` 提供时才做 L1 过滤 |
| `packages/app-shell/src/index.ts` | 公开导出（测试断言的是公开包入口） |

关键代码事实（静态核对）：

```text
SHELL_CAPABILITY_KEYS = titleBar / functionPanel / rightAIAssistant / wasmMonitor / performanceMonitor / projectPersistence / errorBoundary
DEFAULT_ON_CAPABILITY_KEYS = ['errorBoundary']   # 唯一默认开；仅框架安全网
resolveShellSlots() 空入参 → sidebar/rightPanel/titleBarExtra 均为 undefined
describeShellComposition() 空入参 → isCleanFrameworkShell = true
```

## 2. 可回放命令与输出

```bash
cd "GlobalCloud WAE"

# ① 能力开关/槽位契约（纯函数，node）
npx vitest run packages/app-shell/src/shellCapabilities.test.ts
# ✓ |node| packages/app-shell/src/shellCapabilities.test.ts (9 tests)
# Test Files  1 passed (1) / Tests  9 passed (9)

# ② 壳 DOM 行为（jsdom，断言公开包入口）
npx vitest run packages/app-shell/src/shell.dom.test.tsx
# ✓ |dom| packages/app-shell/src/shell.dom.test.tsx (8 tests)
# Test Files  1 passed (1) / Tests  8 passed (8)
```

`shellCapabilities.test.ts`（9 例）关键断言：

```text
✓ ① 不传 capabilities → 项目机件全关；仅 errorBoundary 默认开
✓ ① 只有显式 true 才算开（false / 缺省一律关）；默认开的键可显式关
✓ ① 能力键清单稳定（顺序固定，便于审计）
✓ ② 空入参 → 三个槽位都不渲染
✓ ② 空入参 → 组合摘要判定为「干净的框架壳」（默认安全网不计入项目内容）
✓ ② 传了任意一样 → 不再是干净框架壳（可被自检发现）
✓ 槽位与旧写法等价：旧写法 aiPanel ≡ slots.rightPanel
✓ **开了能力也不臆造节点**：无节点则右侧面板仍为 undefined
```

`shell.dom.test.tsx`（8 例）关键断言：

```text
✓ ① 不传 props：只渲染框架壳 + 空导航提示；全页无 WAME/PVAOS/Command Center/MMC/GPCF/ICP/AaaS 文案
✓ ② slots.sidebar 注入的节点被摆放，框架自带侧栏退场
✓ ③ children 抛错 ⇒ 内容区错误卡片（错误信息 + 重载按钮），侧栏与顶栏仍在
✓ ④ 移动端导航（桌面侧栏全部项 / <md 汉堡+底部 Tab / slots.sidebar 优先）
✓ ⑤ 搜索面板默认不带假热度（未传 popularSearches 时不渲染"热门搜索"）
```

## 3. 判定口径与限制

- 判定依据 = 代码不变量（默认全关 + slots 显式注入）+ 单元/DOM 测试 + 命令真实退出码 0；三者一致。
- 限制：DOM 测试在 jsdom 中运行，未做真实浏览器截图；O1 的"视觉无回归"不在本证据范围。
- `errorBoundary` 默认开是**有意例外**（框架安全网），不计入"项目专属内容"；判据见 `describeShellComposition().isCleanFrameworkShell`。
- 未修改任何 WAE 代码；未 commit/push。
