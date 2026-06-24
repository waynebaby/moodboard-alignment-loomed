# Moodboard Alignment SO Governance Plan

## Scope

将根技能 `SKILL.md` 提升为一个由 Loom Skill Orchestrator 治理的目标 Skill。

本次范围只覆盖根技能自己的 CK1 / CK2 / CK3 / revision 路由、文件产物边界、确认锁和 SO 治理说明；不改动现有 Python 渲染脚本的业务语义。

## Goal

让 moodboard-alignment 具备以下可审查资产：

- 已检入的 `assets/so-workflow/so-template.json` 作为工作流源模板
- 已检入的 `assets/so-workflow/so-package-lock.json` 作为绑定运行时版本锁
- 已检入的 `assets/agents/moodboard-alignment-ck-state-classifier.agent.md` 作为本地分类子代理
- 已检入的治理说明与节点产物映射
- 一份可通过 `dotnet so.dll compile` 的 SO-governed workflow 源模板；正式 `run` / `resume` 必须从该模板复制出仓库外的运行时副本

## Workflow Shape

1. 读取用户输入并调用本地状态分类子代理。
2. 按 `raw_input / ck1_confirmed / ck2_confirmed / revision` 路由。
3. `raw_input` 只产出 CK1 文本包，并在确认点阻塞。
4. `ck1_confirmed` 创建 `data.json` 待确认稿并渲染 `ck2-client.html`、`ck2-execution.html`，然后阻塞。
5. `ck2_confirmed` 校验 `data.json`，生成图像/音频（按项目类型或 `meta.sound_enabled`），渲染三视图 HTML，然后完成。
6. `revision` 只修改点名字段；缺上下文则先阻塞索取上下文，有上下文才继续修订和重渲染。

## Output Families

- blocked checkpoint families:
  - `checkpoint_package`
  - `checkpoint_resume_request`
  - `state_classification_record`
- terminal completion families:
  - `data_json_current`
  - `delivery_response`
  - `updated_views`
  - `workflow_completion_record`
- specialized families:
  - `ck1_template_response`
  - `data_json_draft`
  - `ck2_client_html`
  - `ck2_execution_html`
  - `final_image_assets`
  - `final_audio_assets`
  - `index_client_html`
  - `index_director_html`
  - `index_execution_html`
  - `revision_audit_log`

## Key Constraints

1. CK1 不写文件，不出方案列表，不超过 3 个确认问题。
2. CK2 只能停在确认阶段，不得偷跑 CK3。
3. CK3 必须建立在 CK2 明确确认之后，除非用户明确要求跳过确认直接生成。
4. revision 保护未点名内容；缺上下文不允许直接改写。
5. `data.json` 始终是单一真相源。
