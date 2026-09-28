# Moodboard Alignment SO Governance Plan

## Scope

将根技能 `SKILL.md` 提升为一个由 Loom Skill Orchestrator 治理的目标 Skill。

本次范围只覆盖根技能自己的 CK1 / CK2 / CK3 / revision 路由、文件产物边界、确认锁和 SO 治理说明；不改动现有 Python 渲染脚本的业务语义。

## Goal

让 moodboard-alignment 具备以下可审查资产：

- 已检入的 `assets/so-workflow/so-template.json` 作为工作流源模板
- 已检入的 `assets/so-workflow/so-package-lock.json` 作为绑定运行时版本锁
- 已检入的 `assets/so-workflow/contract.json` 从 `SKILL.md` 显式提取 CK 状态、确认锁、revision 保护和交付约束
- 已检入的 `assets/agents/moodboard-alignment-ck-state-classifier.agent.md` 作为本地分类子代理
- 已检入的治理说明与节点产物映射
- 一份可通过锁定版本 `so.exe compile` 的 SO-governed workflow 源模板；正式 `run` / `resume` 必须从该模板复制出仓库外的运行时副本

补充约束：

- 对任何 `assets/` 下已命名的本地子代理路由，仓库 / 工作区副本优先于全局安装副本，且该精确 `.agent.md` 文件是唯一权威契约
- 每次 `so.exe` 调用后，都要回报 Mermaid continuity
- 当前切片绑定 released `0.3.326` self-contained `win-x64` apphost。精确包 hash/manifest、fresh guide、版本差分语义探针、source-template compile 与 dataflow 均通过；MCP 只可选尝试，不是启动或治理入口门槛。此前 `0.3.318` 证据仅作为历史基线；没有针对真实 moodboard brief 和项目路径的 public `so.exe run` / `so.exe resume` 链路时，不得声明 official governed completion。

## Workflow Shape

1. 使用锁定版本的直接 apphost 完成 fresh guide 与 bounded workflow-fragment 检查；MCP 仅在已匹配或可直接启动时尝试，否则使用 CLI，然后由外部 SubagentCall 调用本地状态分类子代理。
2. 按 `raw_input / ck1_confirmed / ck2_confirmed / revision` 路由。
3. `raw_input` 通过外部 CK1 调用只产出文本包，并在确认点阻塞。
4. `ck1_confirmed` 通过外部 CK2 调用创建 `data.json` 待确认稿并渲染 `ck2-client.html`、`ck2-execution.html`，然后阻塞。
5. `ck2_confirmed` 先严格校验 `data.json`；只有退出码为 0 且无 errors/warnings 才生成图像/音频并渲染三视图。校验失败时进入显式恢复选择，修复或回 CK2 后必须重新渲染 CK2 并再次取得用户批准，之后才重试校验。
6. `revision` 通过外部步骤只修改点名字段；缺上下文则先阻塞索取上下文，有上下文才继续修订和重渲染。

## Output Families

- blocked checkpoint families:
  - `checkpoint_resume_request`
- terminal completion families:
  - `delivery_response`
- startup and fragment-inspection evidence is retained in external execution records; MCP registration and resolver-descriptor output families are not workflow prerequisites
- detailed business artifacts are carried in and independently verified from the external checkpoint/delivery result; they are not declared as produced families until an exact producer contract exists

## Key Constraints

1. CK1 不写文件，不出方案列表，不超过 3 个确认问题。
2. CK2 只能停在确认阶段，不得偷跑 CK3。
3. CK3 必须建立在 CK2 明确确认之后，除非用户明确要求跳过确认直接生成。
4. revision 保护未点名内容；缺上下文不允许直接改写。
5. `data.json` 始终是单一真相源。
