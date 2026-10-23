---
doc_id: GPCF-DOC-5AFF05DB21
title: O2 令牌收口 —— 证据（F-034，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/o2-token-consolidation.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/o2-token-consolidation.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# O2 令牌收口 —— 证据（F-034，2026-10-22）

> 本轮只读检查：未修改 WAE / PKC / Brain / PVA / WAME 任何仓。命令在 `GlobalCloud V0.0.1`（工作区根）或 `GlobalCloud WAE` 仓根执行，已注明。

## 结论

**pass（脚本可用 + 生成链漂移检查通过 + 逐字节比对完成）**，但有一处**清单口径限制需登记**：`tools/verify-token-sources.py` 的"应逐字节相同"清单仍按旧项目名（WAES/PVAOS）硬编码，其中 3/4 路径在当前工作区已不存在 → 脚本 exit 0 **不能单独证明"4 份一致"**；本轮用 sha256 静态比对补核，结论以补核为准（见 §3）。

## 1. 单一来源与 76 令牌

| 项 | 值 |
|---|---|
| 单一来源 | `GlobalCloud WAE/packages/ui-tokens/src/tokens.css` |
| 唯一令牌名（脚本口径） | **76** 个（`--*` 名字去重；声明出现 107 次，分布于 `:root` 38 / `.dark` 34 / `@theme inline` 38，属主题域重复声明，非多源） |
| 文件 sha256 | `54729cdf634fadd501e3c92429ebfabb3f80553157f35051338cbda1337c1bda` |
| 文件字节数 | 4319 |

```bash
# 脚本口径（与 tools/verify-token-sources.py 相同）
python3 - <<'PY'
import re, pathlib
text = pathlib.Path("GlobalCloud WAE/packages/ui-tokens/src/tokens.css").read_text(encoding="utf-8")
names = {m.group(1) for m in re.finditer(r"(--[\w-]+)\s*:\s*([^;]+);", text)}
print(len(names))   # → 76
PY
```

## 2. 生成链（设计令牌 → WAE 消费方）漂移检查

设计令牌单源：`_governance/drafts/ui-spec/tokens/`（`@globalcloud/design-tokens@1.0.0`，`tokens.css` + `runtime.css`）→ `sync_tokens.py` → `packages/ui-tokens/src/gc.tokens.css` / `gc.runtime.css`（生成物头带版本与 sha）。

```bash
python3 "_governance/drafts/ui-spec/tools/sync_tokens.py" --check
# 令牌已同步（@globalcloud/design-tokens@1.0.0，2 个文件）
# exit 0
```

## 3. 跨项目复制件逐字节比对

### 3.1 脚本输出（`tools/verify-token-sources.py`）

```bash
cd "GlobalCloud WAE"
python3 tools/verify-token-sources.py ; echo "exit=$?"
```

```text
单一来源 GlobalCloud WAE/packages/ui-tokens/src/tokens.css（76 令牌, sha 54729cdf634fadd5）

逐字节相同（零视觉回归的可证明依据）：1 份
  ✓ GlobalCloud Brain/default_shadcn_theme.css

路径不存在：['GlobalCloud WAES/src/styles/default_theme.css', 'GlobalCloud PVAOS/src/styles/default_theme.css', 'GlobalCloud PVAOS/default_shadcn_theme.css']

已知偏离（记录在案，未改动对方项目）：
  • GlobalCloud PKC/src/styles/theme.css: 值不同 4 处
  • GlobalCloud Brain/src/styles/theme.css: 值不同 30 处、独有令牌 5

本仓应用对单一来源的消费关系（T2 判据）：
  ✓ apps/wame/src/styles/default_theme.css：薄壳 → 取值来自 @globalcloud/ui-tokens（零重复声明）
  ✓ apps/wame/src/styles/globals.css：薄壳 → 取值来自 @globalcloud/ui-tokens（零重复声明）
exit=0
```

### 3.2 静态补充比对（脚本清单路径已失效，补核实际存在的复制件）

```bash
CANON="GlobalCloud WAE/packages/ui-tokens/src/tokens.css"
shasum -a 256 "$CANON"   # 54729cdf634fadd501e3c92429ebfabb3f80553157f35051338cbda1337c1bda
for f in <候选复制件>; do shasum -a 256 "$f"; done
```

| 文件（当前实际路径） | sha256(16) | 字节 | 与单源逐字节相同 | 说明 |
|---|---|---|---|---|
| `GlobalCloud Brain/default_shadcn_theme.css` | `54729cdf634fadd5` | 4319 | **是** | 脚本清单内、路径有效 |
| `GlobalCloud PVA/default_shadcn_theme.css` | `54729cdf634fadd5` | 4319 | **是** | PVAOS 改名为 PVA 后的实际路径（脚本清单未更新） |
| `GlobalCloud WAME/src/styles/default_theme.css` | `54729cdf634fadd5` | 4319 | **是** | WAME 复制件（脚本清单未列，补核发现） |
| `GlobalCloud PVA/src/styles/default_theme.css` | `9e1ac852417255da` | 4318 | 否 | **值偏离 1 处**：`--muted-foreground` 为 `oklch(0.78 0 0)`，单源为 `oklch(0.708 0 0)`（diff 56 行） |
| `GlobalCloud WAES/src/styles/default_theme.css` | — | — | 路径不存在 | WAES 仓已无 `src/styles/`（布局变化），脚本清单失效 |
| `GlobalCloud WAE/packages/ui-tokens/src/default_theme.css` | `7a9372ed213c09ab` | 208 | 否 | 仓内薄壳/历史件，非复制件，不参与逐字节比对 |

**补核结论**：当前可解析的"同源复制件"中，**3 份逐字节一致**（Brain shadcn、PVA shadcn、WAME default_theme）；PVA `src/styles/default_theme.css` 有 1 处值偏离（需 PVA 属主裁定，**本轮不改**）。

### 3.3 已知偏离登记（只登记，不改对方仓）

| 项目 | 文件 | 偏离 | 处置 |
|---|---|---|---|
| PKC | `GlobalCloud PKC/src/styles/theme.css` | 值不同 **4 处**（`--card`、`--input-background`、`--popover`、`--switch-background`） | 本轮不改，登记待裁定 |
| Brain | `GlobalCloud Brain/src/styles/theme.css` | 值不同 **30 处** + 独有令牌 **5 个**（`--surface-*` ×4、`--violet-glow`；独立深色主题） | 本轮不改，登记待裁定 |

## 4. 限制（必须随结论一起读）

1. `verify-token-sources.py` 的 `EXPECTED_IDENTICAL` / `KNOWN_DIVERGENT` 路径按旧项目名写死（WAES/PVAOS）；项目改名/布局变化后 3 个路径失效，脚本的"4 份一致"判据当前**不可直接成立**，本轮以 §3.2 静态 sha256 补核替代。
2. 逐字节相同只能证明"复制件与单源完全一致"，**不证明视觉零回归**（视觉验证需浏览器截图，不在本轮）。
3. PKC/Brain/PVA 的偏离按任务要求**只登记不改写**；其中 PVA 的 1 处偏离是本轮新发现，未写入任何对方仓。
4. 未修改任何令牌文件；未 commit/push。
