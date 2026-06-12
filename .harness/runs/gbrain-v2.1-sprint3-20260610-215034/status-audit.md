# Harness Governance: gbrain-v2.1-sprint3

## Sprint 3 — DQ 治理闭环 ✅

### 交付

| 文件 | 功能 |
|------|------|
| `services/dq.py` | DQ 评分引擎: authority/freshness/completeness/metadata 四维 |
| `services/repair_tasks.py` | 修复任务状态机: open→assigned→fixing→ready_for_review→accepted→closed |
| `routes/admin_dq.py` | `/admin/dq/distribution`, `/admin/dq/analyze`, `/admin/dq/tasks` |
| `tests/test_dq.py` | 4 tests |

### DQ 分析结果

- 扫描 5,000 页，发现 50 个低分页面
- 最低 DQ=2（缺 frontmatter 字段）
- 自动生成修复建议含 priority 和 reasons

### 修复状态机

```
open → assigned → fixing → ready_for_review → accepted → closed
                                                    ↑ 人工确认
```

`complete` 状态被显式拦截，必须通过人工 `accepted`。

### 全量回归: 21/21 ✅

### 判定: ready_for_human_acceptance
