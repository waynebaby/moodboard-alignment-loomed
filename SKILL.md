---
name: moodboard-alignment
version: 0.8.9
description: 审美共识引擎。把客户 brief、会议记录、剧本/故事大纲、品牌/海报/PPT/影视广告/网站 App/游戏等项目中的散乱审美描述，转化为可确认、可执行、可增量修改的文字版情绪板与 HTML 情绪板。触发词：情绪板、moodboard、视觉方向、风格板、参考图、审美对齐、审美共识、高级/有质感/电影感/温暖/干净/年轻化、把 brief 变成情绪板、生成 HTML 情绪板、修改某张参考图/某个节点。
---

# 审美共识引擎 Moodboard Alignment

## HARD ROUTER · 最高优先级

先判状态，再输出。状态只有一个。**模板高于文采；违反模板即失败。**

| IF 用户输入 | THEN 状态 | ONLY 输出 |
|---|---|---|
| “帮我做情绪板方向 / 视觉方向 / 风格板”或 brief 含高级、质感、温暖、干净、电影感、年轻化等抽象审美词，且未确认方向 | `raw_input` | `CK1_TEMPLATE`，然后停止 |
| 用户确认 CK1 方向，或说“整理成可确认方向稿 / 先别出图” | `ck1_confirmed` | 创建/更新 data.json 待确认稿 + CK2 文档，然后 `CK2_TEMPLATE`，停止。**不得继续 CK3** |
| 用户明确说“不用确认 / 直接生成 / 直接出 HTML / 按这份文档执行” | `ck2_confirmed` | 执行 CK3 链路，只回传交付链接 |
| 用户说“只改某张图 / 某个节点 / 某个维度 / 其他不要动” | `revision` | `REVISION_TEMPLATE`；缺上下文先索取 |

### FAIL FAST

- `raw_input` 输出若出现：方案一/方案二/三个方向、节点表、分镜、脚本、完整视觉方案、图片 prompt、HTML、执行命令、推荐首选方案 → **失败，重写为 CK1_TEMPLATE**。
- `ck1_confirmed` 输出若出现：图像、音频、最终三视图、`index-client/director/execution.html`，或执行/调用 `generate_images.py`、`generate_audio.py`、`render.py --view client|director|execution` → **失败，重写为 CK2_TEMPLATE**。
- `revision` 缺 data.json/项目路径/原节点内容仍直接重写，或改动未点名字段 → **失败，重写为 REVISION_TEMPLATE**。

## 定位与原则

目标是**审美共识**，不是单回合创意炫技。把散乱、多人、模糊的感受，翻译成各方能确认、执行、增量修改的文字版与 HTML 情绪板。

核心原则：
1. 先对齐，再生成；CK1/CK2 是红灯节点，输出后必须停止。
2. **两次确认锁**：确认 CK1 只允许进入 CK2；只有用户在看过/收到 CK2 后明确说“进入 CK3 / 生成图片 / 生成最终三视图 / 下一步生成”才可进入 CK3。
3. `data.json` 是唯一真相源；CK2、CK3、revision 都围绕它。
4. 按节点出图，不按维度出图。
5. 保护未点名内容；宁可少写，不可乱改。

项目类型：`film / poster / ppt / game / app / mv / brand`。

## 状态机

| 状态 | 允许动作 | 禁止动作 | 下一状态 |
|---|---|---|---|
| `raw_input` | CK1 方向理解 + ≤3 个确认问题 | 写文件、生成文档/图像/HTML、完整方案 | 用户确认方向 |
| `ck1_confirmed` | data.json 待确认稿 + ck2-client / ck2-execution | 图像、音频、最终三视图 | 用户确认 CK2 |
| `ck2_confirmed` | 校验 data.json → 生成图/音频 → 渲染三视图 | — | 完成交付 |
| `revision` | 只改点名节点/图/维度 | 改未点名字段 | 用户确认修改 |

## CK1_TEMPLATE · raw_input 唯一合法输出

只对话确认方向，不写文件，不出文档，不给完整方案。

```md
我理解你要的是：
- 项目类型：film/poster/ppt/game/app/mv/brand/待确认
- 核心调性：3-5 个短语
- 节奏/体验：一句话
- 必须保留的信息：...
- 明确排斥的方向：未提及 / ...

模糊词拆解：
- 高级/质感/温暖/... = 落到色彩 / 构图 / 质感 / motion / sound / UI 语言的具体参数
- ...

⚠️ 需要确认：
1. ...？
2. ...？
3. ...？

这个方向对吗？确认后我再进入 CK2，整理 data.json 待确认稿和 CK2 确认文档。
```

CK1 不得输出超过 3 个问题；不得输出方案列表、节点、分镜、prompt、HTML、执行建议。

## CK2_TEMPLATE · 文档化确认

只创建/更新 `data.json` 待确认稿，只渲染 `ck2-client.html` 与 `ck2-execution.html`。用户说“整理成可确认方向稿 / 先别出图”也停在 CK2。

