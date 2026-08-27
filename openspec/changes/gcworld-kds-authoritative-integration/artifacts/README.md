---
doc_id: GPCF-DOC-GCWORLD-049
title: GCWORLD与KDS权威事实集成治理产物
project: GPCF
related_projects: [KDS, WAS, WAES, XWAIL]
domain: openspec
status: draft
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/openspec/changes/gcworld-kds-authoritative-integration/artifacts/README.md
source_path: openspec/changes/gcworld-kds-authoritative-integration/artifacts/README.md
sync_direction: bidirectional
last_reviewed: 2026-08-24
supersedes: []
superseded_by: []
---

# GCWORLD与KDS权威事实集成治理产物

本目录保存独立授权、准入评估和责任方处置请求。D1—D4的历史批准保留，但对应基线已于2026年8月25日失效；Stage A没有激活，不得开始实现。

| 产物 | 用途 |
| --- | --- |
| `gcworld-kds-integration-authorization-request-20260824.yaml` | 已签发后因基线变化在激活前失效的授权范围 |
| `gcworld-kds-integration-authorization-receipt-20260824.yaml` | D1—D4人工批准的可审计回执 |
| `gcworld-kds-integration-authorization-invalidation-20260825.yaml` | 授权基线失效事实与影响范围 |
| `gcworld-kds-14-change-owner-disposition-request-20260824.yaml` | 已被取代、不得交付的14项处置请求 |
| `gcworld-kds-17-change-owner-disposition-request-20260825.yaml` | 已批准、已交付并由KDS责任方接收的17项处置请求 |
| `gcworld-kds-17-change-scope-approval-receipt-20260825.yaml` | 17项扩展范围与交付边界的人工批准回执 |
| `gcworld-kds-17-change-owner-dispatch-receipt-20260825.yaml` | 请求已送达且责任方已确认基线的可审计回执 |
| `gcworld-kds-owner-handoff-receipt-20260825.yaml` | KDS责任方17项归属、保留和处置建议回执 |
| `gcworld-kds-stabilization-authorization-request-20260825.yaml` | D5至D8四类独立专项授权请求 |
| `gcworld-kds-owner-handoff-assessment-20260825.md` | 责任方结论、持续生成源与推荐顺序评估 |
| `gcworld-kds-post-handoff-drift-20260825.yaml` | 责任方零写入回执后由17项增至28项的漂移事实 |
| `gcworld-kds-28-change-owner-disposition-request-20260825.yaml` | 已批准、已交付并完成责任方补充分析的28项只读请求 |
| `gcworld-kds-28-change-scope-approval-receipt-20260825.yaml` | D4只读范围由17项扩展至28项的人工批准回执 |
| `gcworld-kds-28-change-owner-dispatch-receipt-20260825.yaml` | 新增11项已送达KDS责任线程的交付回执 |
| `gcworld-kds-28-change-owner-handoff-receipt-20260825.yaml` | KDS责任方对新增11项来源、保留和稳定窗口的只读补充回执 |
| `gcworld-kds-28-stabilization-authorization-request-20260825.yaml` | 覆盖28项生产者控制、逐路径处置、恢复及重新准入的待独立批准请求 |
| `gcworld-kds-post-d4-drift-20260825.yaml` | D4二十八项补充分析完成后工作树增至二十九项的只读漂移证据 |
| `gcworld-kds-29-change-owner-disposition-request-20260825.yaml` | 已获批准但因交付前漂移而未交付的二十九项只读补充分析请求 |
| `gcworld-kds-29-change-scope-approval-receipt-20260825.yaml` | 二十九项扩围获批但因交付前漂移未生效的人工批准回执 |
| `gcworld-kds-post-29-approval-drift-20260825.yaml` | 二十九项批准后、交付前工作树增至三十一项的只读漂移证据 |
| `gcworld-kds-31-change-owner-disposition-request-20260825.yaml` | 已批准并送达KDS责任方的三十一项只读补充分析请求 |
| `gcworld-kds-31-change-scope-approval-receipt-20260825.yaml` | 三十一项只读范围与责任方交付边界的人工批准回执 |
| `gcworld-kds-31-change-owner-dispatch-receipt-20260825.yaml` | 三项只读补充分析已送达KDS责任线程的交付回执 |
| `gcworld-kds-31-request-reseal-receipt-20260825.yaml` | 责任方发现请求哈希差异后的GPCF解释与最终重封回执 |
| `gcworld-kds-31-change-owner-handoff-receipt-20260825.yaml` | 三项来源、运行关系、处置建议和稳定窗口的责任方最终回执 |
| `gcworld-kds-31-stabilization-authorization-request-20260825.yaml` | 覆盖31项生产者控制、代码审阅、逐路径处置、恢复及重新准入的待独立批准请求 |
| `gcworld-kds-d5-d9-approval-receipt-20260825.yaml` | D5至D9范围和禁止边界的人工批准回执 |
| `gcworld-kds-d5-d9-partial-execution-receipt-20260825.yaml` | D5至D7完成、D8与D9因漂移停止的逐项执行回执 |
| `gcworld-kds-post-d5-d7-drift-20260825.yaml` | KDS由31项增至32项及本轮Python缓存副作用的漂移证据 |
| `gcworld-kds-32-followup-authorization-request-20260825.yaml` | 单一路径恢复与D8、D9重新授权的D16、D17待决请求 |
| `gcworld-kds-d16-d17-approval-receipt-20260825.yaml` | D16单路径恢复与D17冻结协调的人工批准回执 |
| `gcworld-kds-d16-d17-execution-receipt-20260825.yaml` | 精确恢复31项基线、两侧冻结确认与纯元数据来源调查回执 |
| `gcworld-kds-31-stable-window-receipt-20260825.yaml` | 31项路径、状态及严格元数据持续稳定超过10分钟的只读回执 |
| `gcworld-kds-post-stable-window-authorization-request-20260825.yaml` | 两个代码路径受控正文与差异审阅的D10独立授权请求 |
| `gcworld-kds-d10-approval-receipt-20260825.yaml` | 两个代码路径受控正文与差异审阅的D10人工批准回执 |
| `gcworld-kds-d10-owner-review-request-20260825.yaml` | 经密封并送达KDS源码与测试责任方的两文件只读审阅请求 |
| `gcworld-kds-d10-owner-review-receipt-20260825.yaml` | 需求来源、变化目的、代码测试对应关系、风险与推荐处置的只读回执 |
| `gcworld-kds-d12-readonly-review-authorization-request-20260825.yaml` | D12第一阶段剩余二十九项逐路径分级先行、只读审阅的独立授权请求 |
| `gcworld-kds-d12-r1-approval-receipt-20260825.yaml` | D12-R1二十九项分级先行只读审阅的人工批准回执 |
| `gcworld-kds-d12-r1-classification-manifest-20260825.yaml` | 独立分级台账对二十九项的精确匹配清单及正文加载决定 |
| `gcworld-kds-d12-r1-owner-review-request-20260825.yaml` | 密封并分配至KDS与知识工程责任方的D12-R1只读任务 |
| `gcworld-kds-d12-r1-owner-review-receipt-20260825.yaml` | 二十九项逐路径内容或元数据结论、风险和唯一推荐处置总回执 |
| `gcworld-kds-d12-c1-classification-governance-authorization-request-20260825.yaml` | 十六项UNKNOWN零正文、双责任方分级治理的独立授权请求 |
| `gcworld-kds-d12-c1-request-validation-receipt-20260825.yaml` | D12-C1请求结构、31项基线、生产者冻结和项目群门禁的密封验证回执 |
| `gcworld-kds-d12-c1-approval-receipt-20260825.yaml` | D12-C1十六项零正文双责任方分级裁决的人工批准回执 |
| `gcworld-kds-d12-c1-reviewer-declaration-request-20260825.yaml` | 交付两类独立责任方的十六项签名式零正文分级声明请求 |
| `gcworld-kds-d12-c1-reviewer-a-declaration-20260825.yaml` | KDS数据分级与安全责任方对十六项的独立签名式零正文声明 |
| `gcworld-kds-d12-c1-reviewer-b-declaration-20260825.yaml` | 项目群知识工程与内容权威责任方对十六项的独立签名式零正文声明 |
| `gcworld-kds-d12-c1-classification-receipt-20260825.yaml` | 两方均为UNKNOWN、十六项进入例外队列且后续均未授权的D12-C1总回执 |
| `gcworld-kds-d12-c2-authority-attestation-authorization-request-20260825.yaml` | 已因31项到32项漂移在人工决定前失效、不得沿用的D12-C2请求 |
| `gcworld-kds-post-d12-c2-request-drift-20260825.yaml` | D12-C2请求生成后KDS由31项变为32项并使请求在人工决定前失效的只读漂移回执 |
| `gcworld-kds-d12-c2-reseal-approval-receipt-20260825.yaml` | 仅恢复指定单一pyc路径并重建31项基线的人工批准回执 |
| `gcworld-kds-d12-c2-reseal-execution-receipt-20260825.yaml` | 单路径恢复、31项三类指纹和生产者冻结复核的执行回执 |
| `gcworld-kds-d12-c2-authority-attestation-authorization-request-r1-20260825.yaml` | 重新密封后因同一目标路径再次漂移而在人工决定前失效的R1请求 |
| `gcworld-kds-post-d12-c2-r1-validation-drift-20260825.yaml` | R1生成后同一pyc再次变化、非目标31项仍精确一致的漂移回执 |
| `gcworld-kds-d12-c2-final-recovery-execution-receipt-20260825.yaml` | 第二次仅恢复同一获批目标路径并重建31项的最终执行回执 |
| `gcworld-kds-d12-c2-authority-attestation-authorization-request-r2-20260825.yaml` | 最终重新密封、等待独立人工决定的D12-C2十六项逐路径权威声明请求 |
| `gcworld-kds-d12-c2-r2-approval-receipt-20260825.yaml` | D12-C2 R2零正文权威声明治理的人工批准回执 |
| `gcworld-kds-d12-c2-r2-authority-declaration-request-20260825.yaml` | 向KDS和项目群内容权威协调责任方交付的16项逐路径声明请求 |
| `gcworld-kds-d12-c2-r2-reviewer-a-declaration-20260825.yaml` | KDS责任方16项权威未验证、证据不足并保持UNKNOWN的签名声明 |
| `gcworld-kds-d12-c2-r2-reviewer-b-nonresponse-receipt-20260825.yaml` | 第二责任方未在受控执行窗口返回逐项声明的从严回执 |
| `gcworld-kds-d12-c2-r2-classification-receipt-20260825.yaml` | 16项全部保持UNKNOWN、无可登记分类且D12-C2仍为partial的总回执 |
| `gcworld-kds-d12-c2-s1-authority-nomination-authorization-request-20260825.yaml` | 六类真实内容权威主体提名、可选替代复核方与逐路径零正文补充声明的待决独立授权请求 |
| `gcworld-kds-d12-c2-s1-approval-receipt-20260825.yaml` | S1-A与S1-C获批、S1-B未批准的人工决定回执 |
| `gcworld-kds-d12-c2-s1-authority-nomination-request-20260825.yaml` | 向两个既有责任线程交付的六类零内容权威主体提名请求 |
| `gcworld-kds-d12-c2-s1-kds-authority-nomination-declaration-20260825.yaml` | KDS责任线程四组均无法验证真实内容权威主体的签名声明 |
| `gcworld-kds-d12-c2-s1-knowledge-authority-nonresponse-receipt-20260825.yaml` | 项目群知识工程责任线程未返回三组提名声明的从严回执 |
| `gcworld-kds-d12-c2-s1-execution-receipt-20260825.yaml` | 六组零权威主体通过、S1-C无合法收件人且16项继续UNKNOWN的执行总回执 |
| `gcworld-kds-d12-c2-s2-human-authority-designation-request-20260825.yaml` | 六组真实内容权威主体逐组人工指定或明确保持UNKNOWN的待决独立请求 |
| `gcworld-kds-d12-c2-s2-approval-input-receipt-20260825.yaml` | S2获准执行但六组仍为未单选占位符、权威字段为空的人工输入回执 |
| `gcworld-kds-d12-c2-s2-execution-receipt-20260825.yaml` | 六组决定均不完整、零权威指定且十六项继续UNKNOWN的从严执行回执 |
| `gcworld-kds-d12-c2-s2-supplemental-decision-receipt-20260825.yaml` | 老卢以“A”明确六个分组全部选择keep_unknown的人工补充决定回执 |
| `gcworld-kds-d12-c2-s2-closure-receipt-20260825.yaml` | 六组决定已明确、但最终31项基线漂移后按规则停止且尚未生效完成的收口回执 |
| `gcworld-kds-post-d12-c2-s2-closure-drift-20260825.yaml` | S2收口最终复核时31项变为32项、非目标31项仍精确一致并按规则停止的漂移回执 |
| `gcworld-kds-d12-c2-s2-rebaseline-manifest-20260826.yaml` | 旧HEAD至新HEAD单提交、33项Git处置和新干净快照的只读重新基线清单 |
| `gcworld-kds-d12-c2-s2-readonly-rebase-audit-receipt-20260826.yaml` | 33项已进入main但治理有效性不能由Git元数据证明的只读审计总回执 |
| `gcworld-kds-d12-c2-s2-new-baseline-followup-authorization-request-20260826.yaml` | 接受新基线、保持16项UNKNOWN、冻结GBrain和完成S2收口的后续独立授权请求 |
| `gcworld-kds-d12-c2-s2-gbrain-consistency-audit-control-20260826.yaml` | GBrain检索主链路与后台Supervisor、同步任务元数据一致性的只读审计控制 |
| `gcworld-kds-d12-c2-s2-gbrain-component-status-matrix-20260826.yaml` | GBrain、KDS、Hermes与同步任务逐组件健康分级矩阵 |
| `gcworld-kds-d12-c2-s2-gbrain-consistency-audit-receipt-20260826.yaml` | 检索可用但后台仍降级、不一致的受控只读审计回执 |
| `gcworld-kds-d12-c2-s2-gbrain-consistency-followup-authorization-request-20260826.yaml` | RB3配置归属零凭据只读核对的后续独立授权请求 |
| `gcworld-kds-d12-c2-s2-gbrain-rb3-config-ownership-partial-matrix-20260826.yaml` | RB3安全结构字段、暂定归属与范围偏差的部分矩阵 |
| `gcworld-kds-d12-c2-s2-gbrain-rb3-config-ownership-audit-receipt-20260826.yaml` | RB3因日志路径误哈希而停止、零正文输出和零运行变更的偏差回执 |
| `gcworld-kds-d12-c2-s2-gbrain-rb3r1-corrected-replay-authorization-request-20260826.yaml` | 硬排除日志路径后的RB3R1纠正只读重放请求 |
| `gcworld-kds-post-handoff-drift-assessment-20260825.md` | 新增11项范围、授权失效与下一门禁评估 |
| `gcworld-kds-integration-admission-assessment-20260824.md` | 昨日准入事实与阻塞判断 |
| `gcworld-kds-integration-admission-refresh-20260825.md` | 今日基线失效与准入刷新判断 |
