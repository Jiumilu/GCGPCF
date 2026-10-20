---
doc_id: GPCF-DOC-EAF988D469
title: GCMEM 状态
project: GPCF
related_projects: [GPCF]
domain: governance
status: controlled
version: v2.0
owner: GPCF
kds_space: 开发
kds_path: 开发/91-治理与验收/projects/gcmem/STATUS.md
source_path: projects/gcmem/STATUS.md
sync_direction: bidirectional
last_reviewed: 2026-10-20
supersedes: []
superseded_by: []
---

> 同步说明（2026-10-20，老卢授权 E4）：正文由 GCMEM 仓 `docs/docs/STATUS.md` 同步；事实源以 GCMEM 仓为最新，本副本随 E4 同步流程更新。

# GCMEM 状态

本文件只记录 GCMEM 的当前项目节奏状态。功能级进度与证据由主设计文档与 KDS 页承载。

## 当前节奏（2026-10-16 立项）

- **状态**：active（世界资产空间，`WAS-GCMEM`）。
- **当前有效基线（2026-10-20）**：回归 **113/113**（gcmem 52 / api 22 / admin 24 / dsh_capture 15）；账本 138 条（活跃 117）；doctor healthy；四端共账本 + DSH 自动捕获桥在线；管理台排序/候选/导出/仪表盘可用。下一迭代规划见 `docs/GCMEM-下一迭代规划.md`（active，2026-10-20 老卢指示建立长期目标执行）。
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
- **已完成（2026-10-17 第九批·全量评估与加固）**：
  - 全量评估：运行态满分（回归、doctor、API/MCP 实调、bench Top-1 97.8%、干净检出复验）；代码/文档/集成/数据四维审查闭环，0 P0、6 P1 全修复；
  - 加固修复：gbrain 故障/超时检索自动降级为本地结果（`degraded` 标记，不再 500）；`_append` 读-改-写加 flock+线程锁（并发写无丢失）；PUT/CLI text≤300 显式拒绝＋写入净化（换行/控制字符）；非法 type 显式拒绝（API 422 / MCP error，不再静默兜底 fact）；`cmd_sync` 走 `_gbrain_bin()` 回退（launchd PATH 安全）；`.gitignore` 增补 bench 报告；
  - 配置修复：Hermes `memory.provider` 漂移回写 `gcmem`（config.yaml 备份留存）；残留测试进程 96012（19091）清理；
  - 回归 33/33（新增 7 例：gbrain 降级×2 / 净化 / 超长拒绝 / 并发写 / MCP 校验×2）；API 拒绝路径实测 422/400/403；
  - 文档补齐：MASTER-DESIGN v1.1 增补（bigram 主体 / LLM 下沉 / 四端共账本 / ≤3条/日 / 加固项）；四端口径统一——DSH 端技能 2026-10-17 上线（HTTP API 通道 127.0.0.1:19090），当前回归基线 33/33。
- **已完成（2026-10-17 第十批·架构收敛与测试补全）**：
  - 核心管线收敛：`add_memory()` 统一写入管线（校验→判重→LLM→写入→sync，结构化返回），API/MCP/CLI 退化为薄壳，删除双份管线与 stdout 抓取耦合；`stats_dict` / `doctor_dict` / `sync_index` 静默核心下沉，壳层零 `_run_print`；
  - P2-5 mid 语义：`get_all` 过滤列表改用全量下标（与 `get_one` / `history` 对齐）；
  - P2-8 替代链身份：时间戳升秒级＋sup 匹配改「时间＋文本指纹」（`_sup_ref`），同秒孪生条目不再误指向（doctor 校验 / history 上下游 / 近重复跳过全部改用）；生产账本 12 个历史 sup 标注在新校验下全部匹配；
  - P2-9 测试补全：新增 `tests/test_gcmem_api.py`（18 用例，TestClient 全端点：写入/判重/替代链/422/400/403/检索降级/mid 对齐/infer 判重与故障降级）＋LLM 判重/提炼/降级用例＋同秒身份用例；回归基线 **58/58**；
  - P2-10 bench 全临时化：合成账本＋gbrain 桩，不读不写生产，报告加 `mode` 标注；
  - P3 顺手修：`parse_meta` 校验 `\w+`（与 `meta_to_str` 对称）、MCP `tool_get` 实现倒序（与工具描述一致）、gbrain 查询去前导横线（argv 注入面）、`deepseek_key` 支持 `export ` 前缀、API sort 参数 422 校验；
  - 生产部署：`src` ↔ `~/.hermes/scripts` 同步＋launchd 重启，API/MCP 实调通过；生产 doctor 在新身份校验下 healthy=true。
