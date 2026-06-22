---
doc_id: GPCF-DOC-221282A70B
title: GlobalCloud Loop Usability Gates
project: GPCF
related_projects: [GPCF, WAES]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-loop-orchestrator/references/usability-gates.md
source_path: .codex/skills/globalcloud-loop-orchestrator/references/usability-gates.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# GlobalCloud Loop Usability Gates

## 可用性定义

可用不是“文件存在”，而是目标用户可以按说明完成关键任务。

## 每轮最小可用性 evidence

- 关键路径复现步骤。
- 运行命令或访问入口。
- 截图、录屏、日志或人工试用记录。
- 失败场景和恢复方式。

## UI Quality Gate 接入

当 Loop 轮次涉及产品界面、控制塔、工作台、证据页、异常页、AI 对话页、配置页、移动端或桌面端 UI 时，必须调用 `globalcloud-ui-quality-gate`。

最低要求：

- 读取 `.codex/skills/globalcloud-ui-quality-gate/SKILL.md`。
- 读取 `04-ui-delivery/GlobalCloud项目群界面工程整体实施方案.md`。
- 读取 `04-ui-delivery/GlobalCloud项目群UI设计开发治理与评估统一规范.md`。
- 按 `references/quality-checklist.md` 对 G1-G9 逐项给出 `pass`、`partial`、`fail` 或 `not_applicable`。
- 按 `references/evidence-output.md` 输出 UI gate status、工具、验证、状态上限和缺口。
- 若使用 Impeccable、accessibility、Playwright/browser 或 Figma，必须记录命令、入口、截图、失败和未验证项。
- 运行 `python3 tools/kds-sync/validate_loop_ui_quality_baseline.py`，确保 Loop 模板与显式 UI round 结构满足机检要求。

UI 门禁输出的最高状态是 `ui_evidence_candidate`。`ui_ready` 只表示 UI 维度具备 evidence candidate，不表示业务完成、验收完成、accepted 或 integrated。

## 状态上限

| 情况 | 状态上限 |
|---|---|
| 无可用性 evidence | `partial` |
| 关键路径不可复现 | `blocked` |
| 只完成文档但无使用路径 | `partial` |
| 涉及 UI 但未执行 UI Quality Gate | `partial` |
| UI Quality Gate 为 `ui_blocked` | `blocked` |
| UI Quality Gate 为 `ui_rework_required` | `rework_required` |
| UI Quality Gate 为 `ui_partial` | `partial` |
| 可用性验证通过 | 可进入客户满意门禁 |
