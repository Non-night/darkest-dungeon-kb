# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.steal_buff_stat_type
# 分类
扩展/专项字段
# 参数类型
枚举/固定候选值
# 参数约束
- 旧式偷取／真驱散一次处理的 Buff 数量大于 `1024` 时必定崩溃；实际起崩点不确定。`1000` 是安全极限参考，大于 `1000` 有较高崩溃概率，小于 `1000` 也不保证不崩溃，只是概率更低；不得把该参考理解为安全保证。恰好 `1000` 或 `1024` 的必现性未单独确认。 数量边界由当前用户于2026-11-03补充确认，非本轮新增实机测试。迂回表第34条 P902–P906/X1055–X1059 的963未崩溃、1005已崩溃仅保留为当时测试观察，不推导统一精确阈值。该问题亦称驱散溢出／偷取溢出；按源调用须检查单个目标指定源下的匹配数量。原表先集中多个目标 Buff 再对自身真驱散的流程会集中数量，不能泛化所有真驱散均经过此流程。
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
- `任意的buff type（包括下面5个）`：偷取特定类型的buff至effect发起者，极为强力的设置项，将会根据buff的【类型】（也就是buff的stat_type），将目标身上匹配的buff转移。
使用极为自由，搭配【自己偷自己】的技巧后将产生被称为【超级真驱散】的毁灭性效果，如此使用时需要极为慎重。

常规使用时，配合左侧列出的5种dot，可以通过effect设置项和buff设置项实现相似的效果，当使用此设置项进行偷取时，相似效果的effect和buff都将会被匹配，此即“转移流血、转移腐蚀、转移愈合、转移恐惧、转移延迟扰乱”。

非常规使用时，对其他buff类型进行偷取，即【超级真驱散】。由于此偷取不区分buff来源，极易导致来自于小镇建筑的等永久特殊buff被转移，破坏其他作者的代码机制，乃至由于小镇建筑buff无论如何都不会在同一英雄身上重复施加，而对存档造成永久破坏。因此务必尽可能避免在并非“转移流血、转移腐蚀、转移愈合、转移恐惧、转移延迟扰乱”的场合使用steal_buff_stat_type。

历史术语表曾概括为“大于约1024个可能崩溃”，不再作为现行精确阈值；当前数量风险以本词条参数约束中2026-11-03的确认及机制15为准。
- 参数/候选：`hp_dot_bleed
hp_dot_poison
hp_dot_heal
stress_dot
shuffle_dot`
# 作用范围
- Effect 定义行；实际作用对象由调用方目标与 `.target` 等字段共同决定。
- 可能被技能、饰品触发器、ActorDot、spawn、hp_reaction、奇物等系统引用。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
# 常见错误
- 把字段已收录或格式看似正确误当成“引擎行为已验证”。
- 忽略调用方目标、queue、apply_once、死亡/回合外时序等上下文。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:538`
```darkest
effect: .name test_steal_buff .target target .steal_buff_stat_type hp_dot_bleed .on_hit true .on_miss true .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\effects\flagellant.effects.darkest:95`
```darkest
effect: .name "Flag Steal Bleed" .target "target" .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_bleed .on_hit true .on_miss false .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:26`
```darkest
effect: .name "CC Steal Blight" .target "target" .curio_result_type "positive" .chance 100% .steal_buff_stat_type hp_dot_poison .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
