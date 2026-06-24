---
doc_id: GPCF-DOC-KDS-REAL-RUNTIME-BASELINE-20260624
title: KDS 真实运行基线证据 2026-06-24
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md
source_path: docs/harness/KDS/evidence/kds-real-runtime-baseline-20260624.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# KDS 真实运行基线证据 2026-06-24

## 1. 证据范围

本证据记录 KDS 在核心链路 `WAES -> XWAIL -> AaaS -> GFIS/GPC/PVAOS -> KDS/Brain` 中的真实命令、索引、检索和治理边界。

本记录不把 KDS 声明为真实交付完成，不把 GBrain 检索可用声明为 KDS 全量数据治理完成，不把 `ready_for_review` 声明为客户验收通过。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| 项目路径 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud KDS` |
| Git 分支 | `codex/kds-token-api-kds` |
| 工作树状态 | 存在大量既有修改、删除与未跟踪文件，本轮未回滚 |
| GBrain 命令 | `/Users/lujunxiang/.bun/bin/gbrain` |
| 采集时间 | 2026-06-24 |

## 3. 已执行命令

| 命令 | 结果 | 证据结论 |
|---|---|---|
| `python3 -m pytest tests/test_api_smoke.py` | pass，`2 passed in 3.85s` | API smoke 可运行 |
| `python3 scripts/validate_kds_loop_harness.py` | pass，`declared_rounds=1/30 substantive_rounds=1/30 generated_items=5 batch_generated=false substance_gate=pass` | Loop harness 有实质轮次证据 |
| `python3 scripts/validate_kds_l4_sample_knowledge_index.py` | pass，`retrieval=completed backlinks=linked status=ready_for_review` | L4 样本知识索引可检索且回链已建立 |
| `python3 _governance/scripts/validate_evidence_gates.py --root . --json-out /tmp/kds-evidence-gates-20260624.json --md-out /tmp/kds-evidence-gates-20260624.md` | pass，`gate_count=46 issue_count=0 warning_count=0` | evidence gate 当前通过 |
| `python3 _governance/scripts/validate_rag_export.py --root . --admission _governance/rag_admission_latest.json --allowlist _governance/rag_allowlist_latest.txt --manifest _governance/rag_ingest_manifest_latest.jsonl --json-out /tmp/kds-rag-export-20260624.json --md-out /tmp/kds-rag-export-20260624.md` | fail，`error_count=185 warning_count=1` | RAG 导出仍需修复 |
| `gbrain doctor --json --fast` | warnings，`health_score=95`，DB 检查被 fast 模式跳过 | GBrain 基础健康可用但非全量 DB 验证 |
| `gbrain search "GlobalCloud 绿色供应链"` | pass，返回 `GlobalCloud 绿色供应链体系总架构` 等结果 | 关键词检索可用 |
| `gbrain query "GlobalCloud 绿色供应链体系与 KDS 的关系是什么" --no-expand` | pass，返回 KDS 分布式知识系统、总架构、关系总图等结果 | 混合查询可用 |

## 4. 失败与边界

| 阻塞 | 真实结果 | 影响 |
|---|---|---|
| RAG 准入导出失败 | `missing_file`、`sha256_mismatch`、`byte_size_mismatch`、`allowlist_not_admissible` 等错误合计 185 个 | KDS 不能声明 RAG 导出闭环完成 |
| GBrain doctor 使用 `--fast` | 输出 `connection=warn`，DB checks 被跳过 | 不能声明数据库级全量健康完成 |
| L4 样本状态 | `ready_for_review` | 只能进入审查，不能声明客户验收通过 |
| 工作树脏改 | 存在大量既有 wiki 删除和未跟踪文件 | 本轮只采证，不做回滚或清理 |

## 5. 状态结论

```text
kds_api_smoke = verified
kds_loop_harness = verified
kds_l4_sample_knowledge_index = ready_for_review
kds_evidence_gate = verified
kds_gbrain_search = partial_verified
kds_rag_export = repair_required
kds_real_delivery = not_collected
kds_customer_acceptance = not_collected
```

## 6. 非声明边界

当前不登记 KDS 真实运行闭环完成。

当前不登记 KDS 真实集成完成。

当前不登记 KDS 真实交付完成。

当前不登记 KDS 客户验收通过。
