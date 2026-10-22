---
doc_id: GPCF-DOC-F036-EVIDENCE-20261022
title: F-036 PKC 在 WAE 的注册与首批接入演练 —— 证据摘要
project: GPCF
related_projects: [WAE, PKC, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-036-wae-pkc-intake-integration/evidence/summary.md
source_path: features/active/F-036-wae-pkc-intake-integration/evidence/summary.md
sync_direction: local_only
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# F-036 PKC 接入（候选）—— 证据摘要（2026-10-22）

> 性质：**候选接入 / 受控嵌入预演**。只改 WAE 登记侧与入口页；**未改 PKC 仓**业务代码；**不声明 PKC 已接入 / 已集成 / 生产就绪 / 客户验收**。
> 依据：`docs/harness/evidence/pg12-implementation-plan-*.md` 无直接依赖；本 F 依据 F-034 的 `pkc-intake-protocol-20261022.md`（P0–P7 协议）与 WAE 落位/装配规范。

## 1. 结论

- WAE 侧 **PKC 注册已落位（候选）**：`placement.city.yaml` 新增一级应用 `pkc` + 页入口 `pkc-intake`（`requires: pkc`，`source: page`）；`pnpm gen:apps` 已重新生成 `generated.ts`。
- 入口页 `PkcIntakePage.tsx` 以**候选态 + 非声明 + 受控嵌入预演**呈现；默认不发起 PKC 运行时请求；配置 `VITE_PKC_EMBED_URL` 后需人工触发且 iframe 带 sandbox。
- 菜单/权限：`menus.ts` 新增 `pkc` 菜单项（`system-admin/operator/strategist/studio` 可见；viewer/auditor 不可见），并有单测守护。
- 登记层：新增 `docs/assembly-spec/manifests/pkc-intake.yaml`（来源/入口/适配级别/回滚/非声明）。
- 全部 WAE 门禁与测试通过：`check:apps`、`gen:apps --check`、`check:app-assembly`、`typecheck`、根 `test`、`apps/wame test`、`build`；`ui_gate` C10 有效 0。
- **task_flow E2E（2026-10-22 追加，run3 复跑）**：WAE 属主补 `useAppContent.ts` 的 `import { CONSOLE_COLORS }` 后，**原始 dev（无垫片）真实跑通** —— 登录（首登改密）→ 应用壳 → 侧栏 `PKC 知识工作台`（requires pkc）→ `pkc-intake` 候选页（候选态/非声明/机器字段不上屏/受控嵌入 0 外部请求）→ 返回工作台，**10 步 / pageErrors=0 / externalRequests=0**；`task_flow_e2e_status = pass`。详见 `evidence/e2e-20261022/README.md`。
- **未完成**：PKC 仓的令牌（P4）与状态语义（P5）接入、PKC 真实运行时嵌入验收、WAE 一行 import 修复后的无垫片 E2E 重跑 —— 见 §5 阻塞。

## 2. 改动文件（WAE 仓；工作区改动，未 commit/push）

| 文件 | 类型 | 改动 |
|---|---|---|
| `docs/assembly-spec/placement.city.yaml` | 改 | apps 新增 `pkc`（label PKC 知识工作台，icon BookOpenText，order 40）；entries 新增 `pkc-intake`（page、home、requires pkc、source page） |
| `apps/wame/src/app/apps/generated.ts` | 改（生成物） | `pnpm gen:apps` 重新生成：应用 5 / 条目 21 |
| `apps/wame/src/app/apps/pageComponents.tsx` | 改 | 登记页面组件 `pkc-intake → PkcIntakePage` |
| `apps/wame/src/app/apps/PkcIntakePage.tsx` | 新增 | 候选接入入口页：状态徽章、边界/非声明、受控嵌入预演（sandbox iframe，需人工触发）、回滚说明；不暴露机器字段 |
| `apps/wame/src/app/apps/PkcIntakePage.dom.test.tsx` | 新增 | 5 例：候选态/非声明、默认无 iframe、机器字段不上屏、embed 需人工触发、未认证不崩溃 |
| `apps/wame/src/app/apps/AppsShell.tsx` | 改 | ICONS 增 `BookOpenText`（pkc 一级入口图标；未知图标回落 LayoutGrid） |
| `apps/wame/src/app/apps/AppsShell.dom.test.tsx` | 改 | 菜单夹具加 `pkc`；一级应用 4+1、移动端 5 项；角色收敛断言加 pkc（viewer 不可见 / system-admin 可见） |
| `packages/host-kit/src/host/menus.ts` | 改 | 新增 `pkc` 菜单项与 `requires`（system-admin/operator/strategist/studio） |
| `packages/host-kit/src/host/menus.test.ts` | 改 | 新增 pkc 菜单存在性与角色收敛断言 |
| `docs/assembly-spec/manifests/pkc-intake.yaml` | 新增 | PKC 接入模块清单（候选）：来源/技术栈/entry/适配 L2/回滚/非声明，status=candidate |

> 未改 PKC 仓；未改 WAE 的 `assembly.city.yaml`（page 形态入口不进入模块装配集，`check:app-assembly` 一致）。
> 注：`placement.city.yaml` / `generated.ts` / `AppsShell.dom.test.tsx` 同文件内含前一任务（F-034 角色收敛）的未提交改动，本次在其上叠加，未回退。

## 3. 验证命令与真实结果（WAE 仓）

| # | 命令 | 结果 |
|---|---|---|
| 1 | `pnpm check:apps` | pass（P001–P010 全部通过；一级菜单 sidebar 4 项，第 4 项 = PKC，服务应用 7 个二级） |
| 2 | `pnpm gen:apps --check` | pass（2 个生成物最新；应用 5 / 条目 21 / 模块包 19） |
| 3 | `pnpm check:app-assembly` | pass（装配 18 / 落位 21（可见 20 / 隐藏 1）/ 加载器 18；两侧交集 18；A1–A4 一致） |
| 4 | `pnpm typecheck` | pass（exit 0） |
| 5 | `pnpm --filter @globalcloud/wame typecheck` | pass（exit 0） |
| 6 | `pnpm test`（根） | **132 files / 1379 tests passed** |
| 7 | `pnpm --filter @globalcloud/wame test` | **15 files / 98 tests passed**（含 PkcIntakePage 5 例、AppsShell 15 例） |
| 8 | `pnpm --filter @globalcloud/wame exec vitest run src/app/apps/AppsShell.dom.test.tsx src/app/apps/PkcIntakePage.dom.test.tsx` | 2 files / **20 tests passed** |
| 9 | `pnpm build` | pass（仅 >500 kB chunk 体积警告，非阻断） |
| 10 | `python3 _governance/drafts/ui-spec/tools/ui_gate.py "GlobalCloud WAE"` | C1 有效 0；C5 状态字典存在；**C10 治理字段暴露原始 3 / 白名单 3 / 有效 0**；C9 0 |
| 11 | `python3 _governance/tools/gc_standard.py check --repo "GlobalCloud WAE" --fail-on error` | exit 0（error 0） |

> ui_gate `--strict` 当前 exit 1 的成因是**既有** C2 z-index 计数 1（非本次改动新增；本页/本次 diff 未引入 z-index）。如实记录，不粉饰。

## 4. UI gate 六件套（本 Feature 范围）

| gate | 取值 | 证据 |
|---|---|---|
| `functional_completeness` | pass | 注册 + 入口页 + 菜单收敛 + 测试（§3 全部通过） |
| `quality_baseline` | pass | check:apps / gen:apps --check / check:app-assembly / typecheck / test / build / ui_gate C1/C9/C10 有效 0 |
| `multi_user_usability` | **pass（2026-10-22 评审准备补充）** | 隔离临时 IdP 双角色：system-admin 侧栏可见 `app-nav-pkc`；viewer `/me` menus=`[overview, feedback-center, scene, pqc-sop]`（无 pkc）、侧栏 PKC 入口计数 0。证据 `evidence/review-20261022/`（断言 JSON + 截图） |
| `task_flow_e2e_status` | **pass** | run3 原始 dev（无垫片）真实通过：10 步全过、pageErrors=0、externalRequests=0、consoleErrors=1（登录前 /me 401 预期）；前置=WAE 补 `CONSOLE_COLORS` import（`tsc --noEmit` pass）。证据 `evidence/e2e-20261022/` |
| `accessibility_status` | **pass（含 shell 级风险，2026-10-22 评审准备补充）** | pkc 页 h1/aria 正常、页内可交互元素可访问名缺失 0；键盘焦点可见、16 步 Tab distinct=14/无陷阱。风险：AppsShell 无 `<main>` landmark（R-A11Y-1）、shell 1 个未命名按钮（R-A11Y-2），需 WAE 属主修复或评审豁免。证据 `evidence/review-20261022/` |
| `evidence_overexposure_gate` | pass | 入口页不暴露机器字段（DOM 测试断言 packageId/evidenceRefs/contentDigest 等不上屏）+ ui_gate C10 有效 0 |

`status_ceiling` 保持 `partial`（task_flow pending + PKC 侧未接入）。

## 5. 阻塞 / 未完成（真实登记）

1. **PKC 侧令牌与状态语义（协议 P4/P5）**：PKC 仓 `theme.css` 仍为本地实现（`--gc-*` 0 次）、`ui_gate C5` 未发现统一状态字典；需 PKC 属主执行，本任务未改 PKC 仓。
2. **PKC 真实运行时嵌入未验收**：未配置 `VITE_PKC_EMBED_URL`、未做真实 iframe 联调；默认保持预演，不发起请求。
3. **任务流 E2E**：无浏览器端到端证据，`task_flow_e2e_status` 保持 pending。
4. **正式接入评审**：WAE/PKC 属主评审、MMC/身份 403 对齐尚未进行；本 Feature 不声明已接入。

## 6. 回滚

```bash
# WAE 仓：移除登记 + 重新生成（入口消失）
git -C "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud WAE" restore -- \
  docs/assembly-spec/placement.city.yaml \
  apps/wame/src/app/apps/generated.ts \
  apps/wame/src/app/apps/pageComponents.tsx \
  apps/wame/src/app/apps/AppsShell.tsx \
  apps/wame/src/app/apps/AppsShell.dom.test.tsx \
  packages/host-kit/src/host/menus.ts \
  packages/host-kit/src/host/menus.test.ts
rm -f "…/GlobalCloud WAE/apps/wame/src/app/apps/PkcIntakePage.tsx" \
      "…/GlobalCloud WAE/apps/wame/src/app/apps/PkcIntakePage.dom.test.tsx" \
      "…/GlobalCloud WAE/docs/assembly-spec/manifests/pkc-intake.yaml"
# 或最小回滚：从 placement 删除 pkc app/entry 后 pnpm gen:apps（入口消失，代码可保留）
```

无数据迁移、无外部写入、无部署、无权限变更；回滚只影响 WAE 登记侧。

## 7. 非声明

- 不声明 PKC 已接入 / 已集成 / `accepted` / `production_ready` / `customer_accepted`。
- 不声明 PKC 仓业务代码被 WAE 侧改写；不声明真实运行时嵌入已验收。
- 未 commit / push；未关闭 Feature。

## 8. task_flow E2E（2026-10-22 追加）

- **口径**：真实浏览器（Playwright + system Chrome）、真实登录（隔离临时 IdP，口令仅 env）、真实产品 UI，无 mock；环境 `:4301`（4300 被其它会话占用，未终止他人实例）。
- **run1（原始 dev，无垫片）→ fail**：登录/改密通过，随后白屏 `CONSOLE_COLORS is not defined`（WAE HEAD `41ce842` 在 `apps/wame/src/app/hooks/useAppContent.ts` 漏 `import { CONSOLE_COLORS } from './consolePalette'`；与本 Feature 无关）。截图 `screens/f036-run1-raw-fail-wae-console-colors-error.png`。
- **run2（同流程 + 文档化常量垫片）→ PKC 链路 pass**：10 步全过（登录 → 壳 → 侧栏 PKC 入口 → pkc-intake 候选页 → 候选态/非声明/机器字段不上屏/受控嵌入 0 外部请求 → 返回工作台）；`pageErrors=0`，`externalRequests=0`，`consoleErrors=1`（登录前 `/me` 401 会话探测，属预期）。截图 `screens/f036-flow-01…06*.png`，断言 `logs/run2-with-shim/taskflow-assertions.json`。
- **Gate 取值**：`task_flow_e2e_status = fail`（原始产品 dev 不通过，不把垫片运行当作"真实通过"）。
- **解锁**：WAE 属主在 `useAppContent.ts` 补一行 import → 删除 spec 内垫片 → 重跑 `evidence/e2e-20261022/run-e2e.sh` → 全绿后改 `pass`。
- **清理**：4301 已停（0 listener；4300 他人实例未动）、`/tmp/f036-e2e-idp` 已删、软链与 `WAE test-results/` 已删、证据无凭据（`F036a!/F036b!` grep=0）。详见 `evidence/e2e-20261022/README.md`。

### run3（import 修复后复跑 —— 当前 gate 依据）

- **前置**：WAE 工作区已补 `apps/wame/src/app/hooks/useAppContent.ts` 的 `import { CONSOLE_COLORS } from './consolePalette';`（未提交修复，由 WAE 属主完成；`tsc --noEmit` pass）；spec 内临时垫片已删除。
- **运行**：`bash evidence/e2e-20261022/run-e2e.sh`（隔离临时 IdP + WAE dev :4301 + Playwright 原始 dev，无垫片）→ `PLAYWRIGHT_EXIT=0`。
- **结果**：10 步全过（登录+首登改密 → 应用壳 → 侧栏 PKC 入口 → pkc-intake 候选页 → 候选态/非声明/机器字段不上屏/受控嵌入 0 外部请求 → 返回工作台）；`pageErrors=0`、`externalRequests=0`、`consoleErrors=1`（登录前 `/me` 401 预期）。
- **证据**：`screens/f036-flow-01…06*.png`（run3）、`logs/run3-raw-dev-pass/`（taskflow-assertions.json / playwright-run.log / dev-server.log / run-meta.json）；历史 run1（fail）与 run2（垫片 pass）保留在 `screens/run1-raw-fail|run2-with-shim/`、`logs/run1-raw-fail|run2-with-shim/`。
- **Gate**：`task_flow_e2e_status = pass`（原始 dev 真实通过，无垫片）。
- **依赖提醒**：若 WAE 的 `CONSOLE_COLORS` import 修复被回退，本 gate 会回退 fail（run1 可复现）。

## 9. 正式接入评审准备（2026-10-22 追加）

- 六门映射、证据链接、风险/豁免与评审建议见 `evidence/review-20261022/README.md`（评审建议：**conditional**）。
- 本轮新增真实证据：multi_user（A=system-admin 可见 PKC 入口 / B=viewer menus 无 pkc 且侧栏入口 0）、accessibility（键盘焦点可见/aria/无陷阱）、WAE 五项门禁复跑（check:apps / gen:apps --check / typecheck / test 1379 / build 全部 pass）。
- 关键风险：R-A11Y-1（AppsShell 无 `<main>` landmark）与 R-A11Y-2（TopTabs 关闭按钮未命名）**已于 2026-10-22 修复并复跑验证**（mainCount=1 / shellUnnamedCount=0 / 无陷阱；WAE typecheck/test(1379)/build pass）；R-DEP-1（E2E 依赖 WAE 未提交 import 修复）、R-PKC-1（P4/P5）已最小接入（gc 令牌快照 + C5 StatusBadge，ui_gate C6 0→117、C5 存在），残留见 PKC evidence；详见评审 README §6。
- 不声明已接入/状态提升；Feature 未关闭。
