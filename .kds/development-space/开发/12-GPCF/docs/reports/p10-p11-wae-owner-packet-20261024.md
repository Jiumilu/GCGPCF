---
doc_id: GPCF-DOC-A50103148C
title: P10 / P11 · 界面分层与双角色权限一致性 · WAE 属主执行包（2026-10-24 更正版）
project: GPCF
related_projects: [GPC, WAME, PKC, MMC, GPCF, ICP]
domain: docs
status: controlled
version: v1.0
owner: GPCF
kds_space: 开发
kds_path: 开发/12-GPCF/docs/reports/p10-p11-wae-owner-packet-20261024.md
source_path: docs/reports/p10-p11-wae-owner-packet-20261024.md
sync_direction: bidirectional
last_reviewed: unreviewed
supersedes: []
superseded_by: []
---

# P10 / P11 · 界面分层与双角色权限一致性 · WAE 属主执行包（2026-10-24 更正版）

- 依据：计划 P10/P11、`LOOP_UI_PRODUCT_FIRST_CONTROL.md`、WAE 实际装配清单 `docs/assembly-spec/placement.city.yaml`（v1.0 / 2026-10-22）
- **重要更正**：原执行包按"29 service entries"设计矩阵——实测 `placement.city.yaml` 是 **6 个 apps + 22 个 entries**，不再沿用 29 的口径
- 边界：WAE 仓改动由属主执行；GPCF 只出规格与判据（纪律⑤）

## 1. 实际结构（只读核查）

| apps（6） | entries（22） |
|---|---|
| feedback 反馈中心 | feedback-center、feature-plaza |
| spaceai SpaceAI 场景 | spaceai-map3d、spaceai-scene-center、spaceai-home、spaceai-logviewer、spaceai-alarm-center、spaceai-alarm-action、spaceai-message-dispatch |
| pqc PQC 包装业务 | pqc-business、pqc-calc、pqc-orders、pqc-sop |
| pkc PKC 知识工作台 | pkc-intake |
| wasset 项目工作台 | wasset-studio |
| service 服务控制台 | gcas-console、mmc-console、gpcf-console、icp-console、aaas-console、feedback-console、idp-console |

## 2. P10 分层方案（建议直接落 `placement.city.yaml`）

| 层级 | app 级 `ui_plane` | 说明 |
|---|---|---|
| user | feedback、spaceai、pqc、pkc、wasset | 普通用户界面（业务与场景） |
| governance | service | 治理/审计类（GCAs/MMC/GPCF/ICP/AaaS/反馈管理/身份权限） |

**entry 级覆盖（2 条需与 app 级不同）**
| entry | ui_plane | 理由 |
|---|---|---|
| `feature-plaza` | user | 特性广场面向用户 |
| `pkc-intake` | governance | 接入评审候选，含准入判断 |

判据：
```bash
cd "GlobalCloud WAE"
python3 - <<'EOF'
import yaml
d=yaml.safe_load(open('docs/assembly-spec/placement.city.yaml'))
apps=d['apps']; entries=d['entries']
assert len(apps)==6 and len(entries)==22, (len(apps), len(entries))
assert all(a.get('ui_plane') in ('user','governance') for a in apps), 'app 缺 ui_plane'
missing=[e['id'] for e in entries if e.get('ui_plane') not in ('user','governance')]
assert not missing, f'entry 缺 ui_plane: {missing}'
print('P10 ok')
EOF
```
另需：治理页路由统一 `/governance/*`、viewer 访问断言 403/重定向（DOM 用例）。

## 3. P11 双角色矩阵（建议以 22 entries 为行）

行 = 22 entries；列 = `admin` / `viewer`；第三列 `diff_declared`（两者不同时必须说明理由）。

```yaml
# 建议写入 WAE 仓 docs/assembly-spec/role-matrix.yaml（属主执行）
version: v0.1
dimension: entry            # 22 个 entries
roles: [admin, viewer]
required_roles_source: MMC管理数据卡契约_v0.1.md  # entries 的 required_roles 字段口径
rows:
  - entry: feedback-center
    admin: allow
    viewer: allow
    diff_declared: false
  - entry: gpcf-console       # 治理台：viewer 应拒绝
    admin: allow
    viewer: deny
    diff_declared: true
    diff_reason: 治理审计界面仅管理员可见
  # …其余 20 行由属主按同一格式补齐
```

判据：
```bash
# 矩阵覆盖 22/22，且未声明差异为 0
python3 -c "
import yaml;m=yaml.safe_load(open('docs/assembly-spec/role-matrix.yaml'))
assert len(m['rows'])==22, len(m['rows'])
bad=[r['entry'] for r in m['rows'] if r['admin']!=r['viewer'] and not r.get('diff_declared')]
assert not bad, bad
print('P11 ok')"
pnpm vitest run apps/shell   # 双角色 DOM 用例通过
```

## 4. 非声明

通过 ≠ 产品验收；不得声明 accepted/integrated/production_ready；e2e/browser/a11y 归 P16-3。
