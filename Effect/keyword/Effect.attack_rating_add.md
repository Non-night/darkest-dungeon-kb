# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.attack_rating_add
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 接受一个数值参数，可写整数、小数或带 `%` 的数值。
- 常规写法通常使用整数；小数与带 `%` 的写法同样可用。
- 该字段似乎需要与用于建立简写 Buff 的其他字段搭配；已确认的常见搭配包括 `.combat_stat_buff 1` 与 `.riposte 1`，但当前不能断言只有这两种。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.attack_rating_add <number>`：为对应简写 Buff 增加或减少精准（ACC）。
# 作用范围
- `.combat_stat_buff 1` 搭配本字段时，形成普通/通用精准 Buff 的 Effect 简写。这里的“普通/通用”描述简写用途，不表示 Buff 源类型。
- `.riposte 1` 搭配本字段时，形成反击源精准 Buff 的 Effect 简写。
- 其他可用搭配尚未整理完整。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 参数可写整数、小数或带 `%` 的数值；通常使用整数。
- 属于 `.combat_stat_buff` 系战斗属性简写 Buff；文件值 `0.01` 对应游戏内固定增加 1 点精准。
- `.combat_stat_buff 1` 与 `.riposte 1` 是已知常见配套形式。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- Buff 都具有来源；来源可由施加方式决定，也可由专门字段声明。不同 Buff 源具有不同特性。
- 不得仅凭使用了 `.combat_stat_buff 1`，就把“普通/通用”当成某个具体 `.buff_source_type`。
# 常见错误
- 只写 `.attack_rating_add`，却没有提供能够建立对应简写 Buff 的配套字段。
- 把 `.combat_stat_buff 1` 中的普通/通用修饰语误解成 Buff 源类型。
- 默认认为只能与 `.combat_stat_buff 1` 或 `.riposte 1` 搭配；当前仅确认它们是常见搭配，未确认完整集合。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:242`
```darkest
effect: .name "ACC Debuff 1" .target "target" .curio_result_type "negative" .chance 75% .combat_stat_buff 1 .attack_rating_add -10%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:19`
```darkest
effect: .name "Riposte Example"  .target "performer" .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .on_hit true .on_miss true .duration 2 .damage_low_add 0.01 .damage_high_add 0.01 .attack_rating_add 0.01 .crit_chance_add 5% .riposte_effect "Wyrd Bleed 5"
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:408`
```darkest
effect: .name "Deadly Buff 1" .target "target" .curio_result_type "positive" .chance 100%  .combat_stat_buff 1 .attack_rating_add 4% .crit_chance_add 5% .damage_low_multiply 8%  .damage_high_multiply 8%   .on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 `DarkestDungeon\effects\base.effects.darkest:242` 展示 `.combat_stat_buff 1` 搭配写法。
- 原版 `DarkestDungeon\effects\base.effects.darkest:19` 展示 `.riposte 1` 搭配写法。
- 其他可用搭配范围尚未完全确认。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
