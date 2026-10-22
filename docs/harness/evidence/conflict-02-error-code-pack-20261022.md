---
doc_id: GPCF-DOC-CONFLICT-02-ERROR-CODE-PACK-20261022
title: CONFLICT-02 XAP 错误码裁决包（2026-10-22）
project: GPCF
related_projects: [GPCF, XWAIL, WAME]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/conflict-02-error-code-pack-20261022.md
source_path: docs/harness/evidence/conflict-02-error-code-pack-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# CONFLICT-02 XAP 错误码裁决包（2026-10-22）

> 依据：`runtime/contract-matrix.yaml` CONFLICT-02；三处错误码清单不一致。
> 性质：选项包，不代替老卢裁决；不修改代码/契约。

## 1. 现状

| 来源 | 已登记错误码 |
|---|---|
| GPCF《XWAIL-V1.2-Validator 规则清单》 | XAP-1001/1002/1003/2001/2002/2003/2004/5001 |
| XAP 回执规格正文 | XAP-1003/5001/6001/6002/6003/6004/6005/6006 |
| WAME 受理实现 | XAP-2004/4001/5001/5002/5003/6001/6002/6003/6004/6006 |

差异：4001/5002/5003 仅在实现；2002/2003/6005 仅在清单/规格；2004 规格未定义。

## 2. 选项

| 选项 | 做法 | 优点 | 代价 |
|---|---|---|---|
| **A（建议）** | 建 **XAP 错误码注册表**（YAML：码/语义/引入版本/提出方/是否可重试），三处引用同一注册表；未注册码禁止进入实现 | 单一权威；可机器校验 | 需补 4xxx/5xxx 段并改三方引用 |
| B | 以 WAME 实现为准，回写规格与清单 | 改动少 | 实现可能含临时码，规格失真 |
| C | 只做三方映射表，不改实现与规格 | 最快 | 码位仍可能冲突，映射表成新单点 |

## 3. 建议

A：错误码是跨系统稳定分支处理依据，必须有单一权威；映射表不能阻止未来新增码冲突。

## 4. 后续实施

1. 新建 `runtime/xap-error-code-registry.yaml`（GPCF）。
2. XWAIL/WAME 改为引用注册表；未注册码在 CI 阻断。
3. 补 4xxx/5xxx 语义与可重试性。
4. 负例：未注册码被拒。

## 5. 非声明

- 不声明错误码已统一；不声明契约冻结；不声明任何项目状态提升。
