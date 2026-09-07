# Product Design And Acceptance

Use for user-visible product changes: screens, copy, interactions, loading/error/empty states, layout,
style and animation. Store visuals use the separate [store review flow](../../google-play-release/references/store-refresh.md).
Follow a stronger target-repository gate when present. Existing explicit approval of the exact current
design is reusable; UI implementation must wait when required approval is missing.

## Prepare A Concrete Design

Start from the accepted loop and current design system. Use the project's editable design source and
available design skills/tools when helpful; inspect availability instead of assuming a particular vendor
is installed. Keep an established HTML/Figma/other source authoritative; do not silently migrate tools,
replace it with static screenshots, or create a parallel design under another directory.

Show the affected flow and consequential states, including failure/recovery, navigation, accessibility
and representative localization where they affect the decision. Match the scope: a copy fix can be a
small rendered before/after; a new editor needs an interactive or linked flow. Use realistic fictional
data. Identify free/paid or data-handling changes if they affect the user's decision.

Present a reviewable source/preview with what changed and behavioral acceptance criteria. Reuse product
facts; ask only for decisions whose alternatives change meaning. Do not implement feature code, Android
resources or feature tests before approval. Independent research and read-only feasibility checks may
continue; any implementation spike must respect the repository's gate and the user's scope.

## Implement The Accepted Design

After approval, implement the accepted source and its behavior, then verify interaction and visual
consistency as part of the existing validation pass. Device screenshots prove appearance; they do not
alone establish state transitions, persistence, permissions or recovery.

If implementation needs a material change to the approved visible behavior, update the design and return
that change to review before implementing it. Do not reopen unchanged approved parts. Pure logic fixes
or infrastructure work with no visible change follow normal development without a design artifact.
