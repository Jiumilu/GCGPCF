---
doc_id: GPCF-DOC-F031-EVIDENCE-BASELINE
title: F-031 XGD dot 对齐审计基线引用
project: GPCF
related_projects: [GPCF, XGD]
domain: governance
status: draft
version: v0.1
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-031-xgd-dot-alignment/evidence/xgd-dot-alignment-baseline.md
source_path: features/done/F-031-xgd-dot-alignment/evidence/xgd-dot-alignment-baseline.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# XGD dot 对齐审计基线引用（F-031）

> 本文件只是 GPCF 侧台账引用，不复制 XGD 证据正文，也不代表 XGD 已实现、已验收或已交付。

## 来源

| 项 | 值 |
| --- | --- |
| 来源仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XGD`（只读，本轮未写入） |
| 变更目录 | `openspec/changes/xgd-dot-alignment/` |
| 变更文件 | `proposal.md`、`gap-analysis.md`、`design.md`、`tasks.md`、`change-card.md`、`audit-baseline.json` |
| 变更状态 | `candidate` / `pending_human_confirmation`；`tasks.md` 全部 `[ ]`，未开始实施 |
| 审计基线 | `openspec/changes/xgd-dot-alignment/audit-baseline.json` |
| 审计快照 | `generatedAt=2026-10-19T01:47:08Z`，`main@e3680606`，package `2.1.189`，工具数 59 |
| P0 结论 | 6 项能力：0 covered / 6 partial / 0 missing → `p0Readiness.verdict = not_aligned` |

## P0 能力范围（与 audit-baseline.json `byPhase.P0` 一致）

| 能力 id | 名称 | 审计状态 | 本 Feature 处置 |
| --- | --- | --- | --- |
| `dot-identity` | dot 档案与身份 | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |
| `dot-responsibilities` | 常驻职责 | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |
| `dot-activity` | Activity / Outputs | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |
| `dot-schedules` | 周期计划 | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |
| `dot-action-rules` | 自定义规则与行动审查 | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |
| `dot-stop-semantics` | 分层停止 | partial | 纳入 P0 交付范围，待 XGD 实现与验收 |

## 后续阶段（仅路线登记，不在本轮交付）

- P1：多渠道与云端工作区、应用连接器、后台线程、记忆与私密笔记、主动研究
- P2：多 dot / 专家 dot、工作区治理
- P3：语音与移动端

## Evidence Gate 现状（2026-10-19）

```text
$ python3 scripts/gpcf_check_evidence.py F-031
gpcf_feature_evidence feature=F-031 tests=pass build=pass screenshots=pass api=fail summary=fail governance_blockers=2 close_candidate=false
exit=1
```

- 证据未齐属预期：P0 的 `/dot/*` 接口与 Brain UI 证据在 XGD 侧尚未产生，本 Feature 不得关闭。
- 工具误判提示：`screenshots=pass` 来自 `detect_ui_evidence` 的文件名 `ui` 子串匹配，命中自动生成的 `evidence/build.txt`；实际无任何 UI 截图或浏览器证据，详见 `evidence/screenshots.txt`。本轮未修改门禁脚本。

## 台账边界

- 本轮只完成 GPCF 登记与回传：Feature 工作区、`runtime/queue.json`、`runtime/state.json`、`runtime/logs/F-031.jsonl`。
- 未修改 XGD 仓，未修改 GPCF 项目群总体方案与实施方案正文，未提升任何项目状态。
- 审计基线为静态仓库证据快照，不代表运行时行为或外部服务可用性；P0 完成以 XGD `tasks.md` 验收任务为准。
