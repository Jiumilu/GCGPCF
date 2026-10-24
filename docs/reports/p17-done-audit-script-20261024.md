---
doc_id: GPCF-DOC-F0B444F390
title: P17 done 不变量审计脚本（2026-10-24）
project: GPCF
related_projects: [GPCF, WAME]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p17-done-audit-script-20261024.md
source_path: docs/reports/p17-done-audit-script-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P17 done 不变量审计脚本（2026-10-24）

- 脚本：`scripts/gpcf_p17_done_audit.py`｜已并入全量体检（现 15 项）
- 不变量：`features/done` 内每个 Feature **要么证据可关单，要么落在 `runtime/exceptions.yaml` 已登记受控例外内**
- 动因：此前只能靠"人工跑一遍 evidence check 再肉眼比对例外表"，容易漏（尤其是并发会话新关单的 Feature）

## 1. 实测（2026-10-24 16:10）

```
done=23 closable=19 exception=4 violations=[] → pass
```

- done 23 = 19 可关单 + 4 受控例外（EXC-DONE-F-001/006/007/008）
- **violations=[]**：不存在"在 done 里但既不能关单、又没登记例外"的违规项

## 2. 判据

```bash
python3 scripts/gpcf_p17_done_audit.py            # 人读一行
python3 scripts/gpcf_p17_done_audit.py --json     # 含逐 Feature 明细
```

退出码：0 = 不变量成立；1 = 存在未登记例外的不合规 done Feature（应阻断交付）。

## 3. 边界

只审计"证据与例外一致性"，不改变任何 Feature 状态；不声明 accepted/integrated。
