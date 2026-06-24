---
doc_id: GPCF-DOC-187BF785F5
title: Headroom LCX 安全规则
project: KDS
related_projects: [KDS]
domain: general
status: controlled
version: v1.0
owner: KDS
kds_space: 开发
kds_path: 开发/05-KDS/loop/context/headroom/docs/security.md
source_path: loop/context/headroom/docs/security.md
sync_direction: bidirectional
last_reviewed: 2026-06-21
supersedes: []
superseded_by: []
---

# Headroom LCX 安全规则

## 默认设置

```text
HEADROOM_TELEMETRY=off
HEADROOM_PRODUCTION_PROXY=false
HEADROOM_MEMORY_CROSS_PROJECT=false
HEADROOM_LEARN_MODE=preview
HEADROOM_OUTPUT_SHAPER=false
```

## 敏感内容

以下内容默认 block 或 passthrough，不进入压缩链：

- TOKEN、Cookie、Authorization header、API key。
- 客户合同原文、POD 原文、财务凭证、生产凭证。
- KDS 私有空间原文和未脱敏受控原文。
- 设备凭据、部署凭据、release-write workflow secret。

## CCR retrieve

CCR retrieve 必须满足：

```text
reason_required
evidence_record_required
sensitive_check_required
waes_decision_required
```

## Memory

Headroom memory 只能保存工程工作记忆候选，例如路径修正、命令失败原因、依赖安装注意事项和工具限制。它不得保存业务裁决、合同结论、财务结论、合规结论或 KDS 正式事实。
