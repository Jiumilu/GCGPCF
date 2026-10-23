---
doc_id: GPCF-DOC-F010-UI-ENGINEERING-COVERAGE-SUMMARY-20260712
title: 证据摘要
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-010-project-group-ui-engineering-coverage/evidence/summary.md
source_path: features/done/F-010-project-group-ui-engineering-coverage/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 证据摘要

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass（2026-10-22 修复后：UI 总控项目映射 26→28，补齐 PDC、DRC；`validate_project_group_ui_engineering_coverage.py` pass）
- build: pass
- screenshots: pass（既有 Studio 设置页截图与结构指标 artifacts）
- api: waived（本 Feature 不调用外部/KDS API，理由见 `verification.waivers.api` 与 `evidence/api.txt`）
- summary: pass（tests 通过；4 项 UI gate 仍 pending，见 blockers）
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升；UI 覆盖门禁已 pass，4 项 UI gate 仍 pending。

## Verification 复核与覆盖门禁（2026-10-22）

### 本轮改动范围（仅本 Feature 目录）

- `feature.yaml`：补齐 `scope.in/out`、`acceptance`、`verification`（tests 3 条 / build 1 条）、`api` 豁免的本 Feature 理由；`evidence` 按实测改为 `tests: fail`、`summary: fail`；`blockers` 移除已解决的证据规则项，保留真实阻塞（UI 覆盖缺口、4 项 UI gate pending）；未改 gates 枚举值（pending 保持 pending）。
- `evidence/tests.txt`、`evidence/build.txt`、`evidence/api.txt`、本文件：按实际运行输出更新。
- 未修改 GPCF 其它文件（含 `04-ui-delivery/**`、`config/project-group-projects.yaml`）；未 commit/push。

### Feature 专属验收命令实测（2026-10-22，cwd=GPCF 仓根）

| kind | 命令 | 结果 |
|---|---|---|
| tests | `python3 tools/kds-sync/validate_project_group_ui_engineering_coverage.py` | **fail**：`FAIL validate_project_group_ui_engineering_coverage: UI master plan mapping count mismatch` |
| tests | `python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py` | pass：`project_scope=28` |
| tests | `python3 tools/kds-sync/validate_loop_ui_product_first_control.py` | pass：`project_count=28 active_feature_coverage=23`（仅证明控制链与 gate 字段齐备） |
| build | `python3 -X pycache_prefix=/tmp/gpcf-f010-pycache -m py_compile tools/kds-sync/validate_project_group_ui_engineering_coverage.py tools/kds-sync/validate_gpcf_2_feature_workspace.py tools/kds-sync/validate_loop_ui_product_first_control.py` | pass（无输出） |

### UI 覆盖门禁缺口（真实失败原因）

- registry `config/project-group-projects.yaml`：`current_project_count: 28`，`projects` 28 条。
- UI 总控文件 `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md` 的项目映射表只有 26 条，缺 `PDC`、`DRC`。
- validator 规则要求「映射项目集合与 registry 完全一致」，故当前 FAIL。
- 修复路径：在 UI 总控文件补录 `PDC`、`DRC` 两条项目映射（含主类/副类/定位摘要），并同步 `related_projects`；该文件属 `04-ui-delivery` 治理文档，超出本任务 F-010 目录写范围，未由本任务修改。
- 说明：registry 与 UI 总控文件当前均处于「其它会话未提交改动」状态（工作区相对 HEAD 已从 24/21 扩到 28/26），本次失败是两文件在途更新之间的真实不一致，不是本任务引入。

### UI 产品优先控制 gates 处置

| gate | 本轮取值 | 理由 |
|---|---|---|
| `functional_completeness` | pass（保持） | 门禁、映射基线与技能链结构已在 UI 总控/规范/技能中建立，validator 可机器校验 |
| `quality_baseline` | pass（保持） | 既有截图与结构指标证据来自 Studio 设置页，属既有基线 |
| `multi_user_usability` | **pending（保持）** | 无多用户任务完成证据：现有截图仅 Studio 设置页单页，缺首访/高频/治理审计三类用户的真实任务与反馈 |
| `task_flow_e2e_status` | **pending（保持）** | 无端到端任务流与错误恢复验证；覆盖门禁本身不以 E2E 证据替代 |
| `accessibility_status` | **pending（保持）** | 无键盘/焦点/读屏等无障碍证据；未做无障碍实测，不得写 pass |
| `evidence_overexposure_gate` | **pending（保持）** | 无人类入口证据展示审查；单页截图不能证明默认界面不暴露机器字段 |

