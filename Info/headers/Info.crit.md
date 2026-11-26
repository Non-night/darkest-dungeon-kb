# `crit:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄/怪物通用 Header；不能仅依据当前官方实例分布把它判为单侧专用。
- **用途**：定义攻击技能暴击时附加调用的 Effect。
- **官方实例分布**：英雄 20 次字段出现、怪物 11 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.effects` | 后跟最多4个effect id，每个不超过64个字符；字符串参数至多 4 个；每个至多 64 字符 | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 单位使用攻击技能并造成暴击时调用所列 Effect。技能、饰品 Trigger 与暴击特效各自按 AWR、queue false、queue true 时序分组结算。 英雄调用时默认 target 是当前技能目标，可以正常指向敌方；迂回表 P800 的自身目标及不能指向敌方说法已由当前用户2026-11-03纠正。本次目标结论不推广到饰品 Trigger、怪物同名 Header 或全部特殊 target 参数。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.is_valid_effects_target` | 布尔值：`true` 或 `false` | 英雄/怪物通用；不能仅依据当前官方实例分布把它判为单侧专用。 | 布尔开关。`true` 表示启用，`false` 表示不启用；当前资料尚未补齐该开关的更具体引擎行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:2`

```darkest
crit: .effects "on_crit_dmgmarked"
```

`DarkestDungeon\dlc\735730_color_of_madness\monsters\corpse_crystal\corpse_crystal_A\corpse_crystal_A.info.darkest:15`

```darkest
crit: .is_valid_effects_target false
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
