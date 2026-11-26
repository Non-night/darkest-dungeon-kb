# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.crit_chance_add
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 接受一个数值参数，可写整数、小数或带 `%` 的数值。
- 属于 `.combat_stat_buff` 系战斗属性简写 Buff 的属性修正字段；应与对应的简写 Buff 声明配套使用。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.crit_chance_add <number>`：为对应的简写 Buff 增加或减少暴击率。
# 作用范围
- 与 `.combat_stat_buff 1` 等简写 Buff 声明配套时，属于普通/通用战斗属性 Buff；这里的普通/通用不是 Buff 源类型。
- 也可出现在 `.riposte 1` 建立的反击源简写 Buff 中；具体效果仍由所在简写 Buff 的其他字段共同决定。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 参数可写整数、小数或带 `%` 的数值；属于 `.combat_stat_buff` 系战斗属性简写 Buff。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 参数形式与 `.attack_rating_add`、`.attack_rating_multiply` 等已整理的数值型战斗属性字段相同。
# 常见错误
- 将 `.crit_chance_add` 当作独立于简写 Buff 的普通数值效果。
- 忽略其所在的 `.combat_stat_buff` 或其他简写 Buff 配套声明。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:648`
```darkest
effect: .name "Suppression 1" .target "target" .curio_result_type "negative" .chance 100% .duration 2 .combat_stat_buff 1 .attack_rating_add -15% .crit_chance_add -15%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:649`
```darkest
effect: .name "Suppression 2" .target "target" .curio_result_type "negative" .chance 110% .duration 2 .combat_stat_buff 1 .attack_rating_add -16% .crit_chance_add -16%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:650`
```darkest
effect: .name "Suppression 3" .target "target" .curio_result_type "negative" .chance 120% .duration 2 .combat_stat_buff 1 .attack_rating_add -17% .crit_chance_add -17%	.on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 原版 `DarkestDungeon\effects\base.effects.darkest:19` 展示 `.riposte 1` 与 `.crit_chance_add 5%` 的配套写法。
- 用户补充：`.crit_chance_add` 属于 `.combat_stat_buff` 系简写 Buff，参数形式同已整理的数值型战斗属性字段。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
