# `enemy_type:`

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->


- **适用对象**：怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。
- **用途**：定义怪物类型 ID；英雄职业 Mod 的 corpse 等特殊怪物实体也可使用。一个怪物可以连续写多行 `enemy_type:`，因此可同时属于多个 enemy_type/种族；例如 `.id "aaa"` 与 `.id "bbb"` 表示同时属于 aaa 和 bbb。
- **官方实例分布**：怪物 463 次字段出现。
- **可用文件**：同一套 Header/字段语法可写入 `*.info.darkest`、`*.art.darkest`、`*.override.darkest`；具体放置仍应遵循对应单位文件结构。

## 可写字段

| 字段 | 参数形式 | 对象限制 | 含义/边界 | 证据 |
|---|---|---|---|---|
| `.id` | 后跟最多64字符；字符串参数至多 1 个；每个至多 64 字符 | 怪物定义专用；英雄职业 Mod 中仅用于 `corpse` 等特殊怪物实体，不属于普通英雄字段。 | 当前资料只确认该字段及其参数形式；具体引擎行为尚未确认。 | 静态合法字段表、游戏本体/官方 DLC 实例 |

## 多个 `enemy_type` 的原版案例

原版基础游戏的 Unclean Giant A 在同一个怪物定义中连续写出两行 `enemy_type:`：

`DarkestDungeon\monsters\unclean_giant\unclean_giant_A\unclean_giant_A.info.darkest:2-3`

```darkest
enemy_type: .id "man"
enemy_type: .id "beast"
```

这是原版数据中多行字段写法的直接实例。它本身证明的是原版怪物定义确实采用该结构；size-0 也适用多 `enemy_type` 的结论来自“size-0 首先是怪物”的通用规则与当前用户确认，并非此例是 size-0。

## 官方实例

`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\modes\bloodmoon\monsters\brigand_sapper\brigand_sapper_D\brigand_sapper_D.info.darkest:2`

```darkest
enemy_type: .id "man"
```

## 使用边界

- 字段被静态合法值表收录，只证明它是已知可写字段，不自动证明所有调用环境均有效。
- 表中写“尚未确认”的行为不得补造成确定结论。
- 布尔字段分别按 `true` 与 `false` 理解，不使用“1 or 0：效果”式含混描述。
- 百分号数字按百分之一解释，例如 `50%` 等于 `0.5`。
