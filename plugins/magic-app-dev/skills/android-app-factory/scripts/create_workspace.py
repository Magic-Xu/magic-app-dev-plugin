#!/usr/bin/env python3
"""Create a paired Android app and public legal-site workspace."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import date
from pathlib import Path
from typing import Iterable


ANDROID_LOCALE_FOLDERS = {
    "en": "values",
    "zh-CN": "values-zh-rCN",
    "zh-Hant": "values-b+zh+Hant",
    "es": "values-es",
    "pt-BR": "values-pt-rBR",
    "hi": "values-hi",
    "ur": "values-ur",
    "fr": "values-fr",
    "ja": "values-ja",
    "ko": "values-ko",
    "id": "values-in",
    "th": "values-th",
    "vi": "values-vi",
    "ms": "values-ms",
    "fil": "values-b+fil",
}
DEFAULT_ANDROID_LOCALES = tuple(ANDROID_LOCALE_FOLDERS)
SUPPORTED_LEGAL_LOCALES = ("en", "zh-CN")

ANDROID_STRINGS = {
    "en": ("Your app shell is ready.", "Try the state flow", "Interactions: %1$d"),
    "zh-CN": ("你的 App 空壳已经就绪。", "试用状态流", "交互次数：%1$d"),
    "zh-Hant": ("你的 App 空殼已經就緒。", "試用狀態流", "互動次數：%1$d"),
    "es": ("La estructura de tu app está lista.", "Probar el flujo de estado", "Interacciones: %1$d"),
    "pt-BR": ("A estrutura do app está pronta.", "Testar o fluxo de estado", "Interações: %1$d"),
    "hi": ("आपका ऐप ढांचा तैयार है।", "स्टेट फ़्लो आज़माएँ", "इंटरैक्शन: %1$d"),
    "ur": ("آپ کی ایپ کا بنیادی ڈھانچہ تیار ہے۔", "اسٹیٹ فلو آزمائیں", "تعاملات: %1$d"),
    "fr": ("La structure de votre app est prête.", "Tester le flux d’état", "Interactions : %1$d"),
    "ja": ("アプリの基本構成が準備できました。", "状態フローを試す", "操作回数: %1$d"),
    "ko": ("앱 기본 구성이 준비되었습니다.", "상태 흐름 시험", "상호작용: %1$d"),
    "id": ("Kerangka aplikasi Anda sudah siap.", "Coba alur status", "Interaksi: %1$d"),
    "th": ("โครงแอปของคุณพร้อมแล้ว", "ลองโฟลว์สถานะ", "การโต้ตอบ: %1$d"),
    "vi": ("Khung ứng dụng đã sẵn sàng.", "Thử luồng trạng thái", "Lượt tương tác: %1$d"),
    "ms": ("Rangka aplikasi anda sudah sedia.", "Cuba aliran keadaan", "Interaksi: %1$d"),
    "fil": ("Handa na ang balangkas ng app mo.", "Subukan ang state flow", "Mga interaction: %1$d"),
}

SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
PACKAGE_SEGMENT_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
STABLE_VERSION_PATTERN = re.compile(r"^[1-9][0-9]*\.[0-9]+\.[0-9]+$")


class FactoryError(RuntimeError):
    pass


def parse_csv(value: str) -> tuple[str, ...]:
    items = tuple(item.strip() for item in value.split(",") if item.strip())
    if not items:
        raise argparse.ArgumentTypeError("locale list must not be empty")
    if len(set(items)) != len(items):
        raise argparse.ArgumentTypeError("locale list contains duplicates")
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create sibling Android and public legal-site Git repositories."
    )
    parser.add_argument("--app-name", required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--application-id", required=True)
    parser.add_argument("--github-owner", required=True)
    parser.add_argument("--product-sentence-en", required=True)
    parser.add_argument("--product-sentence-zh", required=True)
    parser.add_argument("--parent-dir", required=True)
    parser.add_argument("--magic-platform-version", required=True)
    parser.add_argument("--app-repo-name")
    parser.add_argument("--legal-repo-name")
    parser.add_argument(
        "--android-locales",
        type=parse_csv,
        default=DEFAULT_ANDROID_LOCALES,
    )
    parser.add_argument(
        "--legal-locales",
        type=parse_csv,
        default=SUPPORTED_LEGAL_LOCALES,
    )
    parser.add_argument("--effective-date", default=date.today().isoformat())
    parser.add_argument("--no-git", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def require_nonempty(name: str, value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise FactoryError(f"{name} must not be empty")
    return normalized


def validate_package(application_id: str) -> None:
    parts = application_id.split(".")
    if len(parts) < 2 or not all(PACKAGE_SEGMENT_PATTERN.fullmatch(part) for part in parts):
        raise FactoryError(
            "application ID must contain at least two dot-separated Java identifiers"
        )


def validate_repo_name(label: str, value: str) -> None:
    if not REPO_PATTERN.fullmatch(value) or value in {".", ".."} or value.endswith(".git"):
        raise FactoryError(f"invalid {label}: {value}")


def validate_date(value: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise FactoryError("effective date must use YYYY-MM-DD") from error


def validate_stable_version(value: str) -> None:
    if not STABLE_VERSION_PATTERN.fullmatch(value):
        raise FactoryError(
            "Magic Android Platform version must be a released stable x.y.z version"
        )


def validate_locales(android_locales: Iterable[str], legal_locales: Iterable[str]) -> None:
    unknown_android = sorted(set(android_locales) - set(ANDROID_LOCALE_FOLDERS))
    if unknown_android:
        raise FactoryError(
            "unsupported Android locales: " + ", ".join(unknown_android)
        )
    unknown_legal = sorted(set(legal_locales) - set(SUPPORTED_LEGAL_LOCALES))
    if unknown_legal:
        raise FactoryError(
            "legal translations are not bundled for: " + ", ".join(unknown_legal)
        )
    if "en" not in legal_locales:
        raise FactoryError("English legal pages are required for root app-store URLs")


def run(command: list[str], cwd: Path, capture: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise FactoryError(
            f"command failed in {cwd}: {' '.join(command)}"
            + (f"\n{detail}" if detail else "")
        )
    return (result.stdout or "").strip()


def require_git_identity() -> None:
    for key in ("user.name", "user.email"):
        result = subprocess.run(
            ["git", "config", "--global", "--get", key],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0 or not result.stdout.strip():
            raise FactoryError(
                f"global Git {key} is missing; configure it before generating committed repositories"
            )


def write_text(root: Path, relative: str, content: str, executable: bool = False) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    if executable:
        path.chmod(0o755)


def xml_text(value: str) -> str:
    return html.escape(value, quote=True).replace("'", "\\'")


def kotlin_package_path(application_id: str) -> str:
    return application_id.replace(".", "/")


def app_strings_xml(app_name: str, locale: str) -> str:
    ready, action, count = ANDROID_STRINGS[locale]
    return f"""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{xml_text(app_name)}</string>
    <string name="home_ready">{xml_text(ready)}</string>
    <string name="home_primary_action">{xml_text(action)}</string>
    <string name="home_interaction_count">{xml_text(count)}</string>
