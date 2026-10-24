---
doc_id: GPCF-DOC-F034-BRAIN-TOKEN-DIFF-20261024
title: Brain 主题令牌差异明细（2026-10-24）
project: GPCF
related_projects: [WAE, Brain]
domain: governance
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/brain-token-diff-20261024.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/brain-token-diff-20261024.md
sync_direction: bidirectional
last_reviewed: 2026-10-24
supersedes: []
superseded_by: []
---

# Brain 主题令牌差异明细

对比：WAE `packages/ui-tokens/src/tokens.css` vs Brain `src/styles/theme.css`。
共同变量 76；差异 **25**；Brain 独有 **5**。

## 差异（值不同）

| 变量 | WAE | Brain |
|---|---|---|
| `--font-size` | 16px | 13px |
| `--background` | oklch(0.145 0 0) | #111114 |
| `--foreground` | oklch(0.985 0 0) | #e2e2e8 |
| `--card` | oklch(0.145 0 0) | #18181c |
| `--popover` | oklch(0.145 0 0) | #1e1e24 |
| `--primary` | oklch(0.985 0 0) | #7c6af7 |
| `--secondary` | oklch(0.269 0 0) | #222228 |
| `--muted` | oklch(0.269 0 0) | #1c1c22 |
| `--accent` | oklch(0.269 0 0) | #2a2a34 |
| `--destructive` | oklch(0.396 0.141 25.723) | #e05252 |
| `--border` | oklch(0.269 0 0) | rgba(255,255,255,0.07) |
| `--input` | oklch(0.269 0 0) | #1e1e24 |
| `--input-background` | #f3f3f5 | #1e1e24 |
| `--switch-background` | #cbced4 | #3a3a48 |
| `--ring` | oklch(0.439 0 0) | #7c6af7 |
| `--sidebar-primary` | oklch(0.488 0.243 264.376) | #7c6af7 |
| `--sidebar-ring` | oklch(0.439 0 0) | #7c6af7 |

（其余 8 处为对应 foreground/accent 派生值，见脚本输出。）

## Brain 独有变量

`--surface-chat`、`--surface-panel`、`--surface-panel-alt`、`--surface-sidebar`、`--violet-glow`。

## 结论

- Brain 为独立 hex 主题，不是别名层；差异需 Brain 属主裁定「迁入权威 / 登记受控例外」。
- 本轮不改 Brain。

## 非声明

- 不声明差异已消除；不声明 F-034 可关闭。
