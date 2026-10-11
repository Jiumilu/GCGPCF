---
doc_id: GPCF-DOC-D5E62C7C1E
title: Loop Round GPCF CWME Space Domain Extension Registration Request 001
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-001.md
source_path: docs/harness/loops/loop-round-GPCF-CWME-SPACE-DOMAIN-EXTENSION-REGISTRATION-REQUEST-001.md
sync_direction: bidirectional
last_reviewed: 2026-10-11
supersedes: []
superseded_by: []
---

# Loop Round GPCF CWME Space Domain Extension Registration Request 001

## 输入

- 老卢"4、启动"后先行项：CWME 首月件 B4-1/B4-2 初版件产出（F-017）。
- 域包登记申请一前置（`cwme-ext.ttl` 初版＋映射表 v1）已补齐；B4 件本地验证通过。

## 动作

- 建 `docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.json` / `.md`（request 包）。
- 附件引用 KDS `世界资产/世界模型引擎/ontology/`（ext/mapping/shapes；不复制正文）。
- 保证：不改 WAS 主术语、不改 registry 既有条目；`current_decision` 留 `pending_governance_review`。

## 输出

- `docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.md`
- `docs/harness/evidence/cwme-space-domain-extension-registration-request-20261011.json`

## 检查

- `python3 tools/kds-sync/validate_cwme_space_domain_extension_registration_request.py`
- `python3 tools/kds-sync/validate_was_project_group_ontology_registry.py`（回归）
- `python3 tools/kds-sync/document_control.py`

## 反馈

- 请求包已提交（submitted=true）；`registry_entry_added=false`、`governance_reviewed=false`、`waes_authorized=false`、`accepted=false`。
- 附件核实：cwme-ext.ttl（199 triples/33 类）＋ mapping-v1（40 表）＋ shapes（违规 5 项检出）——均由 F-017 首月件实跑验证。

## 下一轮

registry admission 裁定；受理后按域扩展包登记制登记。CWME 侧进入 B4-3 生成器（本体→TS/SQL/图库）。