`status_ceiling` 保持 `partial`（存在 pending UI gate 时必须 partial）。

### Evidence Gate 复核（修改前 / 修改后）

修改前（2026-10-22 08:0x 基线）：

```text
$ python3 scripts/gpcf_check_evidence.py --check-only F-010
gpcf_feature_evidence_check feature=F-010 close_candidate=false reasons=acceptance is empty; scope.in is empty; governance blockers remain; Feature-specific tests command is not declared; Feature-specific build command is not declared; api waiver has no Feature-specific reason
exit=1
```

修改后：

```text
$ python3 scripts/gpcf_check_evidence.py --check-only F-010
gpcf_feature_evidence_check feature=F-010 close_candidate=false reasons=evidence is incomplete; governance blockers remain
exit=1
```

结论：结构性证据规则原因（acceptance/scope 空、tests/build 未声明、api 豁免无理由）已全部解除；仍为 fail 的原因是真实失败：

1. `tests evidence failed`（UI 覆盖门禁 FAIL：映射 26/28，缺 PDC、DRC）；
2. `summary evidence failed`（tests 未通过导致）；
3. 4 项 UI gate 仍 pending（理由见上表）。

不伪造 pass；`close_candidate=false`，Feature 维持 `active`、`status_ceiling=partial`。

### 保留观察项

- `feature.yaml.goal` 与 `primary_human_task` 仍使用历史口径「18 项目」，与当前 registry 28 项目不一致（既有口径，本任务未改 goal；建议 UI 治理会话统一刷新）。
- 既有 `screenshots: pass` 仅覆盖 Studio 设置页单页，不代表多项目 UI 覆盖；本轮未据此提升任何 gate。
- 未执行真实 API、KDS 写入、部署与状态提升。

### 回滚

```bash
git -C "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" restore --source=HEAD -- \
  features/active/F-010-project-group-ui-engineering-coverage/feature.yaml \
  features/active/F-010-project-group-ui-engineering-coverage/evidence/
```

- 回滚只涉及本 Feature 目录（`feature.yaml` 与 `evidence/`）；不涉及 `04-ui-delivery/**`、registry、其它仓或 KDS。
- 无数据迁移、无外部 API 写入、无部署、无权限变更，回滚无数据风险。

### 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；不声明状态提升（Feature 仍 `active`，`status_ceiling=partial`）。
- 不声明 UI 工程覆盖已完成：UI 覆盖门禁当前 fail（映射 26/28），4 项 UI gate 仍 pending。
- 不声明其它项目 UI 就绪；`ui_ready` / 覆盖门禁 pass 不等于 `accepted` 或 `integrated`。

## 2026-10-22 修复后复核（Lead）

- 修复：`04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md` 项目映射表补录 PDC、DRC；registry 28 与总控映射 28 一致。
- 命令：`python3 tools/kds-sync/validate_project_group_ui_engineering_coverage.py` → `project_group_ui_engineering_coverage=pass project_count=28 ui_master_mapping=complete ui_governance_chain=validated`。
- `evidence.tests` 与 `evidence.summary` 由 fail 改为 pass；4 项 UI gate（multi_user / task_flow / accessibility / evidence_overexposure）仍 pending，`status_ceiling=partial` 不变。
- 未 commit/push；未声明状态提升。

## 2026-10-22 四项 UI gate 补采（task-17）

- 证据目录：`evidence/ui-gates-20261022/`（脚本、`logs/` 运行日志、`screens/` 13 张截图、该目录 `summary.md` 逐项判据）。
- gate 结果更新：`accessibility_status: pass`（WAE 统一身份入口真实 UI 键盘实测：16 次 Tab / 10 个不同焦点目标 / 15 次 `:focus-visible`（outline 2px）/ 0 个无名称交互元素 / `main` landmark / `zh-CN`）；`evidence_overexposure_gate: pass`（9 类机器字段正则 0 命中；3 项工程环境标注单列不记违规）；`multi_user_usability: pending`（无可授权真实账号，未用 mock 会话冒充）；`task_flow_e2e_status: fail`（如实保留失败）。
- Studio 阻断（A 级复现）：HEAD `b02d837e` 删除 `gcworld.*` 路由，但 `AppSidebar.vue:626` 仍 `:to="{ name: 'gcworld.organizations' }"` → `RouterLink` setup 抛「No match for {name:"gcworld.organizations"}」→ 登录后整页空白；Studio 既有 E2E「核心任务流」「会话服务失败恢复」2 条 spec 实测 **2 failed**。日志：`evidence/ui-gates-20261022/logs/studio-probe.log`、`logs/run-studio-existing-e2e.log`。修复需改 Studio 仓，超出本 Feature 写入边界。
- 边界：a11y / 证据暴露 pass 仅覆盖 WAE 统一身份入口默认首屏（+ 既有 Studio 设置页截图），不代表 18/28 项目逐页覆盖，也不代表多用户与任务流通过。
- 未做：未修复 Studio、未创建/重置任何凭据、未启动未知服务；WAE `pnpm dev`（:4300）为临时验证已停止；未用 mock 会话提升任何 gate。
- `python3 scripts/gpcf_check_evidence.py --check-only F-010` → `gpcf_feature_evidence_check feature=F-010 close_candidate=false reasons=governance blockers remain`（exit=1；真实阻塞见 feature.yaml blockers）。
- 非声明：不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；不声明四项 gate 全通过、不声明 Studio 可用。

