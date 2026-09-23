# Moodboard Alignment Governance Notes

## Bound Runtime

- runtime channel: `released`
- resolved version: `0.3.318`
- checked-in authority: `assets/so-workflow/so-package-lock.json`
- runtime mode: `self-contained`, RID `win-x64`
- resolver-owned launch descriptor: runtime-owned, outside this skill folder
- reproducible fresh guide operation: invoke the `launch_file` from the exact-version runtime descriptor with `--guide`
- runtime proof summary: the exact published package was restored through NuGet into the standard global-packages cache; its cache sidecar and locally computed SHA-512 both matched the NuGet catalog `packageHash`; the 0.3.318 resolver then returned a successful descriptor and fresh guide result

> 运行时 proof 与 compile 审计文件保存在 Skill 目录外，它们是环境局部产物，不作为仓库内可移植路径承诺。仓库内只保留可复现所需的版本锁、命令形态和结果摘要。

## Runtime Proof Notes

1. The runtime package `Techne.Loom.SkillOrchestrator.Runtime.win-x64` 0.3.318 downloaded successfully from NuGet. NuGet's flat-container and CDN `.nupkg.sha512` sidecar URLs returned 404, but the NuGet registration catalog entry supplied the official SHA-512 hash.
2. The NuGet client restored the exact package into its standard global-packages cache and generated the adjacent `.nupkg.sha512`; the cache sidecar, locally computed hash, and official catalog hash matched. No hash sidecar was fabricated.
3. The exact-version SO resolver accepted the verified cache entry and emitted the launch descriptor. Its descriptor-bound fresh guide returned version 0.3.318 and a readable package-owned guide path.
4. The resolver generated versioned VS Code and Claude MCP configurations from the same descriptor. A local stdio session completed `initialize`, `notifications/initialized`, registered `so_inspect_workflow_fragment`, and successfully inspected the same external workflow copy.
5. After future package or runtime-layout changes, update evidence from the resolver and exact published artifacts; do not infer runtime paths from older package layouts.

## Execution Status For This Slice

- current slice status: `governance integration complete / compile-ready`
- public `dotnet so.dll run` chain: `pending`
- matching public `dotnet so.dll resume` chain for a blocked run: `pending`
- because no public run/resume chain exists yet, this slice must not claim official governed run evidence

## Source Template Boundary

- checked-in `assets/so-workflow/so-template.json` is source-only authority for review and compile
- `assets/so-workflow/contract.json` records the CK business contract extracted from the authoritative `SKILL.md`
- official `run` / `resume` must target an external runtime copy outside the repository
- even though the JSON carries runtime-shaped fields required by the current SO schema, maintainers must not advance state in the checked-in copy

## Latest Verification

- exact runtime: released `0.3.318`, self-contained `win-x64`
- official NuGet client restore: package SHA-512 matched the NuGet catalog `packageHash`; the generated global-packages sidecar matched the same hash
- resolver preparation id: `prep-fba01b45485c3168`
- fresh guide: passed; returned guide version `0.3.318`
- MCP entry: descriptor-bound stdio handshake and `so_inspect_workflow_fragment` call passed against the compile candidate copy
- compile: passed with zero errors and zero warnings; current workflow hash `505d36aea53313e4c342dd6bc337c16a5ec14d99b367c03087d0092e6987e062`; dataflow report resolved with zero issues
- approval semantic probes: exact-runtime approved resume reached the probe's `Done`; rejected resume remained `waitingExternal` and did not advance
- strict-validation recovery probes: an exact-runtime matrix confirmed that missing fields, null, string-coercible values in any gate field, and a nonzero warning count all route to the CK2 recovery checkpoint; only four correctly typed fields with a clean report reached the image-generation SubagentCall boundary. Selecting `return_to_ck2` recorded `revision_report.data_json_changed=false`, supplied that report as a required CK2-render input, and stopped at the fresh `state.wait_ck2` approval boundary. An earlier `fix_data` probe also reached the revalidation SubagentCall after CK2 rerender and fresh approval; it awaited an external revalidation result and did not generate images.
- public `run` / `resume`: pending; this verification did not supply a real moodboard brief or project root and did not advance the business workflow

## Local Weave-Out

- dedicated local subagent: `assets/agents/moodboard-alignment-ck-state-classifier.agent.md`
- purpose: 统一处理 CK 状态识别、项目类型推断、触发词证据和 revision 上下文缺失判断
- authority rule: 该文件本身就是子代理契约权威；先解析仓库 / 工作区副本，再回退到对应的全局安装副本

## Latest Known Verification Continuity

- latest compile: exact runtime `0.3.318`, status `succeeded`, errors `0`, warnings `0`; dataflow resolved with zero issues; hash `505d36aea53313e4c342dd6bc337c16a5ec14d99b367c03087d0092e6987e062` matches the checked-in source template
- latest MCP startup: descriptor-bound stdio session on server version `0.3.318`; bounded fragment returned without truncation
- audit artifacts: environment-local outputs remain outside the repository; exact absolute paths are reported in the active session, not stored as unresolved relative paths here
- workflow location summary: checked-in source template at `assets/so-workflow/so-template.json`; official run/resume must use an external runtime copy
