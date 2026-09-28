# Moodboard Alignment Governance Notes

## Bound Runtime

- runtime channel: `released`
- resolved version: `0.3.326`
- checked-in authority: `assets/so-workflow/so-package-lock.json`
- runtime mode: self-contained, RID `win-x64`
- executable: exact package apphost `so.exe`; no framework bundle or resolver descriptor is used
- reproducible fresh guide operation: run the exact-version `so.exe --guide` after package hash, manifest, archive safety, and entrypoint checks
- current runtime proof summary: exact package `Techne.Loom.SkillOrchestrator.Runtime.win-x64` measured 37,798,808 bytes; package SHA-256 `c3632d6f648ba82a85d5add521982de36bb6ceb14000c44f8ea516548b6e5dd3`; catalog SHA-512 (Base64) `oDMR4ru76kV3hDQxQdG2d4dr02eEJHQ07eE1Qe3omJFFsr2KTEx4CiZF47Ws0K+8cp9GKGOS4VVNB5dhLipxzQ==`; runtime manifest SHA-256 `9793eef3322014d7cf60c8cabb4718116df402058df2ba82a4c4665edf9a1ac9`; exact package hash and size matched catalog metadata, archive/manifest validated, and fresh guide returned version `0.3.326`

> 运行时 proof 与 compile 审计文件保存在 Skill 目录外，它们是环境局部产物，不作为仓库内可移植路径承诺。仓库内只保留可复现所需的版本锁、命令形态和结果摘要。

## 0.3.326 Evidence Index

- execution-local evidence root: `C:\Users\pwangz3\AppData\Local\Temp\exec-20260928-moodboard-0.3.326` (not checked in and not available to other clones; evidence must be re-collected if this Temp directory is removed)
- reference manifest: `workflow-design/reference-manifest.json`; SHA-256 `db6ad1b034a991e42e2fc611c148bd6df94c8efbecdf1333a05eaa89e8b1d53d`
- designer candidate compile feedback: `workflow-design/candidate-compile-audit-20260928-01/wf-moodboard-alignment-root-governance/step-0001-compiled/workflow.compile-feedback.json`; SHA-256 `47a6eff4c0c11ebb3acd965989c39551d3188fc8ff4a4df54d93eb5e9073234c`
- checked-in source-template compile feedback: `source-template-compile-01/audit/wf-moodboard-alignment-root-governance/step-0001-compiled/workflow.compile-feedback.json`; SHA-256 `ef4dbd0c179f73f0603faab954d00607d250224c74a7a847353fe0f1eb3baaf1`
- guide result: `guide-output.json`; SHA-256 `b5ba8ee73156963aaab6b8f840a65aa62a68a985eeb6bd3edc55a78f1770245a`
- detailed workflow renders, analysis, dataflow, probe instances, events, and command results are stored under the corresponding execution-root subdirectories. They are environment-local; a repository clone cannot independently re-run these historical artifacts without reacquiring and validating the exact published package.

## Previous Runtime Proof Notes (0.3.318)

1. The runtime package `Techne.Loom.SkillOrchestrator.Runtime.win-x64` 0.3.318 downloaded successfully from NuGet. NuGet's flat-container and CDN `.nupkg.sha512` sidecar URLs returned 404, but the NuGet registration catalog entry supplied the official SHA-512 hash.
2. The NuGet client restored the exact package into its standard global-packages cache and generated the adjacent `.nupkg.sha512`; the cache sidecar, locally computed hash, and official catalog hash matched. No hash sidecar was fabricated.
3. The exact-version SO resolver accepted the verified cache entry and emitted the launch descriptor. Its descriptor-bound fresh guide returned version 0.3.318 and a readable package-owned guide path.
4. The resolver generated versioned VS Code and Claude MCP configurations from the same descriptor. A local stdio session completed `initialize`, `notifications/initialized`, registered `so_inspect_workflow_fragment`, and successfully inspected the same external workflow copy.
5. This resolver-based acquisition procedure applies only to the historical 0.3.318 run; future upgrades must follow the selected version's published package and fresh-guide contract rather than infer behavior from this older layout.

## Execution Status For This Slice

- current slice status: `0.3.326 runtime migration complete / compile-ready`
- public `so.exe run` chain for a real moodboard brief and project root: `pending`
- matching public `so.exe resume` chain for a blocked business run: `pending`
- because no public run/resume chain exists yet, this slice must not claim official governed run evidence

## Source Template Boundary

