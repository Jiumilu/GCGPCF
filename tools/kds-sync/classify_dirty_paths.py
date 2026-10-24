#!/usr/bin/env python3
"""PG-04 自指 dirty 治理：项目群 28 仓未提交变更分类器（只读）。

目的
----
把「治理产物污染被审工作树」这件事量化成可复跑的分类基线：
对 `config/project-group-projects.yaml` 中的每个仓执行
    git --no-optional-locks -c core.quotePath=false -C <repo> status --porcelain -uall
解析每条 `XY path`（rename/copy 取 new），按 governance / product / noise /
sensitive / unknown 五类归档，并输出全局统计、逐仓表、按目录聚合的 Top N。

硬边界
----
* 只读：本脚本只执行 `git status` / `git rev-list`，不写任何文件、不建目录、
  不删除、不移动、不 stage/commit/push、不改权限。
* 只依赖 Python 3 标准库；无 PyYAML（config 用受限正则解析，格式漂移会显式报错）。
* 输出确定性：同一工作树状态下，`--json` 的 `digest` 与各类计数稳定不变
  （`generated_at` 与 `ahead/behind` 除外，见 --no-timestamp）。

用法
----
    python3 "GlobalCloud GPCF/tools/kds-sync/classify_dirty_paths.py"
    python3 .../classify_dirty_paths.py --markdown --top 20
    python3 .../classify_dirty_paths.py --json
    python3 .../classify_dirty_paths.py --only GPCF,XiaoC,KDS

退出码
------
    0 成功；2 config/仓路径缺失；3 有仓的 git status 失败（其余仓仍输出）。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys

import yaml
from collections import Counter, OrderedDict
from datetime import datetime
from pathlib import Path

TOOL_NAME = "classify_dirty_paths.py"
TOOL_VERSION = "v1.0"

ROOT = Path(__file__).resolve().parents[2]  # GlobalCloud GPCF 仓根
PROJECT_ROOT = ROOT.parent  # 项目群工作区根
DEFAULT_CONFIG = ROOT / "config/project-group-projects.yaml"

CATEGORIES = ("governance", "product", "noise", "sensitive", "unknown")

# 实际执行的命令模板（占位符 <repo> 为仓目录名）。
# `-c core.quotePath=false` 仅影响中文路径的显示（避免八进制转义），不改变变更集。
COMMAND_TEMPLATE = (
    "git --no-optional-locks -c core.quotePath=false -C <repo> "
    "status --porcelain -uall"
)
UPSTREAM_TEMPLATE = (
    "git --no-optional-locks -C <repo> rev-list --left-right --count "
    "@{upstream}...HEAD"
)

# ---------------------------------------------------------------------------
# 分类规则（可扩展；顺序即优先级，见 classify()）
# ---------------------------------------------------------------------------

# 1) sensitive：凭据/密钥类命名。优先级最高——先命中先归类，便于安全复核。
SENSITIVE_BASENAME_GLOBS = (
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.keystore",
    "id_rsa*",
    "id_ed25519*",
    ".netrc",
    ".npmrc",
)
SENSITIVE_NAME_TOKENS = ("secret", "token", "credential", "api_key", "apikey", "password")
# 命中 SENSTIVE_NAME_TOKENS 但属于下面扩展名的，视为「提到 token 的源码/文档」，
# 不归 sensitive（否则 build_*_token_*.py 这类治理脚本会被大面积误报）。
SENSITIVE_NAME_TOKEN_EXEMPT_EXTENSIONS = (
    ".py",
    ".pyi",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".sh",
    ".md",
    ".mdx",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".html",
    ".vue",
    ".sql",
)

# 2) noise：本机构建/编辑器/系统垃圾，非交付物。
NOISE_BASENAMES = (
    ".DS_Store",
    "Thumbs.db",
    ".coverage",
    ".eslintcache",
    ".stylelintcache",
    ".desktop_root_state.json",
)
# 文件名包含这些片段即视为备份/临时文件（如 `企业信息库.md.bak-2026-10-19`）
NOISE_NAME_INFIXES = (".bak", ".tmp.", ".orig.", ".rej.")
# 未展开环境变量的顶层目录（如字面量 `$CODEX_HOME/`）属本机配置误产物
NOISE_TOP_SEGMENT_PREFIXES = ("$",)
NOISE_DIR_SEGMENTS = (
    "__pycache__",
    "node_modules",
    ".turbo",
    ".scratch",
    ".venv",
    "venv",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    ".cache",
    ".next",
    ".nuxt",
    "dist-info",
    "egg-info",
)
NOISE_EXTENSIONS = (
    ".pyc",
    ".pyo",
    ".log",
    ".swp",
    ".swo",
    ".tmp",
    ".bak",
    ".orig",
    ".rej",
    ".pid",
)

# 3) governance：治理组织自身的产物（被审工作树里最不该被当成「未交付变更」的部分）。
#    前缀匹配（路径以该目录开头）。
GOVERNANCE_PREFIXES = (
    "features/",  # GPCF 2.0 Feature 工作区（feature.yaml / journal.md / evidence/ / artifacts/）
    ".harness/",  # harness run / evidence / logs
    ".kds/",  # KDS 本地镜像与账本
    ".okf/",  # OKF 知识资产生成物
    "docs/harness/",
    "runtime/",  # GPCF 2.0 运行态（queue.json / state.json / logs/）
    "09-status/",  # GPCF 状态台账
    "_meta/",
    "_governance/",  # KDS 治理目录（图健康等）
    ".codex/",
    ".agent-team/",
    "docs/evidence/",
    "docs/reports/",
    "docs/loops/",
    "docs/status/",
    "docs/ledger/",
    "evidence/",
    "artifacts/",
    "reports/",
    "loops/",
    "ledger/",
    "projects/",  # projects/<id>/ 为项目控制记录（STATUS/RISK/ROADMAP）
    "review/",  # 评审/红队/复核产物
    "99_Reports/",  # KDS 巡检/日报/健康报告
)
# 编号治理目录（01-architecture/、02-governance/、04-ui-delivery/ 之类）
GOVERNANCE_NUMERIC_DIR_RE = re.compile(
    r"^\d{2}-(?:ui-)?(?:architecture|governance|status|reports?|harness|evidence|delivery|planning)/"
)
# 任意层级出现这些目录段 → 治理产物（如 features/active/F-001/evidence/...）
GOVERNANCE_DIR_SEGMENTS = ("evidence", "artifacts", "_verify-reports")
# 治理台账类文件（glob，作用于完整相对路径）
GOVERNANCE_PATH_GLOBS = (
    "projects/*/STATUS.md",
    "projects/*/status.md",
    "*/STATUS.md",
    "*/status.md",
    "*.code-workspace",
)
# 仓根受控方案/台账文档（非机制产物，但属治理控制体系；需入库、不宜 ignore）
GOVERNANCE_ROOT_DOC_RE = re.compile(
    r"^(?P<name>[^/]*(?:总体方案|实施方案)[^/]*\.md|PROJECT_HARNESS_MANIFEST\.md|"
    r"AGENTS\.md|CLAUDE\.md|log\.md)$"
)
# governance 子桶：机械产物（可 ignore / 可移出被审面）vs 受控文档（应入库、需 review）
GOVERNANCE_MECHANICAL_PREFIXES = (
    # 注意：`features/` 与 `09-status/` 不整目录算机械产物——
    # feature.yaml / journal.md 与 09-status 台账是受控治理文档，应入库并 review；
    # 其中 features/<lifecycle>/<F-id>/evidence|artifacts 由目录段规则归 mechanical。
    ".harness/",
    ".kds/",
    ".okf/",
    "docs/harness/",
    "runtime/",
    "_meta/",
    "_governance/",
    ".codex/",
    ".agent-team/",
    "docs/evidence/",
    "docs/reports/",
    "docs/loops/",
    "docs/status/",
    "docs/ledger/",
    "evidence/",
    "artifacts/",
    "reports/",
    "loops/",
    "ledger/",
    "99_Reports/",
)

# 4) product：产品/工程面（真正需要被 review 的交付变更）。
PRODUCT_PREFIXES = (
    "src/",
    "apps/",
    "packages/",
    "tests/",
    "test/",
    "scripts/",
    "tools/",
    "config/",
    "configs/",
    "deployments/",
    "deploy/",
    "docker/",
    "infra/",
    "migrations/",
    "lib/",
    "libs/",
    "server/",
    "web/",
    "api/",
    "backend/",
    "frontend/",
    "cmd/",
    "pkg/",
    "internal/",
    ".github/",
    ".gitlab/",
    # 交付文档/业务知识/契约面（PG-16 文档债的处置对象，属被审交付物而非治理机制）
    "docs/",
    "openspec/",  # 变更提案与规格
    "research/",  # 调研产物
    "e2e/",
    "mkdocs/",
    "entities/",  # KDS 知识实体内容
    "schemas/",
    "sop/",
    "templates/",
    "samples/",
)
# 根级代码/工程/交付文档文件（无目录分隔符且扩展名在白名单内）→ product。
PRODUCT_ROOT_EXTENSIONS = (
    ".py",
    ".pyi",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".kts",
    ".c",
    ".h",
    ".cc",
    ".cpp",
    ".cs",
    ".rb",
    ".php",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".sql",
    ".proto",
    ".gradle",
    ".toml",
    ".json",
    ".yaml",
    ".yml",
    ".ini",
    ".cfg",
    ".conf",
    ".css",
    ".scss",
    ".less",
    ".html",
    ".htm",
    ".vue",
    ".svelte",
    ".dockerfile",
    ".mk",
    ".cmake",
    ".lock",
    ".md",
    ".mdx",
    ".rst",
    ".txt",
)


# ---------------------------------------------------------------------------
# config 解析（受限 YAML 子集：只取 projects 里的 {id:.., slug:.., repo:".."}）
# ---------------------------------------------------------------------------

PROJECT_LINE_RE = re.compile(
    r'^\s*-\s*\{\s*id:\s*(?P<id>[^,]+?)\s*,\s*slug:\s*(?P<slug>[^,]+?)\s*,'
    r'\s*repo:\s*"(?P<repo>[^"]+)"\s*\}\s*$'
)


def parse_config(config_path: Path) -> "list[dict[str, str]]":
    if not config_path.is_file():
        raise SystemExit(f"[配置错误] 找不到 config: {config_path}")
    # 首选 yaml 解析：注册表允许附加字段（如 retired / denominator_retained），
    # 受限 regex 只因历史原因保留为兜底。
    try:
        doc = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        items = doc.get("projects") or []
        parsed = [
            {"id": str(item["id"]), "slug": str(item.get("slug", "")), "repo": str(item["repo"])}
            for item in items
            if isinstance(item, dict) and item.get("id") and item.get("repo")
        ]
        if parsed:
            return parsed
    except Exception:
        pass
    projects: "list[dict[str, str]]" = []
    in_projects = False
    for raw in config_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if re.match(r"^projects:\s*$", line):
            in_projects = True
            continue
        if in_projects:
            if re.match(r"^\S", line):  # 顶层键，projects 段结束
                break
            match = PROJECT_LINE_RE.match(line)
            if not match:
                raise SystemExit(
                    "[配置错误] 无法解析 projects 行（格式与脚本预期不一致）: " + line
                )
            projects.append(
                {
                    "id": match.group("id").strip(),
                    "slug": match.group("slug").strip(),
                    "repo": match.group("repo").strip(),
                }
            )
    if not projects:
        raise SystemExit(f"[配置错误] {config_path} 未解析出任何 project")
    return projects


# ---------------------------------------------------------------------------
# git 调用与 porcelain 解析
# ---------------------------------------------------------------------------

C_ESCAPES = {
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
    "\\": "\\",
    '"': '"',
}


def unquote_git_path(text: str) -> str:
    """还原 porcelain 输出里的 C 风格引用（含空格/引号的路径会被加双引号）。"""
    if not (len(text) >= 2 and text[0] == '"' and text[-1] == '"'):
        return text
    body = text[1:-1]
    out: "list[str]" = []
    index = 0
    while index < len(body):
        char = body[index]
        if char != "\\" or index + 1 >= len(body):
            out.append(char)
            index += 1
            continue
        nxt = body[index + 1]
        if nxt in C_ESCAPES:
            out.append(C_ESCAPES[nxt])
            index += 2
        elif nxt.isdigit():  # 八进制转义 \ooo
            digits = body[index + 1:index + 4]
            try:
                out.append(chr(int(digits, 8)))
                index += 4
            except ValueError:
                out.append(char)
                index += 1
        else:
            out.append(nxt)
            index += 2
    return "".join(out)


def split_quoted_rename(rest: str) -> "tuple[str, str] | None":
    """把 `old -> new` 拆成 (old, new)，跳过引号内的 ` -> `。"""
    in_quotes = False
    index = 0
    while index < len(rest):
        char = rest[index]
        if char == "\\" and in_quotes:
            index += 2
            continue
        if char == '"':
            in_quotes = not in_quotes
            index += 1
            continue
        if not in_quotes and rest.startswith(" -> ", index):
            return unquote_git_path(rest[:index]), unquote_git_path(rest[index + 4:])
        index += 1
    return None


def parse_porcelain_line(line: str) -> "tuple[str, str, str] | None":
    """返回 (status, path, path_kind)；path_kind ∈ {normal, renamed_new, ...}。"""
    if len(line) < 4:
        return None
    status = line[:2]
    rest = line[3:] if len(line) > 3 else ""
    if not rest.strip():
        return None
    # rename / copy：`R  old -> new` / `C  old -> new`，取 new（任务口径）。
    if ("R" in status) or ("C" in status):
        pair = split_quoted_rename(rest)
        if pair is not None:
            _old, new = pair
            return status, new, "rename_new"
        return status, unquote_git_path(rest), "rename_fallback"
    return status, unquote_git_path(rest), "normal"


def run_git(repo_dir: Path, args: "list[str]", timeout: int = 180) -> "tuple[int, str, str]":
    try:
        completed = subprocess.run(
            ["git", "--no-optional-locks", *args],
            cwd=str(repo_dir),
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
        return completed.returncode, completed.stdout, completed.stderr
    except subprocess.TimeoutExpired:
        return 124, "", f"git {' '.join(args)} 超时（{timeout}s）"


def read_upstream(repo_dir: Path) -> "tuple[str | None, int | None, int | None]":
    """尽力读取分支与 ahead/behind（只读；失败时安静降级为 None）。"""
    branch = None
    ahead = behind = None
    code, out, _err = run_git(repo_dir, ["rev-parse", "--abbrev-ref", "HEAD"])
    if code == 0 and out.strip() and out.strip() != "HEAD":
        branch = out.strip()
    code, out, _err = run_git(
        repo_dir, ["rev-list", "--left-right", "--count", "@{upstream}...HEAD"]
    )
    if code == 0:
        parts = out.split()
        if len(parts) == 2:
            behind = int(parts[0])
            ahead = int(parts[1])
    return branch, ahead, behind


# ---------------------------------------------------------------------------
# 分类
# ---------------------------------------------------------------------------


def _basename(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def _extension(path: str) -> str:
    name = _basename(path).lower()
    if "." not in name:
        return ""
    return "." + name.rsplit(".", 1)[1]


def _match_any_glob(path: str, globs: "tuple[str, ...]") -> bool:
    from fnmatch import fnmatch

    return any(fnmatch(path, pattern) for pattern in globs)


def _match_any_glob_basename(path: str, globs: "tuple[str, ...]") -> bool:
    from fnmatch import fnmatch

    name = _basename(path)
    return any(fnmatch(name, pattern) for pattern in globs)


def _has_dir_segment(path: str, segments: "tuple[str, ...]") -> bool:
    parts = path.split("/")[:-1]  # 末尾是文件名，不算目录段
    return any(part in segments for part in parts)


def _has_non_ascii_dir_segment(path: str) -> bool:
    """中文/非 ASCII 命名的目录视为业务内容目录（治理产物统一用英文固定目录）。"""
    for segment in path.split("/")[:-1]:
        if any(ord(char) > 127 for char in segment):
            return True
    return False


def _governance_subcategory(path: str) -> str:
    """governance 再分两桶：mechanical（机制自动产物） / controlled（受控治理文档）。"""
    if any(path.startswith(prefix) for prefix in GOVERNANCE_MECHANICAL_PREFIXES):
        return "mechanical"
    if GOVERNANCE_NUMERIC_DIR_RE.match(path):
        return "mechanical" if "governance" in path.split("/")[0] else "controlled"
    if _has_dir_segment(path, ("evidence", "artifacts", "_verify-reports")):
        return "mechanical"
    return "controlled"


def classify(path: str) -> str:
    """按 优先级 sensitive > noise > governance > product > unknown 归类。"""
    name = _basename(path)
    root_segments = path.split("/")

    # 1) sensitive
    if _match_any_glob_basename(name, SENSITIVE_BASENAME_GLOBS):
        return "sensitive"
    if any(token in name.lower() for token in SENSITIVE_NAME_TOKENS):
        if _extension(path) not in SENSITIVE_NAME_TOKEN_EXEMPT_EXTENSIONS:
            return "sensitive"

    # 2) noise
    if name in NOISE_BASENAMES:
        return "noise"
    if any(infix in name.lower() for infix in NOISE_NAME_INFIXES):
        return "noise"
    if root_segments[0].startswith(NOISE_TOP_SEGMENT_PREFIXES):
        return "noise"
    if _has_dir_segment(path, NOISE_DIR_SEGMENTS) or any(
        f"/{segment}/" in path or path.startswith(segment + "/")
        for segment in NOISE_DIR_SEGMENTS
    ):
        return "noise"
    if _extension(path) in NOISE_EXTENSIONS or name.endswith("~"):
        return "noise"

    # 3) governance
    if any(path.startswith(prefix) for prefix in GOVERNANCE_PREFIXES):
        return "governance"
    if GOVERNANCE_NUMERIC_DIR_RE.match(path):
        return "governance"
    if _has_dir_segment(path, GOVERNANCE_DIR_SEGMENTS):
        return "governance"
    if _match_any_glob(path, GOVERNANCE_PATH_GLOBS):
        return "governance"
    if "/" not in path and GOVERNANCE_ROOT_DOC_RE.match(path):
        return "governance"

    # 4) product
    if any(path.startswith(prefix) for prefix in PRODUCT_PREFIXES):
        return "product"
    if "/" not in path and (_extension(path) in PRODUCT_ROOT_EXTENSIONS or path.startswith(".")):
        return "product"
    if _has_non_ascii_dir_segment(path):
        # 中文命名目录：业务知识/交付内容（治理产物不用中文目录名）
        return "product"

    # 5) unknown
    return "unknown"


# ---------------------------------------------------------------------------
# 采集与汇总
# ---------------------------------------------------------------------------


def directory_key(path: str) -> str:
    parts = path.split("/")
    if len(parts) == 1:
        return "(仓根)"
    if len(parts) == 2:
        return parts[0] + "/"
    return parts[0] + "/" + parts[1] + "/"


def collect_repo(project: "dict[str, str]", workspace: Path) -> "dict[str, object]":
    repo_name = project["repo"]
    repo_dir = workspace / repo_name
    record: "dict[str, object]" = {
        "id": project["id"],
        "slug": project["slug"],
        "repo": repo_name,
        "path": str(repo_dir),
        "exists": repo_dir.is_dir(),
        "git": (repo_dir / ".git").exists() or (repo_dir / ".git").is_file(),
        "error": None,
        "dirty": 0,
        "counts": {category: 0 for category in CATEGORIES},
        "counts_untracked": {category: 0 for category in CATEGORIES},
        "counts_tracked": {category: 0 for category in CATEGORIES},
        "governance_sub": {"mechanical": 0, "controlled": 0},
        "governance_sub_untracked": {"mechanical": 0, "controlled": 0},
        "status_counts": {},
        "branch": None,
        "ahead": None,
        "behind": None,
        "paths": [],
        "rename_count": 0,
    }
    if not record["exists"] or not record["git"]:
        record["error"] = "仓目录或 .git 不存在"
        return record

    code, out, err = run_git(
        repo_dir, ["-c", "core.quotePath=false", "status", "--porcelain", "-uall"]
    )
    if code != 0:
        record["error"] = (err or out).strip()[:500] or f"git status 退出码 {code}"
        return record

    counts = Counter()
    untracked_counts = Counter()
    status_counts = Counter()
    governance_sub = Counter()
    governance_sub_untracked = Counter()
    paths: "list[dict[str, str]]" = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parsed = parse_porcelain_line(line)
        if parsed is None:
            continue
        status, path, kind = parsed
        category = classify(path)
        subcategory = _governance_subcategory(path) if category == "governance" else ""
        counts[category] += 1
        is_untracked = status == "??"
        if is_untracked:
            untracked_counts[category] += 1
        if subcategory:
            governance_sub[subcategory] += 1
            if is_untracked:
                governance_sub_untracked[subcategory] += 1
        status_counts[status.strip() or status] += 1
        if kind == "rename_new":
            record["rename_count"] = int(record["rename_count"]) + 1  # type: ignore[arg-type]
        entry = {"path": path, "status": status, "category": category}
        if subcategory:
            entry["subcategory"] = subcategory
        paths.append(entry)

    record["dirty"] = len(paths)
    record["counts"] = {category: counts.get(category, 0) for category in CATEGORIES}
    record["counts_untracked"] = {
        category: untracked_counts.get(category, 0) for category in CATEGORIES
    }
    record["counts_tracked"] = {
        category: counts.get(category, 0) - untracked_counts.get(category, 0)
        for category in CATEGORIES
    }
    record["governance_sub"] = {
        "mechanical": governance_sub.get("mechanical", 0),
        "controlled": governance_sub.get("controlled", 0),
    }
    record["governance_sub_untracked"] = {
        "mechanical": governance_sub_untracked.get("mechanical", 0),
        "controlled": governance_sub_untracked.get("controlled", 0),
    }
    record["status_counts"] = dict(sorted(status_counts.items()))
    record["paths"] = sorted(paths, key=lambda item: item["path"])
    branch, ahead, behind = read_upstream(repo_dir)
    record["branch"], record["ahead"], record["behind"] = branch, ahead, behind
    return record


def summarize(records: "list[dict[str, object]]", top_n: int) -> "dict[str, object]":
    totals = Counter()
    untracked_totals = Counter()
    status_totals = Counter()
    governance_sub_totals = Counter()
    governance_sub_untracked = Counter()
    dir_counter: "Counter[str]" = Counter()
    dir_categories: "dict[str, Counter[str]]" = {}
    for record in records:
        if record["error"]:
            continue
        totals["dirty"] += int(record["dirty"])  # type: ignore[arg-type]
        for category, value in dict(record["counts"]).items():  # type: ignore[arg-type]
            totals[category] += int(value)
        for category, value in dict(record["counts_untracked"]).items():  # type: ignore[arg-type]
            untracked_totals[category] += int(value)
        for subcategory, value in dict(record["governance_sub"]).items():  # type: ignore[arg-type]
            governance_sub_totals[subcategory] += int(value)
        for subcategory, value in dict(record["governance_sub_untracked"]).items():  # type: ignore[arg-type]
            governance_sub_untracked[subcategory] += int(value)
        for status, value in dict(record["status_counts"]).items():  # type: ignore[arg-type]
            status_totals[status] += int(value)
        for item in record["paths"]:  # type: ignore[union-attr]
            key = directory_key(item["path"])
            dir_counter[key] += 1
            dir_categories.setdefault(key, Counter())[item["category"]] += 1

    dirty_total = int(totals.get("dirty", 0))
    category_totals = {category: int(totals.get(category, 0)) for category in CATEGORIES}
    untracked_by_category = {
        category: int(untracked_totals.get(category, 0)) for category in CATEGORIES
    }
    tracked_by_category = {
        category: category_totals[category] - untracked_by_category[category]
        for category in CATEGORIES
    }
    mechanical = int(governance_sub_totals.get("mechanical", 0))
    controlled = int(governance_sub_totals.get("controlled", 0))
    mechanical_untracked = int(governance_sub_untracked.get("mechanical", 0))
    mechanical_tracked = mechanical - mechanical_untracked
    noise_untracked = untracked_by_category["noise"]
    noise_tracked = tracked_by_category["noise"]
    # 只加 .gitignore（不 untrack 已跟踪文件）能隐藏的条数
    ignore_only_hidden = mechanical_untracked + noise_untracked
    ignore_only_visible = max(dirty_total - ignore_only_hidden, 0)
    # 迁移（治理产物目录移出 / git rm --cached + ignore）后 git gate 可见的条数
    reviewable_after_removal = max(dirty_total - mechanical - noise_untracked - noise_tracked, 0)
    top_directories = []
    for key, count in sorted(dir_counter.items(), key=lambda kv: (-kv[1], kv[0]))[:top_n]:
        top_directories.append(
            {
                "dir": key,
                "count": count,
                "categories": {
                    category: int(dir_categories[key].get(category, 0))
                    for category in CATEGORIES
                },
            }
        )

    per_repo_governance = [
        {
            "id": record["id"],
            "repo": record["repo"],
            "dirty": int(record["dirty"]),  # type: ignore[arg-type]
            "governance": int(dict(record["counts"])["governance"]),  # type: ignore[arg-type]
            "ratio": round(
                int(dict(record["counts"])["governance"]) / int(record["dirty"]), 4  # type: ignore[arg-type]
            )
            if int(record["dirty"])  # type: ignore[arg-type]
            else 0.0,
        }
        for record in records
        if not record["error"] and int(record["dirty"]) > 0  # type: ignore[arg-type]
    ]
    per_repo_governance.sort(key=lambda item: (-item["ratio"], -item["dirty"], item["id"]))

    return {
        "project_count": len(records),
        "repos_ok": sum(1 for record in records if not record["error"]),
        "repos_error": sum(1 for record in records if record["error"]),
        "dirty_repos": sum(
            1 for record in records if not record["error"] and int(record["dirty"]) > 0  # type: ignore[arg-type]
        ),
        "clean_repos": sum(
            1 for record in records if not record["error"] and int(record["dirty"]) == 0  # type: ignore[arg-type]
        ),
        "dirty_total": dirty_total,
        "category_totals": category_totals,
        "category_ratios": {
            category: (round(value / dirty_total, 6) if dirty_total else 0.0)
            for category, value in category_totals.items()
        },
        "governance_sub_totals": {
            "mechanical": mechanical,
            "controlled": controlled,
            "mechanical_untracked": mechanical_untracked,
            "mechanical_tracked": mechanical_tracked,
            "controlled_untracked": int(governance_sub_untracked.get("controlled", 0)),
            "controlled_tracked": controlled - int(governance_sub_untracked.get("controlled", 0)),
        },
        "untracked_by_category": untracked_by_category,
        "tracked_by_category": tracked_by_category,
        "ignore_simulation": {
            "ignore_only_hidden": ignore_only_hidden,
            "ignore_only_visible": ignore_only_visible,
            "ignore_only_remaining_mechanical": mechanical_tracked,
            "ignore_only_remaining_noise": noise_tracked,
            "after_migration_visible": reviewable_after_removal,
        },
        "reviewable_after_removal": reviewable_after_removal,
        "reviewable_after_removal_ratio": (
            round(reviewable_after_removal / dirty_total, 6) if dirty_total else 0.0
        ),
        "status_counts": dict(sorted(status_totals.items())),
        "top_directories": top_directories,
        "governance_top_repos": per_repo_governance[:10],
    }


def build_digest(records: "list[dict[str, object]]", summary: "dict[str, object]") -> str:
    """对分类结果做稳定指纹：同一工作树状态下重复运行应一致。"""
    material = {
        "repos": [
            {
                "id": record["id"],
                "repo": record["repo"],
                "dirty": record["dirty"],
                "counts": record["counts"],
                "paths": [[item["status"], item["path"], item["category"]] for item in record["paths"]],  # type: ignore[union-attr]
            }
            for record in records
        ],
        "category_totals": summary["category_totals"],
        "dirty_total": summary["dirty_total"],
    }
    blob = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# 渲染
# ---------------------------------------------------------------------------


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def render_text(payload: "dict[str, object]", top_n: int, per_repo_top: int = 0) -> str:
    summary = payload["summary"]
    records = payload["repos"]
    lines: "list[str]" = []
    lines.append("=" * 78)
    lines.append(f"PG-04 项目群 dirty 路径分类  {payload['tool']} {payload['version']}")
    lines.append("=" * 78)
    lines.append(f"采集时点      : {payload['generated_at']}")
    lines.append(f"工作区根      : {payload['workspace_root']}")
    lines.append(f"config        : {payload['config']}")
    lines.append(f"命令模板      : {payload['command_template']}")
    lines.append(
        f"仓覆盖        : {summary['repos_ok']}/{summary['project_count']} 个仓读取成功"
        f"（失败 {summary['repos_error']}）"
    )
    lines.append(
        f"dirty 汇总    : {summary['dirty_total']} 条 / dirty 仓 {summary['dirty_repos']} 个"
        f" / clean 仓 {summary['clean_repos']} 个"
    )
    lines.append("")
    lines.append("分类分布:")
    for category in CATEGORIES:
        value = summary["category_totals"][category]
        lines.append(f"  {category:<10s}{value:>6d}  {pct(summary['category_ratios'][category])}")
    lines.append(
        f"  ├─ governance/mechanical（机制自动产物）{summary['governance_sub_totals']['mechanical']:>5d}"
    )
    lines.append(
        f"  └─ governance/controlled（受控治理文档）{summary['governance_sub_totals']['controlled']:>5d}"
    )
    lines.append(
        f"移出被审面后（剔除 governance/mechanical + noise）可枚举变更集: "
        f"{summary['reviewable_after_removal']} 条（{pct(summary['reviewable_after_removal_ratio'])}）"
    )
    lines.append("")
    sim = summary["ignore_simulation"]
    lines.append("gitignore / 迁移 只读模拟（不执行）:")
    lines.append(
        f"  governance/mechanical  {summary['governance_sub_totals']['mechanical']} 条"
        f"（未跟踪 {summary['governance_sub_totals']['mechanical_untracked']} / "
        f"已跟踪 {summary['governance_sub_totals']['mechanical_tracked']}）"
    )
    lines.append(
        f"  governance/controlled  {summary['governance_sub_totals']['controlled']} 条"
        f"（未跟踪 {summary['governance_sub_totals']['controlled_untracked']} / "
        f"已跟踪 {summary['governance_sub_totals']['controlled_tracked']}）"
    )
    lines.append(
        f"  noise                  {summary['category_totals']['noise']} 条"
        f"（未跟踪 {summary['untracked_by_category']['noise']} / "
        f"已跟踪 {summary['tracked_by_category']['noise']}）"
    )
    lines.append(
        f"  仅新增 .gitignore（不动已跟踪文件）能隐藏 {sim['ignore_only_hidden']} 条，"
        f"git gate 仍可见 {sim['ignore_only_visible']} 条"
        f"（其中 mechanical 已跟踪 {sim['ignore_only_remaining_mechanical']} 条、"
        f"noise 已跟踪 {sim['ignore_only_remaining_noise']} 条）"
    )
    lines.append(
        f"  执行迁移（目录移出或 git rm --cached + ignore）后 git gate 可见 "
        f"{sim['after_migration_visible']} 条"
    )
    lines.append("")
    lines.append("状态码分布（porcelain XY 的 X 位，空位记 ' '）:")
    for status, value in summary["status_counts"].items():
        lines.append(f"  {status!r:<8s}{value:>6d}")
    lines.append("")
    lines.append("-" * 78)
    lines.append("逐仓分类表（按 dirty 降序）")
    lines.append("-" * 78)
    header = (
        f"{'#':>2}  {'项目':<14s}{'仓目录':<32s}{'dirty':>6s}"
        f"{'gov':>6s}{'prod':>6s}{'noise':>6s}{'sens':>5s}{'unk':>5s}  {'gov占比':>7s}"
    )
    lines.append(header)
    lines.append("-" * len(header))
    ordered = sorted(
        records,
        key=lambda record: (
            -int(record["dirty"]),  # type: ignore[arg-type]
            record["id"],  # type: ignore[return-value]
        ),
    )
    for index, record in enumerate(ordered, start=1):
        counts = record["counts"]
        dirty = int(record["dirty"])  # type: ignore[arg-type]
        ratio = (counts["governance"] / dirty) if dirty else 0.0  # type: ignore[index,operator]
        if record["error"]:
            lines.append(
                f"{index:>2}  {record['id']:<14s}{record['repo']:<32s}{'ERR':>6s}  {record['error']}"
            )
            continue
        lines.append(
            f"{index:>2}  {record['id']:<14s}{record['repo']:<32s}{dirty:>6d}"
            f"{counts['governance']:>6d}{counts['product']:>6d}{counts['noise']:>6d}"  # type: ignore[index]
            f"{counts['sensitive']:>5d}{counts['unknown']:>5d}  {pct(ratio):>7s}"
        )
    lines.append("")
    lines.append("-" * 78)
    lines.append(f"Top {top_n} 目录聚合（按 dirty 条数）")
    lines.append("-" * 78)
    for entry in summary["top_directories"]:
        cats = entry["categories"]
        lines.append(
            f"  {entry['count']:>4d}  {entry['dir']:<44s}"
            f" gov={cats['governance']:<4d} prod={cats['product']:<4d}"
            f" noise={cats['noise']:<3d} sens={cats['sensitive']:<2d} unk={cats['unknown']}"
        )
    if per_repo_top > 0:
        lines.append("")
        lines.append("-" * 78)
        lines.append(f"按仓目录聚合 Top {per_repo_top}（仅列 dirty>0 的仓）")
        lines.append("-" * 78)
        for record in ordered:
            if record["error"] or int(record["dirty"]) == 0:  # type: ignore[arg-type]
                continue
            counter: "Counter[str]" = Counter()
            cats: "dict[str, Counter[str]]" = {}
            for item in record["paths"]:  # type: ignore[union-attr]
                key = directory_key(item["path"])
                counter[key] += 1
                cats.setdefault(key, Counter())[item["category"]] += 1
            lines.append(
                f"  [{record['id']}] {record['repo']}  dirty={record['dirty']}"
            )
            for key, count in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))[:per_repo_top]:
                category_part = " ".join(
                    f"{category}={cats[key].get(category, 0)}"
                    for category in CATEGORIES
                    if cats[key].get(category, 0)
                )
                lines.append(f"      {count:>4d}  {key:<40s} {category_part}")
    lines.append("")
    lines.append(f"结果指纹 digest: {payload['digest']}")
    lines.append("（本脚本只读：未写文件、未删除、未 stage/commit）")
    return "\n".join(lines)


def render_markdown(payload: "dict[str, object]", top_n: int) -> str:
    summary = payload["summary"]
    records = payload["repos"]
    lines: "list[str]" = []
    lines.append(f"> 采集时点 `{payload['generated_at']}`；工具 `{payload['tool']} {payload['version']}`；")
    lines.append(f"> 命令原文 `{payload['command_template']}`。")
    lines.append("")
    lines.append(
        f"**全局**：{summary['repos_ok']}/{summary['project_count']} 仓读取成功；"
        f"dirty 共 **{summary['dirty_total']}** 条，分布 {summary['dirty_repos']} 个仓，"
        f"clean {summary['clean_repos']} 个仓。"
    )
    lines.append("")
    lines.append("| 分类 | 条数 | 占比 |")
    lines.append("|---|---:|---:|")
    for category in CATEGORIES:
        lines.append(
            f"| `{category}` | {summary['category_totals'][category]} | "
            f"{pct(summary['category_ratios'][category])} |"
        )
    lines.append(
        f"| ├─ `governance/mechanical` | {summary['governance_sub_totals']['mechanical']} | "
        f"{pct(summary['governance_sub_totals']['mechanical'] / summary['dirty_total'] if summary['dirty_total'] else 0)} |"
    )
    lines.append(
        f"| └─ `governance/controlled` | {summary['governance_sub_totals']['controlled']} | "
        f"{pct(summary['governance_sub_totals']['controlled'] / summary['dirty_total'] if summary['dirty_total'] else 0)} |"
    )
    lines.append("")
    lines.append(
        f"**移出被审面后**（剔除 `governance/mechanical` + `noise`）Git gate 可枚举变更集："
        f"**{summary['reviewable_after_removal']}** 条"
        f"（{pct(summary['reviewable_after_removal_ratio'])}）。"
    )
    lines.append("")
    lines.append("### gitignore / 迁移 只读模拟（不执行）")
    lines.append("")
    lines.append("| 口径 | 条数 |")
    lines.append("|---|---:|")
    lines.append(f"| 当前 dirty 总数 | {summary['dirty_total']} |")
    lines.append(
        f"| governance/mechanical 未跟踪（`.gitignore` 可直接隐藏） | "
        f"{summary['governance_sub_totals']['mechanical_untracked']} |"
    )
    lines.append(
        f"| governance/mechanical 已跟踪（需目录移出或 `git rm --cached`） | "
        f"{summary['governance_sub_totals']['mechanical_tracked']} |"
    )
    lines.append(
        f"| noise 未跟踪 / 已跟踪 | {summary['untracked_by_category']['noise']} / "
        f"{summary['tracked_by_category']['noise']} |"
    )
    lines.append(f"| 仅新增 `.gitignore` 后 git gate 可见 | {summary['ignore_simulation']['ignore_only_visible']} |")
    lines.append(
        f"| 迁移（目录移出 / `git rm --cached` + ignore）后 git gate 可见 | "
        f"{summary['ignore_simulation']['after_migration_visible']} |"
    )
    lines.append("")
    lines.append("### 逐仓分类表")
    lines.append("")
    lines.append(
        "| # | 项目 | 仓目录 | dirty | governance | ├ mechanical | └ controlled | "
        "product | noise | sensitive | unknown | governance 占比 |"
    )
    lines.append("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    ordered = sorted(
        records,
        key=lambda record: (-int(record["dirty"]), record["id"]),  # type: ignore[arg-type,return-value]
    )
    for index, record in enumerate(ordered, start=1):
        counts = record["counts"]
        sub = record["governance_sub"]
        dirty = int(record["dirty"])  # type: ignore[arg-type]
        ratio = (counts["governance"] / dirty) if dirty else 0.0  # type: ignore[index,operator]
        if record["error"]:
            lines.append(
                f"| {index} | {record['id']} | `{record['repo']}` | ERR | - | - | - | - | - | - | - | {record['error']} |"
            )
            continue
        lines.append(
            f"| {index} | {record['id']} | `{record['repo']}` | {dirty} | {counts['governance']} | "
            f"{sub['mechanical']} | {sub['controlled']} | "
            f"{counts['product']} | {counts['noise']} | {counts['sensitive']} | "
            f"{counts['unknown']} | {pct(ratio)} |"
        )
    lines.append("")
    lines.append(f"### Top {top_n} 目录聚合")
    lines.append("")
    lines.append("| 目录 | 条数 | governance | product | noise | sensitive | unknown |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|")
    for entry in summary["top_directories"]:
        cats = entry["categories"]
        lines.append(
            f"| `{entry['dir']}` | {entry['count']} | {cats['governance']} | {cats['product']} | "
            f"{cats['noise']} | {cats['sensitive']} | {cats['unknown']} |"
        )
    lines.append("")
    status_line = "、".join(f"`{status}`={value}" for status, value in summary["status_counts"].items())
    lines.append(f"状态码分布：{status_line}。")
    lines.append("")
    lines.append(f"结果指纹 `digest = {payload['digest']}`。")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main(argv: "list[str] | None" = None) -> int:
    parser = argparse.ArgumentParser(
        description="PG-04：对项目群 28 仓未提交变更做只读分类（governance/product/noise/sensitive/unknown）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="project-group-projects.yaml 路径")
    parser.add_argument(
        "--only",
        default=None,
        help="只跑指定仓：逗号分隔的 project id 或仓目录名（用于小样试跑）",
    )
    parser.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    parser.add_argument("--markdown", action="store_true", help="输出 Markdown 表格")
    parser.add_argument("--top", type=int, default=20, help="全局目录聚合 Top N，默认 20")
    parser.add_argument(
        "--per-repo-top",
        type=int,
        default=0,
        help="额外输出逐仓目录聚合 Top N（0 表示不输出）",
    )
    parser.add_argument(
        "--no-timestamp",
        action="store_true",
        help="省略 generated_at（用于两次运行逐字节比对确定性）",
    )
    args = parser.parse_args(argv)
    if args.json and args.markdown:
        parser.error("--json 与 --markdown 不能同时使用")

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = (Path.cwd() / config_path).resolve()
    projects = parse_config(config_path)

    selected = projects
    if args.only:
        wanted = {token.strip() for token in args.only.split(",") if token.strip()}
        known = {project["id"] for project in projects} | {project["repo"] for project in projects}
        unknown = wanted - known
        if unknown:
            parser.error(f"--only 中有未知仓: {sorted(unknown)}")
        selected = [
            project
            for project in projects
            if project["id"] in wanted or project["repo"] in wanted
        ]

    workspace = PROJECT_ROOT
    records = [collect_repo(project, workspace) for project in selected]
    summary = summarize(records, args.top)
    digest = build_digest(records, summary)

    payload = OrderedDict(
        [
            ("tool", TOOL_NAME),
            ("version", TOOL_VERSION),
            ("generated_at", None if args.no_timestamp else datetime.now().astimezone().isoformat(timespec="seconds")),
            ("workspace_root", str(workspace)),
            ("gpcf_repo", str(ROOT)),
            ("config", str(config_path)),
            ("command_template", COMMAND_TEMPLATE),
            ("upstream_template", UPSTREAM_TEMPLATE),
            ("project_count", len(projects)),
            ("selected_count", len(selected)),
            ("rules", {
                "precedence": list(CATEGORIES),
                "governance_prefixes": list(GOVERNANCE_PREFIXES),
                "governance_numeric_dir_regex": GOVERNANCE_NUMERIC_DIR_RE.pattern,
                "governance_dir_segments": list(GOVERNANCE_DIR_SEGMENTS),
                "governance_controlled_doc_regex": GOVERNANCE_ROOT_DOC_RE.pattern,
                "governance_mechanical_prefixes": list(GOVERNANCE_MECHANICAL_PREFIXES),
                "product_prefixes": list(PRODUCT_PREFIXES),
                "product_root_extensions": list(PRODUCT_ROOT_EXTENSIONS),
                "noise_basenames": list(NOISE_BASENAMES),
                "noise_name_infixes": list(NOISE_NAME_INFIXES),
                "noise_dir_segments": list(NOISE_DIR_SEGMENTS),
                "noise_extensions": list(NOISE_EXTENSIONS),
                "sensitive_basename_globs": list(SENSITIVE_BASENAME_GLOBS),
                "sensitive_name_tokens": list(SENSITIVE_NAME_TOKENS),
                "sensitive_name_token_exempt_extensions": list(
                    SENSITIVE_NAME_TOKEN_EXEMPT_EXTENSIONS
                ),
                "note": "中文/非 ASCII 目录段归入 product（业务内容）；治理产物统一用英文固定目录。",
            }),
            ("summary", summary),
            ("repos", records),
            ("digest", digest),
        ]
    )

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False))
    elif args.markdown:
        print(render_markdown(payload, args.top))
    else:
        print(render_text(payload, args.top, args.per_repo_top))

    if summary["repos_error"]:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
