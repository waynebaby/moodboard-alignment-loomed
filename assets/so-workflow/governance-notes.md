# Moodboard Alignment Governance Notes

## Bound Runtime

- runtime channel: `released`
- resolved version: `0.2.126`
- checked-in authority: `assets/so-workflow/so-package-lock.json`
- reproducible fresh guide command: `dotnet .\\so.dll --guide --lang en`
- runtime proof summary: the published `0.2.126` bundle was restored and the fresh guide command completed successfully during this enhancement pass

> 运行时 proof 与 compile 审计文件保存在 Skill 目录外，它们是环境局部产物，不作为仓库内可移植路径承诺。仓库内只保留可复现所需的版本锁、命令形态和结果摘要。

## Runtime Proof Notes

1. 已从发布包恢复 `Techne.Loom.SkillOrchestrator`、`Techne.Loom.Common`、`Techne.Loom.Abstractions` 三件套，并放入统一运行时目录。
2. 当前发布包布局实际位于 `lib/net9.0`，而不是旧假设中的 `tools/net10.0/any`。
3. 当前发布包在提取态未暴露 `so.deps.json`，因此 fresh guide 证明采用包内可运行入口 `dotnet .\\so.dll --guide --lang en` 完成。
4. 后续若包布局再次变化，应先更新 `so-package-lock.json` 注释和本文件，再继续新的 enhancement pass。

## Source Template Boundary

- checked-in `assets/so-workflow/so-template.json` is source-only authority for review and compile
- official `run` / `resume` must target an external runtime copy outside the repository
- even though the JSON carries runtime-shaped fields required by the current SO schema, maintainers must not advance state in the checked-in copy

## Local Weave-Out

- dedicated local subagent: `assets/agents/moodboard-alignment-ck-state-classifier.agent.md`
- purpose: 统一处理 CK 状态识别、项目类型推断、触发词证据和 revision 上下文缺失判断
