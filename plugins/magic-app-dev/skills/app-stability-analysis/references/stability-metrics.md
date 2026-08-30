# App Stability Metrics And Triage Reference

The links and Google Play thresholds below were verified on 2026-08-30. Recheck them before making a current policy, rollout, or discoverability decision.

## Measurement Contract

Record the following before interpreting a chart:

- app name, package or bundle ID, platform, production track, version, build, and rollout date;
- current and comparison windows of equal length, time zone, latest complete date, and current-day completeness;
- Firebase project and app, Crashlytics SDK version or coverage, active event-type filters, and symbolication status;
- Play track, device, OS, country, foreground or background visibility, and other active filters;
- numerator, denominator, identity unit, and whether the value is a rate, unique installations, sessions, issue groups, or events.

## Baseline Metrics

| Priority | Metric | Meaning | Source | Guardrail |
| --- | --- | --- | --- | --- |
| Baseline | Crash-free users | `1 - crashed users / all engaged users` for the selected period. A Crashlytics user is an app installation on a device. | Firebase Crashlytics | Fatal crashes only. It is aggregated over the selected window; longer windows naturally tend to be lower. |
| Baseline | Crash-free sessions | `1 - crashed sessions / all sessions` for the selected period. | Firebase Crashlytics | Fatal crashes only and dependent on supported SDK session reporting. |
| Baseline | Fatal affected users and events | Unique installations with at least one fatal issue, plus fatal event count. | Firebase Crashlytics | Rank primarily by affected users, not events. |
| Baseline | Non-fatal affected users and events | Unique installations and events for recorded non-fatal issues. | Firebase Crashlytics | Non-fatal collection depends on app instrumentation and is not included in crash-free percentages. |
| Baseline | ANR affected users and events | Unique installations and ANR events visible to the selected Firebase population. | Firebase Crashlytics | Android 10 and lower ANRs may require Play Console coverage. |
| Baseline | New, regressed, increasing, and velocity issues | Issue groups whose lifecycle or event velocity signals a recent change. | Firebase Crashlytics | Validate the affected version and first-seen time; a label alone does not prove release causality. |
| Baseline | User-perceived crash rate | Percentage of daily users who experienced at least one foreground user-perceived crash. | Google Play Android vitals | Play-installed, diagnostics-sharing eligible population; not directly comparable to Crashlytics crash-free users. |
| Baseline | User-perceived ANR rate | Percentage of daily users who experienced at least one user-perceived ANR. | Google Play Android vitals | A core vital that can affect discoverability. |
| Baseline | Critical issues and anomalies | Play flags for threshold breaches, sharp changes, or device-specific quality problems. | Google Play Android vitals | “No issue” may mean insufficient eligible data; inspect the displayed data state. |
| Diagnostic | Overall ANR and multiple-ANR rates | Daily-user share with any ANR or at least two ANRs. | Google Play Android vitals | Use to detect hidden ANRs and repeated loops beyond the core user-perceived rate. |

Firebase definitions: [Crash-free metrics](https://firebase.google.com/docs/crashlytics/crash-free-metrics). Google Play definitions: [Android vitals](https://support.google.com/googleplay/android-developer/answer/9844486) and [Crashes and ANRs](https://support.google.com/googleplay/android-developer/answer/9859174).

## Current Google Play Guardrails

For phone apps, Google Play currently documents these bad-behavior thresholds:

- overall user-perceived crash rate: **1.09%** of daily users;
- per-phone-model user-perceived crash rate: **8%** of daily users on that model;
- overall user-perceived ANR rate: **0.47%** of daily users;
- per-phone-model user-perceived ANR rate: **8%** of daily users on that model.

Google Play generally considers the preceding 28 days but may respond sooner to spikes. A value below a store threshold can still be a serious release regression, startup failure, purchase failure, or small-cohort incident.

## Issue Triage Fields

For every issue that could change the verdict, collect:

- Firebase or Play issue identifier and displayed title;
- fatal, non-fatal, ANR, foreground, or background classification;
- affected users, event count, affected share when derivable, and comparison change;
- first seen, last seen, recency, regression state, and velocity or anomaly signal;
- app versions, builds, Play tracks, rollout exposure, devices, OS versions, and countries;
- exception type and message or ANR signature;
- top in-app stack frame, thread state for ANRs, and full-symbolication status;
- breadcrumbs, custom keys, logs, preceding analytics events, and related release or dependency changes;
- reproduction status and the smallest missing evidence needed to confirm root cause.

Do not paste a full stack trace into the final report when an exception, top in-app frame, and concise call-chain summary answer the decision.

## Prioritization

Use this order:

1. Official threshold breach, critical issue, or sharp production anomaly.
2. New or regressed issue tied to the current rollout.
3. Startup, data-loss, save/commit, purchase, security, or other high-consequence path.
4. Largest affected-user count or affected share.
5. Increasing velocity or widespread version, device, or OS coverage.
6. Repeated event loop affecting few users.
7. Stable, old, low-impact issue.

Event count is a recurrence signal, not a substitute for affected users.

## Verdict Vocabulary

- **No material signal observed:** no issue is visible in the inspected eligible population and complete window; keep data-coverage caveats.
- **Monitor:** a low-impact or uncertain signal exists, but current evidence does not justify rollout intervention.
- **Investigate before wider rollout:** a new or regressed issue is plausibly release-linked or affects a critical path.
- **Urgent mitigation:** a threshold breach, widespread spike, severe critical-path failure, or data-loss risk requires immediate release action.

Every verdict must name the evidence that would cause it to move up or down one level.
