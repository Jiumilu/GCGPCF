---
doc_id: GPCF-DOC-5BCF9FD65B
title: O4 状态语义层 —— 证据（F-034，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/features/done/F-034-wae-p0-shell-and-role-convergence/evidence/o4-status-semantics.md
source_path: features/done/F-034-wae-p0-shell-and-role-convergence/evidence/o4-status-semantics.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# O4 状态语义层 —— 证据（F-034，2026-10-22）

> 本轮只读检查：未修改 WAE 仓代码。

## 结论

**pass（代码级 S1/S2 判定 + StatusBadge 渲染 + 测试与语义令牌交叉校验均通过）**，并附一项**口径差异登记**：框架侧状态字典成立，但 WAME/PKC 的 `ui_gate` 检查仍是「C5 统一状态字典：未发现」，说明项目侧尚未消费该字典（属后续接入动作，不在本轮改）。

## 1. 7 值字典（唯一口径）

代码：`GlobalCloud WAE/packages/ui-kit/src/statusDictionary.ts`

```text
UNIFIED_STATUSES = running / blocked / partial / review / complete / candidate / human_required   （恰 7 值）
STATUS_LABELS    = 进行中 / 已阻断 / 部分完成 / 待复核 / 已完成 / 候选 / 需人工
PROJECT_STATUS_MAP = 项目自有词 → 7 值之一（中英文常见写法，如 active→running、draft→candidate、待复核→review）
GCPC_GATE_WORDS  = accepted / integrated / production_ready / 已验收 / 已纳管 / 生产就绪（**不属本字典**）
```

## 2. S1 / S2 —— 代码级判定（不靠自觉）

| 约束 | 代码实现 | 行为 |
|---|---|---|
| **S1** 未映射词不得进入统一外壳 | `resolveStatus()` → `{kind:'unmapped'}`；`canEnterUnifiedShell()` 只对 `unified`/`mapped` 返回 true | 未知词显式返回 `unmapped`，**不猜、不兜底**；组件据此显式标注「未映射」 |
| **S2** `complete` ≠ 验收；accepted/integrated/production_ready 不属本字典 | `resolveStatus()` 命中 `GCPC_GATE_WORDS` → `{kind:'gcpc_gate'}`；`PROJECT_STATUS_MAP` 中**不含**这些词 | 门禁词显式标注「属 GCPF 门禁」，**绝不折算成 complete** |

## 3. StatusBadge 组件

代码：`GlobalCloud WAE/packages/ui-kit/src/components/status-badge.tsx`（由 `packages/ui-kit/src/index.ts` 导出）

- 统一值/可映射项目词 → 正常徽章，配色取 `--status-*` 语义令牌；
- `unmapped` → 显式标为「未映射」；`gcpc_gate` → 显式标为「属 GCPF 门禁」；
- `source` prop 仅用于溯源标注（如 `SpaceAI/场景包`）。

语义令牌交叉核对：`packages/ui-tokens/src/semantic.css` 声明 `--status-{7值}` 主色 + `--status-{7值}-subtle` 背景共 **14** 个，且全部是基础令牌别名（不新造颜色）——由测试强制。

六区母模板侧：`packages/ui-templates/src/templateRegions.ts` 的 `REGION_KEYS = main/status/risk/evidence/ai/audit`，状态区规则 S1（状态区走统一字典，未映射不折算）由 `templateRegions.test.ts` 覆盖。

## 4. 可回放命令与输出

```bash
cd "GlobalCloud WAE"

# 状态字典 + 语义令牌 + S1/S2（12 例）
npx vitest run packages/ui-kit/src/statusDictionary.test.ts
# ✓ |node| packages/ui-kit/src/statusDictionary.test.ts (12 tests)
# Test Files  1 passed (1) / Tests  12 passed (12)

# 六区模板与 S1 状态区规则（5 例）
npx vitest run packages/ui-templates/src/templateRegions.test.ts
# ✓ |node| packages/ui-templates/src/templateRegions.test.ts (5 tests)
# Test Files  1 passed (1) / Tests  5 passed (5)
```

`statusDictionary.test.ts` 关键断言：

```text
✓ 字典就 7 值：值集合与顺序稳定
✓ 每个值都有中文标签
✓ 每个值都有语义令牌：主色 + subtle 背景（防"字典加了、样式没加"）
✓ 语义令牌一律是基础令牌别名（不新造颜色）
✓ S1 统一值本身 → unified；已知项目词 → mapped（保留原词溯源）
✓ S1 未知词 → unmapped，且判定为"不得进入"
✓ S1 映射表的值域只能是那 7 个（不许夹带私货）
✓ S2 英中六个门禁词都判为 gcpc_gate，而不是 complete
✓ S2 大小写混写同样命中（accepted / ACCEPTED / Production_Ready）
✓ S2 门禁词**不在**映射表里（避免被人顺手映射掉）
```

`templateRegions.test.ts` 关键断言：

```text
✓ G1 Surface Structure：六区必须显式声明（undefined=缺区；null=显式"无"）
✓ G4 Evidence And Governance：无来源不得作为事实
✓ G5 AI Fact Separation：AI 产出恒为建议、必有来源回指
✓ S1：状态区走统一字典，未映射不折算
```

## 5. 口径差异登记（只登记，本轮不改）

```bash
python3 "_governance/drafts/ui-spec/tools/ui_gate.py" "GlobalCloud WAE"   # → C5 统一状态字典：存在
python3 "_governance/drafts/ui-spec/tools/ui_gate.py" "GlobalCloud WAME"  # → C5 统一状态字典：未发现
python3 "_governance/drafts/ui-spec/tools/ui_gate.py" "GlobalCloud PKC"   # → C5 统一状态字典：未发现
```

即：**框架侧（WAE）具备 7 值字典与 StatusBadge；项目侧（WAME/PKC）尚未消费**，属后续接入动作（不在本轮改写对方仓）。

## 6. 限制

- 本轮证据为代码 + 单元测试 + 语义令牌交叉校验；**未做真实运行时状态数据抽查**，也未做浏览器视觉验证（配色值正确性以 `--status-*` 令牌声明与测试为准）。
- 未修改任何文件；未 commit/push。
