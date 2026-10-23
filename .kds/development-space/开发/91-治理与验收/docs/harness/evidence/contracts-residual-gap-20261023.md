---
doc_id: GPCF-DOC-CONTRACTS-RESIDUAL-GAP-20261023
title: 契约残留差距分析（2026-10-23）
project: GPCF
related_projects: [GPCF, XWAIL, WAME, AAAS, XiaoC]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/contracts-residual-gap-20261023.md
source_path: docs/harness/evidence/contracts-residual-gap-20261023.md
sync_direction: bidirectional
last_reviewed: 2026-10-23
supersedes: []
superseded_by: []
---

# 契约残留差距分析（2026-10-23）

> 8/8 冲突已 closed；本文件跟踪 **closure 中登记的残留**，属后续加固，不影响 closed 结论。

## 1. 总表

| 冲突 | 已落 | 残留 | 属主 | 下一步 |
|---|---|---|---|---|
| 03 casing | XAP §九规则 + 3 转换点 | 未全量消费者逐字段审计 | GPCF + 消费方 | 列消费者清单，抽查字段映射 |
| 04 版本 | manifest v1.2 contentHash + 正负例；漂移 validator 已入 CI | ~~无自动漂移告警~~（已由 `validate_contract_version_drift.py` 补齐，覆盖 4 契约） | GPCF | 扩展契约清单（事件/连接器/canonical） |
| 05 签名 | manifest 显式 signature/digest；WAME signature_status 三态；PoC no_signature | 正式受理未强制拒绝；未新增错误码 | WAME（architecture-contracts 分支） | 按 signature-enforcement-plan 落码 |
| 06 幂等 | 事件 §14.2/14.3 packageRef + 三段映射；packageRef schema + validator | 运行时未消费 packageRef；无完整事件信封 schema | WAME/事件 owner | 事件运行时读取 packageRef；补完整 envelope schema |
| 08 命名 | 事件 §14.4 + 连接器别名/legacy superseded | 运行时域名/连接器代码未改名 | WAE/WAME | 迁移域名与连接器编号，保留 legacy 别名一版 |

## 2. 结论

- 04 的“无自动漂移告警”残留**已由本会话补齐**（漂移 validator + CI），可更新 closure 说明。
- 05/06/08 残留均需跨仓代码或运行时改造，且受 WAME 分支/事件运行时约束。
- 03 为审计类残留，可增量补。

## 3. 非声明

- 不声明残留已清零；不声明任何项目状态提升。
