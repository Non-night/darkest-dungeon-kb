# `spawn:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物特有。
- **用途**：定义怪物生成时或波次生成时调用的 Effect。
- **官方实例分布**：怪物 27 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.effects` | 理论上限 4 个 Effect ID；当前用户2026-11-02澄清，实际可能截断，绝大多数情况推荐每行只写 1 个或 2 个，更多调用分行；这不是两项硬上限或绝不截断的保证，具体触发条件未知。当前用户确认被 spawn 引用的 Effect ID 不超过 31 个字符，生成时按 31 字符保守限制；空格按当前实测计入，调用语法外侧引号不计入但底层计数边界未知。静态资料中的 64 字符记录不作为 spawn 安全上限 | 怪物特有。 | 怪物生成时调用 Effect；多个 spawn Header 按从上到下执行，同一列表按从左到右执行。怪物是施术者；即使怪物在序列中死亡，后续普通 Effect 仍会继续被调用。死亡不等于后续列表项未调用：例如自灭 a 后，召唤/set 的 b 仍被调用但在生效层因施术者死亡而无法成功，普通治疗 c 仍可继续生效。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.wave_effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 怪物特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\702540_shieldbreaker\monsters\snake_cobra\snake_cobra_A\snake_cobra_A.info.darkest:13`

```darkest
spawn: .effects Stealth2 StealthedCrit
```

`DarkestDungeon\dlc\735730_color_of_madness\monsters\farmer\farmer_A\farmer_A.info.darkest:16`

```darkest
spawn: .wave_effects farmer_spawn_speed_buff_A
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