</resources>
"""


def settings_gradle(app_name: str) -> str:
    return f"""pluginManagement {{
    repositories {{
        google {{
            content {{
                includeGroupByRegex("com\\\\.android.*")
                includeGroupByRegex("com\\\\.google.*")
                includeGroupByRegex("androidx.*")
            }}
        }}
        mavenCentral()
        gradlePluginPortal()
    }}
}}

plugins {{
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}}

dependencyResolutionManagement {{
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {{
        google {{
            content {{
                includeGroupByRegex("com\\\\.android.*")
                includeGroupByRegex("com\\\\.google.*")
                includeGroupByRegex("androidx.*")
            }}
        }}
        mavenCentral()
    }}
}}

rootProject.name = {json.dumps(app_name)}
include(":app")
"""


def root_build_gradle(platform_version: str) -> str:
    return f"""plugins {{
    id("io.github.magic-xu.magic-android-application") version {json.dumps(platform_version)} apply false
    id("io.github.magic-xu.magic-android-compose") version {json.dumps(platform_version)} apply false
    id("io.github.magic-xu.magic-android-pulse") version {json.dumps(platform_version)} apply false
    id("io.github.magic-xu.magic-android-quality") version {json.dumps(platform_version)} apply false
}}
"""


def app_build_gradle(application_id: str) -> str:
    return f"""plugins {{
    id("io.github.magic-xu.magic-android-application")
    id("io.github.magic-xu.magic-android-compose")
    id("io.github.magic-xu.magic-android-pulse")
    id("io.github.magic-xu.magic-android-quality")
}}

android {{
    namespace = {json.dumps(application_id)}

    defaultConfig {{
        applicationId = {json.dumps(application_id)}
        versionCode = 1
        versionName = "1.0.0"
    }}
}}
"""


def manifest_xml() -> str:
    return """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="false"
        android:label="@string/app_name"
        android:localeConfig="@xml/locales_config"
        android:supportsRtl="true"
        android:theme="@style/Theme.App">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.App">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
"""


def locales_config(locales: Iterable[str]) -> str:
    entries = "\n".join(f'    <locale android:name="{locale}" />' for locale in locales)
    return f"""<?xml version="1.0" encoding="utf-8"?>
<locale-config xmlns:android="http://schemas.android.com/apk/res/android">
{entries}
</locale-config>
"""


def main_activity(application_id: str) -> str:
    return f"""package {application_id}

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import {application_id}.core.designsystem.AppTheme
import {application_id}.feature.home.ui.HomeRoute

class MainActivity : ComponentActivity() {{
    override fun onCreate(savedInstanceState: Bundle?) {{
        super.onCreate(savedInstanceState)
        setContent {{
            AppTheme {{
                HomeRoute()
            }}
        }}
    }}
}}
"""


def app_theme(application_id: str) -> str:
    return f"""package {application_id}.core.designsystem

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

private val AppColorScheme = lightColorScheme(
    primary = Color(0xFF3459E6),
    onPrimary = Color.White,
    background = Color(0xFFF8F9FF),
    onBackground = Color(0xFF191B23),
    surface = Color.White,
    onSurface = Color(0xFF191B23),
)

