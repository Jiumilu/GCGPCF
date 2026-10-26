// GPCF console · router, command palette and keyboard layer (stage 3).
// Data: console/public/data/*.json written by scripts/console_export.py (read-only).
// Serve with: python3 -m http.server 4173 --directory console

import { esc, num, short, time } from "./ui.js";
import {
  docsPage,
  featurePanel,
  featuresList,
  featuresShell,
  filterFeatures,
  gatesPage,
  home,
  projectsPage,
} from "./views.js";

const DATA = "./public/data";

const state = {
  data: null,
  route: { name: "home", id: null },
  filters: { status: "active", project: "all", priority: "all", q: "" },
  selected: null,
};

const $ = (selector) => document.querySelector(selector);

function parseHash() {
  const hash = (location.hash || "#/").replace(/^#/, "");
  const match = hash.match(/^\/features(?:\/(F-\d{3}))?$/);
  if (match) return { name: "features", id: match[1] || null };
  if (hash === "/projects") return { name: "projects", id: null };
  if (hash === "/gates") return { name: "gates", id: null };
  if (hash === "/docs") return { name: "docs", id: null };
  return { name: "home", id: null };
}

/* ---------- features body ---------- */

function currentFeature(id) {
  return (state.data.features.items || []).find((item) => item.id === id) || null;
}

function paintFeatures() {
  const list = $("#f-list");
  const panel = $("#f-panel");
  if (!list || !panel || !state.data) return;
  const items = filterFeatures(state.data.features.items || [], state.filters);
  list.innerHTML = featuresList(items, state.selected);
  panel.innerHTML = featurePanel(currentFeature(state.selected));
  const count = $("#f-count");
  if (count) {
    const scoped = (state.data.features.items || []).filter((item) =>
      state.filters.status === "done" ? true : item.status !== "done",
    ).length;
    count.textContent = `${num(items.length)} / ${num(scoped)}`;
  }
  $("#p-close")?.addEventListener("click", () => selectFeature(null));
  list.querySelector(".item-row.is-selected")?.scrollIntoView({ block: "nearest" });
}

function selectFeature(id, { push = true } = {}) {
  state.selected = id;
  paintFeatures();
  if (push) history.replaceState(null, "", id ? `#/features/${id}` : "#/features");
}

function bindFeatures() {
  const search = $("#f-search");
  search?.addEventListener("input", () => {
    state.filters.q = search.value;
    paintFeatures();
  });

  const project = $("#f-project");
  project?.addEventListener("change", () => {
    state.filters.project = project.value;
    paintFeatures();
  });

  const bindSeg = (attr, field) => {
    document.querySelectorAll(`[data-${attr}]`).forEach((button) => {
      button.addEventListener("click", () => {
        state.filters[field] = button.dataset[attr];
        document.querySelectorAll(`[data-${attr}]`).forEach((other) => {
          const on = other === button;
          other.classList.toggle("is-on", on);
          other.setAttribute("aria-pressed", String(on));
        });
        paintFeatures();
      });
    });
  };
  bindSeg("status", "status");
  bindSeg("priority", "priority");

  const list = $("#f-list");
  if (list) {
    list.addEventListener("click", (event) => {
      const row = event.target.closest(".item-row");
      if (row) selectFeature(row.dataset.id);
    });
    list.addEventListener("keydown", onListKey);
  }
}

function moveSelection(step) {
  const list = $("#f-list");
  if (!list) return;
  const rows = Array.from(list.querySelectorAll(".item-row"));
  if (!rows.length) return;
  const current = rows.findIndex((row) => row.dataset.id === state.selected);
  const next = current < 0 ? 0 : Math.min(rows.length - 1, Math.max(0, current + step));
  selectFeature(rows[next].dataset.id);
  rows[next].focus({ preventScroll: true });
}

function onListKey(event) {
  if (event.key === "ArrowDown" || event.key === "j") {
    event.preventDefault();
    moveSelection(1);
  } else if (event.key === "ArrowUp" || event.key === "k") {
    event.preventDefault();
    moveSelection(-1);
  } else if (event.key === "Enter") {
    const row = event.target.closest(".item-row");
    const id = row ? row.dataset.id : state.selected;
    if (id) {
      event.preventDefault();
      focusList = true;
      location.hash = `#/features/${id}`;
    }
  } else if (event.key === "Escape") {
    event.preventDefault();
    selectFeature(null);
  }
}

/* ---------- gates copy ---------- */

function bindGates() {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", async () => {
      const text = button.dataset.copy;
      try {
        await navigator.clipboard.writeText(text);
        button.textContent = "已复制";
      } catch (error) {
        button.textContent = "复制失败";
      }
      setTimeout(() => {
        button.textContent = "复制";
      }, 1400);
    });
  });
}

