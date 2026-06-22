---
doc_id: GPCF-DOC-247164F00E
title: Loop Round GPCF-KDS-DKS-013
project: GPCF
related_projects: [GFIS, GPC, PVAOS, WAES, KDS, XiaoC, XGD, GPCF, Studio]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/harness/loops/loop-round-GPCF-KDS-DKS-013.md
source_path: docs/harness/loops/loop-round-GPCF-KDS-DKS-013.md
sync_direction: bidirectional
last_reviewed: 2026-06-22
supersedes: []
superseded_by: []
---

# Loop Round GPCF-KDS-DKS-013

日期：2026-06-17
状态：v0.1 受控 Loop 记录
主题：合作单位接入与组织空间初始化清单

## 1. 输入

1. `GPCF-KDS-DKS-012` 已建立权限与密级矩阵。
2. 用户明确下一家重点是葛化与湖北磷材，未来会有更多工厂建设和区域绿色供应链运营单位接入。
3. 用户要求 AI 服务统一提供，同时允许合作单位未来自购额度、贡献额度和共享额度。
4. 用户要求积分池和收益池纳入 KDS 11 池底座，知识、产值、渠道等贡献都可进入受控评价。

## 2. 动作

1. 新增 `GlobalCloud绿色供应链合作单位接入与组织空间初始化清单.md`。
2. 将飞书、小即、KDS、WAES、GFIS、Hermes、委员会空间拆成组织空间初始化项。
3. 为合作单位建立组织档案、角色、资料包、AI 额度账户、积分账户、悬赏账户和权限矩阵编号建议。
4. 区分葛化首批七类资料包和湖北磷材首批五类资料包。
5. 明确本轮只生成受控初始化清单，不做真实账号、生产权限或资料开放。

## 3. 输出

| 输出 | 路径 | 说明 |
|---|---|---|
| 合作单位接入初始化清单 | `03-data-ai-knowledge/GlobalCloud绿色供应链合作单位接入与组织空间初始化清单.md` | 定义组织空间、角色、密级、资料包、AI 额度、积分、收益、悬赏和接入验收 |
| Loop 记录 | `docs/harness/loops/loop-round-GPCF-KDS-DKS-013.md` | 记录本轮输入、动作、输出、检查和反馈 |

## 4. 检查

已执行以下治理检查：

```bash
python3 tools/kds-sync/document_control.py
python3 tools/kds-sync/check_document_pollution.py
python3 tools/kds-sync/validate_kds_token.py
python3 tools/kds-sync/loop_document_gate.py
```

检查结果：

| 检查项 | 结果 | 说明 |
|---|---|---|
| 文档控制 | pass | 新增文档进入 README、文档控制台账、KDS 开发空间同步台账和 `.kds` 本地镜像 |
| DKS-013 局部 `git diff --check` | pass | DKS-013 相关源文件、台账和镜像无空白格式错误 |
| 污染检查 | pass | `document_pollution=pass` |
| KDS TOKEN 检查 | pass | `kds_token=pass fingerprint=bfd9553d` |
| Loop 文档门禁 | pass | `gate=pass`，`missing_metadata=0`，`missing_readme_dirs=0` |

本轮只声明 DKS-013 范围内门禁通过；不改变 GFIS / GPCF 既有修复状态，不升级项目整体状态。

## 5. 反馈

本轮把合作单位复制接入从战略设想转成受控初始化清单，使葛化试点、湖北磷材并行线和后续工厂 / 区域运营单位接入具备同一套组织、资料、额度、积分、悬赏和治理入口。

本轮不创建真实组织空间、不开放真实资料、不配置生产权限、不确认真实积分、收益或 AI 额度。

## 6. 下一轮建议

```text
GPCF-KDS-DKS-014：
葛化首批资料包入库验收与 GFIS AI 助手试运行任务书。
```

建议直接围绕葛化建设、运营、订单、辽宁远航、现代精工 OEM、质量 / 发货 / POD、金融凭证门禁七类资料包展开。