- **已完成（2026-10-17 第十一批·P3 收尾）**：
  - 检索去重键改全文归一化（前 60 字相同的不同条目不再互相吞并）；
  - `llm_judge` 全量送判（单条截断 200 字、上限 100 条），老条目同义重复/推翻可被发现；
  - `kds_memory.LEDGER` 支持 `GCMEM_LEDGER_PATH` 重定向＋`cmd_add` 标废弃（防旧脚本在测试环境误写生产账本）；
  - `cmd_add` 语义相近提示 gbrain 超时 45s→15s（CLI 交互更跟手）；
  - `gcmem_reasonix_fix.mjs` 轮询 100ms→1s 且直测成功后停止（进程常驻开销降低）；
  - smoke 脚本恒真断言修正（prefetch 二次消费必为 None）＋熔断阈值读插件常量（不再硬编码）；
  - 回归 **61/61**（新增：去重键全文本 / LLM 全量送判 / kds 环境隔离）；生产五文件同步＋重启实调通过；
  - 噪声盘点：10 条 auto-capture 引文截断噪声（mid 12–21，2026-10-16 捕获门控加固前旧数据）已列精确清单，处置方案待老卢授权。
- **已完成（2026-10-17 第十二批·活跃语义与账本噪声清理，老卢授权 A′）**：
  - 检索活跃语义：`search_memory_verbose` 默认跳过被替代条目（本地 bigram 主体与 gbrain 补充命中的账本行均过滤）；`include_superseded=True` 审计开关（API POST/GET search、MCP schema、核心三层齐备）；
  - 替代链指纹容差：sup 构造不再整体 strip（`text[:40]` 尾空格是合法指纹内容），`_sup_ref` / `_entry_ref` 两侧尾空白容差——修复历史 mid=50 的 strip 遗留失配，doctor「sup 指向缺失」note 归零；
  - 账本噪声清理：10 条 auto-capture 引文截断噪声（mid 12–21）逐一 sup 软失效（cleanup 条目 `src=noise-cleanup`，替代链可溯源）；执行前账本备份 `~/.hermes/backups/hermes-memory-log.bak-20261017-noise-cleanup.md`；gbrain 索引同步刷新（1 页导入、2 chunk 嵌入）；
  - 验证：活跃检索「扁平 key」「information_schema」「SenseWorkspace」均只命中干净版本，噪声原文不再直出；审计开关可复现全量；doctor healthy（唯一 note 为清理条目间 0.98 近重复提示，设计使然）；账本 52 条、替代标注 23 个；
  - 回归 **64/64**（新增：活跃语义过滤 / 审计开关复现 / 尾空格指纹容差）。
- **已完成（2026-10-17 第十三批·后台管理应用立项与 M1 工作台，老卢立项：全量 M1-M5 + Vue3+Vite）**：
  - 规划成稿：`docs/GCMEM-后台管理应用规划.md`（对标 Mem0 Dashboard：管理能力面逐项映射，物理删除/多租户明确不建；状态 active）；
  - 后端 `/admin/api/*` 薄壳（overview / 列表分页过滤 / 详情 / 添加 / 软失效 / 检索审计开关 / system / sync），复用 `gcmem` 核心零新逻辑；`/admin` 静态托管 Vue 构建产物（`admin/dist`，生产路径 `~/.hermes/admin/dist`）；
  - **判重分层修复**：`add_memory` 显式替代（sup）跳过判重、infer 模式只挡精确重复（包含关系交 LLM）——修复「替代写入新文本包含旧文本被 409 拒写」缺陷；
  - 前端 M1 工作台（Vue3.5+Vite6+TS+vue-router，hash 路由，GCSpaceAI 同栈）：语义检索面板、列表（活跃/审计双模式）、过滤条（type/source/meta/日期/文本，对标 Mem0 v2 filters AND）、详情抽屉、添加/替代弹窗、系统页最小版（健康/版本/同步索引）；typecheck+build 全绿；
  - 回归 **72/72**（新增 `tests/test_gcmem_admin.py` 8 用例）；生产部署：后端 cp + 前端 dist 部署 + launchd 重启，`/admin` 实调 200 与资源可加载；
  - 遗留待后续批：M2 替代链时间轴+导出、M3 仪表盘、M4 候选复核、M5 打磨。
