# Architecture And Implementation Judgment

Judge architecture by its ability to deliver the accepted product at a reasonable total cost. Apply the
repository's established boundaries. Read architecture decisions, relevant callers, dependency configuration
and CI contracts when they resolve an actual uncertainty; avoid loading the entire documentation tree.
For Android state, tasks, effects and recovery, use [mvi-pulse-compose.md](mvi-pulse-compose.md).

## Ownership And Change Cost

Factory's default direction is `app -> feature -> domain -> core`; upper layers may use lower layers,
never the reverse, and features do not import siblings. Cross-feature coordination belongs in `app`.
Use the target repository's established equivalent. A single Gradle module can enforce component boundaries
through packages and checks; do not introduce modules or migrate frameworks just to match an example app.

- UI renders state and dispatches events. Presentation owns state transitions and UI-facing projections.
  Domain owns business rules and algorithms at the appropriate local/shared scope. Platform/IO adapters
  own system, storage and SDK operations; product-specific orchestration stays with the feature or app owner.
- Keep one authoritative owner for a mutable business fact; derived UI projections are not independent
  writable copies. Trace ownership through construction, use, cancellation, external commit and disposal.
- Keep genuinely shared, stable business concepts in shared domain; business-agnostic primitives belong
  in core. A helper used once may be justified by encapsulation or testability, while similar code in two
  features may represent different rules. Do not use a generic utility package as a business-code overflow.
- Extract components when responsibility, actual reuse or testability justifies the extra boundary. File
  length is a signal; explicit repository limits remain mandatory. Do not split coherent code only to make
  a metric look better, add empty layers, or impose a Contract/ViewModel on every subordinate visual state.
- User-visible strings use Android resources and all supported translations. Reuse design tokens. Inspect
  language/variant parity and runtime meaning; equal string keys alone do not prove a correct translation.

## Turn Quality Goals Into Scenarios

| Goal | Evidence-bearing question |
| --- | --- |
| Cohesion / clear responsibility | Does a business rule have a clear owner? Do changes for the same reason stay together? |
| Low coupling / encapsulation | Can a consumer work through a stable contract without knowing internal state or call order? |
| Useful reuse / extensibility | Does a shared abstraction preserve the same semantics and reduce known change cost? |
| Readability / maintainability | Can a maintainer follow entry, decision, effect and outcome without hidden rules or excessive indirection? |
| Correctness / reliability | Do invariants survive invalid input, failure, cancellation, concurrency and lifecycle transitions? |
| Testability / diagnosability | Can the outcome be reproduced and a failure located without exposing sensitive data? |
| Performance / privacy | Do representative workloads respect the product's latency, memory, offline and data-handling constraints? |

Select the scenarios and measures that matter to this product; do not invent arbitrary universal scores or
thresholds. Abstraction and duplication both have costs. Fix observed risk or a justified change obstacle;
keep aesthetic preferences and speculative future extensibility out of blocking findings.

## Verify Suspicious Implementations And External Advice

Check declared and resolved dependency versions, actual signatures, source/artifact definitions, call sites,
bindings and runtime entrypoints. A plausible name, passing mock or code comment is not proof of a working
integration. Trace failure propagation and fallbacks; a fallback that changes promised output, privacy,
entitlements or persistence is a product decision, not an invisible implementation convenience.

For unfamiliar APIs, disputed recommendations or version-sensitive behavior, consult current primary
documentation and maintained source for the project's versions. State the supported principle, its
applicability and the concrete risk addressed. Record a material adopted decision in project engineering
docs when needed. Do not treat internet examples as authorization to replace the chosen architecture.

These primary references support specific judgments; open only what is relevant and verify current guidance:

- [Android architecture recommendations](https://developer.android.com/topic/architecture/recommendations):
  single sources of truth, unidirectional flow and recommendations adapted to the app.
- [Android modularization](https://developer.android.com/topic/modularization): encapsulation, cohesion,
  coupling and the overhead of excessively fine-grained modules.
- [Google code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html): functionality,
  concurrency, complexity, tests and over-engineering.
- [SEI quality attributes](https://www.sei.cmu.edu/library/reasoning-about-software-quality-attributes/):
  assess quality through concrete scenarios and trade-offs.
- [YAGNI](https://martinfowler.com/bliki/Yagni.html): evaluate present requirements and maintenance cost
  before speculative functionality or generalization.
- [Now in Android](https://github.com/android/nowinandroid/blob/main/docs/ArchitectureLearningJourney.md):
  a maintained example connecting data ownership, business composition, UI state and tests, not a required stack.