/* ---------- palette ---------- */

const palette = { items: [], index: 0 };

function paletteEntries() {
  const entries = [
    { label: "主页", hint: "总览", run: () => { location.hash = "#/"; } },
    { label: "议题", hint: "features", run: () => { location.hash = "#/features"; } },
    { label: "项目", hint: "projects", run: () => { location.hash = "#/projects"; } },
    { label: "门禁", hint: "gates", run: () => { location.hash = "#/gates"; } },
    { label: "台账", hint: "docs", run: () => { location.hash = "#/docs"; } },
    { label: "切换主题", hint: "theme", run: toggleTheme },
  ];
  if (state.data) {
    for (const item of state.data.features.items || []) {
      entries.push({
        label: `${item.id} · ${item.name}`,
        hint: `${item.project} · ${item.priority}`,
        run: () => { location.hash = `#/features/${item.id}`; },
      });
    }
  }
  return entries;
}

function renderPalette(query = "") {
  const list = $("#palette-list");
  if (!list) return;
  const needle = query.trim().toLowerCase();
  palette.items = paletteEntries()
    .filter((entry) => !needle || `${entry.label} ${entry.hint}`.toLowerCase().includes(needle))
    .slice(0, 12);
  palette.index = Math.min(palette.index, Math.max(0, palette.items.length - 1));
  list.innerHTML =
    palette.items
      .map(
        (entry, index) => `<li class="palette-item${index === palette.index ? " is-active" : ""}" data-index="${index}">
          <span class="palette-label">${esc(entry.label)}</span>
          <span class="palette-hint">${esc(entry.hint)}</span>
        </li>`,
      )
      .join("") || `<li class="palette-empty">没有匹配项</li>`;
  list.querySelectorAll(".palette-item").forEach((node) => {
    node.addEventListener("click", () => runPalette(Number(node.dataset.index)));
  });
}

function openPalette() {
  const dialog = $("#palette");
  if (!dialog) return;
  if (typeof dialog.showModal === "function" && !dialog.open) dialog.showModal();
  else dialog.setAttribute("open", "");
  const input = $("#palette-input");
  if (input) {
    input.value = "";
    input.focus();
  }
  palette.index = 0;
  renderPalette("");
}

function closePalette() {
  const dialog = $("#palette");
  if (!dialog) return;
  if (typeof dialog.close === "function" && dialog.open) dialog.close();
  else dialog.removeAttribute("open");
}

function runPalette(index) {
  const entry = palette.items[index];
  if (!entry) return;
  closePalette();
  entry.run();
}

/* ---------- theme ---------- */

function toggleTheme() {
  const root = document.documentElement;
  const next = root.dataset.theme === "light" ? "dark" : "light";
  root.dataset.theme = next;
  try {
    localStorage.setItem("gpcf-theme", next);
  } catch (error) {
    /* ignore */
  }
  const button = $("#theme-toggle");
  if (button) button.textContent = next === "light" ? "☾" : "☀";
}

/* ---------- router ---------- */

function renderRoute() {
  const route = parseHash();
  state.route = route;
  if (route.name === "features") state.selected = route.id;

  const app = $("#app");
  if (!state.data || !app) return;
  app.setAttribute("aria-busy", "false");

  if (route.name === "home") {
    app.innerHTML = home(state.data);
  } else if (route.name === "features") {
    app.innerHTML = featuresShell(state.data);
    bindFeatures();
    const search = $("#f-search");
    if (search) search.value = state.filters.q;
    paintFeatures();
  } else if (route.name === "projects") {
    app.innerHTML = projectsPage(state.data);
  } else if (route.name === "gates") {
    app.innerHTML = gatesPage(state.data);
    bindGates();
  } else {
    app.innerHTML = docsPage(state.data);
  }

  document.querySelectorAll("[data-route]").forEach((link) => {
    link.setAttribute("aria-current", link.dataset.route === route.name ? "page" : "false");
  });

  const titles = { home: "治理控制仓", features: "议题", projects: "项目", gates: "门禁", docs: "台账" };
  document.title = `${titles[route.name]} · GPCF`;
  window.scrollTo({ top: 0, behavior: "auto" });
  if (route.name === "features" && focusList) {
    $("#f-list")?.focus({ preventScroll: true });
    focusList = false;
  }
}

/* ---------- keyboard ---------- */

function isTyping(target) {
  if (!target) return false;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || target.isContentEditable;
}

