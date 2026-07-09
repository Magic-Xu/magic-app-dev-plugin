# Magic App Dev

English | [简体中文](README.zh-CN.md)

Magic App Dev is a personal Codex plugin that packages reusable skills from independent app development work. The plugin is intentionally product-agnostic: it captures workflows, guardrails, and validation habits, not facts from one specific app.

## Install

For normal use, install directly from the GitHub marketplace. You do not need to clone the repository.

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Start a new Codex thread after installing so the plugin skills are loaded.

## Update

The plugin does not update automatically when this GitHub repository changes. Refresh the marketplace snapshot and reinstall the plugin:

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Start a new Codex thread after reinstalling so updated skills are loaded.

## Develop From A Local Checkout

Clone the repository only when you want to inspect the source, edit skills, fork it, or contribute changes.

```bash
git clone https://github.com/Magic-Xu/magic-app-dev-plugin.git
cd magic-app-dev-plugin

codex plugin marketplace add .
codex plugin add magic-app-dev@magic-app-dev-plugin
```

The source of truth for the skills is `plugins/magic-app-dev/skills/`.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `indie-app-demand-research` | Research and rank indie app opportunities from real demand signals before building. |
| `local-first-android-app-builder` | Start or review focused local-first Android apps around a small V1 loop, MVI boundaries, privacy, and validation. |
| `android-app-architecture-guardrails` | Keep Android app code modular through MVI contracts, Compose purity, resources, design tokens, file-size checks, and validation gates. |
| `android-instrumentation-qa-guardrails` | Validate Android UI flows with reproducible adb/instrumentation evidence instead of manual launches. |
| `app-change-self-check` | Self-check app changes before handoff with repository rules, risk-based validation, static rescans, and explicit residual risks. |
| `app-end-to-end-delivery` | Implement, validate, package, and hand off an app feature or bug fix end to end. |
| `github-pr-mainline-release` | Push accepted work, create or reuse a PR, wait for CI, merge safely, and restore local mainline. |

## Repository Layout

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
            └── references/      # optional
```

## Maintenance

- Keep each skill directory name equal to its `SKILL.md` frontmatter `name`.
- Keep skills reusable across apps; do not add app names, package names, private URLs, screenshots, store listings, or one-off release facts.
- Keep `SKILL.md` concise. Move conditional detail into `references/`.
- Update `plugins/magic-app-dev/.codex-plugin/plugin.json` when the plugin metadata or version changes.
- Validate before publishing:

```bash
python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/magic-app-dev
python3 /path/to/skill-creator/scripts/quick_validate.py plugins/magic-app-dev/skills/<skill-name>
```

## Scope

This plugin is for independent app development workflows. It is not a place for project notes, app-specific PRDs, product copy, brand assets, secrets, or deployment credentials.
