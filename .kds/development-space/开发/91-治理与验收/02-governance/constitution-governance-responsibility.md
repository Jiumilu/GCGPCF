---
doc_id: GPCF-DOC-CONSTITUTION-GOVERNANCE-RESPONSIBILITY-20260712
title: GlobalCloud 宪法治理责任与 G00 门禁
project: WAME
related_projects: [GPC, WAME, KDS, GPCF, ICP]
domain: governance
status: controlled
version: v1.1
owner: WAME
kds_space: 开发
kds_path: 开发/91-治理与验收/02-governance/constitution-governance-responsibility.md
source_path: 02-governance/constitution-governance-responsibility.md
sync_direction: bidirectional
last_reviewed: 2026-10-22
supersedes: []
superseded_by: []
---

# GlobalCloud 宪法治理责任与 G00 门禁

## 权责结构

| 责任 | 项目 | 边界 |
|---|---|---|
| 产业领域解释与修订候选 | ICP | 不批准、不写 KDS canonical |
| 修订程序与审计 | SOP | 不改写产业模型、不替代人工确认 |
| 项目群传导与 G00 继承门禁 | GPCF | 不反向改写宪法、不替代业务 owner |
| 授权与状态裁决 | WAME + 人工 | 不制造证据、不绕过人工确认 |
| 正本与版本保管 | KDS | 不解释产业模型、不发布未批准候选 |
| 决策模型（StartLux-Decision v1.1）运行与许可 | WAME（运行/发布/许可）+ GPCF（治理口径/台账） | 不得作为授权或放行依据；权重 CC BY-NC 不得商用；不替代人工裁决 |

## 决策模型（StartLux-Decision v1.1）权责裁定（2026-10-22）

裁定：决策模型是**项目群级公共能力**，不新增项目、不摊入 28 个项目完成度；按两层归属执行——**WAME 承担运行/发布/许可**，**GPCF 承担治理口径与决策台账**。

判定依据（StartLux-Decision 自身判定 + 老卢确认，均 append-only 留痕于 `~/logs/startlux/decisions.jsonl`）：

| 判定点 | 结果 | 台账 id |
|---|---|---|
| 空间归类 `classify(space)` | 世界资产 0.832（none 0.040） | `20261022-053647-96d29b` |
| 归属项目 `decide` | WAME 0.902（GPCF 0.014、group_level 0.074；none 0.0006） | `20261022-053710-21b671` |
| 运行/许可口径（选项重排） `decide` | WAME 0.929（无锚定漂移） | `20261022-053743-87a269` |
| 归属方式 `decide` | 项目群级公共能力 0.903（归入现有项目 0.043） | 同上 |
| 红线闸口 `gate(redline)` | probability_yes 0.8445 → 须老卢确认 | `20261022-053725-00a828` |
| 四种结构 `decide` | 两层归属 0.989（其余 ≤0.007） | `20261022-053819-169ff2` |

确认：老卢 2026-10-22 答复「A」——两层归属。

边界与接入约定：

- 模型结果只作初筛/闸口建议，**不得作为授权、放行或状态提升依据**；人工裁决不可替代。
- 权重许可 CC BY-NC 4.0：仅限内部使用，不得进入对外商业交付；商业化须先取得 StartLux 书面授权。
- 消费方（DSH、Hermes、PMC、WAE、GCMEM 等）按 MCP/Skill 接入，不复制模型正文、不约定专属数据库归属。
- PG-09 资产注册表将该能力作为首条登记项；PG-10 决策台账按 append-only 追加、人工复核以 `review` 行追加，不改旧行。
- WAME 侧 PRD/职责正文的正式吸收，按 WAME 仓一对话一分支规则在其治理会话内完成，本仓不代写。

非声明：本文不改 28 项目范围、不改变任何项目状态、不声明 `accepted` / `integrated` / `production_ready` / `customer_accepted`。

## G00 宪法继承门禁

G00 检查项目群总体方案与项目群实施方案是否声明继承 `GlobalCloud宪法`，并检查产业模型领域主责与 canonical 保管职责是否分离。G00 通过仅表示继承关系和责任结构可回读，不表示修订已获授权、已发布、已集成或生产就绪。

验证命令：

```bash
python3 tools/kds-sync/validate_constitution_inheritance_gate.py
```
