# `armour:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：英雄特有。
- **用途**：定义英雄各级护甲数据。
- **官方实例分布**：英雄 880 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.name` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 知识库编写者2026-10-28明确：英雄武器／护甲名称的本地化Entry ID直接取Info中对应weapon:／armour:的.name字符串，必须完全一致，不固定拼接职业ID。weapon: .name "SF_Ele_weapon_0" 对应Entry ID就是SF_Ele_weapon_0；SF_Ele在该例不是职业ID，不得替换为真实职业ID_weapon_0。原版<hero_id>_weapon_<level>或<hero_id>_armour_<level>只是.name常用命名，不是引擎强制拼接规则。通用格式应写<weapon.name>／<armour.name>；不改变图标路径或升级等级规则。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.def` | 一个数字，支持小数及百分号 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.prot` | 一个数字，支持小数及百分号 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.hp` | 一个数字，支持小数及百分号 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.spd` | 一个数字，支持小数及百分号 | 英雄特有。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.icon` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 英雄特有。 | 直接填写装备 PNG 文件名；对应英雄职业目录 `heroes/<hero_id>/icons_equip/<文件名>`。 | 静态合法字段表、游戏本体/官方 DLC 实例 |
| `.upgradeRequirementCode` | 一个字符 | 英雄特有。 | 应该用于将该级护甲关联到升级树中的升级要求编号。常规写法是代码等级 1 的护甲填写 `0`，代码等级 2 填写 `1`，依次类推；初始 0 级装备通常不写。该映射目前属于根据原版及 Mod 写法作出的推测，尚未专项验证，不得表述为完全确认的硬性规则。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 官方实例

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.art.darkest:9`

```darkest
armour: .name "musketeer_armour_0" .icon "eqp_armour_0.png"
```

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:8`

```darkest
armour: .name "musketeer_armour_0" .def 0% .prot 0 .hp 27 .spd 0
```

`DarkestDungeon\dlc\445700_musketeer\heroes\musketeer\musketeer.info.darkest:9`

```darkest
armour: .name "musketeer_armour_1" .def 5% .prot 0 .hp 32 .spd 0 .upgradeRequirementCode 0
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
