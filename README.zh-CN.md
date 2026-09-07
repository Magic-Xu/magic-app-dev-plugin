# Magic App Dev

[English](README.md) | 简体中文

供多个产品复用的 Codex 工作流插件：需求调研 → 产品规划与设计评审 → Android 开发与验证 → 主干合并 → 首次上架/版本更新 → 数据与稳定性分析 → 迭代效果验证。按当前任务进入，不要求每次从头走完整流程。

## 安装与更新

```bash
codex plugin marketplace add Magic-Xu/magic-app-dev-plugin --ref main
codex plugin add magic-app-dev@magic-app-dev-plugin
```

后续更新：

```bash
codex plugin marketplace upgrade magic-app-dev-plugin
codex plugin add magic-app-dev@magic-app-dev-plugin
```

安装或更新后开启一个新的 Codex 任务，以加载当前插件版本。

## 怎么选

所有入口的显示名统一为 **Magic · 中文任务名**，便于在 Skill 列表中辨认。也可以直接用下表中的 `$<skill-id>` 指定。具体列表的搜索匹配方式由 Codex 客户端决定。

- 不确定该用哪个：选 **Magic · 开发与迭代**，说明当前目标。
- “上架前全盘审查这个版本，修复问题并清理过时内容”：选 **Magic · 版本发布审查与修复**。从实际发布基线核验累计需求、功能交互、架构实现和发布证据；仅要求审查时保持只读，不确定项汇总交给用户决定。
- “上传 AAB、更新版本信息，看看商店要不要改”：选 **Magic · Google Play 发版**。首次上架和只更新商店也使用这个入口。
- “看看这次改动上线后有没有效果”：选产品数据分析或稳定性分析，复用原来的指标、基线和观察窗口。

| 显示名 | 稳定调用 ID | 用途 |
| --- | --- | --- |
| Magic · 需求调研 | `indie-app-demand-research` | 验证真实需求、竞品与分发机会，确定下一步验证。 |
| Magic · 产品规划 | `local-first-android-app-builder` | 明确用户闭环、范围、数据与收费边界，以及设计/验收输入。 |
| Magic · 创建项目 | `android-app-factory` | 创建 Android 与法律站点双仓，验证工程基线，带入设计评审规则。 |
| Magic · 开发与迭代 | `app-end-to-end-delivery` | 不确定用哪个 Skill 时从这里开始；按当前阶段衔接相关工作。 |
| Magic · 真机验证 | `android-instrumentation-qa-guardrails` | 以可复现设备证据验证交互、系统能力和生命周期。 |
| Magic · 设备常亮 | `android-device-keep-awake` | 仅在明确要求时，让指定 Android 设备在开发任务中常亮并可恢复。 |
| Magic · 版本发布审查与修复 | `app-release-review` | 上架前核验累计需求、跨功能冲突和实现，按授权修复、清理并验证发布条件；也支持明确限定范围的检查。 |
| Magic · 合并主干 | `github-pr-mainline-release` | 按授权把已验收改动经适用 PR/CI 门禁合入主干，同步并精确清理。 |
| Magic · Google Play 发版 | `google-play-release` | 首次上架、AAB 更新或商店单独更新；评估无需/局部/全面刷新，保存核验后交给用户送审。 |
| Magic · 产品数据分析 | `app-product-analytics` | 分析获客、留存、漏斗和变现，支持迭代效果验证及项目约定的报告位置。 |
| Magic · 稳定性分析 | `app-stability-analysis` | 诊断 Crash、ANR 与版本回归，检查修复后的恢复效果。 |

## 项目如何接入

复用项目现有的文档索引作为轻量来源地图，链接产品事实、设计源、工程门禁、商店/发布记录和指标定义。Factory 新项目会带入这一索引与设计评审规则；已有项目按需要补齐，不批量迁移目录或自动改写项目规则。

项目的功能排除项、收费/广告、数据处理、语言与国家、构建脚本和送审权限属于项目自身。插件不携带某个 app 的账号、包名、手机或素材。使用 [项目上下文约定](plugins/magic-app-dev/skills/app-end-to-end-delivery/references/project-context.md) 和 [迭代效果衔接](plugins/magic-app-dev/skills/app-end-to-end-delivery/references/iteration-outcomes.md) 维护必要交接，不增加一套平行管理系统。

用户可见变化先审查具体设计，再实现已确认内容。版本/架构只读审查与分析本身不授权修改代码。合并、Console 写入和发布按各自的授权执行；Google Play 默认由用户审查变化后的设计/文案并完成最终送审、发布，所有轨道一致。未来观察窗口不会自动创建定时任务。

报告目的地遵循用户要求或项目约定，未配置时保留飞书默认。飞书/其他文档工具及产物审查 Skill 不随此插件打包，使用前检查可用性；目的地不可用时完成分析并说明交付缺口，不把本地草稿说成已交付的外部报告。

## 开发与验证

```bash
git clone https://github.com/Magic-Xu/magic-app-dev-plugin.git
cd magic-app-dev-plugin
```

在 Git 工作区维护源码，通过 GitHub `main` 分发已验收版本。日常安装保持使用「安装与更新」中的 GitHub 来源；本地改动和 feature 分支需要合入主干并更新插件后才会生效，不把开发目录注册为日常更新源。

源码在 `plugins/magic-app-dev/skills/`。入口只保留选择和关键约束；实现、设计、整版本审查、首次上架等细节按需加载引用文件。需求核对、架构与状态、修复清理和风险验证统一由版本发布审查维护；开发中的局部检查复用其专项参考。

```bash
python3 -m pip install -r tools/plugin/requirements.txt
python3 -B -m unittest discover -s tools/plugin/tests -p 'test_*.py'
python3 -B tools/plugin/validate_skills.py plugins/magic-app-dev
python3 -B tools/plugin/validate_release.py --repo-root . --plugin-root plugins/magic-app-dev --base-ref origin/main
```

包校验覆盖 Skill 元数据、命名、默认调用、局部链接、具名依赖引用和版本递增；CI 执行相同检查。修改 Factory 生成结果时，另外运行其完整生成/构建验收。

[工作流场景评审](tools/plugin/workflow-scenarios.md) 覆盖新产品、小修、大改版、整版本审查、首次上架、商店单独更新、断点续办、数据分析与效果验证。它是行为评估输入及评分标准；静态校验通过不代表模型行为评估已通过。
