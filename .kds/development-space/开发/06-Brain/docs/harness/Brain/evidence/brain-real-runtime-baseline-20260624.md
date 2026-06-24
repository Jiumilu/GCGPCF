---
doc_id: GPCF-DOC-BRAIN-REAL-RUNTIME-BASELINE-20260624
title: Brain 真实运行基线证据 2026-06-24
project: Brain
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, MMC]
domain: docs
status: controlled
version: v1.0
owner: Brain
kds_space: 开发
kds_path: 开发/06-Brain/docs/harness/Brain/evidence/brain-real-runtime-baseline-20260624.md
source_path: docs/harness/Brain/evidence/brain-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Brain 真实运行基线证据 2026-06-24

## 1. 证据范围

本证据记录 Brain 在核心链路 `WAES -> XWAIL -> AaaS -> GFIS/GPC/PVAOS -> KDS/Brain` 中的真实研发、构建、运行健康和 KDS 边界验证结果。

本记录不把单元测试通过声明为真实运行完成，不把历史 harness 文档声明为当前运行健康完成，不把候选推理能力声明为客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 项目路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud Brain` |
| 依赖状态 | `node_modules_present` |
| 工作树状态 | 存在未跟踪总体方案与实施方案、`tools/`，本轮未回滚 |
| 采集时间 | 2026-06-24 |

## 3. 已执行命令

| 命令 | 结果 | 证据结论 |
|---|---|---|
| `npm run lint` | pass，`eslint src/` 无错误输出 | 静态检查通过 |
| `npm run typecheck` | pass，`tsc --NoEmit` 通过 | 类型检查通过 |
| `npm run test` | pass，`21 passed (21)`、`208 passed (208)` | 单元测试通过 |
| `npm run build` | pass，Vite `2100 modules transformed`，构建完成 | 前端构建通过 |
| `npm run validate:runtime-health` | 初次 fail，`ECONNREFUSED 127.0.0.1:5175`；启动 `npm run dev:local` 后 pass，最新 `brain_status=200`、`kds_total_pages=2732` | Brain dev server 运行健康已形成当前证据 |
| `npm run validate:browser-runtime-smoke` | pass，C 口径对齐后输出 `brain_browser_runtime_smoke=pass`、`status=pass_with_boundaries` | 浏览器只读 smoke 与 team 读写分层边界已通过 |
| `npm run validate:browser-user-flow` | pass，`brain_browser_user_flow=pass`、`checks=21`、`status=pass_with_boundaries` | 浏览器用户流已按 C 口径刷新 |
| `npm run validate:read-closure-matrix` | pass，`read_closure_workflow_count=17`，`search.vector-query` 以 vector limited + same-space keyword degrade 边界闭合 | 读闭包矩阵通过，不声明写回闭合 |
| `npm run validate:target-panel-runtime-matrix` | pass，`target_panels=12 api_read_panels=10 preview_read_panels=1 registry_read_panels=1 prompt_invoked=false confirm_execution_api_invoked=false` | 目标面板运行矩阵通过 |
| `npm run validate:target-panel-data-quality` | pass，`checks=30 usable=30 limited=0 empty_but_valid=0 status=pass_with_data_quality_boundaries` | 目标面板数据质量通过 |
| `npm run validate:chinese-gates` | pass，`search_results=5`、`first_title=襄阳汉江石膏_葛化项目招标协同_20260518` | 中文 API/UI/只读授权边界通过 |
| `npm run format:check` | pass，两个 Brain 方案文档 Prettier 修正后 `All matched files use Prettier code style!` | 格式门禁通过 |
| `npm run validate:completion-matrix` | fail，剩余 `status-audit`、`bulk-fix acceptance execution`、`chat LLM boundary` 等授权型证据刷新问题 | completion matrix 仍不可升级 |
| `npm run validate:harness-evidence` | fail，仍依赖 completion/status/bulk-fix/chat 等证据刷新 | harness evidence 不可信任为当前完成 |
| `npm run validate:loop-harness` | fail，继承 `validate:harness-evidence` 失败 | Loop harness 不可升级 |
| `Chrome Playwright live browser observation` | pass，系统 Chrome 打开 `http://127.0.0.1:5175/` 并读取页面可见文本 | 形成当前浏览器可见信号，并已传导到 `browser-runtime-smoke` C 口径 |

