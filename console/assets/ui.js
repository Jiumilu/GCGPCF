// Shared helpers for the GPCF console views.

export const esc = (value) =>
  String(value ?? "").replace(/[&<>"']/g, (ch) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  }[ch]));

export const num = (value) => Number(value ?? 0).toLocaleString("zh-CN");

export const short = (value, keep = 8) => (value ? String(value).slice(0, keep) : "—");

export const time = (iso) => {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.valueOf())) return esc(iso);
  return date.toLocaleString("zh-CN", { hour12: false });
};

export const row = (cells, className = "") =>
  `<div class="row ${className}">${cells.join("")}</div>`;

export const band = (title, note, body, id = "") =>
  `<section class="band"${id ? ` id="${esc(id)}"` : ""}>
    <div class="band-head">
      <h2 class="band-title">${esc(title)}</h2>
      <div class="band-note">${note}</div>
    </div>
    ${body}
  </section>`;

export const tag = (text, tone = "") =>
  `<span class="tag ${tone}">${esc(text)}</span>`;

export const empty = (text) => `<p class="empty">${esc(text)}</p>`;

export const kbd = (text) => `<kbd>${esc(text)}</kbd>`;
