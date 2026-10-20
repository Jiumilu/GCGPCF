---
doc_id: GPCF-SLC-STATUS-20261018
title: GlobalCloud SLC 状态
project: GPCF
related_projects: [GPCF, SLC]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/slc/STATUS.md
source_path: projects/slc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# GlobalCloud SLC 状态

- 路径：`../GlobalCloud SLC`；Vite + Electron + Express 的运力测算应用。
- Git：私有远端 `https://github.com/Jiumilu/GCSLC`；源码基线 `3290ce79efaf9f87dc047504297dfcbda40054ab`、纳管记录 `289e5c17591ebd6ce15a1dfdfc3854b781bedea9` 均已推送。旧历史中的数据库文件与密码哈希仅保留在本地旧分支，未推送到新远端。
- 负责人：GlobalCloud（老卢）；来源为当前本地 SLC 项目。业务数据、环境文件和构建产物不入库。
- 项目群身份：进入 27 项目治理清单；`project_status=registered`，`overall_status=partial/rework`。项目级总体方案和实施方案的双主控继承尚未核验。
- 本轮仅核验 Git 与治理登记；应用类型、测试、构建、关键用户任务和外部依赖未重跑。WAE 装配、G1/G2/G3、客户验收及生产发布均未执行。
- 文档门禁：GPCF 单仓 `loop_document_gate.py --check-only` 曾返回 pass、状态上限 partial；跨仓 `validate_loop_project_group_gate_readiness.py` 返回 fail（20/20 未通过，且脚本未覆盖完整当期清单）。本轮纳管不提升业务或交付状态。
- authorization：用户于 2026-10-18 授权纳入项目群并建立 Git 与远端。
- confirmation：业务验收、正式集成、生产发布和状态提升待人工确认。
- 回退：从中央清单移除 SLC 与本目录登记；独立源码仓库不受影响。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/slc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project slc`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`
