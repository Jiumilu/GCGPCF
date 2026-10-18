---
doc_id: GPCF-DOC-C039431381
title: KDS Sync Tools
project: GPCF
related_projects: [GPC, KDS, GPCF]
domain: tools
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/tools/kds-sync/README.md
source_path: tools/kds-sync/README.md
sync_direction: bidirectional
last_reviewed: 2026-10-18
supersedes: []
superseded_by: []
---

# KDS Sync Tools

用途：维护 GlobalCloud GPCF 文档控制体系、目录 README、KDS `开发` 空间本地镜像和同步台账。

运行：先只读检查，再按源文件限定写入。全量重建须显式使用 `--apply-full` 并先审查影响范围。

```bash
python3 tools/kds-sync/document_control.py --check
DOCUMENT_CONTROL_SCOPE='path/to/document.md' python3 tools/kds-sync/document_control.py
```

输出：

- `09-status/globalcloud-document-control-register.md`
- `09-status/kds-development-space-sync-register.md`
- `09-status/document-deprecation-register.md`
- `.kds/development-space/开发/`
- `.kds/local-mirror-ledger.jsonl`
- `.kds/sync-ledger.jsonl`
