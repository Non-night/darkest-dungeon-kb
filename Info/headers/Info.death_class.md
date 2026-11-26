# `death_class:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。
- **用途**：定义怪物死亡变身/尸体 class 及其触发条件；英雄职业 Mod 中仅用于 corpse 等特殊怪物实体。
- **官方实例分布**：怪物 598 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.monster_class_id` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.random_monster_class_ids` | 后跟最多4个class id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.random_monster_class_chances` | 四个数字，支持小数；参数至多 4 个 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.use_previous_monster_hp` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_on_bleed_dot` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | true：流血伤害致死时允许执行该 death_class；false：不允许。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_on_blight_dot` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | true：腐蚀伤害致死时允许执行该 death_class；false：不允许。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_on_crit` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.reset_scale_anim` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.on_change_sfx` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.type` | 后跟最多32字符；字符串参数至多 1 个；每个至多 32 字符 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.can_die_from_damage` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.carry_over_hp_min_percent` | 一个数字，支持小数及百分号 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 为死亡转阶段时新形态继承的生命值设下限，以新形态最大生命的比例表示。原版 ancestor_pod_D → ancestor_heart_D 写 0.75，黑暗之心转阶段进场时的血量下限为最大生命的 75%。换算出现小数时的取整规则未知。四舍五入是知识库编写者的推测，待实测。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.clear_monster_brain_cooldowns` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.change_class_effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_on_burn_dot` | 布尔值：`true` 或 `false` | 怪物/尸体定义专用（Fire's Edge 新增） | 怪物专用。true：怪物因燃烧伤害死亡时允许执行该 death_class；false：燃烧死亡不启用该 death_class。 | 静态合法字段表、Fire's Edge 无夜译注表、游戏本体/官方 DLC 实例 |

## Fire's Edge 补充

`.is_valid_on_burn_dot` 为新增字段，明确属于怪物 death class；不能遗漏。

```darkest
death_class: .monster_class_id corpse_A .is_valid_on_bleed_dot true .is_valid_on_blight_dot true .is_valid_on_burn_dot true .is_valid_on_crit true
```

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\castellan\castellan_A\castellan_A.info.darkest:11`

```darkest
death_class: .monster_class_id corpse_A .is_valid_on_crit False .type "corpse"
```

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\curtain\curtain_E\curtain_E.info.darkest:12`

```darkest
death_class: .random_monster_class_ids sycophant_B tick_zombie_B .random_monster_class_chances 1.0 1.0 .is_valid_on_crit True .is_valid_on_bleed_dot True .is_valid_on_blight_dot True .is_valid_on_burn_dot True .reset_scale_anim true .on_change_sfx true
```

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\curtain\curtain_H\curtain_H.info.darkest:16`

```darkest
death_class: .monster_class_id baron_B .use_previous_monster_hp true .is_valid_on_bleed_dot true .is_valid_on_blight_dot true .is_valid_on_burn_dot true .is_valid_on_crit true .type baron .clear_monster_brain_cooldowns false .reset_scale_anim false .on_change_sfx true
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
