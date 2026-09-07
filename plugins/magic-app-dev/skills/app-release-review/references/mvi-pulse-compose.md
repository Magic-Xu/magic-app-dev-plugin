# Android State, Tasks And Resource Ownership

Use for stateful Android behavior, asynchronous work, side effects and recovery. Resolve exact Pulse
APIs from the project's dependency version and source; use accepted contracts to judge intended behavior.

## Page State And Inputs

An independently stateful page follows the repository's Contract/State/Intent/Mutation/Effect/ViewModel
pattern. A panel or dialog normally extends its feature owner rather than creating another page Store.
Factory-generated apps use feature-owned Pulse Stores, typed mutations, reducers and ViewModels. Preserve
the selected state-management system; do not add a competing one to implement a local feature.

Keep user/platform input, committed state facts and transient commands distinct. Verify that the real input
path reaches its executor and reducer, state covers applicable outcomes, and UI only renders and dispatches.
Inspect input ordering, backpressure and rejected admission under repeated actions. Enqueueing an input
does not prove business completion. Use existing repository mechanisms instead of another ad hoc queue.

## Tasks, Effects And Lifecycle

For each asynchronous operation identify the scope, task identity, concurrency policy, cancellation path
and condition allowing a result to commit. In Pulse apps, use the project's keyed-task/runtime mechanisms
when available instead of duplicating them with unmanaged Jobs, locks or generation counters. Distinguish
latest-wins work from queued work or duplicate suppression according to the accepted behavior.

Check late results after input replacement, cancellation and disposal. Preserve structured cancellation;
do not silently turn cancellation into success or a user failure. Verify exception isolation where branches
are intended to succeed independently and release SDK/bitmap/file resources according to their owner.

Use lifecycle-aware state/effect collection and the intended ViewModel owner/key. For each transient effect
identify its consumer, active lifecycle, replay/delivery guarantees and possible duplicate/lost consumption.
Navigation, picker launch, sharing and messages may use the project's effect convention; facts necessary
for subsequent correctness must remain in state or durable storage. A replay-zero stream does not promise
delivery across recreation. Do not rely on it as the sole record that a save or entitlement update completed.

Low-level Composables do not perform business decisions, SDK/IO work or repository mutations. UI-scoped
animation, focus and framework adapters may use Compose lifecycle APIs when consistent with project rules;
they do not justify moving business ownership into a composable.

## Persistence And External Operations

Distinguish UI recreation, process restart, recovery from durable facts and genuine background continuation.
SavedState is not a serialized job and an in-process task is not a durable scheduler. Restore only supported
stable fields and normalize transient states according to the product's actual recovery promise.

For shared media or external writes, inspect input identity/snapshot, operation ownership, commit point,
failure cleanup and retry semantics. Where recovery is required, reconcile authoritative external/durable
facts without guessing success, duplicating published output or deleting uncertain user data. Do not invent
cross-process continuation, journals or background services for a product that only promises safe restart.

Use focused transition/integration tests and recreation/device evidence for the affected semantics. See
[release-evidence.md](release-evidence.md) for evidence selection. Official
[UI event guidance](https://developer.android.com/topic/architecture/ui-layer/events) and
[coroutine practices](https://developer.android.com/kotlin/coroutines/coroutines-best-practices) help assess
delivery and lifetime risks; adapt the reasoning to the project's enforced runtime contract.
