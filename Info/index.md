# Info Header 索引

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


按对象范围定位 Header；字段的精确约束见对应文档和 `RAG/info_fields.jsonl`。

## 通用

| Header | 用途 |
|---|---|
| [`display_modifier:`](headers/Info.display_modifier.md) | 控制单位战斗显示、飘字、血条、光环和出生特效等表现。 |
| [`riposte_skill:`](headers/Info.riposte_skill.md) | 定义反击所使用的技能数据；英雄和怪物均可使用。 |
| [`rendering:`](headers/Info.rendering.md) | 调整单位渲染层级。 |
| [`controlled:`](headers/Info.controlled.md) | 定义单位被控制时的目标站位。 |
| [`health_bar:`](headers/Info.health_bar.md) | 指定单位血条类型。 |
| [`mode:`](headers/Info.mode.md) | 定义单位模式/姿态及模式进入后的附加规则。 |
| [`hp_reaction:`](headers/Info.hp_reaction.md) | 按生命比例阈值触发 Effect。 |
| [`death_reaction:`](headers/Info.death_reaction.md) | 定义死亡时对友方、敌方触发的 Effect。 |
| [`crit:`](headers/Info.crit.md) | 定义攻击技能暴击时附加调用的 Effect。 |
| [`additional_effect:`](headers/Info.additional_effect.md) | 声明额外效果对饰品目标/饰品攻击者的有效性。 |
| [`commonfx:`](headers/Info.commonfx.md) | 定义英雄或怪物共用的表现资源，例如死亡特效。 |
| [`tag:`](headers/Info.tag.md) | 为英雄或怪物添加标签。 |
| [`defending_area_pos_offset:`](headers/Info.defending_area_pos_offset.md) | 调整单位被守护区域的位置偏移。 |

## 怪物

| Header | 用途 |
|---|---|
| [`display:`](headers/Info.display.md) | 定义怪物占据的站位尺寸。 |
| [`battle_backdrop:`](headers/Info.battle_backdrop.md) | 定义怪物参与战斗时使用的战斗背景。 |
| [`wave_background:`](headers/Info.wave_background.md) | 定义波次战斗的背景与动画。 |
| [`stats:`](headers/Info.stats.md) | 定义怪物基础属性和抗性。 |
| [`skill:`](headers/Info.skill.md) | 定义怪物主动技能。 |
| [`personality:`](headers/Info.personality.md) | 配置怪物的 personality 参数；当前只确认 `.prefskill` 是合法数字字段，具体用途未知。 |
| [`loot:`](headers/Info.loot.md) | 定义怪物掉落。 |
| [`monster_brain:`](headers/Info.monster_brain.md) | 引用怪物 AI（monster brain）ID。 |
| [`captor_empty:`](headers/Info.captor_empty.md) | 定义捕获者的空载形态及捕获流程。 |
| [`captor_full:`](headers/Info.captor_full.md) | 定义捕获者的满载形态、释放条件和持续伤害。 |
| [`life_link:`](headers/Info.life_link.md) | 定义怪物之间的生命关联、掉落和死亡变身有效性。 |
| [`shared_health:`](headers/Info.shared_health.md) | 用 ID 将怪物加入共享生命组。 |
| [`shape_shifter:`](headers/Info.shape_shifter.md) | 定义怪物按轮次在多个 class 之间变形。 |
| [`torchlight_modifier:`](headers/Info.torchlight_modifier.md) | 定义怪物战斗对火光范围的修正。 |
| [`battle_modifier:`](headers/Info.battle_modifier.md) | 定义怪物在战斗目标、拖延、突袭、召唤站位和常驻 Buff 等方面的规则。 |
| [`death_damage:`](headers/Info.death_damage.md) | 定义怪物死亡时对指定基础 class 造成的伤害。 |
| [`controller:`](headers/Info.controller.md) | 定义控制者的每回合压力代价及解除控制时的 Effect。 |
| [`battle_stage:`](headers/Info.battle_stage.md) | 指定怪物所属的战斗阶段 ID。 |
| [`companion:`](headers/Info.companion.md) | 定义怪物伴生单位、每回合治疗和常驻 Buff。 |
| [`skill_reaction:`](headers/Info.skill_reaction.md) | 定义怪物受击、击杀或被击杀时触发的 Effect。 |
| [`audio_modifier:`](headers/Info.audio_modifier.md) | 定义怪物战斗音频强度、变体和环境音参数。 |
| [`spawn:`](headers/Info.spawn.md) | 定义怪物生成时或波次生成时调用的 Effect。 |
| [`mash_modifier:`](headers/Info.mash_modifier.md) | 调整 infestation mash 死亡流程。 |
| [`torch_settings:`](headers/Info.torch_settings.md) | 引用火把设置 ID；当前官方配置未找到实例。 |
| [`kill_quirk:`](headers/Info.kill_quirk.md) | 无字段 Header；资料说明它会终止 Info 文件分析流程，具体用途尚未确认。 |
| [`tutorial:`](headers/Info.tutorial.md) | 引用怪物相关教程 ID。 |
| [`wave_spawning:`](headers/Info.wave_spawning.md) | 配置无尽农庄等波次生成场景中的怪物生成属性；当前只确认 `.prefers_front` 是合法布尔字段，具体站位行为未知。 |
| [`colour_grade:`](headers/Info.colour_grade.md) | 指定怪物战斗使用的调色名称。 |

