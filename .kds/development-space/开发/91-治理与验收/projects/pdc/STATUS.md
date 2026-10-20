---
doc_id: GPCF-PDC-STATUS-20261018
title: GlobalCloud PDC 状态
project: GPCF
related_projects: [GPCF, PDC]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/pdc/STATUS.md
source_path: projects/pdc/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# GlobalCloud PDC 状态

- 路径：`../GlobalCloud PDC`；独立 Web + Electron 包装设计应用，业务数据保存在本地 SQLite。
- 来源与版本：私有远端 `https://github.com/Jiumilu/GCPDC`；2026-10-18 本地与远端 `main` 同为 `91fb7ce8bb91193645e625b24fcb168661cebc8e`，本地工作树干净。
- 负责人：GlobalCloud（老卢）；项目内 `PROJECT_HARNESS_MANIFEST.md` 记录 v1.2.0、历史门禁与本地打包验证。当前会话未重跑应用功能测试。
- 项目群身份：已进入当前治理清单；`project_status=registered`，`overall_status=partial/rework`。独立仓 `GlobalCloud PDC 总体方案.md` 与 `GlobalCloud PDC 实施方案.md` 为候选，双主控继承待核验。
- 应用装配：未登记 WAE 模块、未执行 G1/G2/G3；独立应用纳管不等于 WAE 集成、客户验收或环境发布。
- authorization：用户于 2026-10-18 授权纳入项目群并建立 Git 与远端；现有私有远端和本地 Git 已核实，无需重复创建或推送。
- confirmation：业务验收、正式集成、生产发布和状态提升均待人工确认。
- 回退：从中央清单移除 PDC 与本目录登记；独立源码仓库及远端不受影响。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/pdc-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project pdc`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`
