# Workflow Commands

本文件记录 moodboard-alignment / 审美共识引擎的底层脚本实现面。主 `SKILL.md` 与 `assets/so-workflow/so-template.json` 定义官方治理入口与工作流边界；本文件只说明这些节点在脚本层通常如何落地，不把脚本直跑声明为高于 SO 的官方入口。

> 推荐从任意工作目录使用绝对脚本路径，避免当前目录不同导致命令不可用。

## SO 治理入口

如果当前运行使用 Loom Skill Orchestrator 治理，先以以下已检入资产为准：

- workflow source template：`assets/so-workflow/so-template.json`
- runtime package lock：`assets/so-workflow/so-package-lock.json`
- CK 状态分类子代理：`assets/agents/moodboard-alignment-ck-state-classifier.agent.md`

治理约束：

1. 先从绑定运行时执行 fresh `dotnet so.dll --guide`，再继续 `compile` / `run` / `resume`。
2. CK 状态判断、触发词识别与 revision 上下文缺口，应优先走 `assets/agents/moodboard-alignment-ck-state-classifier.agent.md`。
3. 运行时 workflow 副本、事件日志和 compile / run 审计产物默认保持在 Skill 目录外。

说明：

- 若处于 SO 治理模式，下面的 Python 命令属于 workflow 节点的底层执行面，不替代 `dotnet so.dll --guide`、`compile`、`run`、`resume` 作为官方工作流控制路径。
- 若调用者没有启用 SO 治理，才可把下面脚本视为手动执行参考。

## 路径变量示例

```bash
SKILL=/var/minis/skills/moodboard-alignment
PROJECT=/var/minis/workspace/moodboards/<project-slug>
DATA=$PROJECT/data.json
```

## CK2：渲染确认文档

CK2 允许创建 / 更新 `data.json` 作为“待确认方向稿”，只渲染确认文档，不生成图像、音频或最终三视图。

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

## CK3：校验 data.json

```bash
python3 $SKILL/scripts/validate_data.py --data-json $DATA
```

严格模式：warning 也返回非零退出码。

```bash
python3 $SKILL/scripts/validate_data.py --data-json $DATA --strict
```

## CK3：生成方向图

需要环境变量 `IMAGE_API_KEY`；如果使用默认 Agnes 后端，也可只设置 `AGNES_API_KEY`。默认直连 OpenAI-compatible Images API：`IMAGE_BASE_URL` 环境变量，缺省为 Agnes `https://apihub.agnes-ai.com/v1`。

```bash
python3 $SKILL/scripts/generate_images.py \
  --data-json $DATA \
  --model agnes-image-2.1-flash
```

单节点重生成：

```bash
python3 $SKILL/scripts/generate_images.py \
  --data-json $DATA \
  --node-id node-opening \
  --model agnes-image-2.1-flash
```

图像生成失败时，脚本会把该节点标记为 `placeholder` 并继续后续节点，不阻塞全流程。

## CK3：生成声音参考

需要环境变量 `AUDIO_API_KEY`；如果使用默认 Mimo TTS 后端，也可只设置 `MIMO_API_KEY`。节点可填写 `voice_prompt` 与 `audio_text`；缺省时脚本会尝试使用 `sound.description`。当前内置音频 provider 为 `mimo_chat_audio`，兼容返回 `choices[0].message.audio.data` 的 chat-audio API。

```bash
python3 $SKILL/scripts/generate_audio.py --data-json $DATA
```

单节点重生成：

```bash
python3 $SKILL/scripts/generate_audio.py \
  --data-json $DATA \
  --node-id node-opening
```

## CK3：渲染最终三视图 HTML

默认建议使用 `--embed` 生成可单文件分发的 HTML。

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

## 推荐输出结构

```text
<project>/
├── data.json
├── ck2-client.html
├── ck2-execution.html
├── index-client.html
├── index-director.html
├── index-execution.html
├── images/
└── audio/
```

## 常见增量修改命令

只重新渲染三视图，不重新生成图像/音频：

```bash
python3 $SKILL/scripts/validate_data.py --data-json $DATA
python3 $SKILL/scripts/render.py --data-json $DATA --output $PROJECT/index-client.html --view client --embed
python3 $SKILL/scripts/render.py --data-json $DATA --output $PROJECT/index-director.html --view director --embed
python3 $SKILL/scripts/render.py --data-json $DATA --output $PROJECT/index-execution.html --view execution --embed
```
