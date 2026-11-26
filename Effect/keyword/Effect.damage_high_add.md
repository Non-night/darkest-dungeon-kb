# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.damage_high_add
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 接受一个数值参数，可写整数、小数或带 `%` 的数值。
- 属于 `.combat_stat_buff` 系战斗属性简写 Buff 的属性修正字段；应与用于建立简写 Buff 的配套声明一起使用。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.damage_high_add <number>`：为对应简写 Buff 增加或减少最高伤害。
# 作用范围
- 与 `.combat_stat_buff 1` 配套时，属于普通/通用战斗属性简写 Buff；“普通/通用”不是 Buff 源类型。
- 也可出现在 `.riposte 1` 建立的反击源简写 Buff 中；具体来源与其他 Buff 特性由配套声明和施加方式共同决定。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 参数可写整数、小数或带 `%` 的数值；属于 `.combat_stat_buff` 系战斗属性简写 Buff，修正最高伤害。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 参数形式与 `.attack_rating_add`、`.attack_rating_multiply`、`.crit_chance_add` 等已整理的数值型战斗属性字段相同。
- `_add` 表示加法修正；`high` 指伤害区间的最高端。
# 常见错误
- 将 `.damage_high_add` 当作脱离简写 Buff 的独立伤害效果。
- 忽略其所在的 `.combat_stat_buff` 或其他简写 Buff 配套声明。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:19`
```darkest
effect: .name "Riposte Example"  .target "performer" .curio_result_type "positive" .chance 100% .riposte 1 .riposte_on_hit_chance_add 100% .riposte_on_miss_chance_add 100% .on_hit true .on_miss true .duration 2 .damage_low_add 0.01 .damage_high_add 0.01 .attack_rating_add 0.01 .crit_chance_add 5% .riposte_effect "Wyrd Bleed 5"
```

# 来源与可信度
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 `DarkestDungeon\effects\base.effects.darkest:19` 展示 `.riposte 1` 与 `.damage_high_add 0.01` 的配套写法。
- 用户补充：`.damage_high_add` 属于 `.combat_stat_buff` 系简写 Buff，参数性质同其他数值型战斗属性字段。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
