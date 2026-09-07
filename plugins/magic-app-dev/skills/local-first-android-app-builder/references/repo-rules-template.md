# Repository Rules

Use when creating or updating agent instructions or engineering rules. Preserve actual repository contracts and
add only durable choices that would change an agent's decisions in this project.

Useful project facts include:

- Product purpose, accepted scope, and data or privacy boundaries.
- Required technology and dependency direction, including the existing page/state pattern.
- Supported locales, design-token source, and platform-effect ownership.
- Current editable product-design source and the applicable owner approval gate before visible implementation.
- Repository layout and authoritative documents, with links rather than copied policy text.
- Actual branch/worktree policy and local validation commands, including enforced CI gates.
- Store, legal, or release obligations relevant to the implemented capabilities.

Select project-specific constraints supported by a maintained source or explicit agreement. Link the context
needed to apply each rule and read it when it governs the current change.

For Factory workspaces, keep editable visuals in `design/`, publishing inputs in `publishing/`, and reproducible
output in ignored `build/`. The generated layout contract and validator define the exact supported paths.
Keep final Android resources in their Android source sets. Reuse generated engineering rules and checks instead
of maintaining a competing template in `AGENTS.md`.

Make verification proportional to the affected behavior while preserving required checks. Reuse valid evidence,
and report material gaps. State release authorization separately from local implementation where the project's
workflow requires it; existing task authorization need not be requested again.
