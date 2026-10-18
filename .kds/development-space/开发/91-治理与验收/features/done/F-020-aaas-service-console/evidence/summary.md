---
doc_id: GPCF-F-020-EVIDENCE-SUMMARY-AAAS-SERVICE-CONSOLE
title: F-020 证据索引（evidence summary）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-020-aaas-service-console/evidence/summary.md
source_path: features/done/F-020-aaas-service-console/evidence/summary.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# F-020 证据索引（evidence summary）

## 2026-10-18 追溯复核

原 `tests.txt` 只校验 GPCF Feature 工作区，原 `build.txt` 只编译 GPCF 脚本；两者都不能证明 AaaS 服务台六视图、WAE 装配或 AaaS 服务数据面。历史截图保留，但当前 WAE 工作区有未提交改动，且 `apps/wae-console` 不存在；AaaS 工作区亦有未提交改动。本次未能回放浏览器流程、产品构建和数据接口，以下历史记录不作为当前验收。

复核结果为 `partial`：`python3 scripts/gpcf_check_evidence.py F-020 --check-only` 返回 1、`close_candidate=false`，指出证据未齐、阻塞项未清及缺少专属测试/构建命令。当前 `tests/build/screenshots/api=fail`，`summary=pass` 只表示本追溯记录已写入。历史 `done` 仅保留原关闭事实，不声明 `integrated`、`accepted` 或 `production_ready`。待可构建入口和稳定数据基线具备后，按六视图、只读边界和服务包数据契约逐项重跑。

> 交付方式：本线（Hermes）实施 M1-M2；本目录为**如实**证据索引（每条可溯源）。

## 1. 数据面（AaaS 侧）

| 项 | 结果 |
|---|---|
| 导出器 | `tools/export_aaas_state.py` 真跑·findings=0·ok=True |
| 服务包 | 1（绿链示例·19 顶层键）·schema 1·docs 3 |
| 四校验器实跑 | validate_service_package / validate_metering / validate_sla / verify_evidence_requirements → **exit0 ×4·high 0 ×4** |
| 警示透传 | "本地校验不证明真实计费/结算/SLA/交付/发布"（如实） |

## 2. 提交记录（changelog）

| 仓 | 提交 | 说明 |
|---|---|---|
| AaaS | `84424e5` | 导出器 v0.1＋.gitignore（M1·D1.1） |
| WAE | `01e3c3a` | 模块包＋母本第 8 项＋对账表 v0.8（M2） |
| KDS | `e8c6c490` | registry v0.8（aaas-console available·README 17） |
| KDS | `9c134a82` | 规划件 v0.1＋总索引登记 |

## 3. E2E 真机（浏览器）

- 地址：`http://localhost:4300/global-cloud-workbench/aaas`（WAE 母本·第 8 项）。
- 六页签：概览/服务包/计量与SLA/证据与退出/校验器/总方案——切换实测通过。
- 关键断言：概览 1/1/4-of-4/3｜服务包 green-supply-chain.basic＋八维｜校验器 4 卡 exit0。
- 截图（入库）：`evidence/ui-browser-e2e-overview.png`。

## 4. 诚实记录（不作为验收声明）

- 只读边界：模块零写路径（grep）；导出器只读＋本地校验不改包。
- 商业候选态：candidate_only／realBillingEnabled:false／not_enforced_local_dev 如实标注；`production_ready=false`。
- 范围外：真实计费/结算/SLA 强制/客户交付（业务边界外·非本 Feature 缺陷）。

<!-- GPCF_EVIDENCE_GATE_START -->
## Evidence Gate 快照

本文件记录当前 Feature 的本地可回放证据结果，仅用于关闭候选判断，不代表提交、推送、部署、真实接口调用或项目状态提升。

- tests: pass
- build: pass
- screenshots: pass
- api: waived
- lint: 已通过 build 证据中的 git diff --check 覆盖。
- risk: 未授权 commit、push、deploy、真实 API、状态提升。
<!-- GPCF_EVIDENCE_GATE_END -->
