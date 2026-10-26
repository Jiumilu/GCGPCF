---
doc_id: GPCF-DOC-EVIDENCE-RULE-VERSION-20261022
title: 项目群关闭证据规则版本 v1.0（冻结）
project: GPCF
related_projects: [GPCF, ALL]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-evidence-rule-version-v1.0.md
source_path: 09-status/globalcloud-evidence-rule-version-v1.0.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 项目群关闭证据规则版本 v1.0（冻结）

> 任务：PG-08（关闭证据规则冻结）。性质：冻结"Feature 关闭需要什么证据"的规则版本，阻止规则再次被回溯改写。
> 非声明：本文不关闭任何 Feature、不提升任何项目状态。

## 1. 控制结论

```text
evidence_rule_version = GCPF-EVIDENCE-RULE-1.0
effective_date = 2026-10-22
freeze_status = frozen
change_requires = change_proposal + human_confirmation
close_conditions = acceptance_non_empty AND scope_in_non_empty AND tests_command AND build_command AND screenshots_evidence_or_reason AND api_evidence_or_reason AND summary
historical_done_policy = re_verify_or_register_exception
auto_close = false
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 2. 关闭条件（逐条）

| # | 条件 | 判据 | 缺失处理 |
|---:|---|---|---|
| 1 | `acceptance` 非空 | feature.yaml 有可验收条目 | 不得关闭；补 acceptance 或登记历史例外 |
| 2 | `scope.in` 非空 | 明确本轮范围 | 同上 |
| 3 | `tests` 命令已声明 | Feature 专属 tests 命令存在 | 补命令并重采 |
| 4 | `build` 命令已声明 | Feature 专属 build 命令存在 | 补命令并重采 |
| 5 | `screenshots` | 有证据，或 waiver 带**本 Feature 专属理由** | 补证据或补理由 |
| 6 | `api` | 有证据，或 waiver 带**本 Feature 专属理由** | 补证据或补理由 |
| 7 | `summary` | pass | 重采 summary |

## 3. 变更程序

1. 任何规则变更必须先写 Change Proposal（目标/影响 Feature/影响项目/回滚）。
2. 由 GPCF 登记，老卢确认后升版本号（1.0 → 1.1）。
3. 旧版本关闭记录不重写；新版本只对生效日之后的关闭生效。
4. 历史 `done` 必须按下表处置：补验通过，或登记为历史例外（保留原状、标注规则版本差异）。

## 4. 历史 done 处置

见 `09-status/globalcloud-done-feature-audit-20261022.md`：10 个 `features/done/*` 中 1 个 pass、9 个 fail；处置为"补验"或"历史例外"，**不自动重开、不自动关闭**。

## 5. 验证命令

```bash
python3 scripts/gpcf_check_evidence.py --check-only <FEATURE_ID>
python3 tools/kds-sync/validate_evidence_rule_version.py
python3 tools/kds-sync/document_control.py
```

## 6. 非声明边界

- 不声明任何 Feature 已关闭或可关闭；
- 不声明任何项目状态提升；
- 不声明规则变更已获老卢确认（本文为规则冻结基线，变更仍需确认）。
