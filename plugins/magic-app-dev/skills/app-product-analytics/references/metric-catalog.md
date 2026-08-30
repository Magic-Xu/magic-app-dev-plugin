# App Product Analytics Metric Catalog

Use this catalog to keep recurring reports comparable. “Baseline” means the row must appear in a full operating review even when the result is zero, unavailable, suppressed, delayed, or not instrumented.

Authoritative definitions should be rechecked when console labels or platform policies change. The links below were verified on 2026-08-30.

## Measurement Contract

Before reading metrics, record:

- app name, package or bundle ID, platform, account, and included release tracks;
- analysis window, comparison window, time zone, latest complete date, and current-day completeness;
- active app version, country, acquisition channel, audience, or device filters;
- whether the number is users, devices, sessions, events, impressions, currency, a rate, a period flow, or a point-in-time snapshot.

Google Play installation statistics use Pacific Time and Firebase / GA4 uses the property's configured time zone. Never merge daily series without reconciling that boundary.

## Acquisition And Installed Audience

| Priority | Metric | Definition and calculation | Preferred source | Interpretation guardrail |
| --- | --- | --- | --- | --- |
| Baseline | Lifetime first-time users | Unique Play users who installed for the first time, accumulated from production launch through the latest complete date. In Play Statistics select `Users > User acquisitions > New users`; sum non-overlapping intervals when no cumulative card is available. | Google Play Console | Includes users who later uninstalled. Excludes non-Play distribution. Do not use Firebase `first_open`. |
| Baseline | Current installed audience | Latest snapshot of users with the app installed on at least one device used in the preceding 30 days. | Google Play Console `Installed audience` | Closest available “still installed” user count. It omits devices inactive for more than 30 days. Do not calculate installs minus losses. |
| Diagnostic | Current install base | Latest snapshot of active devices on which the app is installed. | Google Play Console `Install base` | A device count, not a person count. |
| Baseline | New users in period | First-time installing users acquired inside the analysis window. | Google Play Console | Use Firebase new users only for behavior analysis or a measurement cross-check. |
| Baseline | User acquisitions and losses | All acquired users and all lost users in the window, each as a flow. Loss includes uninstalling from all devices or becoming inactive on all installed devices for more than 30 days. | Google Play Console | Do not interpret user loss as confirmed uninstall-only data. |
| Baseline | User loss rate | User loss divided by installed audience under Play's definition. Report numerator and denominator. | Google Play Console | This is not the same as cohort retention or app churn inferred from inactivity. |
| Baseline | Store listing conversion | Store listing acquisitions divided by eligible store listing visitors for the same locale, surface, and window. | Google Play Console store analysis | Separate Search, Explore, paid/direct, country, and custom listing only when the split can change an ASO decision. |

