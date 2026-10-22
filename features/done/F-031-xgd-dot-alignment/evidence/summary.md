---
doc_id: GPCF-DOC-F031-EVIDENCE-SUMMARY
title: F-031 Evidence Gate 快照与证据摘要
project: GPCF
related_projects: [GPCF, XGD]
domain: governance
status: draft
version: v0.2
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-031-xgd-dot-alignment/evidence/summary.md
source_path: features/done/F-031-xgd-dot-alignment/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: pass
- api: pass
- acceptance_declared: true
- lint: 已通过 build 证据中的 git diff --check、XGD `npm run lint`（335 文件）与 `npm run typecheck`（335/335）覆盖。
- risk: 真实 HTTP 证据只指向本机已运行实例（127.0.0.1:3721），不是客户环境；不声明 accepted/integrated/production_ready/customer_accepted；推送、部署与状态提升须按各自边界人工确认。
<!-- GPCF_EVIDENCE_GATE_END -->

## 一、本轮定位（PJ-17）

F-031（`xgd-dot-alignment`，project: xgd，status: active，stage: candidate）此前 `screenshots/api/summary`
三项 fail，理由是「GPCF 侧只有结构门禁与引用，无 Feature 专属执行证据」。本轮在 `GlobalCloud XGD`
仓**实际复跑**可执行命令并采集真实证据，只改 F-031 目录，不改 XGD 仓文件、不 commit/push。

采集时点：2026-10-22T07:35–07:38+08:00。各命令执行后立即复查 XGD 仓 `git status --porcelain` 为空
（07:35–07:36，无 tracked/untracked 变更）；07:37–07:38 期间有**并发外部进程**在
`GlobalCloud XGD/docs/harness/evidence/` 生成其它文件（如 `standalone-analysis-ui-2026-10-22.png`），
非本任务写入，本任务只写 F-031 目录。

## 二、本轮实跑命令与结果（cwd=`GlobalCloud XGD`）

| # | 命令 | 结果 | 证据 |
|---|---|---|---|
| 1 | `npm run harness:validate` | `xgd_loop_harness=pass`（substance_gate=pass），exit 0 | `evidence/tests.txt` |
| 2 | `npm run test:unit` | `[PASS] unit tests: 9/9 suites`，exit 0 | `evidence/tests.txt` |
| 3 | `npm run test:dot` | `[PASS] dot alignment tests: 108/108 assertions`，exit 0 | `evidence/tests.txt` |
| 4 | `npm run lint` | `[PASS] lint: syntax + secret scan passed for 335 JavaScript files`，exit 0 | `evidence/build.txt` |
| 5 | `npm run typecheck` | `[PASS] syntax check: 335/335 JavaScript files`，exit 0 | `evidence/build.txt` |
| 6 | `npm run smoke:brain-ui` | `[PASS] dot console flow` + `[PASS] brain-ui smoke`（Chromium，真实浏览器流程），exit 0 | `evidence/build.txt` |
| 7 | `python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py`（cwd=GPCF） | `gpcf_2_feature_workspace=pass ... project_scope=28`，exit 0 | `evidence/tests.txt` |

## 三、screenshots / api / summary 三项证据

- **screenshots: pass** —— 对**本机真实运行实例** `http://127.0.0.1:3721/brain-ui` 用 Playwright
  （Chromium 156.0.8078.4）实拍 3 张 1440×900 PNG（Brain UI 主界面 / dot 控制台活动 tab / dot 职责 tab），
  页面 `pageErrors=[]`；dot 浮层实测 `dotHandle=@xiaog`、
  `dotMeta=1 条活跃职责·0 个启用计划·456 条活动·68 个工具`。系统麦克风权限请求在采证时点「取消」，未授权。
  资产：`evidence/screenshots/`。
- **api: pass** —— 对同一实例只读 HTTP `GET`（`--read-only` 探针）：
  `/healthz` 200（db connected、llm configured、memory_count 807）、`/runtime/info` 200
  （version 2.1.194、mode standalone、modeValid/scopeValid=true）、`/dot/*` 8 个只读端点全部 200，
  汇总 `xgd_dot_api_probe=pass endpoints=10/10`。可复跑命令：
  `python3 features/active/F-031-xgd-dot-alignment/evidence/probe_xgd_dot_api.py --read-only`。
  全程 **未启动/停止服务、未发 POST/PUT/DELETE**。
- **summary: pass** —— 即本文件；所有数字来自本轮实测命令输出。

## 四、与 acceptance 的关系（不越权判定）

- 「XGD 侧 P0 本地可回放证据（单元测试、接口测试、Brain UI smoke）齐备并通过 Evidence Gate」：
  本轮已采齐 tests/build/screenshots/api/summary 五项并通过 `--check-only` 结构检查；
  **逐条人工验收仍未执行**，不计为已验收。
- 「分层停止三种语义在 XGD 侧分别可验证后方可评估」：`test:dot` 提供契约级断言
  （4.1 dot 可暂停 / 4.2 TICK 含 PAUSED / 2.6 paused 不参与选择 / 7.6 关开关后工具拒绝 / 8.x 计划触发），
  属自动化契约覆盖，**未**做独立人工端到端验证。
- 其余 acceptance 项涉及 XGD 侧实现与人工确认，保持原状。

## 五、Evidence Gate check-only 输出（2026-10-22 07:38 +0800）

```bash
cd "GlobalCoud GPCF"
python3 scripts/gpcf_check_evidence.py --check-only F-031
```

```text
gpcf_feature_evidence_check feature=F-031 close_candidate=false reasons=governance blockers remain
exit_code: 1
```

解读：`--check-only` 只读检查未报 `evidence is incomplete`，说明五项 evidence（tests/build/screenshots/api/summary）
已齐且为 pass/waived；`close_candidate=false` 的唯一原因是 **governance blockers remain**（候选 Feature 人工确认、
P0 逐条人工验收、分层停止三语义人工验证、P1-P3 与 D10 边界），属候选阶段预期，不构成"证据缺失"。

## 六、未覆盖与不声明

1. 未执行 `electron-builder` 打包/签名（属发布边界 D10），不声明构建产物可发布。
2. 未做 72h/24h 观测的收口，不声明长期稳定性。
3. 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；
   不改变 `status: active`、`stage: candidate`、`candidate_registration.confirmation=pending_human_confirmation`。
4. 截图与 HTTP 证据来自本机运行实例，不代表真实客户环境或业务验收。

## 七、复核命令

```bash
# 1) XGD 仓实测（只读执行，不改仓）
cd "GlobalCloud XGD"
npm run harness:validate && npm run test:unit && npm run test:dot && npm run lint && npm run typecheck && npm run smoke:brain-ui
git status --porcelain   # 期望为空

# 2) 只读 api 探针（需本机 XGD 后端已在 127.0.0.1:3721 运行）
cd "../GlobalCoud GPCF"
python3 features/active/F-031-xgd-dot-alignment/evidence/probe_xgd_dot_api.py --read-only

# 3) GPCF 只读结构检查
python3 scripts/gpcf_check_evidence.py --check-only F-031
```
