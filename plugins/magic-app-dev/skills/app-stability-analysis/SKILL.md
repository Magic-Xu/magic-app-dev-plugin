---
name: app-stability-analysis
description: 稳定性分析：诊断 Crash、ANR、版本回归及修复后的恢复效果；基于 Crashlytics 与商店质量数据，按项目约定交付报告。
---

# App Stability Analysis

Determine whether users face a material stability problem, identify the issues that explain it, and prioritize
investigation by user impact and release risk. Separate observed evidence from root-cause hypotheses.

## Select The Analysis Scope

- For a full stability review, read [references/stability-metrics.md](references/stability-metrics.md) and collect
  every Baseline row, marking platform-inapplicable rows accordingly. Full Android production reviews require both
  Crashlytics and Google Play Android vitals. Record unavailable sources and their effect on the verdict.
- For a specific issue, version comparison, or a diagnostic contribution to an operating review, read the relevant
  reference sections and collect the affected issue and population evidence. Broaden only when findings require it.
- A conceptual stability explanation does not require live data or a new document.

Reuse the current app identity, versions/tracks, rollout boundary, windows, filters, time zone, latest complete
source dates, and SDK/symbolication coverage when still valid. For an unspecified recent full review, use the
latest complete 7 days versus the preceding 7, with a 28-day baseline. Use the release boundary for rollout questions.
Recheck official Play thresholds when they affect a release or discoverability decision.

## Source And Authority

Crashlytics provides issue groups, affected installations, sessions, versions, traces, and breadcrumbs. Play vitals
provides user-perceived rates, ANR coverage, device-specific quality, and store impact for its eligible population.
Use the sources needed for the requested scope; differences in population or event semantics must be explained.
A focused Crashlytics diagnosis alone does not establish overall Android production or Play health.

Analyze source systems read-only. Do not close, mute, assign, or delete issues, change alerts or collection, upload
symbols, or change rollout state without the corresponding user request. Prefer connectors or APIs; use available
browser tools with the user's authorized project session when needed, reusing existing authorization. Ask before
changing accounts, data sources, access scope, or deliverables; a different reading method within the same authorized
source and session is a technical choice. Report unavailable evidence and continue independent diagnosis.

Verify app/package, platform, account, and build/track coverage. Keep production and test populations distinct.
Traces, logs, custom keys, IDs, and breadcrumbs may contain private data; include only the diagnostic evidence needed.

## Diagnose

1. Establish comparable evidence for the question: counts with rates, equal windows and filters, and the relevant
   fatal, non-fatal, or ANR surfaces. A full review covers all three; crash-free metrics cover fatal crashes only.
2. Check new or regressed issues, affected-user trends, release exposure, startup/core-flow failures, and version,
   device, or OS concentration. Inspect overall and per-device Play rates when store quality is in scope.
3. Prioritize severe user consequences and release regressions alongside affected-user count/share and recurrence.
   Event count alone can over-rank one installation in a crash loop. Use the reference's triage criteria as needed.
4. For issues that can change the decision, capture identity, type/signature, users/events, first/last seen,
   versions/devices, top in-app frames, and symbolication coverage. Use traces, breadcrumbs, logs, and relevant
   implementation changes to form a hypothesis; state the missing evidence or reproduction needed to confirm it.
5. Recommend the narrowest next action and evidence of recovery. Distinguish monitoring, investigation before wider
   rollout, and urgent mitigation. A store threshold is a guardrail, not a reason to ignore a severe smaller regression.

## Report And Deliver

Lead with the verdict for the inspected population and window. Include scope/coverage; relevant metric values and
comparisons with denominators; prioritized issues, evidence, confidence, and gaps; and actions with recovery criteria.
Full reviews retain every Baseline row, including unavailable data with reasons. Focused reports contain only what
supports the requested diagnosis. Say "no issue observed in the inspected population and window" when appropriate.

When contributing to `$app-product-analytics`, return findings and evidence to that analysis for its combined report.
For a standalone completed analysis based on live or user-supplied app data, follow the shared
[report delivery](../app-product-analytics/references/report-delivery.md) with title
`<App> 稳定性分析｜<analysis end date>` or the reader's language.

For release recovery checks, use the original issue signature, affected versions/population and recovery
criteria from the [iteration record](../app-end-to-end-delivery/references/iteration-outcomes.md). Verify
actual exposure and source latency before judging the fix; do not equate upload with recovery.

## Evidence Boundaries

- Missing, suppressed, or insufficient data is unknown, not zero crashes.
- Compare crash-free percentages only across compatible windows and populations.
- Event totals do not establish unique affected users, and exception titles alone do not establish root causes.
- No fatal crashes does not establish no ANRs; inspect ANRs whenever the requested stability verdict includes them.
- A diagnostic request does not authorize a code fix. Continue into implementation when the user requests it.
