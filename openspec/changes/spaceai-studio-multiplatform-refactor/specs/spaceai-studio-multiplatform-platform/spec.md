---
doc_id: GPCF-OS-SPACEAI-STUDIO-MULTIPLATFORM-REFACTOR-SPEC-20261010
title: spec
project: SpaceAIStudio
related_projects: [SpaceAIStudio, SpaceAI, Studio, GPCF, KDS]
domain: openspec
status: draft
version: v1.0
owner: 老卢
kds_space: 开发
kds_path: 开发/14-SpaceAIStudio/openspec/changes/spaceai-studio-multiplatform-refactor/specs/spaceai-studio-multiplatform-platform/spec.md
source_path: openspec/changes/spaceai-studio-multiplatform-refactor/specs/spaceai-studio-multiplatform-platform/spec.md
sync_direction: bidirectional
last_reviewed: 2026-10-10
supersedes: []
superseded_by: []
---

## ADDED Requirements

### Requirement: 素材来源与处置边界

项目 MUST 区分素材来源并遵循处置规则：非设备类接入组件（DLL 或其它调用）为我方资产，有源码者 MUST 源码级复用，无源码者 MUST 使用已安装的 `ilspycmd` 工具逆向恢复并逐项登记接口签名；设备类组件为第三方，MUST NOT 逆向。逆向产物 MUST 与原 DLL 行为一致。

#### Scenario: 处置任一依赖

- **WHEN** 处理任一外部依赖
- **THEN** 其处置方式（源码复用 / 逆向 / 第三方替换 / 重新设计）被明确登记，且设备类未被逆向

#### Scenario: 逆向产物核对

- **WHEN** 完成一次逆向
- **THEN** 反编译结果与原 DLL 行为一致，关键接口签名逐项登记

### Requirement: 宿主与模块的装配关系

项目 MUST 保持「宿主 + 模块」的装配关系，并使产品定位与工程装配分层表述：产品定位为空间智能工作台，工程装配为本项目（宿主壳）+ `SpaceAI` 模块库。项目 MUST 定义并维护唯一的插件契约（`plugin-sdk`），模块 MUST NOT 使宿主与其耦合。

#### Scenario: 审查装配关系

- **WHEN** 审查人员检查两个项目的工程角色
- **THEN** 本项目被标注为宿主壳（`OutputType=WinExe`，定义插件契约），`SpaceAI` 的 `MB3000` 被标注为模块库（`OutputType=Library`），且两者治理身份各自独立登记

#### Scenario: 挂载新模块

- **WHEN** 新增一个功能模块
- **THEN** 宿主在不修改壳代码的前提下，仅通过模块清单即可挂载（可装配验收口径）

### Requirement: 项目重定位为空间智能工作台

SpaceAI Studio SHALL 重定位为 GlobalCloud 的空间智能工作台，承担空间感知、空间设备、空间事件、空间可视化职责，并与 GlobalCloud Studio 平行；其身份标识 MUST 保持 `SpaceAIStudio`、slug `spaceai-studio`、角色 `external`，且 MUST NOT 与 GlobalCloud Studio 或 GlobalCloud SpaceAI 合并。

#### Scenario: 审查项目定位

- **WHEN** 审查人员读取项目群总体方案与项目状态入口
- **THEN** SpaceAI Studio 以独立项目出现，职责描述为空间层工作台，且不与 Studio、SpaceAI 合并

### Requirement: 多平台技术路线固定为 Web 优先

项目 SHALL 采用 Vue 3 + Naive UI + Tauri 2（桌面壳）+ Node/Koa BFF + Socket.IO 的技术组合，交付 Windows、macOS、Linux 三端桌面应用，并使用单一前端代码库。

#### Scenario: 审查技术选型

- **WHEN** 审查人员检查技术栈声明
- **THEN** 技术栈与 GlobalCloud Studio 同栈，不存在新增的 .NET 技术栈，且目标端明确为三平台桌面

#### Scenario: 验收三平台构建

- **WHEN** 实施推进到 P5
- **THEN** 三个平台各自产出可安装、可在干净环境运行的构建产物并有对应证据

### Requirement: 遗留资产按三类处置且不宣称功能等价

项目 MUST 把遗留资产分为「可迁移」「需重写」「不可用」三类并逐项登记：领域模型转 TypeScript 类型、REST 与 Socket 协议固证为协议包、插件契约重设计为平台无关契约；窗体 UI 与自定义控件 MUST 作为交互需求输入后重写。

#### Scenario: 审查资产处置表

- **WHEN** 审查人员检查迁移面清单
- **THEN** 全部 245 个业务源文件均有归类，且文档中不存在「功能等价迁移」的表述

#### Scenario: P0 协议固证

- **WHEN** P0 完成
- **THEN** REST 端点与 Socket 报文具有规格书，并与原客户端抓包逐条核对一致

### Requirement: 分期实施且每期可验证

项目 SHALL 按 P0 至 P6 分期推进，每期 MUST 产出可验证交付物并把证据归档到 `.harness/runs/`；P0 MUST NOT 依赖技术选型变更。

#### Scenario: 每期收口

- **WHEN** 某一期完成
- **THEN** 该期交付物可复现、有证据，且下一期启动不被阻塞

### Requirement: 状态天花板与人工确认边界

项目状态 MUST 维持 `partial`；MUST NOT 从本地构建、测试或文档完成推断 `accepted`、`integrated`、`production_ready` 或 `customer_accepted`。

#### Scenario: 本地构建通过

- **WHEN** 三平台构建与单元测试通过
- **THEN** 台账只记录开发证据，集成与验收继续保持待确认

### Requirement: 安全与凭据纪律延续

重构 MUST NOT 取消既有凭据排除，MUST NOT 提交凭据、构建产物或 IDE 状态；新增代码 MUST NOT 硬编码端点或 IP，并须清理遗留的硬编码测试 IP 与重复目录代码。

#### Scenario: 检查新增代码

- **WHEN** 提交重构代码
- **THEN** 无凭据、无硬编码端点或 IP、无重复目录残留
