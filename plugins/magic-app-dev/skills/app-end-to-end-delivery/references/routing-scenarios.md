# Requirement Routing Scenarios

Use these scenarios to test routing decisions, not as code templates. Adapt names and exact test commands to
the target repository. Validation examples are candidate evidence for the affected behavior. Select checks that
cover the accepted risk, preserve repository-mandated gates, and reuse results valid for the current inputs.

## Stateful UI Inside An Existing Feature

**Request:** Add an inline import-progress panel with cancel and retry actions to an existing import page.

- **Owner and reason:** The import `feature` owns the product state and user intents because the panel changes
  how that feature behaves; it is not an independent destination or lifecycle.
- **Minimum artifacts:** Extend the existing feature state, mutations or reducer, intent/effect handling, and
  Compose content. Add state-transition and UI behavior tests. Add a focused component state holder only if
  the existing feature has no suitable owner.
- **Dependency proof:** The UI dispatches events and renders state. It does not call the importer or Android
  APIs directly. No sibling feature dependency is introduced.
- **Deliberately absent:** No new `Screen`, page Contract, ViewModel, navigation route, empty domain layer, or
  gateway is created for the panel itself.
- **Risk-matched validation:** Use focused state/reducer and Compose behavior evidence plus affected compilation.
  Run Platform Quality and Lint when required by repository policy or affected structure/resources. Exercise cancel
  and retry on a device when coroutine cancellation,
  activity lifecycle, or real rendering is part of acceptance. An APK is needed only when installed behavior
  or packaged integration must be proven; an AAB is not evidence for the state transitions.

## Pure Domain Capability

**Request:** Decide whether a saved project is eligible for automatic cleanup from age, pin status, and
retention policy.

- **Owner and reason:** `domain` owns the decision because it is a stable business rule with no UI, Android,
  storage, or clock-reading semantics.
- **Minimum artifacts:** A domain model or policy function and table-driven pure Kotlin tests. Pass the current
  time and project facts into the rule instead of reading them from Android or storage.
- **Dependency proof:** Domain code imports neither feature nor app code and contains no Android type. The
  caller may depend downward on the domain policy.
- **Deliberately absent:** No feature module, UI state, `Screen`, Contract, ViewModel, gateway interface, or
  app coordinator is created unless another accepted behavior actually needs it.
- **Risk-matched validation:** Run boundary-value unit tests and compile the affected domain and consumer
  modules. Run Platform dependency/quality checks if package or module edges changed. Lint, APK/AAB, and device
  validation do not add proof for an otherwise isolated pure rule.

## Android And IO Gateway

**Request:** Export a project to a document selected through Android's Storage Access Framework.

- **Owner and reason:** `core` owns document writing and `ContentResolver` interaction as a system/IO gateway.
  If the export begins from UI, the existing feature emits a typed outcome and `app` owns the activity-result
  and lifecycle coordination; neither layer takes over the other's semantics.
- **Minimum artifacts:** Extend an existing document gateway or add the smallest useful gateway contract and
  Android implementation, deterministic serialization tests, and a boundary integration test. Extend the
  existing feature effect and app handler only when they are part of the requested path.
- **Dependency proof:** Core imports no feature or app code; feature UI contains no `Context`, resolver, stream,
  picker, or filesystem call; app wires the feature outcome to the core capability. No feature depends on a
  sibling feature.
- **Deliberately absent:** No new page or page MVI skeleton is created for the export operation, and the gateway
  does not contain navigation or product UI state.
- **Risk-matched validation:** Use serialization and failure-path tests, Android boundary evidence, and affected
  compilation. Run Platform Quality and Lint for required gates and changed platform/resource boundaries. Use an
  emulator or device to prove provider selection,
  cancellation, write failure, URI access, and reopen behavior when those OS semantics are accepted behavior.
  Build an APK when that device path or packaged manifest integration must be tested; build an AAB only when
  release packaging is in scope.

## Cross-Feature Orchestration

**Request:** After Import completes, open Library and focus the newly imported item.

- **Owner and reason:** The Import feature owns the completion outcome, the Library feature owns how it renders
  a focused item, and `app` owns the route transition and cross-feature effect. A domain coordinator owns shared
  durable business state only if both features genuinely need that same state outside navigation.
- **Minimum artifacts:** A typed Import outcome, an app effect/navigation handler, the smallest Library input
  or domain state update, and handler/integration tests. Reuse existing contracts and coordinators when their
  semantics match.
- **Dependency proof:** Import and Library do not import each other. App depends on both and coordinates them;
  neither feature contains the app router. Domain or core never imports a feature.
- **Deliberately absent:** No duplicate root Store containing both feature states, no feature-to-feature helper,
  no new screen for the transition, and no core gateway when the flow has no system side effect.
- **Risk-matched validation:** Use feature outcome and app handler/route evidence, affected compilation, and required
  quality gates. Add Lint for affected Android APIs/resources and an integration or device flow from completion through the
  focused Library state. APK installation is appropriate when process/lifecycle or packaged navigation is in
  scope; AAB generation is reserved for release-packaging risk or an explicit deliverable.
