---
doc_id: GPCF-DOC-AAE22480F8
title: KDS Security Policy
project: GPCF
related_projects: [GPCF, KDS]
domain: operational-skill
status: operational_controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/.codex/skills/globalcloud-document-governance/references/kds-security-policy.md
source_path: .codex/skills/globalcloud-document-governance/references/kds-security-policy.md
sync_direction: register_and_mirror
last_reviewed: 2026-06-12
supersedes: []
superseded_by: []
---

# KDS Security Policy

## 开发空间

KDS 空间名称固定为：`开发`。

当前安全口径：开发空间仅允许用户本人专用 TOKEN 访问、阅读和编辑。

## TOKEN 变量

```text
KDS_DEVELOPMENT_SPACE_TOKEN
KDS_TOKEN_OWNER=lujunxiang
KDS_SPACE_NAME=开发
KDS_TOKEN_SCOPE=read,write,edit
```

## 禁止事项

- 禁止把 TOKEN 写入 Git。
- 禁止把 TOKEN 写入 `.kds/`。
- 禁止把 TOKEN 写入同步流水。
- 禁止在日志中打印 TOKEN 明文。
- 禁止非专用 TOKEN 访问 KDS 开发空间。

## 校验规则

`validate_kds_token.py` 只检查环境变量是否存在、owner/scope/space 是否正确，并输出 token 指纹前 8 位哈希。没有 TOKEN 时进入 `blocked`，但不得伪造 TOKEN。

## 预留破窗

如未来需要临时授权，可设置 `KDS_BREAK_GLASS_TOKEN_FINGERPRINT`，默认必须为空。
