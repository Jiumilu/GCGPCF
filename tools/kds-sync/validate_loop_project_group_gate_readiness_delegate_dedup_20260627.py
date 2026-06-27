#!/usr/bin/env python3
"""Validate project-group readiness does not rerun duplicate delegated gates."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools/kds-sync/validate_loop_project_group_gate_readiness.py"


def load_module():
    spec = importlib.util.spec_from_file_location("readiness", SCRIPT)
    if spec is None or spec.loader is None:
        raise SystemExit("FAIL: cannot load readiness script")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_gate(path: Path, counter: Path) -> None:
    gate = path / "tools/kds-sync/loop_document_gate.py"
    gate.parent.mkdir(parents=True, exist_ok=True)
    gate.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python3",
                "\"\"\"Delegate project-group loop gate execution to the GPCF canonical gate.\"\"\"",
                "from pathlib import Path",
                "import json",
                f"counter = Path({str(counter)!r})",
                "current = int(counter.read_text(encoding='utf-8')) if counter.exists() else 0",
                "counter.write_text(str(current + 1), encoding='utf-8')",
                "print(json.dumps({'gate': 'pass', 'gate_reasons': []}))",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    gate.chmod(0o755)


def main() -> int:
    module = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        counter = base / "counter.txt"
        repo_a = base / "Repo A"
        repo_b = base / "Repo B"
        write_gate(repo_a, counter)
        write_gate(repo_b, counter)

        original_repos = module.REPOS
        try:
            module.REPOS = [("Repo A", repo_a), ("Repo B", repo_b)]
            rc = module.main()
        finally:
            module.REPOS = original_repos

        calls = int(counter.read_text(encoding="utf-8")) if counter.exists() else 0
        if rc != 0:
            print(f"loop_project_group_gate_readiness_delegate_dedup_20260627=fail rc={rc}")
            return 1
        if calls != 1:
            print(
                "loop_project_group_gate_readiness_delegate_dedup_20260627=fail "
                f"expected_calls=1 actual_calls={calls}"
            )
            return 1

    print("loop_project_group_gate_readiness_delegate_dedup_20260627=pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
