# `incompatible_party_member:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄的队伍不兼容 ID 或标签。
- **官方实例分布**：英雄 2 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.id` | 后跟最多32字符；字符串参数至多 1 个；每个至多 32 字符 | 英雄特有。 | 队伍不兼容组的内部 ID；独立语义尚未完全明确，常规按 `<hero_id>_limit` 命名并仿照原版。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.hero_tag` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 匹配不可同队目标英雄已有的 tag。常规把职业 ID 同时写为英雄 tag 和该参数。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\heroes\flagellant\flagellant.info.darkest:64`

```darkest
incompatible_party_member: .id flagellant_limit .hero_tag flagellant
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
