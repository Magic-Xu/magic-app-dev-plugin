# Generated Workspace Layout

The generator produces:

~~~text
<slug>/
  <slug>.code-workspace
  <slug>-android/
    .app-factory/spec.json
    .git/
    AGENTS.md
    README.md
    app/
    docs/
      decisions/
      engineering/
      legal-source/
      product/
    gradle/
    scripts/sync_legal_site.py
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

- The Android repository owns the product specification and canonical legal source.
- The legal repository owns no private data. It is a publishable projection of "docs/legal-source/".
- "scripts/sync_legal_site.py" copies only the canonical legal-source tree and verifies the target marker before writing.
- The parent workspace is not a third Git repository.

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
