---
name: globalcloud-document-governance
description: GlobalCloud 项目群文档综合治理技能。用于文档治理、KDS 开发空间同步、Loop 文档门禁、文档受控检查、防污染检查、文档健康报告、KDS TOKEN 安全检查，确保项目群所有工作在文档中有体现、受控、更新、真实、防污染并纳入 KDS。
---

# GlobalCloud Document Governance

本技能用于 GlobalCloud 项目群的文档综合治理。触发后默认以当前 GPCF 仓库为治理源，以 KDS `开发` 空间为知识主存镜像。

## 必做流程

1. 读取项目现有文档控制台账：
   - `09-status/globalcloud-document-control-register.md`
   - `09-status/kds-development-space-sync-register.md`
   - `09-status/document-deprecation-register.md`
2. 执行或更新 `tools/kds-sync/document_control.py`，保证新增/修改文档进入受控台账和 KDS 本地镜像。
3. 执行污染检查：`python3 tools/kds-sync/check_document_pollution.py`。
4. 执行 KDS TOKEN 检查：`python3 tools/kds-sync/validate_kds_token.py`。
5. 执行 Loop 文档门禁：`python3 tools/kds-sync/loop_document_gate.py`。
6. 若用户要求健康报告，生成或更新 `09-status/globalcloud-document-health-report.md`。

## 规则入口

- 文档控制规则：读取 `references/document-control-policy.md`。
- Loop 纳入规则：读取 `references/loop-integration-policy.md`。
- KDS TOKEN 与安全规则：读取 `references/kds-security-policy.md`。
- 防污染规则：读取 `references/anti-pollution-rules.md`。

## 硬约束

- 不写入真实 TOKEN。
- 不把 KDS 本地镜像写成真实 KDS API 已同步。
- 不把设计、文档、控制台可见写成业务完成。
- 不允许旧项目命名、旧 AI 定位、旧中台口径回流。
- 有文档债务时，Loop 状态不得高于 `partial`。

## 常用命令

```bash
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
python3 tools/kds-sync/kds_conflict_guard.py
```

