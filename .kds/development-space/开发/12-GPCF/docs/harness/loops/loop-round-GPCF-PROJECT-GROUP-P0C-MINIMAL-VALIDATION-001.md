---
doc_id: GPCF-LOOP-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001
title: Loop Round GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, XiaoC, XGD, XiaoG, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001.md
source_path: docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-26
supersedes: []
superseded_by: []
---

# Loop Round GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001

## run

- 输入：用户要求“下一步”，承接 P0-B。
- 范围：GFIS、WAS、WAES、GPC、PVAOS、XiaoC、XiaoG、XGD、XWAIL、AAAS、SOP 的最小验证命令。
- 执行：
  1. 读取 P0-B 轮次、文档健康报告和 P0-C 任务队列。
  2. 对 11 仓执行 `git status --short --branch` 与 `git diff --check -- .`。
  3. 生成 P0-C evidence、Loop round 和只读 validator。
  4. 同步 KDS 本地镜像并复跑文档/Git 门禁。

## stop

| 字段 | 值 |
|---|---|
| stop_type | remaining_project_minimal_validation_passed |
| stop_reason | 剩余 11 仓最小验证命令均可运行且 diff-check 通过；项目群 Git gate 仍 partial，阻断提交/推送/验收，不阻断继续开发 |

## verify

```bash
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/validate_project_group_p0c_minimal_validation_20260626.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/loop_document_gate.py --check-only
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 tools/kds-sync/kds_conflict_guard.py
cd "/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCoud GPCF" && python3 .codex/skills/globalcloud-project-group-git-clean/scripts/project_group_git_clean_gate.py --root "/Users/lujunxiang/Projects/GlobalCloud V0.0.1" --allow-non-pass-exit-zero
```

## recover

- 本轮新增 P0-C evidence、Loop round 和 validator；恢复时删除这些新增文件并重跑文档控制。
- 本轮只执行只读 Git 命令，不清理 `.DS_Store`、`output/`、`dist` 或知识导入文件。
- 本轮未提交、未推送、未部署、未生产写入、未 schema migrate。

## debug

- 若后续 17 仓 Git gate 回到 blocked，优先检查 sensitive path、behind、diff-check failed。
- WAS `.DS_Store` 是本地产物隔离项，不在 P0-C 自动删除。
- SOP `output/` 和 operations 文档仍需 owner review，不能被写成生产指令。
- GFIS 仍缺真实 source-of-record 与 verified artifact，P0-C 不改变 repair_required。

## 输出

- `docs/harness/evidence/globalcloud-project-group-p0c-minimal-validation-20260626.md`
- `docs/harness/loops/loop-round-GPCF-PROJECT-GROUP-P0C-MINIMAL-VALIDATION-001.md`
- `tools/kds-sync/validate_project_group_p0c_minimal_validation_20260626.py`

## 状态判定

| 字段 | 值 |
|---|---|
| 本轮状态 | evidence_candidate |
| 11 项最小验证 | pass |
| 项目群 Git gate | partial |
| 是否提交/推送 | no |
| 是否 accepted/integrated/production_ready | no |
