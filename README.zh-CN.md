# App Development Skills

[English](README.md) | 简体中文

这个仓库用于沉淀从 app 开发过程中提炼出来的可复用 Codex skills。这里的 skill 必须保持产品无关：可以沉淀强工程流程，但不能依赖某个具体 app 的名称、包名、仓库、截图、商店文案或发布历史。

## Skill 收录标准

只有满足这些条件，才适合放进这个仓库：

- 能在多个 app 之间复用
- 足够具体，能改变 agent 的实际行为
- 足够精简，不浪费上下文
- 不包含具体 app 的产品事实
- 来自重复工作流或真实踩坑

不要把项目笔记、一次性 PRD、产品文案、品牌资产或某个 app 专属发布清单做成 skill。

## Skills

| Skill | 用途 |
| --- | --- |
| `android-app-architecture-guardrails` | 约束 Android app 架构：MVI contract、Compose 纯渲染、资源化、设计 token、文件大小和验证门禁。 |
| `android-instrumentation-qa-guardrails` | 用可复现的 adb/instrumentation 证据验证 Android 真机/模拟器 UI 流程，避免人工启动造成假阳性。 |
| `github-pr-mainline-release` | 在功能验收后推送分支、创建或复用 PR、等待 GitHub Actions CI、安全合并并恢复本地 mainline。 |
| `indie-app-demand-research` | 从真实需求信号调研和排序独立 app 方向，并用本地优先、低运营成本约束做筛选。 |
| `local-first-android-app-builder` | 围绕最小 V1 闭环、本地优先、明确非目标、MVI/pulse/Compose 边界、隐私和验证来启动 Android app。 |

## 本地安装

把需要的 skill 复制或软链到：

```bash
~/.codex/skills/
```

示例：

```bash
ln -s /path/to/app-dev-skills/android-app-architecture-guardrails ~/.codex/skills/android-app-architecture-guardrails
```

这个仓库作为 source of truth；全局安装可以直接指向本仓库里的 skill 目录。

## 仓库结构

每个 skill 位于仓库根目录：

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/      # 可选
```

`SKILL.md` 要保持精简。只有需要按任务条件加载的细节，才放进 `references/`。

## 维护规则

- frontmatter 的 `name` 必须等于目录名。
- description 要足够准确，能正确触发，但不能宽到污染无关任务。
- `agents/openai.yaml` 的 default prompt 要和 skill 名保持一致。
- 提交前移除 app 名称、包名、仓库名、私有链接和发布专属细节。
- 新增或修改 skill 后要做校验。
