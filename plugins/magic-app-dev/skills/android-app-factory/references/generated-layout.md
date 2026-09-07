# Generated Workspace Layout

The generator produces:

~~~text
<slug>/
  <slug>.code-workspace
  <slug>-android/
    .app-factory/spec.json
    .github/workflows/repository-layout.yml
    .git/
    AGENTS.md
    README.md
    app/
    docs/
      README.md
      decisions/
      engineering/
      operations/
      product/
    publishing/
      README.md
      legal/
    gradle/
    tools/
      README.md
      publishing/legal/sync_to_legal_repo.py
      repository/
        validate_layout.py
        tests/test_validate_layout.py
  <slug>-legal/
    .app-factory-legal.json
    .git/
    .nojekyll
    README.md
    assets/site.css
    en/
    zh-CN/
    index.html
    privacy-policy.html
    user-agreement.html
~~~

## Ownership

- The Android repository owns the product specification, repository layout policy, and canonical legal source.
- The legal repository owns no private data. It is a publishable projection of `publishing/legal/`.
- `tools/publishing/legal/sync_to_legal_repo.py` copies only the canonical legal tree and verifies the target marker before writing.
- The parent workspace is not a third Git repository.

## Repository Information Architecture

- `docs/` contains current human-readable product facts, engineering rules, operator procedures, and durable decisions only.
- `design/` contains editable visual sources; `tools/` contains executable helpers; `publishing/` contains external-system inputs; `releases/` contains immutable completed-release evidence.
- Reproducible logs, screenshots, media, reports, and build outputs belong in the ignored root `build/` directory.
- One current source represents each stateful topic. Git history replaces `final`, dated, copied, archived, or version-suffixed document variants.
- The generated repository tests its layout validator and runs it in the `Repository Layout` workflow. Apps may add product-specific required paths or compatibility exceptions without weakening the shared lifecycle boundaries.

## Design And Lifecycle Sources

`docs/README.md` is the initial source map. It links the generation spec, current build configuration,
product requirements, legal sources and engineering rules. Future design, console, release and
measurement sources extend this index; generation does not establish live store or binary state.
`docs/engineering/design-review.md` and `AGENTS.md` require owner approval of current product design
before user-visible feature implementation. The generated ready screen remains an engineering sample.

## Android Baseline

- One ":app" Gradle module.
- Jetpack Compose and Material 3.
- One pinned released Magic Android Platform version supplying Application, Compose, Pulse, and mandatory Quality plugins.
- "HomeContract", "HomeState", "HomeIntent", "HomeEffect", typed "HomeMutation", "HomeMutationReducer", and "HomeViewModel".
- Composables render state and dispatch intents only.
- Design values live in "core/designsystem".
- Dependency direction is `app -> feature -> domain -> core`; features cannot import app or sibling features.
- Each independent page named "XxxScreen" owns an "XxxContract" and "XxxViewModel"; subordinate loading, empty, error, and section visuals use "XxxContent" or "XxxComponent".
- App state is limited to routes and cross-feature coordination.
- All quality gates are mandatory, including feature-UI platform boundaries, locale parity, and the 400-line production Kotlin limit.
- Default Android locales:
  "en", "zh-CN", "zh-Hant", "es", "pt-BR", "hi", "ur", "fr", "ja", "ko", "id", "th", "vi", "ms", and "fil".

The baseline deliberately uses packages inside a single Gradle module. Split modules only after build speed, ownership, reuse, or dependency boundaries justify the cost.
