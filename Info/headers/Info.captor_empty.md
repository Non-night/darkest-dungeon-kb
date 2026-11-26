# `captor_empty:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：定义捕获者的空载形态及捕获流程。
- **官方实例分布**：怪物 27 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.performing_monster_captor_base_class` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.captor_full_monster_class` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.capture_effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.reset_hp` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.count_captor_full_damage` | 布尔值：`true` 或 `false` | 怪物特有。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\monsters\pyre_empty\pyre_empty_A\pyre_empty_A.info.darkest:10`

```darkest
captor_empty: .performing_monster_captor_base_class fanatic .captor_full_monster_class pyre_full_A .reset_hp False .count_captor_full_damage true
```

`DarkestDungeon\monsters\drowned_anchor\drowned_anchor_A\drowned_anchor_A.info.darkest:12`

```darkest
captor_empty: .performing_monster_captor_base_class drowned_anchor .captor_full_monster_class drowned_anchored_A .capture_effects "immobilize"
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
