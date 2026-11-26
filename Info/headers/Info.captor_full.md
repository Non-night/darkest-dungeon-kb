# `captor_full:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：定义捕获者的满载形态、释放条件和持续伤害。
- **官方实例分布**：怪物 66 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.captor_empty_monster_class` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.release_on_death` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.release_on_prisoner_at_deaths_door` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.release_on_prisoner_affliction` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.switch_class_on_death` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.release_effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 怪物特有。 | 捕获者释放被捕获英雄时调用的 Effect ID 列表。同一怪物 Info 内可将其他 `captor_full:` 字段和 `.release_effects` 分开写，也可在多个 `captor_full:` 行重复写 `.release_effects`，各行列表会追加。最终列表容量、重复 ID 和跨行执行顺序待测。Abigail Williams 实例中，`KadathFull` 自杀后变为 `KadathEmpty_G` 并释放英雄，随后 `.queue true` 的释放 Effect `AW_KF_Clear` 按 `KadathEmpty` 类型杀掉空容器；这个时序结论限定于该 Effect 的实际结算。 | 静态合法字段表、Cathelia 的 Abigail Williams 案例、截图与知识库编写者于 2026-11-25 的实测确认；Sources/captor_release_effects_20261125.json、游戏本体/官方 DLC 实例 |
| `.per_turn_damage_percent` | 一个数字，支持小数及百分号 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.per_turn_stress_damage` | 一个数字，支持小数及百分号 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.has_prisoner_overlay` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.unique_first_action_sfx` | 布尔值：`true` 或 `false`；这将变更/char/enemy/%s_captor_full_action为/char/enemy/%s_captor_full_action_first | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.reset_hp` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.use_previous_monster_class_hp` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.add_current_hp` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.use_bark_offset` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\pyre_full\pyre_full_A\pyre_full_A.info.darkest:10`

```darkest
captor_full: .captor_empty_monster_class pyre_empty_A .release_on_death true .release_on_prisoner_at_deaths_door true .per_turn_damage_percent 0.06 .reset_hp False .use_previous_monster_class_hp True .add_current_hp True
```

`DarkestDungeon\monsters\drowned_anchored\drowned_anchored_A\drowned_anchored_A.info.darkest:10`

```darkest
captor_full: .switch_class_on_death false .captor_empty_monster_class drowned_anchor_A .release_on_death true .release_on_prisoner_at_deaths_door false .release_on_prisoner_affliction true .release_effects "unimmobilize" .per_turn_damage_percent 0 .per_turn_stress_damage 6
```

`DarkestDungeon\monsters\drowned_anchored\drowned_anchored_A\drowned_anchored_A.art.darkest:3`

```darkest
captor_full: .has_prisoner_overlay true
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
