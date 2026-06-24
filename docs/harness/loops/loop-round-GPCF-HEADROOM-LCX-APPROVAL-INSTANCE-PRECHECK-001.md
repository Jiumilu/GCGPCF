---
doc_id: GPCF-DOC-F43423639D
title: Loop Round GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md
source_path: docs/harness/loops/loop-round-GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-HEADROOM-LCX-APPROVAL-INSTANCE-PRECHECK-001

## 输入

- 上轮输出：授权字段 schema 与人工审批包模板已生成。
- 本轮目标：建立审批包实例 precheck 与负向实例样例。
- 本轮边界：不补写授权事实、不伪造审批、不采集生产 token、不启动生产代理、不写 KDS、不触达外部 API、不升级 accepted、integrated 或 production_ready。

## 动作

1. 读取授权 schema 与审批包模板。
2. 生成待填写审批包实例。
3. 生成 7 个负向实例样例。
4. 建立 validator，验证待填写实例 blocked、负向实例全部 rejected。

## 输出

- `fixtures/headroom/headroom-lcx-human-approval-package-instance.pending.json`
- `fixtures/headroom/headroom-lcx-human-approval-package-instance-negative-fixtures.json`
- `tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py`
- `tools/kds-sync/validate_headroom_lcx_approval_instance_precheck.py`
- `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.json`
- `docs/harness/evidence/headroom-lcx-approval-instance-precheck-20260622.md`

## 检查

```bash
python3 tools/kds-sync/build_headroom_lcx_approval_instance_precheck.py
python3 tools/kds-sync/validate_headroom_lcx_approval_instance_precheck.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py --check-only
```

## 反馈

待填写实例当前 blocked，负向实例用于防止误授权进入生产测量。

## 下一轮

若用户填写审批包实例，可运行 approval instance validation；否则继续建立审批包实例填写说明和回滚清单。