- **已完成（2026-10-17 第十四批·管理台 M2 替代链与导出）**：
  - 后端：`GET /admin/api/export`（json/csv/md × active/all，Content-Disposition 附件下载，CSV 引号转义）；`/admin/api/memories/{mid}/history` 别名；列表/详情新增 `superseded_by` 字段（审计视图可循「被谁替代」）；
  - 前端：详情抽屉内置替代链时间轴（旧→新、当前高亮）；审计列表行显示「← mid=N」替代指向；工具栏 JSON/CSV/MD 三格式导出按钮（跟随审计开关）；
  - 回归 **77/77**（新增 export 三格式/参数校验/history 别名/superseded_by 5 用例）；生产部署（后端 cp + dist 部署 + 重启）后导出实调正常、/admin 200。
- **已完成（2026-10-17 第十五批·管理台 M3 仪表盘）**：
  - 后端 `/admin/api/overview` 增补 `by_day`（近 14 天按日新增）与 `by_source`（来源分布降序）；
  - 前端仪表盘（纯 CSS 图表，零新依赖）：统计卡片（总条目/活跃/已废止/本周新增/替代标注）、类型分布、来源分布 Top8、近 14 天趋势柱图、doctor 面板（issues/notes 直显）＋一键同步索引；
  - 回归 **77/77**（overview 用例增补趋势/来源断言）；typecheck+build 全绿；生产部署后 /admin 200、overview 实调含 14 天曲线与 15 项来源。
- **已完成（2026-10-17 第十六批·管理台 M4 候选复核工作台）**：
  - 后端：`GET /admin/api/candidates`（夜挖候选文件列表＋条目解析＋超 2 天 stale 标记）、`POST /admin/api/candidates/apply`（采纳走 `add_memory` 统一管线，判重自动跳过，成功后刷新索引一次）、`POST /admin/api/candidates/archive`（移入 `~/.hermes/queues/gcmem-candidates-archive/`，文件名防路径穿越校验）；
  - 前端：候选复核视图（文件选择、条目勾选＋类型徽标、采纳所选、归档文件确认弹窗）；
  - 回归 **79/79**（新增候选列表/采纳判重/归档与路径穿越拒绝 2 用例）；typecheck+build 全绿；生产部署后候选实调正常（真实文件 5 条）、/admin 200。
- **已完成（2026-10-17 第十七批·管理台 M5 收尾，M1–M5 全部交付）**：
  - 系统页补全：服务 PID、gbrain 版本（实时探测）、本机监听说明；`/docs` API 文档入口、同步索引按钮齐备；
  - 打磨项核销：暗色主题（默认）、检索回车快捷键、导出文件名含时间戳（JSON/CSV/MD × active/all）、确认弹窗防误操作（替代/归档）；
  - 鉴权评估结论归档（规划文档 §5）：维持默认无鉴权——仅监听 127.0.0.1、单用户本机；开放非本机访问时再评估 token（高危险变更需授权）；
  - **管理台 M1–M5 全部交付**：记忆工作台（活跃/审计双模式、五维过滤、语义检索、添加/软失效、替代链时间轴）、三格式导出、仪表盘（统计/分布/趋势/doctor/同步）、候选复核工作台（采纳/归档）、系统页；回归 **79/79**；入口 http://127.0.0.1:19090/admin。
- **已完成（2026-10-17 第十八批·gbrain 检索结果缓存，立项实施）**：
  - 核心 `_gbrain_hits` 加线程安全 TTL 缓存（5 分钟滑动续期、上限 128 LRU 驱逐、`sync_index` 成功后整体失效）——AGENTS.md §八 唯一候选优化项正式立项并落地；
  - 四端共用（Hermes/Codex/Reasonix/DSH 检索均受益）；检索主体仍为本地 bigram（零延迟直读账本），缓存只加速补充命中通道，检索语义不变；
  - **生产实测：同查询冷启动 1.996s → 缓存命中 3.8ms（约 500 倍）**；
  - 回归 **82/82**（新增缓存命中/过期/写后失效 3 用例）。