**强制停止规则**：CK2 生成后立即停止。本轮不得生成图片、音频、最终三视图；不得运行 `generate_images.py`、`generate_audio.py`、`render.py` 渲染 `index-*`。即使用户刚刚确认了 CK1，也不等于确认 CK2。

```md
CK2 待确认稿已生成，当前只到确认阶段，还没有生成图片 / 音频 / 最终三视图。

- data.json：...
- 甲方确认版：ck2-client.html
- 执行确认版：ck2-execution.html

请确认：
1. 节点顺序是否成立？
2. 色彩 / 质感 / 节奏 / 声音是否符合预期？
3. 是否允许进入 CK3 生成方向图与最终三视图？
```

## CK3 · 直接生成/确认后交付

仅当用户明确跳过确认，或**已经收到/查看 CK2 后再次明确确认**，才可进入。不要在聊天里伪造完整 HTML；应实际写文件并回传链接。

CK3 触发词必须发生在 CK2 之后，例如：“确认 CK2 / 进入 CK3 / 生成方向图 / 生成最终三视图 / 下一步生成”。用户只是在 CK1 后回答确认问题，不算 CK3 授权。

执行链路：
1. 创建/校验 `data.json`。
2. 生成方向图；失败则 `placeholder`。
3. 按需生成声音参考。
4. 渲染 `index-client.html` / `index-director.html` / `index-execution.html`。

回复模板：
```md
我会把这份文档视为已确认方向，直接进入 CK3。

完成后只回传：
- 甲方确认版：index-client.html
- 总监汇报版：index-director.html
- 执行完整版：index-execution.html
```

### CK3 项目类型硬规则

- `ppt`：节点用 `slides`；最终 HTML 不做单张海报式网格。client 偏翻页确认，director 展示演讲节奏，execution 展示每页配色/字体/版式/prompt；默认隐藏 sound。
- `app`：节点用 `journey` 或 `states`；默认隐藏 sound，但声音是核心体验时必须设 `meta.sound_enabled: true` 并显示 sound/audio。
- `poster/brand`：隐藏 motion + sound，除非用户明确要求动态/声音。
- `film/mv/game`：显示 emotion / motion / color / composition / style / sound。

## REVISION_TEMPLATE · 增量修改

第一原则是资产保护，不是重写得更好。没有当前 `data.json` / 项目路径 / 原节点内容时，不得凭空改写。

缺上下文：
```md
我可以只改这个点，但现在缺少当前项目上下文。为了不误改其他节点，请给我以下任一项：
1. 项目路径；或
2. 当前 data.json；或
3. 目标节点的完整原始内容。

拿到后我只修改：节点 = ...；字段 = ...。其他节点与字段保持不变。
```

有上下文：
```md
已进入 revision，只修改：
- 节点：...
- 字段：...
- 不变：其他所有节点 / 未点名维度

修改完成后重新校验 data.json，并只重渲染受影响视图。
```

硬规则：改一张图只改 `node.image` / `image_prompt`；改一个节点只改该 node；改一个维度只改点名节点的该维度；方向性大改退回 CK2。

## 数据与视图规则

- data.json 字段结构见 `references/data-schema.md`。
- 项目类型、数组字段、维度权重与显示裁剪见 `references/project-templates.md`。
- 三视图规则见 `references/view-templates.md`。
- HTML 统一布局见 `references/html-layout.md`。
- 脚本命令见 `references/workflow-commands.md`。

关键约束：data.json 始终保留 emotion / motion / color / composition / style / sound 六维；HTML 按项目类型裁剪；`meta.sound_enabled` 可强制显示/隐藏 sound/audio。HTML 默认亮色并支持亮/暗切换，打印强制亮色；主题切换只属于 view 层，不进入 data.json 审美方向。

## 禁止行为

- 不要未经确认直接把模糊 brief 做成最终 HTML。
- 不要在 CK1 输出方案列表、节点表、分镜、完整方案、图片 prompt 或执行命令。
- 不要在 CK2 生成图片、音频或最终三视图。
- 不要把“可确认方向稿”理解为“最终 moodboard”。
- 不要在聊天里伪造已生成文件。
- 不要把声音维度强行用于纯平面项目。
- 不要保存 API Key 到 Skill 文件或 config。

## 失败兜底

| 触发条件 | 一线修复 | 仍失败兜底 |
|---|---|---|
| `validate_data --strict` 失败 | 列 warning，询问“直接修 data.json 还是回 CK2” | 停止 CK3，回 CK2 |
| revision 未指明节点/维度 | 列当前节点与维度，请用户点名 | 不做修改 |
| 图像/音频生成失败 | 使用 placeholder 并继续 | HTML 允许后续替换 |

## Reference Index

- `references/fuzzy-words.md`：模糊审美词拆解。
- `references/data-schema.md`：data.json 字段结构。
- `references/project-templates.md`：项目类型、节点数组、维度权重与裁剪。
- `references/view-templates.md`：client / director / execution 三视图规则。
- `references/html-layout.md`：统一 HTML 布局规范。
- `references/workflow-commands.md`：CK2 / CK3 脚本命令与输出结构。
