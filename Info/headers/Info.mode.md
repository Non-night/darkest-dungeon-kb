# `mode:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄/怪物通用 Header；不能仅依据当前官方实例分布把它判为单侧专用。
- **用途**：定义单位模式/姿态及模式进入后的附加规则。
- **官方实例分布**：英雄 13 次字段出现、怪物 90 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.id` | 单个字符串 ID；局师傅表记录至多 32 字符，静态长度规则记录至多 64 字符；资料冲突时保守按 32 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 模式ID。不要把重复同ID的mode:当作技能或Effect式的分行合并：2026-11-08社区测试中模式名称重复显示，战斗开始Effect仅上方定义执行。适用范围及原始证据见Sources/mode_split_20261108.json；不推导跨文件/跨Mod或所有其他模式字段的重复行为。 | 静态合法字段表、同ID模式分行：Cathelia2026-11-08社区测试与截图；Sources/mode_split_20261108.json、游戏本体/官方 DLC 实例 |
| `.is_raid_default` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 知识库编写者确认：通常所说‘模式可以带出战斗’就是该 mode 写有 `.is_raid_default true`；它表示该模式作为可带出战斗的默认模式使用。不要把普通 `.set_mode` 或其他模式字段自动解释成同义语句。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.bark_override_id` | 后跟最多32字符；字符串参数至多 1 个；每个至多 32 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.stress_damage_per_turn` | 一个数字，支持小数 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 英雄 mode 定义中的每回合压力。英雄因眩晕而空过回合时，不触发这项模式压力；仅限该字段，不推广所有回合加压、DOT、冷却或主动跳过回合。证据：迂回表第46条 P1093/X1270–P1094/X1271，当前用户于2026-11-03确认补入；非本轮新增实机测试。怪物持有者的对应行为不由该英雄场景保证。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.battle_complete_combat_skill_id` | 后跟最多512字符；字符串参数至多 1 个；每个至多 512 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 指定战斗结束／脱战时自动使用的技能。迂回表第133条记录该脱战自动技能不处于对应 `skill` Rule 的有效范围，因此由 `skill` Rule 限定的 Buff 在此自动技能调用中不生效；仅限该脱战调用，不推广到普通技能或其他自动调用。原表历史观察的总体结论仍可参考，但新版新增强制选择后的具体交互尚未重测。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.affliction_combat_skill_id` | 后跟最多512字符；字符串参数至多 1 个；每个至多 512 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 指定英雄折磨时自动使用的技能。迂回表第133条后续更正记录：战斗内触发的折磨自动技能处于对应 `skill` Rule 的有效范围，包括使用官方移动位置的隐藏折磨自动技能；战斗外触发的折磨自动技能不处于该范围。P2058 将战斗外折磨自动技能类比脱战技能的说法是早期推测，已由 P2061–P2063 的后续测试区分更正。第135条还记录折磨自动技能大体上能绕过若干技能可用性限制，但新版新增强制选择后的具体交互尚未重测。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.always_guard_actor_base_class_ids` | 后跟最多4个字符串 ID，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_targetable` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 当前用户于2026-11-02确认：该字段属于 mode: 定义。false 时该单位不成为常规技能或 AOE 的指向目标，非指向性 Effect 或其他非技能效果仍可能命中；不能视为绝对免疫。是否运行时切换模式由玩法决定，始终不可选中的设计不必额外切换模式。参见 Mechanics/57-无法被选中迂回.md；非本轮新增实机测试。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.keep_rounds_in_ranks` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.battle_start_effect_ids` | 字符串参数至多 8 个；每个至多 64 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 战斗开始时对该单位调用所列 Effect。至多 8 个 Effect ID，每个 ID 不超过 64 字符。不能用重复同ID的mode:分行追加本列表：Cathelia于2026-11-08测试同文件相邻两条mode:，仅上方第一条的列表执行，下方第二条未执行，并出现模式名称重复显示；上方指书写位置，不是Mod优先级。跨文件/跨Mod及其他字段行为不由此例保证。来源Sources/mode_split_20261108.json。知识库编写者2026-11-09确认可在该列表给自身施加combat_start_additional_effect_ids附魔Buff，新附魔内Effect在本次战斗开始即可触发，用以扩展8个引用不足的调用链；但战斗开始附魔再引出的新战斗开始附魔不能本次连带触发，不能依靠新附魔在本次连带触发来无限递推。不提高原列表上限，切模式仍须原有特殊流程。来源Sources/spawn_sharing_and_mode_start_enchantment_20261109.json。 | 静态合法字段表、同ID模式分行：Cathelia2026-11-08社区测试与截图；Sources/mode_split_20261108.json、Fire's Edge 无夜译注表、游戏本体/官方 DLC 实例 |

## 用战斗开始自附魔扩展 Effect 调用链

知识库编写者2026-11-09确认：模式 `.battle_start_effect_ids` 给自身施加带 `combat_start_additional_effect_ids` 的Buff，该新附魔内部的Effect能在**本次战斗开始**触发。因此原列表8个Effect引用不够用时，可通过附魔扩展调用链，而不是等待下一场战斗。

这不增加原列表8个ID的上限，也不依赖同ID模式分行合并。知识库编写者进一步确认：**战斗开始附魔A再引出新的战斗开始附魔B时，B不能在本次连带触发，不能依靠新附魔在本次连带触发来无限递推。** 模式直接施加A可本次触发，与A施加B不能连带触发是不同层级；不推断B下一场是否触发。附魔Buff的Rule须生效；若其Effect用于切模式，仍遵守既有战斗开始切模式的特殊前置流程。详见 `Mechanics/92-附魔自附魔时序与 AWR 边界.md`，来源 `Sources/spawn_sharing_and_mode_start_enchantment_20261109.json` / `MODE-START-ENCHANT-01`、`MODE-START-ENCHANT-02`；本轮Agent未自行游戏测试。

## 同 ID 模式定义不能按技能或 Effect 式分行合并

知识库编写者提供Cathelia于2026-11-08 22:52的聊天与截图并确认入库：同一文件中相邻两条 `mode:` 均使用 `.id foreigner .is_raid_default true`，第一条的 `.battle_start_effect_ids` 引用2个Effect，第二条引用另外6个Effect。观察到模式名称“降临者之形”重复显示；Cathelia另反馈战斗开始只执行第一条的2个Effect，第二条的6个未执行，而不是合并为8个执行。

这里的“高者生效”仅指**同一文件中书写位置靠上的第一条定义**，不是Mod优先级，也不是已证明的跨文件加载规则。不能通过重复同ID的 `mode:` 来追加战斗开始Effect，更不能套用技能无等级共用分行或Effect同名分行规则。

不由此例推导跨文件、跨Mod/DLC、其他模式字段重复定义或不同 `.is_raid_default` 组合的行为。来源 `Sources/mode_split_20261108.json` 保留原始两条定义、两张截图的相对路径、字节数和SHA-256；不是本轮Agent实机测试，也不把缺少完整Effect定义的片段作为完整可运行示例。

## Fire's Edge 补充

`.battle_start_effect_ids` 为新增模式字段，战斗开始时对单位调用 Effect，至多 8 个 ID。

知识库编写者术语约定：说某个模式“可以带出战斗”，就是指该 `mode:` 写有 `.is_raid_default true`。这句话不等于该模式只在战斗中存在，也不等于任意模式切换都能让它带出战斗；实际仍需结合英雄/怪物侧和战斗外模型边界核对。

`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\heroes\duelist\duelist.info.darkest:67`

```darkest
mode: .id stance_defensive .is_raid_default true .battle_start_effect_ids "Duelist Combat Start Riposte" "Duelist Combat Start Debuff"
```

## 官方实例

`DarkestDungeon\dlc\4964110_fires_edge\features\duelist\heroes\duelist\duelist.info.darkest:67`

```darkest
mode: .id stance_defensive .is_raid_default true .battle_start_effect_ids "Duelist Combat Start Riposte" "Duelist Combat Start Debuff"
```

`DarkestDungeon\heroes\abomination\abomination.info.darkest:57`

```darkest
mode: .id beast .bark_override_id str_beast_bark .affliction_combat_skill_id transform .battle_complete_combat_skill_id transform .stress_damage_per_turn 6
```

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\statue_shield\statue_shield_A\statue_shield_A.info.darkest:14`

```darkest
mode: .id onscreen .is_raid_default true .always_guard_actor_base_class_ids statue_head
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