object AppSpacing {{
    val screen = 24.dp
    val content = 16.dp
    val compact = 8.dp
}}

@Composable
fun AppTheme(content: @Composable () -> Unit) {{
    MaterialTheme(
        colorScheme = AppColorScheme,
        content = content,
    )
}}
"""


def home_contract(application_id: str) -> str:
    return f"""package {application_id}.feature.home.contract

import com.magic.mvicore.contract.MviState
import com.magic.mvicore.contract.MviUiIntent
import com.magic.mvicore.contract.UiEffect

data class HomeState(
    val interactionCount: Int = 0,
) : MviState

sealed interface HomeIntent : MviUiIntent {{
    data object OnPrimaryClick : HomeIntent
}}

sealed interface HomeEffect : UiEffect
"""


def home_mutation(application_id: str) -> str:
    return f"""package {application_id}.feature.home.presentation

import com.magic.mvicore.contract.MviMutation
import com.magic.mvicore.contract.PulseMutationReducer
import com.magic.mvicore.contract.ReduceOutcome
import {application_id}.feature.home.contract.HomeEffect
import {application_id}.feature.home.contract.HomeState

sealed interface HomeMutation : MviMutation {{
    data object InteractionIncremented : HomeMutation
}}

object HomeMutationReducer : PulseMutationReducer<HomeState, HomeMutation, HomeEffect> {{
    override fun reduce(
        previous: HomeState,
        mutation: HomeMutation,
    ): ReduceOutcome<HomeState, HomeEffect> = when (mutation) {{
        HomeMutation.InteractionIncremented -> ReduceOutcome.Changed(
            previous.copy(interactionCount = previous.interactionCount + 1),
        )
    }}
}}
"""


def home_view_model(application_id: str) -> str:
    return f"""package {application_id}.feature.home.presentation

import com.magic.mvicore.android.PulseIntentContext
import com.magic.mvicore.android.PulseIntentExecutionDecision
import com.magic.mvicore.android.PulseSplitStoreViewModel
import com.magic.mvicore.android.PulseUiIntentExecutor
import {application_id}.feature.home.contract.HomeEffect
import {application_id}.feature.home.contract.HomeIntent
import {application_id}.feature.home.contract.HomeState

class HomeViewModel : PulseSplitStoreViewModel<
    HomeState,
    HomeIntent,
    HomeMutation,
    HomeEffect,
    >(
    initialState = HomeState(),
    mutationReducer = HomeMutationReducer,
    uiIntentExecutor = HomeIntentExecutor,
) {{
    fun accept(intent: HomeIntent) {{
        trySend(intent)
    }}
}}

private object HomeIntentExecutor : PulseUiIntentExecutor<
    HomeState,
    HomeIntent,
    HomeMutation,
    > {{
    override suspend fun execute(
        intent: HomeIntent,
        context: PulseIntentContext<HomeState, HomeMutation>,
    ): PulseIntentExecutionDecision {{
        when (intent) {{
            HomeIntent.OnPrimaryClick -> context.mutate(HomeMutation.InteractionIncremented)
        }}
        return PulseIntentExecutionDecision.Completed
    }}
}}
"""


def home_screen(application_id: str) -> str:
    return f"""package {application_id}.feature.home.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.lifecycle.viewmodel.compose.viewModel
import com.magic.mvicore.android.compose.collectStateAsStateWithLifecycle
import {application_id}.R
import {application_id}.core.designsystem.AppSpacing
import {application_id}.feature.home.contract.HomeIntent
import {application_id}.feature.home.contract.HomeState
import {application_id}.feature.home.presentation.HomeViewModel

@Composable
fun HomeRoute(viewModel: HomeViewModel = viewModel()) {{
    val lifecycleOwner = LocalLifecycleOwner.current
    val state by viewModel.collectStateAsStateWithLifecycle(lifecycleOwner)
    HomeScreen(
        state = state,
        onIntent = viewModel::accept,
    )
}}

@Composable
fun HomeScreen(
    state: HomeState,
    onIntent: (HomeIntent) -> Unit,
) {{
    Surface(modifier = Modifier.fillMaxSize()) {{
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(AppSpacing.screen),
            verticalArrangement = Arrangement.spacedBy(
                AppSpacing.content,
                Alignment.CenterVertically,
            ),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {{
            Text(text = stringResource(R.string.app_name))
            Text(text = stringResource(R.string.home_ready))
            Text(
                text = stringResource(
                    R.string.home_interaction_count,
                    state.interactionCount,
                )
            )
            Button(onClick = {{ onIntent(HomeIntent.OnPrimaryClick) }}) {{
                Text(text = stringResource(R.string.home_primary_action))
            }}
        }}
    }}
}}
"""


def home_mutation_reducer_test(application_id: str) -> str:
    return f"""package {application_id}.feature.home.presentation

import {application_id}.feature.home.contract.HomeState
import com.magic.mvicore.contract.PulseReducer
import com.magic.mvicore.testing.runPulseTest
import org.junit.Assert.assertEquals
import org.junit.Test

