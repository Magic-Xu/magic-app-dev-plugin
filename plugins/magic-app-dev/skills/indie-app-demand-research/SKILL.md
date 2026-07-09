---
name: indie-app-demand-research
description: Research and rank indie app opportunities from real demand signals before building. Use when the user asks to find app ideas, validate product directions, mine revenue marketplaces such as TrustMRR, summarize X/Twitter founder threads for demand lessons, compare mobile/web/SaaS opportunities that could become apps, or choose local-first, low-ops, no-server app directions for an indie developer.
---

# Indie App Demand Research

## Core Rule

Start from paid demand, not from product ideas, technologies, or what would be fun to build.

The job is to answer: who has an urgent problem, how are they already trying to solve it, why would they pay, how can they be reached, and can the first version be shipped with low operating cost?

If the user's goal, constraints, audience, platform, geography, monetization preference, or risk tolerance is unclear and materially changes the answer, stop and ask. If the requested path is slower than a direct validation path, say so and propose the shorter route.

## Workflow

1. Define the decision.
   - Capture the user's target platform, development strengths, budget, server tolerance, desired price model, time horizon, and categories to include or exclude.
   - Convert vague wishes into a decision sentence: "Pick N directions for X developer to validate next under Y constraints."
   - Treat "many users" as insufficient. Prefer "many reachable users with a painful enough problem to pay."

2. Gather current evidence.
   - Browse for current external facts; do not rely on stale model memory for revenue, rankings, platform APIs, competitors, or founder claims.
   - For user-provided X/Twitter links, fetch the original page when possible. If blocked, use a public mirror or syndication endpoint, and state the source limitation.
   - For TrustMRR, prefer its documented public AI endpoint when available. Do not scrape full marketplace pages when the site provides an API or says not to scrape.
   - Add other evidence only when it changes the decision: App Store listings and reviews, Google Trends/Search, Reddit/Quora/community complaints, SEO pages, acquisition listings, pricing pages, and public revenue screenshots.
   - Record retrieval dates for drift-prone evidence.

3. Extract demand signals.
   - Strong signals: verified revenue, active subscriptions, high-intent search terms, repeat complaints, expensive existing alternatives, manual workarounds, paid templates/courses, and niche communities already buying.
   - Weak signals: likes, views, downloads without revenue, generic AI novelty, broad "productivity" claims, founder excitement, and features that users expect free.
   - Separate distribution evidence from product evidence. A viral video proves attention, not durable demand.

4. Diagnose why existing ideas fail or work.
   - Frequency: daily/weekly problems beat rare utilities.
   - Urgency: pain tied to money, health, status, children, safety, compliance, or saved time monetizes better.
   - Willingness to pay: professionals, parents, hobbyists with expensive gear, and people avoiding embarrassment often pay more than casual users.
   - Reachability: ASO/search/community channels must be plausible for a solo developer.
   - Competition: crowded markets are acceptable only with a sharper niche, channel, or local-first advantage.

5. Apply the local-first app filter.
   - Prefer directions where the core value can run on-device: camera, microphone, files, OCR, speech, health sensors, screen time APIs, local ML, reminders, widgets, shortcuts, or offline content.
   - Penalize directions that require ongoing inference cost, human moderation, large cloud storage, scraping at scale, real-time collaboration, marketplace liquidity, or customer support-heavy B2B workflows.
   - Prefer privacy-sensitive workflows where local-first is a reason to buy, not just an implementation detail.

6. Score candidates before ranking.
   - Demand strength: 0-5
   - Willingness to pay: 0-5
   - Reachable channel: 0-5
   - Local-first fit: 0-5
   - Build feasibility for the user: 0-5
   - Ops cost: 0-5, where 5 means near-zero ongoing server/vendor cost
   - Differentiation wedge: 0-5
   - Subtract risk penalties for regulation, policy rejection, platform dependency, saturated generic AI, copyright, privacy, or unclear monetization.

7. Output a decision-ready shortlist.
   - Lead with the recommended direction, not a neutral list.
   - For each direction include: target user, painful job-to-be-done, evidence, local-first MVP, monetization, acquisition channel, key risk, and the fastest validation test.
   - Cut directions that are interesting but not suitable for the user's stated constraints.
   - Keep the final answer concise enough to change a build/no-build decision.

## Validation Standard

Do not recommend building a full app first when a faster paid-demand test exists.

Prefer validation in this order:

1. Landing page with concrete pricing and checkout/waitlist.
2. App Store keyword/review analysis plus a fake-door or TestFlight MVP.
3. Manual concierge version for professional or niche workflows.
4. Tiny paid utility with one complete loop.

Useful thresholds:

- At least 3 checkout clicks or qualified leads per 100 targeted visitors.
- At least 5 direct user conversations with repeated, specific pain.
- At least 3 competitors or substitutes with visible pricing or revenue.
- A V1 that can be shipped in days or weeks, not months.

## Output Shape

Use this structure unless the user asks otherwise:

1. Short conclusion: what to do and what not to do.
2. Source lessons: what the provided sources imply.
3. Ranked directions: table or compact bullets.
4. First validation plan: exact next actions and pass/fail criteria.
5. Caveats: evidence limits, stale data, or assumptions.

When asked for "5 directions", provide exactly 5 unless there is not enough evidence. If fewer than 5 are credible, say so and explain why.

## Red Flags

- Building because the technology is exciting.
- Choosing a category only because a founder post went viral.
- Mistaking downloads, followers, likes, or impressions for payment intent.
- Generic AI wrapper with ongoing model costs and no proprietary channel.
- Low-frequency consumer utility with no urgency and free substitutes.
- App ideas that require server operations when the user's constraint is local-first.
