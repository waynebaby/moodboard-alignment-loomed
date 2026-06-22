# 项目类型模板

## 通用层

所有项目都经过：输入识别 → 对齐检测 → CK1 → CK2 → CK3。

六维不变，但权重随项目变化；data.json 中所有六维字段始终保持（不删字段），但 HTML 中根据项目类型只显示相关维度。

## HTML 维度显示规则

data.json 保留完整六维，HTML 只显示该项目类型有意义的维度：

| 项目类型 | emotion | motion | color | composition | style | sound |
|---|---|---|---|---|---|---|
| film | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| mv | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| poster | ✅ | — | ✅ | ✅ | ✅ | — |
| brand | ✅ | — | ✅ | ✅ | ✅ | — |
| ppt | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| app | ✅ | ✅ | ✅ | ✅ | ✅ | — |
| game | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| unknown | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

说明：
- 「motion 动作/节奏」在影视、MV、PPT、游戏、App 中有意义（镜头运动/页面切换/交互节奏/游戏状态切换），在海报和品牌中不显示。
- 「sound 声音」在影视、MV、游戏中有明确维度，在海报/品牌/PPT/App 中默认不显示——声音可在执行层注意中提及，不进 node card。
- 如果 App/PPT/品牌/H5 等项目本身是声音驱动体验，可在 `meta.sound_enabled: true` 时强制显示 sound/audio；也可用 `false` 强制隐藏。
- emotion、color、composition、style 所有类型都显示。

数据保持完整，显示按类型裁剪。

## film / 影视广告

数组字段：`timeline`

适合：广告片、品牌短片、剧情短片、纪录片、TVC、宣传片。

结构：开场 / 发展 / 转折 / 高潮 / 回落，可按材料调整。

权重：emotion > motion > color > composition > sound > style。声音必须写。

CK2 必写：
- 时间范围
- 情绪曲线
- 动作/剪辑节奏
- 色彩迁移
- 构图与镜头倾向
- 声音密度/参考
- 执行注意：拍摄/灯光/后期/声音

## mv / 音乐 MV

数组字段：`timeline`

结构跟随音乐段落：intro / verse / pre-chorus / chorus / bridge / outro。

权重：sound > motion > color > emotion > composition > style。

必须把音乐段落和视觉变化对应起来。

## poster / 海报美术

数组字段：`frames`

适合：海报、主视觉、KV、平面美术、封面。

结构：主视觉定调，可追加变体 A/B/C。

权重：composition > color > style > emotion。sound 可省略或转译为视觉节奏。

CK2 必写：
- 核心定调
- 主体/背景/留白比例
- 视觉重心
- 色板
- 材质/字体/图形倾向
- 适配尺寸注意

## brand / 品牌产品

数组字段：`frames`

适合：品牌调性、产品发布、品牌视觉方向。

结构：核心定调 / 使用场景 / 细节质感 / 延展样式。

权重：color > style > composition > emotion。

必须回答：这个品牌给人的第一感觉是什么，和竞品如何区分。

## ppt / 宣讲演示

数组字段：`slides`

适合：路演、汇报、提案、发布会 Keynote。

结构：封面 / 背景 / 问题 / 方案 / 数据 / 高潮页 / 结尾。

权重：color > composition > motion > style。sound 通常省略。

CK2 必写：
- 页面情绪地图
- 色彩切换规则
- 信息密度
- 字体/图表风格
- 高潮页视觉策略

## app / 网站 App

数组字段：`journey`

适合：网站、App、H5、小程序、产品界面。

结构：入口 / 浏览 / 决策 / 操作 / 成功反馈 / 空状态。

权重：motion > color > composition > style > emotion。sound 通常省略。

必须把审美词转成 UI 语言：信息层级、留白、组件圆角、按钮状态、动效节奏。

## game / 游戏互动

数组字段：`states`

适合：游戏、互动装置、沉浸式体验。

结构：主菜单 / 教程 / 探索 / 战斗 / Boss / 失败 / 结局。

权重：motion > sound > color > composition > emotion > style。

必须描述状态切换和玩家心理变化。

## unknown

如果项目类型未知，先问一个必要问题：
> 这份情绪板主要用于影视/广告、平面海报、PPT、App/网站、游戏互动，还是品牌定调？

如果用户不想选，默认用 `brand` 做中性情绪板。
