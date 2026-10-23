---
doc_id: GPCF-DOC-SIGNATURE-ENFORCEMENT-PLAN-20261022
title: 强制签名策略实施方案（CONFLICT-05 残留，2026-10-22）
project: GPCF
related_projects: [GPCF, WAME, XWAIL]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/docs/harness/evidence/signature-enforcement-plan-20261022.md
source_path: docs/harness/evidence/signature-enforcement-plan-20261022.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# 强制签名策略实施方案（CONFLICT-05 残留）

> 现状：WAME 仅记录 `signature_status`（formal / no_signature / invalid_signature），不拒绝。
> 本文件是实施方案，未落代码；落代码须在 WAME `wame/architecture-contracts` 分支执行（WAME AGENTS 分支绑定）。

## 1. 目标策略

| 模式 | 行为 |
|---|---|
| `record_only`（默认，现行为） | 记录三态，不拒绝 |
| `formal_required` | 发布阶段要求 `signature_status=formal`；否则 `RejectError("XAP-2001", ...)` |
| PoC 例外 | 显式 allowlist（`XAP_POC_PACKAGE_PREFIXES`）或 `requestType` 标记；PoC 发布仍标 `no_signature`，不得作为治理证据 |

## 2. 建议 diff（WAME `server/xap-intake/intake_core.py`）

```python
SIGNATURE_POLICIES = {"record_only", "formal_required"}

def _signature_policy() -> str:
    mode = os.environ.get("XAP_SIGNATURE_POLICY", "record_only").strip().lower()
    return mode if mode in SIGNATURE_POLICIES else "record_only"

def _is_poc_package(package_id: str) -> bool:
    prefixes = [p.strip() for p in os.environ.get("XAP_POC_PACKAGE_PREFIXES", "").split(",") if p.strip()]
    return any(package_id.startswith(p) for p in prefixes)
```

在 `publish()` 计算 `signature_status` 后：

```python
if _signature_policy() == "formal_required" and signature_status != "formal":
    if not _is_poc_package(package_id):
        raise RejectError("XAP-2001", f"正式治理要求签名（当前 {signature_status}）")
```

## 3. 测试

1. 默认 `record_only`：现有 no_signature 发布不受影响（回归）。
2. `formal_required` + 无签名：`publish` 抛 XAP-2001。
3. `formal_required` + PoC allowlist：允许发布，`signatureStatus=no_signature`。
4. `formal_required` + formal 签名：允许发布。

## 4. 回滚

- 清空/设 `XAP_SIGNATURE_POLICY=record_only` 即回旧行为；
- 无 DB 迁移（仅新增环境变量读取）。

## 5. 未执行原因

- 当前 WAME 分支为 `wame/pm-governance`；按其 AGENTS「PM 综合管理会话禁止业务代码实现」与「一对话一分支」，本代码改动须切 `wame/architecture-contracts` 或新开架构/契约会话执行。
- 本文件仅方案，不构成已落仓。

## 6. 非声明

- 不声明强制签名已启用；不声明 CONFLICT-05 残留已关闭；不声明任何项目状态提升。
