---
doc_id: GPCF-DOC-00463F9971
title: Headroom LCX 许可证与 OSS 合规
project: GPCF
related_projects: [GPCF]
domain: general
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/loop/context/headroom/docs/license.md
source_path: loop/context/headroom/docs/license.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Headroom LCX 许可证与 OSS 合规

Headroom 上游仓库标注 Apache-2.0。项目群内部使用必须保留：

- 上游仓库地址。
- 许可证名称。
- 版本锁定记录。
- 修改说明。
- 安全审查结论。

## 内部登记口径

```yaml
name: headroom
repo: chopratejas/headroom
license: Apache-2.0
usage:
  - proxy
  - sdk
  - mcp
  - agent_wrap
  - ccr
distribution:
  internal: true
  external: pending_review
production_admission_gate: false
```

## 边界

本文件不构成法律意见。对外分发、修改版分发、商业嵌入或品牌使用必须另行通过 OSS/Legal review。
