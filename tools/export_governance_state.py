#!/usr/bin/env python3
"""GPCF 治理状态导出 v0.1（M1·D1.1·2026-10-14）

对齐：《GPCF治理控制台_全量规划_v0.1》§四 D1 治理数据面；
按八视图组织数据源（概览/交付队列/项目群运转/主方案台账/三闭环/文档控制/规则与变更/门禁与证据）。

只读纪律：
- 不写任何治理数据（仅产物落 runtime/evidence/）；
- 解析失败如实记入 findings（不猜测、不补数）；
- 计数以磁盘实存为准；-1 表示"读取失败"（不是 0）。

用法：python3 tools/export_governance_state.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "runtime" / "evidence"

findings: list[dict] = []


def note(section: str, msg: str) -> None:
    findings.append({"section": section, "finding": msg,
                     "at": datetime.now(timezone.utc).isoformat()})


def count_files(d: Path, pattern: str = "*") -> int:
    try:
        return sum(1 for p in d.glob(pattern) if p.is_file())
    except Exception as e:
        note(str(d), f"计数失败：{e}")
        return -1


def count_files_recursive(d: Path) -> int:
    try:
        return sum(1 for p in d.rglob("*") if p.is_file())
    except Exception as e:
        note(str(d), f"递归计数失败：{e}")
        return -1


def list_dirs(d: Path) -> list[str]:
    try:
        return sorted(p.name for p in d.iterdir() if p.is_dir())
    except Exception as e:
        note(str(d), f"列举失败：{e}")
        return []


def list_files(d: Path, pattern: str = "*") -> list[str]:
    try:
        return sorted(p.name for p in d.glob(pattern) if p.is_file())
    except Exception as e:
        note(str(d), f"列举失败：{e}")
        return []


def read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        note(str(p.relative_to(ROOT)), f"JSON 解析失败：{e}")
        return None


def mtime(p: Path) -> str:
    try:
        return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()
    except Exception:
        return ""


def recent(d: Path, pattern: str, n: int = 5) -> list[dict]:
    try:
        files = [p for p in d.glob(pattern) if p.is_file()]
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return [{"name": p.name, "mtime": mtime(p)} for p in files[:n]]
    except Exception as e:
        note(str(d), f"最近文件读取失败：{e}")
        return []


def main() -> int:
    sections: dict = {}

    # ── 视图2 交付队列：runtime/queue.json + state.json ──
    q = read_json(ROOT / "runtime" / "queue.json")
    st = read_json(ROOT / "runtime" / "state.json")
    q_stats: dict = {}
    if isinstance(q, dict) and isinstance(q.get("queue"), list):
        by_status: dict[str, int] = {}
        for item in q["queue"]:
            s = str(item.get("status", "unknown"))
            by_status[s] = by_status.get(s, 0) + 1
        q_stats = {"queue_total": len(q["queue"]), "queue_by_status": by_status,
                   "schema_version": q.get("schema_version"),
                   "items": [
                       {"id": it.get("id"), "name": it.get("name"), "project": it.get("project"),
                        "priority": it.get("priority"), "status": it.get("status"),
                        "current_role": it.get("current_role"), "updated_at": it.get("updated_at")}
                       for it in q["queue"]
                   ]}
    elif q is not None:
        note("delivery", "queue.json 结构不符（无 queue 数组）——如实标注")
    sections["delivery"] = {
        "queue": q_stats,
        "state": {k: st.get(k) for k in
                  ("schema_version", "mode", "current_feature", "roles",
                   "active_feature_count", "queue_length", "updated_at")} if isinstance(st, dict) else {},
    }

    # ── 交付队列·features ──
    active = list_dirs(ROOT / "features" / "active")
    done = list_dirs(ROOT / "features" / "done")
    sections["features"] = {"active": active, "active_count": len(active),
                            "done_count": len(done), "done": done}

    # ── 视图5 三闭环：loops/ ──
    sections["loops"] = [{"name": f, "mtime": mtime(ROOT / "loops" / f)}
                         for f in list_files(ROOT / "loops", "*.md")]

    # ── 视图6 文档控制：09-status/ + KDS 同步 ──
    st_dir = ROOT / "09-status"
    sections["document_control"] = {
        "count": count_files(st_dir, "*.md"),
        "recent": recent(st_dir, "*.md"),
        "kds_sync_registers": list_files(st_dir, "kds-*"),
    }

    # ── 视图4 主方案台账 ──
    mp = ROOT / "09-status" / "globalcloud-project-master-plan-control-register.md"
    sections["master_plan_register"] = {"exists": mp.is_file(), "file": mp.name,
                                        "mtime": mtime(mp)}

    # ── 视图7 规则与变更：okf/ + openspec/ ──
    sections["policies"] = {
        "okf_count": count_files(ROOT / "okf", "*.yaml"),
        "okf_names": list_files(ROOT / "okf", "*.yaml"),
        "openspec_changes": len(list_dirs(ROOT / "openspec" / "changes")),
        "openspec_specs": len(list_dirs(ROOT / "openspec" / "specs")),
    }

    # ── 视图3 项目群运转：projects/ + registry + 05/06 ──
    proj_names = list_dirs(ROOT / "projects")
    sections["projects"] = {
        "count": len(proj_names),
        "names": proj_names,
        "files_per_project": {n: count_files_recursive(ROOT / "projects" / n) for n in proj_names},
        "state_matrix": (ROOT / "registry" / "project-state-matrix.yaml").is_file(),
        "agent_team_files": count_files(ROOT / "05-agent-team", "*.md"),
        "workstream_files": count_files(ROOT / "06-workstreams", "*.md"),
    }

    # ── 视图8 门禁与证据 ──
    sections["gates_evidence"] = {
        "acceptance_files": count_files(ROOT / "07-acceptance", "*.md"),
        "evidence_samples_files": count_files_recursive(ROOT / "08-evidence-samples"),
        "harness_evidence_files": count_files_recursive(ROOT / "docs" / "harness" / "evidence"),
        "governance_tool_scripts": count_files(ROOT / "tools" / "kds-sync", "*.py"),
    }

    out = {
        "schema": "gpcf-governance-state/0.1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "sourceRoot": str(ROOT),
        "views": "八视图（治理概览/交付队列/项目群运转/主方案台账/三闭环/文档控制/规则与变更/门禁与证据）",
        "sections": sections,
        "findings": findings,
        "ok": len(findings) == 0,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUT_DIR / f"governance-state-{datetime.now():%Y%m%d-%H%M}.json"
    outfile.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── stdout 摘要 ──
    d = sections["delivery"]
    print(f"[gpcf] governance state export → {outfile.relative_to(ROOT)}")
    print(f"[gpcf] queue={d['queue'].get('queue_total', '?')} "
          f"by_status={d['queue'].get('queue_by_status', {})}")
    print(f"[gpcf] state: mode={d['state'].get('mode')} current={d['state'].get('current_feature')} "
          f"roles={len(d['state'].get('roles', []))} active={d['state'].get('active_feature_count')}")
    print(f"[gpcf] features: active={sections['features']['active_count']} done={sections['features']['done_count']}")
    print(f"[gpcf] document_control={sections['document_control']['count']} "
          f"okf_policies={sections['policies']['okf_count']} "
          f"openspec_changes={sections['policies']['openspec_changes']}")
    print(f"[gpcf] projects={sections['projects']['count']} "
          f"agent_team={sections['projects']['agent_team_files']} "
          f"workstreams={sections['projects']['workstream_files']}")
    print(f"[gpcf] gates: acceptance={sections['gates_evidence']['acceptance_files']} "
          f"evidence_samples={sections['gates_evidence']['evidence_samples_files']} "
          f"harness_evidence={sections['gates_evidence']['harness_evidence_files']} "
          f"tool_scripts={sections['gates_evidence']['governance_tool_scripts']}")
    print(f"[gpcf] findings={len(findings)} ok={out['ok']}")
    for f in findings[:5]:
        print(f"  ! {f['section']}: {f['finding']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
