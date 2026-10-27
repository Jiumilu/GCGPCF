---
doc_id: GPCF-DOC-PJ03-WAS-FEATURE-REVIEW-20261022
title: PJ-03 WAS F-022/F-023 状态复核与 P4 输入清单（2026-10-22）
project: GPCF
related_projects: [WAS, GPCF, GFIS, GPC]
domain: status
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/pj03-was-feature-review-20261022.md
source_path: docs/harness/evidence/pj03-was-feature-review-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# PJ-03 WAS F-022/F-023 状态复核与 P4 输入清单

> 任务：PJ-03（WAS：F-022/F-023 收口 + P4 输入清单）。性质：只读复核 + 输入清单；不关闭 Feature、不改状态、不写 WAS 仓。

## 1. 复核结果

| Feature | 优先级 | close_candidate | 失败原因（`gpcf_check_evidence.py` 原文归并） |
|---|---|---|---|
| `F-022-was-scenario-flow-extension` | P2 | false | evidence 不完整；governance blockers 仍在；tests/build 命令未声明；screenshots/api 豁免无本 Feature 理由 |
| `F-023-was-flow-naming-migration` | P2 | false | 同上 |

结论：**两个 Feature 均不能关闭**。共性问题不是代码，而是证据规则未声明；个性问题是 F-022 需 WAS 治理复核与 XWAIL flowType 影响评估，F-023 需兼容窗口与存量引用排期。

## 2. 收口建议

### F-022（场景流扩展）
1. 完成 WAS 治理复核（裁定文本一致性已具备，需治理方确认）。
2. 补 XWAIL flowType 影响评估结论。
3. 声明 Feature 专属 tests/build 命令（建议由 WAS owner 从 `scripts/alignment_scan.py` / `gen_flow_consts.py` 中确认可回放入口，**未确认前不得写 pass**）。
4. 补 screenshots/api 豁免的本 Feature 理由。
5. 满足后再跑一次 `gpcf_check_evidence.py`，仍不得自动关闭。

### F-023（命名迁移）
1. 明确兼容窗口关闭时点与存量引用切换排期。
2. 补术语迁移表与 validator 的可回放命令。
3. 补 screenshots/api 豁免理由。
4. 满足后再判定。

## 3. P4 真实输入清单（供 PG-05）

> 来源：`09-status/gpcf-project-status-matrix.md` WAS 行；当前 `real_source_records=0`、`valid_source_records=0`、`formal_confirmation_files=0`。

| # | 输入 | 用途 | 待确认 owner |
|---:|---|---|---|
| 1 | 真实客户订单原件或平台订单回执 | 触发 P4 真实业务验证 | GPC / 辽宁远航订单 owner |
| 2 | 客户确认的产品规格 | 校验对象与规格一致性 | 客户 / 销售 owner |
| 3 | 交付要求 | 运行层验收依据 | 业务 owner |
| 4 | 签发方与责任方确认 | 权威签署与责任归属 | 签发方 |
| 5 | KDS source backlink + runtime site context | 事实源与运行上下文 | KDS / 现场 owner |

纪律：未取得上述真实输入前，`real_source_records` 保持 0；不得以 fixture / 治理 validator 替代真实 source-record。

## 4. 非声明

- 不声明 F-022/F-023 已关闭或可关闭；
- 不声明 WAS 真实业务验证或客户验收；
- 不声明任何 `accepted` / `integrated` / `production_ready` / `customer_accepted`。