Google Play definitions: [View app statistics](https://support.google.com/googleplay/android-developer/answer/139628) and [recent metric semantics](https://support.google.com/googleplay/android-developer/answer/9419939).

## Activation, Activity, Engagement, And Retention

| Priority | Metric | Definition and calculation | Preferred source | Interpretation guardrail |
| --- | --- | --- | --- | --- |
| Baseline | DAU | Unique users who opened or actively used the app on the latest complete day. | Google Play DAU for distribution reach; Firebase / GA4 active users for product behavior | State which definition and date is used. Current-day data is provisional. |
| Baseline | WAU | Unique active users in the trailing 7 days. | Firebase / GA4 | Use a trailing window consistently; do not sum DAU. |
| Baseline | MAU | Unique active users in the trailing 28 days for Google Play, or the explicitly stated GA4 window. | Google Play or Firebase / GA4 | Label 28-day versus 30-day windows. |
| Baseline | Stickiness | DAU divided by MAU, using compatible source, identity, and window definitions. | Google Play or one analytics system | Daily use is not desirable for every utility. Judge against intended usage cadence and the app's own trend. |
| Baseline | Activation rate | Unique new users who complete the app-specific first value event within a fixed window divided by eligible new users in the same acquisition cohort. | Firebase / GA4 funnel or exploration | Define the value event and window. App open, screen view, and permission grant are not automatically activation. |
| Baseline | Core funnel conversion | Unique users completing each meaningful step divided by unique users entering the funnel, with an explicitly open or closed funnel and fixed window. | Firebase / GA4 | Use users, not event counts. Preserve step order when the product flow requires it. |
| Baseline | D1, D7, D30 retention | Percentage of a first-acquisition or first-value cohort that returns or repeats the defined value behavior on day 1, 7, and 30. | Firebase / GA4 retention or cohort exploration | State whether retention means any activity or repeat value. Younger cohorts cannot yet have D30. |
| Baseline | Returning users | Unique users active in the period who initiated a prior session before the period or current session, using the displayed platform definition. | Firebase / GA4 | Do not add new and returning users unless the platform documents them as mutually exclusive for that report. |
| Baseline | Engagement | Average engagement time per active user, sessions per active user, and median or distribution when available. | Firebase / GA4 | A long session can mean value or friction. Interpret with completed core outcomes. |

GA4 definitions: [user metrics](https://support.google.com/analytics/answer/12253918), [retention report](https://support.google.com/analytics/answer/11004084), and [data freshness](https://support.google.com/analytics/answer/11198161).

## Monetization

Keep purchase monetization and ad monetization separate before calculating total revenue.

| Priority | Metric | Definition and calculation | Preferred source | Interpretation guardrail |
| --- | --- | --- | --- | --- |
| Baseline | Purchase revenue | Play proceeds or the clearly named gross or estimated revenue for the period, including the stated tax, fee, refund, and currency treatment. | Google Play financial reports or purchase backend | Do not mix gross sales, proceeds, and estimated revenue. |
| Baseline | Unique payers | Unique users with at least one valid purchase in the period. | Google Play or purchase backend | Exclude sandbox/test orders and account for refunds when the source supports it. |
| Baseline | Active-user payer rate | Unique payers divided by active users in the same daily or monthly window. Report both counts. | Google Play buyer ratio or aligned purchase and activity data | Name the denominator: DAU, WAU, or MAU. |
| Baseline | Cohort install-to-payer conversion | Users in an acquisition cohort who make a first valid purchase within N days divided by new users in that same cohort. | Purchase backend plus acquisition data | State N and cohort maturity. This answers a different question from active-user payer rate. |
| Baseline | ARPU | Aligned purchase plus ad revenue divided by active users in the same period, or purchase-only ARPU when explicitly labeled. | Aligned Google Play, AdMob, and activity data | Name included revenue sources and currency. |
| Baseline | ARPPU | Purchase revenue net of defined refunds divided by unique payers in the same period. | Google Play or purchase backend | Do not include non-paying ad viewers in the denominator. |
| Diagnostic | Realized LTV | Cumulative net revenue generated by a mature acquisition cohort divided by users in that cohort. | Purchase backend or cohort export | Do not extrapolate immature cohorts without labeling a prediction model. |
| Baseline | Ad estimated earnings | Estimated ad revenue for the period. | AdMob | Estimated earnings can change before finalization. |
| Baseline | Ads ARPU / ARPDAU | Ad estimated earnings divided by active users for the aligned period. | AdMob Ads Activity | Align active-user scope; do not substitute impressions. |
| Baseline | Ad delivery health | Requests, match rate = matched requests / requests, show rate = impressions / matched requests, impressions, eCPM, ad viewer rate, and ad load latency when available. | AdMob | Diagnose volume, fill, rendering, and price separately; eCPM alone does not explain revenue. |

AdMob definitions: [Ads Activity metrics](https://support.google.com/admob/answer/10979428). LTV and ARPPU terminology: [RevenueCat cohort and LTV definitions](https://www.revenuecat.com/docs/dashboard-and-metrics/charts/cohorts-and-ltv-index).

## Product Quality And Store Health

| Priority | Metric | Definition and calculation | Preferred source | Interpretation guardrail |
| --- | --- | --- | --- | --- |
| Baseline | Crash-free users and sessions | Percent of engaged installations or sessions without a fatal crash for one fixed window. | Firebase Crashlytics | Fatal-only in Crashlytics; do not compare percentages from different window lengths. Apply `app-stability-analysis` for detail. |
| Baseline | User-perceived crash rate | Daily users who experienced at least one foreground user-perceived crash divided by daily users. | Google Play Android vitals | Data covers eligible Play-installed devices that share diagnostics, not every installation. |
| Baseline | User-perceived ANR rate | Daily users who experienced at least one user-perceived ANR divided by daily users. | Google Play Android vitals | Treat “insufficient data” as unknown. Apply `app-stability-analysis` for clusters. |
| Baseline | Store rating | Current Google Play rating, rating volume, and recent rating trend. | Google Play Console | Pair rating changes with review themes and release timing; do not infer causes from the average alone. |
| Diagnostic | Release adoption and update loss | Active installed versions, update coverage, and device loss after update. | Google Play Console | Use this to separate product-wide changes from a bad release cohort. |

Android vitals definitions: [technical quality](https://support.google.com/googleplay/android-developer/answer/9844486). Crash-free definitions: [Firebase Crashlytics crash-free metrics](https://firebase.google.com/docs/crashlytics/crash-free-metrics).

## Diagnostic Segments

Use a segment only when it can distinguish plausible causes:

- release version and Play track for regressions or adoption;
- acquisition source and store surface for acquisition quality;
- country for listing localization, price, revenue, or ad-market differences;
- device model, OS, and form factor for compatibility or stability;
- new versus returning users for activation versus ongoing value;
- payer versus non-payer or ad viewer versus non-viewer for monetization effects.

Avoid slicing a small sample until every segment is noise. Record privacy suppression and minimum-threshold behavior.

## Interpretation Order

Analyze in this order so downstream outcomes are not mistaken for root causes:

1. Distribution: listing visitors, conversion, first-time users.
2. Activation: first meaningful value completion.
3. Retention and activity: cohorts, DAU/WAU/MAU, stickiness.
4. Core behavior: funnel completion and frequency.
5. Monetization: payer conversion, purchase value, ad delivery, ARPU and LTV.
6. Quality: crashes, ANRs, ratings, and release-specific loss.

For each material movement, report the observed fact, the most plausible interpretation, an alternative explanation, and the next query or experiment that would distinguish them.
