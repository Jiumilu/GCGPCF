#!/usr/bin/env python3
"""Export a read-only JSON snapshot of the GPCF control repo for the console UI.

Stage 1 of the v3 design ("one page, four drill-downs"). The exporter only
reads the repo; it never writes features/**, runtime/queue.json or
projects/*/STATUS.md. Output goes to console/public/data/*.json.

Truth chain (see runtime/status-source-of-truth.yaml):
  feature.yaml is the only writable source; queue.json / STATUS.md are
  derived views. Any mismatch is reported as drift instead of being fixed.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

from gpcf_feature_lib import ACTIVE, DONE, QUEUE_FILE, ROOT, STATE_FILE

DATA_DIR = ROOT / "console/public/data"
CONFIG_FILE = ROOT / "config/project-group-projects.yaml"
HEALTH_REPORT = ROOT / "09-status/globalcloud-document-health-report.md"
DOC_REGISTER = ROOT / "09-status/globalcloud-document-control-register.md"
TRUTH_SOURCE_FILE = ROOT / "runtime/status-source-of-truth.yaml"
ROADMAP_FILE = ROOT / "projects/gpcf/ROADMAP.md"
LOGS_DIR = ROOT / "runtime/logs"
FEATURE_ID_RE = re.compile(r"^(F-\d{3})")
SKIP_PARTS = {".git", ".kds", ".zcode", "node_modules", "dist", "tmp", ".pytest_cache", "__pycache__"}

# Mirrors runtime/status-source-of-truth.yaml. Kept local on purpose: the
# exporter must not import a gate that could write the derived views.
STEP_TO_QUEUE_STATUS = {
    "plan": "plan",
    "implement": "implement",
    "evaluate": "evaluated",
    "repair": "repair",
    "commit": "commit",
}
ROLE_BY_STEP = {
    "plan": "Planner",
    "implement": "Builder",
    "evaluate": "Evaluator",
    "repair": "Repair",
    "commit": "Recorder",
}
INITIAL_QUEUE_STATUS = "queued"
INITIAL_ROLE = "Dispatcher"

GATES = [
    {
        "id": "document",
        "name": "文档门禁",
        "scope": "Markdown 元数据 / KDS 镜像",
        "command": "python3 tools/kds-sync/loop_document_gate.py --check-only",
        "script": "tools/kds-sync/loop_document_gate.py",
    },
    {
        "id": "pollution",
        "name": "污染检查",
        "scope": "旧命名、旧口径回流",
        "command": "python3 tools/kds-sync/check_document_pollution.py",
        "script": "tools/kds-sync/check_document_pollution.py",
    },
    {
        "id": "kds_token",
        "name": "KDS TOKEN",
        "scope": "镜像写入鉴权",
        "command": "python3 tools/kds-sync/validate_kds_token.py",
        "script": "tools/kds-sync/validate_kds_token.py",
    },
    {
        "id": "workspace",
        "name": "工作区校验",
        "scope": "Feature 结构与命名",
        "command": "python3 tools/kds-sync/validate_gpcf_2_feature_workspace.py",
        "script": "tools/kds-sync/validate_gpcf_2_feature_workspace.py",
    },
    {
        "id": "contract",
        "name": "契约矩阵",
        "scope": "跨项目契约一致性",
        "command": "python3 tools/kds-sync/validate_contract_matrix.py",
        "script": "tools/kds-sync/validate_contract_matrix.py",
    },
    {
        "id": "evidence",
        "name": "证据门禁",
        "scope": "证据五件套完整性",
        "command": "python3 scripts/gpcf_check_evidence.py <F>",
        "script": "scripts/gpcf_check_evidence.py",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"not a mapping: {rel(path)}")
    return data


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"not an object: {rel(path)}")
    return data


def git(*args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value or None


def load_projects() -> list[dict[str, Any]]:
    data = read_yaml(CONFIG_FILE)
    items = []
    for entry in data.get("projects") or []:
        if not isinstance(entry, dict):
            continue
        items.append(
            {
                "slug": str(entry.get("slug") or "").strip(),
                "id": str(entry.get("id") or "").strip(),
                "repo": str(entry.get("repo") or "").strip(),
            }
        )
    return sorted(items, key=lambda item: item["slug"])


def load_features(project_slugs: set[str]) -> list[dict[str, Any]]:
    features: list[dict[str, Any]] = []
    for folder in (ACTIVE, DONE):
        if not folder.is_dir():
            continue
        for workspace in sorted(folder.iterdir()):
            if not workspace.is_dir():
                continue
            match = FEATURE_ID_RE.match(workspace.name)
            feature_file = workspace / "feature.yaml"
            if not match or not feature_file.is_file():
                continue
            data = read_yaml(feature_file)
            loop = data.get("loop") or {}
            evidence = data.get("evidence") or {}
            ui = data.get("ui_product_first_control") or {}
            gates = ui.get("gates") or {}
            blockers = [str(item) for item in (data.get("blockers") or [])]
            features.append(
                {
                    "id": match.group(1),
                    "name": str(data.get("name") or "").strip(),
                    "project": str(data.get("project") or "").strip(),
                    "project_retired": str(data.get("project") or "") not in project_slugs,
                    "priority": str(data.get("priority") or "").strip(),
                    "status": str(data.get("status") or "").strip(),
                    "owner": str(data.get("owner") or "").strip(),
                    "goal": str(data.get("goal") or "").strip(),
                    "step": str(loop.get("current_step") or "").strip(),
                    "iteration": int(loop.get("iteration") or 0),
                    "workspace": rel(workspace),
                    "acceptance_count": len(data.get("acceptance") or []),
                    "scope_in_count": len((data.get("scope") or {}).get("in") or []),
                    "evidence": {
                        key: str(evidence.get(key) or "").strip()
                        for key in ("tests", "build", "api", "screenshots", "summary")
                    },
                    "gates": {
                        key: str(gates.get(key) or "").strip()
                        for key in (
                            "functional_completeness",
                            "quality_baseline",
                            "multi_user_usability",
                            "task_flow_e2e_status",
                            "accessibility_status",
                            "evidence_overexposure_gate",
                        )
                    },
                    "status_ceiling": str(ui.get("status_ceiling") or "").strip(),
                    "review_status": data.get("review_status") or None,
                    "blockers": blockers,
                    "blocker_count": len(blockers),
                    "updated_at": data.get("updated_at") or None,
                }
            )
    return sorted(features, key=lambda item: item["id"])


def expected_queue_status(feature: dict[str, Any]) -> str:
    if feature["status"] == "done":
        return "closed"
    if feature["status"] == "blocked":
        return "blocked"
    return STEP_TO_QUEUE_STATUS.get(feature["step"], "")


def classify_drift(
    features: list[dict[str, Any]], queue: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    """Compare derived queue entries against the feature.yaml truth.

    kind:
      drift            truth and derived view disagree on a mapped field
      mapping_gap      queue holds the initial state, which the mapping does
                       not define (status "queued" / role "Dispatcher")
      missing_in_queue workspace exists without a queue entry
      orphan_in_queue  queue entry without a workspace
    """
    by_id = {item["id"]: item for item in features}
    drifts: list[dict[str, Any]] = []
    for feature in features:
        fid = feature["id"]
        entry = queue.get(fid)
        if entry is None:
            drifts.append(
                {
                    "feature": fid,
                    "kind": "missing_in_queue",
                    "field": "queue.entry",
                    "truth": "workspace exists",
                    "derived": "absent",
                }
            )
            continue
        expected_status = expected_queue_status(feature)
        actual_status = str(entry.get("status") or "").strip()
        if expected_status and actual_status != expected_status:
            initial = feature["step"] == "plan" and actual_status == INITIAL_QUEUE_STATUS
            kind = "mapping_gap" if initial else "drift"
            drifts.append(
                {
                    "feature": fid,
                    "kind": kind,
                    "field": "queue.status",
                    "truth": expected_status,
                    "derived": actual_status,
                }
            )
        expected_role = (
            "Recorder" if feature["status"] == "done" else ROLE_BY_STEP.get(feature["step"], "")
        )
        actual_role = str(entry.get("current_role") or "").strip()
        if expected_role and actual_role != expected_role:
            initial = feature["step"] == "plan" and actual_role == INITIAL_ROLE
            kind = "mapping_gap" if initial else "drift"
            drifts.append(
                {
                    "feature": fid,
                    "kind": kind,
                    "field": "queue.current_role",
                    "truth": expected_role,
                    "derived": actual_role,
                }
            )
        for field in ("project", "priority"):
            truth = str(feature[field])
            derived = str(entry.get(field) or "").strip()
            if derived and derived != truth:
                drifts.append(
                    {
                        "feature": fid,
                        "kind": "drift",
                        "field": f"queue.{field}",
                        "truth": truth,
                        "derived": derived,
                    }
                )
    for fid in sorted(queue):
        if fid in by_id:
            continue
        drifts.append(
            {
                "feature": fid,
                "kind": "orphan_in_queue",
                "field": "feature.workspace",
                "truth": "absent",
                "derived": "queue entry",
            }
        )
    return sorted(drifts, key=lambda item: (item["feature"], item["field"]))


def build_projects(
    projects: list[dict[str, Any]], features: list[dict[str, Any]]
) -> dict[str, Any]:
    counts: dict[str, int] = {}
    total: dict[str, int] = {}
    for feature in features:
        slug = feature["project"]
        total[slug] = total.get(slug, 0) + 1
        if feature["status"] != "done":
            counts[slug] = counts.get(slug, 0) + 1
    items = []
    for project in projects:
        slug = project["slug"]
        items.append(
            {
                **project,
                "active_features": counts.get(slug, 0),
                "total_features": total.get(slug, 0),
                "has_status": (ROOT / "projects" / slug / "STATUS.md").is_file(),
                "has_roadmap": (ROOT / "projects" / slug / "ROADMAP.md").is_file(),
                "has_risk": (ROOT / "projects" / slug / "RISK.md").is_file(),
            }
        )
    known = {project["slug"] for project in projects}
    retired = sorted({slug for slug in total if slug not in known})
    return {"count": len(items), "items": items, "unregistered_attribution": retired}


def parse_health() -> dict[str, Any]:
    if not HEALTH_REPORT.is_file():
        return {}
    text = HEALTH_REPORT.read_text(encoding="utf-8")
    result: dict[str, Any] = {}

    def grab(pattern: str) -> str | None:
        match = re.search(pattern, text)
        return match.group(1).strip() if match else None

    generated = grab(r"生成时间：(\S+)")
    if generated:
        result["generated_at"] = generated
    gate = grab(r"Loop 文档门禁：`([^`]+)`")
    if gate:
        result["loop_gate"] = gate
    for key, pattern in (
        ("repo_markdown", r"- 仓库 Markdown：\s*([\d,]+)"),
        ("metadata_missing", r"- 元数据缺失：\s*([\d,]+)"),
        ("readme_missing_dirs", r"- README 缺失目录：\s*([\d,]+)"),
        ("review_overdue_90d", r"受控文档复核逾期（>90 天）：\s*([\d,]+)"),
        ("status_ceiling", r"- 治理状态上限：\s*(\S+)"),
    ):
        value = grab(pattern)
        if value:
            result[key] = value
    status_counts: dict[str, int] = {}
    for match in re.finditer(r"^- (archive|controlled|draft|okf_derived): (\d+)$", text, re.M):
        status_counts[match.group(1)] = int(match.group(2))
    if status_counts:
        result["status_counts"] = status_counts
    return result


def count_repo_markdown() -> int:
    total = 0
    for path in ROOT.rglob("*.md"):
        if SKIP_PARTS & set(path.parts):
            continue
        total += 1
    return total


def count_registered_docs() -> int:
    if not DOC_REGISTER.is_file():
        return 0
    text = DOC_REGISTER.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if line.startswith("| GPCF-DOC"))


def parse_roadmap() -> dict[str, Any]:
    if not ROADMAP_FILE.is_file():
        return {"source": rel(ROADMAP_FILE), "items": []}
    items = []
    for line in ROADMAP_FILE.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^- Phase (\d+)：(.+)$", line.strip())
        if match:
            items.append({"phase": int(match.group(1)), "text": match.group(2).strip("。 ")})
    return {"source": rel(ROADMAP_FILE), "items": sorted(items, key=lambda item: item["phase"])}


def load_loops() -> dict[str, Any]:
    """Role transitions recorded by gpcf_dispatch.py in runtime/logs/F-*.jsonl."""
    items: list[dict[str, Any]] = []
    if LOGS_DIR.is_dir():
        for path in sorted(LOGS_DIR.glob("F-*.jsonl")):
            fallback = path.stem
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(row, dict):
                    continue
                items.append(
                    {
                        "feature": str(row.get("feature_id") or fallback),
                        "role": str(row.get("role") or ""),
                        "status": str(row.get("status") or ""),
                        "at": row.get("timestamp"),
                        "input": str(row.get("input") or ""),
                        "output": str(row.get("output") or ""),
                        "evidence": str(row.get("evidence") or ""),
                    }
                )
    items.sort(key=lambda item: (str(item["at"] or ""), item["feature"], item["role"]))
    by_role: dict[str, int] = {}
    for item in items:
        by_role[item["role"]] = by_role.get(item["role"], 0) + 1
    return {
        "count": len(items),
        "features": len({item["feature"] for item in items}),
        "by_role": dict(sorted(by_role.items())),
        "items": items,
    }


def build_gates(health: dict[str, Any]) -> dict[str, Any]:
    items = []
    for gate in GATES:
        script = ROOT / gate["script"]
        items.append(
            {
                **gate,
                "script_exists": script.is_file(),
                "last_result": health.get("loop_gate") if gate["id"] == "document" else None,
            }
        )
    return {
        "count": len(items),
        "items": items,
        "last_result_source": rel(HEALTH_REPORT) if health else None,
    }


def build_docs(health: dict[str, Any]) -> dict[str, Any]:
    return {
        "repo_markdown": count_repo_markdown(),
        "registered_docs": count_registered_docs(),
        "health": health,
        "sources": [rel(DOC_REGISTER), rel(HEALTH_REPORT)],
    }


def build_meta(
    features: list[dict[str, Any]],
    projects: dict[str, Any],
    queue: list[dict[str, Any]],
    state: dict[str, Any],
    drifts: list[dict[str, Any]],
    generated_at: str,
    roadmap: dict[str, Any],
) -> dict[str, Any]:
    kinds: dict[str, int] = {}
    for item in drifts:
        kinds[item["kind"]] = kinds.get(item["kind"], 0) + 1
    true_drift = sorted({i["feature"] for i in drifts if i["kind"] == "drift"})
    gaps = sorted({i["feature"] for i in drifts if i["kind"] == "mapping_gap"})
    active = [f for f in features if f["status"] != "done"]
    return {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "source_sha": git("rev-parse", "HEAD"),
        "source_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "repo": "GlobalCloud GPCF",
        "counts": {
            "projects": projects["count"],
            "features": len(features),
            "active": len(active),
            "done": len(features) - len(active),
            "queue": len(queue),
            "blockers": sum(f["blocker_count"] for f in active),
            "features_with_blockers": sum(1 for f in active if f["blocker_count"]),
        },
        "runtime": {
            "current_feature": state.get("current_feature"),
            "queue_length": state.get("queue_length"),
            "active_feature_count": state.get("active_feature_count"),
            "mode": state.get("mode"),
        },
        "drift": {
            "total": len(drifts),
            "distinct_features": len({i["feature"] for i in drifts}),
            "by_kind": kinds,
            "true_drift_features": true_drift,
            "mapping_gap_features": gaps,
            "items": drifts,
            "policy": "以 feature.yaml 为准；派生视图不一致时阻断，禁止人工改派生侧对齐",
        },
        "roadmap": roadmap,
        "truth_source": {
            "feature": "features/{active|done}/F-*/feature.yaml",
            "mapping": rel(TRUTH_SOURCE_FILE),
        },
        "non_claims": [
            "只读快照，不代表业务实现完成或客户交付",
            "不声明 accepted / integrated / production_ready",
        ],
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def export(out_dir: Path) -> dict[str, Any]:
    generated_at = now()
    projects = load_projects()
    slugs = {project["slug"] for project in projects}
    features = load_features(slugs)
    queue_payload = read_json(QUEUE_FILE) if QUEUE_FILE.is_file() else {}
    state = read_json(STATE_FILE) if STATE_FILE.is_file() else {}
    queue_items = [
        entry for entry in (queue_payload.get("queue") or []) if isinstance(entry, dict)
    ]
    queue_by_id = {str(entry.get("id") or ""): entry for entry in queue_items}
    drifts = classify_drift(features, queue_by_id)
    drift_by_feature: dict[str, list[dict[str, Any]]] = {}
    for item in drifts:
        drift_by_feature.setdefault(item["feature"], []).append(item)
    for feature in features:
        feature["drift"] = drift_by_feature.get(feature["id"], [])
        entry = queue_by_id.get(feature["id"]) or {}
        feature["derived_queue"] = (
            {
                "status": str(entry.get("status") or ""),
                "current_role": str(entry.get("current_role") or ""),
                "updated_at": entry.get("updated_at"),
            }
            if entry
            else None
        )
    health = parse_health()
    project_payload = build_projects(projects, features)
    meta = build_meta(
        features, project_payload, queue_items, state, drifts, generated_at, parse_roadmap()
    )

    write_json(out_dir / "features.json", {"items": features, "count": len(features)})
    write_json(out_dir / "projects.json", project_payload)
    write_json(out_dir / "gates.json", build_gates(health))
    write_json(out_dir / "docs.json", build_docs(health))
    write_json(out_dir / "loops.json", load_loops())
    write_json(out_dir / "meta.json", meta)
    return meta


FILES = ("features.json", "projects.json", "gates.json", "docs.json", "loops.json", "meta.json")


def compare_snapshots(fresh_dir: Path, current_dir: Path) -> list[dict[str, str]]:
    report: list[dict[str, str]] = []
    for name in FILES:
        current = current_dir / name
        if not current.is_file():
            report.append({"file": name, "state": "missing"})
            continue
        left = json.loads((fresh_dir / name).read_text(encoding="utf-8"))
        right = json.loads(current.read_text(encoding="utf-8"))
        if name == "meta.json":
            # 身份字段随提交变化（生成时间、生成时的 HEAD），不参与一致性判断
            for field in ("generated_at", "source_sha"):
                left.pop(field, None)
                right.pop(field, None)
        report.append({"file": name, "state": "ok" if left == right else "stale"})
    return report


def check_snapshot(out_dir: Path, quiet: bool) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        export(Path(tmp))
        report = compare_snapshots(Path(tmp), out_dir)
    stale = [item for item in report if item["state"] != "ok"]
    if not quiet:
        for item in report:
            print(f"console_export: {item['file']}: {item['state']}")
    reasons = ", ".join(f"{item['file']}={item['state']}" for item in stale) or "in sync"
    print(f"console_export: check={'pass' if not stale else 'stale'} ({reasons})")
    return 0 if not stale else 1


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export read-only GPCF console data")
    parser.add_argument("--out", type=Path, default=DATA_DIR, help="output directory")
    parser.add_argument("--quiet", action="store_true", help="print nothing on success")
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare the existing snapshot with a fresh export (ignores generated_at/source_sha); exit 1 when stale",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)
    out_dir = args.out if args.out.is_absolute() else ROOT / args.out
    if args.check:
        try:
            return check_snapshot(out_dir, args.quiet)
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL: console check: {exc}", file=sys.stderr)
            return 1
    try:
        meta = export(out_dir)
    except Exception as exc:  # noqa: BLE001 - surface the failure and exit non-zero
        print(f"FAIL: console export: {exc}", file=sys.stderr)
        return 1
    if not args.quiet:
        counts = meta["counts"]
        drift = meta["drift"]
        print(
            "console_export: "
            f"projects={counts['projects']} features={counts['features']} "
            f"active={counts['active']} drift={drift['total']} "
            f"by_kind={json.dumps(drift['by_kind'], ensure_ascii=False, sort_keys=True)}"
        )
        print(f"console_export: wrote {rel(out_dir) if out_dir.is_relative_to(ROOT) else out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
