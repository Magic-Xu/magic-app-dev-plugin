---
name: local-first-android-app-builder
description: 产品规划：定义 Android 产品的用户闭环、版本范围、数据与收费边界、设计验收和效果指标。Plan a local-first product before design or project creation; this skill does not generate a workspace.
---

# Android Product Planning

Turn an idea or next-version objective into a small, complete user loop and buildable acceptance scope.
The stable skill ID is retained for existing callers; project generation belongs to Android App Factory.
Reuse accepted decisions when continuing an existing product.

## Define The Product Decision

Resolve the user and job, shortest path to useful value, current-version inclusions/exclusions, important
failure/recovery behavior, and system capabilities. Distinguish evidence of demand from product hypotheses.
For uncertain demand, use [需求调研](../indie-app-demand-research/SKILL.md) for the relevant question.

Specify local storage, exports/transmissions, logging/telemetry, deletion, offline behavior and operating
cost boundaries. Keep sensitive content out of logs. The core loop should not depend on ancillary ads,
analytics or monitoring. Network-dependent features follow the accepted offline contract.

Clarify free/paid entitlement, ads, trial/restore behavior and account requirements only when applicable;
do not infer them from a competitor or add them to every V1. Changes to actual data collection require
aligned implementation, privacy/legal sources and store declarations before publication.

Define acceptance in user outcomes and consequential failure paths. For a product hypothesis, select an
existing metric/baseline, success criterion and observation window using
[iteration outcomes](../app-end-to-end-delivery/references/iteration-outcomes.md). Missing measurement is
not permission to introduce tracking. A maintenance fix can use functional acceptance alone.

Ask when missing information changes product meaning, permissions, data handling or the deliverable.
Routine implementation choices follow the repository. Record only durable accepted facts in their
existing sources, with open decisions clearly separated; do not duplicate a product framework per task.

## Continue To The Requested Stage

- Use [kickoff context](references/bootstrap-checklist.md) for scope and source placement.
- Use [design and acceptance](../app-end-to-end-delivery/references/design-and-acceptance.md) for visible
  changes; obtain required design approval before feature implementation.
- Use [repository rules](references/repo-rules-template.md) when authoring project-specific instructions.
- Use [创建项目](../android-app-factory/SKILL.md) for a new paired Android/legal workspace.
- Use [implementation delivery](../app-end-to-end-delivery/references/implementation-delivery.md) for an
  accepted implementation request. Architecture and MVI guidance belong to
  the release-review [architecture reference](../app-release-review/references/architecture-and-implementation.md);
  reuse that guidance without starting a release audit during planning.

A planning-only task ends with a concrete plan and decisions. An implementation request continues after
product decisions and required design approval; do not reopen established scope or generate a new app
for an existing project.
