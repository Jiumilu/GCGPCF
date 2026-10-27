"""测试用 git 子进程环境：剥掉所有 ``GIT_*`` 变量（2026-10-27 P0 修复）。

为什么需要
----------
git 在 pre-commit hook 里会向子进程导出 ``GIT_DIR`` / ``GIT_WORK_TREE`` /
``GIT_INDEX_FILE`` / ``GIT_PREFIX`` 等变量。测试在 ``tempfile`` 里执行的
``git init / config / add / commit`` 若继承这些变量，git 会把这些操作打到
**真实仓**上——已实测复现：

* ``GIT_DIR`` 单设：真实仓被推进一笔（内容含测试临时文件），
  ``user.name`` / ``user.email`` 被改成 fixture 身份；
* 再带 ``GIT_WORK_TREE``：测试本身还会因为 pathspec 解析错位而**假红**。

所以凡测试里直接调 ``git`` 的地方，一律显式传 ``env=clean_git_env()``；
被测代码内部自己调 git 的情形由 ``tests/conftest.py`` 的会话级剥除兜底。

用法::

    subprocess.run(["git", "init", "-q"], cwd=tmp, check=True, env=clean_git_env())
"""

from __future__ import annotations

import os


def clean_git_env(base: dict[str, str] | None = None) -> dict[str, str]:
    """返回一份去掉了所有 ``GIT_*`` 键的环境变量副本。

    不修改 ``os.environ``，也不修改传入的 ``base``，调用方可以安全多次调用。
    """
    env = dict(os.environ if base is None else base)
    for key in [k for k in env if k.startswith("GIT_")]:
        env.pop(key, None)
    return env