## 英雄

| Header | 用途 |
|---|---|
| [`resistances:`](headers/Info.resistances.md) | 定义英雄各类抗性。 |
| [`weapon:`](headers/Info.weapon.md) | 定义英雄各级武器数据。 |
| [`armour:`](headers/Info.armour.md) | 定义英雄各级护甲数据。 |
| [`combat_skill:`](headers/Info.combat_skill.md) | 定义英雄主动战斗技能。 |
| [`combat_move_skill:`](headers/Info.combat_move_skill.md) | 定义英雄的战斗移动技能。 |
| [`id_index:`](headers/Info.id_index.md) | 定义英雄职业 ID 的索引。 |
| [`sorting_index:`](headers/Info.sorting_index.md) | 定义英雄职业排序索引；当前官方配置未找到实例。 |
| [`generation:`](headers/Info.generation.md) | 定义英雄生成时的怪癖、技能、牌组和事件依赖。 |
| [`skill_selection:`](headers/Info.skill_selection.md) | 定义英雄可选战斗技能及最大装备数量。 |
| [`incompatible_party_member:`](headers/Info.incompatible_party_member.md) | 定义英雄的队伍不兼容 ID 或标签。 |
| [`deaths_door:`](headers/Info.deaths_door.md) | 定义英雄进入死门、离开死门及心脏病恢复时的 Buff/Effect。 |
| [`last_hero:`](headers/Info.last_hero.md) | 定义仅剩最后一名英雄时的 Buff；当前官方配置未找到实例。 |
| [`extra_battle_loot:`](headers/Info.extra_battle_loot.md) | 定义英雄带来的额外战斗掉落。 |
| [`extra_curio_loot:`](headers/Info.extra_curio_loot.md) | 定义英雄互动奇物时的额外战利品。由该英雄亲自互动任意奇物，且本次互动实际产出战利品时，按 `.code` 引用的 Loot 表额外抽取 `.count` 次。 |
| [`extra_shard_bonus:`](headers/Info.extra_shard_bonus.md) | 定义英雄带来的额外水晶奖励。 |
| [`extra_stack_limit:`](headers/Info.extra_stack_limit.md) | 引用英雄可提高堆叠上限的物品 ID。 |
| [`progression:`](headers/Info.progression.md) | 定义英雄是否参与看护者目标。 |
| [`overstressed_modifier:`](headers/Info.overstressed_modifier.md) | 覆盖英雄爆压时可抽取的美德/折磨及概率。 |
| [`activity_modifier:`](headers/Info.activity_modifier.md) | 覆盖英雄可参与的城镇活动和减压量。 |
| [`quirk_modifier:`](headers/Info.quirk_modifier.md) | 定义英雄职业天生不兼容的怪癖/疾病 class。 |
| [`act_out_display:`](headers/Info.act_out_display.md) | 定义英雄发生 act out 并攻击友方时使用的动画、FX 与音效。act out 不只来自折磨或美德，怪癖、疾病等系统也可以带出 act out；原版猩红诅咒系列即包含此类行为。 |
| [`restriction:`](headers/Info.restriction.md) | 限制英雄职业所需启用的 DLC；当前官方配置未找到实例。 |

## 怪物/尸体特殊

| Header | 用途 |
|---|---|
| [`enemy_type:`](headers/Info.enemy_type.md) | 定义怪物类型 ID；英雄职业 Mod 的 corpse 等特殊怪物实体也可使用。一个怪物可以连续写多行 `enemy_type:`，因此可同时属于多个 enemy_type/种族；例如 `.id "aaa"` 与 `.id "bbb"` 表示同时属于 aaa 和 bbb。 |
| [`initiative:`](headers/Info.initiative.md) | 定义怪物每轮行动点数量及行动提示显示；英雄职业 Mod 的 corpse 等特殊怪物实体也可使用。 |
| [`death_class:`](headers/Info.death_class.md) | 定义怪物死亡变身/尸体 class 及其触发条件；英雄职业 Mod 中仅用于 corpse 等特殊怪物实体。 |
| [`life_time:`](headers/Info.life_time.md) | 定义怪物实体的存活轮次限制和掉落检查；英雄职业 Mod 中仅用于 corpse 等特殊怪物实体。 |
