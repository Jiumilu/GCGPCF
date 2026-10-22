---
doc_id: GPCF-DOC-F026-GCMEM-EVIDENCE-20261018
title: F-026 GCMEM 纳管证据摘要
project: GPCF
related_projects: [GCMEM, GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-026-gcmem-governance-onboarding/evidence/summary.md
source_path: features/done/F-026-gcmem-governance-onboarding/evidence/summary.md
sync_direction: local_only
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: waived
- api: waived
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: GCMEM 独立仓提交与推送已由用户授权并完成；GPCF 远端仍待隔离既有未推送提交；部署及状态提升未经授权。
<!-- GPCF_EVIDENCE_GATE_END -->

## Verification 复核与 Evidence Gate（2026-10-22）

### 本轮改动范围（仅本 Feature 目录）

- `feature.yaml`：新增 `verification`（tests 2 条、build 3 条、screenshots/api 的本 Feature 专属豁免理由）；移除已解决的证据规则 blocker；按 2026-10-22 只读复验刷新既有 blocker（保留中央文档门禁 1 项，移除已解除的「wae 登记」项）。
- `evidence/tests.txt`、`evidence/build.txt`、`evidence/api.txt`、`evidence/screenshots.txt`、本文件：按实际运行输出更新。
- 未修改 GCMEM 仓受版本控制文件与 GPCF 其它文件；未 commit/push。
- 基线差异说明：任务开始时工作区 `feature.yaml` 相对 HEAD 已被改成仅含证据规则 blocker（未提交改动），HEAD 记录的两项既有 blocker 被覆盖；本轮按 HEAD 恢复既有真实 blocker 并逐项只读复验，未丢失治理记录。

### Feature 专属验收命令实测（2026-10-22，cwd=GPCF 仓根，按 Evidence Gate 的 argv 规则）

| kind | 命令（摘要） | 结果 |
|---|---|---|
| tests | `python3 -m pytest -q -p no:cacheprovider "…/GlobalCloud Mem/tests"` | pass，`439 passed in 32.31s` |
| tests | `python3 "…/GlobalCloud Mem/src/gcmem.py" doctor --json` | pass，`healthy=true`，total=508（live 账本快照） |
| build | `python3 -X pycache_prefix=/tmp/gcmem-pycache -m py_compile` + 9 个核心源文件 | pass（无输出） |
| build | `git -C "…/GlobalCloud Mem" diff --check HEAD origin/main` | pass（无输出） |
| build | `git -C "…/GlobalCloud Mem" diff --quiet HEAD origin/main` | pass（HEAD 与本地 origin/main 树一致） |

GCMEM 仓 canonical 命令（来源：`GlobalCloud Mem/README.md`、`AGENTS.md`）：`cd tests && PYTHONPATH= /usr/bin/python3 -m pytest -q`（实测 `439 passed in 27.78s`）、`PYTHONPATH= python3 src/gcmem.py doctor --json`（实测 `healthy=true`）。写入 `verification` 的是其 Gate 可执行等价形式（Gate 仅接受 `python3`/`git`，且 cwd 固定为 GPCF 仓根）；两种形式均已实跑。

补充只读校验（未纳入 `verification`，仅记录）：`python3 "…/GlobalCloud Mem/scripts/validate_contracts.py" --json` → `ok=true, fails=0`（schema/examples 全 PASS；生产账本 298 条可全部解析、32 条 meta 校验通过）。

### Evidence Gate 复核（修改前 / 修改后）

修改前（2026-10-22 07:05 基线）：

```text
$ python3 scripts/gpcf_check_evidence.py --check-only F-026
gpcf_feature_evidence_check feature=F-026 close_candidate=false reasons=governance blockers remain; Feature-specific tests command is not declared; Feature-specific build command is not declared; screenshots waiver has no Feature-specific reason; api waiver has no Feature-specific reason
exit=1
```

修改后：

```text
$ python3 scripts/gpcf_check_evidence.py --check-only F-026
gpcf_feature_evidence_check feature=F-026 close_candidate=false reasons=governance blockers remain
exit=1
```

结论：证据规则类原因（tests/build 未声明、screenshots/api 豁免无本 Feature 理由）已全部解除。`blockers` 按 2026-10-22 只读复验结果更新：

- **保留（真实）**：GPCF 中央文档门禁 rework_required（既有项，非本 Feature 可清理范围；`scope.out` 明确“不清理 GPCF 既有无关门禁问题”）。复验 `loop_document_gate.py --check-only` 输出 `gate=rework_required`，当前理由为 `missing_metadata`（1）、`missing_readme_dirs`（1）、`hard_failure:project_group_live_status_current`、`hard_failure:project_group_live_status_snapshot`。
- **移除（已解除）**：原 blocker「技能链总检查：既有 wae 目录未列入 23 项目登记」。复验 `config/project-group-projects.yaml` 注册 28 个项目且含 `wae`、`projects/` 目录 28 个且无未登记目录，`validate_project_group_skill_chain.py` 输出 `pass covered_projects=28`，`validate_gpcf_2_feature_workspace.py` 输出 `pass project_scope=28`，该 blocking 条件已不存在。

因此 `--check-only` 仍为 fail（`reasons=governance blockers remain`）：如实保留真实 blocker，不伪造 pass；`close_candidate=false`，本 Feature 维持 `active`、`ui_product_first_control.status_ceiling=partial` 不变。

### 既有 blocker 复验（2026-10-22，只读）

| 复验命令 | 输出摘要 | 判定 |
|---|---|---|
| `python3 tools/kds-sync/loop_document_gate.py --check-only` | `gate=rework_required`；reasons: `missing_metadata`、`missing_readme_dirs`、`hard_failure:project_group_live_status_current`、`hard_failure:project_group_live_status_snapshot`；`missing_metadata=1`、`missing_readme_dirs=1`、`review_overdue_90d=2812` | 中央文档门禁仍未通过 → blocker 保留（文本按当前理由刷新） |
| `python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py` | `gpcf_2_feature_workspace=pass ... project_scope=28` | 项目登记覆盖 28 |
| `python3 tools/kds-sync/validate_project_group_skill_chain.py` | `project_group_skill_chain=pass ... covered_projects=28` | 技能链检查通过 |
| registry vs `projects/` 目录比对（读 `config/project-group-projects.yaml`） | 注册 28 / 目录 28；`wae` 已在注册表；无未登记目录 | 原「wae 未列入登记」blocker 已解除 |
| `python3 tools/kds-sync/check_document_pollution.py` | `document_pollution=pass` | 污染项当前 pass |
| `python3 tools/kds-sync/validate_loop_ui_product_first_control.py` | `loop_ui_product_first_control=pass ... project_count=28` | UI control 当前 pass |
| `python3 tools/kds-sync/document_control.py --check` | exit 0（列出当日新增文档） | 文档控制检查通过 |

说明：中央门禁 `--check-only` 按脚本语义不写 health report / KDS mirror；执行前后 `git status` 对比仅出现并行其它会话的改动（F-011 evidence），本任务未引入 F-026 目录之外的变更。原 blocker 文本中的 `UI control` / `document_pollution` 已不成立，故 blocker 文本按当前复验结果刷新为 `missing_metadata` / `missing_readme_dirs` / 两个 status 校验 hard failure；该刷新为事实校准，不构成状态提升。

### 保留观察项（不改变 blocker 判定）

- GCMEM 仓工作区存在他人未提交改动（`M "GlobalCloud GCMEM 总体方案.md"` 及若干 untracked）；本任务只读、只运行验证命令，未改动、未清理、未 stash；canonical pytest 运行可能更新 GCMEM 仓内已被 gitignore 的 `.pytest_cache/`。
- GPCF 仓本地 `main` 相对 `origin/main` 为 ahead 12 / behind 128（本任务只读基线，未 fetch、未 push；非本 Feature 证据门原因）。
- GCMEM 账本为 live append-only（`GlobalCloud KDS/_meta/hermes-memory-log.md`），doctor 的 `total` 随时间增长（同日 298 → 508）；比对以 `healthy=true` 与 `issues=[]` 为准。
- Feature `acceptance` 仍写「GPCF 23 项目 OpenSpec 覆盖」，与当前 `config/project-group-projects.yaml` 的 28 项目口径不一致（既有口径差异，本任务未改 acceptance，留给 GPCF 治理会话统一）。

### 回滚

```bash
git -C "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" restore --source=HEAD -- \
  features/active/F-026-gcmem-governance-onboarding/feature.yaml \
  features/active/F-026-gcmem-governance-onboarding/evidence/
```

- 回滚只涉及本 Feature 目录（`feature.yaml` 与 `evidence/`）；不涉及 GCMEM 仓、GPCF 其它文件、KDS 或共享配置。
- 无数据迁移、无外部 API 写入、无部署、无权限变更，回滚无数据风险。

### 非声明

- 不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`；不声明状态提升（Feature 仍 `active`，`status_ceiling=partial`）。
- 不声明 Evidence Gate 已关闭：`close_candidate=false`，仅证据规则项解除；中央文档门禁 rework_required 这 1 项既有治理 blocker 仍按真实状态保留。
- 不声明 GCMEM 部署、推送或生产写入；本任务未调用真实 API、未写生产账本。
