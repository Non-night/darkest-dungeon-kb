# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.buff_source_type
# 分类
Buff/战斗属性
# 参数类型
单个字符串（未知值统一归入 `combat_end` Buff 源）
# 参数约束
- 参数为单个字符串；可填写已收录或未收录的源类型标识。
- 未收录/非法参数不会创建新的自定义源类型；游戏引擎会将其统一视为 `combat_end` Buff 源。
- 源类型的 `Icon` 行若为 `None`，该源下的 Buff 不具有图标。
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
- `.buff_source_type <source>`：为 `buff_ids` 中声明的 Buff 指定 Buff 源类型。
# 作用范围
- 用于给已通过 `buff_ids` 引用的 Buff 声明来源；来源也可能由施加方式或其他专门字段决定。
- 源类型会影响 Buff 的图标、清除、适用范围和其他独有机制，不能只把它当作分类标签。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- `.buff_source_type` 为 `buff_ids` 中声明的 Buff 指定来源；Buff 源不是单纯分类标签。
- 源类型表中 `Icon = None` 表示该来源下的 Buff 不具有图标；`bsrc_notspecified`、`bsrc_last_hero` 与 `bsrc_flashback_start` 非必要不作持久 Buff 来源，`bsrc_battle_modifier` 会在 Any Update 后清除。
- 详见：[Mechanics/15-Buff源与真驱散.md](../../Mechanics/15-Buff源与真驱散.md)
- Buff 源类型的详细表格已转写到 `Mechanics/15-Buff源与真驱散.md`；该表中的 `Icon = None` 表示该源下的 Buff 不具有图标。
- 任意未知/非法源参数都会被引擎归入 `combat_end` 源；这里的 `combat_end` 是 Buff 源，不是持续时间类型。
- 当前用户于 2026-11-02 确认：真光环源 `bsrc_battle_modifier` 需要图标且必定有图标，不能作为无图标来源；来源表 Icon 栏为空不等于 `None`。
- 国内旧式瞬间真驱散较常用 `bsrc_last_hero` 与 `bsrc_flashback_start`（蛇梦开始源）；国外也较常用 `bsrc_notspecified`。非必要不应将这三种源用于持久 Buff；`bsrc_battle_modifier` 的清除时机为 Any Update，不能承担持久 Buff 来源。这是来源经验和生命周期边界，不是当前推荐使用瞬间真驱散。
# 常见错误
- 把任意字符串误认为可以创建彼此独立的自定义 Buff 源。
- 混淆 `combat_end` Buff 源与 `combat_end` 持续时间类型。
- 只依据源名称推断 Buff 的清除或图标行为，却不查源类型表。
- 把 `Icon = None` 的源当作会显示普通 Buff 图标的来源。
- 在需要长期存在的 Buff 中随意使用 `bsrc_notspecified`、`bsrc_last_hero` 或 `bsrc_flashback_start`，或把 Any Update 清除的 `bsrc_battle_modifier` 当作持久来源。
- 为利用自动清除而把 `bsrc_battle_modifier` 误称为无图标源。
# 代码案例
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2160`
```darkest
effect: .name "on_crit_acc"    .target "performer" .curio_result_type "positive" .chance 100% .buff_source_type bsrc_crit .buff_ids "on_crit_acc" .on_hit true .on_miss false .apply_once true
```
- 官方 DLC `4964110_fires_edge`：`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\effects\duelist.effects.darkest:2`
```darkest
effect: .name "on_crit_duelist_def"    .target "performer" .curio_result_type "positive" .chance 100% .buff_source_type bsrc_crit .buff_ids "on_crit_duelist_def" .on_hit true .on_miss false .apply_once true
```
- 游戏本体：`DarkestDungeon\effects\base.effects.darkest:2161`
```darkest
effect: .name "on_crit_def"    .target "performer" .curio_result_type "positive" .chance 100% .buff_source_type bsrc_crit .buff_ids "on_crit_def" .on_hit true .on_miss false .apply_once true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 术语表工作簿：`Sasiji的buff源类型表` 的 `Icon`、清除方式和独有机制行。
- 迂回表第 1 条 P349/X357、P350/X358；当前用户 2026-11-02 对国内外用源经验和持久 Buff 边界作出更正。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
