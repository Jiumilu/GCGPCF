---
doc_id: GPCF-DOC-26AF30C1B1
title: GlobalCloud MMC Project Harness Manifest
project: MMC
related_projects: [GFIS, GPC, WAES, KDS, MMC, GPCF]
domain: docs
status: controlled
version: v1.0
owner: MMC
kds_space: 开发
kds_path: 开发/11-MMC/docs/harness/MMC/PROJECT_HARNESS_MANIFEST.md
source_path: docs/harness/MMC/PROJECT_HARNESS_MANIFEST.md
sync_direction: bidirectional
last_reviewed: 2026-06-24
supersedes: []
superseded_by: []
---

# GlobalCloud MMC Project Harness Manifest

## 项目定位

MMC 是 GlobalCloud 项目群的管理配置中心与治理模板基线，负责把项目群可复用的配置、模板、准入规则、质量门禁、状态判定口径和受控目录结构沉淀为可执行治理资产。

## 最小闭环目标

| 目标 | 描述 | 状态 |
|---|---|---|
| 治理模板基线 | 汇总 Loop、Harness、KDS、文档控制、验收模板的统一入口 | planned |
| 配置标准化 | 建立项目级配置项、状态项、准入项、风险项和回滚项的字段口径 | planned |
| 门禁复用 | 将 GPCF 已验证的文档门禁、污染检查、KDS 检查抽象为项目群复用清单 | planned |
| 证据可追溯 | 为 MMC 自身建立 loop-state、evidence-index 和 loop records | initialized |

## 边界

- MMC 不承接 GFIS 工厂事实主账。
- MMC 不承接 GPC 客户协同、合同、回款或 POD 主责。
- MMC 不承接 KDS 知识主存和真实 Token 存储。
- MMC 不承接 WAES 的最终验收裁决权。
- MMC 只沉淀配置、模板、治理字段和准入标准。

## 当前门禁

| 门禁 | 当前值 |
|---|---|
| loop-state | initialized |
| evidence-index | initialized |
| accepted/integrated | forbidden_without_human_acceptance |
| Git push | not_done |
| KDS Token | pass via GPCF private env, fingerprint=bfd9553d |
| 生产写入 | not_applicable |

Current state remains `partial` until MMC 真实项目仓、模板复用验证、跨项目引用和人工验收完成。
