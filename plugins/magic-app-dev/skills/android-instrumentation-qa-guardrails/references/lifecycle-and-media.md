# Lifecycle And Media QA

Read when accepted behavior includes configuration changes, Activity recreation, or media editing/export. Select
only the parts relevant to the requested flow.

## Configuration Changes

Language, theme, font scale, orientation, and other configuration changes may recreate the Activity. Verify the
state that the product requires to survive recreation, including its backing runtime objects:

- UI state may still say content exists after a bitmap or media object is lost.
- A ViewModel may preserve intent state while Compose `remember` loses the backing object.
- A route may survive while a transient operation resets.

State required across Activity recreation belongs in a lifecycle-aware owner. Large images do not belong in saved
instance state. Persist or re-decode media when process-death recovery is part of the requirement; Activity
recreation alone does not establish that requirement.

## Editor And Media Flows

For an accepted editing/export flow, prove the relevant state and output: load or create media, perform the edit,
exercise undo/redo when affected, save/export, and verify the result exists and reflects the requested behavior.
Exercise configuration changes, sharing, or provider failure when those semantics are in scope. Navigation or a
screenshot of a success message alone does not prove that the saved result is usable.

Restore the previous app language and any settings changed by the test in cleanup so the device remains reusable.
