---
doc_id: GPCF-DOC-07ADF1B23E
title: Headroom L2 Project Group Dry Run Evidence
project: KDS
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, Brain, PKC, XiaoC, XGD, XiaoG, MMC, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md
source_path: docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.md
sync_direction: bidirectional
last_reviewed: 2026-06-23
supersedes: []
superseded_by: []
---

# Headroom L2 Project Group Dry Run Evidence

## Evidence ID

`HEADROOM-L2-PROJECT-GROUP-DRY-RUN-20260621`

## 结论

本轮完成 Headroom 项目群 L2 dry-run 样本测量链路：15 个项目/域均已从受控文档或 evidence 中提取样本，生成 token before/after、成本 before/after、saving_rate、marker 保真和 admission gate。

当前 `compressor_mode=structured_surrogate_no_headroom_runtime`。这证明项目群级成本模型和 Loop 测量链路可执行，不证明真实 `headroom-ai` runtime 已安装、真实 Headroom 压缩器已接入、生产 token 节省已经发生，或任何项目已 accepted、integrated、production_ready。

## 覆盖范围

| 字段 | 值 |
|---|---|
| project_count | 15 |
| projects_covered | GPCF, KDS, Brain, WAES, GFIS, GPC, PVAOS, Edge, PKC, XiaoC, XGD, XiaoG, MMC, Studio, WAS |
| source_fixture | `fixtures/headroom/headroom-l2-project-group-sources.json` |
| evidence_json | `docs/harness/evidence/headroom-l2-project-group-dry-run-20260621.json` |
| generator | `tools/kds-sync/generate_headroom_l2_project_group_dry_run.py` |
| validator | `tools/kds-sync/validate_headroom_l2_project_group_dry_run.py` |

## 测量摘要

| 指标 | 当前值 |
|---|---:|
| input_tokens_before | 224759 |
| input_tokens_after | 2359 |
| baseline_cost | 292186.55 |
| headroom_cost | 3066.15 |
| gross_saving | 289120.4 |
| saving_rate | 0.989506 |
| all_admission_gates_pass | true |

## 安全边界

- `HEADROOM_TELEMETRY=off` 口径保持。
- 不保存原始敏感文本。
- 不启用跨项目 memory。
- 不写真实 KDS。
- 不执行真实外部 API 写入。
- 不生产代理、不部署、不提交、不推送。
- 不升级 accepted、integrated 或 production_ready。

## 下一步

下一轮应扩大真实 tool-output payload 样本，保持 telemetry off，并用同一 source fixture 复跑，比较真实压缩器、runtime adapter 与 structured surrogate 的 saving_rate、marker 保真和 retrieval miss。
