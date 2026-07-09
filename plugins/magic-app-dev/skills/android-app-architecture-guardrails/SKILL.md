---
name: android-app-architecture-guardrails
description: Use when implementing, refactoring, or reviewing Android app code where maintainability matters; enforces role-based decomposition, MVI/contract hygiene, Compose UI purity, resource/i18n discipline, file-size limits, utility extraction, and validation gates. Business/domain agnostic and suitable for any Android app.
---

# Android App Architecture Guardrails

## Overview

Use this skill before adding, refactoring, or reviewing Android app code that can affect architecture, UI structure, state flow, platform calls, resources, or long-term maintainability. Prefer the target repository's own rules when they are stricter.

## Workflow

1. Inspect local context before editing:
   - Read `AGENTS.md`, `docs/engineering/`, active feature docs, and nearby files.
   - Find existing patterns for MVI, Compose routing, design tokens, resources, tests, and platform gateways.
   - Check file sizes with `rg --files -g '*.kt' | xargs wc -l | sort -nr`.

2. Define the responsibility boundary:
   - `ui`: Compose rendering and event dispatch only.
   - `presentation`: ViewModel, reducer, intent/effect handling, state mapping.
   - `contract`: public page state, intents, effects, UI-facing enums.
   - `domain`: pure business rules, models, algorithms, render engines.
   - `data` or platform/core gateways: file IO, pickers, sharing, permissions, external navigation, SDK calls.
   - `core/designsystem` and `core/ui`: tokens and reusable UI primitives.
   - `core/common`: business-agnostic utilities.

3. Refactor by moving behavior to its owner:
   - Move system calls out of Composables into gateways, handlers, or app-level effect coordinators.
   - Move pure conversions and calculations into named mapper/util files.
   - Move repeated UI controls into reusable components.
   - Keep app shells focused on dependency wiring, route switching, and cross-page effects.
   - Do not introduce new dependencies unless the task truly requires them.

4. Keep MVI and Compose clean:
   - New pages define `XxxContract`, `XxxState`, `XxxIntent`, `XxxEffect`, and `XxxViewModel` first.
   - Composables receive state and callbacks; they do not decide navigation, call SDKs, read/write files, or mutate repositories directly.
   - One-off commands such as navigation, picker open, save, share, or toast should be modeled as effects or handled by a route/effect coordinator.

5. Control file and component size:
   - Any Kotlin/Compose file over 800 lines must be split before completion.
   - Treat files over 400 lines as review hotspots; split if the file mixes responsibilities.
   - Split Compose screens by role: route/screen shell, top bar, content/preview, controls, dialogs/sheets, rows/chips.
   - Prefer a small named file over private helper piles inside a large screen.

6. Enforce resources and design tokens:
   - All user-visible strings go through Android string resources.
   - When a repo supports multiple locales, update every supported `values-*` directory together.
   - Do not hardcode colors, spacing, radius, or typography in formal page code when a token exists.
   - If a repeated value has no token, add a narrow token or local component constant instead of scattering literals.

7. Validate before finishing:
   - Run the narrowest useful compile/test command.
   - Re-run file-size checks.
   - Search for hardcoded UI text, direct platform calls in UI, and duplicate helpers.
   - Update `docs/engineering/` or `docs/decisions/` when adding a new rule, boundary, or architectural decision.

## Review Checklist

- Does every changed file have one primary responsibility?
- Are UI, state, domain, and platform boundaries still separate?
- Are new utilities business-agnostic and placed outside feature packages when reusable?
- Are page contracts updated before UI behavior changes?
- Are strings localized and visual values tokenized?
- Are all changed files below 800 lines?
- Did verification run, and are remaining risks explicit?
