# From Findings To A Verified Iteration

Use when analysis identifies an actionable product problem, or when checking whether a released change
achieved its intended outcome. Keep the record in the existing issue, product requirement, analysis or
release evidence. A small maintenance fix need not become an experiment.

## Before Development

Connect the proposed change to the observed problem: affected users/cohort, source/window and baseline,
working explanation with confidence, expected user outcome, acceptance criteria, primary metric and
relevant guardrail. Name an observation window and the evidence needed to decide improved, unchanged,
regressed or inconclusive. Separate functional acceptance from business effect.

Use existing telemetry when it answers the question. Missing instrumentation is a proposed product/data
change, not permission to add a collecting SDK or transmit new data. Request the missing scope decision
and follow the design/data gates if that work is chosen. An analysis request alone does not authorize a
fix, Issue creation in an external system, or a rollout change.

## When The Change Ships

Link the accepted requirement and source change to the actual published version, exposure/rollout and
publication time. Carry forward the metric definition and baseline; do not reset the hypothesis after
seeing results. For store work, track the published store revision separately from the binary version.
Choose an observation window relative to real exposure and source latency, not upload time.

## Check The Outcome

Use product analytics or stability analysis for the decision, with comparable windows, versions,
populations and definitions. Consider rollout share, acquisition mix, seasonality, concurrent changes,
small samples and data latency. A before/after association alone does not prove causation.

State the result against the original criteria and remaining uncertainty. Recommend the next smallest
decision: retain, investigate, iterate, or consider rollback. Do not execute a new feature or rollout
change without its corresponding authorization. Insufficient evidence remains inconclusive.

Reuse the analysis report destination. Updating an existing outcome record avoids a second report of the
same analysis. A future verification window is a plan, not an active monitor: create a reminder or
automation only when the user requests one, using the available scheduling capability.
