# Magic App Dev

English | [简体中文](README.zh-CN.md)

Reusable Codex workflows across products: demand research → product planning and design approval → Android implementation and verification → mainline integration → first launch / release updates → analytics and stability → iteration outcome verification. Start at the requested stage; ordinary tasks do not run the entire lifecycle.

## Install and update

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

For later updates:

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

Start a new Codex task after installation or updating to load the current plugin.

## Choose a workflow

All display names use **Magic · 中文任务名**. Invoke the English IDs listed below as `$<skill-id>`. Picker search matching is controlled by the Codex client.

- Start with **Magic · 开发与迭代** when you do not know which specialist fits.
- Use **Magic · 版本发布审查与修复** before Google Play release to review cumulative requirements, feature interactions, architecture, implementation and release evidence. Ask for review and repair to fix confirmed in-scope defects and remove proven obsolete content; review-only requests remain read-only.
- Use **Magic · Google Play 发版** for AAB uploads, version notes, first launch or store-only changes. Version updates assess whether the store needs no, partial or full refresh.
- Use product or stability analysis to verify a shipped iteration against its original metric, baseline and observation window.

| Display name | Stable invocation ID | Purpose |
| --- | --- | --- |
| Magic · 需求调研 | `indie-app-demand-research` | Validate demand and distribution evidence and select the next validation decision. |
| Magic · 产品规划 | `local-first-android-app-builder` | Define the user loop, scope, data/commercial boundaries, design inputs and acceptance. |
| Magic · 创建项目 | `android-app-factory` | Generate and validate paired Android/legal repositories with a product-design review policy. |
| Magic · 开发与迭代 | `app-end-to-end-delivery` | Start here when the stage or specialist is unclear; coordinate only the requested lifecycle work. |
| Magic · 真机验证 | `android-instrumentation-qa-guardrails` | Prove Android interactions, system boundaries and lifecycle behavior with reproducible evidence. |
| Magic · 设备常亮 | `android-device-keep-awake` | Keep a specified device awake only when explicitly requested; preserve restoration state. |
| Magic · 版本发布审查与修复 | `app-release-review` | Review the whole release, reconcile requirements and implementation, repair authorized defects and verify readiness; also supports explicitly scoped checks. |
| Magic · 合并主干 | `github-pr-mainline-release` | Integrate accepted work through applicable PR/CI gates, synchronize mainline and clean up precisely. |
| Magic · Google Play 发版 | `google-play-release` | Prepare first launch, AAB updates or store-only changes; assess None/Partial/Full refresh and hand off verified drafts. |
| Magic · 产品数据分析 | `app-product-analytics` | Analyze acquisition, retention, funnels and monetization, including iteration outcomes and configured report delivery. |
| Magic · 稳定性分析 | `app-stability-analysis` | Diagnose crashes, ANRs and release regressions, and verify recovery after a fix. |

## Adopt in a project

Reuse the existing documentation index as a small source map linking product truth, editable design, engineering gates, release/store records and metrics. Factory seeds this index and a design-review policy in new projects. Existing projects adopt what they need without automatic directory migration or rule rewrites.

Product exclusions, monetization/ads, data flows, languages/countries, build scripts and submission authority stay project-owned. The plugin contains no app-specific account, package, device or capture assets. Use the [project context contract](plugins/magic-app-dev/skills/app-end-to-end-delivery/references/project-context.md) and [iteration outcomes](plugins/magic-app-dev/skills/app-end-to-end-delivery/references/iteration-outcomes.md) for necessary handoffs without a parallel management system.

Review concrete user-visible designs before implementing them. Audits and analyses do not themselves authorize code changes. Integration, Console writes and publication use their respective authorization. By default, the owner reviews changed store design/copy and performs final review submission and publication on every Google Play track. A planned observation window does not create a scheduled task.

Report delivery follows the user/project destination, retaining Lark as the unconfigured default. Document tools and optional artifact-review skills are not bundled. Check availability, complete independent analysis when delivery is blocked, and do not claim a local draft fulfills an agreed external report.

## Develop and validate

```bash
git clone https://github.com/Magic-Xu/magic-app-dev-plugin.git
cd magic-app-dev-plugin
```

Maintain source in a Git checkout and distribute accepted versions through GitHub `main`. The installed marketplace stays on the GitHub source from “Install and update”; local edits and feature branches become available only after integration and a plugin update. Do not register the development directory as the normal update source.

Source is under `plugins/magic-app-dev/skills/`. Entrypoints retain routing and essential constraints; implementation, design, version audit and first-launch details load only when needed. Release review owns requirement reconciliation, architecture/state guidance, repair and risk-based verification in one workflow; focused development checks reuse its references.

```bash
python3 -m pip install -r tools/plugin/requirements.txt
python3 -B -m unittest discover -s tools/plugin/tests -p 'test_*.py'
python3 -B tools/plugin/validate_skills.py plugins/magic-app-dev
python3 -B tools/plugin/validate_release.py --repo-root . --plugin-root plugins/magic-app-dev --base-ref origin/main
```

Package CI checks metadata, naming, default invocations, local links, named skill references and release version progression. Factory output changes additionally require its full generation/build acceptance.

The [workflow scenario review](tools/plugin/workflow-scenarios.md) supplies behavioral evaluation fixtures and criteria for new products, routine fixes, major UI changes, version audits, first launches, store-only updates, resumption, analysis and outcome checks. Passing static lint is not a passing model-behavior evaluation.