- **已完成（2026-10-17 第十九批·管理台打磨，impeccable polish）**：
  - 设计系统立项：PRODUCT.md（product 面、老卢单用户、现代产品·清爽，反装饰/反模板 SaaS/反手绘，WCAG AA）+ DESIGN.md（Google Stitch 体例，六节 + named rules）+ `.impeccable/design.json` 侧车与 live 配置；
  - 主题重写：深色终端感 → 浅色现代产品（蓝相微染色中性底 oklch(0.975 0.004 250) + 单一工作蓝 oklch(0.52 0.19 255)，AA 对比全部达标，占位符/次级文本 ≥4.5:1）；「晨雾底/纸面/侧栏灰/发际线/墨/灰墨」token 化；
  - 全状态词汇：button/input 补齐 hover/focus-visible（2px 蓝环+蓝雾光晕）/active/disabled；z-index 刻度（backdrop 40/modal 50/toast 60）；动效 150-250ms ease-out 仅 transform/opacity + prefers-reduced-motion 全量降级；
  - 组件打磨：列表加载骨架屏、教学型空态、固定 toast 区域（role=status/aria-live）、弹层 role=dialog/aria-modal + Esc 关闭 + 自动聚焦、表单 label 关联、审计复选框统一 label.check、窄屏（≤860px）侧栏折叠顶栏；
  - 清理：旧哈希 dist 产物清空重部署；typecheck+build 全绿；生产部署后 /admin 与全部资源 200。
- **已完成（2026-10-17 第二十批·风格改为工作蓝，老卢指示）**：
  - 色板策略由 Restrained（单强调 ≤10%）升为 **Committed（工作蓝主调）**：新增「工作蓝深面」oklch(0.42 0.16 255) 承载侧栏整面（白字 ≈8.5:1、浅蓝次级字 ≈6.8:1），页面底改为肉眼可见的蓝染 oklch(0.965 0.012 255)，悬停面蓝洗 oklch(0.94 0.018 255)，表头蓝带、页面标题工作蓝身份线、toast 深蓝底、仪表盘数字蓝化；
  - 语义色（绿/琥珀/赭红/紫）维持只服务类型徽标与状态；对比度全部 ≥4.5:1（深蓝面文字专项核对）；
  - 设计系统同步：PRODUCT.md 品牌性格、DESIGN.md 色彩/导航/Do-Don'ts（One Voice Rule → **Blue Home Rule**）、design.json 侧车（colorMeta 增 blue-deep、narrative 全量更新）；
  - typecheck+build 全绿；生产部署后 token 实测（blue-deep/蓝染底/浅蓝次级字均在线）、/admin 200；账本已录视觉风格偏好（preference）。
- **已完成（2026-10-19 第二十一批·DSH 端自动捕获 + 账本停更诊断，老卢「全部继续」授权）**：
  - 诊断：账本 10-18 12:30 后停更**非服务故障**（API/doctor 均健康、写入链路正常）。真实原因三叠加：① Hermes 即时捕获句式门控漏收「记住：」类显式指令；② DSH 端无 MemoryProvider 钩子，只有技能按需写（当天 15 个会话只读不写）；③ 候选区 9 条历史碎片积压未复核。
  - 修复 1（核心 `gcmem.py`）：`PATTERNS` 新增「记住/记下/记一下/以后记得」句式（归 preference，入账去前缀），新增 `_match_text` 统一取捕获组；新增 `is_sensitive` 凭据守卫（token/令牌/密钥/密码/secret/bearer/长随机串一律不入账，即时捕获与候选提炼共用）；新增回归 `test_capture_remember_instruction`、`test_capture_skips_credentials`。
  - 修复 2（DSH 自动捕获，新增 `src/gcmem_dsh_capture.py`）：launchd `ai.globalcloud.gcmem-dsh-capture` 每 10 分钟增量扫描 `~/.dsh/sessions`（只认 `source.kind=user` 且带 rpcId 的真人消息，子代理任务包/runtime-context/skill-catalog 排除），复用 `cmd_capture` 句式门控入账；`ai.globalcloud.gcmem-dsh-mine` 每日 23:40 以 `llm_extract` 挖掘当天 DSH 对话：correction/preference 自动入账（≤10 条/日），decision/fact/entity 写候选文件 `gcmem-candidates-<date>-dsh.txt` 待 admin 复核；状态 `~/.hermes/queues/dsh-capture-state.json`，单轮文件锁 + 成本闸（≤40 次 LLM 调用/日）。
  - 修复 3（候选复核）：10-16（5 条）/10-18（4 条）候选逐条复核，确认均为文档引文/机器反馈碎片，**0 条入账、全部归档**至 `~/.hermes/queues/gcmem-candidates-archive/`（可恢复）；doctor 候选积压提示清除。
  - 验证：回归 **57/57**（test_gcmem 49 + test_dsh_capture 8）；`/stats` total 80→92、last=2026-10-19；doctor healthy=true；capture 首轮回填实跑 captured=1；mine 实跑 added=10/candidates=22；两个新 launchd 服务已 load 并实跑。
  - 部署：`gcmem.py`、`gcmem_dsh_capture.py` 同步 `~/.hermes/scripts/` 并重启 API；AGENTS.md §二/§三/§七 同步更新，DSH 技能补充自动捕获说明。
