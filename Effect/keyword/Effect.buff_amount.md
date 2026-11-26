# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_amount
# 分类
Buff/战斗属性
# 参数类型
单个数值（整数、小数或带 `%` 的数值）
# 参数约束
- 单参数数值关键字；可写整数、小数或带 `%` 的数值。
- 必须与 `.buff_type` 配套使用；缺少 `.buff_type` 时的引擎结果当前未确认。
# 固定值 / 参数候选
- 无固定候选表；按下方参数说明填写。
# 语义
- `.buff_amount <value>`：为 `.buff_type` 系列简写 Buff 提供数值。
# 作用范围
- 仅作为 `.buff_type` 系列简写 Buff 的数值字段使用，不能脱离 `.buff_type` 单独解释。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 与 `.buff_type` 配套构成 `.buff_type` 系列简写 Buff；可写整数、小数或带 `%` 的数值。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- 原版实例确认整数以外的小数和百分号写法均可用；整数写法属于已确认的参数形式，但当前原版案例中未找到直接实例。
# 常见错误
- 只写 `.buff_amount`，不写配套的 `.buff_type`。
- 把 `.buff_amount` 当成独立伤害、治疗或通用数值字段。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2185`
```darkest
effect: .name "test_torchlight_burn" .target target .chance 100% .buff_type torchlight_burn_percent .buff_amount -0.10 .on_hit true .on_miss false
```
- 官方 DLC `702540_shieldbreaker`：`DarkestDungeon\dlc\702540_shieldbreaker\effects\shieldbreaker.effects.darkest:52`
```darkest
effect: .name "Expose Crit Debuff 1" .target "target" .curio_result_type "negative" .chance 100% .buff_type crit_received_chance .buff_amount 8%	.on_hit true .on_miss false
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:324`
```darkest
effect: .name "Stacking Heal 1" .target "target" .curio_result_type "positive" .chance 100% .buff_type hp_heal_received_percent .buff_amount 20%  .on_hit true .on_miss true	.queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 参数形式与配套关系来自原版配置、社区资料和已整理的字段关系。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
