# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_duration_type
# 分类
Buff/战斗属性
# 参数类型
枚举/固定候选值
# 参数约束
- 参数必须使用 12 个已知合法持续时间类型之一：`round`、`combat_end`、`quest_end`、`quest_complete`、`quest_not_complete`、`activity_end`、`idle_start_town_visit`、`till_removed`、`none`、`before_turn`、`after_turn`、`after_round`。
- 填写非法参数会发生什么当前未确认；创作时不得使用合法表以外的值。
- 与 `.duration` 配套决定 Effect 所施加 Buff 的持续时间。
# 固定值 / 参数候选
- `round`
- `combat_end`
- `quest_end`
- `quest_complete`
- `quest_not_complete`
- `activity_end`
- `idle_start_town_visit`
- `till_removed`
- `none`
- `before_turn`
- `after_turn`
- `after_round`
# 语义
- `.buff_duration_type <type>`：指定持续时间按哪一种事件扣减或保持。
# 作用范围
- Effect 通过 `.buff_ids` 引用 Buff 时，本字段会覆盖 Buff 定义中的 `duration_type`。
- Effect 中未填写本字段时，才使用被引用 Buff 自身定义的 `duration_type`。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 只使用 12 个已知合法值；非法参数的行为当前未确认。
- Effect 中填写该字段时，会覆盖被引用 Buff 定义中的 `duration_type`。
- 详见：[Mechanics/17-Buff持续时间类型与实际清除.md](../../Mechanics/17-Buff持续时间类型与实际清除.md)
- 持续类型只决定持续时间的正常扣减事件；Buff 仍可能因 `remove_if_not_active`、`remove_on_battle_complete` 或 Buff 源的自动清除时机提前消失。
# 常见错误
- 使用 12 个合法值以外的参数。
- 只按持续类型推算真实存续时间，忽略 Buff 自身移除参数和 Buff 源。
- 同时在 Effect 与 Buff 中定义持续类型，却误以为 Buff 定义优先。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:771`
```darkest
effect: .name "Crusader Bulwark Mark" .target "performer" .curio_result_type "positive" .chance 100% .tag 1 .duration 1 .buff_duration_type combat_end	.on_hit true .on_miss true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:765`
```darkest
effect: .name "Crusader Bulwark 1" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .protection_rating_add 20%	.on_hit true .on_miss true .queue true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:766`
```darkest
effect: .name "Crusader Bulwark 2" .target "performer" .curio_result_type "positive" .chance 100% .duration 1 .buff_duration_type combat_end .combat_stat_buff 1 .protection_rating_add 22%	.on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 12 种合法值来自原版字段表与社区持续时间资料；逐类型行为按已整理的社区测试结论记录。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
