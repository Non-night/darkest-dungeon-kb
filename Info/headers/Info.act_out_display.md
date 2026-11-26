# `act_out_display:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄发生 act out 并攻击友方时使用的动画、FX 与音效。act out 不只来自折磨或美德，怪癖、疾病等系统也可以带出 act out；原版猩红诅咒系列即包含此类行为。
- **官方实例分布**：英雄 80 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.attack_friendly_anim` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 引用英雄 anim Skeleton 内部的友伤动画名，不是 `.skel` 文件名。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.attack_friendly_fx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 引用英雄 fx 或可用共用 FX Skeleton 内部的动画名，不是资源文件名。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.attack_friendly_targchestfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 引用目标胸口锚点播放的 FX 动画名；可来自职业 fx 或游戏全局共用 FX。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.attack_friendly_sfx` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 英雄发生 act out 并攻击友方时播放的对应音频事件。参数形如 `/char/ally/<事件名>`。这里的 act out 不只来自折磨或美德，怪癖、疾病等也可以带出 act out；原版猩红诅咒系列即存在相关行为。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.art.darkest:25`

```darkest
act_out_display: .attack_friendly_anim "attack_pistol" .attack_friendly_fx "sidearm" .attack_friendly_targchestfx "sidearm_target" .attack_friendly_sfx "/char/ally/musketeer_sidearm"
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