let sequence = "";
let focusList = false;

function onKeydown(event) {
  const key = event.key.toLowerCase();

  if ((event.metaKey || event.ctrlKey) && key === "k") {
    event.preventDefault();
    openPalette();
    return;
  }
  if (event.key === "Escape") {
    if (state.route.name === "features" && state.selected) {
      event.preventDefault();
      selectFeature(null);
    }
    return;
  }
  if (isTyping(event.target) || event.metaKey || event.ctrlKey || event.altKey) return;

  if (["g", "h", "f", "p", "d"].includes(key)) {
    sequence = (sequence + key).slice(-2);
    if (sequence === "gh") {
      location.hash = "#/";
      sequence = "";
    } else if (sequence === "gf") {
      focusList = true;
      location.hash = "#/features";
      sequence = "";
    } else if (sequence === "gp") {
      location.hash = "#/projects";
      sequence = "";
    } else if (sequence === "gg") {
      location.hash = "#/gates";
      sequence = "";
    } else if (sequence === "gd") {
      location.hash = "#/docs";
      sequence = "";
    }
    return;
  }
  sequence = "";
}

/* ---------- boot ---------- */

async function loadData() {
  const names = ["features", "projects", "gates", "docs", "meta"];
  const payloads = await Promise.all(
    names.map(async (name) => {
      const response = await fetch(`${DATA}/${name}.json`, { cache: "no-store" });
      if (!response.ok) throw new Error(`${name}.json HTTP ${response.status}`);
      return [name, await response.json()];
    }),
  );
  state.data = Object.fromEntries(payloads);
}

function fail(error) {
  const app = $("#app");
  if (!app) return;
  app.setAttribute("aria-busy", "false");
  app.innerHTML = `<div class="error">
    <h2>数据没有加载出来</h2>
    <p>先运行 <code>python3 scripts/console_export.py</code> 生成快照，再用本地静态服务器打开：<code>python3 -m http.server 4173 --directory console</code></p>
    <p style="margin-top:8px">${esc(error && error.message ? error.message : error)}</p>
  </div>`;
}

function bindChrome() {
  const input = $("#palette-input");
  input?.addEventListener("input", (event) => {
    palette.index = 0;
    renderPalette(event.target.value);
  });
  input?.addEventListener("keydown", (event) => {
    if (event.key === "ArrowDown") {
      event.preventDefault();
      palette.index = Math.min(palette.index + 1, Math.max(0, palette.items.length - 1));
      renderPalette(input.value);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      palette.index = Math.max(0, palette.index - 1);
      renderPalette(input.value);
    } else if (event.key === "Enter") {
      event.preventDefault();
      runPalette(palette.index);
    }
  });
  $("#palette")?.addEventListener("close", () => {
    $("#palette-trigger")?.focus({ preventScroll: true });
  });
  document.querySelectorAll("[data-open-palette]").forEach((button) => {
    button.addEventListener("click", () => openPalette());
  });
  $("#theme-toggle")?.addEventListener("click", toggleTheme);
  window.addEventListener("hashchange", renderRoute);
  document.addEventListener("keydown", onKeydown);
}

async function main() {
  bindChrome();
  try {
    await loadData();
    renderRoute();
    $("#masthead-meta").textContent = `快照 ${time(state.data.meta.generated_at)} · ${short(state.data.meta.source_sha, 9)}`;
    const foot = $("#pagefoot");
    if (foot) {
      const meta = state.data.meta;
      foot.innerHTML = `
        <div>真值来源 ${esc(meta.truth_source.feature)} · 映射 ${esc(meta.truth_source.mapping)}</div>
        <div>快照生成 ${time(meta.generated_at)} · 源提交 ${esc(meta.source_sha || "—")}</div>
        <ul class="claims">${(meta.non_claims || []).map((claim) => `<li>${esc(claim)}</li>`).join("")}</ul>
      `;
    }
    if (new URLSearchParams(location.search).has("probe")) {
      const body = getComputedStyle(document.body);
      document.body.dataset.probe = JSON.stringify({
        innerWidth: window.innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        route: state.route.name,
        rows: document.querySelectorAll(".row").length,
        ink: body.color,
        bg: body.backgroundColor,
      });
    }
    window.__gpcf = {
      route: () => state.route,
      selected: () => state.selected,
      paletteOpen: () => Boolean($("#palette")?.open),
      short,
    };
  } catch (error) {
    fail(error);
    if (new URLSearchParams(location.search).has("probe")) {
      document.body.dataset.probe = JSON.stringify({ error: String(error) });
    }
  }
}

main();
