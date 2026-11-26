# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.attack_rating_multiply
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 接受一个数值参数，可写整数、小数或带 `%` 的数值。
- 常规写法通常使用小数或带 `%` 的数值；整数在语法上也属于可接受的数值形式。
- 该字段似乎需要与用于建立简写 Buff 的其他字段搭配；已确认的常见搭配包括 `.combat_stat_buff 1` 与 `.riposte 1`，但当前不能断言只有这两种。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.attack_rating_multiply <number>`：为对应简写 Buff 提供精准（ACC）倍率修正。
# 作用范围
- `.combat_stat_buff 1` 搭配本字段时，形成普通/通用精准 Buff 的 Effect 简写。这里的“普通/通用”描述简写用途，不表示 Buff 源类型。
- `.riposte 1` 搭配本字段时，形成反击源精准 Buff 的 Effect 简写。
- 当前原版未找到本字段实例；已收录 Mod 案例只直接展示 `.combat_stat_buff 1` 搭配。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 参数可写整数、小数或带 `%` 的数值；通常使用小数或带 `%` 的数值。
- 属于 `.combat_stat_buff` 系战斗属性简写 Buff；这是倍率修正，不得把数值 `0.01` 直接解释为固定增加 1 点精准。
- 完整可用搭配尚未确认。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- Buff 都具有来源；来源可由施加方式决定，也可由专门字段声明。不同 Buff 源具有不同特性。
- `.riposte 1` 可作为反击源简写搭配属于机制结论；当前没有本字段的原版或已收录 Mod 直接实例用于单独证明该组合。
# 常见错误
- 只写 `.attack_rating_multiply`，却没有提供能够建立对应简写 Buff 的配套字段。
- 把 `.combat_stat_buff 1` 中的普通/通用修饰语误解成 Buff 源类型。
- 把唯一的 Mod 案例当成原版引擎规范。
# 代码案例
- Mod「The Lunar Princess Class Mod」：`effects\millap_ranni.effects.darkest:124`
```darkest
effect: .name "ranni_rare_accdebuff" .target "target" .duration 2 .chance -9000% .combat_stat_buff 1 .attack_rating_multiply -0.66 .on_hit true .on_miss false .has_description false
```

# 来源与可信度
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 原版与官方 DLC 未找到 `.attack_rating_multiply` 的直接 Effect 实例。
- 已收录 Mod 案例展示 `.combat_stat_buff 1 .attack_rating_multiply -0.66`。
- 数值形式与配套范围中未完全确认的部分不得扩张为全引擎确定规则。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
