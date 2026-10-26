// Single source of truth for status labels and tones (v1.4 G-UI-3).
// Every view resolves a raw value through resolveStatus() instead of
// carrying its own label map.

export const statusDictionary = {
  // 证据五件套
  evidence: {
    pass: { label: "通过", tone: "ok" },
    waived: { label: "豁免", tone: "dim" },
    pending: { label: "待补", tone: "warn" },
    fail: { label: "失败", tone: "bad" },
  },
  // ui_product_first_control 六项门禁
  gate: {
    pass: { label: "通过", tone: "ok" },
    waived: { label: "豁免", tone: "dim" },
    pending: { label: "待补", tone: "warn" },
    fail: { label: "失败", tone: "bad" },
  },
  // LOOP 步骤
  step: {
    plan: { label: "计划", glyph: "○" },
    implement: { label: "实施", glyph: "◐" },
    evaluate: { label: "评估", glyph: "◑" },
    commit: { label: "提交", glyph: "●" },
    repair: { label: "修复", glyph: "◒" },
    done: { label: "已完成", glyph: "✔" },
  },
  // 派生视图差异
  drift: {
    drift: { label: "派生漂移", tone: "bad" },
    mapping_gap: { label: "映射缺口", tone: "" },
    missing_in_queue: { label: "队列缺项", tone: "" },
    orphan_in_queue: { label: "孤立条目", tone: "warn" },
  },
  // 健康快照
  health: {
    pass: { label: "通过", tone: "ok" },
    rework_required: { label: "需返工", tone: "bad" },
    partial: { label: "部分", tone: "warn" },
  },
};

export function resolveStatus(group, value) {
  const table = statusDictionary[group] || {};
  return table[value] || { label: String(value ?? "—"), tone: "" };
}
