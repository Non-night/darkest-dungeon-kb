# `initiative:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。
- **用途**：定义怪物每轮行动点数量及行动提示显示；英雄职业 Mod 的 corpse 等特殊怪物实体也可使用。
- **官方实例分布**：怪物 395 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.number_of_turns_per_round` | 一个数字 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 怪物每个整轮获得的行动点数量。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.hide_indicator` | 布尔值：`true` 或 `false` | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\modes\bloodmoon\monsters\brigand_sapper\brigand_sapper_D\brigand_sapper_D.info.darkest:12`

```darkest
initiative: .number_of_turns_per_round 2
```

`DarkestDungeon\monsters\formless_guard\formless_guard_A\formless_guard_A.info.darkest:7`

```darkest
initiative: .number_of_turns_per_round 1 .hide_indicator true
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
