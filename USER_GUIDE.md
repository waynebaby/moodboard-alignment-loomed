# 用户指南｜Moodboard Alignment / 审美共识引擎

> **Moodboard Alignment turns fuzzy aesthetic briefs into confirmable, executable, and incrementally editable HTML moodboards.**  
> 审美共识引擎把 brief、会议记录、剧本读本、品牌文档、PPT 主题、App/游戏设定中的模糊审美描述，转化为可确认、可执行、可增量修改的 HTML 情绪板。

---

## 1. 这个 Skill 是什么

**审美共识引擎**不是一个单纯的「生成漂亮图片」工具，也不是一次性 moodboard prompt。

它的核心目标是：

> 把客户、创意负责人和执行团队脑子里模糊、不一致、难以落地的审美语言，转化为一组可确认、可执行、可修改的共同语言。

它生成的情绪板主要服务三个受众：

| 受众 | 他们关心什么 | 对应输出 |
|---|---|---|
| 客户 / 甲方 | 方向对不对、感觉是不是想要的 | client 版，短、准、少技术细节 |
| 创意 / 导演 / 总监 / 决策者 | 审美判断、风格是否成立、是否能汇报 | director 版，展示方向描述、风险、执行注意 |
| 执行团队 | 具体怎么落地、怎么生成图、怎么拍、怎么买、怎么设计 | execution 版，展开六维、image prompt、执行信息 |

所以，这个 Skill 的重点不是「图有多好看」，而是：

- 是否把模糊审美词拆清楚；
- 是否把方向变成可以确认的文档；
- 是否让不同受众看到合适的信息密度；
- 是否能保护已确认内容，只修改用户点名的部分；
- 是否能继续作为拍摄、AI 生成、美术、采买、设计、声音参考的执行资产。

---

## 2. 它能接受哪些输入

这个 Skill 不要求用户一开始就准备好完整 brief。它可以接受非常散乱的输入。

常见输入包括：

### 2.1 影视 / 广告 / 短片

- 客户 brief；
- 会议记录；
- 剧本大纲；
- 剧本定稿；
- 叙事开发读本；
- 分场大纲；
- 角色 / 场景 / 道具 / 资产清单；
- 导演阐述草稿；
- 只是一句「想要高级、有质感、温暖一点」。

### 2.2 品牌 / 海报 / Campaign

- 品牌定位文档；
- 产品介绍；
- KV 方向描述；
- 参考图描述；
- 活动主题；
- 竞品风格避让要求。

### 2.3 PPT / 发布会 / 路演

- 文章；
- 演讲主题；
- PPT 大纲；
- 发布会内容；
- 一组页面标题；
- 只是一句「想要轻松、俏皮、温暖纸感」。

### 2.4 App / 网站 / 游戏 / 互动体验

- 产品构想；
- 用户旅程；
- 世界观；
- 游戏状态设计；
- 交互体验描述；
- 声音驱动体验说明。

### 2.5 资产清单

也可以输入执行层清单，例如：

- 场景清单；
- 道具清单；
- 服装清单；
- 角色出场表；
- 拍摄资产清单。

这时，审美共识引擎可以把「要买什么 / 要设计什么」进一步转化成：

- 买成什么质感；
- 什么颜色不能用；
- 什么材质更合适；
- 哪些参考图可用；
- 哪些方向要避开。

---

## 3. 核心工作流：CK1 → CK2 → CK3 → Revision

这个 Skill 最重要的是 checkpoint 工作流。

### 3.1 流程图

#### 影视 AI 前期开发链路

![影视 AI 前期开发链路](docs/visual-pipelines/d2/film-pipeline-sketch.png)

[查看 HTML 信息图](docs/visual-pipelines/film-pipeline-card.html)

#### 相关影视类 Skills

这张「影视 AI 前期开发链路」图中的上游环节，可以和作者之前开源的几个影视类 Skill 配合使用：

