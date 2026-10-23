---
doc_id: GPCF-DOC-327AA406B7
title: Studio 例外催签包（三方签署，2026-10-22）
project: GPCF
related_projects: [AAAS, Brain, WAS, XiaoC, WAME, GPC, Studio, GPCF, XWAIL, GFIS, MMC, KDS, XiaoG, PVAOS, SOP, PKC, XGD, ICP]
domain: governance
status: 催签材料（WAE 本地成文；通知外部需老卢授权）
version: v0.1
owner: WAE 工程线
kds_space: 开发
kds_path: 开发/91-治理与验收/features/active/F-034-wae-p0-shell-and-role-convergence/evidence/studio-exception-nudge-20261022.md
source_path: features/active/F-034-wae-p0-shell-and-role-convergence/evidence/studio-exception-nudge-20261022.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
created: 2026-10-22
basis:
  - docs/plan/Studio例外演练_三件套_20261022.md（三件套 + 三方审批表）
  - GPCF `studio-retirement-alternative-plan-20261022.md`（deprecated 冻结决策）
  - 决策模型 `studio_exception_approve` 0.67（WAE 侧 hold）
---

# Studio 例外催签包

> 现状：M3 批次 0 的例外**材料已齐、三方审批表已就位**，但**三方均未签**；WAE 侧此前按模型**主动暂缓**（避免单方先签形成事实压力）。
> 本包把"每方到底要签什么、不签卡住什么、建议的签署顺序"一次讲清，便于推动。

## 一、签署状态

| 方 | 要确认的事项 | 状态 |
|---|---|---|
| **GPCF**（治理） | 例外三件套与不扩散承诺符合项目群口径；F-011 不重开；F-010 证据引用方式可接受 | ⏳ 未签 |
| **WAE**（框架） | 替代方案中 WAE 承接范围与受控方案 v1.2 一致；不据此提升 WAE 状态 | ⏳ **主动暂缓**（模型 hold 0.67，建议最后签） |
| **目标项目**（Studio 属主 / 老卢） | 确认 Studio `deprecated` 冻结、职责迁移、范围（28→27 与否）、F-015 归属 | ⏳ 未签 |

## 二、每方的最小动作（都只是一次确认，不需要写代码）

| 方 | 最小动作 | 预计成本 |
|---|---|---|
| GPCF | 在 `Studio例外演练_三件套_20261022.md` §六 回一句"治理口径通过"（或指出要改的条款） | 5 分钟 |
| Studio 属主（老卢） | 回三件事：① 确认 `deprecated` 冻结；② 范围 28→27 是/否；③ F-015 转 World 还是登记历史例外 | 5 分钟 |
| WAE | 在 GPCF 与 Studio 属主表态后签"承接范围与 v1.2 一致" | 5 分钟 |

## 三、不签会卡住什么

| 不签方 | 卡住 |
|---|---|
| GPCF 不签 | 例外不生效；M3 批次 0 无法结项；后续批次（PKC/Brain/PVAOS）的"例外先例"缺失 |
| Studio 属主不签 | Studio 的 `deprecated` 标注、范围调整、F-015 归属都悬空；WAE 无法声明"Studio 不作实际纳入" |
| WAE 暂缓（当前） | 不影响已完成的 WAE 侧工作；但如果 GPCF/Studio 已签，WAE 会立即补签 |

## 四、建议的签署顺序（降低反复）

```text
① GPCF 出治理口径（5 分钟）
   ↓
② Studio 属主确认冻结/范围/F-015（5 分钟）
   ↓
③ WAE 签承接范围（5 分钟，与 v1.2 对齐）
   ↓
④ 例外生效 → M3 批次 0 结项 → 批次 1（PKC）按已有推进包继续
```

## 五、签完之后发生什么（避免"签了也没用"）

1. **M3 批次 0 结项**：Studio 例外材料归档到 F-034 证据（GPCF 侧已有 `evidence/` 目录）；
2. **Studio 状态落地**：由 Studio 属主在 Studio 仓补 `deprecated` 标注（当前 README/总体方案尚无该标记）；
3. **F-015 归属**：按 Studio 属主裁定转 World 或登记历史例外（不自动关闭）；
4. **WAE 状态不变**：仍 `active`；例外生效只代表"Studio 不作实际纳入"，不提升任何项目状态。

## 六、WAE 已备好的材料（签署方无需另找）

| 材料 | 位置 |
|---|---|
| 三件套 + 三方审批表 | WAE `docs/plan/Studio例外演练_三件套_20261022.md` |
| 只读核对（Studio HEAD `6984c4a5`、回归仍在、无 deprecated 标记） | 同上 §二 |
| 作废替代方案（GPCF 侧） | `GlobalCloud GPCF/docs/harness/evidence/studio-retirement-alternative-plan-20261022.md` |
| 例外定义（pj24 计划） | GPCF `docs/harness/evidence/pj24-wae-p0-plan-20261022.md` §109/§124 |

## 七、非声明

1. 不声明 Studio 已接入/已作废执行完毕；
2. 不代替任何一方签字；签署以各自书面确认为准；
3. 通知/投递到 GPCF 或 Studio 仓需老卢授权（跨仓写入）。
