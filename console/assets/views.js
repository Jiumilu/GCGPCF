// View renderers. Every number comes from console/public/data/*.json.

import { band, empty, esc, kbd, num, row, short, tag, time } from "./ui.js";
import { resolveStatus } from "./status.js";

const PRIORITIES = ["P0", "P1", "P2"];
const STEPS = [
  ["commit", "提交", "●"],
  ["evaluate", "评估", "◑"],
  ["implement", "实施", "◐"],
  ["plan", "计划", "○"],
  ["repair", "修复", "◒"],
];


function progressCell(label, value, total, caption, tone) {
  const ratio = total > 0 ? Math.min(100, (value / total) * 100) : 0;
  return `<div class="progress-cell">
    <div class="progress-label">${esc(label)}</div>
    <div class="progress-value">${num(value)}<span> / ${num(total)}</span></div>
    <div class="progress-caption">${caption}</div>
    <div class="bar"><div class="bar-fill${tone ? ` ${tone}` : ""}" style="width:${ratio.toFixed(1)}%"></div></div>
  </div>`;
}

function facts(counts, gates, docs, loops) {
  const loop = loops
    ? `<span><a class="factlink" href="#/loops"><b>${num(loops.count)}</b> 条角色流转</a></span>`
    : "";
  return `<div class="facts">
    <a class="factlink" href="#/projects"><b>${num(counts.projects)}</b> 项目</a>
    <a class="factlink" href="#/features"><b>${num(counts.features)}</b> Feature（<b>${num(counts.active)}</b> 活跃 · ${num(counts.done)} 已关闭）</a>
    ${loop}
    <a class="factlink" href="#/gates"><b>${num(gates.count)}</b> 门禁</a>
    <a class="factlink" href="#/docs"><b>${num(docs.registered_docs)}</b> 登记文档 · 仓内 ${num(docs.repo_markdown)} 篇 Markdown</a>
  </div>`;
}

function decideItems(features, meta) {
  const items = [];
  const byId = new Map(features.map((item) => [item.id, item]));
  const blocker = features
    .filter((item) => item.blocker_count > 0)
    .sort((a, b) => b.blocker_count - a.blocker_count || a.id.localeCompare(b.id))[0];
  if (blocker) {
    items.push({
      tag: "阻塞", tone: "bad", href: `#/features/${blocker.id}`,
      title: `${blocker.id} · ${blocker.name}`,
      note: `${blocker.blocker_count} 条阻塞 · 迭代 ${blocker.iteration} · ${blocker.project}`,
      action: "裁定",
    });
  }
  const review = features.find((item) => item.review_status);
  if (review) {
    items.push({
      tag: "待评审", tone: "warn", href: `#/features/${review.id}`,
      title: `${review.id} · ${review.name}`,
      note: `评审 ${review.review_status} · 阻塞 ${review.blocker_count} 条`,
      action: "裁决",
    });
  }
  const driftIds = (meta.drift.true_drift_features || []).slice();
  if (driftIds.length) {
    items.push({
      tag: "派生漂移", tone: "warn", href: `#/features/${driftIds[0]}`,
      title: driftIds.join(" / "),
      note: `真值与 queue.json 不一致 · 迭代 ${driftIds.map((id) => (byId.get(id) || {}).iteration ?? "?").join("/")}`,
      action: "重跑",
    });
  }
  const missing = (meta.drift.items || []).filter((item) => item.kind === "missing_in_queue").map((item) => item.feature);
  if (missing.length) {
    items.push({
      tag: "队列缺项", tone: "", href: "",
      title: missing.join(" / "),
      note: "工作区存在，runtime/queue.json 无条目",
      action: "补录",
    });
  }
  return items;
}

