# Magic App Dev

English | [简体中文](README.zh-CN.md)

Magic App Dev is a Codex plugin for app development workflows: idea validation, local-first Android development, architecture review, device QA, change self-checks, delivery, and GitHub release work.

## Install

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Open a new Codex thread after installing.

## Update

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Open a new Codex thread after updating.

## Develop

Use a local checkout when you want to inspect, edit, fork, or contribute to the plugin.

```bash
git clone https://github.com/Magic-Xu/magic-app-dev-plugin.git
cd magic-app-dev-plugin

codex plugin marketplace add .
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Skill source lives in `plugins/magic-app-dev/skills/`.

## Skills

| Skill | Purpose |
| --- | --- |
| `indie-app-demand-research` | Research and rank app opportunities from real demand signals. |
| `local-first-android-app-builder` | Plan, bootstrap, or review focused local-first Android apps. |
| `android-app-architecture-guardrails` | Keep Android code modular across MVI, Compose, resources, and validation gates. |
| `android-instrumentation-qa-guardrails` | Validate Android UI flows with reproducible adb/instrumentation evidence. |
| `app-change-self-check` | Check app changes before handoff with concrete validation evidence. |
| `app-end-to-end-delivery` | Implement, validate, package, and hand off app features or bug fixes. |
| `github-pr-mainline-release` | Push accepted work, open or reuse a PR, apply the configured-CI or no-CI validation gate, squash merge when appropriate, clean up the source branch, and restore mainline. |

## Layout

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
