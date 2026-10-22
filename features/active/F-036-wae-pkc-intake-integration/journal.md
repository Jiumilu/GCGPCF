---
doc_id: GPCF-DOC-F036-JOURNAL
title: F-036 wae-pkc-intake-integration
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/journal.md
source_path: features/active/F-036-wae-pkc-intake-integration/journal.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-036 wae-pkc-intake-integration

## LOOP 日志

### Iteration 0

1. 这轮做什么？
   - 创建 Feature Workspace。
2. 改了什么？
   - 初始化 feature.yaml、journal.md、evidence/、artifacts/。
3. 怎么验证？
   - 关闭前运行 gpcf_check_evidence.py。
4. 发现什么问题？
   - none
5. 是否可以提交？
   - 否，Evidence Gate 仍待验证。

## 2026-10-22 实施记录（F-036 · agent，未 commit/push）

- 改动：WAE `placement.city.yaml` 注册 pkc 一级应用 + pkc-intake 页入口（requires pkc）、`gen:apps` 重生成、`pageComponents.tsx` 登记、`PkcIntakePage.tsx`（候选态/非声明/受控嵌入预演）+ DOM 测试、`AppsShell` 图标与测试夹具、`menus.ts` 菜单与单测、`manifests/pkc-intake.yaml`。
- 验证：check:apps / gen:apps --check / check:app-assembly / typecheck / 根 test 132 files/1379 / apps/wame test 15 files/98 / build 全部 pass；ui_gate C10 有效 0；gc_standard error 0。
- 阻塞：PKC 仓令牌/状态语义（P4/P5）待 PKC 属主；真实受控嵌入未联调；任务流 E2E pending；正式接入评审未做。
- 结论：WAE 侧注册与入口落位完成（候选），不声明 PKC 已接入；不关闭 Feature。

## 2026-10-22 task_flow E2E（task-28 · agent，未 commit/push）

- 环境：WAE dev `:4301`（4300 被其它会话占用，未终止他人实例）+ 隔离临时 IdP `/tmp/f036-e2e-idp`（bootstrap 唯一 system-admin，口令仅 env）；Playwright（WAE apps/wame 安装 + system Chrome，复用 F-010 配置模式）。
- run1 原始 dev → fail：登录/改密通过后白屏 `CONSOLE_COLORS is not defined`（WAE HEAD 41ce842 在 `useAppContent.ts` 漏 import；与本 Feature 无关）。
- run2 同流程 + 文档化常量垫片（逐字同 consolePalette.ts）→ PKC 链路 pass：10 步全过，`pageErrors=0`、`externalRequests=0`、`consoleErrors=1`（登录前 `/me` 401 预期）。
- 决定：`task_flow_e2e_status=fail`（不把垫片运行当作真实通过）；解锁=WAE 补一行 import 后删垫片重跑。
- 证据：`evidence/e2e-20261022/`（README、run-e2e.sh、config、spec、screens、logs）；清理确认：4301 已停、临时 IdP/软链/WAE test-results 已删、证据 grep 凭据=0。

## 2026-10-22 task_flow E2E 复跑（task-29 · agent，未 commit/push）

- 前置：WAE 属主已补 `apps/wame/src/app/hooks/useAppContent.ts` 的 `import { CONSOLE_COLORS }`（未提交工作区修复，tsc pass）；删除 spec 内临时常量垫片，归档垫片版 spec 至 `evidence/e2e-20261022/logs/run2-with-shim/*.txt`（testMatch 只跑主 spec）。
- run3（原始 dev，无垫片）→ **pass**：`PLAYWRIGHT_EXIT=0`；10 步全过，`pageErrors=0`、`externalRequests=0`、`consoleErrors=1`（登录前 `/me` 401 预期）。
- Gate：`task_flow_e2e_status = fail → pass`；依赖 WAE import 修复不被回退（回退则 run1 可复现 fail）。
- 证据：`evidence/e2e-20261022/screens/f036-flow-*.png`、`logs/run3-raw-dev-pass/`；README v1.1 与 evidence/summary §8 已更新。
- 清理：4301 已停（0 listener）、`/tmp/f036-e2e-idp` 已删、node_modules 软链已删、WAE test-results 已删、无实际口令入证据。

## 2026-10-22 正式接入评审准备（task-31 · agent，未 commit/push）

- 新增证据目录 `evidence/review-20261022/`（README 六门映射/风险/建议 + run-review.sh + config/spec + screens×4 + review-assertions.json + WAE 门禁记录）。
- multi_user：隔离临时 IdP 双角色（A=system-admin bootstrap、B=viewer 由 A 经 POST /api/idp/users 建号）；A 侧栏可见 `app-nav-pkc`；B `/me` menus 无 pkc 且侧栏 PKC 入口计数 0 —— **pass**。
- accessibility：pkc 页 h1/aria 正常、页内 unnamed=0；键盘焦点可见（app-nav-pkc outline+ring）、16 步 Tab distinct=14 无陷阱 —— **pass（含 shell 级风险 R-A11Y-1 无 `<main>` landmark、R-A11Y-2 1 个未命名控件）**。
- WAE 门禁复跑：check:apps / gen:apps --check / typecheck / test(1379) / build 全 exit 0（记录 `logs/wae-checks.log`）。
- gates：multi_user_usability waived→pass、accessibility_status waived→pass；六门现全部 pass；评审建议 **conditional**。
- 清理：4301 已停（0 listener）、4300 他人实例未动、/tmp 与 node_modules 软链已删、证据无实际口令。

## 2026-10-22 WAE shell a11y 修复（task-32 · agent，未 commit/push）

- 定位（不靠猜）：扩 F-036 review a11y 探针输出 shellUnnamedList，锁定唯一未命名控件 = `TopTabs.tsx` 项目标签关闭按钮（`<Button size="icon"><X/></Button>`，hover 才显示；父 class `flex items-center min-w-0 max-w-64 group bg-background border-b-2 border-cyan-600`）。
- 修复（只改 aria/landmark，不改行为）：① `apps/wame/src/app/apps/AppsShell.tsx` 内容区 `<section>`→`<main>`（class 保留、闭合同步）；② `apps/wame/src/app/components/TopTabs.tsx` 关闭按钮补 `aria-label="关闭项目标签：<title>"`。
- 复跑指标（`evidence/review-20261022/run-review.sh`）：`mainLandmark=true`、`mainCount=1`（无重复 main）、`shellUnnamedCount=0`、`pageUnnamed=[]`、`keyboardReachedPkc=true`、`navFocusVisible=true`、`trap=false`、`distinct=14`、`pageErrors=0`。
- WAE 门禁复跑：typecheck pass、test 132 files/1379 pass、build pass（记录 `evidence/review-20261022/logs/wae-checks.log` 末节）。
- 证据更新：`evidence/review-20261022/README.md` R-A11Y-1/2 标已修复并附新日志/截图路径；F-036 gates 仍全 pass。
- 清理：4301 已停（0 listener；runner 已加预检+精确收尾防残留）、4300 他人实例未动、临时 IdP/软链已删；未 commit/push。
