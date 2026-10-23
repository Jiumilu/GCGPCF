---
doc_id: GPCF-DOC-0EB767BDC4
title: XWAIL 状态
project: XWAIL
related_projects: [XWAIL]
domain: governance
status: controlled
version: v1.1
owner: XWAIL
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/xwail/STATUS.md
source_path: projects/xwail/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# XWAIL 状态

本文件只记录 XWAIL 的当前项目节奏状态。功能级进度、证据、阻塞和关闭状态统一由 features 目录中的 feature.yaml 承载。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/xwail-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project xwail`
- 默认 Loop：`Delivery`
- Evidence/Harness：`required/required`

## 2026-10-22 当前状态

- **活跃 Feature：0**。`features/active/` 下 23 个活跃 Feature 无一登记到 XWAIL（`runtime/queue.json` 无 `project: xwail` 条目）。
- **当前阶段**：`ready_for_review / local_dev_boundary / integration_precheck_candidate / wrapper_review_required`（文档声明，见 `09-status/globalcloud-core-chain-real-evidence-register.md` XWAIL 行）。
- **已通过的本地能力**：XWAIL 最小 Validator、XAP build check、XAP verify 三条命令 + AaaS ServicePackage/Metering/SLA/EvidenceRequirement 四条命令，共 7 条本地命令、`commands_failed=0`。
- **阻塞一：delegated wrapper replay 未确认**——约束任务 `XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001` 未收口，状态被压在 `wrapper_review_required` 之下，需人工确认后才能向下游传导。
- **阻塞二：WAME 出口未修复**——同批证据记 `wame_status = repair_required / authorization_boundary`，`WAME -> XWAIL -> AaaS` 链断在 WAME 侧，XWAIL 无法单方推进。
- **XAP 打包/验包在 GPCF 2.0 中仅以 F-033（xiaoc）PoC 范围承接**，未形成 XWAIL 自己的 Feature 验收。

## 已知证据

| 证据 | 路径 | 一句话 |
|---|---|---|
| 契约预检证据 | `docs/harness/XWAIL/evidence/xwail-wame-aaas-contract-precheck-20260625.md` | 7 条本地命令全 pass；`result = xwail_wame_aaas_contract_precheck = pass`、`xwail_status_candidate = integration_precheck_candidate`；**文件自述不执行 WAME 发布、不证明生产绑定** |
| 证据一致性校验脚本 | `tools/kds-sync/validate_xwail_wame_aaas_contract_precheck.py` | 对该证据与登记文本做校验（本次未复跑） |
| 状态登记 | `09-status/globalcloud-core-chain-real-evidence-register.md` | 记 `wrapper_review_required` 与 delegate review replay 约束为当前前置 |
| 阶段推进矩阵 | `docs/harness/evidence/globalcloud-project-group-status-advancement-matrix-20260625.md` | 记 XWAIL 当前态与「delegated wrapper replay 未确认」 |
| F-033 PoC 承接范围 | `features/active/F-033-r1-ecosystem-integration/feature.yaml` | XAP manifest 打包与完整性验包在 PoC scope 内；`WAME 正式治理裁定/发布` 未做 |
| 项目级方案 | `../GlobalCloud XWAIL/GlobalCloud XWAIL 实施方案.md`、`../GlobalCloud XWAIL/XWAIL实施方案.md` | 项目实施方案入口（仅确认存在，本轮未复跑其命令） |

证据分级：上表契约预检为**本地集成预检（local dev boundary）**，非真实业务运行；**未执行** WAME 发布、AaaS 真实绑定、真实外部 API 写入或部署。

## 到下一状态门的关键缺口

1. **delegated wrapper replay 未确认**（`XWAIL-LOOP-GATE-DELEGATE-REVIEW-REPLAY-20260627-001`），XWAIL 停在 `wrapper_review_required`，状态无法传导。
2. **无 Feature 载体**：XWAIL 的 validator/XAP 能力未进入 GPCF 2.0 Feature 队列，没有 `feature.yaml`、`evidence` 与 `gpcf_check_evidence.py` 级可回放结果。
3. **WAME 侧出口未闭合**：`repair_required / authorization_boundary` 未解除，`WAME -> XWAIL -> AaaS` 前置链未通。
4. **XAP 验包无签名**：F-033 记为「XWAIL 包完整性通过（无签名）」，签名与正式发布未验证。

## 本轮不做与非声明

- 不声明 `accepted`、`integrated`、`production_ready`、`customer_accepted`。
- 不声明完整工具链闭环、WAME 发布或 AaaS 绑定完成（与契约预检证据自述边界一致）。
- 不替代 XWAIL 项目实施方案，也不替代任何 Feature 的 `feature.yaml` / `evidence`。
- 本页只记项目级节奏与缺口；上表结论来自受控文档，未在本轮复跑命令。
- 本轮未 commit、未 push。
