---
doc_id: GPCF-DOC-8EC9A00BFD
title: GlobalCloud GPCF 项目群治理控制仓
project: GPCF
related_projects: [GPC, WAME, KDS, GPCF]
domain: general
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/00-项目群总控/README.md
source_path: README.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud GPCF 项目群治理控制仓

GlobalCoud GPCF 是 GlobalCloud 项目群的 Feature 交付中心与轻治理控制仓。历史体系文档继续受控保留，新开发默认从 Feature Workspace 进入。

主要入口：

| 入口 | 用途 |
|---|---|
| `00-index/README.md` | 项目群总索引与统一口径入口 |
| `09-status/globalcloud-project-mainline-alignment-matrix.md` | 历史 12 项目主线对齐矩阵；当前范围见项目注册表 |
| `09-status/globalcloud-document-control-register.md` | 文档控制总台账 |
| `09-status/kds-development-space-sync-register.md` | KDS 开发空间同步台账 |
| `09-status/globalcloud-document-health-report.md` | 文档健康报告 |
| `tools/kds-sync/` | 文档控制、KDS 同步和 Loop 文档门禁脚本 |
| `features/active/` | GPCF 2.0 Feature 交付入口 |
| `projects/` | 当前 28 项目的节奏入口；当前范围见 `config/project-group-projects.yaml` |
| `loops/` | GPCF 2.0 执行、复核、修复闭环 |
| `runtime/queue.json` | Feature 调度队列 |
| `runtime/state.json` | Feature 交付运行状态 |

文档治理要求：

- 新增 Markdown 文档必须纳入文档控制台账。
- 新增目录必须有 README。
- KDS `开发` 空间同步必须留下同步流水。
- 旧命名、旧 AI 定位和真实性污染不得回流。

GPCF 2.0 开发入口：

```bash
python scripts/gpcf_new_feature.py --project gpcf --name supplier-onboarding --priority P0 --goal "完成供应商入驻主流程"
```

GPCF 2.0 开发出口：

```bash
python scripts/gpcf_close_feature.py F-001
```

GPCF 2.0 Evidence Gate：

```bash
python scripts/gpcf_check_evidence.py F-001
```

GPCF 2.0 Runtime 调度：

```bash
python scripts/gpcf_dispatch.py F-001
```

<!-- 2026-10-22 文档可读性整改（R07/R08/R09）：以下为 append-only 补齐的缺失章节，上文未改动 -->

## 测试与门禁

本仓测试：

```bash
python3 -m pytest tests/ -q
```

关键门禁（CI 同款，均可本地复跑）：

```bash
python3 tools/kds-sync/loop_document_gate.py --check-only
python3 tools/kds-sync/validate_contract_matrix.py
python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py
python3 tools/kds-sync/validate_project_group_caliber_baseline.py
```

## 目录结构

```text
GlobalCloud GPCF/
├── $CODEX_HOME/                 # **待核**（仓内无该目录说明）
├── 00-index/                    # 总索引（按目录名前缀推断）
├── 01-architecture/             # 架构（按目录名前缀推断）
├── 02-governance/               # 治理（按目录名前缀推断）
├── 03-data-ai-knowledge/        # 数据/AI/知识（按目录名前缀推断）
├── 04-ui-delivery/              # 界面与交付（按目录名前缀推断）
├── 05-agent-team/               # Agent 团队（按目录名前缀推断）
├── 06-workstreams/              # 工作流（按目录名前缀推断）
├── 07-acceptance/               # 验收（按目录名前缀推断）
├── 08-evidence-samples/         # 证据样例（按目录名前缀推断）
├── 09-status/                   # 状态台账（按目录名前缀推断）
├── 10-archive/                  # 归档（按目录名前缀推断）
├── config/                      # 配置
├── docs/                        # 设计、方案、报告、归档
├── features/                    # Feature 工作区
├── fixtures/                    # 夹具
├── governance/                  # 治理
├── harness/                     # Harness 资产
├── loop/                        # **待核**（仓内无该目录说明）
├── loops/                       # 闭环记录
├── .gitignore                   
├── AGENTS.md                    
├── PROJECT_HARNESS_MANIFEST.md  
├── README.md                    
└── …… 另有 11 个一级目录未展开（见仓内实际内容）
```
