# `shape_shifter:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：定义怪物按轮次在多个 class 之间变形。
- **官方实例分布**：怪物 84 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.monster_class_ids` | 后跟最多4个class id，每个不超过32个字符；字符串参数至多 4 个；每个至多 32 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.monster_class_chances` | 四个数字，支持小数；参数至多 4 个 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.monster_class_valid_ranks` | 支持‘~’及数字 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.round_frequency` | 一个数字 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.fx_name` | 后跟最多128字符；字符串参数至多 1 个；每个至多 128 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\monsters\formless_guard\formless_guard_A\formless_guard_A.info.darkest:11`

```darkest
shape_shifter: .monster_class_ids formless_melee_A formless_weak_A formless_ranged_A .monster_class_chances 1 1 1 .monster_class_valid_ranks 12 1234 34 .round_frequency 1
```

`DarkestDungeon\monsters\formless_guard\formless_guard_A\formless_guard_A.art.darkest:3`

```darkest
shape_shifter: .fx_name "fx/formless_mutate/formless_mutate.sprite.skel"
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
