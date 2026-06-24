---
doc_id: GPCF-DOC-C9A7E8D2B1
title: Frontmatter 写入权责清单（tools/kds-sync）
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
domain: tools
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/tools/kds-sync/FRONTMATTER_OWNERSHIP.md
source_path: tools/kds-sync/FRONTMATTER_OWNERSHIP.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# Frontmatter 写入权责清单（tools/kds-sync）

## 1. 主权文件（只允许对应工具直接重写 frontmatter）

| 路径 | 工具 | 行为 | 备注 |
| --- | --- | --- | --- |
| `09-status/globalcloud-document-control-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | `apply_frontmatter` | 受控文档台账主写入 |
| `09-status/kds-development-space-sync-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | `apply_frontmatter` | KDS 同步台账主写入 |
| `09-status/document-deprecation-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | `apply_frontmatter` | 文档废弃台账主写入 |
| `09-status/globalcloud-document-health-report.md` | [loop_document_gate.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/loop_document_gate.py) | 专有报表覆盖 | 仅本文件由该工具持有 |
| `.kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-control-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | 镜像同步 | 镜像来源于主控台账 |
| `.kds/development-space/开发/91-治理与验收/09-status/kds-development-space-sync-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | 镜像同步 | 镜像来源于主控台账 |
| `.kds/development-space/开发/91-治理与验收/09-status/document-deprecation-register.md` | [document_control.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/document_control.py) | 镜像同步 | 镜像来源于主控台账 |
| `.kds/development-space/开发/91-治理与验收/09-status/globalcloud-document-health-report.md` | [loop_document_gate.py](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/loop_document_gate.py) | 镜像同步 | 与 health report 对齐 |

## 2. 标准写入模式（文档/证据产物）

- 这类脚本默认使用 `preserve_frontmatter`，目标是保留现有 frontmatter：
  - `build_*`
  - `run_*`
  - `generate_*`
- 典型脚本路径在本 repo 下按 `tools/kds-sync/`，例如：
- [构建知识空白复核模板脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/build_base_knowledge_blank_review_templates.py)
- [构建知识确认队列视图脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/build_base_knowledge_confirmation_queue_views.py)
- [构建收敛收尾演练证据脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/build_base_knowledge_closure_dry_run_evidence.py)
- [运行 Headroom LCX 项目组回放稳定性脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/run_headroom_lcx_project_group_replay_stability.py)

## 3. 只读链路（建议仅读取 frontmatter）

- 以 `check_*`、`validate_*` 为主，不应修改受控 frontmatter。
- 其中包含但不限于：
- [Loop 治理文档校验脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/validate_loop_governance_docs.py)
- [Loop 代码图目标优化校验脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/validate_loop_codegraph_goal_optimization.py)
- [AGENT 到达门禁校验脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/validate_agent_reach_loop_admission.py)
- [文档污染检测脚本](/Users/lujunxiang/Projects/GlobalCloud%20V0.0.1/GlobalCoud%20GPCF/tools/kds-sync/check_document_pollution.py)

## 4. 执行优先级（当前链路建议）

1. `document_control.py`（主权重写）
2. `loop_document_gate.py`（健康报表单写）
3. `build_*/run_*` 证据生成（按顺序串行执行）
4. `validate_*`/`check_*` 只读校验

## 5. 冲突控制原则

- 同一文件不得并发写入，尤其是 `09-status/*`、`.kds/development-space/` 与受控 frontmatter 文件。
- 任一阶段失败立刻退出并补齐 `kds_sync` 错误闭环证据。
- 关键受控 frontmatter 只允许上述主权工具改写。
