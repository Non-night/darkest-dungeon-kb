# `overstressed_modifier:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：覆盖英雄爆压时可抽取的美德/折磨及概率。
- **官方实例分布**：英雄 2 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.override_trait_type_ids` | 后跟最多8个什么东西的 id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 【什么东西的 id】：美德折磨名称 包括自定义的 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.override_trait_type_chances` | 八个数字，支持小数；参数至多 8 个 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\heroes\flagellant\flagellant.info.darkest:57`

```darkest
overstressed_modifier: .override_trait_type_ids berserk .override_trait_type_chances 1.0
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