class HomeMutationReducerTest {{
    @Test
    fun mutationIncrementsInteractionCount() = runPulseTest {{
        val store = testStore(
            initialState = HomeState(interactionCount = 2),
            reducer = PulseReducer(HomeMutationReducer::reduce),
        )
        store.send(HomeMutation.InteractionIncremented)
        runCurrent()

        assertEquals(3, store.state.value.interactionCount)
        store.failureProbe.assertEmpty()
    }}
}}
"""


def app_agents(android_locales: Iterable[str]) -> str:
    locale_text = ", ".join(android_locales)
    return f"""# Android App Collaboration Rules

## Product boundary

- Define the smallest complete V1 loop before implementing product features.
- Do not add accounts, servers, cloud sync, ads, billing, analytics, or sensitive permissions without explicit product scope and a legal-policy update.

## Architecture

- UI uses Jetpack Compose.
- Page state uses MVI and pulse.
- Define XxxContract, XxxState, XxxIntent, XxxEffect, typed XxxMutation, and XxxViewModel before page behavior.
- Every independent page named `XxxScreen` owns an `XxxContract` and `XxxViewModel`. Subordinate loading, empty, error, and section visuals use `XxxContent` or `XxxComponent` instead of `Screen`.
- The app Store owns routes and app-level coordination only; it must not absorb feature state.
- Keep the dependency direction `app -> feature -> domain -> core`. Features must not depend on app or sibling features.
- Magic Android Platform quality rules are mandatory and cannot be disabled or relaxed.
- Composables render state and dispatch intents. Keep business rules, navigation decisions, system calls, file IO, and network IO outside Composables.
- Keep image, media, storage, network, and other platform capabilities behind interfaces.

## Resources

- Put user-visible text in Android string resources.
- Update every supported locale together: {locale_text}.
- Put shared color, typography, spacing, radius, and size values in the design system.

## Legal source

- Canonical public-site and legal files live in docs/legal-source.
- Run scripts/sync_legal_site.py after approved legal changes.
- Update the Privacy Policy before releasing capabilities that change data collection, sharing, storage, permissions, ads, billing, analytics, or accounts.

## Git

- Do not edit on main or master. Create or continue a task branch.
- Keep changes scoped and validate the smallest relevant unit test and compile task.
"""


def sync_legal_script(legal_repo_name: str) -> str:
    return f'''#!/usr/bin/env python3
"""Copy canonical legal-site files into the sibling public repository."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?")
    args = parser.parse_args()

    app_root = Path(__file__).resolve().parents[1]
    source = app_root / "docs" / "legal-source"
    target = (
        Path(args.target).expanduser().resolve()
        if args.target
        else (app_root.parent / {legal_repo_name!r}).resolve()
    )

    marker_path = target / ".app-factory-legal.json"
    if not target.is_dir() or not marker_path.is_file():
        raise SystemExit(f"Refusing to sync: target marker missing in {{target}}")

    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    if marker.get("repository") != {legal_repo_name!r}:
        raise SystemExit("Refusing to sync: target repository marker does not match")

    for source_path in sorted(source.rglob("*")):
        if not source_path.is_file():
            continue
        relative = source_path.relative_to(source)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
        print(f"synced {{relative}}")

    print(f"Legal site synced to {{target}}. Review and commit it separately.")


if __name__ == "__main__":
    main()
