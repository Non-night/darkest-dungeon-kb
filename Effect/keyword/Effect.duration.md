# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.duration
# 分类
扩展/专项字段
# 参数类型
数值（整数/小数及单位以参数说明为准）
# 参数约束
- 数值表示持续多少个 `.buff_duration_type` 所指定的时间单位。
- 小于 0 的持续时间不会正常耗尽，但仍可能被 Buff 自身参数或 Buff 源提前清除。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.duration <value>`：指定 Effect 所施加效果或 Buff 的持续时间数值。
# 作用范围
- Effect 通过 `.buff_ids` 引用 Buff 时，本字段会覆盖 Buff 定义中的 `duration`。
- Effect 中未填写本字段时，才使用被引用 Buff 自身定义的 `duration`。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 数值单位由持续时间类型决定；Effect 中填写该字段时，会覆盖被引用 Buff 定义中的 `duration`。
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
- Effect 中的持续时间字段优先于 Buff 定义中的对应字段。把持续时间写在 Effect 中而不写在 Buff 中是一种常见书写习惯，不是强制规范或特别推荐。
# 常见错误
- 脱离持续时间类型解释 `.duration` 的单位。
- 认为负持续时间或尚未到期就能阻止来源清除、脱战清除等提前移除。
- 同时在 Effect 与 Buff 中定义持续时间，却误以为 Buff 定义优先。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:108`
```darkest
effect: .name "Blight 1" .target "target" .curio_result_type "negative" .chance 100%  .dotPoison 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:109`
```darkest
effect: .name "Blight 2" .target "target" .curio_result_type "negative" .chance 110%  .dotPoison 2 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:110`
```darkest
effect: .name "Blight 3" .target "target" .curio_result_type "negative" .chance 120%  .dotPoison 3 .duration 3	.on_hit true .on_miss false .can_apply_on_death true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 持续时间覆盖规则与真实清除边界来自社区测试及术语表说明。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
