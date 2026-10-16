---
doc_id: GPCF-DOC-EAF988D469
title: GCMEM 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/STATUS.md
source_path: projects/gcmem/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-16
supersedes: []
superseded_by: []
---

# GCMEM 状态

本文件只记录 GCMEM 的当前项目节奏状态。功能级进度与证据由主设计文档与 KDS 页承载。

## 当前节奏（2026-10-16 立项）

- **状态**：active（世界资产空间，`WAS-GCMEM`）。
- **已完成**：
  - 记忆账本上线：`KDS/_meta/hermes-memory-log.md`（append-only；首条检索命中 0.91）；
  - mem0 退役：插件卸载＋备份留存（`~/.hermes/backups/mem0-plugin-*.tar.gz`）；
  - 服务接口：`~/.hermes/scripts/gcmem.py`（add / search / sync / stats / candidates / import-candidates）；
  - 自动迭代接入：夜间对话挖掘（每晚 23:00）提炼候选并自动入账；
  - 周报指标切换：体系进化周报由「Mem0 记忆数」改为「KDS 记忆条目数」。
- **已完成（2026-10-16 第二批）**：
  - 小G 记忆栈迁移·本机侧：后端 `primary=gcmem`（mem0_local / cognee 退役）＋控制台文案更新＋add / search 全链实测通过；
  - gbrain 升级 0.60.139 → 0.60.257：驻留进程全量重启、writer 门闸通过、回归完成；缺嵌块已清至仅剩 3 个 held 大页（当地批补清零）；当晚再升 0.60.260（serve/autopilot/supervisor 全量换版、门闸复过）。
- **已完成（2026-10-16 第三批·对标 mem0）**：GCMEM v1.2——归一化判重＋相似提示＋`--supersedes` 替代标注＋`search --scope memory` 聚焦检索；夜挖新增全量候选留存与 LLM 复核入账层（≤3 条/日，宁缺毋滥）。
- **已完成（2026-10-16 第五批·held 大页补嵌）**：三页 2482 块全部补嵌完成（engineering-gates 370 ＋ wiki/log×2 各 1056）；同步定位 gbrain 0.60.257 本地 provider「批准回旋镖」缺陷（consent=null → 页级批准无授权载体）并沉淀绕行法（gbrain 技能 P1 节）；终验 doctor：partial_embedding OK / embed_staleness OK / 缺嵌 0 / brain_score 88。
- **已完成（2026-10-16 第四批·会话注入层）**：GCMEM v1.3——Hermes 记忆 provider 插件上线（`memory.provider=gcmem`）：每轮自动预取注入＋纠正/偏好即时捕获＋`gcmem_search` 工具＋熔断保护；实测预取 2.3s / 工具 1.0s / 加载器装载 / 实弹探针通过。
- **已完成（2026-10-16 第六批·mem0 清尾）**：旧模块链归档（`xiaoji_mem0_memory.py`＋`xiaoji_mem0_daily.sh` → `~/.hermes/backups/mem0-retire-20261016/`）；patrol / lint / feedback 三处引用摘除或更名（分类标签 `gcmem_wrong`）；残留仅注释与已停用留档（backend `mem0_local` 块 disabled）。
- **已完成（2026-10-16 第七批·工程加固 v1.4）**：`gcmem.py doctor` 巡检上线（生产账本全过）；回归测试 20/20（pytest，3.55s）+ provider 冒烟离线全绿；`GCMEM_LEDGER_PATH` 测试注入点；体系进化周报接入 doctor 摘报。
- **进行中**：小G 记忆栈容器侧随下次部署切换。⚠️ 状态注记（2026-10-16）：小G 全栈已暂停（老卢指示）——relay + server 已 bootout+disable（恢复见 `~/.globalcloud-xiaog-runtime/ops/PAUSE-20261016.md`）；恢复后继续容器侧切换。

## 关联

- 设计主文档：`projects/gcmem/MASTER-DESIGN.md`
- 记忆主存：`KDS/_meta/hermes-memory-log.md`｜项目页：`KDS/世界资产/GCMEM.md`
- 上游：GKE-001 知识工程（长期记忆条目为 working 级，随人工确认流转）