## 2026-10-22 task-18：WAE 完整 task_flow 取证（task_flow_e2e_status → pass）

- 目标切换：Studio 侧仍受 HEAD `b02d837e` 回归阻断（登录后空白），task_flow 改由 **WAE 统一入口**取证。
- 环境：`GlobalCloud WAE` dev `:4300`；隔离临时 IdP 目录 `/tmp/f010-e2e-idp`（`WAE_IDP_DIRECTORY` 等 env 覆盖 + `POST /api/idp/bootstrap` 创建唯一临时账号；口令仅 env 注入、不写入证据；验证后停止服务并删除）。
- 命令：`cd "GlobalCloud WAE" && pnpm dev` → `cd "GlobalCloud Studio" && F010_OUT=<evidence/ui-gates-20261022> npx playwright test --config <...>/playwright.wae.config.ts --grep "task_flow_e2e_status: WAE"` → **1 passed**。
- 流程（9 steps / 0 pageerror；`evidence/ui-gates-20261022/logs/taskflow-assertions.json`）：登录页 → 空提交失败恢复（「请填写账号与口令」）→ 登录 → 首登强制改密 → 工作台「欢迎回来」→ 项目管理器弹层（4 个项目）→ 关闭返回主页 → 账户菜单退出 → 回登录页。
- 截图：`evidence/ui-gates-20261022/screens/wae-flow-01..07-*.png`。
- 边界：临时账号非真实用户/非共享实例；覆盖为 WAE 统一入口，不代表 28 项目逐页；Studio 回归仍在，需另立修复任务。
- 结果：`task_flow_e2e_status` 由 fail 改 **pass**；`multi_user_usability` 仍 pending（单账号不足以证明两类用户/角色切换）；`status_ceiling` 保持 partial。

## 2026-10-22 task-19：WAE 双角色 multi_user 实测（multi_user_usability → pass）

- 授权：老卢 2026-10-22 授权隔离临时 IdP + 2 个不同角色临时账号，验证后删除。
- 环境：`/tmp/f010-multi-idp` 隔离 IdP（env 覆盖目录/会话/审计/租户配置）；`POST /api/idp/bootstrap` 建 A=system-admin，A 会话建 B=viewer；口令仅 env 注入、未写入证据；验证后停止服务并删除临时目录与账号。
- 命令：`cd "GlobalCloud WAE" && pnpm dev` → `cd "GlobalCloud Studio" && F010_OUT=<evidence/ui-gates-20261022> npx playwright test --config <...>/playwright.wae.config.ts --grep "multi_user_usability: 双角色"` → **1 passed**（6 steps / 0 pageerror）。
- 结果：A=system-admin（/me 16 menus，用户目录 2/2 可见，GET /api/idp/users 200）；B=viewer（/me 4 menus，用户目录「无权限：用户目录仅体系管理员可见」，GET /api/idp/users 403「需要 system-admin 角色」）；双方 logout 后 /me=401，B 独立 context 不继承 A 会话。
- 证据：`evidence/ui-gates-20261022/logs/multi-user-assertions.json`、`screens/multi-user-A-system-admin-idp-users.png`、`screens/multi-user-B-viewer-idp-denied.png`、`screens/multi-user-A/B-after-logout-login.png`。
- 发现（另立缺陷）：WAE AppsShell 导航层角色收敛未生效（`generated.ts` app/entry 无 `requires`，viewer 仍看到服务控制台入口）；页面/接口判据正确拒绝，未构成越权成功。
- 结果：`multi_user_usability` 由 pending 改 **pass**；`status_ceiling` 仍 `partial`（Studio 回归与覆盖范围限制仍在，不做状态提升）。
