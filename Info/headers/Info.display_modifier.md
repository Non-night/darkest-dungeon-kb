# `display_modifier:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄/怪物通用 Header；不能仅依据当前官方实例分布把它判为单侧专用。
- **用途**：控制单位战斗显示、飘字、血条、光环和出生特效等表现。
- **官方实例分布**：怪物 52 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.disable_halos` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.disabled_popup_text_types` | 固定候选：`actor_dot_complete`、`pass`、`hp_heal_dot_onset`、`hp_heal_dot`、`hp_heal_dot_crit`、`miss`、`no_damage`、`crit_damage`、`damage`、`death_avoided`、`deathblow`、`hero_heal`、`hero_heal_crit`、`monster_heal`、`monster_heal_crit`、`stress_reduce`、`stress_damage`、`resist`、`move_resist`、`disease_resist`、`buff`、`debuff`、`debuff_resist`、`stun`、`stun_resist`、`stun_clear`、`poison`、`poison_resist`、`bleed`、`bleed_resist`、`cured`、`cure_failed`、`tagged`、`guard`、`guard_failed`、`riposte`、`full`、`heart_attack`、`heal_failed`、`vampire`、`vampire_resist`、`stress_dot`、`stress_dot_resist`、`shuffle_dot`、`shuffle_dot_resist`、`health_damage_block_onset`、`health_damage_block`、`tag_block`、`damage_reflect`、`control_resist`、`refresh_skills`、`daze`、`daze_resist`、`guard_break`；后跟最多54个选项 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 隐藏该单位作为受术者时，对应类型的战斗结算 pop。多个参数同时生效；英雄与怪物行为一致。它只改变演出，不改变实际判定或抗性。隐藏范围不只文字，还会一并去掉该 pop 相关的音效、结算时间延迟等表现流程。例如填写 `disease_resist debuff_resist` 后，该单位受到疾病或减益并成功抵抗时，不再播放相应抵抗 pop。该设置没有来源区分，因此为隐藏筛选逻辑门产生的抵抗提示，也会同时隐藏正常技能造成的同类抵抗提示。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.use_centre_skill_announcement` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.disable_health` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.anim_override` | 后跟最多32字符；字符串参数至多 1 个；每个至多 32 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.show_spawn_fx` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\735730_color_of_madness\monsters\corpse_crystal\corpse_crystal_A\corpse_crystal_A.art.darkest:5`

```darkest
display_modifier: .disable_halos true .show_spawn_fx false .disabled_popup_text_types resist
```

`DarkestDungeon\monsters\ancestor_heart\ancestor_heart_D\ancestor_heart_D.art.darkest:8`

```darkest
display_modifier: .use_centre_skill_announcement true .show_spawn_fx false
```

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\curtain\curtain_A\curtain_A.art.darkest:3`

```darkest
display_modifier: .disable_health True
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
