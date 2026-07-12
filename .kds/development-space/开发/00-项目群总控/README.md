---
doc_id: GPCF-DOC-8EC9A00BFD
title: GlobalCloud GPCF 项目群治理控制仓
project: GPCF
related_projects: [GPC, WAES, KDS, GPCF]
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
| `09-status/globalcloud-project-mainline-alignment-matrix.md` | 12 项目主线对齐矩阵 |
| `09-status/globalcloud-document-control-register.md` | 文档控制总台账 |
| `09-status/kds-development-space-sync-register.md` | KDS 开发空间同步台账 |
| `09-status/globalcloud-document-health-report.md` | 文档健康报告 |
| `tools/kds-sync/` | 文档控制、KDS 同步和 Loop 文档门禁脚本 |
| `features/active/` | GPCF 2.0 Feature 交付入口 |
| `projects/` | 项目群 18 项目的 ROADMAP、STATUS、RISK 节奏文件 |
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
