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

export function age(iso) {
  if (!iso) return { label: "—", stale: true };
  const stamp = new Date(iso).valueOf();
  if (Number.isNaN(stamp)) return { label: "—", stale: true };
  const minutes = Math.max(0, Math.round((Date.now() - stamp) / 60000));
  const label = minutes < 1 ? "刚刚"
    : minutes < 60 ? `${minutes} 分钟前`
    : minutes < 1440 ? `${Math.round(minutes / 60)} 小时前`
    : `${Math.round(minutes / 1440)} 天前`;
  return { label, stale: minutes > 1440 };
}

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
