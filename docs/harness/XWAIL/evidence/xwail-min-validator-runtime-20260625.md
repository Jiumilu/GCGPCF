---
doc_id: GPCF-DOC-XWAIL-MIN-VALIDATOR-RUNTIME-20260625
title: XWAIL 最小 Validator/XAP 运行证据 2026-06-25
project: GPCF
related_projects: [GPCF, WAES]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/XWAIL/evidence/xwail-min-validator-runtime-20260625.md
source_path: docs/harness/XWAIL/evidence/xwail-min-validator-runtime-20260625.md
sync_direction: bidirectional
last_reviewed: 2026-06-25
supersedes: []
superseded_by: []
---

# XWAIL 最小 Validator/XAP 运行证据 2026-06-25

## 1. 证据定位

本文登记 `XWAIL-MIN-VALIDATOR-001` 的本地真实执行结果。

本文只证明 XWAIL 仓已建立最小本地 Validator、XAP build check 和 XAP verify 命令入口。本文不声明完整 XWAIL 工具链完成，不声明 WAES 授权或发布，不声明 AaaS 绑定，不声明业务交付或客户验收。

## 2. 执行环境

| 项 | 内容 |
|---|---|
| XWAIL 仓库 | `/Users/lujunxiang/Projects/GlobalCloud V0.0.1/GlobalCloud XWAIL` |
| 执行日期 | 2026-06-25 |
| 缺口复现目录 | `/tmp/xwail-min-validator-20260625-090336` |
| 通过复跑目录 | `/tmp/xwail-min-validator-20260625-090607` |
| 初始状态 | `scripts/validate_xwail.py`、`scripts/build_xap.py`、`scripts/verify_xap.py` 均不存在 |
| 本轮修改边界 | 只新增最小本地 Draft 模型、Draft XAP manifest、JSON schema 占位和三个本地验证脚本 |

## 3. 初始失败

首次运行规划命令失败：

```text
python3 scripts/validate_xwail.py --all
can't open file .../scripts/validate_xwail.py: [Errno 2] No such file or directory

python3 scripts/build_xap.py --check
can't open file .../scripts/build_xap.py: [Errno 2] No such file or directory

python3 scripts/verify_xap.py --all
can't open file .../scripts/verify_xap.py: [Errno 2] No such file or directory
```

## 4. 新增实现

| 类型 | 文件 |
|---|---|
| 共享校验逻辑 | `scripts/xwail_common.py` |
| XWAIL 模型校验命令 | `scripts/validate_xwail.py` |
| XAP build check 命令 | `scripts/build_xap.py` |
| XAP verify 命令 | `scripts/verify_xap.py` |
| 最小 XWAIL 样例 | `models/examples/warehouse-basic.xwail.json` |
| 最小 XAP 包 | `packages/examples/logistics/manifest.xap.json` |
| XAP 内模型 | `packages/examples/logistics/models/warehouse-basic.xwail.json` |
| JSON Schema 占位 | `schemas-json/xwail-core.schema.json`、`schemas-json/xap-manifest.schema.json` |

最小校验覆盖：

- WAS 八维：`Physical`、`Rule`、`Intellectual`、`Data`、`Economic`、`Energy`、`Organization`、`SpaceTime`。
- WAS 八流枚举边界。
- `ontologyRef` 必填。
- `wasBaseline`、`ontologyVersion`、`xwailVersion` 必填。
- `waesStatus` 受控，且 `Authorized`/`Published` 必须有 WAES evidence。
- XAP manifest 必须声明 WAS/Ontology/XWAIL/Profile/AaaS/WAES 兼容字段和 rollback 边界。

## 5. 复跑命令与结果

| 命令 | 结果 |
|---|---|
| `python3 scripts/validate_xwail.py --all` | pass，`checked=2 issue_count=0 high_count=0` |
| `python3 scripts/build_xap.py --check` | pass，`checked=1 issue_count=0 high_count=0`，模型 digest 为 `b99644c9b3fbc83303c7dc5ef09d8ffc200c310ee9a311c5f4607cdf9e05aecd` |
| `python3 scripts/verify_xap.py --all` | pass，`checked=1 issue_count=0 high_count=0` |

命令输出均包含边界：

```text
validator success is not WAES publication, AaaS binding, business delivery, or customer acceptance
```

## 6. 状态建议

```text
xwail_min_validator = verified_with_local_dev_boundary
xwail_validate_all = pass
xap_build_check = pass
xap_verify_all = pass
xwail_checked_models = 2
xap_checked_manifests = 1
xwail_status_candidate = ready_for_review
waes_status = Draft
accepted = false
integrated = false
production_ready = false
customer_accepted = false
```

## 7. 保留边界

| 边界 | 说明 |
|---|---|
| local dev only | 本轮只证明本地 Draft 样例、Draft XAP 和最小命令入口通过 |
| incomplete toolchain | 不代表完整 XSD、JSON Schema、Policy as Code、CI、签名、迁移和编辑器工具链完成 |
| no WAES publication | `waesStatus=Draft`，未注册、未授权、未发布 |
| no AaaS binding | `aaasServicePackageVersion=not-bound` |
| no customer acceptance | 没有客户验收人、验收场景或签收证据 |

## 8. 下一步

1. 将 XWAIL 最小 Validator 作为 `WAES -> XWAIL -> AaaS` 链路的本地契约输入。
2. 下一轮可推进 AaaS 最小 ServicePackage/Metering/SLA/EvidenceRequirement 命令。
3. WAES 仍需用户授权后才能修复 lint/runtime 并接入 XWAIL 结果。
