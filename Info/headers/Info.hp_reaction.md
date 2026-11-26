# `hp_reaction:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄/怪物通用 Header；不能仅依据当前官方实例分布把它判为单侧专用。
- **用途**：按生命比例阈值触发 Effect。
- **官方实例分布**：英雄 3 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.hp_ratio` | 一个数字，支持小数 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 生命比例阈值；阈值为闭区间，等于该值时也满足对应方向。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_under` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | true：生命比例小于等于阈值时满足；false：生命比例大于等于阈值时满足。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 生命值变化后立即检查；条件满足时立即调用 Effect，可插入当前 spawn Effect 序列。该 Header 所属单位是 Effect 施术者。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\heroes\flagellant\flagellant.info.darkest:59`

```darkest
hp_reaction: .hp_ratio 0.40 .is_under true .effects flagellant_low_hp_reaction
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
