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
last_reviewed: 2026-10-18
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
- **已完成（2026-10-17 第八批·跨端服务化 v1.5·对标 mem0）**：
  - MCP server `gcmem_mcp.py`（零依赖 stdio，5 工具）＋ HTTP API `gcmem_api.py`（mem0 兼容 REST，127.0.0.1:19090，launchd `ai.globalcloud.gcmem-api` 常驻）；
  - LLM 能力下沉核心：`llm_extract` 对话提炼、`llm_judge` 语义判重/冲突合并（同义改写拒写、推翻自动标替代链，实测闭环）；
  - 检索质量升级：账本条目字级 bigram 本地排序为检索主体（原文+时间+类型直出），gbrain 降为补充，CLI/MCP/API 三端统一 `search_memory`；
  - **三端实测打通**：Hermes（provider 插件）✅／Codex（MCP，gcmem_search 实弹返回账本条目）✅／Reasonix（MCP 5 tools 握手 60ms＋gcmem_search 实弹）✅；
  - **Reasonix 0.46.1 修复**：bundled undici 污染响应体解压（br 不解压→LLM 空回复 0 成本），`~/.local/bin/reasonix` wrapper 注入 preload 强制 Accept-Encoding: identity 根治；config.json 换新 DeepSeek key（旧 key 401，余额 ¥472 验证）；
  - **Codex 修复**：models_cache.json 旧 schema（缺 base_instructions）备份移除重建；hooks.json 顶层 description 字段摘除；
  - 回归 22/22（新增本地排序命中用例）；运维技能 `gcmem-ops` 沉淀（坑速查 7 条）。
- **进行中**：小G 记忆栈容器侧随下次部署切换。⚠️ 状态注记（2026-10-16）：小G 全栈已暂停（老卢指示）——relay + server 已 bootout+disable（恢复见 `~/.globalcloud-xiaog-runtime/ops/PAUSE-20261016.md`）；恢复后继续容器侧切换。

## 关联

- 设计主文档：`projects/gcmem/MASTER-DESIGN.md`
- 记忆主存：`KDS/_meta/hermes-memory-log.md`｜项目页：`KDS/世界资产/GCMEM.md`
- 上游：GKE-001 知识工程（长期记忆条目为 working 级，随人工确认流转）

## 项目群纳管（2026-10-18）

- 本地 `GlobalCloud Mem` 仓 `main` 与私有远端 `Jiumilu/GCMem` 的 `main` 已核对一致；本仓项目总体方案、实施方案和 Harness 清单为当前项目级控制入口。
- 当前 `overall_status=partial`；管理台与本机 API 已运行，容器侧迁移、连续三日夜挖验收及跨项目集成尚待证据。`authorization`：本地 Git、私有远端与纳管获用户授权；`confirmation`：业务验收与生产发布待人工确认。
- 2026-10-18 本仓回归 82/82；GPCF 中央文档门禁保持 `rework_required`，不提升项目群状态。

## OpenSpec 入口

- 策略：`conditional`
- 中央入口：`openspec/changes/gcmem-<change>/`
- Feature：`python scripts/gpcf_new_feature.py --project gcmem`
- 默认 Loop：`Governance`
- Evidence/Harness：`required/required`
