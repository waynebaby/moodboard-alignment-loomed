# Moodboard Alignment Node To File Map

## Checked-In Governance Assets

| Workflow Concern | Checked-in Asset | Purpose |
| --- | --- | --- |
| SO governance wording | `SKILL.md` | 约束 CK 路由、SO 执行边界与运行时硬化规则 |
| Runtime version authority | `assets/so-workflow/so-package-lock.json` | 锁定 SO 包版本、通道与恢复规则 |
| Target business contract | `assets/so-workflow/contract.json` | 从 `SKILL.md` 提取 CK 状态、确认边界、revision 和输出约束 |
| Workflow source template | `assets/so-workflow/so-template.json` | CK1 / CK2 / CK3 / revision 的 SO 图结构 |
| Planning authority | `assets/so-workflow/skill-plan.md` | 本次治理切片的范围、目标、输出族 |
| State classification weave-out | `assets/agents/moodboard-alignment-ck-state-classifier.agent.md` | 识别 CK 状态、项目类型与 revision 上下文；该精确文件也是子代理权威契约 |
| Governance notes | `assets/so-workflow/governance-notes.md` | 记录 guide / package index / runtime proof 的治理结论 |

## External Execution And Script Surfaces

CK business actions are modeled as explicit canonical `SubagentCall` result seams. The caller executes the referenced local script or authority file, then resumes with the structured result; placeholder `workflow.*` names are not treated as registered SO tools.

| Workflow Node Family | Repo File / Script | Output |
| --- | --- | --- |
| CK2 render | `scripts/render_ck2.py` | `ck2-client.html`, `ck2-execution.html` |
| Data validation | `scripts/validate_data.py` | schema / strict validation report |
| CK3 validation recovery | `assets/so-workflow/so-template.json` + `scripts/validate_data.py` | Failed strict reports route to a user-selected fix-or-return-to-CK2 seam; corrected data is re-rendered and requires fresh CK2 approval before retry |
| Image generation | `scripts/generate_images.py` | `images/` assets or placeholders |
| Audio generation | `scripts/generate_audio.py` | `audio/` assets |
| Final render | `scripts/render.py` | `index-client.html`, `index-director.html`, `index-execution.html` |
| Data contract | `references/data-schema.md` | `data.json` structure authority |
| Project-type slicing | `references/project-templates.md` | per-type array fields and dimension visibility |
| View rules | `references/view-templates.md` | client / director / execution rendering rules |
| HTML layout | `references/html-layout.md` | final HTML structure and interaction rules |
