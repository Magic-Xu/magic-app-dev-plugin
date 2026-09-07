# MVI, Pulse, And Compose Ownership

Use when deciding page state and effect ownership. The target repository's working implementation and enforced
contracts are authoritative for exact Pulse APIs, names, and required artifacts.

## Page Or Component

An independent page owns its public state, user intents, effects, and state holder under the repository's MVI
pattern. Update the contract with the changed behavior. A panel, dialog, loading state, or other subordinate UI
normally extends its existing feature owner instead of gaining a second page contract or ViewModel.

Factory-generated apps use feature-owned Pulse Stores, typed mutations, reducers, and ViewModels. Independent
pages use `XxxScreen`; subordinate visual states use `XxxContent` or `XxxComponent`. Follow the generated examples
for API usage instead of introducing a second state-management pattern.

## State And Effects

- State represents rendering facts such as selection, progress, form values, errors, and undo availability.
- Intents name the user's action or relevant external result precisely, such as `OnSaveClick` or `OnImagePicked`.
- Reducers or state holders own transitions. Domain logic belongs in domain rules; Android and IO behavior
  belongs behind the repository's platform gateways.
- Effects represent one-time commands such as navigation, picker launch, sharing, or a message. Route or
  app-level coordinators handle them using the existing lifecycle convention.
- Low-level Composables render state and dispatch events; they do not perform repository mutations or SDK/IO work.

## Structure And Validation

Extract components when responsibilities, reuse, or testability justify them. File length is a review signal;
enforced repository limits still apply, including the Factory Platform's production Kotlin limit.

Verify changed transitions and effect handling with the task's validation plan. Use device or recreation evidence
when lifecycle semantics matter; a routine visual edit does not require rebuilding the entire page architecture.
