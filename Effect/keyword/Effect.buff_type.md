# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_type
# 分类
Buff/战斗属性
# 参数类型
枚举/固定候选值
# 参数约束
- 参数必须使用下方收录的主类型原样值。
- 必须与 `.buff_amount` 配套使用；缺少 `.buff_amount` 时的引擎结果当前未确认。
- `combat_stat_multiply`、`combat_stat_add`、`resistance`、`activity_side_effect_chance`、`disable_combat_skill_attribute` 必须同时填写 `.buff_sub_type`。
- `.buff_type riposte` 可以填写 `.buff_sub_type`；该组合存在红字风险，但并非必然报错。
# 固定值 / 参数候选
- `hp_heal_amount`
- `hp_heal_percent`
- `hp_heal_received_percent`
- `combat_stat_multiply`
- `combat_stat_add`
- `resistance`
- `poison_chance`
- `bleed_chance`
- `stress_dmg_percent`
- `stress_dmg_received_percent`
- `stress_heal_percent`
- `stress_heal_received_percent`
- `party_surprise_chance`
- `monsters_surprise_chance`
- `ambush_chance`
- `scouting_chance`
- `starving_damage_percent`
- `upgrade_discount`
- `damage_received_percent`
- `debuff_chance`
- `resolve_check_percent`
- `stun_chance`
- `move_chance`
- `remove_negative_quirk_chance`
- `food_consumption_percent`
- `resolve_xp_bonus_percent`
- `activity_side_effect_chance`
- `vampire_evolution_duration`
- `quirk_evolution_death_immune`
- `disable_combat_skill_attribute`
- `guard_blocked`
- `tag_blocked`
- `ignore_protection`
- `ignore_stealth`
- `crit_received_chance`
- `riposte`
- `tag`
- `guarded`
- `vampire`
- `stealth`
- `hp_dot_bleed`
- `hp_dot_poison`
- `hp_dot_heal`
- `stress_dot`
- `shuffle_dot`
- `torch_increase_percent`
- `torch_decrease_percent`
- `torchlight_burn_percent`
- `stress_on_miss`
- `stress_from_idle_in_town`
- `shard_reward_percent`
- `shard_consume_percent`
- `damage_reflect_percent`
- `hp_dot_bleed_duration_received_percent`
- `hp_dot_bleed_duration_percent`
- `hp_dot_bleed_amount_received_percent`
- `hp_dot_bleed_amount_percent`
- `hp_dot_poison_duration_received_percent`
- `hp_dot_poison_duration_percent`
- `hp_dot_poison_amount_received_percent`
- `hp_dot_poison_amount_percent`
- `stress_dot_duration_received_percent`
- `stress_dot_duration_percent`
- `stress_dot_amount_received_percent`
- `stress_dot_amount_percent`
- `hp_heal_dot_duration_received_percent`
- `hp_heal_dot_duration_percent`
- `hp_heal_dot_amount_received_percent`
- `hp_heal_dot_amount_percent`
- `shuffle_dot_duration_received_percent`
- `shuffle_dot_duration_percent`
- `guard_duration_received_percent`
- `guard_duration_percent`
- `cure_bleed_received_chance`
- `cure_poison_received_chance`
- `cure_bleed_chance`
- `cure_poison_chance`
- `random_target_friendly_chance`
- `random_target_attack_chance`
- `transfer_debuff_from_attacker_chance`
- `transfer_buff_from_attacker_chance`
- `quirk_tag_evolution_duration`
- `deathblow_chance`
- `heartattack_stress_heal_percent`
- `ignore_guard`
- `buff_duration_percent`
- `riposte_duration_percent`
# 语义
- `.buff_type <type>`：选择 `.buff_type` 系列简写 Buff 的主类型。
# 作用范围
- 与 `.buff_amount` 共同建立简写 Buff；部分主类型还需要 `.buff_sub_type`。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 与 `.buff_amount` 配套；部分主类型必须同时填写 `.buff_sub_type`。
- `riposte` 可以填写 `.buff_sub_type`；该组合可能产生红字但并非必然报错，出现红字时 Buff 仍会生效。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- `.buff_type riposte` 可以同时填写 `.buff_sub_type`；该组合有可能产生红字报错，但并非必然报错，具体触发范围尚未明确。
- 如果产生红字，已知表现是 Buff 仍会出现并生效；目前尚未确认还有哪些主类型存在同类行为。
- 当前用户明确补充（2026-09-24）：在绝大多数情况下，不应设计或使用 `.buff_type disable_combat_skill_attribute` 搭配 `.buff_sub_type buff` 或 `debuff`；禁用增益技能/禁用减益技能极易误伤自定义文本。只有确有必要且已核对影响范围时才考虑例外。
- 当前用户明确补充（2026-09-24）：不要把 `description_tooltip_id` 挂载在 `.buff_type tag` 上；这会强制在 Buff 栏渲染标记图标和内容。常驻驱散 Buff 或其他不需要标记出现的场合，即使 amount 为 0，也不要使用 Buff 型 `tag`。
# 常见错误
- 只写 `.buff_type`，不写配套的 `.buff_amount`。
- 对要求副类型的主类型漏写 `.buff_sub_type`；具体后果当前未确认。
- 把 `riposte` 与 `.buff_sub_type` 的组合误写成绝对禁止，或误写成必然产生红字。
- 不检查主副类型关系，任意组合 `.buff_type` 与 `.buff_sub_type`。
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
- 主类型候选值和主副类型关系来自术语表及已整理的字段关系。
- `riposte` 允许搭配副类型及其可能产生红字的行为来自社区实测结论。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
