# MVI + Pulse + Compose Pattern

Use this reference when creating or changing a page.

## Contract First

Create or update the contract before UI behavior:

- `XxxContract.kt`
- `XxxState`
- `XxxIntent`
- `XxxEffect`

State is for durable rendering data. Effect is for one-time commands.

Good state:

- selected item
- loading flag
- error state that affects rendering
- form values
- undo/redo availability

Good effects:

- navigate
- open system picker
- launch share sheet
- show toast/snackbar
- request permission

## ViewModel

The ViewModel:

- receives intents
- updates pulse state
- calls use cases or gateways
- emits effects
- coordinates asynchronous work

The ViewModel should not draw UI, hold Compose-only state, or directly duplicate platform code that belongs in a gateway.

## Compose

Composable functions:

- collect state
- render UI
- dispatch intents

Do not call SDKs, filesystems, repositories, or navigation APIs directly from low-level UI components. Route/shell components may collect effects and hand them to app-level coordinators when that is the repo pattern.

## Naming

Prefer:

- `OnSaveClick`
- `OnPickerDismiss`
- `OnImagePicked`
- `OnModeSelected`
- `OnStrengthChanged`

Avoid:

- `UpdateData`
- `HandleClick`
- `DoAction`
- `Process`

## Splitting Rule

Split screens by responsibility:

- route/effect collector
- screen composition
- top bar
- main content
- control panel
- bottom bar
- sheet/dialog
- row/card/chip components

Files over 400 lines are review hotspots. Files over 800 lines should be split before completion unless the repository has a different hard threshold.
