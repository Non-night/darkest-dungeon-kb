# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_sub_type
# 分类
Buff/战斗属性
# 参数类型
枚举/固定候选值
# 参数约束
- 参数必须使用下方收录的副类型原样值，并与当前 `.buff_type` 的主副类型关系匹配。
- 仅在当前 `.buff_type` 要求或明确支持副类型时填写，不能脱离 `.buff_type` 单独使用。
- `combat_stat_multiply`、`combat_stat_add`、`resistance`、`activity_side_effect_chance`、`disable_combat_skill_attribute` 必须填写该字段；漏写后果当前未确认。
- `.buff_type riposte` 时可以填写该字段，但该组合存在非必然的红字风险。
# 固定值 / 参数候选
- `max_hp`
- `damage_low`
- `damage_high`
- `attack_rating`
- `crit_chance`
- `defense_rating`
- `protection_rating`
- `speed_rating`
- `riposte_on_hit_chance`
- `riposte_on_miss_chance`
- `stun`
- `move`
- `poison`
- `bleed`
- `disease`
- `debuff`
- `death_blow`
- `trap`
- `armour`
- `weapon`
- `combat_skill`
- `camping_skill`
- `add_currency`
- `remove_currency`
- `add_trinket`
- `remove_trinket`
- `activity_lock`
- `apply_buff`
- `go_missing`
- `heal`
- `buff`
- `tag`
- `stress`
- `guard`
- `daze`
- `hero_skill`
- `hero_skill_multi_target`
- `monster_skill`
- `monster_skill_multi_target`
- `camp_skill`
- `camp_skill_multi_target`
- `companion`
- `eat`
- `act_out`
- `damage_heal`
- `effect`
- `flashback`
- `dot`
- `hunger`
- `hero_crit`
- `hero_killing_blow`
- `mode`
- `control`
- `unkown`
- `town_idle`
- `quest_fail`
- `pass`
- `camping_relieve_stress`
- `camping_eat`
- `tile`
- `retreat`
- `capture`
- `monster_crit`
# 语义
- `.buff_sub_type <sub_type>`：进一步限定 `.buff_type` 系列简写 Buff 的具体子类型。
# 作用范围
- 只属于 `.buff_type` 与 `.buff_amount` 构成的简写 Buff；是否需要填写由主类型决定。
# 引擎行为（重要）
- 原版扫描未找到直接实例；下方案例来自 Mod，只能证明社区内容存在这种写法，仍需实机验证。
- 只在当前 `.buff_type` 要求或明确支持副类型时填写；主副类型必须匹配。
- `riposte` 可以搭配副类型；该组合可能产生红字但并非必然报错，出现红字时 Buff 仍会生效。
- 详见：[Mechanics/14-Effect数值参数与简写Buff.md](../../Mechanics/14-Effect数值参数与简写Buff.md)
- `.buff_type riposte` 可以同时填写 `.buff_sub_type`；该组合可能产生红字报错，但并非必然报错。
- 如果产生红字，Buff 仍会出现并生效；具体触发范围及其他同类主类型尚未确认。
# 常见错误
- 对必须使用副类型的主类型漏写 `.buff_sub_type`。
- 在没有明确主副类型关系时自行添加副类型。
- 把 `riposte` 搭配副类型描述为绝对禁止或必然产生红字。
# 代码案例
- Mod「The Cabinet of Curiosities (test build)」：`effects\deepones_puffers.effects.darkest:36`
```darkest
effect: .name "puffers_ResD_A" .target "target" .chance 100% .duration 3 .buff_type resistance .buff_sub_type move .buff_amount -0.18 .on_hit true .on_miss false
```
- Mod「The Cabinet of Curiosities (test build)」：`effects\deepones_crab.effects.darkest:27`
```darkest
effect: .name "Crab_Bleed_Res_B" .target "target" .chance 120% .duration 3 .buff_type resistance .buff_sub_type bleed .buff_amount -0.25 .on_hit true .on_miss false
```
- Mod「The Cabinet of Curiosities (test build)」：`effects\deepones_harpoon.effects.darkest:14`
```darkest
effect: .name "harpoon_Res_Bleed_A" .target "target" .chance 100% .duration 3 .buff_type resistance .buff_sub_type bleed .buff_amount -0.18 .on_hit true .on_miss false
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例回退：原版未找到该字段时，优先从 Workshop `262060` 选择 Mod 实例；Workshop 无实例时再从本地 `mods` 回退选择。
- 副类型候选值和主副类型关系来自术语表及已整理的字段关系。
- `riposte` 允许搭配副类型及其可能产生红字的行为来自社区实测结论。
- 可信度原则：Mod 只确认该 Mod 如此书写；原版未提供直接实例，不能据此宣称为已验证的引擎规范。