export function home(data) {
  const { features, gates, docs, meta } = data;
  const list = features.items || [];
  const driftCount = (meta.drift.true_drift_features || []).length;
  const doneRatio = meta.counts.features ? (meta.counts.done / meta.counts.features) * 100 : 0;

  const issues = list
    .filter((item) => item.blocker_count > 0)
    .sort((a, b) => b.blocker_count - a.blocker_count || a.id.localeCompare(b.id))
    .slice(0, 6)
    .map((item) => `<a class="row issues-row" href="#/features/${esc(item.id)}">
      <span class="prio">${esc(item.priority)}</span>
      <span class="id">${esc(item.id)}</span>
      <span class="title" title="${esc(item.name)}">${esc(item.name)}</span>
      <span class="note">阻塞 ${num(item.blocker_count)} 条</span>
      <span class="count">迭代 ${num(item.iteration)}</span>
    </a>`)
    .join("");

  const decide = decideItems(list, meta)
    .map((item) => `<a class="row decide-row" href="${esc(item.href)}"${item.href ? "" : ' aria-disabled="true" tabindex="-1"'}>
      ${tag(item.tag, item.tone)}
      <span class="title" title="${esc(item.title)}">${esc(item.title)}</span>
      <span class="note" title="${esc(item.note)}">${esc(item.note)}</span>
      <span class="action">${esc(item.action)}</span>
    </a>`)
    .join("");

  const phases = ((meta.roadmap && meta.roadmap.items) || [])
    .map((item) => `<div class="phase">
      <span class="phase-no">P${num(item.phase)}</span>
      <span class="phase-text">${esc(item.text).replace(/`([^`]+)`/g, "<code>$1</code>")}</span>
    </div>`)
    .join("");

  const health = docs.health || {};
  const controlled = health.status_counts ? health.status_counts.controlled : "—";

  return `
    <section class="hero">
      <h1>项目群的交付调度台</h1>
      <p class="lede">Feature 进，证据出，门禁判。这一页只回答三件事：现在推进什么、卡在哪道门禁、要谁裁定；每个数字都来自仓库快照，可回溯到文件。</p>
      ${facts(meta.counts, gates, docs, data.loops)}
    </section>
    ${band("进度", `活跃 ${num(meta.counts.active)} · 队列 ${num(meta.counts.queue)}`, `<div class="progress-grid">
      ${progressCell("已关闭", meta.counts.done, meta.counts.features, `完成率 ${doneRatio.toFixed(0)}%`, "")}
      ${progressCell("受阻 Feature", meta.counts.features_with_blockers, meta.counts.active, `共 ${num(meta.counts.blockers)} 条阻塞`, "warn")}
      ${progressCell("派生漂移", driftCount, meta.counts.active, `${num(meta.drift.total)} 条差异 · 映射缺口 ${num((meta.drift.mapping_gap_features || []).length)} 个 Feature`, driftCount ? "bad" : "")}
    </div>`)}
    ${band("卡点", `${num(meta.counts.features_with_blockers)} 个 Feature 有阻塞 · 共 ${num(meta.counts.blockers)} 条`, `<div class="list">${issues}</div>`)}
    ${band("待裁", `${decideItems(list, meta).length} 条 · 按「谁该动」排序`, `<div class="list decide">${decide}</div>`)}
    ${band("路线", esc((meta.roadmap && meta.roadmap.source) || "ROADMAP"), `<div class="roadmap">${phases}</div>`)}
    ${band("文档与门禁", `${num(gates.count)} 道闸口 · 均可本地复跑`, `
      <div class="list gates">${(gates.items || []).map((gate) => `<div class="row gates-row">
        <span class="id">${esc(gate.id)}</span>
        <span class="title">${esc(gate.name)}</span>
        <span class="note">${esc(gate.scope)}</span>
        <span class="count">${esc(gate.last_result || (gate.script_exists ? "可跑" : "缺脚本"))}</span>
      </div>`).join("")}</div>
      <div class="docstrip">
        <span>受控 <b>${num(controlled)}</b></span>
        <span>复核逾期 <b>${num(health.review_overdue_90d)}</b>（&gt;90 天）</span>
        <span>登记 <b>${num(docs.registered_docs)}</b></span>
        <span>Loop 文档门禁 <b>${esc(health.loop_gate || "—")}</b></span>
        <span>健康快照 ${esc(health.generated_at ? time(health.generated_at) : "—")}</span>
      </div>`)}
  `;
}

/* ---------- features ---------- */

export function featuresShell(data) {
  const projects = Array.from(new Set((data.features.items || []).map((item) => item.project))).sort();
  return `
    <section class="hero compact">
      <h1>议题</h1>
      <p class="lede">${num(data.meta.counts.active)} 激活 · ${num(data.meta.counts.done)} 已关闭。按步骤分组，行内点击或 ${kbd("↑")}${kbd("↓")} 选中、${kbd("Enter")} 打开。</p>
    </section>
    <div class="toolbar">
      <input class="search" id="f-search" type="search" placeholder="搜索 ID / 名称 / 负责人" aria-label="搜索议题">
      <div class="seg" role="group" aria-label="按状态筛选">
        <button data-status="active" class="is-on" aria-pressed="true">活跃</button>
        <button data-status="done" aria-pressed="false">已关闭</button>
        <button data-status="all" aria-pressed="false">全部</button>
      </div>
      <select id="f-project" aria-label="按项目筛选">
        <option value="all">全部项目</option>
        ${projects.map((slug) => `<option value="${esc(slug)}">${esc(slug)}</option>`).join("")}
      </select>
      <div class="seg" role="group" aria-label="按优先级筛选">
        <button data-priority="all" class="is-on" aria-pressed="true">全部</button>
        ${PRIORITIES.map((p) => `<button data-priority="${p}" aria-pressed="false">${p}</button>`).join("")}
      </div>
      <span class="count" id="f-count"></span>
    </div>
    <div class="split">
      <div class="list" id="f-list" tabindex="0" role="listbox" aria-label="议题列表"></div>
      <aside class="panel" id="f-panel" aria-live="polite"></aside>
    </div>
    <p class="hint">${kbd("G")} 再按 ${kbd("H")} 返回主页 · ${kbd("⌘K")} 命令面板 · ${kbd("Esc")} 关闭右侧面板</p>
  `;
}

export function filterFeatures(features, filters) {
  const query = (filters.q || "").trim().toLowerCase();
  return features
    .filter((item) => {
      if (filters.status === "active" && item.status === "done") return false;
      if (filters.status === "done" && item.status !== "done") return false;
      if (filters.project !== "all" && item.project !== filters.project) return false;
      if (filters.priority !== "all" && item.priority !== filters.priority) return false;
      if (query) {
        const haystack = `${item.id} ${item.name} ${item.owner} ${item.project}`.toLowerCase();
        if (!haystack.includes(query)) return false;
      }
      return true;
    })
    .sort((a, b) => a.id.localeCompare(b.id));
}

export function featuresList(items, selected) {
  if (!items.length) return empty("没有符合条件的议题。");
  const groups = new Map();
  for (const item of items) {
    const key = item.status === "done" ? "done" : item.step || "plan";
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(item);
  }
  const order = STEPS.map(([key]) => key);
  if (groups.has("done")) order.push("done");
  const labels = new Map(STEPS.map(([key, label]) => [key, label]));
  labels.set("done", "已完成");

  return order
    .filter((key) => groups.has(key))
    .map((key) => {
      const list = groups.get(key);
      const rows = list.map((item) => {
        const isSel = item.id === selected;
        const drift = item.drift && item.drift.length ? `<span class="dot bad" title="派生漂移"></span>` : "";
        return `<div class="row item-row${isSel ? " is-selected" : ""}" role="option" aria-selected="${isSel}" tabindex="-1" data-id="${esc(item.id)}">
          <span class="prio">${esc(item.priority)}</span>
          <span class="id">${esc(item.id)}</span>
          <span class="title" title="${esc(item.name)}">${esc(item.name)}</span>
          <span class="note">${esc(item.project)} · ${esc(item.owner)}</span>
          <span class="count">${drift}${num(item.iteration)}</span>
        </div>`;
      });
      return `<div class="group"><div class="group-head">${esc(labels.get(key) || key)} <span>${list.length}</span></div>${rows.join("")}</div>`;
    })
    .join("");
}

export function featurePanel(item) {
  if (!item) {
    return `<div class="panel-empty">
      <p class="dim">选中一条议题查看证据与门禁。</p>
      <p class="dim">也可以直接访问 <code>#/features/${esc("F-036")}</code>。</p>
    </div>`;
  }
  const evidence = [
    ["测试", item.evidence.tests],
    ["构建", item.evidence.build],
    ["接口", item.evidence.api],
    ["截图", item.evidence.screenshots],
    ["结论", item.evidence.summary],
  ]
    .map(([label, value]) => `<div class="kv"><span class="k">${esc(label)}</span><span class="v">${dotValue(value)}</span></div>`)
    .join("");

  const gates = [
    ["功能完整", item.gates.functional_completeness],
    ["质量基线", item.gates.quality_baseline],
    ["多用户可用", item.gates.multi_user_usability],
    ["任务流 E2E", item.gates.task_flow_e2e_status],
    ["无障碍", item.gates.accessibility_status],
    ["证据不过曝", item.gates.evidence_overexposure_gate],
  ]
    .map(([label, value]) => `<div class="kv"><span class="k">${esc(label)}</span><span class="v">${dotValue(value)}</span></div>`)
    .join("");

  const blockers = (item.blockers || []).slice(0, 2)
    .map((text) => `<li>${esc(text)}</li>`)
    .join("");

  const drift = (item.drift || [])
    .map((entry) => `<li><code>${esc(entry.field)}</code> 真值 <b>${esc(entry.truth)}</b> · 派生 <b>${esc(entry.derived)}</b> <span class="tag ${resolveStatus("drift", entry.kind).tone}">${esc(resolveStatus("drift", entry.kind).label)}</span></li>`)
    .join("");

  return `
    <div class="panel-head">
      <span class="id">${esc(item.id)}</span>
      <button class="icon" id="p-close" aria-label="关闭详情面板">×</button>
    </div>
    <h2 class="panel-title">${esc(item.name)}</h2>
    <div class="panel-meta">${esc(item.priority)} · ${esc(item.project)} · ${esc(item.owner)} · 迭代 ${num(item.iteration)}</div>
    <p class="panel-goal">${esc(item.goal)}</p>
    <h3 class="panel-h">证据五件套</h3>
    ${evidence}
    <h3 class="panel-h">门禁六项</h3>
    ${gates}
    <h3 class="panel-h">阻塞 ${num(item.blocker_count)} 条</h3>
    ${blockers ? `<ul class="panel-list">${blockers}</ul>` : `<p class="dim">无</p>`}
    ${drift ? `<h3 class="panel-h">派生差异 ${num(item.drift.length)}</h3><ul class="panel-list">${drift}</ul>` : ""}
    <h3 class="panel-h">工作区</h3>
    <p class="dim mono">${esc(item.workspace)}</p>
    <p class="dim">status_ceiling <code>${esc(item.status_ceiling || "—")}</code>${item.review_status ? ` · review <code>${esc(item.review_status)}</code>` : ""} · 更新 ${esc((item.updated_at || "").slice(0, 10))}</p>
  `;
}

function dotValue(value) {
  const status = resolveStatus("evidence", value);
  return `<span class="dot ${status.tone}" aria-hidden="true"></span>${esc(status.label)}`;
}

/* ---------- gates ---------- */

export function gatesPage(data) {
  const gates = data.gates.items || [];
  const cards = gates
    .map((gate) => `<div class="gate">
      <div class="gate-head">
        <h2 class="gate-name">${esc(gate.name)}</h2>
        <span class="tag ${gate.last_result === "pass" ? "ok" : ""}">${esc(gate.last_result || (gate.script_exists ? "可跑" : "缺脚本"))}</span>
      </div>
      <p class="gate-scope">${esc(gate.scope)}</p>
      <div class="cmd">
        <code>${esc(gate.command)}</code>
        <button class="icon copy" data-copy="${esc(gate.command)}" aria-label="复制 ${esc(gate.name)} 命令">复制</button>
      </div>
      <p class="gate-script dim mono">${esc(gate.script)}</p>
    </div>`)
    .join("");

  const features = (data.features.items || []).filter((item) => item.status !== "done");
  const matrix = features
    .map((item) => {
      const cells = [item.evidence.tests, item.evidence.build, item.evidence.api, item.evidence.screenshots, item.evidence.summary]
        .map((value) => {
          const status = resolveStatus("evidence", value);
          return `<span class="dot ${status.tone}" title="${esc(status.label)}"></span>`;
        })
        .join("");
      return `<div class="row matrix-row">
        <span class="id">${esc(item.id)}</span>
        <span class="title">${esc(item.name)}</span>
        <span class="matrix">${cells}</span>
      </div>`;
    })
    .join("");

  return `
    <section class="hero compact">
      <h1>门禁</h1>
      <p class="lede">六道闸口各自独立、可本地复跑；每条命令都可以直接复制到终端。下面的证据矩阵只反映快照里的五件套状态。</p>
    </section>
    <div class="gate-grid">${cards}</div>
    ${band("证据矩阵", `${features.length} 个活跃 Feature × 五件套（测试 · 构建 · 接口 · 截图 · 结论）`, `<div class="list matrix-list">${matrix}</div>`)}
  `;
}

/* ---------- docs ---------- */

export function docsPage(data) {
  const docs = data.docs || {};
  const health = docs.health || {};
  const counts = health.status_counts || {};
  const total = Object.values(counts).reduce((sum, value) => sum + Number(value || 0), 0);
  const bars = Object.entries(counts)
    .sort((a, b) => Number(b[1]) - Number(a[1]))
    .map(([key, value]) => {
      const pct = total ? (Number(value) / total) * 100 : 0;
      return `<div class="status-row">
        <span class="k">${esc(key)}</span>
        <div class="bar"><div class="bar-fill" style="width:${pct.toFixed(1)}%"></div></div>
        <span class="count">${num(value)}</span>
      </div>`;
    })
    .join("");

  return `
    <section class="hero compact">
      <h1>台账</h1>
      <p class="lede">文档控制与健康快照。这里展示的是导出时读到的那份健康报告（${esc(time(health.generated_at || ""))}），不是实时值。</p>
      ${facts(data.meta.counts, data.gates, docs)}
    </section>
    ${band("总量", `登记 ${num(docs.registered_docs)} · 仓内 ${num(docs.repo_markdown)} 篇`, `<div class="docs-grid">
      <div class="progress-cell"><div class="progress-label">登记文档</div><div class="progress-value">${num(docs.registered_docs)}</div><div class="progress-caption">09-status 台账行数</div></div>
      <div class="progress-cell"><div class="progress-label">仓内 Markdown</div><div class="progress-value">${num(docs.repo_markdown)}</div><div class="progress-caption">与 Loop 门禁同口径</div></div>
      <div class="progress-cell"><div class="progress-label">复核逾期</div><div class="progress-value">${num(health.review_overdue_90d)}</div><div class="progress-caption">&gt;90 天未复核</div></div>
    </div>`)}
    ${band("状态分布", `健康快照 ${esc(health.generated_at ? time(health.generated_at) : "—")}`, `<div class="status-list">${bars || empty("没有状态分布数据。")}</div>`)}
    ${band("来源", "只读", `<div class="kv"><span class="k">台账</span><span class="v mono">${esc((docs.sources || [])[0] || "—")}</span></div>
      <div class="kv"><span class="k">健康报告</span><span class="v mono">${esc((docs.sources || [])[1] || "—")}</span></div>
      <div class="kv"><span class="k">Loop 门禁</span><span class="v">${esc(health.loop_gate || "—")}</span></div>
      <div class="kv"><span class="k">治理上限</span><span class="v">${esc(health.status_ceiling || "—")}</span></div>`)}
  `;
}

export function projectsPage(data) {
  const projects = (data.projects.items || []).slice().sort(
    (a, b) => b.active_features - a.active_features || a.slug.localeCompare(b.slug),
  );
  const withActive = projects.filter((item) => item.active_features > 0).length;
  const totalActive = projects.reduce((sum, item) => sum + item.active_features, 0);
  const rows = projects
    .map((item) => {
      const missing = [
        ["STATUS", item.has_status],
        ["ROADMAP", item.has_roadmap],
        ["RISK", item.has_risk],
      ].filter(([, ok]) => !ok).map(([label]) => label);
      const entries = missing.length
        ? missing.map((label) => `<span class="entry is-missing">缺 ${esc(label)}</span>`).join("")
        : `<span class="entry">齐全</span>`;
      return `<div class="row proj-row">
        <span class="slug">${esc(item.slug)}</span>
        <span class="title">${esc(item.repo || item.id)}</span>
        <span class="count">${num(item.active_features)}</span>
        <span class="count">${num(item.total_features)}</span>
        <span class="entries">${entries}</span>
      </div>`;
    })
    .join("");
  const retired = (data.projects.unregistered_attribution || [])
    .map((slug) => `<code>${esc(slug)}</code>`)
    .join("、");

  return `
    <section class="hero compact">
      <h1>项目</h1>
      <p class="lede">${num(projects.length)} 个项目登记在 <code>config/project-group-projects.yaml</code>；活跃列来自 feature.yaml 的归属，入口列只表示文件是否存在，不表示内容已复核。</p>
      <div class="facts">
        <span><b>${num(withActive)}</b> 个项目有活跃 Feature</span>
        <span>活跃条目合计 <b>${num(totalActive)}</b></span>
        <span>无活跃归属 <b>${num(projects.length - withActive)}</b> 个</span>
      </div>
    </section>
    <div class="list proj-head">
      <span class="slug">项目</span><span class="title">名称</span>
      <span class="count">活跃</span><span class="count">总计</span><span class="entries">入口</span>
    </div>
    <div class="list">${rows}</div>
    ${retired ? `<p class="hint">历史归属：${retired} 已退出项目清单，其 Feature 保留为历史口径，不计入活跃分母。</p>` : ""}
  `;
}

export function loopsPage(data) {
  const loops = data.loops || { count: 0, features: 0, by_role: {}, items: [] };
  const items = (loops.items || []).slice().reverse();
  const roles = Object.entries(loops.by_role || {}).sort((a, b) => b[1] - a[1]);
  const peak = roles.length ? roles[0][1] : 1;
  const roleRows = roles
    .map(([role, count]) => `<div class="status-row">
      <span class="k">${esc(role)}</span>
      <div class="bar"><div class="bar-fill" style="width:${((count / peak) * 100).toFixed(1)}%"></div></div>
      <span class="count">${num(count)}</span>
    </div>`)
    .join("");
  const recent = items.slice(0, 24)
    .map((item) => `<div class="row loop-row">
      <span class="id">${esc(shortTime(item.at))}</span>
      <span class="id">${esc(item.feature)}</span>
      <span><span class="tag">${esc(item.role)}</span></span>
      <span class="note">${esc(item.status)}</span>
      <span class="title" title="${esc(item.output || item.input)}">${esc(item.output || item.input)}</span>
    </div>`)
    .join("");

  return `
    <section class="hero compact">
      <h1>循环</h1>
      <p class="lede">来自 <code>runtime/logs/F-*.jsonl</code> 的角色流转：Dispatcher → Planner → Builder → Evaluator → Repair → Recorder。这里只回放已经落盘的事实，不做推断。</p>
      <div class="facts">
        <span><b>${num(loops.count)}</b> 条流转</span>
        <span><b>${num(loops.features)}</b> 个 Feature</span>
        <span>${roles.length} 个角色有记录</span>
      </div>
    </section>
    ${band("角色分布", `${num(loops.count)} 条`, `<div class="status-list">${roleRows || empty("没有流转记录。")}</div>`)}
    ${band("最近流转", `最新 ${Math.min(24, loops.count)} 条`, `<div class="list">${recent || empty("没有流转记录。")}</div>`)}
  `;
}

function shortTime(iso) {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.valueOf())) return String(iso).slice(5, 16);
  return date.toLocaleString("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", hour12: false });
}

export { short };
