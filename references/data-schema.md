# data.json Schema

## 顶层结构

```json
{
  "meta": {
    "project": "项目名",
    "project_type": "film|poster|ppt|game|app|mv|brand",
    "style": "整体风格定位",
    "aspectRatio": "1:1",
    "sound_enabled": false,
    "created": "ISO-8601 时间",
    "version": 1
  },
  "summary": {
    "one_sentence": "一句话定调",
    "keywords": ["关键词1", "关键词2"],
    "aligned": ["已对齐共识"],
    "risks": ["待注意分歧或风险"]
  },
  "palette": [
    {"name": "暖米色", "hex": "#C4A882", "usage": "主色"}
  ],
  "timeline|frames|slides|states|journey": [],
  "view": "client|director|execution"
}
```

## 节点结构

每个节点通用字段：

```json
{
  "id": "node-opening",
  "label": "开场",
  "timeRange": "0-30s 可选",
  "emotion": {
    "type": "克制的平静",
    "intensity": 4,
    "keywords": ["疏离", "观察者视角"],
    "description": "..."
  },
  "motion": {
    "type": "缓慢",
    "intensity": 2,
    "description": "静态构图，缓慢推轨，剪辑稀疏"
  },
  "color": {
    "palette": ["#5B748C", "#D8D2C8"],
    "temperature": "冷灰蓝，约 6500K",
    "saturation": "低饱和",
    "description": "..."
  },
  "composition": {
    "type": "封闭空间",
    "camera": "平视/轻微俯拍/仰拍",
    "dof": "浅景深/深景深",
    "description": "..."
  },
  "style": {
    "keywords": ["人文质感", "克制"],
    "texture": "自然光、轻微颗粒、哑光",
    "description": "..."
  },
  "sound": {
    "density": "稀疏",
    "type": "极简环境音",
    "reverb": "干声/小空间",
    "reference": "参考曲目或链接，可空",
    "description": "..."
  },
  "image": {
    "url": "images/node-opening.png 或空",
    "description": "图像内容描述",
    "status": "placeholder|generated|external"
  },
  "image_prompt": "用于生成该节点方向图的提示词",
  "voice_prompt": "音色描述，用于 TTS 生成声音参考（可选）",
  "audio_text": "合成文本，TTS 朗读内容（可选）",
  "audio": {
    "url": "audio/node-opening_xxx.wav 或空",
    "status": "generated",
    "model": "mimo-v2.5-tts-voicedesign",
    "generated_at": "ISO-8601",
    "duration_hint": "~13s"
  }
}
```

## 字段规则

- `id` 使用小写英文、数字、短横线。
- `intensity` 为 1-10。
- 纯平面项目可将 `sound` 留空对象，但不要删除字段。
- 没有生成图时，`image.status` 使用 `placeholder`。
- 图片路径使用相对路径，便于 HTML 单目录分发。
- `voice_prompt` 和 `audio_text` 为可选字段，用于 TTS 音频生成。有值时 `generate_audio.py` 会自动生成。
- `meta.sound_enabled` 为可选布尔值：`true` 强制在 HTML 中显示 sound/audio，`false` 强制隐藏，缺省时按项目类型规则裁剪。
- `audio` 对象由脚本写入，用户不手动填写。
- 修改时只改用户点名字段，保护其他字段。