- **已完成（2026-10-20 第二十二批·全量排序 + 捕获误吸修复，老卢指示）**：
  - 排序（管理台 + API 全量）：列表接口统一 `sort` + `order` 参数，**默认最近时间优先（time/desc）**——`GET /v1/memories/`、`/admin/api/memories`、`/admin/api/export`（json/csv/md 三格式同步排序）、`/admin/api/candidates`（默认文件 mtime 倒序，`sort=time|name`）；管理台记忆表头「时间/类型/来源」可点击切换升降序（↕/▲/▼ + aria-sort，导出跟随当前排序），候选工作台文件默认最近优先、条目可切原始/类型/内容。
  - 优化：日终挖掘的自动入账改走 `infer=True`（LLM 语义判重/替代链），防跨日重复入账（doctor 已见两对 0.91–0.92 近似重复）。
  - 修复 DSH 自动捕获误吸：spawn/teammate 任务提示以 `kind=user + rpcId` 注入会话首条，字段上与真人消息无法区分 → 新增「首 turn 前 `agent/inbox/spliced` 注入消息 id」结构判定，即时捕获与日终挖掘双路排除；修复前已入库的 5 条片段保留（append-only，可经 admin「替代」作废）。
  - 验证：回归 **100/100**（test_gcmem 49 + test_gcmem_api 21 + test_gcmem_admin 19 + test_dsh_capture 11）；生产 API 实调——默认倒序、asc/type/mid、非法 sort/order 422 均符合，导出默认最近优先、候选文件 mtime 倒序；admin typecheck+build 全绿，新 dist 部署后 `/admin` 200 且 chunk 含排序逻辑；capture 桥实跑 captured=0（任务包已排除，真人消息保留）。
  - 部署：`gcmem_api.py`、`gcmem_dsh_capture.py` 同步 `~/.hermes/scripts/` 并重启 API；前端 `admin/dist` → `~/.hermes/admin/dist`。
- **已完成（2026-10-20 第二十三批·记忆面收敛与防重复，老卢「继续」）**：
  - 记忆面收敛：`GET /v1/memories/` 新增 `include_superseded`（默认 false，只返回活跃记忆，响应带 `ledger_total` 与每条的 `superseded` 标记）；MCP `gcmem_get` 同口径（新增 `include_superseded` 参数，默认只看活跃）。生产实测：默认 total 105 / ledger_total 119，审计模式 119。
  - 防重复入账：DSH 日终挖掘在 `infer=True` 之外增加 difflib ≥0.90 近似重复守卫（与 doctor 同口径、零 LLM 成本）；doctor 现存 2 对历史近似重复保留（append-only）。
  - 体验：记忆工作台新增每页条数选择（20/50/100/200，切换即回第 1 页）；仪表盘新增「最近记忆」卡（最近 8 条、时间倒序、跳转全部记忆）。
  - 验证：回归 **103/103**（test_gcmem 50 + test_gcmem_api 22 + test_gcmem_admin 19 + test_dsh_capture 12）；`/v1` 与 MCP get 活跃面实调；admin typecheck+build 全绿，新 dist 含「最近记忆/每页条数」且 `/admin` 200；doctor healthy=true。
  - 部署：`gcmem_api.py`/`gcmem_mcp.py`/`gcmem_dsh_capture.py` 同步 `~/.hermes/scripts/` + API 重启；前端 `admin/dist` → `~/.hermes/admin/dist`。
