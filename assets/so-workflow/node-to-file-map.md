# Moodboard Alignment Node To File Map

## Checked-In Governance Assets

| Workflow Concern | Checked-in Asset | Purpose |
| --- | --- | --- |
| SO governance wording | `SKILL.md` | 约束 CK 路由、SO 执行边界与运行时硬化规则 |
| Runtime version authority | `assets/so-workflow/so-package-lock.json` | 锁定 SO 包版本、通道与恢复规则 |
| Workflow source template | `assets/so-workflow/so-template.json` | CK1 / CK2 / CK3 / revision 的 SO 图结构 |
| Planning authority | `assets/so-workflow/skill-plan.md` | 本次治理切片的范围、目标、输出族 |
| State classification weave-out | `assets/agents/moodboard-alignment-ck-state-classifier.agent.md` | 识别 CK 状态、项目类型与 revision 上下文 |
| Governance notes | `assets/so-workflow/governance-notes.md` | 记录 guide / package index / runtime proof 的治理结论 |

## Runtime And Script Surfaces

| Workflow Node Family | Repo File / Script | Output |
| --- | --- | --- |
| CK2 render | `scripts/render_ck2.py` | `ck2-client.html`, `ck2-execution.html` |
| Data validation | `scripts/validate_data.py` | schema / strict validation report |
| Image generation | `scripts/generate_images.py` | `images/` assets or placeholders |
| Audio generation | `scripts/generate_audio.py` | `audio/` assets |
| Final render | `scripts/render.py` | `index-client.html`, `index-director.html`, `index-execution.html` |
| Data contract | `references/data-schema.md` | `data.json` structure authority |
| Project-type slicing | `references/project-templates.md` | per-type array fields and dimension visibility |
| View rules | `references/view-templates.md` | client / director / execution rendering rules |
| HTML layout | `references/html-layout.md` | final HTML structure and interaction rules |
