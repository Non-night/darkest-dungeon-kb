# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.steal_buff_source_type
# 分类
扩展/专项字段
# 参数类型
枚举/固定候选值
# 参数约束
- 旧式偷取／真驱散一次处理的 Buff 数量大于 `1024` 时必定崩溃；实际起崩点不确定。`1000` 是安全极限参考，大于 `1000` 有较高崩溃概率，小于 `1000` 也不保证不崩溃，只是概率更低；不得把该参考理解为安全保证。恰好 `1000` 或 `1024` 的必现性未单独确认。 数量边界由当前用户于2026-11-03补充确认，非本轮新增实机测试。迂回表第34条 P902–P906/X1055–X1059 的963未崩溃、1005已崩溃仅保留为当时测试观察，不推导统一精确阈值。该问题亦称驱散溢出／偷取溢出；按源调用须检查单个目标指定源下的匹配数量。原表先集中多个目标 Buff 再对自身真驱散的流程会集中数量，不能泛化所有真驱散均经过此流程。
- 偷取仍不建议使用：可能错误地偷走不该被偷的 Buff，只有在严格受控的环境中才可自由使用。收录偷取机制或含偷取的方案，不代表推荐在普通环境使用；“标志物”用途不提供隔离其他 Buff 的性质。当前用户于2026-11-03明确补充；非本轮新增实机测试。
- 参数使用已收录的 Buff 源类型标识。
- 该字段会按 Buff 来源匹配目标身上的 Buff；不要把它当作只匹配某一个 Buff ID 的普通驱散字段。
- 真驱散和瞬间真驱散都可能影响同一来源下的多个 Buff，使用前必须确认来源范围。
# 固定值 / 参数候选
- `bsrc_skill`
- `bsrc_notspecified`
- `bsrc_affliction`
- `bsrc_virtue`
- `bsrc_item`
- `bsrc_curio`
- `bsrc_disease`
- `bsrc_riposte`
- `bsrc_campingskill`
- `bsrc_quirk`
- `bsrc_trinket`
- `bsrc_trinket_set`
- `bsrc_instantSkill`
- `bsrc_guard`
- `bsrc_deathsdoor`
- `bsrc_deathsdoor_recovery`
- `bsrc_deathsdoor_recovery_heart_attack`
- `bsrc_quest_failure`
- `bsrc_companion`
- `bsrc_stun`
- `bsrc_town`
- `bsrc_district`
- `bsrc_torchsettings`
- `bsrc_crit`
- `bsrc_trinket_additional_effect`
- `bsrc_battle_modifier`
- `bsrc_never_again`
- `bsrc_vampire`
- `bsrc_town_event`
- `bsrc_flashback_start`
- `bsrc_flashback_result`
- `bsrc_completed_darkest_dungeon_quest_party_hero`
- `bsrc_quest_modifier`
- `bsrc_last_hero`
- `combat_end`
# 语义
- `.steal_buff_source_type <source>`：将目标身上属于指定源类型的 Buff 偷取至 Effect 发起者。
- 当偷取目标是 Effect 发起者自身时，该源类型的 Buff 会因偷取后丢弃而直接消失；这称为真驱散。
# 作用范围
- 作用单位由 `.target` 和调用方决定；匹配单位是目标身上属于指定 Buff 源的全部相关 Buff。
- 从 size0 等特殊单位发起偷取并在完成后自灭时，效果上也可等同于真驱散。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 按指定来源偷取目标身上的全部 Buff；目标为 Effect 发起者自身时，匹配 Buff 会直接消失，形成真驱散。
- 瞬间真驱散是旧式按源善后方案；当前可用 `clear_buffs_on_rule_active` 时应使用 Buff ID 定向驱散，不把前者用于强度或清除本应不可驱散的其他作者 Buff。
- 详见：[Mechanics/15-Buff源与真驱散.md](../../Mechanics/15-Buff源与真驱散.md)
- 该字段是按来源批量处理 Buff 的强力字段；真驱散可能同时影响同一来源的多个 Buff。
- 旧式瞬间真驱散的国内用源较常见 `bsrc_last_hero`、`bsrc_flashback_start`，国外还较常见 `bsrc_notspecified`；`bsrc_battle_modifier` 可用但不常见。当前可用 ID 定向驱散时，不应再将按源瞬间真驱散作为善后方案。
- 社区经验明确不建议对 `bsrc_district` 使用真驱散，也不建议对 `bsrc_skill` 使用真驱散；不要在不了解迂回代码时滥用。
- 真驱散只用于迂回机制设计，不作为强度手段；不得直接移除其他作者设计中本应不可驱散的增减益。崩溃和不可逆存档变动是原表警示的风险，不是每次操作必然发生的引擎结论。
# 常见错误
- 以为该字段只移除一个 Buff，忽略它会匹配指定源下的全部 Buff。
- 未确认 `.target` 就使用自己偷自己，造成非预期的批量真驱散。
- 对 `bsrc_district` 或 `bsrc_skill` 使用真驱散，却没有评估对城镇建筑或技能 Buff 的全局影响。
- 把瞬间真驱散使用源用于长期 Buff。
- 为提高强度而按源清除本应不可驱散的其他作者 Buff，或在可用 ID 定向驱散时仍将旧式按源瞬间真驱散当作默认清理方案。
# 代码案例
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:272`
```darkest
effect: .name "Absorb Effect" 	.target "target" .chance 100% .steal_buff_source_type bsrc_skill  .on_hit true .on_miss false .queue true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:332`
```darkest
effect: .name "Viscount Absorb Effect" 	.target "target" .chance 100% .steal_buff_source_type bsrc_skill  .on_hit true .on_miss false .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 术语表工作簿 `Effects` 对 `.steal_buff_source_type` 的说明。
- 真驱散、瞬间真驱散及来源选择属于社区迂回代码经验；字段的批量匹配行为需按来源范围推理。
- 迂回表第 1 条 P352/X362 的设计安全告诫；当前用户 2026-11-02 确认纳入，并更正 P350/X358 的用源经验，要求可用版本改采 Buff ID 定向驱散。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
