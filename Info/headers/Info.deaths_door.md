# `deaths_door:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄进入死门、离开死门及心脏病恢复时的 Buff/Effect。
- **官方实例分布**：英雄 62 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.buffs` | 后跟最多8个buff id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 英雄生命降到 0 并进入死门时获得的 Buff。与普通死门恢复、心衰恢复 Buff 互斥，不叠层。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.recovery_buffs` | 后跟最多8个buff id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 英雄通过普通治疗从死门恢复到正生命时获得；进入死门时的 Buff 同时消失。三类死门相关 Buff 至多存在一种。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.recovery_heart_attack_buffs` | 后跟最多8个buff id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 英雄因心衰进入死门后，再由治疗恢复到正生命时获得。与死门 Buff、普通恢复 Buff 互斥，不叠层。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.enter_effects` | 后跟最多8个effect id，每个不超过64个字符；字符串参数至多 8 个；每个至多 64 字符 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.enter_effect_round_cooldown` | 一个数字 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:52`

```darkest
deaths_door: .buffs deathsdoorACCDebuff deathsdoorDMGLowDebuff deathsdoorDMGHighDebuff deathsdoorSPDDebuff deathsdoorSRDebuff .recovery_buffs mortalityACCDebuff mortalityDMGLowDebuff mortalityDMGHighDebuff mortalitySPDDebuff mortalitySRDebuff .recovery_heart_attack_buffs heartattackACCDebuff heartattackDMGLowDebuff heartattackDMGHighDebuff heartattackSPDDebuff heartattackSRDebuff
```

`DarkestDungeon\dlc\580100_crimson_court\features\flagellant\heroes\flagellant\flagellant.info.darkest:53`

```darkest
deaths_door: .buffs FdeathsdoorACCbuff FdeathsdoorDMGLowBuff FdeathsdoorDMGHighBuff FdeathsdoorSPDBuff FdeathsdoorSTUNRESISTBuff FdeathsdoorBLIGHTRESISTBuff FdeathsdoorBLEEDRESISTBuff FdeathsdoorDEBUFFRESISTBuff .recovery_buffs .recovery_heart_attack_buffs heartattackACCDebuff heartattackDMGLowDebuff heartattackDMGHighDebuff heartattackSPDDebuff heartattackSRDebuff .enter_effects flagellant_death_door_enter .enter_effect_round_cooldown 1
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
