# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.combat_stat_buff
# 分类
Buff/战斗属性
# 参数类型
数字布尔（合法值：`0`、`1`）
# 参数约束
- 参数使用数字布尔；建立该系列简写 Buff 时写 `.combat_stat_buff 1`。
- 需要与具体战斗属性改变量字段配套；完整字段集合尚未在本词条中穷举。
# 固定值 / 参数候选
- `0`
- `1`
# 语义
- `.combat_stat_buff 1`：启用 `.combat_stat_buff` 系列的 Effect 简写战斗属性 Buff。
# 作用范围
- 属于 Effect 简写 Buff 的一种，与 `.buff_type` / `.buff_amount` 系列并列，不能把“Effect 简写 Buff”只理解为 `.buff_type` 系列。
- 原版配套实例包括 `.speed_rating_add`、`.attack_rating_add`、`.defense_rating_add` 等战斗属性改变量字段。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.combat_stat_buff` 系列是另一类 Effect 简写 Buff；`.combat_stat_buff 1` 与战斗属性改变量字段配套使用。
- 所有 `combat_stat_*` 系战斗属性 Buff 都先计算固定值／add，再对加法后的结果计算百分比／multiply。
- “普通/通用”只描述该简写形式，不是 Buff 源类型。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- `.combat_stat_buff 1` 配套战斗属性改变量字段时，形成普通/通用的简写战斗属性 Buff；“普通/通用”不是 Buff 源类型。
- 所有 `combat_stat_*` 系战斗属性 Buff 均按先加后乘结算：先计入固定值／`*_add`，再对加法后的结果应用百分比／`*_multiply`。
# 常见错误
- 把“Effect 简写 Buff”与 `.buff_type` 系列视为完全同义。
- 只写 `.combat_stat_buff 1`，却没有提供具体战斗属性改变量字段。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:215`
```darkest
effect: .name "Self Speed" 	 .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .speed_rating_add 9	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:242`
```darkest
effect: .name "ACC Debuff 1" .target "target" .curio_result_type "negative" .chance 75% .combat_stat_buff 1 .attack_rating_add -10%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:231`
```darkest
effect: .name "Dodge 1" .target "performer" .curio_result_type "positive" .chance 100% .combat_stat_buff 1 .defense_rating_add 20%	.on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 游戏本体存在 `.combat_stat_buff 1` 与多个战斗属性改变量字段配套的直接实例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
