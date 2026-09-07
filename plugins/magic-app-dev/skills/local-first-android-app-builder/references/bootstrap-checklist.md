# Android App Kickoff

Use when turning a product idea into a buildable V1. Reuse accepted product facts and the target repository's
layout; this reference does not prescribe files that every app must create.

## Product And Data Decisions

Describe the user, job, shortest complete loop, required capabilities, and meaningful scope exclusions.
Identify local storage, export, network transmission, telemetry, and deletion behavior for the data involved.
Choose acceptance evidence for the loop and its most consequential failure paths.

Start with the largest uncertainty that can change feasibility or product value. A platform capability spike,
domain prototype, or UI flow may each be the appropriate first step. Add monetization, accounts, cloud sync,
or automation when the accepted loop requires them.

## Artifact Placement

Update the existing authoritative documents. In Factory workspaces, follow the generated layout contract:

| Purpose | Location |
| --- | --- |
| Current product scope and behavior | `docs/product/` |
| Current engineering and validation rules | `docs/engineering/` |
| Operator procedures | `docs/operations/` |
| Durable architectural decisions | `docs/decisions/` |
| Editable visual sources and design previews | `design/` |
| Executable helpers | `tools/` |
| Legal, store, and website publishing inputs | `publishing/` |
| Reproducible screenshots, logs, and build output | ignored `build/` |

Keep repository-wide agent instructions in `AGENTS.md`, linking to maintained sources when needed. Do not create
parallel copies of requirements or engineering rules. Existing repositories may have different valid layouts;
do not migrate them as a side effect of product planning.

## Workspace Creation

For Magic Android workspaces, use `$android-app-factory`. Its generator owns the paired repositories, Platform
baseline, locale set, layout gate, and initial build acceptance. Do not reproduce its template here.

For an existing app, extend the established structure. Split Gradle modules when build speed, ownership, reuse,
or dependency enforcement justifies the cost. Add only the state and platform boundaries needed by the core loop.
