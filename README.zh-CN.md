# Magic App Dev

[English](README.md) | 简体中文

Magic App Dev 是一个个人 Codex 插件，用来打包你在独立 app 开发中沉淀的可复用 skills。它的目标不是记录某个具体 app 的事实，而是沉淀工作流、工程约束和验证习惯。

## 安装

把这个 GitHub 仓库添加为 Codex plugin marketplace：

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

以后仓库更新后，刷新 marketplace 快照并重新安装插件：

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

重新安装后，开启一个新的 Codex 线程来加载更新后的 skills。

本地开发时，也可以在仓库 checkout 中直接安装：

```bash
codex plugin marketplace add .
codex plugin add magic-app-dev@magic-app-dev-plugin
```

## 包含的 Skills

| Skill | 用途 |
| --- | --- |
| `indie-app-demand-research` | 从真实需求信号调研和排序独立 app 方向，避免从想法或技术栈倒推产品。 |
| `local-first-android-app-builder` | 围绕最小 V1 闭环、本地优先、MVI 边界、隐私和验证来启动或审查 Android app。 |
| `android-app-architecture-guardrails` | 约束 Android app 架构：MVI contract、Compose 纯渲染、资源化、设计 token、文件大小和验证门禁。 |
| `android-instrumentation-qa-guardrails` | 用可复现的 adb/instrumentation 证据验证 Android UI 流程，避免人工启动造成假阳性。 |
| `app-change-self-check` | 在交付前按仓库规则、风险分层验证、静态复扫和剩余风险说明来做 app 改动自检。 |
| `app-end-to-end-delivery` | 端到端实现、验证、打包和交付 app feature 或 bug fix。 |
| `github-pr-mainline-release` | 在功能验收后推送分支、创建或复用 PR、等待 CI、安全合并并恢复本地 mainline。 |

## 仓库结构

```text
.agents/
└── plugins/
    └── marketplace.json
plugins/
└── magic-app-dev/
    ├── .codex-plugin/
    │   └── plugin.json
    └── skills/
        └── <skill-name>/
            ├── SKILL.md
            ├── agents/
            │   └── openai.yaml
            └── references/      # 可选
```

所有 skill 的唯一源码都在 `plugins/magic-app-dev/skills/`。

## 维护规则

- skill 目录名必须等于 `SKILL.md` frontmatter 里的 `name`。
- skill 必须能跨 app 复用；不要加入 app 名、包名、私有链接、截图、商店文案或一次性发布事实。
- `SKILL.md` 保持精简。需要按任务条件加载的细节放进 `references/`。
- 插件元信息或版本变化时，更新 `plugins/magic-app-dev/.codex-plugin/plugin.json`。
- 发布前验证：

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/magic-app-dev
python3 /path/to/skill-creator/scripts/quick_validate.py plugins/magic-app-dev/skills/<skill-name>
```

## 边界

这个插件只放独立 app 开发工作流。不要放项目笔记、一次性 PRD、产品文案、品牌资产、密钥或部署凭证。