## 4. 当前浏览器可见信号候选证据

本轮使用系统 Chrome 的 Playwright channel 进行真实页面读取。Playwright 自带 Chromium 缓存缺失，因此未使用 bundled Chromium；也没有把 Chrome 观察伪装成 Safari Computer Use。

| 检查项 | 当前可见信号 | 结论 |
|---|---|---|
| Dashboard personal | `总览 (personal)`、`KDS API`、`totalPages=2732`、`graphNodes=280`、`graphEdges=1085` | pass |
| Search personal idle | `KDS GRAPH 浏览`、`personal`、`KDS graph browse`、未展示本地 wikiPages fallback 文案 | pass |
| Search personal query | 查询 `GlobalCloud 绿色供应链` 后显示 `8 个结果 · personal · KDS 关键词搜索 · KDS API`，结果含 `绿色供应链`、`工业绿链` 等 KDS 实时结果 | pass |
| Chat/settings registry | 页面显示 `MMC LLM · 8`、LLM 输入与授权 checkbox 未勾选；本轮未发送 prompt | pass_registry_only |
| Team space | 当前显示 `总览 (team)`、`KDS API`、`totalPages=2732`、`graphNodes=132`、`graphEdges=192`，Search 显示 `KDS GRAPH 浏览 team` | confirmed_c_read_write_split |

候选解释：

```text
brain_chrome_browser_visible_signals = confirmed
brain_team_authorization_contract = confirmed_c_read_write_split
reason = user confirmed option C: team can read KDS dashboard/graph/search, while write, prompt, secret, and persistent operations remain authorization-controlled
```

## 4. 失败与边界

| 阻塞 | 真实结果 | 影响 |
|---|---|---|
| Brain dev server 初始未运行 | 初次 `ECONNREFUSED 127.0.0.1:5175`，启动 `npm run dev:local` 后 `brain_runtime_health=pass` | 运行健康阻塞已部分解除，但不能替代正式浏览器与 harness 闭环 |
| 浏览器 user flow 证据 | 已刷新并通过 C 口径 | 仍不代表写入、prompt、secret 或持久化操作授权 |
| 浏览器自动化依赖 | Playwright bundled Chromium 缺失；系统 Chrome channel 可用 | 当前 browser smoke 已按 Chrome Playwright 与 C 口径通过，但不代表完整浏览器自动化覆盖 |
| Team 授权行为变化 | 用户已确认 C：team 可读 KDS dashboard/graph/search，写入、prompt、secret、持久化操作继续强授权 | 已从待确认漂移转为受控基线 |
| harness evidence 失败 | status-audit、bulk-fix execution、authorized prompt 证据仍需刷新 | 不能声明 harness 当前可信闭合 |
| KDS 运行联动 | runtime health 读取最新 `kds_total_pages=2732`，browser smoke、browser user-flow、read-closure、Chinese gates 已通过，但 write-boundary、bulk-fix execution、authorized prompt 仍未刷新 | 只能登记部分运行验证，集成仍为 `repair_required` |
| 格式门禁 | `npm run format:check` 已通过 | 格式阻塞已解除 |

## 5. 状态结论

```text
brain_static_check = verified
brain_typecheck = verified
brain_unit_tests = verified
brain_build = verified
brain_runtime_health = verified
brain_target_panel_runtime_matrix = verified
brain_target_panel_data_quality = verified
brain_format_check = verified
brain_browser_user_flow = verified_with_boundaries
brain_read_closure_matrix = verified_with_boundaries
brain_chinese_gates = verified_with_boundaries
brain_completion_matrix = repair_required
brain_chrome_browser_visible_signals = confirmed
brain_team_authorization_contract = confirmed_c_read_write_split
brain_browser_runtime_smoke = verified_with_boundaries
brain_harness_evidence = repair_required
brain_real_delivery = not_collected
brain_customer_acceptance = not_collected
```

## 6. 非声明边界

当前不登记 Brain 真实运行闭环完成。

当前不登记 Brain 真实集成完成。

当前不登记 Brain 真实交付完成。

当前不登记 Brain 客户验收通过。
