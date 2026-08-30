---
name: app-product-analytics
description: Analyze a released app's acquisition, installed audience, activity, retention, product funnel, monetization, store conversion, and top-level quality using authoritative console data. Use when the user asks for an app KPI review, growth diagnosis, recurring operating report, Firebase or Google Play analysis, user or revenue metrics, or an explanation of app analytics. Use app-stability-analysis for issue-level crash or ANR diagnosis.
---

# App Product Analytics

## Outcome

Produce a decision-ready operating review from live data. Separate acquisition, current installed audience, product usage, retention, monetization, and stability instead of treating every console number as “users.” Explain what changed, the strongest evidence for why, and the next decision.

Read [references/metric-catalog.md](references/metric-catalog.md) before collecting a full operating review or defining a recurring dashboard. For a narrowly scoped follow-up, read only the relevant catalog section.

## Access And Authority

- Work read-only unless the user explicitly asks to change analytics, billing, advertising, alert, or report configuration. Changing a date range or temporary filter is read-only; saving reports, marking events, closing issues, or changing alerts is not.
- Prefer an available first-party connector, reporting API, or exported report. If none can access the authenticated data and the user requested or approved browser use, use the browser skill and the user's existing logged-in console session.
- Verify the app name, package or bundle ID, platform, production track, and account before reading numbers. Do not silently analyze another project with a similar name.
- If authentication, permission, browser control, or missing data blocks the primary path, state the exact limitation. Do not switch to screenshots, guessed values, another account, or a different data source unless the user authorizes that fallback.
- Never expose account IDs, user identifiers, stack traces, financial details, or other private console data beyond what the requested report needs.

## Source Of Truth

Use the source whose collection semantics match the question:

- Google Play Console: Play acquisition, lifetime first-time installers, installed audience, user loss, store conversion, Play billing revenue, ratings, and Android vitals.
- Firebase / Google Analytics: active behavior, engagement, retention cohorts, audiences, and product events or funnels.
- AdMob: ad earnings, requests, impressions, eCPM, match rate, show rate, ad viewers, and ads ARPU.
- A purchase backend or subscription platform: entitlement, renewal, refund, trial, and cohort LTV when Play Console cannot answer the question.

Do not force agreement between platforms. Explain measurement differences when two sources count different identities, time zones, channels, or events.

## Workflow

1. Fix the analysis contract.
   - Record the app identity, requested window, comparison window, report time zone, latest complete data date, release or campaign boundaries, and the decision the report should support.
   - Default a “recent” operating review to the latest complete 28 days versus the preceding 28 days. Also report the latest complete day for daily metrics. Use another window when product cadence or the user's question requires it.

2. Collect the mandatory baseline.
   - Query every “Baseline” row in the metric catalog, even when the result is zero, unavailable, below a privacy threshold, or not yet instrumented.
   - Record the displayed label, raw value, source, date range, filters, unit, and freshness before interpreting it.
   - For small samples, show counts with rates. A rate without its numerator and denominator is not decision-ready.

3. Collect diagnostic breakdowns only where they can explain a material change.
   - Prefer app version or release, country, acquisition source, device or OS, and new versus returning users.
   - Trace one product-value funnel from entry to the app's meaningful completed outcome. Define activation from that outcome, not from a generic screen view or app open.
   - When monetization exists, separate purchase revenue from ad revenue and separate payer conversion from ad exposure.

4. Validate the semantics.
   - Distinguish users from devices, unique users from event counts, snapshots from flows, first installs from reinstalls, active users from installed users, and period totals from lifetime totals.
   - Treat `first_open` as a first launch after install or reinstall, not a Play download count or current install base.
   - Treat “no data,” privacy-threshold suppression, and incomplete processing as unknown, not zero.
   - Compare like-for-like windows, filters, versions, currencies, and time zones. Label provisional current-day data.

5. Diagnose before recommending.
   - Start with the largest decision-relevant change, then move through acquisition, activation, retention, engagement, monetization, and quality.
   - A correlation around a release or campaign is evidence for a hypothesis, not proof of causality. State what additional breakdown or experiment would distinguish competing explanations.
   - Recommend no more than three actions, ordered by expected impact and confidence. Tie each action to a metric that can confirm or reject it.

6. Escalate stability anomalies.
   - Include the stability summary from the catalog in the operating review.
   - If crash-free usage, user-perceived crash rate, ANR rate, a new issue, or a release-specific spike is material, apply `app-stability-analysis` for issue-level diagnosis.

## Required Report Shape

Lead with a short conclusion, then include:

1. **Scope and freshness:** app identity, windows, time zones, latest complete dates, active filters, and unavailable sources.
2. **KPI table:** metric, current value, previous value, absolute or relative change, definition, source, and data status.
3. **Funnel and segments:** only the breakdowns that explain a material result.
4. **Findings:** observed fact, interpretation, confidence, and evidence gap.
5. **Actions:** owner-independent next step, expected metric movement, and verification window.

If a required metric cannot be obtained, keep its row and write the specific reason and the shortest path to make it measurable.

## Hard Boundaries

- Do not estimate current installed users as cumulative installs minus uninstalls; use installed audience or install base directly.
- Do not call an event count a user count.
- Do not report “paid conversion” without naming its denominator and cohort window.
- Do not add Play billing revenue and AdMob revenue without aligning currency, date, refunds, and tax treatment.
- Do not recommend paid acquisition from downloads alone; require activation or retention and monetization evidence.
- Do not manufacture benchmarks. Prefer the app's own trend and comparable cohorts; clearly label any current external benchmark and its source.