- **进行中（2026-10-20 第二十四批·P0 证据与治理底座）**：
  - **A3 文档基线纠偏 已完成**：README/AGENTS 成稿/vs-mem0 两文档回归基线、`MASTER-DESIGN` 增补 §11 v1.2（四端接入/双通道挖掘/捕获口径/默认活跃面与排序/防重复/检索基线）。
  - **B1 重复/噪声治理工具 已完成**：新增 `GET /admin/api/duplicates`（doctor 同口径，跳过治理记录与已废止项）+ `POST /admin/api/memories/{mid}/dedupe`、`/retire`（append-only 软处置）；管理台系统页「重复治理」面板 + 记忆详情「作废」入口；回归 106/106。
  - **B2 历史噪声处置 已完成**：2 对近似重复合并（mid 87→110、82→101）、5 条任务包误吸片段作废（mid 111–115）；doctor notes 归零；操作留痕 mid 123–129（账本 130 条、活跃 109）。
  - **A1 三夜挖掘验收 进行中（1/3）**：10-19 首夜 DSH added=10/candidates=29，mid 101–110 复核 10/10 采纳、误吸 0；10-20、10-21 夜采集中；记录 `docs/GCMEM-三夜挖掘验收.md`。
  - **A2 四端回归 已完成（2026-10-20）**：Hermes 捕获 CLI 实调 +1；Codex 新会话 MCP gcmem_get total=117；Reasonix 新会话 MCP 5 tools 握手 319ms、gcmem_get total=117/ledger=138；DSH HTTP/桥/运行指标正常。记录 `docs/GCMEM-四端回归记录.md`。
- **进行中（2026-10-20 第二十五批·P1 质量与消费体验）**：
  - **B3 候选复核效率 已完成**：候选页新增按类型/内容过滤、全选当前、清空选择、超 2 天文件提示；typecheck+build 全绿。2026-10-20 实操复核 10-19 两文件（70 条）：15 条改写入账（mid 138–152）、其余归档，候选队列清空，记录 `docs/GCMEM-候选复核记录.md`。
  - **B4 挖掘质量指标 已完成**：`gcmem_dsh_capture.py --mine` 落盘 `~/.hermes/queues/dsh-mine-stats.jsonl`（sessions/calls/items/added/candidates/skipped，支持 `--backfill` 仅指标补跑）；新增 `GET /admin/api/mining-stats` 与仪表盘「挖掘质量（近 7 天）」卡。10-19 指标已补跑（backfill，added=0）；补跑时另有 7 条真实会话偏好入账并保留。
  - **C1 检索质量评测集 已完成**：`tests/eval_queries.json`（22 条真实查询）+ `tests/eval_retrieval.py`（Hit@1/3、Recall@5、MRR，对比 relevance/recency/blend）；生产实测 relevance Hit@1 0.591 / Hit@3 0.864 / Recall@5 0.886 / MRR 0.730，recency 0.091/0.182/0.250/0.208，blend≈relevance；报告 `tests/eval_retrieval_report.json`（不提交）。
  - **C2 meta 约定 已完成**：约定 `project=`/`origin=`/`session=`；`gcmem.py capture` 支持可选 `meta`；DSH 捕获桥从会话路径自动解析并注入 `project=<GlobalCloud 项目名>`（即时捕获 + 挖掘自动入账），新增单测 3 例。
  - **C3 消费方文档 已完成**：新增 `docs/GCMEM-四端接入说明.md`（四端配置、默认活跃面/排序、治理入口、自检清单）；DSH 技能补充列表参数与治理入口；README 更新。
- **进行中（2026-10-20 第二十六批·P2 运营与外部）**：
  - **D1 管理台体验 已完成**：记忆列表批量选择/全选本页/批量作废（逐条 append-only 软处置）、表格横向滚动包裹 + 窄屏（≤860px）隐藏 meta/来源列。
  - **D2 运行指标 已完成**：`GET /admin/api/metrics`（请求/错误率、分组延迟 P50/P95、写入速率、账本规模、LLM 判重调用/失败/重复/替代/提炼计数）；仪表盘「运行指标」卡；`gcmem.py` 增加 `llm_judge_stats()` 计数（进程内，重启清零）。
  - **D3 备份/恢复演练 已完成**：新增 `scripts/backup_ledger_snapshot.sh`（每日 23:50 launchd `ai.globalcloud.gcmem-backup` 快照 + sha256，不自动删除）与 `scripts/restore_drill.sh`；演练：快照恢复 138 条 healthy、KDS git HEAD 仅 21 条 healthy（RPO 约 4 天）；记录见 `docs/GCMEM-备份恢复演练.md`。
  - **E1–E4 待外部条件**：E4 差异清单已出（`docs/GCMEM-文档同步差异清单_20261020.md`，只读盘点，KDS/GPCF 写入待授权）；E1 小G 迁移暂停、E2 Reasonix 升级回归、E3 DSH 全局指令并入。
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
