# Magic App Dev

English | [简体中文](README.zh-CN.md)

Magic App Dev is a Codex plugin for independent app development workflows: idea validation, product and stability analytics, paired Android/legal workspace creation, local-first Android development, architecture review, Android device setup and QA, change self-checks, delivery, and GitHub release work.

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
| `app-product-analytics` | Analyze live acquisition, installed audience, activity, retention, product funnels, monetization, store conversion, and top-level quality, then deliver a verified Lark report. |
| `app-stability-analysis` | Diagnose live crashes, non-fatal errors, ANRs, regressions, and release stability, then deliver a verified Lark report. |
| `android-app-factory` | Create a paired private-ready Android repository and public-ready GitHub Pages legal repository. |
| `local-first-android-app-builder` | Plan, bootstrap, or review focused local-first Android apps. |
| `android-app-architecture-guardrails` | Keep Android code modular across MVI, Compose, resources, and validation gates. |
| `android-device-keep-awake` | Keep one connected Android device awake on its active charging source during an explicitly requested long development task. |
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
            ├── scripts/
            └── references/
```
