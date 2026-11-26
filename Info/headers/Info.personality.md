# `personality:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：配置怪物的 personality 参数；当前只确认 `.prefskill` 是合法数字字段，具体用途未知。
- **官方实例分布**：怪物 383 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.prefskill` | 一个数字，大于0将会自减1 | 怪物特有。 | 具体用途未知。当前只确认它是怪物侧的合法数字字段，且静态参数资料记载大于 0 的输入会在内部减 1；不能据字段名断言它一定表示技能偏好，也不能断言 `-1` 表示无偏好、禁用选择或 Size 0 占位值。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\modes\bloodmoon\monsters\brigand_sapper\brigand_sapper_D\brigand_sapper_D.info.darkest:9`

```darkest
personality: .prefskill -1
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
