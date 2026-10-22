---
doc_id: GPCF-DOC-0A8D4A5642
title: P19 · 29 项目组合决策模板（90 天末执行）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p19-combination-decision-template-20261022.md
source_path: docs/reports/p19-combination-decision-template-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P19 · 29 项目组合决策模板（90 天末执行）

- 日期：2026-10-22｜状态：模板，**现在不执行**；90 天末按本模板逐项裁定
- 数据源：`runtime/plan-20261022/decisions.yaml`（当前处置）+ 各项目证据 + 本次 90 天结果

## 1. 每项目必填字段

| 字段 | 取值 | 依据 |
|---|---|---|
| project / slug | 29 项 | 注册表 |
| current_disposition | continue/merge/pause/exit | decisions.yaml（Q6 裁定） |
| day90_disposition | continue/merge/pause/exit/switch | 本次重新裁定 |
| evidence_refs | 路径列表 | 证据/STATUS/门禁结果 |
| blocker_resolved | true/false | 90 天内是否解除 |
| c_dev_delta / c_real_delta | 数值 | VU 台账前后对比 |
| decision_basis | 一句话 | 决策模型结论 + 老卢裁定 |
| auth_id | 回执号 | 授权台账 |

## 2. 裁定规则（先跑模型再问）

1. 对每个项目跑 `classify_project_status`（idea/candidate/active/waiting/paused/completed/archived）；
2. 对"是否继续投入"跑 `gate(redline)` 与 `authorization_qa`；
3. 合并/退出项逐一出清单 + 回滚方案 + `gate(rule=redline)` + 回执（不得批量口令）；
4. 决策结论写 `decisions.yaml` 新版本（append-only：旧条目保留 + 标注替代）。

## 3. 判据（P19 完成）

```bash
python3 -c "import yaml;d=yaml.safe_load(open('runtime/plan-20261022/decisions.yaml'));p=d['projects'];
assert len(p)==29 and all(x.get('day90_disposition') and x.get('decision_basis') and x.get('auth_id') for x in p);print('p19 ok')"
jq -s '[.[]|select(.kind=="dispose")]|length' runtime/audit/decision-ledger-20261022.jsonl   # ≥29
```

## 4. 边界

- 本模板不构成任何处置结论；不声明状态提升；
- 合并/退出会改分母与跨仓，仍需逐项授权。
