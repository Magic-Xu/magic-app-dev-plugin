# Magic App Dev

[English](README.md) | 简体中文

Magic App Dev 是一个用于 app 开发工作流的 Codex 插件，覆盖选题验证、本地优先 Android 开发、架构审查、设备 QA、改动自检、交付和 GitHub 发布流程。

## 安装

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

安装后开启一个新的 Codex 线程。

## 更新

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

更新后开启一个新的 Codex 线程。

## 开发

需要查看源码、修改、fork 或贡献插件时，再使用本地 checkout。

```bash
git clone https://github.com/Magic-Xu/magic-app-dev-plugin.git
cd magic-app-dev-plugin

codex plugin marketplace add .
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Skill 源码位于 `plugins/magic-app-dev/skills/`。

## Skills

| Skill | 用途 |
| --- | --- |
| `indie-app-demand-research` | 从真实需求信号调研和排序 app 机会。 |
| `local-first-android-app-builder` | 规划、启动或审查本地优先 Android app。 |
| `android-app-architecture-guardrails` | 约束 Android 代码的 MVI、Compose、资源和验证门禁。 |
| `android-instrumentation-qa-guardrails` | 用可复现的 adb/instrumentation 证据验证 Android UI 流程。 |
| `app-change-self-check` | 交付前用具体证据检查 app 改动。 |
| `app-end-to-end-delivery` | 端到端实现、验证、打包和交付 app feature 或 bug fix。 |
| `github-pr-mainline-release` | 推送已验收改动、创建或复用 PR、等待 CI、合并并恢复 mainline。 |

## 结构

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
            └── references/
```
