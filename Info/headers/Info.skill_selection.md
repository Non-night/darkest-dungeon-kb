# `skill_selection:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄可选战斗技能及最大装备数量。
- **官方实例分布**：英雄 40 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.can_select_combat_skills` | 布尔值：`true` 或 `false` | 英雄特有。 | true：允许玩家自由配置技能；false：强制携带全部技能，即使技能总数超过最大可选数也仍全部携带。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.number_of_selected_combat_skills_max` | 一个数字 | 英雄特有。 | 允许自由配置时的最大携带技能数。强制全技能时仍建议填写，且不小于技能总数。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:55`

```darkest
skill_selection: .can_select_combat_skills true .number_of_selected_combat_skills_max 4
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
