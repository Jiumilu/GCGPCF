---
doc_id: GPCF-DOC-9F56DFB107
title: GC-Knowledge Fabric P0-D2 目录编号与挂池规则 LOOP evidence
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-GCKF-P0-D2-001.md
source_path: docs/harness/loops/loop-round-GPCF-GCKF-P0-D2-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# GC-Knowledge Fabric P0-D2 目录编号与挂池规则 LOOP evidence

## 本轮目标

完成 P0-D2：固化对象编号规则、KDS 十一池挂接规则、Domain + Pool 双维模型，并生成 pool binding validator 输入清单。

## 本轮输入资料

- `docs/gc-knowledge-fabric/p0-startup-pack-v0.1.md`
- `docs/gc-knowledge-fabric/p0-two-week-execution-schedule-v0.1.md`
- `docs/gc-knowledge-fabric/requirements-confirmation-and-p0-p2-implementation-plan-v0.1.md`

## 本轮新增知识对象

- `docs/gc-knowledge-fabric/object-numbering-rule-v0.1.md`
- `docs/gc-knowledge-fabric/kds-eleven-pool-binding-rule-v0.1.md`
- `docs/gc-knowledge-fabric/domain-pool-dual-model-v0.1.md`
- `docs/gc-knowledge-fabric/pool-binding-validator-input-v0.1.md`
- `docs/harness/loops/loop-round-GPCF-GCKF-P0-D2-001.md`

## 本轮检查

| 检查项 | 结果 |
|---|---|
| 是否真实写入业务系统 | 否 |
| 是否调用生产 KDS API | 否 |
| 是否确认业务事实 | 否 |
| 是否生成 pool binding validator 输入 | 是 |
| 是否保持 v0.1 draft | 是 |

## 风险与阻塞

| 风险 | 等级 | 处理 |
|---|---|---|
| 挂池被误解为事实确认 | P1 | 文档明确挂池不等于事实确认 |
| 无法判断挂池 | P2 | 默认 DATA + repair_required |
| 敏感资料挂池后被开放引用 | P1 | 默认 metadata-only 或 blocked |

## 下一轮动作

进入 P0-D3：

- 建立 OKF ontology。
- 建立 knowledge object schema。
- 建立 domain/pool/trust/flow policy。
- 准备 YAML/JSON parse 校验。
