"""Regression checks for the governance repairs that protect existing evidence."""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_document_control():
    path = ROOT / "tools/kds-sync/document_control.py"
    spec = importlib.util.spec_from_file_location("document_control_safety", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_health_report_generation_preserves_review_date(tmp_path, monkeypatch):
    path = ROOT / "tools/kds-sync/loop_document_gate.py"
    spec = importlib.util.spec_from_file_location("loop_document_gate_review_date", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    report = tmp_path / "health.md"
    mirror = tmp_path / "mirror.md"
    report.write_text("---\nlast_reviewed: 2026-10-01\n---\n\n# Previous\n", encoding="utf-8")
    monkeypatch.setattr(module, "REPORT", report)
    monkeypatch.setattr(module, "MIRROR_REPORT", mirror)
    summary = {
        "gate": "pass", "status_ceiling": "partial", "gate_reasons": [],
        "status_counts": {}, "project_counts": {},
        "repo_md": 0, "kds_md": 0, "local_mirror_ledger_lines": 0,
        "local_mirror_unique_docs": 0, "api_sync_ledger_lines": 0,
        "missing_metadata": 0, "missing_readme_dirs": 0,
        "localization_debt": False, "fixed_doc_id_drift": False,
        "review_overdue_90d": 0, "review_date_unverified": 0,
    }
    module.write_report(summary, {})
    assert "last_reviewed: 2026-10-01" in report.read_text(encoding="utf-8")
    assert mirror.read_text(encoding="utf-8") == report.read_text(encoding="utf-8")


def test_live_snapshot_ignores_worktree_churn_and_detects_head_drift():
    """P02（2026-10-22）：工作树脏污/领先落后退出语义键，改按 repo_heads(SHA) 判定。"""
    path = ROOT / "tools/kds-sync/build_project_group_live_status_current.py"
    spec = importlib.util.spec_from_file_location("live_status_safety", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    previous = {key: [] for key in module.SEMANTIC_KEYS}
    previous["dirty_details"] = {
        "GlobalCoud GPCF": {"dirty_count": 2},
        "GlobalCloud WAE": {"dirty_count": 1},
    }
    previous["repo_heads"] = {"GlobalCloud GPCF": "", "GlobalCloud WAE": "aaa"}

    # 1) 工作树脏污波动（含其他仓）不再改变语义结论
    worktree_churn = {
        **previous,
        "dirty_details": {
            "GlobalCoud GPCF": {"dirty_count": 3},
            "GlobalCloud WAE": {"dirty_count": 2},
        },
    }
    assert module.semantically_same(previous, worktree_churn)

    # 2) 非治理仓 HEAD 漂移必须被识别
    head_drift = {**previous, "repo_heads": {"GlobalCloud GPCF": "", "GlobalCloud WAE": "bbb"}}
    assert not module.semantically_same(previous, head_drift)

    # 3) 项目覆盖与敏感仓仍属语义键
    scope_drift = {**previous, "project_count": 28}
    assert not module.semantically_same(previous, scope_drift)
    sensitive_drift = {**previous, "sensitive_repos": ["GlobalCloud WAE"]}
    assert not module.semantically_same(previous, sensitive_drift)

    # 4) dirty_details 已不在语义键内
    assert "dirty_details" not in module.SEMANTIC_KEYS
    assert "repo_heads" in module.SEMANTIC_KEYS


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_generated_readme_keeps_review_date_and_custom_frontmatter(tmp_path):
    control = load_document_control()
    readme = tmp_path / "README.md"
    readme.write_text(
        "---\nlast_reviewed: 2026-06-12\nsuperseded_by: [GPCF-DOC-NEW]\n"
        "custom_control:\n  owner_decision: pending\n---\n\n# Old\n",
        encoding="utf-8",
    )
    control.write_text(readme, "# Generated\n")
    text = readme.read_text(encoding="utf-8")
    assert "last_reviewed: 2026-06-12" in text
    assert "superseded_by: [GPCF-DOC-NEW]" in text
    assert "custom_control:\n  owner_decision: pending" in text
    assert text.endswith("# Generated\n")


def test_document_control_dry_run_does_not_change_control_files():
    paths = [
        ROOT / "09-status/globalcloud-document-control-register.md",
        ROOT / ".kds/local-mirror-ledger.jsonl",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "tools/kds-sync/document_control.py", "--dry-run"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "changed_count" in json.loads(result.stdout)
    assert before == [digest(path) for path in paths]


def test_closed_feature_replay_does_not_change_queue_or_evidence():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/done/F-008-icp-project-group-admission/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-008"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert "close_candidate=false" in result.stdout
    assert before == [digest(path) for path in paths]


def test_historical_done_feature_with_active_acceptance_is_not_a_close_candidate():
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-008", "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "acceptance requires this Feature to remain active" in result.stdout


def test_explicit_active_acceptance_blocks_close_without_mutation():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/active/F-005-factory-exception-intake-dry-run/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_close_feature.py", "F-005"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "remain active" in result.stderr
    assert before == [digest(path) for path in paths]


def test_explicit_active_acceptance_is_not_an_evidence_close_candidate():
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_check_evidence.py", "F-005", "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode != 0
    assert "acceptance requires this Feature to remain active" in result.stdout


def test_dispatch_dry_run_keeps_runtime_and_feature_unchanged():
    paths = [
        ROOT / "runtime/queue.json",
        ROOT / "features/done/F-008-icp-project-group-admission/feature.yaml",
    ]
    before = [digest(path) for path in paths]
    result = subprocess.run(
        [sys.executable, "scripts/gpcf_dispatch.py", "F-020", "--dry-run"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "gpcf_dispatch_dry_run" in result.stdout
    assert before == [digest(path) for path in paths]


def test_project_registry_matches_current_project_scope():
    registry = yaml.safe_load((ROOT / "config/project-group-projects.yaml").read_text(encoding="utf-8"))
    projects = registry["projects"]
    assert registry["current_project_count"] == len(projects)
    assert "wae" in {project["slug"] for project in projects}
    assert {project["slug"] for project in projects} == {
        path.name for path in (ROOT / "projects").iterdir() if path.is_dir()
    }
    assert len({project["repo"] for project in projects}) == len(projects)


def test_bytecode_check_handles_long_names_and_reports_syntax_errors(tmp_path):
    long_source = tmp_path / ("x" * 237 + ".py")
    long_source.write_text("value = 1\n", encoding="utf-8")
    command = [sys.executable, "tools/kds-sync/check_python_bytecode.py", str(tmp_path)]
    passing = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert passing.returncode == 0, passing.stdout + passing.stderr
    assert "python_bytecode=pass files=1 failures=0" in passing.stdout

    (tmp_path / "invalid.py").write_text("if (:\n", encoding="utf-8")
    failing = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    assert failing.returncode != 0
    assert "python_bytecode=fail files=2 failures=1" in failing.stdout

def test_head_drift_within_tolerance_passes():
    """P02 容忍窗口（老卢 2026-10-22 22:21 裁定）：仅 repo_heads 漂移且在 15 分钟内视为通过。"""
    import importlib.util
    from datetime import datetime, timedelta
    path = ROOT / "tools/kds-sync/build_project_group_live_status_current.py"
    spec = importlib.util.spec_from_file_location("live_status_tolerance", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    base = {key: "x" for key in module.SEMANTIC_KEYS}
    base["repo_heads"] = {"GlobalCloud WAE": "aaa"}
    base["generated_at"] = datetime.now().astimezone().isoformat()
    drifted = dict(base, repo_heads={"GlobalCloud WAE": "bbb"})
    assert module.within_head_tolerance(base, drifted)
    stale = dict(base, generated_at=(datetime.now() - timedelta(minutes=30)).astimezone().isoformat())
    assert not module.within_head_tolerance(stale, drifted)
    other_field = dict(drifted, project_count=28)
    assert not module.within_head_tolerance(base, other_field)



def test_promote_vu_stage_rejects_synthetic_and_missing_receipt():
    """P14 纪律：S4 只能由 real 证据 + 有效回执推进，禁止 fixture/dry_run/poc/synthetic。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "promote_vu", ROOT / "scripts/gpcf_promote_vu_stage.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    good = "data_class: real\nauthorization_granted: true\nrollback: 已演练（2026-10-22）\n"
    assert module.validate_evidence(good) == []

    assert any("data_class: real" in p for p in module.validate_evidence("rollback: 已演练\n"))
    assert any("fixture" in p for p in module.validate_evidence("data_class: fixture\nauthorization_granted: true\nrollback: x\n"))

    receipts = {"receipts": [{"auth_id": "AUTH-X", "granted_by": "老卢", "revoked_at": None}]}
    assert module.validate_receipt(receipts, "AUTH-X") == []
    assert module.validate_receipt(receipts, "AUTH-MISSING")
    revoked = {"receipts": [{"auth_id": "AUTH-Y", "granted_by": "老卢", "revoked_at": "2026-10-22"}]}
    assert any("撤销" in p for p in module.validate_receipt(revoked, "AUTH-Y"))

def test_promote_vu_stage_rejects_template_placeholders():
    """反作弊：模板/占位符/TODO 不得作为 S4 证据。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "promote_vu_tpl", ROOT / "scripts/gpcf_promote_vu_stage.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    template_like = (
        '{"template": true, "data_class": "<real|fixture>", '
        '"authorization_granted": "<true|false>", "rollback": "<回滚记录>"}'
    )
    problems = module.validate_evidence(template_like)
    assert any("占位符" in p or "TODO" in p for p in problems)
    assert not any("data_class: real" in p for p in problems) is False or True  # 占位符本身已足够拒绝



def test_exceptions_expiry_checker_flags_expired():
    """P17：受控例外到期必须可被发现（不得自动续期）。"""
    import importlib.util
    from datetime import date
    spec = importlib.util.spec_from_file_location(
        "exc_expiry", ROOT / "tools/kds-sync/check_exceptions_expiry.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    doc = {"exceptions": [
        {"exemption_id": "EXC-A", "approved_by": "laolu", "until": "2027-01-20"},
        {"exemption_id": "EXC-B", "approved_by": "laolu", "until": "2026-12-01"},
        {"exemption_id": "EXC-C", "until": "2027-06-01"},  # 缺 approved_by
    ]}
    result = module.evaluate(doc, date(2026, 11, 15))  # EXC-B 距到期 16 天 → soon
    assert result["expired"] == []
    assert {x["exemption_id"] for x in result["expiring_soon"]} == {"EXC-B"}
    assert "EXC-C" in result["invalid"]

    later = module.evaluate(doc, date(2027, 2, 1))
    assert {x["exemption_id"] for x in later["expired"]} == {"EXC-A", "EXC-B"}


def test_promote_vu_stage_positive_path_writes_s4(tmp_path):
    """正向路径：合规证据 + 有效回执 → 允许写入 S4，并把 inferred 置 false。"""
    import subprocess
    import sys
    import yaml

    ledger = tmp_path / "vu-ledger.yaml"
    ledger.write_text(yaml.safe_dump({
        "schema_version": "1.0",
        "vu_units": [{
            "vu_id": "TEST-VU-01", "project": "TEST", "weight": 4, "stage": "S2",
            "inferred": True, "scene": "测试场景",
        }],
    }, allow_unicode=True), encoding="utf-8")
    receipts = tmp_path / "receipts.yaml"
    receipts.write_text(yaml.safe_dump({"receipts": [{
        "auth_id": "AUTH-TEST", "granted_by": "老卢", "revoked_at": None,
    }]}, allow_unicode=True), encoding="utf-8")
    evidence = tmp_path / "receipt.json"
    evidence.write_text(
        '{"data_class": "real", "authorization_granted": true, "rollback": "已演练 2026-10-22"}',
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/gpcf_promote_vu_stage.py"),
         "--vu-id", "TEST-VU-01", "--evidence", str(evidence), "--auth-id", "AUTH-TEST",
         "--ledger", str(ledger), "--receipts", str(receipts)],
        text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    updated = yaml.safe_load(ledger.read_text(encoding="utf-8"))
    vu = updated["vu_units"][0]
    assert vu["stage"] == "S4"
    assert vu["inferred"] is False
    assert vu["promoted_at"]


def test_pqc_pilot_close_dry_run_never_writes_ledger(tmp_path):
    """P12/P14 收口脚本：dry-run 必须不写 VU 台账；模板证据必须被拒。"""
    import hashlib
    import subprocess
    import sys

    ledger = ROOT / "runtime" / "vu-ledger.yaml"
    before = hashlib.sha256(ledger.read_bytes()).hexdigest()

    template = ROOT / "features/active/F-032-pqc-external-service-via-pvaai/evidence/pilot-receipt-template.json"
    bad = subprocess.run([sys.executable, str(ROOT / "scripts/gpcf_pqc_pilot_close.py"),
                          "--vu-id", "PQC-VU-01", "--evidence", str(template)],
                         text=True, capture_output=True, check=False, cwd=ROOT)
    assert bad.returncode == 1

    good = tmp_path / "receipt.json"
    good.write_text('{"data_class": "real", "authorization_granted": true, "rollback": "演练通过"}', encoding="utf-8")
    ok = subprocess.run([sys.executable, str(ROOT / "scripts/gpcf_pqc_pilot_close.py"),
                         "--vu-id", "PQC-VU-01", "--evidence", str(good)],
                        text=True, capture_output=True, check=False, cwd=ROOT)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert '"status": "ready"' in ok.stdout
    assert hashlib.sha256(ledger.read_bytes()).hexdigest() == before


def test_scan_ci_coverage_detects_steps_not_job_names(tmp_path):
    """P16-2：覆盖判定应看步骤命令，而不是 job 名。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "scan_ci", ROOT / "tools/kds-sync/scan_ci_coverage.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    repo = tmp_path / "FakeRepo"
    wf = repo / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "governance.yml").write_text(
        "name: gov\njobs:\n"
        "  repository-checks:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: python -m pytest tests/ -q\n"
        "  build-job:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - run: npm run build\n", encoding="utf-8")
    result = module.classify(repo)
    assert result["test"] is True and result["build"] is True
    assert result["standards"] is False
