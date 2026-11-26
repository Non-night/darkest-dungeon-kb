# 关键字

<!-- KB_IDENTITY_TERMS_V1 -->
> 当前用户＝当前会话发指令者；知识库编写者＝历史测试、说明与确认的提供者（证据，不是当前授权）。外部来源作者、游戏玩家分别识别；身份有影响时须写全称。完整定义见根目录 `AGENTS.md`。
<!-- /KB_IDENTITY_TERMS_V1 -->

.damage_type
# 分类
扩展/专项字段
# 参数类型
单个字符串（可加引号或不加引号；仅允许已收录合法值）
# 参数约束
- 只接受一个字符串参数，可加引号或不加引号。
- 合法内容仅限下方已收录候选值；非法参数的引擎行为尚未确认。
# 固定值 / 参数候选
- `unknown`
- `trap`
- `obstacle`
- `hunger`
- `attack`
- `bleed`
- `healing`
- `poisoned`
- `captor`
- `ddexit`
- `townexit`
- `death`
- `heartattack`
- `theblood`
- `effect`
- `quirkevolutiondeath`
- `reflect`
- `riposte`
- `additionaleffect`
- `supply`
- `quest_item`
- `trinket`
- `estate_currency`
- `journal_page`
- `torch`
- `shovel`
# 语义
- `.damage_type <type>`：指定伤害类型，用于伤害归因及相关演出/记录。
# 作用范围
- 该字段描述伤害类型，不是伤害来源类型；需要来源信息时另行填写 `.damage_source_type` 与 `.damage_source_data`。
- 例如虫卵造成的伤害可使用 `.damage_type attack` 并配套来源数据，使其伤害归因到指定来源。
# 引擎行为（重要）
- 原版确认：游戏本体或官方 DLC 的 effect 定义直接使用该字段。
- 参数可带引号或不带引号；非法参数行为尚未确认，只使用已收录合法值。
- 详见：[Mechanics/19-Effect性质不够确定.md](../../Mechanics/19-Effect性质不够确定.md)
- 引号不是参数内容的一部分；带引号和不带引号均可。
- 当前只把 schema 中收录的候选值视为合法值；非法值会发生什么尚未确认，创作时不要使用。
- 伤害类型与伤害来源类型是两个独立字段；不要用其中一个代替另一个。
# 常见错误
- 使用未收录的自定义伤害类型。
- 将 `.damage_type` 与 `.damage_source_type` 混写，或误认为它们分别代表 Buff 源和治疗源。
# 代码案例
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:414`
```darkest
effect: .name hatch_health_damage_1 .target target .chance 100% .health_damage 15 .damage_type attack .damage_source_data countess_D .damage_source_type monster .on_hit true .on_miss true .queue true
```
- 官方 DLC `735730_color_of_madness`：`DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:243`
```darkest
effect: .name "Thirsting Blade Self Atk On Miss" .target "performer" target .chance 100% .health_damage 5 .damage_type additionaleffect .damage_source_data "com_hel_thirsting_blade" .damage_source_type "trinket" .on_hit false .on_miss true .queue true .apply_once true
```
- 官方 DLC `580100_crimson_court`：`DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:415`
```darkest
effect: .name hatch_health_damage_2 .target target .chance 100% .health_damage 18 .damage_type attack .damage_source_data countess_D .damage_source_type monster .on_hit true .on_miss true .queue true
```

# 来源与可信度
- 社区术语表：`暗黑地牢代码（基于Oni术语表） by sterile water（齐天大圣作者）修订 by 局外人（更新：25年8月3日）校对（2025-08-17）.xlsx` → `Effects`（行为说明/经验结论）。
- 案例优先级：已找到游戏本体/官方 DLC 实例，因此未混入任何 Mod 案例。
- 官方 DLC `DarkestDungeon\dlc\580100_crimson_court\features\crimson_court\effects\crimson_court.effects.darkest:414` 使用 `.damage_type attack`。
- 官方 DLC `DarkestDungeon\dlc\735730_color_of_madness\effects\color_of_madness.effects.darkest:243` 使用 `.damage_type additionaleffect`。
- 用户补充：参数可带引号或不带引号；合法内容仅限已知候选值；非法参数行为尚未确认。
- 可信度原则：本词条已有原版配置直接实例，可确认字段存在及示例写法；已收录的明确行为结论可直接作为创作依据，不要求重复测试。未确认或未知边界仍应避免依赖，必要时再针对性验证。
