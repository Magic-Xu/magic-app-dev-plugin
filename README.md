# App Development Skills

English | [简体中文](README.zh-CN.md)

Reusable Codex skills extracted from app development work. The skills in this repository should stay product-agnostic: they may encode strong engineering workflows, but they must not depend on one app's name, package, repository, screenshots, store listing, or release history.

## Skill Selection Criteria

A skill belongs here only when it is:

- reusable across multiple apps
- specific enough to change agent behavior
- small enough to load without wasting context
- free of app-specific product facts
- backed by a repeated workflow or a real failure mode

Do not add project notes, one-off PRDs, product copy, brand assets, or app-specific release checklists as skills.

## Skills

| Skill | Purpose |
| --- | --- |
| `android-app-architecture-guardrails` | Keep Android app code modular: MVI contracts, Compose purity, resources, design tokens, file-size checks, and validation gates. |
| `android-instrumentation-qa-guardrails` | Validate Android connected-device UI flows with reproducible adb/instrumentation evidence instead of manual launches. |
| `github-pr-mainline-release` | Push an accepted feature branch, create or reuse a PR, wait for GitHub Actions CI, merge safely, and restore local mainline. |
| `local-first-android-app-builder` | Bootstrap a focused local-first Android app around a small V1 loop, clear non-goals, MVI/pulse/Compose boundaries, privacy, and validation. |

## Local Install

Install a skill globally by linking or copying its folder into:

```bash
~/.codex/skills/
```

Example:

```bash
ln -s /path/to/app-dev-skills/android-app-architecture-guardrails ~/.codex/skills/android-app-architecture-guardrails
```

This repository is intended to be the source of truth; global installs can point back to folders in this repo.

## Repository Layout

Each skill lives at the repository root:

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/      # optional
```

Keep `SKILL.md` concise. Put task-specific detail in `references/` only when it should be loaded conditionally.

## Maintenance Rules

- Keep frontmatter `name` equal to the folder name.
- Keep descriptions broad enough to trigger correctly, but not so broad that unrelated tasks load the skill.
- Keep `agents/openai.yaml` default prompts aligned with the skill name.
- Remove app names, package names, repository names, private URLs, and release-only details before committing.
- Validate a new or changed skill before publishing.
