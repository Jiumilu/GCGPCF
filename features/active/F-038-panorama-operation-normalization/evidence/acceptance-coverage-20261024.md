---
doc_id: GPCF-DOC-F038-ACCEPTANCE-COVERAGE-20261024
title: F-038 人工验收项的自动化覆盖（2026-10-24）
project: GPCF
related_projects: [SpaceAI Platform]
domain: governance
status: draft
version: v1.0
owner: GPCF
last_reviewed: 2026-10-24
---

# 人工验收项的自动化覆盖

## 已自动覆盖（18 tests passed）

`plugins/map-3d/tests/panorama-bubble-layer.test.ts`：
- 提交前必须确认；成功 POST /Disposal/Add + 审计 + 清输入；
- **失败保留确认层与备注可重试**；
- 取消直接关层。

`plugins/map-3d/tests/panorama-cwme-actions.test.ts`：
- 回投确认层 + 预览含“只追加/模拟数据”声明；
- 回投成功：POST 审计 + 计数 +1 + 回执；
- **回投失败：错误提示、不写审计、计数不变、确认层保持**；
- **30s 幂等：同内容短时间重投不发第二次请求**。

## 仍需人工/属主确认

1. 真实浏览器视觉与交互手感（非逻辑断言）；
2. 生产/演示环境下的实际派单与 CWME 回投路径；
3. SpaceAI 属主签字。

## 非声明

- 不声明人工验收已完成；不声明 F-038 可关闭。
