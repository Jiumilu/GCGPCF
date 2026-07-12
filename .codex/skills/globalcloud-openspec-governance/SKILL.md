---
doc_id: GPCF-DOC-A7C2E40931
name: globalcloud-openspec-governance
description: GlobalCloud 项目群 OpenSpec 变更治理入口。用于提出、实施、同步或归档 OpenSpec 变更，以及用户要求把 OpenSpec 纳入项目群、Loop、Feature 或文档门禁时；路由 openspec-propose、openspec-apply-change、openspec-sync-specs、openspec-archive-change，并强制衔接 GPCF Feature、文档、evidence、Harness 和人工确认边界。
---

# GlobalCloud OpenSpec Governance

将 OpenSpec 作为项目群规格变更层使用，不把它当作交付状态裁决器。

## 路由

| 意图 | 必须加载的技能 |
|---|---|
| 新建变更提案、规格、设计和任务 | `openspec-propose` |
| 开始或继续实现变更任务 | `openspec-apply-change` |
| 将 delta specs 合入主规格且暂不归档 | `openspec-sync-specs` |
| 完成后归档变更 | `openspec-archive-change` |

先加载本技能，再加载且严格执行对应 OpenSpec 官方技能。不得复制官方技能流程或绕过其 CLI 状态解析。

## 项目群工作流

1. 读取 `AGENTS.md`、`config/project-group-projects.yaml`、`09-status/globalcloud-project-group-openspec-applicability-matrix.md`、`openspec/config.yaml`、目标 change 的 `.openspec.yaml` 与 `openspec status --change <name> --json`。
2. 明确变更影响的 Program、Project、Feature 和仓库；新开发必须使用 `python scripts/gpcf_new_feature.py` 建立或绑定 Feature。
3. 提案阶段使用 `openspec-propose`，把项目群约束写入 proposal/design/specs/tasks，不把约束块原样复制进产物。
4. 实施阶段使用 `openspec-apply-change`；逐项完成任务并同步 Feature `journal.md` 与 `evidence/`，不得只勾选任务而无实现证据。
5. 规格同步使用 `openspec-sync-specs`；同步后运行文档控制与污染检查。
6. 归档前使用 `openspec-archive-change`，并先通过 Feature Evidence Gate、文档门禁和适用的测试/构建/lint。
7. OpenSpec 完成或归档只表示规格工作流完成；最终验收与状态裁决仍交给 Harness Governance。

## 强制门禁

- `openspec status --change <name> --json` 是 artifact 状态与路径的事实源，不猜测目录。
- OpenSpec 任务与 GPCF Feature 必须可追溯；没有 Feature 绑定时不得进入实现。
- 修改 Markdown 后运行：
  ```bash
  python3 tools/kds-sync/document_control.py
  python3 tools/kds-sync/check_document_pollution.py
  python3 tools/kds-sync/validate_kds_token.py
  python3 tools/kds-sync/loop_document_gate.py
  ```
- 实施证据必须由 `python scripts/gpcf_check_evidence.py <FEATURE_ID>` 产生本地可回放结果。
- 18 项目覆盖必须通过 `python3 tools/kds-sync/validate_project_group_openspec_coverage.py`。
- 未经人工确认，不得声明 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。
- OpenSpec 归档不得替代 Git clean、运行、集成、交付或客户验收门禁。
- KDS TOKEN 失败为 `blocked`；文档债务或门禁未通过时最高为 `partial/rework`。
- 严格遵守 `DO NOT send optional commentary`。

## 最小输出

仅报告 change、Feature、已完成 artifact/task、验证证据、门禁状态、阻塞项和下一项必要动作。
