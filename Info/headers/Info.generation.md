# `generation:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄生成时的怪癖、技能、牌组和事件依赖。
- **官方实例分布**：英雄 204 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.is_generation_enabled` | 布尔值：`true` 或 `false` | 英雄特有。 | 控制该英雄职业能否进入常规刷新池。当前已知能够获得英雄的途径只有马车、城镇事件和监狱（原版猩红庭院秘门）：写 `true` 时该职业可以在马车和监狱中刷新；写 `false` 时该职业不能在马车或监狱中刷新，但仍可由事件直接给予。该字段还会连带控制职业饰品刷新：当其为 `false` 时，所有职业要求列表包含该职业的饰品都无法正常刷新。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_positive_quirks_min` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始正面怪癖数量随机区间的下限，并且包含该下限。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_positive_quirks_max` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始正面怪癖数量随机区间的上限，并且包含该上限；与 `.number_of_positive_quirks_min` 共同构成闭区间。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_negative_quirks_min` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始负面怪癖数量随机区间的下限，并且包含该下限。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_negative_quirks_max` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始负面怪癖数量随机区间的上限，并且包含该上限；与 `.number_of_negative_quirks_min` 共同构成闭区间。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_class_specific_camping_skills` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始随机解锁的职业专属扎营技能数量。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 知识库编写者确认（2026-09-20）：写 0 会在过周时产生红字 `HeroGeneration: Number of class specific camping skills is 0`，但不阻止英雄正常刷新。 详见 Mechanics/49-扎营技能文件、通用专属分类与图标.md。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_shared_camping_skills` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始随机解锁的通用扎营技能数量。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 知识库编写者确认（2026-09-20）：写 0 会在过周时产生红字 `HeroGeneration: Number of shared camping skills is 0`，但不阻止英雄正常刷新。 写大于 0 不会凭空提供通用技能：该英雄定义里不存在通用扎营技能时，仍不会出现通用技能；苦修是知识库编写者提供的例子，库内原版 generation 实例确有此字段为 1。 详见 Mechanics/49-扎营技能文件、通用专属分类与图标.md。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_random_combat_skills` | 一个数字 | 英雄特有。 | 英雄在马车中生成时，初始随机解锁的战斗技能数量。由 `.generation_guaranteed true` 保证携带的技能不计入这一随机数量。该字段对城镇事件直接给予的英雄和监狱中生成的英雄是否生效，目前未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_cards_in_deck` | 一个数字 | 英雄特有。 | 配置该职业在常规马车招募卡组中的牌数。原版关闭火枪手 DLC 时弩手为 6 张，开启后火枪手加入 3 张并扣减弩手 3 张。牌数与 `.card_chance` 分别如何作用、如何算出实际刷新概率及参数边界仍未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.card_chance` | 一个数字，支持小数及百分号 | 英雄特有。 | 常规马车招募中的卡牌配置参数。原版弩手与火枪手此值均为 `1.0`。已有调试经验是临时写极大值，重进游戏并过周观察该职业是否更快刷出。该字段的具体作用、它与 `.number_of_cards_in_deck` 的组合公式、数值上下限及负数和零值行为仍未明确。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.reduce_number_of_cards_in_deck_hero_class_id` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 指定要在常规马车招募卡组中减去牌数的职业 ID，减去多少张由 `.reduce_number_of_cards_in_deck_amount` 指定。原版火枪手在此写 `arbalest`。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.reduce_number_of_cards_in_deck_amount` | 一个数字 | 英雄特有。 | 将 `.reduce_number_of_cards_in_deck_hero_class_id` 所指定职业的马车招募牌数减少该数值。原版火枪手指定弩手并写 `3`，所以关闭火枪手 DLC 时弩手 6 张，开启后弩手 3 张、火枪手 3 张，两者的 `.card_chance` 均为 `1.0`。据知识库编写者 2026-11-21 说明，同等条件下开启火枪手 DLC 后常规马车抽到火枪手或弩手的合计刷新概率，等于关闭时抽到弩手的概率。两参数的抽取机制与边界仍未知。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.town_event_dependency` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 指定事件发生后才允许该英雄在马车中自然刷新。若英雄被设计为仅能通过事件获得，本参数必须指向不存在或永不发生的事件 ID；不得引用负责赠送英雄的事件或任何会实际发生的既有事件，否则该事件发生后会解锁马车自然刷新。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:57`

```darkest
generation:  .is_generation_enabled false .number_of_positive_quirks_min 1 .number_of_positive_quirks_max 2 .number_of_negative_quirks_min 1 .number_of_negative_quirks_max 2 .number_of_class_specific_camping_skills 2 .number_of_shared_camping_skills 1 .number_of_random_combat_skills 4 .number_of_cards_in_deck 3 .card_chance 1.0 .reduce_number_of_cards_in_deck_hero_class_id arbalest .reduce_number_of_cards_in_deck_amount 3
```

`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\heroes\flagellant\flagellant.info.darkest:63`

```darkest
generation: .is_generation_enabled true .town_event_dependency "first_flagellant" .number_of_positive_quirks_min 1 .number_of_positive_quirks_max 2 .number_of_negative_quirks_min 1 .number_of_negative_quirks_max 2 .number_of_class_specific_camping_skills 2 .number_of_shared_camping_skills 1 .number_of_random_combat_skills 4 .number_of_cards_in_deck 6 .card_chance 1.0
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
