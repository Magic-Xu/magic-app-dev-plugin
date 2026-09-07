# Project Context And Stage Handoffs

Use when multiple stages or future tasks need the same product context. Keep facts in the app's own
repository, using its existing documentation index or operations document as a small **source map**.
Link authoritative files instead of copying their contents. For Factory apps, extend `docs/README.md`.
For existing apps, retain their established structure. A small fix does not require a new context document.

## Resolve Only What The Task Needs

| Concern | Source to locate |
| --- | --- |
| Identity | App name, package/bundle ID, owning app/legal/Platform repositories; actual console project and links when configured |
| Product truth | Current behavior, core loop, scope/exclusions, accepted requirements, data flows and commercial model |
| Design | Current editable UI/brand/store sources, approval evidence, rendering/capture instructions |
| Engineering | Actual architecture, branch/worktree policy, build/version/signing configuration references, required CI/device gates |
| Market coverage | App UI languages, store listing locales/overrides, and distribution countries as separate sets |
| Publication | Binary and store baselines independently; draft/submitted/live status with observation source and time |
| Measurement | Product-value outcome, existing event/metric definitions, authorized data sources, report destination and verification window |
| Authority | Accepted design scope, code integration and store write boundaries, final owner actions |

Secret values, login tokens, phone serials, browser tab IDs and local cache paths do not belong in the
shared plugin or public/legal repository. Reference existing secret/configuration providers without
copying secrets. Console access and remote creation remain subject to the user's requested scope.

## Keep Facts And Evidence Distinct

Requirements express intended behavior; code and appropriate device evidence establish implementation;
Console establishes publication status. Reconcile discrepancies before changing product meaning. A
generation spec describes the initial scaffold and is not proof of the app's current SDKs or data flows.
An unconfigured integration stays unconfigured; do not create accounts, tracking or external documents
just to complete a source map.

Record a useful stage handoff in the existing requirement, issue or release record, referencing:

- Accepted outcome and exclusions; relevant design approval and its scope.
- Source baseline/candidate and owning branch/worktree, plus included uncommitted changes if relevant.
- Completed evidence with its inputs, environment and coverage; unresolved findings or decisions.
- Actual current external state and the next requested or owner action.
- For product experiments, the original hypothesis, metric and observation window.

Do not duplicate a full report, create a new management database, or archive stale parallel copies.
When resuming, recheck volatile external state and evidence affected by changed inputs; reuse stable
facts and still-valid checks. Update a live release pointer only after publication is established.
