---
doc_id: GPCF-DOC-L3-ADMISSION-20260613
title: GlobalCloud L3 Admission Matrix
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF]
domain: status
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/09-status/globalcloud-l3-admission-matrix.md
source_path: 09-status/globalcloud-l3-admission-matrix.md
sync_direction: bidirectional
last_reviewed: 2026-06-13
supersedes: []
superseded_by: []
---

# GlobalCloud L3 Admission Matrix

日期：2026-06-13
来源：`python3 tools/kds-sync/assess_l3_admission.py`
机器证据：`docs/harness/evidence/l3_admission_assessment.json`

## 评分模型

| 维度 | 分值 |
|---|---:|
| 真实项目仓 | 10 |
| L3 任务队列 | 10 |
| 代码/配置闭环 | 15 |
| 测试/验证命令 | 15 |
| evidence 体系 | 10 |
| loop-state | 8 |
| Git 门禁 | 8 |
| 风险/回滚 | 8 |
| 跨项目依赖 | 6 |
| 可用性/客户满意 | 5 |
| 自我进化 | 5 |

## 准入结果

| 项目 | 代号 | 分数 | 准入状态 | 主要缺口 |
|---|---|---:|---|---|
| GFIS | GF | 97 | L3 Ready | 自我进化机制仍可深化 |
| GPC | GP | 79 | L2.5 | 缺 loop-state；evidence 不完整；L3 队列不足；自我进化不足 |
| PVAOS | PV | 76 | L2.5 | 缺 loop-state；evidence 不完整；可用性/客户满意不足 |
| WAES | WA | 73 | L2.5 | 缺 loop-state；evidence 不完整；可用性/客户满意不足 |
| KDS | KD | 94 | L3 Ready | 自我进化机制仍可深化 |
| Brain | BR | 97 | L3 Ready | 自我进化机制仍可深化 |
| PKC | PK | 92 | L3 Ready | 自我进化机制仍可深化 |
| XiaoC | XC | 97 | L3 Ready | 自我进化机制仍可深化 |
| XGD | XD | 85 | L3 Conditional | L3 队列不足；自我进化不足 |
| XiaoG | XG | 82 | L3 Conditional | 真实代码/配置、validator、smoke test、loop-state、evidence 已补齐；Git dirty、风险/回滚、可用性和自我进化仍需补齐 |
| MMC | MM | 97 | L3 Conditional | L3 队列、自我进化、依赖 dry-run、运行态测试均已闭合；因工作区尚未提交，Git 门禁限制为 L3 Conditional |
| GPCF | CF | 76 | governance_hub | 总控仓以治理中枢单独判定，不作为业务 L3 Ready |

## MMC 实质整改记录

| 字段 | 结果 |
|---|---|
| Round ID | `GPCF-MM-LR-002` |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 2 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | none |
| 分数变化 | 71 -> 89 |
| 状态变化 | L2.5 -> L3 Conditional |

| 字段 | 结果 |
|---|---|
| Round ID | `GPCF-MM-LR-003` |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 2 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | none |
| 本轮闭合缺口 | KDS/Brain/PKC dependency dry-run evidence |
| 更新后剩余缺口 | Git 工作区未提交；自我进化机制不足；L3 队列仍需结构化 |

| 字段 | 结果 |
|---|---|
| Round ID | `GPCF-MM-LR-004` |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 2 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | none |
| 本轮闭合缺口 | self-evolution checklist；next L3 task queue |
| 更新后剩余缺口 | Git 工作区未提交，需授权后准备 commit-readiness / commit / push |
| 分数变化 | 89 -> 97 |
| 状态说明 | 分数达到 L3 Ready 区间，但 Git dirty，按门禁保持 L3 Conditional |

| 字段 | 结果 |
|---|---|
| Round ID | `GPCF-MM-LR-005` |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 2 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |
| 本轮闭合缺口 | commit-readiness evidence |
| 更新后剩余缺口 | Git 工作区仍未提交；实际 stage/commit/push 需明确授权 |
| 分数变化 | 97 -> 97 |
| 状态说明 | 已具备本地提交就绪证据；未授权提交前仍为 L3 Conditional |

本轮真实落地点在 MMC 项目仓：

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/scripts/validate_mmc_l3_admission.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/scripts/dry_run_mmc_dependencies.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/scripts/validate_mmc_self_evolution.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/scripts/validate_mmc_commit_readiness.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/self-evolution-checklist.json`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/loops/loop-round-GPCF-MM-LR-002.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/loops/loop-round-GPCF-MM-LR-003.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/loops/loop-round-GPCF-MM-LR-004.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/loops/loop-round-GPCF-MM-LR-005.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/loop-state.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud MMC/docs/harness/evidence/evidence-index.md`

验证结果：

| 命令 | 结果 |
|---|---|
| `python3 scripts/validate_mmc_loop_harness.py` | pass |
| `python3 scripts/validate_mmc_l3_admission.py` | pass |
| `python3 scripts/dry_run_mmc_dependencies.py` | pass; KDS/Brain/PKC dependency dry-run, no production write, no real external API, no token read |
| `python3 scripts/validate_mmc_self_evolution.py` | pass |
| `python3 scripts/validate_mmc_commit_readiness.py` | pass; `stage=false commit=false push=false sensitive_paths=0 unexpected_paths=0` |
| `MMC_TEST_MODE=true python3 -m pytest runtime/tests -q` | 30 passed |
| `bash runtime/scripts/contract_test.sh` | pass |
| `git diff --check -- .` | pass |
| `python3 tools/kds-sync/assess_l3_admission.py` | pass |

## 约束

- 该矩阵是 L3 准入评估，不是业务验收结论。
- 任何项目不得因分数达到 L3 Ready 自动升级为 `accepted` 或 `integrated`。
- MMC 本轮未执行 Git push、生产写入、真实外部 API 写入、数据库迁移、权限变更、Registry 退役或部署。
- 下一实质轮次可在明确授权后执行 MMC commit/push；若未授权，则应转入下一个低分真实项目仓。

## XiaoG 实质整改记录

| 字段 | 结果 |
|---|---|
| Round ID | `XiaoG-LR-001` |
| declared_rounds | 1/15 |
| substantive_rounds | 1/15 |
| generated_items | 6 |
| batch_generated | false |
| substance_gate | pass |
| stop_type | authorization_boundary |
| 本轮闭合缺口 | 真实代码/配置识别；项目级 validator；smoke test；loop-state；evidence |
| 更新后剩余缺口 | Git 工作区未提交；风险/回滚；可用性/客户满意；自我进化机制 |
| 分数变化 | 29 -> 82 |
| 状态变化 | L1/L0 -> L3 Conditional |

XiaoG 本轮真实落地点：

- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/scripts/validate_xiaog_l3_bootstrap.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/scripts/test_xiaog_l3_bootstrap.py`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/docs/harness/README.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/docs/harness/loop-state.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/docs/harness/evidence/evidence-index.md`
- `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XiaoG/docs/harness/loops/loop-round-XiaoG-LR-001.md`

验证结果：

| 命令 | 结果 |
|---|---|
| `python3 scripts/validate_xiaog_l3_bootstrap.py` | pass |
| `python3 scripts/test_xiaog_l3_bootstrap.py` | pass |
| `git diff --check -- .` | pass |
| `python3 tools/kds-sync/assess_l3_admission.py` | pass |

约束：

- 本轮未执行 Docker 部署、设备 OTA、真实外部 API、Token 读取、提交、推送或 accepted/integrated 升级。
