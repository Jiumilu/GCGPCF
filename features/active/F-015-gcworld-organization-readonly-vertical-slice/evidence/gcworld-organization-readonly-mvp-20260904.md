---
doc_id: GPCF-F-015-EVIDENCE-GCWORLD-ORGANIZATION-READONLY-MVP-20260904
title: F-015 GCWORLD组织资产与项目运行只读纵切交付回执
project: GPCF
status: partial
date: 2026-09-04
---

# F-015 GCWORLD组织资产与项目运行只读纵切交付回执

## 结论

GCWORLD业务开发主线已将第一个只读闭环扩展为：组织资产总览、资产详情、证据关系图谱与项目运行事项核对。状态保持`active/partial/not_complete`，未执行提交、推送、部署或状态提升。

## 业务进度

- 用户可从Studio全局导航进入“组织世界”。
- 用户可在938项候选资产中按名称、类别和优先级查找。
- 用户可查看单一资产画像、状态、责任路由、证据数量和摘要。
- 用户可追溯候选、来源和关系证据，所有关系边仍显式标记为待核验。
- 用户可切换“项目运行”，在28项KDS项目登记中按名称、负责人、下一行动和状态查找。
- 用户可核对项目负责人、登记截止、下一行动与最近会议；缺失值不推断、不补写。

## 工程与数据进度

| 项目 | 结果 |
|---|---|
| 快照 | 938项候选组织资产、28项项目登记；正式0、模拟0 |
| 来源版本 | KDS提交`341264982d47c2b7cabe92c5a107ad0d8cad653c`，树`946fdf51cd7f25b7c566e79843d0351236ff2231` |
| 项目注册表 | `工业绿链/project-registry.yaml`，SHA-256=`c567d6e8ff9583916b9ed3a0e22021988c150d652bac58ceef5df0a6e0aed20a` |
| 前端组合快照 | SHA-256=`d8470e11f4dd5e7773ceb9fad92fd36a7a18dc6afcd5d7aad70ab6779f0b16fa` |
| 项目登记分布 | 运行中6、候选18、未确认2、构想1、已归档1；18项有下一行动 |
| 相关组件测试 | 31/31通过 |
| 生产构建 | 通过 |
| 浏览器业务流 | 1/1通过，意外请求0 |
| CodeGraph机器证据 | 完成并通过自验证，SHA-256=`400c4d818d58e4793f627e98e642409c6a2a336c36bc8c469afb32aa5af07530` |
| 浏览器截图 | SHA-256=`c1511e8720bfac4764392d10a2ddba260a1d5c0ede1d5559dd7fe013c97a441d` |

## 治理伴随线

- 不自动合并身份，不生成正式世界资产。
- 不写KDS，不提升事实，不授予Agent真实业务权限。
- KDS浮动工作树不进入快照；项目注册表仅从固定HEAD读取，`active`等值只表述为登记状态。
- 不以名称自动建立资产—项目关系，不执行项目行动。
- 221项高优先级身份复核保持伴随任务，不再阻塞普通界面开发、候选数据展示和内部测试。

## 未闭环项

1. Studio全仓回归共324个测试文件，322个通过、1个跳过，未修改的`SessionObjectPanel`测试中17项失败；单独复跑一致。
2. Studio本地LOOP门禁仍将LR-918视为最新索引轮次，其无源码变更豁免与本轮不匹配，导致Harness传递失败。
3. 上述两项不阻塞本轮只读业务功能的本地演示，但阻塞将F-015标记为完成或可发布。
4. 项目登记存在历史截止日期，需后续由业务责任人通过独立治理节点确认新鲜度；本轮不因此冻结界面开发。

## 对应证据

- Studio中文总回执：`docs/harness/evidence/gcworld-organization-readonly-mvp-20260904.md`
- Studio CodeGraph机器证据：`docs/harness/evidence/codegraph/gcworld-organization-readonly-mvp-20260904.json`
- Studio浏览器截图：`test-results/gcworld-organization-world.png`
