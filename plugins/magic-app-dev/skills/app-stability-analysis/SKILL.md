---
name: app-stability-analysis
description: Diagnose a released app's crashes, non-fatal errors, ANRs, regressions, and release stability from Firebase Crashlytics and app-store quality data. Use when the user asks whether an app is crashing, requests a recent Crashlytics or Android vitals review, wants the highest-impact issue or affected versions and devices, or needs a release stability assessment. Do not use for general growth and revenue reporting unless stability is the main question.
---

# App Stability Analysis

## Outcome

Determine whether users are experiencing a material stability problem, identify the smallest evidence-backed issue set that explains it, and prioritize root-cause investigation by user impact and release risk.

Read [references/stability-metrics.md](references/stability-metrics.md) before a full crash or ANR review. Recheck linked platform thresholds when they can affect a release or store-discoverability decision.

## Access And Authority

- Analyze live console data read-only. Do not close, mute, assign, delete, or change the state of an issue; change alerts; upload symbols or mappings; or alter collection settings unless the user explicitly asks.
- Prefer an available first-party connector or reporting API. When none can access the authenticated project and the user requested or approved browser use, use the browser skill with their logged-in Firebase and Play Console session.
- Verify app name, package or bundle ID, platform, production track, version, and account before using a dashboard. Avoid mixing debug, internal-test, and production builds unless the user asks for that comparison.
- If browser control, permission, or data coverage blocks a source, report the limitation. Do not silently substitute screenshots, another project, or a different quality source.
- Stack traces, custom keys, logs, user IDs, and breadcrumbs may contain private data. Quote only the minimum technical evidence required for diagnosis.

## Required Sources

- Firebase Crashlytics is the primary source for fatal and non-fatal issue groups, affected installations, sessions, regressions, versions, stack traces, breadcrumbs, and custom keys.
- Google Play Android vitals is required for Android production reviews because it provides user-perceived crash and ANR rates, foreground clusters, device-specific bad behavior, and Play discoverability impact.
- Use both sources when available. Their populations and event semantics differ, so disagreement is diagnostic evidence rather than a reason to average them.

## Workflow

1. Establish comparable scope.
   - Record the app identity, latest production version and rollout date, requested window, preceding comparison window, time zone, latest complete data date, build or track filters, and Crashlytics SDK coverage.
   - Default “recent” to the latest complete 7 days versus the preceding 7 days for incident detection, plus a 28-day view for baseline. Use the release boundary when the question concerns a rollout.

2. Read the stability overview.
   - Collect every Baseline metric in the reference, including rows that display zero, no data, insufficient data, or unavailable.
   - Report counts alongside percentages. Crash-free percentages are meaningful only with their window and sample size.
   - Check Firebase fatal, non-fatal, and ANR surfaces separately; crash-free charts cover fatal crashes only.

3. Detect the release or incident signal.
   - Compare the same metric, window length, app population, and filter set.
   - Look for new, regressed, increasing, velocity-alerted, or release-specific issues; spikes in affected users; startup or core-flow failures; and concentration by version, device, OS, or Play track.
   - In Android vitals, inspect both overall and per-device user-perceived rates and any critical-issue or anomaly flag.

4. Triage by users and user journey.
   - Rank issue groups first by affected users and affected share, then by recurrence, trend, critical-path location, regression status, and rollout exposure.
   - Do not rank solely by raw event count: one user in a crash loop can generate many events.
   - Treat startup, import/open, save/commit, purchase, and data-loss paths as higher consequence when supported by stack or breadcrumb evidence.

5. Deep-dive only the issues that can change the decision.
   - Capture issue title and ID, fatal/non-fatal/ANR type, exception or ANR signature, affected users, events, first and last seen, versions, devices or OS, top in-app frame, and whether symbolication is complete.
   - Use stack traces, breadcrumbs, logs, custom keys, and recent code or dependency changes to form a root-cause hypothesis.
   - Separate observed evidence from inference. Name the missing artifact or reproduction that would confirm the hypothesis.

6. Make the release decision explicit.
   - State whether the data supports “no material signal,” “monitor,” “investigate before wider rollout,” or “urgent mitigation.”
   - Use official Play bad-behavior thresholds as guardrails, not as permission to ignore a severe lower-volume regression.
   - Recommend the narrowest next action: reproduce, inspect a specific code path, compare one version, halt or slow a rollout when authorized, or add missing diagnostics in a later code task.

## Required Report Shape

1. **Verdict:** one sentence answering whether a material stability problem exists.
2. **Scope and coverage:** app, versions or tracks, windows, latest complete dates, filters, SDK or symbolication caveats, and unavailable sources.
3. **Stability table:** current, previous, change, numerator and denominator, source, and status for each baseline metric.
4. **Prioritized issues:** affected users, event count, trend, versions or devices, critical path, evidence, and confidence.
5. **Decision and actions:** severity, immediate action, owner-independent validation, and the metric or issue state that would show recovery.

If no issue is visible, say “no issue observed in the inspected population and window,” not “the app has no crashes.”

## Hard Boundaries

- Do not treat “no data” or a privacy-threshold blank as zero crashes.
- Do not compare crash-free user percentages across different window lengths.
- Do not infer unique affected users from event totals.
- Do not declare a root cause from an exception title alone.
- Do not omit ANRs just because Crashlytics shows no fatal crashes.
- Do not apply a code fix during a diagnostic-only request. Hand off a concrete implementation target when the user asks for the fix.
