---
doc_id: GPCF-DOC-9CD0369F87
title: F-014 · 真实会议数据试点授权申请包（待老卢签发）
project: KDS
related_projects: [WAME, KDS, MMC, Project]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/reports/f014-real-data-pilot-authorization-request-20261022.md
source_path: docs/reports/f014-real-data-pilot-authorization-request-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# F-014 · 真实会议数据试点授权申请包（待老卢签发）

- 日期：2026-10-22｜依据：F-014 owner/scope/留存已裁定（`AUTH-PG-F014-LEDGER-OWNER-20261022`）
- 状态：**已批准 B1+B2（2026-10-22 22:52，老卢问答裁定）**；回执 `AUTH-PG-F014-REAL-MEETING-PILOT-20261022`。B3（KDS/MMC 配置边界）**未批准**，另行申请。
- 脱敏口径：**最严**——仅保留议题/结论/行动项/责任人角色，姓名与联系方式一律去除（模型 97.4%）。
- 接收台账：Project（PMC / Plane）；留存：24 个月后归档

## 1. 申请的三件事

| # | 动作 | 数据范围 | 回滚 |
|---|---|---|---|
| B1 | 接入**真实会议纪要**（脱敏）作为 canonical 候选来源 | 待定：哪类会议、哪些字段、脱敏规则（建议仅保留议题/结论/行动项/责任人角色，去除姓名与联系方式） | 单据级删除 + 候选作废 |
| B2 | MMC 委派 + 人工确认后向 PMC 写入项目条目（**禁止自动写入**） | 仅经人工确认的条目 | 逐条撤回 + Plane 操作日志 |
| B3 | KDS/MMC 运行配置边界变更（属主执行） | 配置项清单另附 | 配置回滚脚本 |

## 2. 建议授权范围（最小）

```
AUTH-PG-F014-REAL-MEETING-PILOT-20261022
scope: f014_real_meeting_data_pilot
actions_allowed: read, intake_real_meeting_minutes_deidentified, write_kds_canonical_candidate,
                 mmc_delegation_dry_run, write_evidence
actions_forbidden: planner_auto_write, customer_data_export, production_deploy,
                   kds_mmc_config_change, status_promotion, push
expires_at: 2027-01-20T23:59:59+08:00
```

## 3. 验收判据

1. 真实会议纪要（脱敏）→ KDS canonical 候选 → MMC 委派 → 人工确认 → PMC 条目，全链有回执；
2. **无任何自动写入**（日志可证 0 次）；
3. 脱敏对照表随回执留档；
4. 数据可撤回演练 1 次通过；
5. 不得据此声明 accepted/integrated/production_ready。

## 4. 需老卢决策

1. 是否批准最小范围（B1+B2，不含 B3 配置变更）？
2. 会议数据范围：哪类会议、保留哪些字段（姓名/联系方式是否一律去除）？
3. KDS/MMC 配置边界变更是否本轮一并授权（跨项目属主执行）？

## 5. 裁定结果（2026-10-22 22:52）

1. ✅ 批准 B1+B2（真实纪要脱敏接入 + MMC 委派 + 人工确认写 PMC），**禁止自动写入**。
2. ✅ 脱敏最严（去姓名与联系方式）。
3. ❌ B3 KDS/MMC 运行配置边界变更未批，需属主单独执行。