- checked-in `assets/so-workflow/so-template.json` is source-only authority for review and compile
- `assets/so-workflow/contract.json` records the CK business contract extracted from the authoritative `SKILL.md`
- official `run` / `resume` must target an external runtime copy outside the repository
- even though the JSON carries runtime-shaped fields required by the current SO schema, maintainers must not advance state in the checked-in copy

## Current Verification (0.3.326)

- exact runtime: released `Techne.Loom.SkillOrchestrator.Runtime.win-x64` `0.3.326`; package size and SHA-512 matched the exact registration catalog entry
- package layout: `runtime.json` declared `so.exe`, RID `win-x64`, and a single-file runtime; nuspec identity, guide path, duplicate entries, traversal safety, and archive bounds passed
- fresh guide: direct apphost returned version `0.3.326` and a readable package-owned guide path
- schema/demo: generated by the same apphost; demo compile passed with zero errors and zero warnings
- runtime semantic drift probes: inherited `ToolCall/noop` literal-write compiled but failed at runtime without producing the expected context; replacement `StateUpdate/state.update` reached `Done` with the expected non-empty value
- canonical resume probe: the exact-version fixture blocked on `WaitResume`, then the matching resume projected the required approval payload and reached `Done` with the approved value and gate evaluation passed
- canonical resume probe: exact-runtime fixture compiled and reached `Done` on the same external workflow copy after resume; required inputs and gate evaluation passed
- source-template compile: passed with zero errors and zero warnings; workflow hash `193844cfbf32f3e42caa1dda376cc8a2ce6fada4b04fbfa0ded96d3a0d0b2c62` matches the checked-in template; dataflow resolved with zero issues
- designer candidate compile: passed with zero errors and zero warnings; candidate hash `d8ef57c0202f53ac5d853f84bfe3ef4932a4ba4aca6ac4ef9209de7526831c80`; the candidate's bootstrap migration removes resolver-descriptor and required-MCP startup dependencies while preserving business gates
- MCP: optional only; no registration is required for fresh guide or CLI workflow inspection
- public business `run` / `resume`: pending; no real moodboard brief/project root was supplied, so this evidence does not claim business completion

## Previous Verified Baseline (0.3.318)

- exact runtime: released `0.3.318`, self-contained `win-x64`
- official NuGet client restore: package SHA-512 matched the NuGet catalog `packageHash`; the generated global-packages sidecar matched the same hash
- resolver preparation id: `prep-fba01b45485c3168`
- fresh guide: passed; returned guide version `0.3.318`
- MCP entry: descriptor-bound stdio handshake and `so_inspect_workflow_fragment` call passed against the compile candidate copy
- compile: passed with zero errors and zero warnings; current workflow hash `505d36aea53313e4c342dd6bc337c16a5ec14d99b367c03087d0092e6987e062`; dataflow report resolved with zero issues
- approval semantic probes: exact-runtime approved resume reached the probe's `Done`; rejected resume remained `waitingExternal` and did not advance
- strict-validation recovery probes: an exact-runtime matrix confirmed that missing fields, null, string-coercible values in any gate field, and a nonzero warning count all route to the CK2 recovery checkpoint; only four correctly typed fields with a clean report reached the image-generation SubagentCall boundary. Selecting `return_to_ck2` recorded `revision_report.data_json_changed=false`, supplied that report as a required CK2-render input, and stopped at the fresh `state.wait_ck2` approval boundary. An earlier `fix_data` probe also reached the revalidation SubagentCall after CK2 rerender and fresh approval; it awaited an external revalidation result and did not generate images.
- public `run` / `resume`: pending; this historical verification did not supply a real moodboard brief or project root and did not advance the business workflow

## Local Weave-Out

- dedicated local subagent: `assets/agents/moodboard-alignment-ck-state-classifier.agent.md`
- purpose: 统一处理 CK 状态识别、项目类型推断、触发词证据和 revision 上下文缺失判断
- authority rule: 该文件本身就是子代理契约权威；先解析仓库 / 工作区副本，再回退到对应的全局安装副本

## Previous Continuity (0.3.318)

- latest compile: exact runtime `0.3.318`, status `succeeded`, errors `0`, warnings `0`; dataflow resolved with zero issues; hash `505d36aea53313e4c342dd6bc337c16a5ec14d99b367c03087d0092e6987e062` matches the checked-in source template
- latest MCP startup: descriptor-bound stdio session on server version `0.3.318`; bounded fragment returned without truncation
- audit artifacts: environment-local outputs remain outside the repository; exact absolute paths are reported in the active session, not stored as unresolved relative paths here
- workflow location summary: checked-in source template at `assets/so-workflow/so-template.json`; official run/resume must use an external runtime copy
