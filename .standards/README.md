# `.standards/` — 项目群规范检查快照（勿手改）

由项目群治理仓 `_governance/tools/sync_vendor.py` 生成，供本仓 CI（GitHub-hosted runner）使用。
- 检查器：`tools/gc_standard.py`（Python3 标准库，无依赖）
- 规则：`rules/standards.yaml` + `rules/exceptions.yaml`
- 注册表快照：`registry/project-group-projects.yaml`
- 版本：见 `VERSION`（治理仓提交 + 生成时间）

更新方式：在项目群工作区跑 `python3 _governance/tools/sync_vendor.py --apply`，不要手改本目录。