'''


def app_readme(app_name: str, product_sentence: str, legal_repo_name: str) -> str:
    return f"""# {app_name}

{product_sentence}

## Build

Requires JDK 17 or newer. Android Studio's bundled JBR is supported.

~~~bash
./gradlew check :app:assembleDebug :app:assembleRelease :app:bundleRelease
~~~

## Legal site

Canonical website and legal files are stored in "docs/legal-source".

Sync them into the sibling public repository:

~~~bash
python3 scripts/sync_legal_site.py ../{legal_repo_name}
~~~
"""


def product_requirements(
    app_name: str,
    sentence_en: str,
    sentence_zh: str,
) -> str:
    return f"""# {app_name} V1 Requirements

## Product sentence

- English: {sentence_en}
- 简体中文：{sentence_zh}

## Before feature implementation

Define:

- The shortest complete path from user intent to delivered value.
- Explicit V1 inclusions and exclusions.
- Local, exported, logged, and network data.
- Required Android system capabilities.

The generated ready screen validates architecture and compilation only; it is not the product's V1 loop.
"""


def architecture_doc() -> str:
    return """# Architecture

The starter begins with one Gradle application module and package boundaries:

- "app": route state, composition, and cross-feature effect coordination only.
- "core/designsystem": shared visual tokens and theme.
- "feature/<feature>/contract": State, Intent, and Effect.
- "feature/<feature>/presentation": typed mutations, reducer, intent executor, and ViewModel.
- "feature/<feature>/ui": state rendering and intent dispatch.
- "domain": stable business models and coordinators shared across features.
- "core": business-independent platform, storage, network, UI, and design-system capabilities.

Dependency direction is `app -> feature -> domain -> core`. A feature cannot import app or a sibling
feature. Each independent page named `XxxScreen` has its own `XxxContract` and `XxxViewModel`;
subordinate loading, empty, error, and section visuals use `XxxContent` or `XxxComponent`. An
app-level Store is never a container for feature state. Platform quality checks enforce these rules,
locale parity, package paths, and the 400-line production Kotlin limit without consumer exemptions.

Split Gradle modules only when build speed, ownership, reuse, or enforceable dependency boundaries justify the added cost.
"""


def testing_doc() -> str:
    return """# Testing

Minimum validation for the generated shell:

~~~bash
./gradlew check :app:assembleDebug :app:assembleRelease :app:bundleRelease
~~~

For later changes, run the narrowest relevant unit tests first, then compile the affected variant. Device behavior requires an emulator or physical-device check.
"""


def html_document(lang: str, title: str, css_href: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="{html.escape(lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="{html.escape(css_href)}">
</head>
<body>
{body}
</body>
</html>
"""


def site_css() -> str:
    return """:root {
  color-scheme: light dark;
  --background: #f6f7fb;
  --surface: #ffffff;
  --text: #191b23;
  --muted: #5e6472;
  --primary: #3459e6;
  --line: #dde1eb;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root {
    --background: #111318;
    --surface: #1b1e25;
    --text: #f5f6fa;
    --muted: #b7bdc9;
    --primary: #91a7ff;
    --line: #353a45;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--background); color: var(--text); }
main { width: min(780px, calc(100% - 32px)); margin: 0 auto; padding: 56px 0 72px; }
h1 { margin: 0 0 12px; font-size: clamp(2rem, 7vw, 3.4rem); line-height: 1.05; }
h2 { margin-top: 32px; font-size: 1.25rem; }
p, li { color: var(--muted); line-height: 1.7; }
a { color: var(--primary); }
.meta, .card { border: 1px solid var(--line); background: var(--surface); border-radius: 18px; padding: 18px; }
.grid { display: grid; gap: 14px; margin-top: 28px; }
.card { display: block; color: var(--text); text-decoration: none; }
.card strong { display: block; margin-bottom: 6px; }
.back { display: inline-block; margin-bottom: 28px; }
footer { margin-top: 40px; color: var(--muted); font-size: .875rem; }
"""


def legal_home(
    app_name: str,
    sentence: str,
    locale: str,
    effective_date: str,
    github_owner: str,
    legal_repo_name: str,
    nested: bool,
) -> str:
    is_zh = locale == "zh-CN"
    prefix = "../" if nested else "./"
    if nested:
        language_link = "../en/" if is_zh else "../zh-CN/"
    else:
        language_link = "./en/" if is_zh else "./zh-CN/"
    language_label = "English" if is_zh else "简体中文"
    privacy_label = "隐私政策" if is_zh else "Privacy Policy"
    agreement_label = "用户协议" if is_zh else "User Agreement"
    feedback_label = "问题反馈" if is_zh else "Support and feedback"
    body = f"""  <main>
    <h1>{html.escape(app_name)}</h1>
    <p>{html.escape(sentence)}</p>
    <div class="grid">
      <a class="card" href="./privacy-policy.html"><strong>{privacy_label}</strong></a>
      <a class="card" href="./user-agreement.html"><strong>{agreement_label}</strong></a>
      <a class="card" href="{html.escape(language_link)}"><strong>{language_label}</strong></a>
      <a class="card" href="https://github.com/{html.escape(github_owner)}/{html.escape(legal_repo_name)}/issues"><strong>{feedback_label}</strong></a>
    </div>
    <footer>{html.escape(effective_date)}</footer>
  </main>"""
    return html_document(locale, app_name, f"{prefix}assets/site.css", body)


def privacy_page(app_name: str, locale: str, effective_date: str, nested: bool) -> str:
    css = "../assets/site.css" if nested else "./assets/site.css"
    if locale == "zh-CN":
        body = f"""  <main>
    <a class="back" href="./index.html">返回</a>
    <h1>{html.escape(app_name)} 隐私政策</h1>
    <div class="meta">生效日期：{html.escape(effective_date)}</div>
    <p>当前初始版本被设计为本地优先的最小应用空壳。</p>
    <h2>1. 数据收集</h2>
    <p>当前版本不要求账号，不收集或上传个人信息，也不包含分析、崩溃上报或广告 SDK。</p>
    <h2>2. 本地数据</h2>
    <p>当前版本仅在设备上运行，不包含服务端或云端上传能力。</p>
    <h2>3. 权限</h2>
    <p>当前版本不请求敏感运行时权限。</p>
    <h2>4. 广告与付费</h2>
    <p>当前版本不包含广告、应用内购买或订阅。</p>
    <h2>5. 数据共享与删除</h2>
    <p>当前版本不会出售或共享个人数据。你可以通过清除应用存储或卸载应用来删除本地数据。</p>
    <h2>6. 变更</h2>
    <p>如果后续版本增加账号、上传、分析、广告、付费或新的系统权限，本政策将在发布前更新。</p>
  </main>"""
        return html_document(locale, f"{app_name} 隐私政策", css, body)

    body = f"""  <main>
    <a class="back" href="./index.html">Back</a>
    <h1>{html.escape(app_name)} Privacy Policy</h1>
    <div class="meta">Effective date: {html.escape(effective_date)}</div>
    <p>The initial release is a minimal local-first application shell.</p>
    <h2>1. Data collection</h2>
    <p>The current version requires no account, collects or uploads no personal information, and includes no analytics, crash-reporting, or advertising SDK.</p>
    <h2>2. Local data</h2>
    <p>The current version runs on the device and includes no server or cloud-upload capability.</p>
    <h2>3. Permissions</h2>
    <p>The current version requests no sensitive runtime permission.</p>
    <h2>4. Advertising and payments</h2>
    <p>The current version includes no advertising, in-app purchase, or subscription.</p>
    <h2>5. Sharing and deletion</h2>
    <p>The current version does not sell or share personal data. Local data can be removed by clearing app storage or uninstalling the app.</p>
    <h2>6. Changes</h2>
    <p>This policy will be updated before a release adds accounts, upload, analytics, advertising, payments, or new system permissions.</p>
  </main>"""
    return html_document("en", f"{app_name} Privacy Policy", css, body)


def agreement_page(app_name: str, locale: str, effective_date: str, nested: bool) -> str:
    css = "../assets/site.css" if nested else "./assets/site.css"
    if locale == "zh-CN":
        body = f"""  <main>
    <a class="back" href="./index.html">返回</a>
    <h1>{html.escape(app_name)} 用户协议</h1>
    <div class="meta">生效日期：{html.escape(effective_date)}</div>
    <p>使用 {html.escape(app_name)} 即表示你同意在应用明确提供的功能范围内使用它。</p>
    <h2>1. 产品范围</h2>
    <p>当前版本是最小应用空壳，不提供账号、云服务、自动化操作、广告或付费能力。</p>
    <h2>2. 用户责任</h2>
    <p>你应依法使用本应用，并对自己处理、保存或分享的内容负责。</p>
    <h2>3. 可用性</h2>
    <p>应用会尽力保持稳定，但不保证在所有设备和系统版本上始终可用或表现完全一致。</p>
    <h2>4. 协议变更</h2>
    <p>协议会随产品能力变化更新，并在本页面标注新的生效日期。</p>
  </main>"""
        return html_document(locale, f"{app_name} 用户协议", css, body)

    body = f"""  <main>
    <a class="back" href="./index.html">Back</a>
    <h1>{html.escape(app_name)} User Agreement</h1>
    <div class="meta">Effective date: {html.escape(effective_date)}</div>
    <p>By using {html.escape(app_name)}, you agree to use it within the functionality explicitly provided by the app.</p>
    <h2>1. Product scope</h2>
    <p>The current version is a minimal app shell and provides no account, cloud service, automated action, advertising, or payment capability.</p>
    <h2>2. Your responsibility</h2>
    <p>You must use the app lawfully and remain responsible for content you process, save, or share.</p>
    <h2>3. Availability</h2>
    <p>The app aims to remain stable but does not guarantee uninterrupted or identical behavior across every device and operating-system version.</p>
    <h2>4. Changes</h2>
    <p>This agreement may change as product capabilities change. A new effective date will be shown on this page.</p>
  </main>"""
    return html_document("en", f"{app_name} User Agreement", css, body)


def legal_files(spec: dict) -> dict[str, str]:
    app = spec["app"]
    repos = spec["repositories"]
    effective_date = spec["legal"]["effectiveDate"]
    files = {
        ".nojekyll": "",
        ".app-factory-legal.json": json.dumps(
            {
                "schemaVersion": 1,
                "repository": repos["legal"],
                "generatedBy": "android-app-factory",
            },
            ensure_ascii=False,
            indent=2,
        ),
        "assets/site.css": site_css(),
        "index.html": legal_home(
            app["name"],
            app["productSentence"]["en"],
            "en",
            effective_date,
            spec["github"]["owner"],
            repos["legal"],
            nested=False,
        ),
        "privacy-policy.html": privacy_page(
            app["name"], "en", effective_date, nested=False
        ),
        "user-agreement.html": agreement_page(
            app["name"], "en", effective_date, nested=False
        ),
        "404.html": html_document(
            "en",
            f"{app['name']} - Not Found",
            "./assets/site.css",
            '  <main><h1>Page not found</h1><p><a href="./index.html">Return home</a></p></main>',
        ),
        "README.md": f"""# {app['name']} Website and Legal Pages

Public GitHub Pages content for {app['name']}.

- Homepage: "index.html"
- Privacy Policy: "privacy-policy.html"
- User Agreement: "user-agreement.html"
- Localized routes: "en/" and "zh-CN/"

GitHub Pages source: "main" branch, repository root.
""",
    }

    if "en" in spec["legal"]["locales"]:
        files["en/index.html"] = legal_home(
            app["name"],
            app["productSentence"]["en"],
            "en",
            effective_date,
            spec["github"]["owner"],
            repos["legal"],
            nested=True,
        )
        files["en/privacy-policy.html"] = privacy_page(
            app["name"], "en", effective_date, nested=True
        )
        files["en/user-agreement.html"] = agreement_page(
            app["name"], "en", effective_date, nested=True
        )
    if "zh-CN" in spec["legal"]["locales"]:
        files["zh-CN/index.html"] = legal_home(
            app["name"],
            app["productSentence"]["zh-CN"],
            "zh-CN",
            effective_date,
            spec["github"]["owner"],
            repos["legal"],
            nested=True,
        )
        files["zh-CN/privacy-policy.html"] = privacy_page(
            app["name"], "zh-CN", effective_date, nested=True
        )
        files["zh-CN/user-agreement.html"] = agreement_page(
            app["name"], "zh-CN", effective_date, nested=True
        )
    return files


def app_files(spec: dict) -> dict[str, str]:
    app = spec["app"]
    repos = spec["repositories"]
    application_id = app["applicationId"]
    package_path = kotlin_package_path(application_id)
    files = {
        ".gitignore": """.gradle/
.idea/
.kotlin/
**/build/
local.properties
*.iml
*.jks
*.keystore
""",
        ".app-factory/spec.json": json.dumps(spec, ensure_ascii=False, indent=2),
        "AGENTS.md": app_agents(app["androidLocales"]),
        "README.md": app_readme(
            app["name"],
            app["productSentence"]["en"],
            repos["legal"],
        ),
        "settings.gradle.kts": settings_gradle(app["name"]),
        "build.gradle.kts": root_build_gradle(spec["platform"]["version"]),
        "gradle.properties": """org.gradle.jvmargs=-Xmx2g -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
""",
        "app/build.gradle.kts": app_build_gradle(application_id),
        "app/proguard-rules.pro": "# Add project-specific R8 rules only when required.\n",
        "app/src/main/AndroidManifest.xml": manifest_xml(),
        "app/src/main/res/xml/locales_config.xml": locales_config(
            app["androidLocales"]
        ),
        "app/src/main/res/values/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.App" parent="android:style/Theme.Material.Light.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowLightStatusBar">true</item>
        <item name="android:navigationBarColor">@android:color/white</item>
    </style>
</resources>
""",
        "app/src/main/res/values-night/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.App" parent="android:style/Theme.Material.NoActionBar">
        <item name="android:fontFamily">sans</item>
        <item name="android:windowLightStatusBar">false</item>
        <item name="android:navigationBarColor">@android:color/black</item>
    </style>
</resources>
""",
        f"app/src/main/java/{package_path}/MainActivity.kt": main_activity(
            application_id
        ),
        f"app/src/main/java/{package_path}/core/designsystem/AppTheme.kt": app_theme(
            application_id
        ),
        f"app/src/main/java/{package_path}/feature/home/contract/HomeContract.kt": home_contract(
            application_id
        ),
        f"app/src/main/java/{package_path}/feature/home/presentation/HomeMutation.kt": home_mutation(
            application_id
        ),
        f"app/src/main/java/{package_path}/feature/home/presentation/HomeViewModel.kt": home_view_model(
            application_id
        ),
        f"app/src/main/java/{package_path}/feature/home/ui/HomeScreen.kt": home_screen(
            application_id
        ),
        f"app/src/test/java/{package_path}/feature/home/presentation/HomeMutationReducerTest.kt": home_mutation_reducer_test(
            application_id
        ),
        "scripts/sync_legal_site.py": sync_legal_script(repos["legal"]),
        "docs/product/v1-requirements.md": product_requirements(
            app["name"],
            app["productSentence"]["en"],
            app["productSentence"]["zh-CN"],
        ),
        "docs/engineering/architecture.md": architecture_doc(),
        "docs/engineering/testing.md": testing_doc(),
        "docs/decisions/README.md": """# Architecture Decisions

Add numbered decision records only for choices that materially constrain later work.
""",
        "docs/LEGAL_HOSTING.md": f"""# Legal Hosting

Public repository: "{spec['github']['owner']}/{repos['legal']}"

Expected Pages URLs:

- https://{spec['github']['owner'].lower()}.github.io/{repos['legal']}/
- https://{spec['github']['owner'].lower()}.github.io/{repos['legal']}/privacy-policy.html
- https://{spec['github']['owner'].lower()}.github.io/{repos['legal']}/user-agreement.html

The public repository is generated from "docs/legal-source".
""",
    }
    for locale in app["androidLocales"]:
        folder = ANDROID_LOCALE_FOLDERS[locale]
        files[f"app/src/main/res/{folder}/strings.xml"] = app_strings_xml(
            app["name"], locale
        )
    return files


def copy_gradle_wrapper(app_root: Path) -> None:
    skill_root = Path(__file__).resolve().parents[1]
    source = skill_root / "assets" / "gradle-wrapper"
    required = (
        "gradlew",
        "gradlew.bat",
        "gradle/wrapper/gradle-wrapper.jar",
        "gradle/wrapper/gradle-wrapper.properties",
    )
    for relative in required:
        source_path = source / relative
        if not source_path.is_file():
            raise FactoryError(f"bundled Gradle wrapper asset is missing: {source_path}")
        destination = app_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
    (app_root / "gradlew").chmod(0o755)


def initialize_git(repo: Path, commit_message: str) -> None:
    run(["git", "init", "-b", "main"], cwd=repo)
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", commit_message], cwd=repo)


def create_spec(args: argparse.Namespace) -> dict:
    app_name = require_nonempty("app name", args.app_name)
    slug = require_nonempty("slug", args.slug)
    if not SLUG_PATTERN.fullmatch(slug):
        raise FactoryError(
            "slug must use lowercase letters, digits, and single hyphens"
        )
    application_id = require_nonempty("application ID", args.application_id)
    validate_package(application_id)
    github_owner = require_nonempty("GitHub owner", args.github_owner)
    product_en = require_nonempty(
        "English product sentence", args.product_sentence_en
    )
    product_zh = require_nonempty(
        "Chinese product sentence", args.product_sentence_zh
    )
    validate_date(args.effective_date)
    platform_version = require_nonempty(
        "Magic Android Platform version", args.magic_platform_version
    )
    validate_stable_version(platform_version)
    validate_locales(args.android_locales, args.legal_locales)

    app_repo_name = args.app_repo_name or f"{slug}-android"
    legal_repo_name = args.legal_repo_name or f"{slug}-legal"
    validate_repo_name("Android repository name", app_repo_name)
    validate_repo_name("legal repository name", legal_repo_name)
    if app_repo_name == legal_repo_name:
        raise FactoryError("Android and legal repository names must differ")

    return {
        "schemaVersion": 2,
        "generatedBy": "android-app-factory",
        "platform": {
            "coordinates": "io.github.magic-xu:magic-android-platform-gradle-plugin",
            "version": platform_version,
            "qualityPolicy": "mandatory",
        },
        "app": {
            "name": app_name,
            "slug": slug,
            "applicationId": application_id,
            "productSentence": {
                "en": product_en,
                "zh-CN": product_zh,
            },
            "androidLocales": list(args.android_locales),
        },
        "github": {"owner": github_owner},
        "repositories": {
            "android": app_repo_name,
            "legal": legal_repo_name,
        },
        "legal": {
            "effectiveDate": args.effective_date,
            "locales": list(args.legal_locales),
            "capabilities": {
                "accounts": False,
                "serverUpload": False,
                "ads": False,
                "billing": False,
                "analytics": False,
                "sensitiveRuntimePermissions": [],
            },
        },
    }


def plan(spec: dict, parent: Path, init_git: bool) -> dict:
    workspace = parent / spec["app"]["slug"]
    return {
        "workspace": str(workspace),
        "androidRepository": {
            "path": str(workspace / spec["repositories"]["android"]),
            "remote": f"{spec['github']['owner']}/{spec['repositories']['android']}",
            "visibility": "private",
        },
        "legalRepository": {
            "path": str(workspace / spec["repositories"]["legal"]),
            "remote": f"{spec['github']['owner']}/{spec['repositories']['legal']}",
            "visibility": "public",
        },
        "initializeGit": init_git,
        "remoteMutation": False,
    }


def generate(args: argparse.Namespace) -> dict:
    spec = create_spec(args)
    parent = Path(args.parent_dir).expanduser().resolve()
    if not parent.is_dir():
        raise FactoryError(f"parent directory does not exist: {parent}")
    resolved_plan = plan(spec, parent, init_git=not args.no_git)
    if args.dry_run:
        return resolved_plan

    workspace = Path(resolved_plan["workspace"])
    if workspace.exists():
        raise FactoryError(f"destination already exists: {workspace}")
    if not args.no_git:
        require_git_identity()

    staging = parent / f".{spec['app']['slug']}.staging-{uuid.uuid4().hex[:10]}"
    if staging.exists():
        raise FactoryError(f"staging path unexpectedly exists: {staging}")

    try:
        app_root = staging / spec["repositories"]["android"]
        legal_root = staging / spec["repositories"]["legal"]
        app_root.mkdir(parents=True)
        legal_root.mkdir(parents=True)

        generated_legal_files = legal_files(spec)
        for relative, content in app_files(spec).items():
            write_text(
                app_root,
                relative,
                content,
                executable=relative == "scripts/sync_legal_site.py",
            )
        copy_gradle_wrapper(app_root)

        for relative, content in generated_legal_files.items():
            write_text(legal_root, relative, content)
            write_text(app_root / "docs" / "legal-source", relative, content)

        write_text(
            staging,
            f"{spec['app']['slug']}.code-workspace",
            json.dumps(
                {
                    "folders": [
                        {"path": spec["repositories"]["android"]},
                        {"path": spec["repositories"]["legal"]},
                    ],
                    "settings": {},
                },
                indent=2,
            ),
        )

        if not args.no_git:
            initialize_git(app_root, "chore: initialize Android app shell")
            initialize_git(legal_root, "chore: initialize public app website")

        os.replace(staging, workspace)
    except BaseException:
        if staging.exists():
            shutil.rmtree(staging)
        raise

    return resolved_plan


def main() -> int:
    try:
        args = parse_args()
        result = generate(args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except FactoryError as error:
        print(f"android-app-factory: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
