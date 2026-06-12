# Harness Governance: gbrain-v2.2 — Agent-Assisted Governance ✅

## 交付清单

| 文件 | 功能 |
|------|------|
| `services/agent_tasks.py` | 任务状态机: create→start→submit→accept/reject |
| `services/patch_review.py` | Patch 安全审查（禁止 DROP/DELETE/system） |
| `services/conflict_detection.py` | 文件/API/行为三类冲突检测 |
| `routes/admin_agent.py` | `/admin/agent/*` 端点 |
| `agent/agent-contract.md` | Agent 输入输出协议 |
| `agent/agent-result.schema.yaml` | Agent 结果格式规范 |
| `tests/test_agent.py` | 7 tests |

## Agent 工作流验证

```
create → not_started
  → start → in_progress (workspace created)
    → submit → ready_for_human_acceptance (patch + review)
      → accept → accepted ✅
      → reject → in_progress ✅
```

## Patch 安全审查

| 检查 | 结果 |
|------|------|
| frontmatter 修改 | approved ✅ |
| DROP/DELETE 检测 | rejected ✅ |
| system call 检测 | rejected ✅ |

## Agent 约束

- 最高状态: `ready_for_human_acceptance`（不可 auto-complete）
- 必须走 patch，不可直接写文件
- 必须有 before/after evidence
- 人工 accept/reject 控制

## 全量回归: 34/34 ✅

## 判定: ready_for_human_acceptance