| Skill | GitHub | 简介 | 与本 Skill 的关系 |
|---|---|---|---|
| Narrative to Screen Reader / 叙事转译 | [zhlmi/narrative-to-screen-reader](https://github.com/zhlmi/narrative-to-screen-reader) | 分析你手上的故事，并翻译成影视开发语言的叙事转译 Skill | 可输出完整开发读本、导演读本、演员读本等，作为审美共识引擎的上游输入 |
| Script Forging / 剧本锻造 | [zhlmi/script-forging](https://github.com/zhlmi/script-forging) | 把你手上已有的好故事，锻造成真正的剧本和分镜的专业 Skill | 可输出剧本定稿、分场大纲、分镜表、资产清单，进入审美共识层 |
| Tragedy Narrative Guard / 悲剧叙事哨兵 | [zhlmi/tragedy-narrative-guard](https://github.com/zhlmi/tragedy-narrative-guard) | 爱情悲剧叙事哨兵 Skill | 可用于检查悲剧叙事方向、情绪边界和终局约束，再转入情绪板做视听对齐 |

它们不是使用本 Skill 的前置条件。审美共识引擎也可以单独读取 brief、会议记录、剧本、品牌文档、PPT 大纲或资产清单。

#### 审美共识引擎通用工作流

![审美共识引擎通用工作流](docs/visual-pipelines/d2/general-workflow-sketch.png)

[查看 HTML 信息图](docs/visual-pipelines/general-workflow-card.html)

### 3.2 Checkpoint 工作流

```text
输入材料
  ↓
CK1 方向确认
  ↓
CK2 文字版方向稿 / 确认文档
  ↓
CK3 多视图 HTML 情绪板
  ↓
Revision 增量修改
```

---

## 4. 六维设计思路

审美共识引擎用六个维度拆解一个方向节点：

```text
emotion / motion / color / composition / style / sound
```

这六维不是为了把描述写复杂，而是为了把「感觉」拆成执行团队能理解的参数。

| 维度 | 解决的问题 | 常见落点 |
|---|---|---|
| emotion 情绪 | 这个节点让人产生什么心理感受？ | 疏离、安心、压迫、温暖、危险、余韵、克制、兴奋 |
| motion 动作 / 节奏 | 它是快还是慢？流动还是停滞？ | 镜头运动、剪辑密度、页面切换、交互动效、游戏状态变化 |
| color 色彩 | 它靠什么色温、饱和度、色彩关系建立气质？ | 主色、辅助色、冷暖关系、饱和度、明暗、色彩迁移 |
| composition 构图 | 观众如何看见它？视觉重心在哪里？ | 远近关系、留白比例、人物站位、镜头角度、界面层级 |
| style 风格 / 质感 | 它摸起来、看起来是什么材质？属于什么美学系统？ | 胶片颗粒、玻璃、金属、纸感、手绘、工业感、UI 组件语言 |
| sound 声音 | 它听起来是什么空间、密度和情绪？ | 环境音、人声、混响、声音密度、BGM 气质、沉默与留白 |

### 4.1 为什么是这六维

很多审美沟通的问题来自一句话太抽象：

```text
高级一点 / 有质感 / 温暖一点 / 科技感 / 电影感 / 年轻化
```

这些词直接交给执行团队，通常不能指导拍摄、设计、调色或生成。

六维拆解的目的，是把这类词翻译成可以讨论和执行的语言：

- 「高级」可能是低饱和、强留白、稳定构图、细线条、少文字；
- 「温暖」可能是低反差暖光、木质/织物材质、慢节奏、人声靠近；
- 「科技感」可能是冷色屏幕光、网格构图、低噪界面、电子脉冲声；
- 「电影感」可能是宽容度、光比、景深、空间层次和剪辑节奏，而不只是加黑边。

### 4.2 六维不等于六张图

每个节点仍然只生成一张方向图。

这张图承载该节点的：

```text
情绪 + 节奏 + 色彩 + 构图 + 质感 + 声音想象
```

不要把六维拆成六张图。六维是思考和执行参数，不是图片数量。

### 4.3 不同项目的六维权重不同

六维会一直保留在 data.json 中，但 HTML 会根据项目类型裁剪显示。

例如：

- 影视 / MV / 游戏：sound 很重要；
- 海报 / 品牌：通常隐藏 motion 和 sound；
- PPT：motion 可表示页面切换和信息节奏，sound 通常隐藏；
- App：motion 表示交互节奏，sound 默认隐藏，除非它是声音驱动体验。

这保证了同一套数据结构可以服务不同项目，但不会让 HTML 显示无意义的维度。

---

## 5. CK1：方向确认

### 4.1 CK1 的目的

CK1 的目的不是生成最终情绪板，而是先确认：

- 项目类型是什么；
- 核心调性是什么；
- 用户说的「高级」「质感」「温暖」「电影感」到底应该落到哪些视觉 / 声音 / 节奏参数上；
- 有哪些方向必须避开；
- 还需要问哪几个关键问题。

### 4.2 CK1 应该输出什么

CK1 只输出：

- 项目类型；
- 核心调性；
- 节奏 / 体验；
- 必须保留的信息；
- 明确排斥的方向；
- 模糊词拆解；
- 最多 3 个确认问题。

### 4.3 CK1 不应该做什么

CK1 不应该：

- 生成最终 HTML；
- 生成图片；
- 生成音频；
- 输出完整分镜；
- 输出完整节点表；
- 输出 image prompt；
- 自作主张进入 CK3。

用户确认 CK1 后，只能进入 CK2，不能直接进入 CK3。

---

## 6. CK2：文字版方向稿 / 确认文档

### 5.1 CK2 的目的

CK2 的目的是把已经确认的方向，固化成一份可审查、可讨论、可修改的文字版方向资产。

更具体地说，CK2 是**第一次正式对齐甲方需求**的阶段。

它把 CK1 中得到的方向判断，整理成客户、创意和执行团队都能看懂的确认文档，用来确认：

- 节点顺序是否成立；
- 色彩、质感、节奏、声音方向是否正确；
- 哪些内容已经达成共识；
- 哪些风险需要提前暴露；
- 是否允许进入视觉生成和最终三视图阶段。

它是「生成之前的确认层」。

CK2 阶段会创建 / 更新：

```text
data.json
ck2-client.html
ck2-execution.html
```

### 5.2 CK2 输出给谁看

CK2 有两个确认文档：

| 文件 | 受众 | 目的 |
|---|---|---|
| `ck2-client.html` | 客户 / 甲方 | 快速确认方向、调性、节点是否正确 |
| `ck2-execution.html` | 执行团队 / 创意团队 | 确认六维细节、image prompt、执行注意是否成立 |

### 5.3 CK2 为什么重要

示例输出：

- [CK2 甲方确认版](examples/companion-robot-booth/ck2-client.html)
- [CK2 执行确认版](examples/companion-robot-booth/ck2-execution.html)

这两个示例来自「具身智能家庭陪护机器人 — 户外展台设计」，可以用来对比 CK2 阶段的 client / execution 信息密度差异。

很多 AI 工作流的问题是：

> 用户刚确认一点方向，AI 就直接生成最终结果。

审美共识引擎故意把 CK2 作为红灯节点：

```text
CK1 确认 ≠ CK3 授权
CK2 确认 = 才能进入 CK3
```

也就是说，用户确认 CK1 后，系统必须停在 CK2，让用户看到文字版方向稿，再决定是否进入最终生成。

### 5.4 CK2 不应该做什么

CK2 不应该：

- 生成方向图；
- 生成音频；
- 生成最终三视图；
- 输出 `index-client.html` / `index-director.html` / `index-execution.html`。

---

## 7. CK3：多视图 HTML 情绪板

### 6.1 CK3 的目的

CK3 是最终交付阶段。

它把已经确认的 `data.json` 转成一组可查看、可分享、可执行的 HTML 情绪板。

更具体地说，CK3 是**把已确认需求真正落地**的阶段。

它不再只是文字确认，而是生成视觉版、声音参考和执行可用的多视图 HTML，让三类人进入同一个执行参照：

- 客户看到方向是否符合预期；
- 创意 / 导演 / 总监看到风格是否成立、能不能汇报；
- 执行团队看到图片、prompt、六维参数和落地注意。

CK3 通常会执行：

```text
校验 data.json
  ↓
生成方向图
  ↓
按需生成声音参考
  ↓
渲染三视图 HTML
```

### 6.2 CK3 输出什么

CK3 输出三个最终 HTML：

| 文件 | 名称 | 受众 | 内容密度 |
|---|---|---|---|
| `index-client.html` | 甲方确认版 | 客户 / 甲方 | 最简洁，只看图、标题、关键词 |
| `index-director.html` | 总监 / 导演汇报版 | 创意负责人 / 决策者 | 展示方向描述、风险、执行注意 |
| `index-execution.html` | 执行完整版 | 设计师 / 摄影 / 调色 / AI 生成 / 美术 / 声音团队 | 展开完整六维、image prompt、执行信息 |

示例输出：

- [CK3 甲方确认版](examples/companion-robot-booth/index-client.html)
- [CK3 总监汇报版](examples/companion-robot-booth/index-director.html)
- [CK3 执行完整版](examples/companion-robot-booth/index-execution.html)

这三个示例来自同一个「具身智能家庭陪护机器人 — 户外展台设计」项目。最终 HTML 使用压缩 JPEG 内嵌图片，不含音频，单文件体积约 1MB，适合快速预览三视图差异。

### 6.3 CK3 的 HTML 特性

最终 HTML 支持：

- 默认亮色；
- 亮 / 暗主题切换；
- localStorage 记忆用户选择；
- 打印 / 导出 PDF 时强制亮色；
- 图片点击 lightbox，查看原始比例完整图；
- 可选 `--embed` 把图片 / 音频嵌入单文件 HTML；
- 音频播放器，用于声音参考。

### 6.4 图片显示规则

节点卡片中，图片统一显示为 1:1，以保持页面布局稳定。

但如果原图不是 1:1，用户可以点击图片打开 lightbox，以原始比例完整查看。

这个交互属于 view 层，不改变 data.json，也不改变统一布局规则。

---

## 8. Revision：增量修改

### 7.1 Revision 的目的

Revision 不是重做整个情绪板，而是保护已确认资产，只修改用户明确点名的部分。

例如：

```text
只改最后一张图，其他节点不要动。
```

系统应该只修改：

```text
目标节点的 image / image_prompt
```

不应该改其他节点、色板、整体方向。

### 7.2 缺上下文时怎么办

如果用户只说「改某张图」，但当前没有项目路径或 data.json，系统应该先索取上下文：

```text
请提供项目路径、当前 data.json，或目标节点的完整原始内容。
```

不要凭空重写。

---

## 9. 安装与目录结构

### 8.1 仓库结构

典型结构：

```text
moodboard-alignment/
├── SKILL.md
├── references/
│   ├── data-schema.md
│   ├── fuzzy-words.md
│   ├── html-layout.md
│   ├── project-templates.md
│   ├── view-templates.md
│   └── workflow-commands.md
└── scripts/
    ├── config.py
    ├── generate_images.py
    ├── generate_audio.py
    ├── render.py
    ├── render_ck2.py
    ├── utils.py
    └── validate_data.py
```

### 8.2 依赖

脚本尽量只使用 Python 标准库。

你需要：

```bash
python3
```

图像生成和 TTS 需要可用的 API Key。

---

## 10. 模型后端配置

### 9.1 默认后端

本项目默认保留作者使用的模型后端：

| 类型 | 默认服务 | 默认模型 |
|---|---|---|
| 图像生成 | Agnes OpenAI-compatible Images API | `agnes-image-2.1-flash` |
| TTS 声音参考 | Mimo chat-audio compatible API | `mimo-v2.5-tts-voicedesign` |

如果你使用同样的服务，只需要设置 API Key。

### 9.2 使用 Agnes 生图

设置：

```bash
export AGNES_API_KEY="your-key"
```

默认：

```text
AGNES_BASE_URL=https://apihub.agnes-ai.com/v1
DEFAULT_IMAGE_MODEL=agnes-image-2.1-flash
```

### 9.3 使用其他 OpenAI-compatible 图像模型

如果你的图像服务兼容：

```text
POST /v1/images/generations
```

可以设置：

```bash
export IMAGE_BASE_URL="https://your-image-api/v1"
export IMAGE_API_KEY="your-key"
export DEFAULT_IMAGE_MODEL="your-image-model"
```

图像返回支持：

- `b64_json`；
- `url`；
- 常见 base64 字段。

### 9.4 使用 Mimo TTS

设置：

```bash
export MIMO_API_KEY="your-key"
```

默认：

```text
MIMO_BASE_URL=https://token-plan-cn.xiaomimimo.com/v1
DEFAULT_AUDIO_MODEL=mimo-v2.5-tts-voicedesign
```

### 9.5 使用其他兼容 TTS

如果你的 TTS 服务兼容当前 chat-audio 格式，可以设置：

```bash
export AUDIO_BASE_URL="https://your-audio-api/v1"
export AUDIO_API_KEY="your-key"
export DEFAULT_AUDIO_MODEL="your-tts-model"
```

当前内置音频 provider 为：

```text
AUDIO_PROVIDER=mimo_chat_audio
```

它调用：

```text
POST /chat/completions
```

并期望返回：

```text
choices[0].message.audio.data
```

如果你的 TTS 服务不是这个格式，请让你的 Agent 根据服务商文档修改：

```text
scripts/generate_audio.py
```

通常需要适配两件事：

1. 请求 payload；
2. 返回音频数据解析方式。

---

## 11. 最简单的使用方式

### 10.1 最简单提示词

你可以直接对 Agent 说：

```text
请使用 moodboard-alignment / 审美共识引擎，阅读这份文档，先进入 CK1，帮我做情绪板方向确认。
```

或者：

```text
把这份 brief 变成可确认、可执行、可增量修改的情绪板。请按 CK1 → CK2 → CK3 流程走，不要跳过确认。
```

如果你想直接跳过确认：

```text
这份文档已经确认，不用再问，直接进入 CK3，生成三视图 HTML 情绪板。
```

如果你只想改一个节点：

```text
只改“终局余韵”这一张图，让它更克制、更有留白，其他节点不要动。
```

---

## 12. 命令行使用

下面假设：

```bash
SKILL=/path/to/moodboard-alignment
PROJECT=/path/to/my-moodboard-project
DATA=$PROJECT/data.json
```

### 11.1 渲染 CK2 确认文档

```bash
python3 $SKILL/scripts/render_ck2.py \
  --data-json $DATA \
  --output $PROJECT/ck2-client.html \
  --audience client

python3 $SKILL/scripts/render_ck2.py \
  --data-json $DATA \
  --output $PROJECT/ck2-execution.html \
  --audience execution
```

### 11.2 校验 data.json

```bash
python3 $SKILL/scripts/validate_data.py --data-json $DATA
```

严格模式：

```bash
python3 $SKILL/scripts/validate_data.py --data-json $DATA --strict
```

### 11.3 生成方向图

```bash
python3 $SKILL/scripts/generate_images.py \
  --data-json $DATA
```

指定模型：

```bash
python3 $SKILL/scripts/generate_images.py \
  --data-json $DATA \
  --model agnes-image-2.1-flash
```

只重生成一个节点：

```bash
python3 $SKILL/scripts/generate_images.py \
  --data-json $DATA \
  --node-id node-opening
```

### 11.4 生成声音参考

```bash
python3 $SKILL/scripts/generate_audio.py \
  --data-json $DATA
```

只重生成一个节点：

```bash
python3 $SKILL/scripts/generate_audio.py \
  --data-json $DATA \
  --node-id node-opening
```

### 11.5 渲染最终三视图 HTML

推荐使用 `--embed` 生成可单文件分发的 HTML：

```bash
python3 $SKILL/scripts/render.py \
  --data-json $DATA \
  --output $PROJECT/index-client.html \
  --view client \
  --embed

python3 $SKILL/scripts/render.py \
  --data-json $DATA \
  --output $PROJECT/index-director.html \
  --view director \
  --embed

python3 $SKILL/scripts/render.py \
  --data-json $DATA \
  --output $PROJECT/index-execution.html \
  --view execution \
  --embed
```

---

## 13. data.json 的基本概念

`data.json` 是这个 Skill 的唯一真相源。

它保存：

- 项目信息；
- 项目类型；
- 整体风格；
- 关键词；
- 色板；
- 节点；
- 每个节点的六维描述；
- 图片路径；
- image prompt；
- 声音参考；
- 音频路径。

项目类型决定节点数组字段：

| 项目类型 | 节点字段 |
|---|---|
| film / mv | `timeline` |
| poster / brand | `frames` |
| ppt | `slides` |
| app | `journey` |
| game | `states` |

更多字段见：

```text
references/data-schema.md
```

---

## 14. 项目类型与声音显示

data.json 中始终保留六维：

```text
emotion / motion / color / composition / style / sound
```

但 HTML 会根据项目类型裁剪显示。

一般规则：

| 项目类型 | 是否默认显示 sound |
|---|---|
| film | 是 |
| mv | 是 |
| game | 是 |
| app | 否，除非声音是核心体验 |
| ppt | 否 |
| poster | 否 |
| brand | 否 |

如果 App / PPT / 品牌 / H5 本身是声音驱动体验，可以在 `meta` 中设置：

```json
"sound_enabled": true
```

---

## 15. 常见问题

### Q1：为什么 CK1 不直接生成情绪板？

因为 CK1 的目标是对齐方向。如果用户只说「高级一点、有质感」，直接生成最终情绪板很容易跑偏。

CK1 先把模糊审美词拆成可确认的参数，再进入 CK2。

### Q2：为什么要 CK2？

CK2 是生成前的确认层。它让客户和执行团队先看到文字版方向稿，确认节点、色彩、节奏、声音等是否成立。

没有 CK2，很容易出现：

```text
用户只是确认了大方向，AI 却直接生成最终成品。
```

### Q3：CK3 的三视图有什么区别？

- client：给客户看，少信息；
- director：给导演 / 总监 / 老板看，中等信息；
- execution：给执行团队看，完整信息。

### Q4：图片为什么在卡片里都是 1:1？

为了统一布局。不同项目可能生成横图、竖图、方图，如果直接按原比例排版，页面会很乱。

所以 node card 中统一使用 1:1 裁切。但用户可以点击图片，用 lightbox 查看原始比例完整图。

### Q5：我可以只改一张图吗？

可以。请明确说：

```text
只改某某节点这张图，其他节点不要动。
```

如果当前没有 data.json 或项目路径，系统应该先索取上下文，不应凭空重写。

### Q6：没有图像 API Key 能用吗？

可以用 CK1、CK2、data.json、HTML 渲染，但无法生成方向图。图片会保持 placeholder 或已有外部图片。

### Q7：没有 TTS API Key 能用吗？

可以。声音参考不是所有项目都必需。没有 TTS 时，可以只保留 sound 描述，不生成音频播放器。

---

## 16. 关于音乐生成参考

当前版本内置的是两类声音能力：

1. `sound` 维度：描述每个节点的声音密度、空间、混响、环境音、BGM 气质等；
2. `generate_audio.py`：生成 TTS 声音参考，适合角色台词、旁白、语气、声音质感。

它还没有内置完整的音乐生成模块。

这是有意保持克制：音乐生成会让 CK3 链路变重，也会带来更多模型后端差异。不同音乐模型的接口格式、时长控制、歌词/纯音乐参数、返回音频方式都不一样，过早内置会增加普通用户的使用成本。

如果项目确实需要音乐参考，可以有两种方式：

### 16.1 在当前版本中先用文字固定音乐方向

可以在节点的 `sound.description` 或执行层注意中写清楚：

- BGM 气质；
- 速度 / BPM；
- 乐器；
- 情绪弧线；
- 是否需要主题动机；
- 参考曲目；
- 哪些音乐方向禁止使用。

例如：

```text
极简钢琴 + 低频弦乐，慢速，前半段保持冷色悬浮感，终局前暖色和声短暂出现后迅速褪去。不要史诗化，不要煽情弦乐墙。
```

这已经足够指导剪辑、声音设计或后续音乐生成。

### 16.2 后续自行增加 generate_music.py

如果用户需要真正生成音乐，可以让自己的 Agent 根据所使用的音乐模型 API 增加一个可选脚本，例如：

```text
scripts/generate_music.py
```

推荐定位是「可选扩展」，不要默认阻塞 CK3：

```bash
python3 scripts/generate_music.py --data-json path/to/data.json
```

建议第一版只做项目级音乐主题参考，而不是每个节点都生成一段音乐：

```json
"music_theme": {
  "prompt": "项目级音乐生成提示词",
  "style": "ambient / piano / synth / strings",
  "mood": "克制、温暖、带裂缝",
  "duration": 30,
  "instrumental": true,
  "url": "music/theme_xxx.mp3",
  "status": "generated",
  "model": "your-music-model",
  "generated_at": "ISO-8601"
}
```

适合优先加入音乐生成的项目类型：

| 项目类型 | 是否适合音乐生成 | 说明 |
|---|---|---|
| film | 适合 | BGM / 情绪主题 / 剪辑节奏参考 |
| mv | 强适合 | 音乐本身就是结构核心 |
| game | 适合 | 主题动机、状态音乐、战斗/探索循环 |
| app | 视情况 | 声音驱动体验适合，普通工具型 App 不需要 |
| ppt / brand | 视情况 | 发布会、品牌片、campaign 可选 |
| poster | 通常不需要 | 可用文字描述音乐感，不必生成 |

一句话：

> 当前版本先用 sound 维度固定音乐方向；真正的音乐生成可以作为后续可选模块加入。

---

## 17. 版本历史

### v0.8.9

- CK3 HTML 图片增加 click-to-see-native 交互；
- node card 仍保持 1:1 统一布局；
- 点击图片打开 lightbox，按原始比例完整查看；
- 支持点击背景 / 关闭按钮 / Esc 关闭；
- 打印时隐藏 lightbox 与 hover 提示；
- `html-layout.md` 补充原比例预览规则。

### v0.8.8

- `config.py` 增加通用 `IMAGE_*` / `AUDIO_*` 后端配置；
- 保留 `AGNES_*` / `MIMO_*` 作为默认兼容配置；
- `generate_images.py` 使用 `IMAGE_BASE_URL` / `IMAGE_API_KEY`；
- `generate_audio.py` 使用 `AUDIO_BASE_URL` / `AUDIO_API_KEY` / `AUDIO_PROVIDER`；
- `workflow-commands.md` 更新开源环境变量说明。

### v0.8.7

- HTML 默认亮色，支持亮 / 暗主题切换；
- localStorage 记忆主题选择；
- 打印强制亮色；
- 明确主题切换属于 view 层，不进入 data.json。

### v0.8.6

- 主 Skill 硬化 + 瘦身；
- 增加 HARD ROUTER；
- 强化 CK1 / CK2 / CK3 / revision 状态边界；
- 增加 CK3 项目类型硬规则。

### v0.8.5 及以前

- 建立 CK1 → CK2 → CK3 工作流；
- 建立 data.json 单一真相源；
- 建立 client / director / execution 三视图；
- 接入图像生成；
- 接入 TTS 声音参考；
- 支持增量修改。

---

## 18. 一句话总结

审美共识引擎不是为了让 AI 一次性生成漂亮方案，而是为了把模糊审美需求变成：

```text
客户能确认、创意能判断、执行能落地、后续能修改的方向资产。
```
