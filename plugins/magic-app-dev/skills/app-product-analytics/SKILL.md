---
name: app-product-analytics
description: 产品数据分析：获客、活跃、留存、漏斗与变现，支持经营总览、专项问题和上线后的效果验证；按项目约定交付可核验报告。
---

# App Product Analytics

Explain what changed, the strongest evidence for why, and the next product decision. Separate acquisition,
installed audience, usage, retention, monetization, and stability according to their measurement semantics.

## Scope And Access

- For a full operating review or recurring dashboard, read [references/metric-catalog.md](references/metric-catalog.md)
  and collect every Baseline row, including unavailable or not-applicable rows with their reasons.
- For a focused question, collect only the relevant metrics and the context needed to interpret them. Read the
  matching catalog sections; broaden collection when a material finding or unresolved hypothesis requires it.
- A conceptual metric explanation needs neither console access nor a new report document.

Establish the app identity, decision, analysis and comparison windows, time zone, filters, and latest complete
source dates. Reuse context and evidence valid for the same app, population, and window. For an unspecified recent
operating review, default to the latest complete 28 days versus the preceding 28, plus the latest complete day for
daily metrics; adjust to the question or product cadence.

Work read-only in source systems unless configuration changes are explicitly requested. Prefer a first-party
connector, reporting API, or export; use available browser tools with the user's authorized console session when
needed. Reuse existing authorization. Changing a reading method within that source and session does not authorize
changing accounts, data sources, access scope, or the deliverable. Report blocked coverage and continue independent
analysis; ask before a fallback changes those boundaries. Do not replace missing data with guessed values.

Verify app name, package or bundle ID, platform, account, and relevant release-track coverage before interpreting
numbers. Limit private console data in the report to what the decision needs. Temporary filters are read-only;
saving reports, marking events, changing alerts, or altering billing or advertising settings are mutations.

## Collect And Interpret

Use the source whose semantics answer the question:

- Google Play Console for Play acquisition, installed audience, store conversion, Play billing, ratings, and vitals.
- Firebase / GA4 for active behavior, engagement, retention cohorts, and product events or funnels.
- AdMob for ad earnings, delivery, exposure, and ads ARPU.
- A purchase backend or subscription platform for entitlements, renewals, refunds, trials, and cohort LTV when needed.

Record source labels, values, units, windows, filters, and freshness. Show counts with rates for small samples.
Distinguish users, devices, sessions, and events; snapshots and flows; new installs and reinstalls; period and
lifetime totals. `first_open` is a first launch after install or reinstall, not Play downloads or installed audience.
Missing, suppressed, or incomplete data is unknown, not zero. Align populations, windows, currencies, and time zones
before comparing or combining sources; explain remaining differences instead of forcing agreement.

Investigate the largest decision-relevant change. Use version, country, channel, device/OS, or new/returning splits
when they distinguish plausible causes. Trace the product-value funnel when activation or conversion matters;
define activation from the completed user outcome. Separate purchase revenue, ad revenue, payer conversion, and ad
exposure. Treat release or campaign correlations as hypotheses and name the evidence needed to distinguish them.

When a stability anomaly can change the operating decision, use `$app-stability-analysis` for the affected issues.
Pass the existing scope and evidence, request only the necessary diagnosis, and incorporate its findings into this
analysis. The operating review owns the combined report; the nested diagnosis does not create a second document.

## Report And Deliver

Lead with the conclusion. Include scope and freshness; relevant KPI values, comparisons, definitions, sources, and
data status; explanatory funnel or segment evidence; findings with confidence and gaps; and prioritized actions
with a metric and window for verification. Full reviews retain all Baseline rows. Focused reports include the rows
needed to answer their question. Use only as much structure and as many actions as the decision needs.

For each completed analysis using live or user-supplied app data, follow
[references/report-delivery.md](references/report-delivery.md). Use `<App> 数据分析｜<analysis end date>`
or the reader's language; the report destination follows the request/project preference.

For a proposed iteration or a request to verify a shipped change, use
[iteration outcomes](../app-end-to-end-delivery/references/iteration-outcomes.md). Connect the finding,
accepted action, original metric/baseline, actual published exposure and observation window. Analysis
alone does not authorize implementing recommendations or scheduling monitoring.

## Measurement Boundaries

- Use installed audience directly; cumulative installs minus losses does not establish current installed users.
- Name the denominator and cohort window for paid conversion; event totals do not establish unique users.
- Align currency, dates, refunds, and tax treatment before adding purchase and ad revenue.
- Require activation or retention and monetization evidence before recommending paid acquisition from growth data.
- Prefer the app's own trend and comparable cohorts. Source and label external benchmarks; do not invent them.
